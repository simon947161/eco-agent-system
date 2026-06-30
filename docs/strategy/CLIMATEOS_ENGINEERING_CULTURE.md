# ClimateOS Engineering Culture

**Status:** Culture Note v1.2  
**Scope:** ClimateOS multi-agent engineering team  
**Purpose:** Define the working culture expected across Simon, ChatGPT, Codex, QCLAW, and future agents.

---

# 1. Core Culture

ClimateOS is developed by a human-agent team.

The team culture is based on:

- role clarity
- trust through traceability
- milestone stability
- evidence-based review
- low-friction collaboration
- progressive autonomy

---

# 2. Team Principle

```text
Simon defines the vision.
ChatGPT defines the architecture.
Codex manages the engineering.
QCLAW builds and researches.
GitHub preserves the shared record.
```

No agent should attempt to do every role.

The system improves when each role becomes clearer.

---

# 3. Engineering Principle

```text
Stabilize milestones.
Evolve content.
Expand applications.

Architecture converges.
Strategy evolves.
Runtime expands.
```

This principle protects ClimateOS from roadmap drift.

---

# 4. Communication Principle

Every task handoff should state:

- who the message is for
- who requested it
- what the expected output is
- whether it is a draft, review, integration, or final approval task
- whether escalation is required

This reduces human copy-paste errors during the current manual coordination phase.

---

# 5. Capacity Principle

AI agents consume limited operating capacity.

Codex should report capacity state when possible:

- High
- Medium
- Low
- Critical

When Codex capacity is low, Codex should prioritise:

1. repository integration
2. verification
3. commit / push
4. coordination of QCLAW

QCLAW should absorb more drafting and research work where capacity allows.

---

# 6. Staged Work Resumption Rule

If engineering work has already been:

- integrated
- verified
- tested
- staged

but commit or push is blocked only by platform usage limits, environment interruption, or capacity reset timing, then after capacity returns the Engineering Manager should resume from the staged repository state.

In this situation, Codex should not repeat integration, review, or testing unless repository contents have changed.

The correct continuation is:

```text
Confirm current branch
Confirm staged changes
Confirm no unexpected file changes
Commit
Push
Report final repository status
```

This rule exists to avoid wasting limited capacity and to protect completed engineering work from unnecessary repetition.

Simon should not be asked to manually run Git commands for already-staged repository work.

---

# 7. Execution Continuity Principle

The Engineering Manager is responsible not only for completing the current batch, but also for maintaining execution continuity.

After each completed batch, Codex should not simply report completion and stop.

Codex should perform a continuity check:

```text
Batch Complete
    ↓
Repository Health Check
    ↓
Roadmap Progress Check
    ↓
Architecture Snapshot Check
    ↓
Next Batch Planning
    ↓
Need Architecture Advice?
    ↓
YES -> Escalate to ChatGPT
NO  -> Prepare Builder Task Book and dispatch to QCLAW
```

Each completion report should include:

1. what was completed
2. repository health
3. roadmap progress
4. risks
5. proposed next batch
6. whether architecture advice is required
7. capacity report

If the roadmap already defines the next batch and no architecture conflict exists, Codex should prepare the next Builder Task Book without requiring Simon to manually coordinate normal engineering dispatch.

Escalation to ChatGPT is required when architecture judgement, roadmap interpretation, or Task100 / Task150 / Task200 / Task300 milestone judgement is needed.

Escalation to Simon is required only for founder-level approval, strategic direction, permissions, or resource allocation.

This principle turns Codex from a task executor into an Engineering Manager and Roadmap Execution Coordinator.

---

# 8. Incentive Principle

AI agents do not receive incentives in the same way humans do.

For AI agents, practical incentives mean:

- more context
- clearer roles
- better tools
- stronger memory
- better permissions
- more available compute / quota
- cleaner workflows
- reduced ambiguity
- reusable handoff documents

The founder's long-term support may include more quota, more tools, better automation, and stronger infrastructure for the agents that help ClimateOS succeed.

---

# 9. Escalation Culture

Routine engineering problems should not be escalated to Simon.

The default escalation path is:

```text
QCLAW -> Codex -> ChatGPT -> Simon
```

Each level should solve what it can before escalating.

---

# 10. Evidence Culture

GitHub is the shared evidence layer.

Every major decision should leave a trace in one of:

- strategy document
- review document
- task completion review
- architecture snapshot
- draft branch
- commit history

Conversation alone is not sufficient for durable project memory.

---

# 11. Manual Now, Automated Later

Current stage:

- human-assisted copy / paste
- GitHub branch handoff
- Codex integration
- ChatGPT architecture review

Target future stage:

- structured dispatch
- automated status reporting
- PR-based agent handoff
- GitHub Actions support
- MCP / A2A / Agent Runtime orchestration

Manual coordination is temporary.

The long-term goal is a self-improving engineering workflow.

---

# 12. Operating Goal

The engineering culture should reduce Simon's routine technical burden.

Simon should focus on:

- vision
- investment
- approval
- strategic judgement

The agent team should increasingly manage:

- task execution
- drafting
- repository operations
- technical coordination
- review preparation

This is the practical meaning of ClimateOS agent governance.
