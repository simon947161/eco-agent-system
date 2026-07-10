# Task610-611 External Scientific Model Reuse And Adapter Policy

## Purpose

Define policy for reusing external scientific models and considering future
adapters without implementing adapters in Task601-620.

## Policy Statement

ClimateOS may reference external scientific models as sources of context,
scenario evidence, or validation questions only when their role, assumptions,
limitations, licensing, provenance, and review status are explicit.

## External Model Categories

- Open scientific models with documented methods.
- Government or institutional datasets and tools.
- Commercial tools with restricted licensing.
- Research prototypes.
- Local specialist models.
- Founder-reserved private models or assets.

## Reuse Rules

- Do not treat model output as direct proof without review.
- Record model assumptions and domain fit.
- Record whether the model is generic, site-calibrated, or expert-reviewed.
- Preserve input boundary and output boundary.
- Separate model reuse from model integration.
- Require human review before model output informs governance.
- Require Founder Gate approval before any adapter or connector is built.

## Adapter Policy

A future adapter proposal must include:

- model identity and owner;
- licensing and permission status;
- input and output contract;
- validation evidence;
- uncertainty handling;
- failure handling;
- privacy and private-asset boundary;
- human review step;
- prohibited uses;
- tests;
- stop condition.

## Private EcoEngine Boundary

Task610-611 does not authorize access to Founder-reserved private EcoEngine
assets or `D:\eco_engine_v200`. No private model file, source tree, assumption,
or output may be scanned, summarized, migrated, reconstructed, uploaded,
published, or integrated.

## Current Capability

No adapter, connector, CLI, API, external model call, live data call, or runtime
integration is created by this policy.

