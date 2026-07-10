# Task491-500 Local Persistence Foundation

## Purpose

Create a local SQLite persistence layer for candidate-only Evidence Passport prototype records.

## Implemented

- SQLite initialization.
- Schema version table.
- Candidate records table.
- Relationship records table.
- Human Review records table.
- Founder Gate records table.
- Audit events table.
- Model suggestion table.
- Archive events table.
- Local reset procedure.
- Deterministic seed fixtures.
- JSON import path for seed fixtures.
- Local persistence tests.

## Mutable Database Boundary

The generated SQLite database remains under:

```text
prototype/climateos-local-controlled-prototype-core/local_data/
```

That path is ignored and must not be committed.

## No-Cloud Verification

No cloud database, external synchronization, remote persistence, distributed database abstraction, or production ORM is introduced.
