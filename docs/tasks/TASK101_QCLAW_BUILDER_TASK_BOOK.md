# Task101 QCLAW Builder Task Book

## Authority

Architecture Authority: ChatGPT

Engineering Authority: Codex

Builder: QCLAW

Final Approval: Simon

## Purpose

Prepare the Task101 Human Use Graduation Test Suite for ClimateOS.

Task101 is a documentation-only test design task. It should define a human-readable test suite that checks whether the frozen ClimateOS Foundation can support real environmental project judgment.

Task101 must not implement runtime functionality.

## Repository Truth

Official branch:

```text
task46-repository-control-codex-batch-queue
```

Before drafting, synchronize with the current official repository state and review:

- `docs/tasks/TASK100_FOUNDATION_GRADUATION_FREEZE_RECORD.md`
- `docs/tasks/TASK100_FOUNDATION_GRADUATION_REVIEW.md`
- `docs/tasks/TASK100_FOUNDATION_GRADUATION_APPROVAL_RECORD.md`
- `docs/tasks/TASK100_QCLAW_BUILDER_TASK_BOOK.md`
- `PROJECT_INDEX.md`
- `00_PROJECT_CONTROL/TASK_INDEX.md`
- `docs/tasks/TASK101_PLUS_RECOMMENDATIONS.md`

Treat the official branch as Repository Truth.

## Three Truth Model

Repository Truth:

- Official branch.
- Maintained by Codex.

Builder Truth:

- QCLAW draft branch.
- Draft content only until reviewed and integrated.

Architecture Truth:

- Architecture Snapshot and accepted ChatGPT architecture decisions.
- Task100 frozen records.
- A100-01 Environmental Mainline Protection Principle.

QCLAW must not treat draft content as official until Codex integrates it.

## Source Of Authority

Task101 drafting is authorized by:

- [Task100 Foundation Graduation Freeze Record](TASK100_FOUNDATION_GRADUATION_FREEZE_RECORD.md)
- [Task100 Foundation Graduation Review](TASK100_FOUNDATION_GRADUATION_REVIEW.md)
- Architecture Comment A100-01 - Environmental Mainline Protection Principle
- Task101 read-only planning pass

Task100 is closed and frozen. Task101 must inherit Task100 conclusions without reopening Task100 artifacts.

## Task101 Mission

Task101 should:

- test practical human use of the frozen ClimateOS Foundation
- validate whether ClimateOS can support real environmental project judgment
- translate Task100 graduation checks into reusable human-use test design
- keep test scenarios human-readable, reviewable, and bounded
- prepare ClimateOS for the next controlled phase without implementing runtime behavior

Task101 should not claim that any scenario result is a validated environmental conclusion.

## Mandatory Inheritance From Task100

Task101 must inherit and operationalize the five Task100 graduation checks:

- Reality Test
- Evidence Test
- Validation Test
- Governance Test
- Inheritance Test

These checks should be used as the backbone of the Task101 test suite.

## Required Task101 Design Criteria

The Task101 test suite must define:

- human readability criteria
- responsibility boundary criteria
- evidence sufficiency criteria
- pass/fail decision model
- test input/output template
- scenario catalog
- runtime inheritance mapping

Each criterion should remain conceptual and documentation-only. Do not create automated scoring logic.

## Candidate Scenario Set

Task101 should include a compact first-pass scenario set:

- CarbonOS: carbon claim / ESG disclosure judgment
- WaterOS: drainage or stormwater risk judgment
- EnergyOS: community energy project judgment
- BuildingOS: building module / interface judgment
- Climate Data: NASA or BOM climate observation interpretation

The scenarios are test designs only. They must not be presented as validated environmental findings.

## Recommended Compact Deliverable Structure

Create a compact first-pass file set:

```text
docs/tasks/task101_human_use_graduation_test_suite/

README.md
TASK101_HUMAN_USE_GRADUATION_TEST_SUITE.md
TEST_SCENARIO_CATALOG.md
TEST_INPUT_OUTPUT_TEMPLATE.md
PASS_FAIL_DECISION_MODEL.md
TASK101_COMPLETION_REVIEW.md
```

Additional criteria files may be added later only if needed.

## Deliverable Guidance

### README.md

Explain the purpose, scope, status, and navigation for the Task101 test suite.

### TASK101_HUMAN_USE_GRADUATION_TEST_SUITE.md

Define the overall human-use graduation test suite and explain how it inherits Task100.

### TEST_SCENARIO_CATALOG.md

Describe the compact scenario set and the purpose of each scenario.

### TEST_INPUT_OUTPUT_TEMPLATE.md

Provide a reusable template for:

- test input
- expected human-readable output
- evidence notes
- validation notes
- governance boundary notes
- responsibility boundary notes

### PASS_FAIL_DECISION_MODEL.md

Define a simple documentation-only pass/fail model.

The model should help reviewers decide whether a scenario shows sufficient foundation readiness. It must not introduce automated scoring or runtime logic.

### TASK101_COMPLETION_REVIEW.md

Summarize:

- what Task101 tested
- which Task100 checks were inherited
- which candidate scenarios were defined
- what remains unresolved
- whether ClimateOS is ready for the next controlled phase of human-use testing

## Scope Limits

Task101 must not:

- modify frozen Task100 artifacts
- implement runtime code
- create APIs
- build MCP tools
- create website functionality
- begin Task102 or later tasks
- change ClimateOS Core architecture
- treat test scenarios as validated environmental conclusions

## Frozen Task100 Protection

Do not modify:

- `docs/tasks/TASK100_QCLAW_BUILDER_TASK_BOOK.md`
- `docs/tasks/TASK100_FOUNDATION_GRADUATION_REVIEW.md`
- `docs/tasks/TASK100_FOUNDATION_GRADUATION_APPROVAL_RECORD.md`
- `docs/tasks/TASK100_FOUNDATION_GRADUATION_FREEZE_RECORD.md`

Any change to frozen Task100 artifacts requires a Change Request and approval.

## Environmental Mainline Protection

Task101 must preserve A100-01 Environmental Mainline Protection Principle.

ClimateOS Core exists to support:

- environmental observation
- environmental evidence
- environmental validation
- environmental governance
- environmental action

Runtime, Agent, MCP, SDK, website, repository workflow, and Builder Dispatch are supporting mechanisms. They are not the ClimateOS mission.

Task101 should test whether ClimateOS can support real environmental project judgment, not merely whether documents are internally complete.

## Builder Assignment

Builder:

- QCLAW

Codex role:

- engineering manager
- integration reviewer
- repository maintainer

QCloud role:

- parked unless later approved for demonstrator implementation

## Verification Requirements

QCLAW must verify:

- focused Markdown links are valid
- no Task100 frozen artifacts were modified
- no implementation files were created
- no runtime, API, MCP, or website functionality was introduced
- Task101 remains documentation-only
- working tree is clean after commit, if QCLAW performs git operations

Codex must independently verify the draft before integration.

## Final Report Requirements

QCLAW's completion report must include:

- files changed
- summary of Task101 draft content
- recommended Task101 file structure
- confirmation that no Task100 frozen artifacts were modified
- confirmation that no implementation files were created
- verification results
- unresolved issues

## Escalation Rule

If QCLAW discovers:

- roadmap conflict
- architecture contradiction
- missing interface that changes Task101 scope
- repository safety issue
- pressure to reopen Task100 frozen artifacts
- pressure to begin Task102 or later work

Stop.

Report to Codex.

Do not redesign independently.

## Architecture Review Closing Format

Future review closeouts should use:

```text
Architecture Review Result

APPROVED / APPROVED WITH REFINEMENTS / REJECTED

Dispatch Decision

Ready for Builder Dispatch / Hold

Engineering Action

Codex prepares and dispatches the Builder Task Book.

Builder

QCLAW

Status

Ready for QCLAW Draft Preparation.
```

## Status

Ready for QCLAW draft preparation.
