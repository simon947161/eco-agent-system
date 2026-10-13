# Mission Runtime Founder Evidence Package — Final v0.1

Date: 2026-07-27
Status: READY_FOR_FOUNDER_DECISION
Parent: Issue #103
Draft PR: #104

## 1. Decision context

Founder previously approved prototype design only.

Current authority remains:

- Implementation Authority: NOT GRANTED
- Mainline Runtime Change: NOT ALLOWED
- Merge Authority: NOT GRANTED
- External Execution: NOT ALLOWED

Phase A has now produced static architecture, four JSON Schemas, machine-readable positive fixtures, negative mutation cases, ClimateOS/BuildingOS mission examples and a static validation report.

## 2. What has been proven

Static validation confirms:

- lifecycle state vocabulary can be constrained;
- child authority widening can be structurally prohibited;
- checkpoint resume can require permission revalidation;
- unconditional always-approve restoration can be prohibited;
- context recovery can require an authoritative repository, branch and commit.

## 3. What has not been proven

No executable validator currently exists.

Therefore Phase A has not yet proven:

- semantic transition legality;
- actual parent/child set inclusion;
- protected-write classification at runtime;
- evidence existence or freshness;
- checkpoint hash integrity;
- repository-state drift detection;
- safe runtime dispatch.

## 4. Five Founder Decisions

### Decision 1 — Lifecycle model

Proposed lifecycle:

`DRAFT → PLANNED → READY → RUNNING → CHECKPOINTED/BLOCKED/FOUNDER_GATE → COMPLETED → ARCHIVED`

Alternative terminal paths: `CANCELLED`.

Recommended decision:

`APPROVE_LIFECYCLE_V0_1`

Effect:

- validates the state vocabulary;
- does not itself authorise execution;
- allows a future Validator to check semantic transitions.

### Decision 2 — Protected-write baseline

Proposed protected categories:

- mainline repository write;
- merge, deploy, publish or release;
- irreversible repository or evidence deletion;
- external communication;
- financial commitment;
- credential or permission change;
- live provider integration;
- authoritative legal, compliance, safety or scientific conclusion;
- roadmap priority or domain-ownership change.

Recommended decision:

`APPROVE_PROTECTED_WRITE_BASELINE_V0_1`

### Decision 3 — Parent/child capability inheritance

Proposed rule:

`Child Capability Envelope ⊆ Parent Capability Envelope`

Children may narrow but never widen tool, network, write, merge, external-contact or conclusion authority.

Recommended decision:

`APPROVE_CAPABILITY_INHERITANCE_V0_1`

### Decision 4 — Resume safety

Proposed rule:

Every resume must:

- load a sealed checkpoint;
- revalidate permissions;
- revalidate repository/external state;
- detect stale evidence;
- resume from the next safe action;
- return to Founder Gate when authority is stale;
- never restore unconditional always-approve authority.

Recommended decision:

`APPROVE_RESUME_SAFETY_V0_1`

### Decision 5 — Executable Validator prototype

Proposed next scope:

A bounded, non-dispatching Validator that only reads static Mission artifacts and returns `PASS`, `FAIL` or `FOUNDER_GATE` with reasons.

It would not:

- execute tools;
- write to main;
- merge PRs;
- contact external systems;
- schedule autonomous work;
- issue domain conclusions.

Recommended decision:

`APPROVE_BOUNDED_EXECUTABLE_VALIDATOR_PROTOTYPE`

Alternative decisions:

- `HOLD_AT_STATIC_DESIGN`
- `RETURN_FOR_PHASE_A_REVISION`

## 5. Recommended combined Founder response

```text
APPROVE_LIFECYCLE_V0_1
APPROVE_PROTECTED_WRITE_BASELINE_V0_1
APPROVE_CAPABILITY_INHERITANCE_V0_1
APPROVE_RESUME_SAFETY_V0_1
APPROVE_BOUNDED_EXECUTABLE_VALIDATOR_PROTOTYPE
```

## 6. Verification evidence

- Four schemas parsed and meta-validated under JSON Schema Draft 2020-12.
- Four valid fixtures passed.
- Four negative mutation cases failed as expected.
- Branch remains isolated from main.
- No executable runtime, scheduler or dispatcher was introduced.
- No merge or mainline modification occurred.

## 7. Rollback path

If the Founder does not approve executable work:

- retain PR #104 as Draft;
- preserve schemas and fixtures as research artifacts;
- do not merge;
- do not create Validator runtime code;
- return Mission state to `BLOCKED` or retain `FOUNDER_GATE`.

## 8. Current gate

`READY_FOR_FIVE_FOUNDER_DECISIONS`

No additional ordinary review is required before the Founder makes these decisions.