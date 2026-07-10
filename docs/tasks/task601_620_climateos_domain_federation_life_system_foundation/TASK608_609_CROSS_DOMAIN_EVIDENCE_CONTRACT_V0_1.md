# Task608-609 Cross-Domain Evidence Contract v0.1

## Purpose

Define a conceptual, non-operational Evidence Contract for passing evidence
between ClimateOS domains.

## Status

This is a conceptual specification only. It is not a schema, API contract,
database migration, runtime interface, validation engine, or operational
Evidence Passport.

## Contract Intent

The Evidence Contract should preserve enough context for another domain to
understand what a record claims, where it came from, how it was interpreted,
what uncertainty remains, and what review is still required.

## Conceptual Fields

| Field | Purpose |
| --- | --- |
| Evidence ID | Stable reference for discussion and review. |
| Origin Domain | Domain that first created or interpreted the record. |
| Receiving Domain | Domain asked to reuse, review, or challenge the record. |
| Claim Type | What the evidence is being asked to support. |
| Source Type | Observation, document, field note, model output, expert review, community signal, or other source. |
| Source Status | Raw, curated, reviewed, disputed, stale, or superseded. |
| Method Context | Method, assumption, model, observation method, or interpretation basis. |
| Spatial Context | Site, boundary, transect, region, or unresolved spatial scope. |
| Temporal Context | Date, period, baseline, trend window, or unresolved time scope. |
| Uncertainty | Known limits, missing evidence, disagreement, or confidence status. |
| Review State | Draft, human review needed, reviewed, rejected, superseded, or Founder Gate required. |
| Prohibited Reuse | Constraints on reuse, publication, scoring, certification, or private-source exposure. |
| Cross-Domain Notes | Context needed by the receiving domain. |

## Evidence Contract Principles

- Preserve meaning before optimizing structure.
- Carry uncertainty with the evidence.
- Treat method context as evidence, not metadata decoration.
- Make prohibited reuse explicit.
- Keep human review visible.
- Do not convert conceptual fields into runtime requirements without a future
  implementation gate.

## Validation Requirements

Future work must test the contract with non-sensitive examples from at least
three domains before any runtime design is considered.

## Open Questions

- Which fields are mandatory for Alpha Runtime?
- How should conflicting domain interpretations be represented?
- Should Evidence Contract records be separate from Evidence Passport records,
  or one layer within them?
