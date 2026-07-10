# Task511-520 Human Review And Founder Gate Controls

## Human Review Controls

Human Review transitions require:

- record identifier;
- new status;
- reviewer label;
- reason;
- linked risk flags where applicable;
- Founder Gate trigger where applicable.

The API rejects incomplete review transition payloads through FastAPI / Pydantic validation.

No model suggestion, import function, seed script, or workflow rule marks its own output as human-reviewed.

## Founder Gate Controls

Founder Gate records require:

- gate trigger;
- affected records;
- decision date;
- decision status;
- Founder instruction text.

Founder Gate records are manual records. The prototype does not make Founder decisions or pass a gate automatically.

## Audit Trail

Human Review transitions and Founder Gate entries create audit events with actor provenance.

## Task520 Checkpoint Reference

See [TASK520_CHECKPOINT_RECORD.md](TASK520_CHECKPOINT_RECORD.md).
