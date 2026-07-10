# Failure, Concurrency, Performance, And Windows Operations

## Failure Handling

Task541-600 adds explicit local failure behavior for corrupt backups, unsupported schema versions, invalid status transitions, duplicate imports, duplicate relationships, oversized requests, and invalid host headers.

## SQLite Concurrency

SQLite connections use a busy timeout and close after context-manager use. Tests exercise bounded concurrent foreground writes without background workers or schedulers.

## Synthetic Performance

Synthetic local performance checks use deterministic generated candidate records. They do not use live sources, model providers, external calls, or operational data.

Command:

```powershell
python scripts/generate_synthetic_dataset.py --scale 100
```

## Windows Local Operation

Command helpers are foreground PowerShell-compatible scripts. Generated data remains ignored under local-only output directories.

## Boundary

This sprint does not create monitoring, telemetry, scheduler, background worker, queue, service manager, cloud deployment, QCloud integration, n8n workflow, MCP tool, or autonomous agent.
