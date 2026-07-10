import sqlite3
from pathlib import Path

from climateos_local_prototype.database import connect, get_schema_version
from climateos_local_prototype.diagnostics import run_data_integrity_diagnostics, safe_integrity_check
from climateos_local_prototype.maintenance import create_backup, restore_backup, validate_backup
from climateos_local_prototype.migrations import migrate_database, migration_preflight
from climateos_local_prototype.repository import PrototypeRepository
from climateos_local_prototype.seed import seed_database


def _seeded_db(path: Path) -> PrototypeRepository:
    repository = PrototypeRepository(path)
    seed_database(repository)
    return repository


def _create_v1_database(path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with sqlite3.connect(path) as connection:
        connection.executescript(
            """
            CREATE TABLE schema_version (
                version INTEGER PRIMARY KEY,
                applied_at TEXT NOT NULL
            );
            INSERT INTO schema_version (version, applied_at) VALUES (1, datetime('now'));

            CREATE TABLE candidate_records (
                id TEXT PRIMARY KEY,
                record_type TEXT NOT NULL,
                title TEXT NOT NULL,
                status TEXT NOT NULL,
                summary TEXT NOT NULL DEFAULT '',
                source_ids TEXT NOT NULL DEFAULT '[]',
                signal_ids TEXT NOT NULL DEFAULT '[]',
                claim_ids TEXT NOT NULL DEFAULT '[]',
                knowledge_object_ids TEXT NOT NULL DEFAULT '[]',
                evidence_ids TEXT NOT NULL DEFAULT '[]',
                readiness_label TEXT NOT NULL,
                risk_flags TEXT NOT NULL DEFAULT '[]',
                human_review_need TEXT NOT NULL DEFAULT '',
                founder_gate_need TEXT NOT NULL DEFAULT '',
                boundary_label TEXT NOT NULL,
                created_at TEXT NOT NULL,
                updated_at TEXT NOT NULL,
                archived_at TEXT
            );

            CREATE TABLE relationships (
                id TEXT PRIMARY KEY,
                from_record_id TEXT NOT NULL,
                to_record_id TEXT NOT NULL,
                relationship_type TEXT NOT NULL,
                created_by TEXT NOT NULL,
                reason TEXT NOT NULL,
                created_at TEXT NOT NULL
            );

            CREATE TABLE human_reviews (
                id TEXT PRIMARY KEY,
                record_id TEXT NOT NULL,
                previous_status TEXT NOT NULL,
                new_status TEXT NOT NULL,
                reviewer_label TEXT NOT NULL,
                review_reason TEXT NOT NULL,
                linked_risk_flags TEXT NOT NULL DEFAULT '[]',
                founder_gate_trigger TEXT NOT NULL DEFAULT '',
                created_at TEXT NOT NULL
            );

            CREATE TABLE founder_gates (
                id TEXT PRIMARY KEY,
                gate_trigger TEXT NOT NULL,
                affected_record_ids TEXT NOT NULL DEFAULT '[]',
                decision_date TEXT NOT NULL,
                decision_status TEXT NOT NULL,
                founder_instruction_text TEXT NOT NULL,
                scope_allowed TEXT NOT NULL DEFAULT '',
                scope_prohibited TEXT NOT NULL DEFAULT '',
                review_or_expiry_requirement TEXT NOT NULL DEFAULT '',
                archive_reference TEXT NOT NULL DEFAULT '',
                created_at TEXT NOT NULL
            );

            CREATE TABLE audit_events (
                id TEXT PRIMARY KEY,
                event_type TEXT NOT NULL,
                actor_type TEXT NOT NULL,
                actor_label TEXT NOT NULL,
                record_id TEXT,
                detail_json TEXT NOT NULL,
                created_at TEXT NOT NULL
            );

            CREATE TABLE model_suggestions (
                id TEXT PRIMARY KEY,
                response_id TEXT NOT NULL,
                category TEXT NOT NULL,
                target_record_id TEXT NOT NULL DEFAULT '',
                suggestion_text TEXT NOT NULL,
                provenance TEXT NOT NULL,
                disposition TEXT NOT NULL DEFAULT 'pending',
                reviewer_label TEXT NOT NULL DEFAULT '',
                disposition_reason TEXT NOT NULL DEFAULT '',
                created_at TEXT NOT NULL,
                decided_at TEXT
            );

            CREATE TABLE archive_events (
                id TEXT PRIMARY KEY,
                case_id TEXT NOT NULL,
                export_path TEXT NOT NULL,
                reviewer_label TEXT NOT NULL,
                reason TEXT NOT NULL,
                created_at TEXT NOT NULL
            );
            """
        )


def test_manual_backup_validate_restore_and_checksum(tmp_path):
    source = tmp_path / "source.sqlite3"
    _seeded_db(source)

    backup = create_backup(source, backup_root=tmp_path / "backups", label="manual-test")
    backup_dir = Path(backup["backup_dir"])
    assert (backup_dir / "database.sqlite3").exists()
    assert (backup_dir / "backup-manifest.json").exists()
    assert backup["manifest"]["integrity_check"]["status"] == "healthy"

    validation = validate_backup(backup_dir)
    assert validation["status"] == "healthy"

    restored = tmp_path / "restored.sqlite3"
    restore = restore_backup(backup_dir, restored, actor_label="Reviewer A")
    assert restore["status"] == "restored"
    assert len(PrototypeRepository(restored).list_candidates()) == 5

    (backup_dir / "database.sqlite3").write_bytes(b"not a sqlite database")
    assert validate_backup(backup_dir)["status"] == "failed"


def test_restore_refuses_invalid_backup_and_preserves_existing_database(tmp_path):
    target = tmp_path / "target.sqlite3"
    _seeded_db(target)
    backup = create_backup(target, backup_root=tmp_path / "backups", label="restore-test")
    backup_dir = Path(backup["backup_dir"])
    (backup_dir / "database.sqlite3").write_bytes(b"corrupt")

    try:
        restore_backup(backup_dir, target, actor_label="Reviewer A")
    except ValueError as exc:
        assert "checksum" in str(exc).lower()
    else:
        raise AssertionError("Restore should reject a corrupt backup.")

    assert safe_integrity_check(target)["status"] == "healthy"
    assert len(PrototypeRepository(target).list_candidates()) == 5


def test_integrity_diagnostics_detect_invalid_status(tmp_path):
    db_path = tmp_path / "diagnostics.sqlite3"
    _seeded_db(db_path)
    assert safe_integrity_check(db_path)["status"] == "healthy"
    assert run_data_integrity_diagnostics(db_path)["status"] == "healthy"

    with connect(db_path) as connection:
        connection.execute("UPDATE candidate_records SET status = 'Certified' WHERE id = 'S001'")

    diagnostics = run_data_integrity_diagnostics(db_path)
    assert diagnostics["status"] == "failed"
    assert any(issue["kind"] == "invalid_status" for issue in diagnostics["issues"])


def test_migration_preflight_dry_run_and_apply_from_v1(tmp_path):
    db_path = tmp_path / "v1.sqlite3"
    _create_v1_database(db_path)

    preflight = migration_preflight(db_path)
    assert preflight["status"] == "ready"
    assert preflight["current_version"] == 1
    assert preflight["pending"]

    dry_run = migrate_database(db_path, dry_run=True)
    assert dry_run["status"] == "dry_run"
    with connect(db_path) as connection:
        assert "sequence_number" not in {row["name"] for row in connection.execute("PRAGMA table_info(audit_events)")}

    migrated = migrate_database(db_path, backup_root=tmp_path / "migration_backups", actor_label="Reviewer A")
    assert migrated["status"] == "migrated"
    with connect(db_path) as connection:
        assert get_schema_version(connection) == 2
        assert "sequence_number" in {row["name"] for row in connection.execute("PRAGMA table_info(audit_events)")}
        assert "supersedes_gate_id" in {row["name"] for row in connection.execute("PRAGMA table_info(founder_gates)")}


def test_unsupported_schema_version_is_deferred(tmp_path):
    db_path = tmp_path / "future.sqlite3"
    with sqlite3.connect(db_path) as connection:
        connection.execute("CREATE TABLE schema_version (version INTEGER PRIMARY KEY, applied_at TEXT NOT NULL)")
        connection.execute("INSERT INTO schema_version (version, applied_at) VALUES (99, datetime('now'))")

    preflight = migration_preflight(db_path)
    assert preflight["status"] == "unsupported"
    assert preflight["current_version"] == 99
