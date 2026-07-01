# Task100 QCLAW Builder Task Book

## Authority

Architecture Authority: ChatGPT

Engineering Authority: Codex

Builder: QCLAW

Final Approval: Simon

## Purpose

Prepare the Task100 Foundation Graduation package for ClimateOS.

Task100 is the Foundation completion milestone. It should confirm what governance capabilities ClimateOS Foundation has established and which future runtimes can inherit those capabilities.

Required framing:

```text
ClimateOS Foundation does not implement domain intelligence.

It establishes the common governance capabilities inherited by every future domain runtime.
```

## Repository Truth

Official branch:

```text
task46-repository-control-codex-batch-queue
```

Before drafting, synchronize with the current official repository state and review:

- `docs/review/ARCHITECTURE_SNAPSHOT.md`
- `docs/strategy/FOUNDATION_ROADMAP_STABILITY_DECISION.md`
- `docs/strategy/CLIMATEOS_AGENT_GOVERNANCE_CHARTER.md`
- `docs/strategy/CLIMATEOS_ENGINEERING_CULTURE.md`
- `PROJECT_INDEX.md`
- `00_PROJECT_CONTROL/TASK_INDEX.md`
- `docs/tasks/BATCH25_VALIDATION_DEMONSTRATION_AND_PREFLIGHT_REVIEW.md`
- `docs/tasks/TASK101_PLUS_RECOMMENDATIONS.md`

## Three Truth Model

Repository Truth:

- Official branch.
- Maintained by Codex.

Builder Truth:

- QCLAW draft branch.
- Draft content only until reviewed and integrated.

Architecture Truth:

- Architecture Snapshot and accepted ChatGPT architecture decisions.

QCLAW must not treat draft content as official until Codex integrates it.

## Strategic Position

ClimateOS is one governance programme with multiple workstreams.

Current workstreams:

- Workstream A: ClimateOS Foundation
- Workstream B: BuildingOS Engineering

Future workstreams may include:

- CarbonOS
- WaterOS
- EnergyOS
- LandOS

Task100 belongs to Workstream A.

BuildingOS MCP work belongs to Workstream B and must not be pulled into Task100.

## Task100 Objective

Task100 should answer:

```text
What governance capabilities has ClimateOS Foundation established,
and which future runtimes are now able to inherit those capabilities?
```

Task100 should not merely summarize files. It should synthesize the Foundation as a capability platform.

## Required Scope

Task100 must include:

- Foundation Architecture Review
- Engineering Review
- Foundation Graduation Review
- Governance Capability Review
- Future Runtime Inheritance Review
- Transition toward Governance Runtime
- Task101+ Transition Plan

## Required Deliverables

Create:

```text
docs/tasks/TASK100_FOUNDATION_GRADUATION_REVIEW.md
docs/tasks/TASK100_FOUNDATION_ARCHITECTURE_REVIEW.md
docs/tasks/TASK100_ENGINEERING_REVIEW.md
docs/tasks/TASK100_GOVERNANCE_CAPABILITY_REVIEW.md
docs/tasks/TASK100_RUNTIME_INHERITANCE_REVIEW.md
docs/tasks/TASK100_GOVERNANCE_RUNTIME_TRANSITION.md
docs/tasks/TASK100_TASK101_PLUS_TRANSITION_PLAN.md
docs/tasks/BATCH26_TASK100_FOUNDATION_GRADUATION_REVIEW.md
```

Update:

```text
PROJECT_INDEX.md
00_PROJECT_CONTROL/TASK_INDEX.md
docs/README.md
docs/tasks/README.md
docs/tasks/ACTIVE_TASKS.md
docs/tasks/COMPLETED_TASKS.md
```

## Required Content Guidance

### Foundation Architecture Review

Review Task58 through Task99 as one coherent Foundation architecture.

Confirm:

- no roadmap redesign
- no unnecessary new Foundation layers
- Task100 remains the Foundation completion milestone
- Task101+ items remain parked outside Foundation completion

### Engineering Review

Review:

- repository health
- documentation organization
- navigation
- verification requirements
- test status
- known generated artifacts
- handoff readiness for future runtimes

### Foundation Graduation Review

Confirm what ClimateOS Foundation has built.

Focus on capability platform maturity, not product completion.

Include a short `Graduation Philosophy` section near the end of
`docs/tasks/TASK100_FOUNDATION_GRADUATION_REVIEW.md`.

Required text:

```text
ClimateOS Foundation does not solve every future problem.

It establishes the governance capabilities that allow future problems to be solved in a trustworthy way.

ClimateOS Foundation is not the destination.

It is the common governance foundation upon which future domain runtimes can safely evolve.

Every future runtime - including CarbonOS, WaterOS, EnergyOS, BuildingOS and other domain systems - should inherit these common governance capabilities rather than reinvent them.

This is the meaning of Foundation Graduation.
```

### Governance Capability Review

Summarize common governance capabilities established by Foundation, including:

- observation management
- relationship reasoning
- radar/change detection concepts
- evidence synthesis
- proof/reality claim review
- knowledge runtime
- validation framework
- confidence framework
- collective validation
- review engine
- review workflow
- validation runtime interface
- validation packs
- validation IO model
- benchmark library
- examples, reference objects, demonstrations, and preflight review

### Runtime Inheritance Review

Explain how future runtimes can inherit Foundation capabilities.

Future runtimes include:

- Governance Runtime
- Domain Runtime
- CarbonOS
- WaterOS
- EnergyOS
- LandOS
- BuildingOS, as an engineering and infrastructure workstream

Clarify that Foundation does not implement domain intelligence.

### Governance Runtime Transition

Describe transition readiness only.

Do not implement Governance Runtime.

Do not define APIs, code, scoring engines, automation, blockchain, token models, or production systems.

### Task101+ Transition Plan

Review `docs/tasks/TASK101_PLUS_RECOMMENDATIONS.md`.

Separate:

- post-Foundation engineering recommendations
- domain runtime recommendations
- BuildingOS engineering experiments
- future MCP / Agent SDK / GitHub Workflow / multi-agent collaboration items

## Explicit Non-Goals

Task100 must not:

- implement Governance Runtime
- implement Domain Runtime
- implement CarbonOS, WaterOS, EnergyOS, LandOS, or BuildingOS runtime capability
- implement MCP Server
- implement APIs
- implement automated validation
- implement scoring engines
- implement workflow engines
- implement blockchain, token models, or financial products
- redesign the roadmap
- introduce unnecessary new Foundation layers
- move Task101+ ideas into Task100 unless they are required to explain graduation readiness

## BuildingOS Boundary

BuildingOS is a parallel engineering workstream.

Accepted BuildingOS MCP positioning:

```text
BuildingOS Core
-> Governance Runtime
-> Module SDK
-> MCP Server
-> Agent / Tool Interface
```

MCP should expose governed capabilities, not raw Core structures.

This is not Task100 scope. Record related observations as Task101+ or BuildingOS workstream recommendations.

## Verification Requirements

QCLAW should verify:

- all required files exist
- all internal Markdown links are valid
- Task100 docs remain documentation-only
- no runtime code is added
- no API implementation is added
- no Governance Runtime implementation is added
- no BuildingOS MCP implementation is added
- no roadmap redesign is introduced

If tests are available, QCLAW should run:

```text
python -m unittest discover
```

If tests generate known CCZPS-Lite artifacts, report them so Codex can restore generated output before integration if required.

## Draft Branch

QCLAW should use:

```text
qclaw/task100-foundation-graduation-draft
```

If this branch name is unavailable, use:

```text
qcloud/task100-foundation-graduation-draft
```

Do not push to the official branch.

## QCLAW Completion Report Format

Return:

```text
Task ID: Task100
Draft Branch:
Commit Hash:
Files Created:
Files Modified:
Verification Performed:
Tests Run:
Results:
Architecture Notes:
Roadmap Stability Notes:
Task101+ Notes:
Risks:
Needs Codex Decision: yes/no
Needs Architecture Review: yes/no
Needs Simon Approval: yes/no
```

## Escalation Rule

Stop and report to Codex if any of the following occur:

- roadmap conflict
- architecture contradiction
- missing interface requiring architecture judgement
- repository safety issue
- pressure to implement runtime capability
- pressure to redesign Task100
- uncertainty about whether a Task101+ idea belongs inside Task100

Do not redesign independently.

## Codex Integration Plan

After QCLAW returns draft work, Codex will:

1. Compare draft branch with official branch.
2. Verify required files and links.
3. Review architecture wording.
4. Confirm Task100 does not implement runtime capability.
5. Run repository tests.
6. Restore generated artifacts if necessary.
7. Integrate, commit, and push to the official branch.
8. Produce an Engineering Report with execution continuity fields.

## Engineering Report Requirements

Codex final integration report must include:

1. Completed Work
2. Repository Health
3. Architecture Health
4. Roadmap Progress
5. Engineering Health
6. Capacity Status
7. Risks
8. Proposed Next Batch
9. Architecture Advice Required: YES / NO

## Architecture Review Closing Format

Use this closing format for future milestone architecture reviews:

```text
Architecture Review Result

APPROVED
APPROVED WITH REFINEMENTS
REJECTED

Dispatch Decision

Ready for Builder Dispatch
Hold

Engineering Action

Codex prepares and dispatches the Builder Task Book.

Builder

QCLAW

Status

Ready for QCLAW Draft Preparation.
```

Task100 current status:

```text
Architecture Review Result

APPROVED

Dispatch Decision

Ready for Builder Dispatch

Engineering Action

Codex prepares and dispatches the Builder Task Book.

Builder

QCLAW

Status

Ready for QCLAW Draft Preparation.
```

## Status

Ready for QCLAW draft preparation after Codex dispatch.

