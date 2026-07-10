import sqlite3
from pathlib import Path

SCHEMA_VERSION = 1


def connect(db_path: str | Path) -> sqlite3.Connection:
    path = Path(db_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    connection = sqlite3.connect(path)
    connection.row_factory = sqlite3.Row
    connection.execute("PRAGMA foreign_keys = ON")
    return connection


def initialize_database(db_path: str | Path) -> None:
    with connect(db_path) as connection:
        connection.executescript(
            """
            CREATE TABLE IF NOT EXISTS schema_version (
                version INTEGER PRIMARY KEY,
                applied_at TEXT NOT NULL
            );

            CREATE TABLE IF NOT EXISTS candidate_records (
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

            CREATE TABLE IF NOT EXISTS relationships (
                id TEXT PRIMARY KEY,
                from_record_id TEXT NOT NULL,
                to_record_id TEXT NOT NULL,
                relationship_type TEXT NOT NULL,
                created_by TEXT NOT NULL,
                reason TEXT NOT NULL,
                created_at TEXT NOT NULL,
                FOREIGN KEY (from_record_id) REFERENCES candidate_records(id),
                FOREIGN KEY (to_record_id) REFERENCES candidate_records(id)
            );

            CREATE TABLE IF NOT EXISTS human_reviews (
                id TEXT PRIMARY KEY,
                record_id TEXT NOT NULL,
                previous_status TEXT NOT NULL,
                new_status TEXT NOT NULL,
                reviewer_label TEXT NOT NULL,
                review_reason TEXT NOT NULL,
                linked_risk_flags TEXT NOT NULL DEFAULT '[]',
                founder_gate_trigger TEXT NOT NULL DEFAULT '',
                created_at TEXT NOT NULL,
                FOREIGN KEY (record_id) REFERENCES candidate_records(id)
            );

            CREATE TABLE IF NOT EXISTS founder_gates (
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

            CREATE TABLE IF NOT EXISTS audit_events (
                id TEXT PRIMARY KEY,
                event_type TEXT NOT NULL,
                actor_type TEXT NOT NULL,
                actor_label TEXT NOT NULL,
                record_id TEXT,
                detail_json TEXT NOT NULL,
                created_at TEXT NOT NULL
            );

            CREATE TABLE IF NOT EXISTS model_suggestions (
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

            CREATE TABLE IF NOT EXISTS archive_events (
                id TEXT PRIMARY KEY,
                case_id TEXT NOT NULL,
                export_path TEXT NOT NULL,
                reviewer_label TEXT NOT NULL,
                reason TEXT NOT NULL,
                created_at TEXT NOT NULL
            );
            """
        )
        connection.execute(
            "INSERT OR IGNORE INTO schema_version (version, applied_at) VALUES (?, datetime('now'))",
            (SCHEMA_VERSION,),
        )


def reset_database(db_path: str | Path) -> None:
    path = Path(db_path)
    if path.exists():
        path.unlink()
    initialize_database(path)
