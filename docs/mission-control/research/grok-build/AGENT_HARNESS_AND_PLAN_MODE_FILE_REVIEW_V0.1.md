# Grok Build Agent Harness and Plan Mode File Review v0.1

**Project:** ClimateOS / Mission Control / PRI  
**Status:** FILE-LEVEL RESEARCH BASELINE  
**Date:** 2026-07-22  
**Mode:** RESEARCH-ONLY / RFC-ONLY / NO MAINLINE CHANGE

---

## 1. Scope

本文件对 Grok Build 的 Agent Harness 与 Plan Mode 进行第一轮文件级研究，目标是提炼可用于 ClimateOS、BuildingOS、CarbonOS、WaterOS、EnergyOS、Matrix 与 PRI 的工程模式。

本文件不授权复制代码、引入依赖或修改 Runtime。

---

## 2. Source Revision

- Repository: `xai-org/grok-build`
- Reviewed revision: `3af4d5d39897855bdcc74f23e690024a5dc05573`
- Evidence class: Official public source repository
- Limitation: 公开仓库可能是内部系统的同步切片，不能把“未发现”解释为“生产系统不存在”。

---

## 3. File-Level Index

### 3.1 Plan Mode core

- `crates/codegen/xai-grok-shell/src/session/plan_mode.rs`
  - PlanModeTracker
  - PlanModeState
  - lifecycle persistence
  - approval state
  - restart recovery
  - reminder injection state

- `crates/codegen/xai-grok-tools/src/implementations/grok_build/enter_plan_mode/mod.rs`
  - agent-initiated plan-mode entry tool

- `crates/codegen/xai-grok-tools/src/implementations/grok_build/exit_plan_mode/mod.rs`
  - approval handoff and implementation transition

- `crates/codegen/xai-grok-pager/src/slash/commands/plan.rs`
  - user-initiated plan entry

- `crates/codegen/xai-grok-pager/src/app/dispatch/modes.rs`
  - TUI mode switching

- `crates/codegen/xai-grok-pager/docs/user-guide/19-plan-mode.md`
  - public behavioural contract

### 3.2 Agent Harness related

- `crates/codegen/xai-grok-agent/src/builder.rs`
  - agent construction and dependency assembly

- `crates/codegen/xai-grok-agent/src/config.rs`
  - agent configuration surface

- `crates/codegen/xai-grok-shell/src/session/*`
  - session actor, prompt handling, completion handling, compaction and tool-call routing

- `crates/codegen/xai-grok-tools/src/registry/types.rs`
  - tool registry types and dispatch metadata

- `crates/codegen/xai-grok-tools/src/types/tool_io.rs`
  - tool input/output contracts

- `crates/codegen/xai-grok-workspace/src/permission/auto_mode.rs`
  - approval and automatic execution policy interaction

---

## 4. Plan Mode Architecture

### 4.1 State model

Grok Build uses a session-scoped explicit state machine:

```text
Inactive
  ├─ user toggle → Pending
  ├─ agent tool approval → Active
Pending
  ├─ first prompt → Active
  └─ toggle off → Inactive
Active
  ├─ approved plan → Inactive
  ├─ idle toggle off → Inactive
  └─ in-flight toggle off → ExitPending
ExitPending
  └─ turn completion → Inactive
```

The state is not merely prompt text. It is represented in runtime state, persisted to disk, restored after restart, and integrated with session lifecycle.

### 4.2 Plan artifact

The plan is stored as a durable session artifact:

```text
~/.grok/sessions/<cwd>/<session-id>/plan.md
```

Expected content:

- Context
- recommended approach
- critical files
- reusable functions/utilities
- end-to-end verification

This is stronger than an ephemeral chat plan because it becomes inspectable, reviewable and restartable.

### 4.3 Approval model

Plan Mode separates:

```text
explore → write plan → human review → approve/revise/abandon → implement
```

It supports:

- inline comments
- freeform revision notes
- approval with comments
- repeated revision cycles
- abandoning the plan without implementation

### 4.4 Persistence and recovery

The runtime persists:

- active state
- prior activation
- reminder counter
- pending exit reminder
- pending plan approval

Transient in-flight states are normalized on restart. This is a useful pattern for recoverable missions: persist durable intent, collapse unsafe transient state.

---

## 5. Agent Harness Findings

The public code suggests the Harness is distributed across several crates rather than concentrated in one monolithic controller.

```text
Agent Builder / Config
        ↓
Session Actor
        ↓
Prompt + Context Assembly
        ↓
Model Completion
        ↓
Tool Registry / Tool Dispatch
        ↓
Workspace / Permission Runtime
        ↓
Session Persistence / UI / ACP
```

Key engineering patterns:

1. **Session-scoped mutable governance state**  
   Mode and approval state belong to the session runtime, not merely to model prompts.

2. **Dedicated tool contracts**  
   Entering and exiting Plan Mode are tools with explicit lifecycle effects.

3. **Durable planning artifact**  
   Plan is a file, not only a transient answer.

4. **Approval surface is a runtime component**  
   Human review is represented in product state and survives restart.

5. **Context reminders are actively managed**  
   The runtime reinjects state reminders and preserves mode through compaction.

6. **Harness is channel-agnostic**  
   TUI, ACP and headless surfaces converge on shared session semantics.

---

## 6. Critical Risks and Non-Adoptable Behaviour

### R-01 — Parent Plan Gate does not automatically govern child agents

The user guide explicitly states that subagents start with a fresh Plan Mode tracker. A write-capable child may therefore edit while the parent remains in Plan Mode.

**ClimateOS judgment:** REJECT AS-IS.

Required adaptation:

```text
Parent Mission Gate
    ↓ inherited mandatory policy
Child Agent Capability Envelope
    ↓
Tool / File / Network / Evidence Permissions
```

No child agent should escape a parent mission's read-only or Founder Gate state unless an explicit delegated exception exists.

### R-02 — Shell writes are not covered by edit-tool enforcement

The Plan Mode edit gate blocks editing tools, but does not inspect Bash redirection or other shell-side writes.

**ClimateOS judgment:** REJECT AS-IS.

Required adaptation:

- sandbox-level filesystem policy
- command classification
- write-set declaration
- post-run diff validation
- immutable protected paths

### R-03 — Plan artifact is implementation-centric

The plan template is optimized for software modification. ClimateOS missions also require:

- evidence basis
- domain assumptions
- uncertainty
- environmental or policy impact
- affected geography
- data lineage
- governance authority
- rollback and invalidation rules

**ClimateOS judgment:** ADAPT.

### R-04 — Approval is primarily plan approval

ClimateOS needs multiple gates:

```text
Research Gate
Architecture Gate
Evidence Gate
Safety Gate
Founder Gate
Operational Release Gate
```

A single approve/revise/quit surface is insufficient for domain runtime governance.

---

## 7. Proposed ClimateOS Mission Planning Runtime

### 7.1 Mission states

```text
DISCOVERED
SCOPED
PLANNING_READ_ONLY
PLAN_REVIEW_PENDING
PLAN_REVISION_REQUIRED
PLAN_APPROVED
EXECUTING
EVIDENCE_REVIEW_PENDING
FOUNDER_REVIEW_PENDING
ACCEPTED
REJECTED
SUSPENDED
RECOVERY_REQUIRED
SUPERSEDED
```

### 7.2 Mission Plan artifact

Recommended file:

```text
MISSION_PLAN.md
```

Required sections:

1. Mission intent
2. Scope and non-scope
3. Source and evidence register
4. Existing capability reuse
5. Proposed architecture
6. Files/systems affected
7. Agent and tool permissions
8. Validation plan
9. Failure and recovery plan
10. Human review gates
11. Expected evidence outputs
12. Adoption classification

### 7.3 Mission checkpoint bundle

```text
mission.json
MISSION_PLAN.md
EVIDENCE_REGISTER.md
DECISION_LOG.md
VALIDATION_REPORT.md
RECOVERY_STATE.json
```

### 7.4 Parent-child governance

Every child agent must inherit:

- mission ID
- parent agent ID
- capability mode
- allowed write paths
- allowed tools
- network scope
- evidence obligations
- token/time budget
- stop conditions
- review gate

---

## 8. Preliminary Classification

| Capability | Classification | Reason |
|---|---|---|
| Explicit plan state machine | ADOPT | Strong lifecycle clarity |
| Durable plan artifact | ADOPT | Supports review and recovery |
| Read-only planning phase | ADAPT | Must enforce beyond edit tools |
| Human approval surface | ADAPT | Needs multi-gate governance |
| Restart persistence | ADOPT | Essential for Mission Control |
| Compaction-aware state reminder | ADOPT | Prevents context drift |
| Parent-child independent plan state | REJECT | Governance escape risk |
| Tool-only write blocking | REJECT | Shell and external tool bypass risk |
| Session-scoped governance state | ADOPT | Correct runtime placement |
| Implementation-centric plan schema | ADAPT | Must add evidence and domain governance |

---

## 9. Next Research

1. Trace Agent Builder to SessionActor construction.
2. Trace prompt/context assembly and compaction.
3. Trace tool registry to permission decision.
4. Trace subagent delegation and capability modes.
5. Trace workspace checkpoint and VCS recovery.
6. Draft `MISSION_RUNTIME_RFC_V0.1.md`.

---

## 10. Research Status

```text
FILE_LEVEL_INDEX: COMPLETE_V0.1
PLAN_MODE_STATE_MACHINE: REVIEWED
PLAN_APPROVAL: REVIEWED
PERSISTENCE: REVIEWED
PARENT_CHILD_GOVERNANCE: RISK_IDENTIFIED
MAINLINE_CHANGE: NONE
FOUNDER_ACTION: NOT_REQUIRED
```
