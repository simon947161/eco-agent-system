from pathlib import Path
from typing import Any

from .database import (
    SCHEMA_VERSION,
    UnsupportedSchemaVersionError,
    connect,
    get_schema_version,
    migrate_connection_to_latest,
)
from .maintenance import create_backup
from .repository import PrototypeRepository


def migration_preflight(db_path: str | Path) -> dict[str, Any]:
    with connect(db_path) as connection:
        current = get_schema_version(connection)
        try:
            pending = migrate_connection_to_latest(connection, dry_run=True)
        except UnsupportedSchemaVersionError as exc:
            return {
                "status": "unsupported",
                "current_version": current,
                "target_version": SCHEMA_VERSION,
                "pending": [],
                "error": str(exc),
            }
    status = "ready" if current <= SCHEMA_VERSION else "unsupported"
    return {"status": status, "current_version": current, "target_version": SCHEMA_VERSION, "pending": pending}


def migrate_database(
    db_path: str | Path,
    dry_run: bool = False,
    backup_root: str | Path | None = None,
    actor_label: str = "local operator",
) -> dict[str, Any]:
    preflight = migration_preflight(db_path)
    if preflight["status"] == "unsupported":
        raise ValueError("Unsupported schema version.")
    if dry_run:
        return {**preflight, "status": "dry_run"}

    backup_result = create_backup(
        db_path,
        backup_root=backup_root or Path(db_path).parent / "migration_backups",
        label="pre-migration",
        actor_label=actor_label,
        audit=False,
    )
    with connect(db_path) as connection:
        pending = migrate_connection_to_latest(connection, dry_run=False)
        current = get_schema_version(connection)
    repository = PrototypeRepository(db_path)
    repository.audit(
        "migration_completed",
        "human_action",
        actor_label,
        None,
        {"from_version": preflight["current_version"], "to_version": current, "pending": pending},
    )
    return {
        "status": "migrated" if pending else "already_current",
        "from_version": preflight["current_version"],
        "to_version": current,
        "pending": pending,
        "backup": backup_result,
    }
