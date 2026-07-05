# Task131-140 Codex Kickoff Instruction

## Status

```text
Task131-140: NOT STARTED
This file is a kickoff instruction only.
```

This document prepares the next controlled task range. It does not authorize implementation, runtime development, QCloud dispatch, public disclosure, or operational CarbonOS / ClimateOS use.

## Required First Read

Before any Task131-140 work, the next AI agent must read:

```text
docs/tasks/TASK121_130_CLOSURE_CONTEXT_PACKET.md
docs/tasks/TASK121_130_CARBONOS_NON_OPERATIONAL_PILOT_APPROVAL_RECORD.md
docs/tasks/TASK121_130_CARBONOS_NON_OPERATIONAL_PILOT_FREEZE_RECORD.md
docs/tasks/ACTIVE_TASKS.md
00_PROJECT_CONTROL/TASK_INDEX.md
```

## Repository

```text
https://github.com/simon947161/eco-agent-system.git
```

## Official Branch

```text
task46-repository-control-codex-batch-queue
```

## Current Baseline Before Task131-140

```text
Task121-130: CLOSED / FROZEN / VERIFIED
Active task: None
QCloud: SUSPENDED
```

The latest closure HEAD before this kickoff packet was:

```text
a7e857806a5f9b3dbd2e707215b3167bea072b92
```

## Highest Priority Before Any New Work

The first Task131-140 activity must be repository environment recovery.

The local Codex workspace repeatedly failed to write Git metadata under `.git`, including `FETCH_HEAD`, `index.lock`, and `ORIG_HEAD.lock`. This makes normal branch switching, commits, fetches, and pushes unreliable.

Do not continue substantive ClimateOS / CarbonOS development until this is fixed or a clean replacement workspace is confirmed.

## Proposed Task131-140 Structure

| Task | Proposed Focus | Status |
| --- | --- | --- |
| Task131 | Repository environment incident review and workspace inventory | Proposed only |
| Task132 | Diagnose `.git` permission failures and Windows Git / Schannel issues | Proposed only |
| Task133 | Create or repair a stable Codex workspace on D drive | Proposed only |
| Task134 | Git health-check protocol: fetch, checkout, branch, commit, push, clean status | Proposed only |
| Task135 | Codex workspace operating rules and no-QCloud builder boundary | Proposed only |
| Task136 | Task121-130 dependency and reuse review for next CarbonOS phase | Proposed only |
| Task137 | CarbonOS Evidence Passport next-phase options, documentation-only | Proposed only |
| Task138 | Human / expert review escalation model refinement, documentation-only | Proposed only |
| Task139 | Non-operational pilot-to-runtime readiness gap review, documentation-only | Proposed only |
| Task140 | Task131-140 closure / architecture gate | Proposed only |

This structure is only a proposed kickoff map. The founder must explicitly approve the actual Task131-140 task brief before work starts.

## Strict Boundaries

Task131-140 must not create:

- runtime implementation
- APIs
- MCP tools
- websites
- calculators
- databases
- compliance engines
- assurance engines
- scoring engines
- automation
- real carbon conclusions
- public disclosure claims
- QCloud dispatch
- operational governance authority

## QCloud Boundary

QCloud remains suspended from ClimateOS and BuildingOS work.

No Task131-140 instruction may assign QCloud to repository control, architecture, implementation, merge, freeze, approval, or governance-sensitive work unless the founder later issues a specific written reversal.

## Required Opening Gate for Next Thread

The next thread should begin with this sequence:

```text
1. Read Task121-130 Closure Context Packet / PCTP.
2. Confirm Task121-130 remains closed / frozen.
3. Confirm Active task is None.
4. Do not start Task131-140 implementation.
5. Diagnose and repair local Git / Codex workspace permissions.
6. Only after environment repair, draft the formal Task131-140 execution brief.
```

## Environment Repair Expectations

The next thread should investigate at least:

- whether the local repo is on the wrong branch
- whether `.git` files are read-only or locked
- whether another process is locking the repo
- whether Windows Defender / Controlled Folder Access is blocking writes
- whether the workspace should be recloned into a new clean folder
- whether Git should consistently use OpenSSL instead of Schannel for this repo
- whether GitHub CLI authentication is needed or should be avoided
- whether Codex has folder write permission for the chosen workspace

## Do Not Start Automatically

This file does not itself authorize Task131-140 work.

The next founder authorization must be explicit and should state whether the first step is:

```text
A. Environment repair only
B. Formal Task131-140 brief drafting only
C. Task131-140 execution after environment repair
D. Stop
```

## Human Summary

Task131-140 should not begin as a feature sprint. It should begin as a repository-stability and process-recovery sprint, because the local `.git` permission problem has become the main blocker and must be fixed before the next ClimateOS / CarbonOS development cycle.
