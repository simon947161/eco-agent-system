# Repository Governance

## Purpose

This document defines the maintainable operating structure for ClimateOS /
eco-agent-system.

## Governance Principles

- Preserve the distinction between implemented, planned, and vision work.
- Keep ClimateOS positioned as an evolving Earth System Governance Runtime.
- Prefer documentation-first foundations before runtime implementation.
- Keep changes small, reviewable, and scoped.
- Preserve provider independence and engine independence.
- Maintain human-readable outputs for non-programmer project owners.
- Avoid unsupported claims about scientific, regulatory, financial, or
  automated decision capability.

## Repository Operating Layers

```text
Root orientation
-> Project control
-> ClimateOS core layers
-> Subsystem foundations
-> Demonstrations
-> Docs governance structures
-> Tests and release artifacts
```

## Change Rules

Documentation-only tasks should not modify runtime logic.

Runtime tasks should define scope, inputs, outputs, tests, limitations, and
rollback expectations before implementation.

External integrations should not be added without explicit task approval.

## Review Expectations

Every task should report:

- files created
- files modified
- verification performed
- test result or reason tests were not run
- explicit limitations

## Boundary

This document establishes governance guidance only. It does not add runtime
workflow automation or enforcement.

