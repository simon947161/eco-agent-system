# Architecture Decisions

New Architecture Decision Records should be added rather than silently
rewriting earlier decisions.

## ADR-001 - Use repository control layer before expanding agents

**Status:** Accepted

**Context:** Agent and subsystem ideas are growing faster than shared task and
decision controls.

**Decision:** Use `00_PROJECT_CONTROL/` as the starting point for roadmap,
tasks, queue, rules, templates, and architecture decisions.

**Consequence:** Future work has clearer scope and review criteria, with a small
documentation-maintenance cost.

## ADR-002 - Keep ClimateOS as master system

**Status:** Accepted

**Context:** Carbon, energy, park, ESG, and GIS capabilities need a shared
evidence and governance foundation.

**Decision:** Keep ClimateOS as the master system and CarbonOS, EnergyOS,
ParkOS, ESGOS, and GISOS as subsystem layers.

**Consequence:** Subsystems reuse common core concepts instead of creating
isolated architectures.

## ADR-003 - Keep GIS/DEM work planning-only by default

**Status:** Accepted

**Context:** Spatial processing requires provenance, specialist methods,
licensing, validation, and professional review.

**Decision:** Keep GIS/DEM work planning-only unless explicitly implemented by
a future approved task.

**Consequence:** Configured context and access plans are not mistaken for
verified GIS/DEM evidence.

## ADR-004 - Prefer human-readable Markdown and JSON

**Status:** Accepted

**Context:** Users are not necessarily programmers, and outputs must remain
reviewable without complex tooling.

**Decision:** Prefer human-readable Markdown and JSON when they meet the task.

**Consequence:** Artifacts remain accessible and auditable.

## ADR-005 - Use Codex batch queue

**Status:** Accepted

**Context:** Large or ambiguous task groups increase review difficulty, token
use, and unrelated-change risk.

**Decision:** Organise small explicit tasks in a Codex batch queue and normally
complete one task per session.

**Consequence:** Work is easier to review and resume, while progress remains
intentionally incremental.
