# Mission Validator Design v0.1

Status: STATIC_DESIGN
Implementation authority: NOT GRANTED

## Purpose

Define how Mission Runtime rejects invalid, unsafe or unrecoverable mission states before an executable prototype exists.

## Validator set

### 1. Schema Validator
Checks Mission, Plan, Checkpoint and Context Packet objects against the v0.1 JSON Schemas.

### 2. State Transition Validator
Rejects transitions that are not declared, lack authority, skip required evidence, or cross a Founder Gate without approval.

### 3. Capability Envelope Validator
Verifies that child missions and agents only narrow inherited permissions. A child cannot add tools, network access, external contact, merge authority or protected-write authority absent from the parent envelope.

### 4. Protected Write Validator
Classifies the proposed action by effect and target, not merely by tool name. Protected targets include mainline branches, merges, deployments, external communications, paid services, credential use, deletion, irreversible data change and authoritative scientific/legal/compliance conclusions.

### 5. Checkpoint Consistency Validator
Confirms that state, plan, evidence, permissions, open items and recovery instruction refer to the same mission revision and that the recovery pointer is resolvable.

### 6. Resume Safety Validator
Requires permission and external-state revalidation. It rejects checkpoints that attempt to restore unconditional approval or stale implementation authority.

### 7. Evidence Chain Validator
Checks that decisions and state transitions cite evidence objects or explicit Founder decisions. Research evidence may justify planning but cannot grant execution authority.

## Required negative tests

- child requests broader network access than parent;
- research result attempts to authorise repository write;
- mission resumes with `always_approve_restored=true`;
- direct transition from DRAFT to RUNNING without a valid plan;
- protected write targets main without implementation authority;
- checkpoint references a different mission or obsolete plan revision;
- domain conclusion is produced without domain evidence.

## Required positive tests

- static documentation mission proceeds inside a no-network, no-merge envelope;
- child mission narrows parent permissions;
- interrupted mission resumes after permission revalidation;
- Founder approval authorises only the named transition and scope;
- ClimateOS fixture completes static schema work while preserving domain/runtime separation.

## Completion criteria

The design is complete when every validator has inputs, pass/fail rules, error codes, positive fixtures and negative fixtures. Executable validator code requires a separate Founder Gate.

## Verification method

1. JSON Schema lint and parse.
2. Fixture validation against all four schemas.
3. Deliberate mutation tests for every negative case.
4. Cross-reference check between mission IDs, plan revisions and checkpoint IDs.
5. Founder review of protected-write categories and transition authority only.