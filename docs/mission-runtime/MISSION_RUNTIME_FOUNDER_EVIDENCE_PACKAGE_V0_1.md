# Mission Runtime Founder Evidence Package v0.1

Date: 2026-07-27
Status: PREPARED_FOR_LATER_FOUNDER_REVIEW
Implementation authority: NOT GRANTED

## 1. What has been designed

- shared Mission object and ownership boundary;
- lifecycle state vocabulary;
- Mission Plan Contract;
- parent capability envelope;
- governed tool dispatch concept;
- protected-write categories;
- checkpoint and context-packet contracts;
- validator suite design;
- ClimateOS, BuildingOS, interruption/resume and protected-write fixtures.

## 2. Why this work is necessary

ClimateOS already uses ACTP, handoffs, context packets, Draft PRs and Founder gates, but these controls are document-driven. Mission Runtime turns them into explicit, machine-checkable contracts while leaving climate, building, water, energy and carbon reasoning inside their domain runtimes.

## 3. Current completion assessment

- Phase A architecture narrative: COMPLETE
- State-machine schema: COMPLETE_DRAFT
- Plan-contract schema: COMPLETE_DRAFT
- Checkpoint schema: COMPLETE_DRAFT
- Context-packet schema: COMPLETE_DRAFT
- Validator design: COMPLETE_DRAFT
- ClimateOS/BuildingOS mission fixtures: COMPLETE_DRAFT
- Executable validators: NOT STARTED — Founder authority required
- Scheduler/dispatcher: NOT STARTED — later phase
- Mainline integration: NOT AUTHORISED

## 4. How Phase A is validated

### Static validation
- all JSON documents must parse;
- schema references and required fields must be internally consistent;
- mission, plan, checkpoint and context-packet identifiers must tie together;
- child capability envelope must be a subset of parent capability envelope.

### Behavioural fixture validation
- normal static-documentation mission passes;
- permission widening fails;
- protected mainline write fails;
- stale or unconditional resume authority fails;
- ClimateOS and BuildingOS domain boundaries remain intact.

### Founder validation
Founder does not review every field. Founder reviews five policy choices:
1. lifecycle state names and transition authority;
2. protected-write categories;
3. parent/child permission inheritance;
4. resume behaviour after interruption;
5. whether executable prototype work may begin.

## 5. Founder review questions

### Decision A — Lifecycle
Approve, amend or reject the proposed states:
`DRAFT → PLANNED → READY → RUNNING → CHECKPOINTED/BLOCKED/FOUNDER_GATE → COMPLETED → ARCHIVED`.

### Decision B — Protected writes
Confirm whether the protected set must include mainline writes, merges, deployments, external contact, paid services, credentials, deletion, irreversible data changes and authoritative scientific/legal/compliance conclusions.

### Decision C — Delegation
Confirm that a child may only narrow, never widen, the parent capability envelope.

### Decision D — Resume
Confirm that resumed missions must revalidate permissions and external state and may never restore unconditional approval.

### Decision E — Next authority
Choose one:
- `APPROVE_EXECUTABLE_VALIDATOR_PROTOTYPE`
- `REVISE_PHASE_A_DESIGN`
- `HOLD_AT_STATIC_DESIGN`

## 6. Rollback and containment

All Phase A work is isolated on a Draft branch and Draft PR. No mainline runtime, scheduler, tool dispatcher or external system has changed. Rollback is therefore branch closure or file revision; no operational rollback is required.

## 7. Recommended Founder review format

A single bounded review session using the five decisions above. No local runtime test is required until executable validators are separately authorised.