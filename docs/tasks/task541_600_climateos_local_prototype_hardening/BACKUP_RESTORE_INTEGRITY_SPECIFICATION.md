# Backup, Restore, And Integrity Specification

## Backup Command

```powershell
python scripts/backup_db.py --label manual-review
```

The command creates a manual local backup under:

```text
local_backups/
```

Generated backup directories contain:

- `database.sqlite3`
- `backup-manifest.json`
- `backup-report.md`

The manifest records schema version, source path, backup path, file size, SHA-256 checksum, integrity status, and manual-only boundary.

## Restore Command

```powershell
python scripts/restore_db.py <backup_dir> --target-db-path local_data/climateos_local_prototype.sqlite3
```

Restore validates the manifest, checksum, and SQLite integrity before replacement. If a target database already exists, restore preserves a copy under `restore_preserved/` before replacing it.

## Integrity Command

```powershell
python scripts/integrity_check.py
python scripts/integrity_check.py --data-diagnostics
```

The first command runs SQLite integrity and foreign-key checks. The second runs prototype data diagnostics.

## Boundary

Backup and restore are local manual maintenance actions only. They do not publish, synchronize, deploy, upload, commit, push, automate, or operate Evidence Passport.
