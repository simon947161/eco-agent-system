# Grok Build Adoption Matrix v0.1

**Project:** ClimateOS / Mission Control / Matrix / PRI  
**Status:** CANDIDATE ADOPTION REVIEW  
**Date:** 2026-07-22  
**Decision Authority:** Founder  
**Mode:** RFC-ONLY / NO AUTOMATIC ADOPTION

---

## 1. Decision Classes

- **ADOPT** — 原理和模式可直接进入 RFC 优先队列，但仍需 ClimateOS 自主实现
- **ADAPT** — 值得采用，但必须按 Evidence、Trust、Governance 要求改造
- **OBSERVE** — 继续跟踪，当前不进入近期路线图
- **REJECT** — 当前形式不适合 ClimateOS 或存在治理风险

---

## 2. Adoption Matrix

| ID | Capability | Decision | Priority | ClimateOS target | Rationale | Required safeguards |
|---|---|---|---:|---|---|---|
| AM-001 | Explicit mission/plan state machine | ADOPT | P0 | Mission Control | 清晰表达任务生命周期，支持恢复和审计 | 状态必须 machine-readable；允许 domain substates |
| AM-002 | Durable plan file | ADOPT | P0 | Mission Runtime | 计划可审查、可恢复、可迁移 | 扩展为 evidence-aware Mission Plan |
| AM-003 | Read-only planning phase | ADAPT | P0 | Governance Runtime | 减少误改和返工 | 必须覆盖 shell、MCP、subagent、external writes |
| AM-004 | Human approval before implementation | ADAPT | P0 | Founder Gate | 符合现有治理习惯 | 扩展为多级 gate，不只 approve/revise/quit |
| AM-005 | Persisted plan approval state | ADOPT | P0 | Mission Checkpoint | 支持跨进程和跨线程继续 | 决策记录需绑定 identity、time、revision |
| AM-006 | Transient-state normalization on restart | ADOPT | P0 | Recovery Runtime | 避免恢复到不安全的 in-flight 状态 | 明确 safe restart policy 和 recovery owner |
| AM-007 | Context reminder after compaction | ADOPT | P1 | Knowledge Runtime | 降低长任务中的状态漂移 | 提醒内容应由 mission state 自动生成 |
| AM-008 | Session-scoped governance state | ADOPT | P0 | Mission Control | 治理不能只存在提示词里 | 关键状态需独立于模型并持久化 |
| AM-009 | Tool registry and typed tool I/O | ADAPT | P0 | Matrix / Adapter Runtime | 有利于发现、路由、验证和审计 | 加入 identity、authority、evidence、risk、version |
| AM-010 | Agent builder/config separation | ADAPT | P1 | Agent Runtime | 有利于构造不同类型 Agent | 配置必须受 governance policy 约束 |
| AM-011 | Shared semantics across TUI/ACP/headless | ADAPT | P1 | PRI Interface Layer | 支持手机、桌面、Codex、CI 等多入口 | 所有入口必须共享同一 mission truth |
| AM-012 | User-triggered `/plan` interaction | OBSERVE | P2 | Mission Control UX | 简单直观，但不是核心架构 | 后续设计自然语言与 UI 双入口 |
| AM-013 | Inline plan comments | ADAPT | P1 | Founder Review UX | 提高局部修改效率 | 评论必须进入 decision log，不能只留在 UI |
| AM-014 | Approval with comments | ADAPT | P1 | Governance Runtime | 支持条件性批准 | 条件必须转为可验证 acceptance criteria |
| AM-015 | Parent and child agents use independent plan gates | REJECT | P0 risk | Multi-Agent Runtime | 子 Agent 可逃逸父任务只读门禁 | 强制继承 parent policy，例外需显式授权 |
| AM-016 | Write blocking limited to edit tools | REJECT | P0 risk | Security Runtime | shell redirection/MCP/external actions可能绕过 | sandbox、write-set、diff validation、protected paths |
| AM-017 | Always-approve remains armed below Plan Mode | REJECT | P0 risk | Permission Runtime | 退出规划后可能立即恢复高权限 | 每个阶段重新评估权限，不自动恢复高权限 |
| AM-018 | Plan schema centred on code files and tests | ADAPT | P0 | ClimateOS Mission Plan | 对软件开发有效，但不覆盖环境证据与政策风险 | 添加 geography、data lineage、uncertainty、impact、authority |
| AM-019 | Dedicated enter/exit plan tools | ADAPT | P1 | Mission Tool Contract | 生命周期动作明确 | 增加 actor identity、reason、revision、gate type |
| AM-020 | Plan state survives process restart | ADOPT | P0 | Mission Runtime | 长周期任务必需 | 与 ACTP/Handoff/Git revision 联合校验 |
| AM-021 | Research tasks skip Plan Mode and use subagents | REJECT AS RULE | P0 | Research Runtime | ClimateOS 研究同样可能高风险且需要计划 | 按风险和影响决定，而非按“研究/编码”二分 |
| AM-022 | Public monorepo slice as architecture evidence | OBSERVE | P1 | Strategic Radar | 有学习价值但证据不完整 | 固定 source revision，区分 confirmed/inferred/unknown |

---

## 3. Recommended Roadmap Placement

### Immediate RFC queue — P0

1. `MISSION_STATE_MACHINE_RFC_V0.1`
2. `MISSION_PLAN_CONTRACT_RFC_V0.1`
3. `MISSION_CHECKPOINT_BUNDLE_RFC_V0.1`
4. `PARENT_CHILD_CAPABILITY_ENVELOPE_RFC_V0.1`
5. `GOVERNED_TOOL_DISPATCH_ENVELOPE_RFC_V0.1`
6. `PROTECTED_WRITE_BOUNDARY_RFC_V0.1`

### P1

1. Matrix Tool/Skill/Agent Registry
2. Compaction-aware mission reminders
3. Conditional approval criteria
4. Shared session semantics across ChatGPT/Codex/CLI/ACP
5. Inline decision comments and evidence links

### Observe

1. TUI details
2. plugin UX
3. local model routing
4. public repository evolution
5. headless interface conventions

---

## 4. Proposed Task Placement

Because the current ClimateOS history already contains task ranges beyond 2000, task numbers must be allocated by Mission Control only after checking the authoritative current ledger. This document therefore proposes **work packages**, not invented task numbers.

| Work package | Suggested horizon | Dependency |
|---|---|---|
| WP-HARNESS-01 Mission State Machine | near-term | none |
| WP-HARNESS-02 Mission Plan Contract | near-term | WP-HARNESS-01 |
| WP-HARNESS-03 Checkpoint Bundle | near-term | 01–02 |
| WP-HARNESS-04 Tool Dispatch Envelope | near/mid | Matrix registry direction |
| WP-HARNESS-05 Parent-child governance | mid-term | Agent identity + permission model |
| WP-HARNESS-06 Multi-interface session semantics | mid-term | Mission Runtime stable |
| WP-HARNESS-07 UI/TUI experience | later | core governance complete |

---

## 5. Risk Assessment

### High

- Governance bypass through child agents
- Shell/external write bypass
- automatic restoration of elevated permission
- confusing documentation patterns with implemented runtime
- importing external abstractions before ClimateOS contracts are stable

### Medium

- over-engineering Mission Control too early
- fragmenting registries across Matrix and domain OS
- excessive state complexity
- human review fatigue

### Low

- adopting durable plan artifacts
- persisting approval state
- normalizing transient state on restart
- adding source revision and evidence grade

---

## 6. Founder Decision Gate

No item in this matrix authorizes implementation.

Founder may decide per item:

```text
APPROVE_FOR_RFC
REVISE
DEFER
REJECT
APPROVE_FOR_PROTOTYPE
```

Default state:

```text
PENDING_FOUNDER_RFC_PRIORITISATION
```

---

## 7. Recommended Decision

Recommended current decision:

```text
APPROVE_FOR_RFC:
- AM-001 to AM-010, subject to listed safeguards
- AM-020

CONTINUE_RESEARCH:
- AM-011 to AM-014
- AM-019
- AM-022

REJECT_AS-IS:
- AM-015 to AM-018
- AM-021
```

This approach absorbs the useful engineering discipline without importing Grok Build's governance gaps.

---

## 8. Status

```text
ADOPTION_MATRIX: COMPLETE_V0.1
ADOPT: 6
ADAPT: 10
OBSERVE: 2
REJECT / REJECT_AS_RULE: 4
RUNTIME_CHANGE: NONE
NEXT: MISSION_RUNTIME_RFC_V0.1
```
