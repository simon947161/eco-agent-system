# Task531-540 Archive Export, Integration Testing And Closure

## Purpose

Create local archive export, integration tests, prohibited-capability review, future gate questions, and the Task540 hard stop record.

## Local Archive Bundle

Archive export may generate:

- `case-manifest.json`
- `source-candidate-register.md`
- `signal-register.md`
- `claim-candidate-register.md`
- `knowledge-object-register.md`
- `evidence-candidate-register.md`
- `evidence-readiness-record.json`
- `risk-flag-register.json`
- `human-review-record.json`
- `founder-gate-record.json`
- `audit-log.json`
- `closure-summary.md`

Generated runtime export paths are ignored and not committed.

## Integration Testing

Tests cover:

- schema validation;
- candidate status validation;
- relationship integrity;
- SQLite initialization;
- local persistence;
- FastAPI request validation;
- localhost-only configuration;
- prohibited public binding;
- audit-event creation;
- Human Review transitions;
- Founder Gate manual recording;
- mock model suggestions;
- malformed imported responses;
- suggestion provenance;
- archive generation;
- no live model-provider dependency;
- no GitHub automation dependency;
- no Task541 directory.

## Closure Records

- [TASK541_600_GATE_QUESTIONS.md](TASK541_600_GATE_QUESTIONS.md)
- [TASK540_HARD_STOP_RECORD.md](TASK540_HARD_STOP_RECORD.md)
- [TASK481_540_SPRINT_CLOSURE_PACKET.md](TASK481_540_SPRINT_CLOSURE_PACKET.md)
