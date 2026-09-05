# Mission Runtime Founder Review Gate v0.1

Date: 2026-07-27
Status: REVIEW_DEFERRED_UNTIL_FOUNDER_AVAILABLE
Parent: Issue #103

## Review purpose

Founder review is not required for ordinary documentation, schema drafting, fixtures or non-executable validators.

Founder review is required before Mission Runtime moves from static prototype design to executable runtime work.

## Founder decisions required

### Gate 1 — Lifecycle authority

Confirm whether these protected transitions require Founder authority:

- `PLANNING -> READY_FOR_EXECUTION`
- `FOUNDER_GATE -> EXECUTING`
- `VALIDATING -> COMPLETED`
- any transition enabling protected writes

Recommended default: Founder authority for protected transitions; delegated authority allowed only through an explicit permission envelope.

### Gate 2 — Protected-write classes

Confirm the protected categories:

- mainline runtime change;
- merge/deploy/publish/release;
- irreversible repository action;
- external communication;
- financial commitment;
- credential or permission change;
- live provider integration;
- publication of legal, compliance, safety or scientific conclusions;
- authoritative evidence deletion;
- roadmap or domain-ownership change.

Recommended default: approve this list as the minimum baseline.

### Gate 3 — Parent/child authority inheritance

Confirm:

- child missions inherit the parent's capability ceiling;
- children may narrow but never widen authority;
- no child Plan Gate may bypass the parent authority chain;
- tool, network, write and conclusion authority are inherited separately.

Recommended default: approve.

### Gate 4 — Resume behaviour

Confirm that resume must:

- load a sealed checkpoint;
- re-check permissions and repository state;
- detect stale evidence and changed conditions;
- resume from the next safe action;
- return to Founder Gate if authority is stale;
- never restore an unconditional always-approve state.

Recommended default: approve.

### Gate 5 — Executable prototype authority

Choose one future decision:

- `APPROVE_STATIC_SCHEMA_ONLY`
- `APPROVE_BOUNDED_EXECUTABLE_PROTOTYPE`
- `RETURN_FOR_SCHEMA_REVISION`

No decision is required today. Until a future Gate 5 decision, implementation authority remains not granted.

## What Founder does not need to review now

- wording and formatting;
- ordinary object fields;
- non-executable JSON Schema mechanics;
- fixture naming;
- validator test layout;
- documentation organisation;
- Draft PR creation.

## Review evidence package to prepare

Before asking the Founder to decide, Mission Control must provide:

1. one-page architecture map;
2. mission lifecycle diagram;
3. one ClimateOS mission example;
4. one BuildingOS child-mission example;
5. one interruption/checkpoint/resume example;
6. one protected-write denial example;
7. exact list of changes an executable prototype would make;
8. explicit rollback path.

## Current decision

`REVIEW_NOT_REQUIRED_YET`

Continue Phase A static schema work. Stop before executable scheduler, dispatcher, protected-write engine or mainline integration.