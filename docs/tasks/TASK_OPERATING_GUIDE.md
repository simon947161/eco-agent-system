# Task Operating Guide

## Purpose

This guide explains how future contributors and AI agents should handle tasks.

## Task Flow

```text
Request
-> Scope check
-> Repository scan
-> Implementation
-> Verification
-> Summary
-> Stop or await approval
```

## Standard Task Report

Every task should report:

- Task ID or short name
- Files created
- Files modified
- Tests executed
- Verification result
- Notes and limitations

## Safety Rules

- Do not modify runtime logic during documentation-only tasks.
- Do not start the next task without approval when the user requests stop
  behavior.
- Do not push, merge, or create PRs unless explicitly requested.
- Restore unrelated test-generated artifacts.

## Boundary

This guide is documentation only. It does not automate task execution.

