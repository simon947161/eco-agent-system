# ClimateOS Existing Capability Crosswalk v0.1

**Project:** ClimateOS / Mission Control / Matrix / PRI  
**Status:** RESEARCH CROSSWALK  
**Date:** 2026-07-22  
**Mode:** EVIDENCE-CONSERVATIVE / RFC-ONLY

---

## 1. Purpose

将 Grok Build Agent Harness 与 Plan Mode 中观察到的能力，与 ClimateOS 当前已经形成的工程雏形进行对照，避免重复建设，也避免因外部框架而推翻既有路线。

本文件基于当前仓库研究文件、已完成任务链、ACTP/Handoff 工作方式及现有 Runtime 方向进行保守判断。未找到直接代码证据的能力标记为 `DOCUMENTED_PATTERN` 或 `PARTIAL`，不虚构实现完成度。

---

## 2. Maturity Labels

- `IMPLEMENTED` — 已存在可运行实现或明确代码证据
- `PARTIAL` — 已有部分实现，但合同、治理或覆盖范围不完整
- `DOCUMENTED_PATTERN` — 已形成稳定工作方法或文档协议，尚未固化为 Runtime
- `PLANNED` — 已进入架构或路线图
- `GAP` — 尚未形成可靠能力
- `UNKNOWN` — 当前证据不足

---

## 3. Crosswalk

| Grok Build capability | ClimateOS existing capability | Maturity | Assessment |
|---|---|---:|---|
| Agent Harness | Mission Control + ACTP task continuation | DOCUMENTED_PATTERN | 已能跨线程维持任务状态、分支、验证点和下一步，但尚未统一为可执行 Harness contract |
| Session lifecycle | ACTP / Handoff / task state documents | DOCUMENTED_PATTERN | 已具备恢复上下文的文档协议，缺少统一 machine-readable state machine |
| Plan Mode | Founder review gates、Draft PR、任务书审批 | PARTIAL | 已存在先计划后实施的治理习惯，但没有统一只读规划 Runtime |
| Durable plan artifact | Task brief、ACTP、Handoff、RFC 草案 | DOCUMENTED_PATTERN | 计划已持久化，但文件结构和字段尚未统一 |
| Approval UI/state | Founder accepted / pending review / draft states | PARTIAL | 决策状态已被记录，但不是统一审批状态机 |
| Tool registry | Source registry、adapter registry、model registry | PARTIAL | ClimateOS 已有多类 registry 思想，可扩展到 Tool/Skill/Agent Registry |
| Tool routing | Adapter Runtime / Hybrid Orchestrator | PARTIAL | 已面向气候模型和数据源形成编排雏形，尚未形成通用受治理工具信封 |
| Permission mode | Security、permission、network、audit contracts | PARTIAL | 1721–1780 已建立安全与审计方向，但需统一到 Agent capability envelope |
| Checkpoint/recovery | Git commit、PR、ACTP revision、cycle IDs | PARTIAL | 已具备人工可恢复基础，缺少统一 Mission Checkpoint Bundle |
| Context compaction | Handoff / context packet | DOCUMENTED_PATTERN | 已解决长线程迁移，但尚未自动生成和验证 |
| Long memory | Project memory、radar、monthly research program | PARTIAL | 已有长期项目记忆和周期研究，需区分 session/project/runtime/evidence memory |
| Subagents | 多线程、Codex delegation、Radar roles | DOCUMENTED_PATTERN | 已有实际委派模式，但缺少 parent-child accountability contract |
| Skills system | Task templates、radar workflows、domain methods | DOCUMENTED_PATTERN | 可复用能力存在，但未形成版本化 Skill Registry |
| MCP | Adapter Runtime / proposed MCP strategy | PLANNED | 方向明确，正式 server、contract、identity、permission 尚待建设 |
| Hooks | Radar cadence、monthly cycle、review triggers | DOCUMENTED_PATTERN | 已有周期触发规则，尚未形成通用 Hook Runtime |
| Headless execution | Codex task execution / GitHub workflow | PARTIAL | 有非交互执行实践，但缺乏统一任务协议和安全边界 |
| Multi-channel interface | ChatGPT、Codex、GitHub、local QGIS | PARTIAL | 多界面已存在，但缺少共享 session semantics |
| Evidence capture | Evidence Object / Trust Runtime direction | PLANNED/PARTIAL | 已上升为核心架构目标，需与每次 Agent action 绑定 |
| Governance runtime | Trust Runtime + Governance Runtime | PLANNED | 战略方向明确，是比 Grok Build 更强的差异化核心 |

---

## 4. Existing Strengths That Should Be Preserved

### 4.1 Evidence-first architecture

ClimateOS 已从 `AI + GIS + Climate Data` 升级为：

```text
Evidence + Trust + Governance Runtime
```

这是不能被通用 coding-agent 框架稀释的核心。

### 4.2 Founder review and controlled progression

现有任务链多次使用：

- Draft PR
- Human review pending
- Founder accepted
- no mainline change
- human verification deferred
- branch-specific evidence

这些已经构成 Governance Runtime 的原始材料。

### 4.3 Domain-specific registries

ClimateOS 已形成或规划：

- Model Registry
- Source Registry
- Adapter Readiness
- Evidence Object
- Radar system
- monthly/annual research cycle

因此无需复制外部通用 registry，而应将其统一到 Matrix。

### 4.4 Long-horizon mission continuity

ACTP、Handoff、context packets 与 Task sequence 已证明：系统能够跨线程、跨日期、跨工具持续推进。这一点比单次 coding session 更接近 PRI 的长期任务要求。

---

## 5. Main Gaps

### G-01 — No canonical Mission State Machine

当前状态词丰富但分散，例如：

- READY_FOR_FOUNDER_REVIEW
- DRAFT
- OPEN
- NOT_MERGED
- ACTIVE_AWAITING_FIRST_HUMAN_REVIEW
- ACCEPTED
- PASS

需要统一 machine-readable mission states，并允许 domain-specific substates。

### G-02 — No unified Mission Checkpoint Bundle

Git、ACTP、Handoff、validation evidence 分散存在。应统一为：

```text
mission.json
MISSION_PLAN.md
EVIDENCE_REGISTER.md
DECISION_LOG.md
VALIDATION_REPORT.md
RECOVERY_STATE.json
```

### G-03 — No governed parent-child delegation contract

Codex、ChatGPT、Radar、future subagents 之间尚无统一：

- identity
- authority
- write scope
- tool scope
- budget
- evidence duty
- recovery owner

### G-04 — No universal Skill contract

现有方法可复用，但尚不能被自动发现、版本控制、依赖解析和退役。

### G-05 — Tool execution not universally wrapped in evidence

未来每次重要调用应同时生成：

- intent
- input source
- permission basis
- output artifact
- validation
- provenance
- failure state

### G-06 — Planning and implementation boundaries are procedural, not enforced

当前依赖任务书与纪律。应逐步升级为 runtime-enforced read-only planning、protected paths 和 delegated capability envelopes。

---

## 6. Proposed Ownership Map

```text
Mission Control
├── Mission lifecycle
├── Planning and recovery
├── Agent dispatch
├── Founder gates
└── Cross-OS coordination

Matrix
├── Agent Registry
├── Skill Registry
├── Tool / MCP Registry
├── Capability Matrix
├── Permission Policy
└── Version / dependency graph

Domain OS
├── ClimateOS
├── BuildingOS
├── CarbonOS
├── WaterOS
├── EnergyOS
└── future WorldOS

Trust Runtime
├── identity
├── evidence
├── provenance
├── credential
└── audit

Governance Runtime
├── authority
├── review gate
├── policy
├── exception
└── release decision
```

---

## 7. Near-Term Reuse Candidates

1. Convert ACTP fields into a canonical `mission.json` schema.
2. Convert existing task briefs into `MISSION_PLAN.md` template.
3. Reuse Source Registry patterns for Tool/Skill Registry.
4. Reuse Evidence Object direction for tool-call evidence envelope.
5. Reuse Draft PR and Founder accepted states for approval state machine.
6. Reuse Handoff generation for automatic context checkpointing.
7. Reuse monthly research cycle for Hook Runtime design.

---

## 8. Conclusion

ClimateOS is not starting from zero. It already has substantial governance, evidence, continuity and registry primitives, but many remain document-driven rather than runtime-enforced.

The correct strategy is:

```text
Do not replace existing architecture.
Formalise existing patterns.
Add machine-readable contracts.
Enforce permissions and evidence.
Use Grok Build as comparative engineering evidence.
```

---

## 9. Status

```text
CROSSWALK: COMPLETE_V0.1
EXISTING_STRENGTHS: IDENTIFIED
PRIMARY_GAPS: IDENTIFIED
MAINLINE_CHANGE: NONE
NEXT: ADOPTION_MATRIX_AND_MISSION_RUNTIME_RFC
```
