# ClimateOS Evidence Passport Local Controlled Prototype Core v0.2

Task481-540 created a manually started localhost-only prototype for review of candidate records.

Task541-600 hardens that same local prototype with manual backup / restore, SQLite integrity checks, schema migration controls, data diagnostics, Human Review state-machine enforcement, Founder Gate history, local input limits, import preview, conflict behavior, concurrency handling, and deterministic tests.

Task691-700 adds a bounded Alpha Runtime Skeleton under `/api/alpha/`. It uses
in-memory, restart-cleared state and synthetic/public-safe fixtures to
demonstrate Evidence Contract candidates, fixture-only domains, human review,
refusal, correction, escalation, evidence-grounded deliberation, audit, and
revision rollback without changing the SQLite schema.

Boundary:

- Prototype / Candidate / Non-Operational.
- Local FastAPI service only.
- SQLite file is local, mutable, and not committed.
- No live source retrieval.
- No live model provider.
- Alpha Runtime Skeleton state is in-memory and non-persistent.
- No GitHub automation.
- No scheduler, background worker, autonomous agent, deployment, scoring, compliance, assurance, certification, ESG/carbon conclusion, standards interpretation, or framework interpretation.

## Python Version Used

The Codex workspace Python available during implementation was:

```text
Python 3.12.13
```

## Install Dependencies

Use a local virtual environment outside committed source control:

```powershell
python -m venv .venv
.\.venv\Scripts\python -m pip install -r requirements.txt
```

## Initialize Local Database

```powershell
python scripts/init_db.py --reset --seed
```

The default database path is:

```text
local_data/climateos_local_prototype.sqlite3
```

## Run Local Service

```powershell
python scripts/run_local_service.py --host 127.0.0.1 --port 8765
```

Allowed hosts are `127.0.0.1` and `localhost`.

## Local API Routes

- `GET /api/health`
- `GET /api/candidates`
- `POST /api/candidates`
- `GET /api/candidates/{record_id}`
- `PATCH /api/candidates/{record_id}`
- `POST /api/candidates/{record_id}/archive`
- `POST /api/candidates/{record_id}/review-transition`
- `POST /api/relationships`
- `POST /api/founder-gates`
- `GET /api/audit-events`
- `POST /api/model/prompt-bundle`
- `POST /api/model/mock-response`
- `POST /api/model/import-preview`
- `POST /api/model/import-response`
- `POST /api/model/suggestions/{suggestion_id}/decision`
- `POST /api/archive/export`
- `GET /api/maintenance/integrity`
- `GET /api/maintenance/diagnostics`
- `POST /api/maintenance/backup`
- `POST /api/maintenance/backup/validate`
- `POST /api/maintenance/restore`
- `GET /api/maintenance/migration/preflight`
- `POST /api/maintenance/migration/run`
- `GET /api/alpha/capabilities`
- `GET /api/alpha/domains`
- `GET|POST /api/alpha/evidence-contracts`
- `GET /api/alpha/evidence-contracts/{record_id}`
- `POST /api/alpha/evidence-contracts/{record_id}/review-actions`
- `POST /api/alpha/evidence-contracts/{record_id}/rollback`
- `GET|POST /api/alpha/deliberations`
- `GET /api/alpha/audit-events`
- `GET /api/alpha/diagnostics`

These routes are local prototype interfaces only. They are not production APIs.

## Local Maintenance Commands

```powershell
python scripts/backup_db.py --label manual-review
python scripts/restore_db.py <backup_dir> --validate-only
python scripts/restore_db.py <backup_dir>
python scripts/integrity_check.py
python scripts/integrity_check.py --data-diagnostics
python scripts/migrate_db.py
python scripts/migrate_db.py --run --dry-run
python scripts/migrate_db.py --run
python scripts/generate_synthetic_dataset.py --scale 100
```

These commands are foreground local review helpers only. They do not upload, synchronize, deploy, automate, score, certify, assure, interpret standards, or operate Evidence Passport.

## Alpha Runtime Skeleton Demonstration

Run the service, open `http://127.0.0.1:8765`, and select **Alpha Review**.
The screen can inspect capabilities, fixture domains, current in-memory
Evidence Contracts, and Alpha audit events. Create/review operations are
available through the local prototype routes for deterministic tests and
controlled inspection.

Important boundaries:

- restart clears all Alpha state;
- no Alpha data is written to SQLite;
- fixtures do not represent real environmental observations;
- no conclusion, score, certification, compliance decision, or automated action
  is produced;
- no external model, live source, MCP, private EcoEngine, or network connector
  is used.

## Run Tests

```powershell
python -m pytest tests
```

## Generated Files

The following generated paths must remain uncommitted:

- `.venv/`
- `local_data/`
- `runtime_exports/`
- `local_backups/`
- `local_diagnostics/`
- `*.sqlite3`
