# Schema Version And Migration Policy

## Current Schema Version

Task541-600 updates the local prototype schema version to:

```text
2
```

## Version 2 Additions

- `audit_events.sequence_number`
- `audit_events.operation_id`
- `founder_gates.supersedes_gate_id`
- `founder_gates.decision_version`

## Migration Requirements

Future local migrations must provide:

- Current schema version detection.
- Target schema version reporting.
- Pending migration list.
- Preflight mode.
- Dry-run mode.
- Pre-migration local backup.
- Unsupported future-version rejection.
- Deterministic tests.

## Migration Commands

```powershell
python scripts/migrate_db.py
python scripts/migrate_db.py --run --dry-run
python scripts/migrate_db.py --run
```

## Boundary

Schema migration is local SQLite prototype maintenance only. It is not a production database migration framework and does not authorize external persistence, cloud database, data warehouse, vector database, knowledge graph runtime, or operational Evidence Passport storage.
