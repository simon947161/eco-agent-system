# Agent Collaboration Radar

**Status:** Radar v0.1  
**Scope:** ClimateOS multi-agent collaboration, automation, communication, and repository workflow  
**Purpose:** Track methods that can reduce manual copy-paste coordination between ChatGPT, Codex, QCLAW, and future builder agents.

---

# 1. Why This Radar Exists

ClimateOS is now developed by a human-agent team.

The current workflow still requires Simon to manually move messages between ChatGPT, Codex, and QCLAW.

This is acceptable as a temporary bridge, but it is not the long-term goal.

The long-term goal is to create a more automated agent collaboration system where planning, dispatch, building, review, integration, and reporting can move through structured handoff objects with minimal manual intervention.

---

# 2. Current Working Method

Current method:

```text
ChatGPT -> Task Book
Codex -> Engineering Dispatch / Integration
QCLAW -> Draft Branch / Draft Work
Codex -> Review / Commit / Push
ChatGPT -> Architecture Review
Simon -> Approval / Direction
```

Current message bus:

```text
GitHub branches
GitHub commits
GitHub pull requests
Markdown task books
Architecture Snapshot
Completion reviews
```

This is the most reliable current approach.

---

# 3. Radar Categories

## Category A — GitHub Workflow

Purpose:

Use GitHub as the asynchronous communication and evidence layer between agents.

Current maturity:

High for current workflow.

Methods to track:

- draft branches
- pull requests
- issue templates
- PR review comments
- GitHub Actions
- branch protection
- automated link checks
- task completion templates

Near-term recommendation:

Continue using GitHub as the primary message bus before adopting deeper agent-to-agent automation.

---

## Category B — MCP / Model Context Protocol

Purpose:

Connect agents to tools, files, repositories, databases, and structured resources through a common protocol.

Potential ClimateOS use:

- connect agents to GitHub
- connect agents to Obsidian / Knowledge Garden
- connect agents to local documentation stores
- expose task books and architecture snapshots as resources
- standardise tool access across agents

Risks:

- security
- permissions
- prompt injection
- tool misuse
- poor tool descriptions

Near-term recommendation:

Monitor. Do not disrupt Task100. Consider MCP after Foundation Graduation as Task101+ engineering work.

---

## Category C — A2A / Agent-to-Agent Protocol

Purpose:

Enable agents from different systems to discover capabilities, exchange messages, coordinate tasks, and return artifacts.

Potential ClimateOS use:

- ChatGPT as Planner agent
- Codex as Engineering Manager agent
- QCLAW as Builder agent
- future agents as specialised builders or reviewers
- structured task handoff using agent cards or capability descriptions

Near-term recommendation:

Monitor as a strategic direction. Do not rely on A2A for current Task100 delivery.

---

## Category D — Agent SDK / Runtime Orchestration

Purpose:

Create explicit workflows that assign tasks to agents and manage state, output, and review.

Potential ClimateOS use:

- Planner -> Dispatcher -> Builder -> Reviewer -> Repository Maintainer workflow
- status tracking
- retries
- escalation
- output validation
- task logs

Near-term recommendation:

Record patterns as Task101+ Engineering Recommendations. Do not implement before Task100 unless required.

---

# 4. Current Implementation Priority

Priority order:

1. GitHub branch / PR workflow
2. Standard task handoff templates
3. Architecture Snapshot update discipline
4. Codex capacity reporting
5. QCLAW draft branch discipline
6. GitHub Actions for simple checks
7. MCP feasibility review
8. A2A feasibility review
9. Agent runtime orchestration

---

# 5. Capacity Reporting Requirement

Codex should include a Capacity Report when possible:

```text
Capacity status: High / Medium / Low / Critical
Suggested next batch size: 1 Batch / 2 Batches / Pause
Recommended delegation: Codex / QCLAW / defer
Risk: none / moderate / high
```

QCLAW should include execution limits or constraints when relevant.

This enables the Planner to schedule work without wasting limited capacity.

---

# 6. Standard Handoff Metadata

Every handoff should identify:

- recipient
- sender
- role of recipient
- task type
- branch name
- expected output
- escalation route
- whether the output is draft or official

This reduces human copy-paste risk.

---

# 7. Task101+ Engineering Recommendations

Current recommendations:

- create PR-based QCLAW handoff workflow
- create standard QCLAW Builder Task Book template
- create standard Codex Integration Report template
- create standard Capacity Report section
- create GitHub Actions link check or documentation check
- evaluate MCP for GitHub / Knowledge Garden access
- evaluate A2A for long-term Planner / Manager / Builder communication
- design Agent Runtime after Task100

---

# 8. No-Go Before Task100

Before Task100, do not:

- redesign the roadmap around agent automation
- introduce complex orchestration systems
- replace GitHub branch workflow
- require full A2A or MCP deployment
- allow automation to change milestone objectives

Task100 remains the Foundation Graduation milestone.

---

# 9. Bottom Line

The current best method is:

```text
GitHub as message bus.
Codex as repository maintainer.
QCLAW as builder.
ChatGPT as planner and reviewer.
Simon as founder and final approver.
```

Future automation should reduce Simon's manual coordination burden while preserving roadmap stability and repository truth.
