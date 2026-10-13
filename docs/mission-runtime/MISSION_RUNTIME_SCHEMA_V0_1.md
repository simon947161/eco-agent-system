# Mission Runtime Schema v0.1

Date: 2026-07-27
Status: PROTOTYPE_DESIGN
Authority: Founder-approved design only; implementation not authorised
Parent: Issue #103

## 1. Purpose

Mission Runtime is the shared lifecycle and governance runtime for ClimateOS, BuildingOS, WaterOS, EnergyOS, CarbonOS and future WorldOS domains.

It coordinates work. It does not replace domain reasoning.

```text
Mission Control
  -> Mission Runtime
      -> Matrix registries
      -> Domain Runtime
      -> governed tools
      -> evidence and checkpoints
```

## 2. Ownership boundary

Mission Runtime owns:

- mission identity and lifecycle;
- plan contract and dependency graph;
- checkpoints and recovery;
- context-packet transfer;
- capability and permission envelopes;
- governed tool dispatch;
- protected-write gates;
- evidence-chain references;
- archive and resume state.

Domain Runtime owns:

- climate, building, water, energy or carbon reasoning;
- domain objects, models and validators;
- domain-specific evidence interpretation;
- scientific, engineering and regulatory logic.

Matrix owns registries for capabilities, agents, skills, tools and permissions.

## 3. Canonical mission object

A mission record must contain:

- `mission_id`
- `mission_type`
- `title`
- `owner`
- `domain_runtime`
- `parent_mission_id`
- `lifecycle_state`
- `priority`
- `plan_contract_ref`
- `capability_envelope_ref`
- `permission_envelope_ref`
- `context_packet_ref`
- `current_checkpoint_ref`
- `evidence_bundle_refs`
- `dependency_refs`
- `authority_chain`
- `created_at`
- `updated_at`
- `resume_policy`
- `archive_policy`

## 4. Lifecycle states

Proposed states:

1. `PROPOSED`
2. `RESEARCHING`
3. `PLANNING`
4. `READY_FOR_EXECUTION`
5. `EXECUTING`
6. `PAUSED`
7. `BLOCKED`
8. `FOUNDER_GATE`
9. `VALIDATING`
10. `COMPLETED`
11. `ARCHIVED`
12. `CANCELLED`
13. `FAILED_RECOVERABLE`
14. `FAILED_TERMINAL`

No agent may move a mission into `READY_FOR_EXECUTION`, leave `FOUNDER_GATE`, or authorise a protected write unless the authority chain permits it.

## 5. Plan contract

A plan is a governed object, not free-form notes.

Required fields:

- objective and success criteria;
- bounded scope and explicit exclusions;
- ordered work packages;
- dependencies;
- required capabilities;
- allowed tools;
- protected-write classes;
- validation requirements;
- evidence requirements;
- interruption and resume behaviour;
- Founder Gate conditions;
- completion and archive conditions.

Research findings may be attached as evidence to a plan. Research cannot self-authorise execution.

## 6. Parent capability envelope

Every child mission or sub-agent inherits a capability ceiling from its parent.

A child may narrow authority, but may not widen:

- tool access;
- write scope;
- network access;
- external communication;
- financial authority;
- merge or deployment authority;
- legal or scientific conclusion authority.

Independent child Plan Gates are rejected when they would bypass the parent authority chain.

## 7. Governed tool dispatch

Tool permission is evaluated from action effect, not tool name alone.

Dispatch evaluation must consider:

- actor;
- mission state;
- capability envelope;
- permission envelope;
- target resource;
- action class;
- reversibility;
- externality;
- evidence requirement;
- approval requirement.

The same tool may be allowed for a read and blocked for a protected write.

## 8. Protected write boundary

Initial protected-write classes:

- mainline runtime or production configuration;
- merge, deploy, publish or release;
- irreversible repository history change;
- external message, application or institutional contact;
- paid service or financial commitment;
- credential, secret or permission modification;
- live provider integration;
- legal, compliance, safety or scientific conclusion publication;
- deletion of authoritative evidence;
- change to roadmap priority or domain ownership.

## 9. Checkpoint bundle

A checkpoint must preserve:

- mission state;
- accepted plan revision;
- completed and pending work packages;
- evidence references;
- tool actions and results;
- current permissions;
- unresolved questions;
- active blockers;
- git/repository revision where applicable;
- recovery pointer;
- next safe action;
- Founder Gate status.

A checkpoint is immutable after sealing. Corrections create a superseding checkpoint.

## 10. Resume policy

Resume must never use an unconditional always-approve mode.

On resume the runtime must:

1. load the latest valid checkpoint;
2. re-evaluate current permissions and protected-write boundaries;
3. verify dependencies and repository state;
4. identify stale evidence or changed external conditions;
5. continue only from the next safe action;
6. return to Founder Gate when previous authority is no longer valid.

## 11. ClimateOS and CII integration

Mission Runtime coordinates CII batches such as ontology, teleconnection graph, provider adapter and BuildingOS translation.

It stores mission state, dependencies, checkpoints, permissions and evidence references.

ClimateOS continues to define Earth-system physics and evidence semantics. BuildingOS continues to define engineering-risk translation.

## 12. Prototype boundary

This schema authorises only documentation, static schemas, fixtures and validators.

It does not authorise:

- executable scheduler;
- live dispatcher;
- autonomous writes;
- mainline runtime modification;
- external tool execution;
- automatic merge;
- always-on autonomous operation.
