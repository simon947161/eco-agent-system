# ClimateOS Engineering Culture

**Status:** Culture Note v1.0  
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

# 6. Incentive Principle

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

# 7. Escalation Culture

Routine engineering problems should not be escalated to Simon.

The default escalation path is:

```text
QCLAW -> Codex -> ChatGPT -> Simon
```

Each level should solve what it can before escalating.

---

# 8. Evidence Culture

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

# 9. Manual Now, Automated Later

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

# 10. Operating Goal

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
