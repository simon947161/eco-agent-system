# Green Power Classification Agent Roadmap

## Purpose

This roadmap separates the Task51 documentation foundation from future
implementation and integration work.

## Phase 1: Foundation

**Status:** Completed by Task51.

**Expected outputs:** purpose, classification framework, conceptual input and
output models, evidence requirements, validation rules, governance notes,
example scenarios, and roadmap.

No executable functionality is included.

## Phase 2: Classification Logic

**Status:** Not Started.

**Expected outputs:** versioned deterministic rules, controlled field schema,
invalid-input behavior, human-readable result builder, fixtures, and focused
unit tests.

Logic must preserve `Unknown` and `Needs Review`, avoid regulatory claims, and
remain separate from carbon calculations.

## Phase 3: Validation Integration

**Status:** Not Started.

**Expected outputs:** evidence completeness, consistency, traceability,
boundary, period, unit, duplicate-recognition, and uncertainty checks aligned
with future ValidationOS conventions.

Validation findings will support reviewers and will not approve claims.

## Phase 4: Carbon Accounting Integration

**Status:** Not Started.

**Expected outputs:** a documented handoff from reviewed classification
records to the future Carbon Accounting Agent, including identifiers,
versions, boundaries, quantities, evidence, uncertainty, and review status.

This phase requires the Carbon Accounting Agent foundation and does not imply
emissions calculations in the classification agent.

## Phase 5: Scenario Integration

**Status:** Not Started.

**Expected outputs:** bounded scenario inputs, assumptions, example result
packs, review notes, and limitations aligned with ScenarioOS.

Scenario demonstrations must not be presented as operational classification,
professional advice, or validated environmental claims.

## Next Recommended Task

Task52 should establish the Carbon Accounting Agent foundation and define how
it consumes reviewed green-power classification records without weakening
their evidence, uncertainty, or review status.
