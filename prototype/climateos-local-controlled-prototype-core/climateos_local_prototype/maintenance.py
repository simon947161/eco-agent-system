import hashlib
import json
import re
import shutil
import sqlite3
from pathlib import Path
from typing import Any

from .config import LOCAL_BACKUP_DIR
from .database import SCHEMA_VERSION, connect
from .diagnostics import safe_integrity_check
from .repository import PrototypeRepository, new_id, now_iso


def _safe_label(value: str) -> str:
    if not re.fullmatch(r"[A-Za-z0-9_.-]+", value):
        raise ValueError("Labels may contain only letters, numbers, underscore, dash, and dot.")
    if ".." in value or "/" in value or "\\" in value or re.match(r"^[A-Za-z]:", value):
        raise ValueError("Labels must not contain path traversal, separators, or drive prefixes.")
    return value


def _safe_child(root: Path, child_name: str) -> Path:
    resolved_root = root.resolve()
    resolved_child = (resolved_root / child_name).resolve()
    resolved_child.relative_to(resolved_root)
    return resolved_child


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _write_json(path: Path, payload: Any) -> None:
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=True) + "\n", encoding="utf-8")


def create_backup(
    db_path: str | Path,
    backup_root: str | Path = LOCAL_BACKUP_DIR,
    label: str = "manual",
    actor_label: str = "local operator",
    audit: bool = True,
) -> dict[str, Any]:
    source = Path(db_path)
    if not source.exists():
        raise FileNotFoundError(f"Source database does not exist: {source}")
    safe_label = _safe_label(label)
    repository = PrototypeRepository(source) if audit else None
    if repository is not None:
        repository.audit("backup_started", "human_action", actor_label, None, {"label": safe_label})

    integrity = safe_integrity_check(source)
    if integrity["status"] != "healthy":
        if repository is not None:
            repository.audit("backup_failed", "system_validation", actor_label, None, {"integrity": integrity})
        raise ValueError("Backup refused because source database integrity check failed.")

    timestamp = now_iso().replace(":", "").replace("-", "")
    root = Path(backup_root)
    root.mkdir(parents=True, exist_ok=True)
    backup_dir = _safe_child(root, f"{safe_label}-{timestamp}-{new_id('BKP')}")
    backup_dir.mkdir(parents=True, exist_ok=False)
    backup_file = backup_dir / "database.sqlite3"

    source_connection = sqlite3.connect(source)
    backup_connection = sqlite3.connect(backup_file)
    try:
        source_connection.backup(backup_connection)
    finally:
        backup_connection.close()
        source_connection.close()

    manifest = {
        "backup_id": backup_dir.name,
        "created_at": now_iso(),
        "boundary_label": "Prototype / Candidate / Non-Operational",
        "schema_version": SCHEMA_VERSION,
        "source_database": str(source),
        "backup_file": str(backup_file),
        "file_size": backup_file.stat().st_size,
        "sha256": _sha256(backup_file),
        "integrity_check": safe_integrity_check(backup_file),
        "manual_only": True,
    }
    _write_json(backup_dir / "backup-manifest.json", manifest)
    (backup_dir / "backup-report.md").write_text(
        "\n".join(
            [
                "# Local Backup Report",
                "",
                "Prototype / Candidate / Non-Operational",
                "",
                f"- Backup ID: {manifest['backup_id']}",
                f"- Integrity: {manifest['integrity_check']['status']}",
                "- Scope: local manual backup only.",
                "",
            ]
        ),
        encoding="utf-8",
    )
    if repository is not None:
        repository.audit("backup_created", "human_action", actor_label, None, {"backup_id": backup_dir.name})
    return {"backup_dir": str(backup_dir), "backup_file": str(backup_file), "manifest": manifest}


def validate_backup(backup_dir: str | Path) -> dict[str, Any]:
    directory = Path(backup_dir)
    manifest_path = directory / "backup-manifest.json"
    backup_file = directory / "database.sqlite3"
    if not manifest_path.exists() or not backup_file.exists():
        return {"status": "failed", "error": "Backup manifest or database file is missing."}
    try:
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        return {"status": "failed", "error": f"Backup manifest is invalid JSON: {exc}"}
    if manifest.get("sha256") != _sha256(backup_file):
        return {"status": "failed", "error": "Backup checksum mismatch."}
    integrity = safe_integrity_check(backup_file)
    if integrity["status"] != "healthy":
        return {"status": "failed", "error": "Backup database integrity check failed.", "integrity": integrity}
    return {"status": "healthy", "manifest": manifest, "integrity": integrity}


def restore_backup(
    backup_dir: str | Path,
    target_db_path: str | Path,
    actor_label: str = "local operator",
) -> dict[str, Any]:
    validation = validate_backup(backup_dir)
    target = Path(target_db_path)
    if validation["status"] != "healthy":
        if target.exists():
            PrototypeRepository(target).audit("restore_failed", "system_validation", actor_label, None, validation)
        raise ValueError(validation.get("error", "Backup validation failed."))

    target.parent.mkdir(parents=True, exist_ok=True)
    preserved_path = None
    if target.exists():
        preserved_dir = target.parent / "restore_preserved"
        preserved_dir.mkdir(parents=True, exist_ok=True)
        preserved_path = preserved_dir / f"{target.stem}-{now_iso().replace(':', '').replace('-', '')}-{new_id('PRE')}.sqlite3"
        shutil.copy2(target, preserved_path)

    temp_target = target.with_suffix(target.suffix + ".restore_tmp")
    shutil.copy2(Path(backup_dir) / "database.sqlite3", temp_target)
    restored_integrity = safe_integrity_check(temp_target)
    if restored_integrity["status"] != "healthy":
        temp_target.unlink(missing_ok=True)
        if target.exists():
            PrototypeRepository(target).audit("restore_failed", "system_validation", actor_label, None, restored_integrity)
        raise ValueError("Restored database failed integrity validation; original database preserved.")

    temp_target.replace(target)
    repository = PrototypeRepository(target)
    repository.audit(
        "restore_completed",
        "human_action",
        actor_label,
        None,
        {"backup_dir": str(backup_dir), "preserved_database": str(preserved_path) if preserved_path else ""},
    )
    return {
        "status": "restored",
        "target_database": str(target),
        "preserved_database": str(preserved_path) if preserved_path else "",
        "integrity": restored_integrity,
    }
