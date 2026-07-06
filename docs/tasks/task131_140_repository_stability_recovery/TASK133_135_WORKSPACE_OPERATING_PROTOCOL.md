# Task133-135 Workspace Operating Protocol

## Purpose

This document completes Batch B for the Task131-140 repository-stability recovery sprint.

It combines:

- Task133: confirm stable D drive Codex workspace operating mode
- Task134: define Git health-check protocol for branch, commit, status, fetch, and push readiness
- Task135: codify Codex workspace operating rules and no-QCloud builder boundary

This protocol is documentation-only. It does not change Git config, change ownership or permissions, resume QCloud, create runtime capability, or implement Task136-140.

## Official Workspace Assumptions

| Item | Operating Assumption |
| --- | --- |
| Workspace root | `D:\Codex\ClimateOS` |
| Working repository | `D:\Codex\ClimateOS\eco-agent-system-codex-working` |
| Official branch | `task46-repository-control-codex-batch-queue` |
| Normal Codex mode | Programming mode in the normal Codex shell |
| OneDrive workspace | Not used for this repo |
| QCloud | Suspended from ClimateOS and BuildingOS work |

The D drive repository is the current stable working environment for controlled Codex documentation and repository-governance work.

## Normal Codex Shell Operating Mode

Use the normal Codex shell for ordinary read, edit, validation, and local commit work.

Expected normal state before starting a task:

```text
git branch --show-current
git status --short
git rev-parse HEAD
git ls-remote origin task46-repository-control-codex-batch-queue
```

Start work only when:

- the branch is `task46-repository-control-codex-batch-queue`
- `git status --short` is clean
- local HEAD is the expected official branch commit or an approved descendant
- remote official branch matches the expected baseline for the task

If these checks do not match, stop and report the exact output.

## Git Preflight Before Work

Run these checks before task edits:

```text
git branch --show-current
git status --short
git log -1 --oneline
git remote -v
git ls-remote origin task46-repository-control-codex-batch-queue
```

Do not auto-repair mismatches unless the human instruction explicitly authorizes the repair.

## Git Checks Before Commit

Before staging and committing:

```text
git diff
git status --short
git diff --check
```

Confirm:

- changed files are inside the authorized task scope
- generated or test-output files are not accidentally included
- `git diff --check` has no whitespace errors
- boundary terms still preserve no-runtime, no-QCloud, and no-closure limits

Use the requested commit message when one is supplied.

## Git Checks Before Push

Before push:

```text
git status --short
git log -1 --oneline
git rev-parse HEAD
git ls-remote origin task46-repository-control-codex-batch-queue
```

Push readiness is not push authorization.

Push only when the human explicitly asks to push, and only the branch or commit requested by that instruction.

After push:

```text
git ls-remote origin task46-repository-control-codex-batch-queue
git status --short
```

Report the remote SHA and clean status.

## safe.directory and Dubious-Ownership Handling

Task132 classified the dubious-ownership guard as a manageable escalated-context risk.

Rules:

- Do not change global Git config unless the human explicitly approves.
- Do not add the whole D drive as a safe directory.
- Do not change Windows ownership or permissions.
- If commit or push hits the known dubious-ownership guard, use only a one-command repo-specific override:

```text
git -c safe.directory=D:/Codex/ClimateOS/eco-agent-system-codex-working <git command>
```

Record whether the override was used in the final report.

## Human / Founder Gates

The following remain separately gated:

- push to remote
- PR creation
- merge
- approval record creation
- freeze record creation
- closure record creation
- any Task136-140 work
- any runtime, API, MCP, website, calculator, database, compliance, assurance, scoring, or automation work

No agent should infer approval from prior successful tasks, a clean Git state, or an approved brief.

## QCloud Suspended Boundary

QCloud remains suspended from ClimateOS and BuildingOS work unless the founder later issues an explicit written reversal.

This protocol does not create:

- QCloud dispatch
- QCloud branch
- QCloud packet
- QCloud runtime task
- QCloud repository-control task
- QCloud merge / approval / freeze task
- QCloud architecture or governance-sensitive task

## Prohibited Work During This Recovery Sprint

Unless explicitly authorized in a later task, do not create or modify:

- runtime implementation
- API implementation
- MCP implementation
- website implementation
- calculator implementation
- database implementation
- compliance engine
- assurance engine
- scoring engine
- automation
- real carbon conclusions
- public disclosure claims
- QCloud dispatch artifacts
- closure records

## Handoff Rules Before Task136

Before Task136 starts:

- Task133-135 must be reviewed.
- The official branch should be clean and pushed.
- Task136 scope should be restated from the frozen brief.
- The human should confirm that Task136 remains documentation-only.
- Any remote operation should remain separately gated.

Task136 must not be started automatically from this protocol.

## Batch B Result

```text
Task133: COMPLETED
Task134: COMPLETED
Task135: COMPLETED
Task136-140: NOT STARTED
QCloud Builder Work: SUSPENDED
Runtime Implementation: NOT STARTED
Fixes Applied: NONE
```
