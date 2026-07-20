"""Local-only backup/export and restore-preview controls for research records.

This module never copies SQLite, never imports a backup, and never writes outside an
explicit dedicated local root.  Backups are continuity artefacts, not scientific
evidence or environmental conclusions.
"""

from __future__ import annotations

import hashlib
import json
import os
import re
import tempfile
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Iterable

from .program import PROGRAM_ID, PersistentResearchRuntime

BACKUP_SCHEMA = "climateos.local_private_continuity.v0.1"
PRIVACY_LABEL = "LOCAL_PRIVATE_CONTINUITY_NOT_SCIENTIFIC_EVIDENCE"
DEFAULT_MAX_BYTES = 256 * 1024
_SAFE_NAME = re.compile(r"[A-Za-z0-9][A-Za-z0-9._-]{0,119}\.json\Z")


class ContinuityBoundaryError(ValueError):
    """A path, size, schema, identity, or privacy boundary was violated."""


def _now() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def canonical_json(value: Any) -> bytes:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")


def content_digest(value: Any) -> str:
    return "sha256:" + hashlib.sha256(canonical_json(value)).hexdigest()


def _record_digest(value: dict[str, Any]) -> str:
    return content_digest(value)


class LocalPrivateContinuity:
    """Create bounded local backups and preview restore differences without mutation."""

    def __init__(
        self,
        programs: PersistentResearchRuntime,
        local_root: str | Path,
        *,
        max_bytes: int = DEFAULT_MAX_BYTES,
    ) -> None:
        if not isinstance(max_bytes, int) or not 4096 <= max_bytes <= 2 * 1024 * 1024:
            raise ContinuityBoundaryError("max_bytes must be 4096..2097152")
        self.programs = programs
        self.local_root = Path(local_root)
        self.max_bytes = max_bytes

    def _selected_cycles(self, program_id: str, cycle_ids: Iterable[str] | None) -> list[dict[str, Any]]:
        available = self.programs.list_cycles(program_id)
        by_id = {item["cycle_id"]: item for item in available}
        if cycle_ids is None:
            selected_ids = [item["cycle_id"] for item in available]
        else:
            selected_ids = list(cycle_ids)
            if not selected_ids or len(selected_ids) > 120:
                raise ContinuityBoundaryError("cycle_ids must contain 1..120 identities")
            if len(selected_ids) != len(set(selected_ids)):
                raise ContinuityBoundaryError("cycle_ids must be unique")
            if any(not isinstance(item, str) or item not in by_id for item in selected_ids):
                raise ContinuityBoundaryError("cycle selection contains an unknown identity")
        return [self.programs.get_cycle(cycle_id) for cycle_id in selected_ids]

    def build_envelope(
        self,
        *,
        program_id: str = PROGRAM_ID,
        cycle_ids: Iterable[str] | None = None,
        exported_at: str | None = None,
    ) -> dict[str, Any]:
        program = self.programs.get_program(program_id)
        program_record = {key: value for key, value in program.items() if key != "cycles"}
        cycles = self._selected_cycles(program_id, cycle_ids)
        content = {
            "program": program_record,
            "cycles": cycles,
        }
        manifest = {
            "schema_id": BACKUP_SCHEMA,
            "privacy_label": PRIVACY_LABEL,
            "program_id": program_id,
            "exported_at": exported_at or _now(),
            "record_counts": {
                "programs": 1,
                "cycles": len(cycles),
                "observations": sum(len(item.get("observations", [])) for item in cycles),
                "source_snapshots": sum(len(item.get("source_snapshots", [])) for item in cycles),
            },
            "content_digest": content_digest(content),
            "restore_mode": "PREVIEW_ONLY_NO_DATABASE_MUTATION",
            "scientific_status": "NOT_AN_ENVIRONMENTAL_CONCLUSION",
        }
        envelope = {"manifest": manifest, "content": content}
        payload = canonical_json(envelope)
        if len(payload) > self.max_bytes:
            raise ContinuityBoundaryError("backup payload exceeds the configured size ceiling")
        return envelope

    def preview_backup(
        self,
        *,
        program_id: str = PROGRAM_ID,
        cycle_ids: Iterable[str] | None = None,
        exported_at: str | None = None,
    ) -> dict[str, Any]:
        envelope = self.build_envelope(program_id=program_id, cycle_ids=cycle_ids, exported_at=exported_at)
        payload = canonical_json(envelope)
        return {
            "operation": "PREVIEW_ONLY",
            "would_write": False,
            "sqlite_changed": False,
            "root": str(self.local_root),
            "suggested_filename": f"{program_id.lower()}-{envelope['manifest']['exported_at'][:10]}.json",
            "payload_bytes": len(payload),
            "max_bytes": self.max_bytes,
            "manifest": envelope["manifest"],
        }

    def _destination(self, relative_name: str) -> Path:
        if not isinstance(relative_name, str) or not _SAFE_NAME.fullmatch(relative_name):
            raise ContinuityBoundaryError("backup filename must be a simple .json name")
        if Path(relative_name).is_absolute() or Path(relative_name).name != relative_name:
            raise ContinuityBoundaryError("backup destination must not contain a path")
        root = self.local_root.resolve(strict=False)
        if self.local_root.exists() and self.local_root.is_symlink():
            raise ContinuityBoundaryError("backup root must not be a symlink")
        root.mkdir(parents=True, exist_ok=True)
        if self.local_root.is_symlink():
            raise ContinuityBoundaryError("backup root must not be a symlink")
        destination = root / relative_name
        if destination.parent != root:
            raise ContinuityBoundaryError("backup destination escaped the local root")
        if destination.exists() or destination.is_symlink():
            raise ContinuityBoundaryError("backup destination already exists; overwrite refused")
        return destination

    def export_new_file(
        self,
        relative_name: str,
        *,
        program_id: str = PROGRAM_ID,
        cycle_ids: Iterable[str] | None = None,
        exported_at: str | None = None,
    ) -> dict[str, Any]:
        envelope = self.build_envelope(program_id=program_id, cycle_ids=cycle_ids, exported_at=exported_at)
        payload = canonical_json(envelope)
        destination = self._destination(relative_name)
        temp_path: Path | None = None
        try:
            fd, temp_name = tempfile.mkstemp(prefix=".climateos-continuity-", suffix=".tmp", dir=destination.parent)
            temp_path = Path(temp_name)
            with os.fdopen(fd, "wb") as handle:
                handle.write(payload)
                handle.flush()
                os.fsync(handle.fileno())
            if temp_path.stat().st_size != len(payload):
                raise ContinuityBoundaryError("temporary backup verification failed")
            # Reserve the final name without replacement, then atomically replace only our empty reservation.
            reserve_fd = os.open(destination, os.O_CREAT | os.O_EXCL | os.O_WRONLY)
            os.close(reserve_fd)
            os.replace(temp_path, destination)
            temp_path = None
        except Exception:
            if destination.exists() and destination.stat().st_size == 0:
                destination.unlink(missing_ok=True)
            raise
        finally:
            if temp_path is not None:
                temp_path.unlink(missing_ok=True)
        written = destination.read_bytes()
        if written != payload:
            destination.unlink(missing_ok=True)
            raise ContinuityBoundaryError("written backup failed byte verification")
        return {
            "operation": "NEW_FILE_EXPORT_COMPLETE",
            "path": str(destination),
            "payload_bytes": len(payload),
            "file_digest": "sha256:" + hashlib.sha256(written).hexdigest(),
            "content_digest": envelope["manifest"]["content_digest"],
            "overwrite": False,
            "sqlite_changed": False,
            "privacy_label": PRIVACY_LABEL,
        }

    def _read_named_backup(self, relative_name: str) -> tuple[Path, bytes]:
        if not isinstance(relative_name, str) or not _SAFE_NAME.fullmatch(relative_name):
            raise ContinuityBoundaryError("backup filename must be a simple .json name")
        root = self.local_root.resolve(strict=False)
        if self.local_root.is_symlink():
            raise ContinuityBoundaryError("backup root must not be a symlink")
        path = root / relative_name
        if path.parent != root or path.is_symlink() or not path.is_file():
            raise ContinuityBoundaryError("backup is missing or outside the admitted local root")
        size = path.stat().st_size
        if not 1 <= size <= self.max_bytes:
            raise ContinuityBoundaryError("backup size is outside the admitted ceiling")
        return path, path.read_bytes()

    def validate_envelope(self, raw: bytes) -> dict[str, Any]:
        if not isinstance(raw, bytes) or not 1 <= len(raw) <= self.max_bytes:
            raise ContinuityBoundaryError("backup size is outside the admitted ceiling")
        try:
            value = json.loads(raw.decode("utf-8"))
        except (UnicodeDecodeError, json.JSONDecodeError) as exc:
            raise ContinuityBoundaryError("backup must be valid UTF-8 JSON") from exc
        if not isinstance(value, dict) or set(value) != {"manifest", "content"}:
            raise ContinuityBoundaryError("backup envelope fields are closed")
        manifest, content = value["manifest"], value["content"]
        required_manifest = {
            "schema_id", "privacy_label", "program_id", "exported_at", "record_counts",
            "content_digest", "restore_mode", "scientific_status",
        }
        if not isinstance(manifest, dict) or set(manifest) != required_manifest:
            raise ContinuityBoundaryError("backup manifest fields are closed")
        if manifest["schema_id"] != BACKUP_SCHEMA or manifest["privacy_label"] != PRIVACY_LABEL:
            raise ContinuityBoundaryError("backup schema or privacy label is incompatible")
        if manifest["restore_mode"] != "PREVIEW_ONLY_NO_DATABASE_MUTATION":
            raise ContinuityBoundaryError("automatic restore is not admitted")
        if not isinstance(content, dict) or set(content) != {"program", "cycles"}:
            raise ContinuityBoundaryError("backup content fields are closed")
        if content_digest(content) != manifest["content_digest"]:
            raise ContinuityBoundaryError("backup content digest mismatch")
        if content.get("program", {}).get("program_id") != manifest["program_id"]:
            raise ContinuityBoundaryError("backup program identity mismatch")
        cycles = content.get("cycles")
        if not isinstance(cycles, list) or len(cycles) > 120:
            raise ContinuityBoundaryError("backup cycle collection is invalid")
        identities = [item.get("cycle_id") for item in cycles if isinstance(item, dict)]
        if len(identities) != len(cycles) or any(not item for item in identities) or len(set(identities)) != len(identities):
            raise ContinuityBoundaryError("backup cycle identities are invalid")
        expected_counts = {
            "programs": 1,
            "cycles": len(cycles),
            "observations": sum(len(item.get("observations", [])) for item in cycles),
            "source_snapshots": sum(len(item.get("source_snapshots", [])) for item in cycles),
        }
        if manifest["record_counts"] != expected_counts:
            raise ContinuityBoundaryError("backup record counts do not match content")
        return value

    def restore_difference_preview(self, relative_name: str) -> dict[str, Any]:
        path, raw = self._read_named_backup(relative_name)
        envelope = self.validate_envelope(raw)
        manifest, content = envelope["manifest"], envelope["content"]
        program_id = manifest["program_id"]
        try:
            current_program = self.programs.get_program(program_id)
            current_program = {key: value for key, value in current_program.items() if key != "cycles"}
            current_cycles = {item["cycle_id"]: self.programs.get_cycle(item["cycle_id"]) for item in self.programs.list_cycles(program_id)}
        except KeyError:
            current_program, current_cycles = None, {}
        backup_cycles = {item["cycle_id"]: item for item in content["cycles"]}
        common = sorted(set(current_cycles) & set(backup_cycles))
        changed = [cycle_id for cycle_id in common if _record_digest(current_cycles[cycle_id]) != _record_digest(backup_cycles[cycle_id])]
        return {
            "operation": "RESTORE_DIFFERENCE_PREVIEW_ONLY",
            "path": str(path),
            "valid": True,
            "sqlite_changed": False,
            "automatic_import_available": False,
            "program_state": (
                "MISSING_LOCALLY" if current_program is None else
                "UNCHANGED" if _record_digest(current_program) == _record_digest(content["program"]) else
                "DIFFERENT"
            ),
            "cycles_only_in_backup": sorted(set(backup_cycles) - set(current_cycles)),
            "cycles_only_locally": sorted(set(current_cycles) - set(backup_cycles)),
            "cycles_changed": changed,
            "cycles_unchanged": sorted(set(common) - set(changed)),
            "manifest": manifest,
        }
