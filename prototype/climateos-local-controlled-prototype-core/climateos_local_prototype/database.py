import sqlite3
from collections.abc import Iterator
from contextlib import contextmanager
from pathlib import Path
from time import sleep

from .config import SQLITE_BUSY_TIMEOUT_MS

SCHEMA_VERSION = 3

SQLITE_LOCK_RETRY_DELAYS_SECONDS = (0.025, 0.05, 0.1)

REQUIRED_TABLES = {
    "schema_version",
    "candidate_records",
    "relationships",
    "human_reviews",
    "founder_gates",
    "audit_events",
    "model_suggestions",
    "archive_events",
    "alpha_evidence_contracts",
    "alpha_evidence_revisions",
    "alpha_audit_events",
    "alpha_deliberations",
}


class UnsupportedSchemaVersionError(ValueError):
    pass


class ClosingConnection(sqlite3.Connection):
    def __exit__(self, exc_type, exc_value, traceback) -> bool:
        try:
            return bool(super().__exit__(exc_type, exc_value, traceback))
        finally:
            self.close()


def connect(db_path: str | Path) -> sqlite3.Connection:
    path = Path(db_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    connection = sqlite3.connect(path, timeout=SQLITE_BUSY_TIMEOUT_MS / 1000, factory=ClosingConnection)
    connection.row_factory = sqlite3.Row
    connection.execute("PRAGMA foreign_keys = ON")
    connection.execute(f"PRAGMA busy_timeout = {SQLITE_BUSY_TIMEOUT_MS}")
    return connection


def _is_locked_error(error: sqlite3.OperationalError) -> bool:
    message = str(error).lower()
    return "database is locked" in message or "database table is locked" in message


def _begin_immediate(connection: sqlite3.Connection) -> None:
    for attempt in range(len(SQLITE_LOCK_RETRY_DELAYS_SECONDS) + 1):
        try:
            connection.execute("BEGIN IMMEDIATE")
            return
        except sqlite3.OperationalError as error:
            if not _is_locked_error(error) or attempt == len(SQLITE_LOCK_RETRY_DELAYS_SECONDS):
                raise
            sleep(SQLITE_LOCK_RETRY_DELAYS_SECONDS[attempt])


@contextmanager
def write_transaction(db_path: str | Path) -> Iterator[sqlite3.Connection]:
    """Acquire one bounded foreground writer and commit or roll back atomically."""

    connection = connect(db_path)
    try:
        _begin_immediate(connection)
        try:
            yield connection
        except BaseException:
            connection.rollback()
            raise
        else:
            connection.commit()
    finally:
        connection.close()


def _table_columns(connection: sqlite3.Connection, table_name: str) -> set[str]:
    return {row["name"] for row in connection.execute(f"PRAGMA table_info({table_name})")}


def get_schema_version(connection: sqlite3.Connection) -> int:
    table = connection.execute(
        "SELECT name FROM sqlite_master WHERE type = 'table' AND name = 'schema_version'"
    ).fetchone()
    if table is None:
        return 0
    row = connection.execute("SELECT MAX(version) AS version FROM schema_version").fetchone()
    return int(row["version"] or 0)


def set_schema_version(connection: sqlite3.Connection, version: int) -> None:
    connection.execute(
        "INSERT OR IGNORE INTO schema_version (version, applied_at) VALUES (?, datetime('now'))",
        (version,),
    )


def migrate_connection_to_latest(connection: sqlite3.Connection, dry_run: bool = False) -> list[str]:
    current = get_schema_version(connection)
    if current > SCHEMA_VERSION:
        raise UnsupportedSchemaVersionError(
            f"Database schema version {current} is newer than supported version {SCHEMA_VERSION}."
        )
    pending: list[str] = []
    if current < 2:
        pending.append("1->2 add audit sequencing and Founder Gate history fields")
        if not dry_run:
            audit_columns = _table_columns(connection, "audit_events")
            if "sequence_number" not in audit_columns:
                connection.execute("ALTER TABLE audit_events ADD COLUMN sequence_number INTEGER NOT NULL DEFAULT 0")
            if "operation_id" not in audit_columns:
                connection.execute("ALTER TABLE audit_events ADD COLUMN operation_id TEXT NOT NULL DEFAULT ''")

            founder_columns = _table_columns(connection, "founder_gates")
            if "supersedes_gate_id" not in founder_columns:
                connection.execute("ALTER TABLE founder_gates ADD COLUMN supersedes_gate_id TEXT NOT NULL DEFAULT ''")
            if "decision_version" not in founder_columns:
                connection.execute("ALTER TABLE founder_gates ADD COLUMN decision_version INTEGER NOT NULL DEFAULT 1")

            rows = connection.execute(
                "SELECT rowid FROM audit_events ORDER BY created_at, id"
            ).fetchall()
            for sequence, row in enumerate(rows, start=1):
                connection.execute(
                    "UPDATE audit_events SET sequence_number = ? WHERE rowid = ?",
                    (sequence, row["rowid"]),
                )
            set_schema_version(connection, 2)
    if current < 3:
        pending.append("2->3 add persistent Alpha Review Loop tables")
        if not dry_run:
            connection.executescript(
                """
                CREATE TABLE IF NOT EXISTS alpha_evidence_contracts (
                    id TEXT PRIMARY KEY,
                    domain TEXT NOT NULL,
                    state TEXT NOT NULL,
                    revision INTEGER NOT NULL,
                    record_json TEXT NOT NULL,
                    created_at TEXT NOT NULL,
                    updated_at TEXT NOT NULL
                );
                CREATE TABLE IF NOT EXISTS alpha_evidence_revisions (
                    evidence_id TEXT NOT NULL,
                    revision INTEGER NOT NULL,
                    snapshot_json TEXT NOT NULL,
                    created_at TEXT NOT NULL,
                    PRIMARY KEY (evidence_id, revision),
                    FOREIGN KEY (evidence_id) REFERENCES alpha_evidence_contracts(id)
                );
                CREATE TABLE IF NOT EXISTS alpha_audit_events (
                    sequence_number INTEGER PRIMARY KEY AUTOINCREMENT,
                    id TEXT NOT NULL UNIQUE,
                    event_type TEXT NOT NULL,
                    actor_label TEXT NOT NULL,
                    record_id TEXT NOT NULL,
                    detail_json TEXT NOT NULL,
                    created_at TEXT NOT NULL,
                    boundary_label TEXT NOT NULL
                );
                CREATE TABLE IF NOT EXISTS alpha_deliberations (
                    id TEXT PRIMARY KEY,
                    record_json TEXT NOT NULL,
                    created_at TEXT NOT NULL
                );
                CREATE INDEX IF NOT EXISTS idx_alpha_evidence_domain_state
                    ON alpha_evidence_contracts(domain, state);
                CREATE INDEX IF NOT EXISTS idx_alpha_audit_record
                    ON alpha_audit_events(record_id, sequence_number);
                """
            )
            set_schema_version(connection, 3)
    return pending


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
                supersedes_gate_id TEXT NOT NULL DEFAULT '',
                decision_version INTEGER NOT NULL DEFAULT 1,
                created_at TEXT NOT NULL
            );

            CREATE TABLE IF NOT EXISTS audit_events (
                id TEXT PRIMARY KEY,
                event_type TEXT NOT NULL,
                actor_type TEXT NOT NULL,
                actor_label TEXT NOT NULL,
                record_id TEXT,
                detail_json TEXT NOT NULL,
                sequence_number INTEGER NOT NULL DEFAULT 0,
                operation_id TEXT NOT NULL DEFAULT '',
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

            CREATE TABLE IF NOT EXISTS alpha_evidence_contracts (
                id TEXT PRIMARY KEY,
                domain TEXT NOT NULL,
                state TEXT NOT NULL,
                revision INTEGER NOT NULL,
                record_json TEXT NOT NULL,
                created_at TEXT NOT NULL,
                updated_at TEXT NOT NULL
            );

            CREATE TABLE IF NOT EXISTS alpha_evidence_revisions (
                evidence_id TEXT NOT NULL,
                revision INTEGER NOT NULL,
                snapshot_json TEXT NOT NULL,
                created_at TEXT NOT NULL,
                PRIMARY KEY (evidence_id, revision),
                FOREIGN KEY (evidence_id) REFERENCES alpha_evidence_contracts(id)
            );

            CREATE TABLE IF NOT EXISTS alpha_audit_events (
                sequence_number INTEGER PRIMARY KEY AUTOINCREMENT,
                id TEXT NOT NULL UNIQUE,
                event_type TEXT NOT NULL,
                actor_label TEXT NOT NULL,
                record_id TEXT NOT NULL,
                detail_json TEXT NOT NULL,
                created_at TEXT NOT NULL,
                boundary_label TEXT NOT NULL
            );

            CREATE TABLE IF NOT EXISTS alpha_deliberations (
                id TEXT PRIMARY KEY,
                record_json TEXT NOT NULL,
                created_at TEXT NOT NULL
            );

            CREATE INDEX IF NOT EXISTS idx_alpha_evidence_domain_state
                ON alpha_evidence_contracts(domain, state);
            CREATE INDEX IF NOT EXISTS idx_alpha_audit_record
                ON alpha_audit_events(record_id, sequence_number);
            """
        )
        current = get_schema_version(connection)
        if current == 0:
            audit_columns = _table_columns(connection, "audit_events")
            founder_columns = _table_columns(connection, "founder_gates")
            if "sequence_number" not in audit_columns or "supersedes_gate_id" not in founder_columns:
                set_schema_version(connection, 1)
                migrate_connection_to_latest(connection)
            else:
                set_schema_version(connection, SCHEMA_VERSION)
        else:
            migrate_connection_to_latest(connection)


def reset_database(db_path: str | Path) -> None:
    path = Path(db_path)
    if path.exists():
        path.unlink()
    initialize_database(path)
