# ClimateOS Multi-Agent Workflow

Status: Workflow Guide v0.1

## Purpose

This document defines the current multi-agent development workflow for ClimateOS.

The workflow separates planning, drafting, repository integration, and review.

## Core Roles

### Planner

Responsible for architecture, roadmap, task planning, and final decision synthesis.

Current primary agent: ChatGPT.

### Draft Builder

Responsible for preparing draft documentation or task outputs when repository maintainer capacity is limited.

Current possible agent: QCLAW.

Draft Builders should work on draft branches only.

### Repository Maintainer

Responsible for official repository integration, commit, push, verification, and repository health.

Current primary agent: Codex.

### Reviewer

Responsible for architecture review, consistency analysis, risk identification, and Task101+ recommendations.

Current primary agent: QCLAW.

## Branch Flow

Draft Builder branch pattern:

```text
qclaw/batch-XX-draft
```

Official working branch:

```text
task46-repository-control-codex-batch-queue
```

The Draft Builder must not push directly to the official working branch.

The Repository Maintainer reviews and integrates draft branches into the official branch.

## Standard Workflow

1. Simon defines the goal.
2. Planner prepares the task book.
3. Draft Builder creates a draft branch or draft pack.
4. Repository Maintainer reviews and integrates.
5. Reviewer performs architecture review.
6. Planner accepts, rejects, or defers recommendations.
7. Architecture Snapshot is updated when needed.
8. Next Batch Sprint begins.

## QCLAW Draft Branch Rule

When QCLAW produces repository work, it should use:

```text
qclaw/batch-XX-draft
```

QCLAW should return:

- branch name
- commit hashes
- files created
- files modified
- tests run or not run
- known limitations
- Codex verification notes

## Codex Integration Rule

Codex should:

- fetch the draft branch
- compare against the official branch
- review file paths
- verify naming consistency
- check Markdown links
- update indexes if needed
- run tests
- restore generated artifacts
- commit and push to the official branch

Codex should not blindly merge.

## Review Rule

Review agents should use:

```text
docs/review/ARCHITECTURE_SNAPSHOT.md
```

They should provide recommendations only.

Accepted changes may be assigned to Codex or parked as Task101+ recommendations.

## Current Principle

GitHub acts as the asynchronous message bus between agents.

Draft branches and review documents are the handoff objects.

Repository truth remains in the official working branch.
