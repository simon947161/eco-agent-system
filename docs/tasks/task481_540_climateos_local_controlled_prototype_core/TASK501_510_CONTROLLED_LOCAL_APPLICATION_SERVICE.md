# Task501-510 Controlled Local Application Service

## Purpose

Create the controlled FastAPI localhost-only service and same-origin local frontend.

## Implemented Route Inventory

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

## Startup Command

```powershell
python scripts/run_local_service.py --host 127.0.0.1 --port 8765
```

Allowed host values are:

```text
127.0.0.1
localhost
```

## Control Confirmation

- Manual startup only.
- Same-origin local frontend and API.
- No wildcard CORS.
- No public host configuration.
- No deployment configuration.
- No authentication or multi-user system.
- No scheduler or background workflow.
