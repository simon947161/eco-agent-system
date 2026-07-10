# ClimateOS Evidence Passport Local Controlled Prototype Core v0.1

Task481-540 creates a manually started localhost-only prototype for review of candidate records.

Boundary:

- Prototype / Candidate / Non-Operational.
- Local FastAPI service only.
- SQLite file is local, mutable, and not committed.
- No live source retrieval.
- No live model provider.
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
- `POST /api/model/import-response`
- `POST /api/model/suggestions/{suggestion_id}/decision`
- `POST /api/archive/export`

These routes are local prototype interfaces only. They are not production APIs.

## Run Tests

```powershell
python -m pytest tests
```

## Generated Files

The following generated paths must remain uncommitted:

- `.venv/`
- `local_data/`
- `runtime_exports/`
- `*.sqlite3`
