# Dependency Inventory And Maintenance Guide

## Locked Prototype Stack

Task541-600 preserves the Task481-540 local prototype stack:

- Python 3.12-compatible runtime.
- FastAPI.
- Uvicorn.
- SQLite from the Python standard library.
- Pydantic.
- pytest.
- httpx for FastAPI test client support.
- Local HTML / CSS / JavaScript.
- JSON and Markdown export.

## Requirements File

The prototype dependency record remains:

```text
prototype/climateos-local-controlled-prototype-core/requirements.txt
```

No external provider SDK, cloud SDK, authentication framework, task queue, scheduler, telemetry dependency, vector database, database server, MCP package, n8n package, or deployment package was added.

## Maintenance Commands

```powershell
python scripts/init_db.py --reset --seed
python scripts/backup_db.py --label manual-review
python scripts/restore_db.py <backup_dir> --validate-only
python scripts/integrity_check.py --data-diagnostics
python scripts/migrate_db.py
python -m pytest tests
```

## Boundary

Dependency maintenance is local prototype maintenance only. It does not authorize production operation, deployment, live integration, automated scheduling, external retrieval, or operational Evidence Passport.
