# Input, Import, And Local API Security

## Purpose

Task541-600 adds local hardening controls for the existing Task481-540 FastAPI prototype routes.

## Local Controls

- Host header guard allows localhost, `127.0.0.1`, and the test client host only.
- Request-size limit rejects oversized inputs before route handling.
- Validation errors are normalized into JSON-safe error payloads.
- Static security headers are added to local responses.
- Candidate list supports bounded filtering, search, limit, and offset.
- Model response import has suggestion count and duplicate suggestion-ID validation.
- Import preview reports conflicts without writing records.
- Duplicate response and duplicate relationship conflicts return explicit local conflict responses.

## Local Route Additions

- `POST /api/model/import-preview`
- `GET /api/maintenance/integrity`
- `GET /api/maintenance/diagnostics`
- `POST /api/maintenance/backup`
- `POST /api/maintenance/backup/validate`
- `POST /api/maintenance/restore`
- `GET /api/maintenance/migration/preflight`
- `POST /api/maintenance/migration/run`

## Boundary

These are local prototype routes only. They are not production API routes, not external APIs, not public services, not authentication, not authorization, not deployment, not automation, and not operational Evidence Passport.
