# MISSION_RUNTIME_RFC_V0.1

**Project:** ClimateOS / BuildingOS / CarbonOS / WaterOS / EnergyOS / Mission Control / Matrix / PRI  
**Status:** DRAFT_FOR_FOUNDER_REVIEW  
**Version:** 0.1  
**Date:** 2026-07-23  
**Owner:** Mission Control  
**Decision Authority:** Founder  
**Mode:** RFC-ONLY / NO AUTOMATIC IMPLEMENTATION / NO MAINLINE RUNTIME CHANGE

---

## 0. Executive Decision Summary

本 RFC 提议建立一个跨 ClimateOS、BuildingOS、CarbonOS、WaterOS、EnergyOS 及未来 WorldOS 的 **Mission Runtime**。

Mission Runtime 不负责替代各 Domain OS 的专业推理，也不负责把外部 Agent 框架搬入 ClimateOS。其职责是为所有长期、复杂、跨线程、跨工具、跨 Agent 的任务提供统一的：

- 生命周期状态；
- 计划与审批；
- 检查点与恢复；
- 父子 Agent 权限继承；
- 工具调用治理；
- 写入边界与回滚；
- 证据与决策记录。

本 RFC 建议批准以下六项规范进入原型设计阶段，但不授权进入主线 Runtime：

1. `MISSION_STATE_MACHINE_RFC`
2. `MISSION_PLAN_CONTRACT_RFC`
3. `MISSION_CHECKPOINT_BUNDLE_RFC`
4. `PARENT_CHILD_CAPABILITY_ENVELOPE_RFC`
5. `GOVERNED_TOOL_DISPATCH_ENVELOPE_RFC`
6. `PROTECTED_WRITE_BOUNDARY_RFC`

建议 Founder 当前决策：

```text
APPROVE_FOR_PROTOTYPE_DESIGN
IMPLEMENTATION_AUTHORITY: NOT_GRANTED
MAINLINE_CHANGE: PROHIBITED
```

---

## 1. Problem Statement

ClimateOS 已经形成了大量 Mission Runtime 的雏形，包括：

- ACTP；
- Handoff；
- Context Packet；
- Task continuation；
- Founder review；
- Draft PR；
- Git revision checkpoint；
- Evidence Object；
- Source Registry；
- Model Registry；
- Adapter Runtime；
- Hybrid Orchestrator；
- Trust Runtime；
- 周期性 Radar 与长期研究计划；
- 人类验证延迟机制。

但这些能力目前分散在文档、线程、Git、人工工作流和不同 Runtime 之间，尚未形成统一的 machine-readable Mission Contract。

当前主要风险包括：

1. 任务状态依赖聊天上下文，容易随线程、压缩或模型切换发生漂移；
2. 计划、执行、验证、Founder 审批之间缺乏统一状态机；
3. 父 Agent 的治理边界不能保证对子 Agent 自动生效；
4. Tool、Shell、MCP、GitHub、外部系统写入缺乏统一调用信封；
5. 检查点通常只记录 Git commit，不能完整表达证据、权限、待验证事项和恢复条件；
6. ACTP 与 Handoff 有较强表达力，但仍主要由人阅读，难以被 Runtime 自动验证；
7. 高权限模式在任务阶段变化后可能被不恰当地恢复；
8. 研究任务、政策任务和环境任务不能仅套用软件编码式 Plan Mode。

Mission Runtime 的目标是将这些既有实践形式化，而不是推翻现有架构。

---

## 2. Design Principles

### 2.1 ClimateOS-first

所有规范必须服务 ClimateOS 自主架构，不绑定 Grok、OpenAI、Claude、Codex 或其他单一模型与平台。

### 2.2 Evidence before execution

任何影响数据、模型、代码、政策结论、环境判断或外部系统的任务，都应先声明证据需求和验证方式。

### 2.3 Governance is runtime state

治理状态不得只存在于提示词、聊天记忆或 UI 文案中，必须持久化为独立、可审计状态。

### 2.4 Least authority by phase

权限应随任务阶段动态收缩或扩展。进入下一阶段时，不自动恢复上一阶段的高权限。

### 2.5 Parent policy dominates

子 Agent、Skill、MCP Tool、Hook 与外部执行器不得获得高于父 Mission 的权限，除非经过显式且可审计的授权。

### 2.6 Recoverable by design

任何长期 Mission 都必须能够在进程重启、线程迁移、上下文压缩、模型更换和人工延迟后恢复。

### 2.7 Domain autonomy

Mission Runtime 只管理任务，不替代 ClimateOS、BuildingOS、WaterOS 等 Domain OS 的专业方法、证据标准与结论权威。

### 2.8 Human review proportional to risk

Founder Gate 和人工验证应基于影响、不可逆性、证据质量和权限风险，而不是所有任务一刀切。

---

## 3. Proposed Architecture

```text
PRI
│
├── Mission Control
│   ├── Mission State Machine
│   ├── Planning Runtime
│   ├── Checkpoint and Recovery
│   ├── Founder / Human Gates
│   └── Cross-OS Coordination
│
├── Matrix
│   ├── Agent Registry
│   ├── Skill Registry
│   ├── Tool / MCP Registry
│   ├── Capability Matrix
│   ├── Permission Policy
│   └── Version / Dependency Graph
│
├── Governance and Trust
│   ├── Identity
│   ├── Authority
│   ├── Evidence
│   ├── Provenance
│   ├── Risk
│   └── Audit
│
└── Domain OS Runtimes
    ├── ClimateOS
    ├── BuildingOS
    ├── CarbonOS
    ├── WaterOS
    ├── EnergyOS
    └── Future WorldOS
```

Mission Runtime 应位于 Mission Control 与 Matrix 的交界处：

- Mission Control 负责运行任务；
- Matrix 负责声明能力与权限；
- Trust Runtime 负责身份、证据与权威；
- Domain OS 负责专业判断和执行语义。

---

# Part A — MISSION_STATE_MACHINE_RFC

## 4. Mission State Machine

### 4.1 Required Core States

```text
DRAFT
RESEARCHING
PLANNING
AWAITING_APPROVAL
APPROVED_FOR_EXECUTION
EXECUTING
AWAITING_HUMAN_VALIDATION
VALIDATING
BLOCKED
PAUSED
RECOVERING
COMPLETED
REJECTED
CANCELLED
ARCHIVED
```

### 4.2 State Meaning

| State | Meaning |
|---|---|
| `DRAFT` | Mission 已建立，但尚未进入正式研究或计划 |
| `RESEARCHING` | 正在建立来源、事实、现状和约束 |
| `PLANNING` | 正在形成可执行计划，默认禁止未授权主线写入 |
| `AWAITING_APPROVAL` | 计划或关键阶段等待 Founder/授权人决策 |
| `APPROVED_FOR_EXECUTION` | 已批准执行，但尚未开始 |
| `EXECUTING` | 正在执行已批准范围 |
| `AWAITING_HUMAN_VALIDATION` | 自动工作完成，但需要人类现实检查 |
| `VALIDATING` | 正在进行测试、证据核验、现场检查或审查 |
| `BLOCKED` | 因依赖、证据、权限、技术或外部条件无法前进 |
| `PAUSED` | 有意暂停，可安全恢复 |
| `RECOVERING` | 从中断、失败、上下文迁移或状态不一致中恢复 |
| `COMPLETED` | 已达到验收标准 |
| `REJECTED` | 计划或成果被拒绝，不应继续执行 |
| `CANCELLED` | Mission 被主动终止 |
| `ARCHIVED` | Mission 已封存，仅供检索与审计 |

### 4.3 Mandatory Transition Rules

1. `PLANNING → EXECUTING` 不得直接发生，必须经过 `AWAITING_APPROVAL` 和 `APPROVED_FOR_EXECUTION`，除非 Mission 明确属于预批准低风险类别。
2. `EXECUTING → COMPLETED` 必须满足 acceptance criteria；高风险 Mission 应经过 `VALIDATING`。
3. 所有不可逆写入、外部发布、合并、发送、删除、政策结论发布和真实环境行动，应具有单独 gate。
4. `BLOCKED` 必须记录 blocker owner、解除条件和最后检查时间。
5. `RECOVERING` 不得继承未确认的 in-flight 权限。
6. 恢复时所有瞬态状态必须归一化到安全状态。

### 4.4 Safe Restart Policy

进程、线程或 Agent 重启后：

| Previous state | Restart state |
|---|---|
| `EXECUTING` | `RECOVERING` |
| `VALIDATING` | `RECOVERING` |
| `AWAITING_APPROVAL` | 保持，但重新核验 approval record |
| `PLANNING` | 保持，只读边界继续生效 |
| `APPROVED_FOR_EXECUTION` | 保持，但重新计算权限和 source revision |
| `BLOCKED` | 保持 |
| `PAUSED` | 保持 |
| `COMPLETED` | 保持，只读 |

### 4.5 Domain Substates

Domain OS 可以扩展子状态，例如：

```text
ClimateOS:
DATA_ACQUISITION
MODEL_EVALUATION
PHYSICAL_CONSISTENCY_REVIEW
EVIDENCE_SYNTHESIS

BuildingOS:
CODE_REVIEW
DESIGN_REVIEW
COMPLIANCE_CHECK
DOCUMENTATION_FREEZE

WaterOS:
CATCHMENT_REVIEW
WATER_QUALITY_VALIDATION
FIELD_INSPECTION_PENDING
```

Domain substate 不得绕过核心 Mission State Machine。

---

# Part B — MISSION_PLAN_CONTRACT_RFC

## 5. Mission Plan Contract

### 5.1 Purpose

Mission Plan 不只是实现步骤，而是对目的、证据、范围、权限、影响、验证和恢复方式的正式声明。

### 5.2 Required Fields

```yaml
mission_id: string
mission_title: string
mission_version: string
project_scope: []
owner: string
decision_authority: string
created_at: datetime
updated_at: datetime
current_state: enum
risk_class: LOW | MEDIUM | HIGH | CRITICAL

context:
  problem_statement: string
  why_now: string
  existing_capabilities: []
  constraints: []

objectives:
  primary: []
  non_goals: []

research_basis:
  source_register: []
  source_revision: []
  evidence_grade: []
  confirmed: []
  inferred: []
  unknown: []

execution_plan:
  stages: []
  dependencies: []
  critical_paths: []
  expected_outputs: []

capability_requirements:
  agents: []
  skills: []
  tools: []
  mcp_servers: []
  external_systems: []

permission_request:
  read_scope: []
  declared_write_set: []
  network_scope: []
  external_actions: []
  prohibited_actions: []

validation:
  acceptance_criteria: []
  tests: []
  evidence_obligations: []
  human_validation: []

recovery:
  checkpoint_frequency: string
  rollback_method: string
  recovery_owner: string
  safe_stop_conditions: []

approval:
  required_gates: []
  decision_records: []
```

### 5.3 Plan Classes

| Class | Use case | Default boundary |
|---|---|---|
| `MICRO_PLAN` | 清晰、低风险、短任务 | 可预批准 |
| `STANDARD_PLAN` | 多步骤任务 | 执行前审批 |
| `ARCHITECTURE_PLAN` | 架构与跨系统变化 | Founder Gate |
| `RESEARCH_PLAN` | 高影响研究、政策、环境或标准研究 | Evidence Gate |
| `FIELD_ACTION_PLAN` | 真实世界现场、设备、环境或人员行动 | Human validation required |
| `RELEASE_PLAN` | 发布、合并、部署、对外发送 | Release Gate |

### 5.4 Planning Boundary

进入 `PLANNING` 后：

允许：

- 读取仓库和文档；
- 搜索与研究；
- 创建或修改 Mission Plan；
- 创建研究笔记和 RFC 草稿；
- 运行明确声明为只读的分析；
- 形成候选 diff，但不应用。

默认禁止：

- 修改主线 Runtime；
- 合并 PR；
- 发布或部署；
- 删除或覆盖数据；
- 发送外部消息；
- 修改外部系统；
- 子 Agent 绕过父 Mission 权限；
- Shell、MCP 或 Hook 进行未声明写入。

---

# Part C — MISSION_CHECKPOINT_BUNDLE_RFC

## 6. Mission Checkpoint Bundle

### 6.1 Purpose

Checkpoint 不应只是 Git commit。它必须足以让另一个 Agent、线程或人类在不了解前文的情况下安全恢复 Mission。

### 6.2 Required Bundle

```yaml
checkpoint_id: string
mission_id: string
checkpoint_version: string
created_at: datetime
created_by:
  actor_id: string
  actor_type: HUMAN | AGENT | SYSTEM

mission_state:
  current_state: enum
  domain_substate: string
  state_reason: string

repository_state:
  repositories: []
  branches: []
  commits: []
  working_tree_status: []
  open_prs: []

plan_state:
  plan_revision: string
  approved_scope: []
  unapproved_scope: []
  pending_comments: []

execution_state:
  completed_steps: []
  current_step: string
  pending_steps: []
  blockers: []

validation_state:
  tests_run: []
  evidence_collected: []
  human_checks_pending: []
  known_failures: []

permission_state:
  active_capability_envelope: string
  elevated_permissions: []
  revoked_permissions: []

recovery_state:
  resume_instruction: string
  rollback_point: string
  unsafe_assumptions: []
  next_safe_action: string

handoff:
  summary: string
  next_thread_read_order: []
  founder_action_required: boolean
```

### 6.3 ACTP and Handoff Integration

现有 ACTP 与 Handoff 保留，但应逐步分为：

- **Human-readable layer:** Markdown；
- **Machine-readable layer:** YAML/JSON；
- **Evidence links:** Git、数据、测试、图片、日志、外部来源；
- **Decision links:** Founder approval、review comments、validation record。

### 6.4 Checkpoint Trigger

应在以下情况自动或半自动生成 Checkpoint：

- 状态转换；
- 线程迁移；
- 上下文压缩；
- Agent 切换；
- PR 创建或合并前后；
- 人类验证前后；
- 风险等级变化；
- Blocked 或 Recovery；
- 每个重要 Work Package 完成时。

---

# Part D — PARENT_CHILD_CAPABILITY_ENVELOPE_RFC

## 7. Parent–Child Capability Envelope

### 7.1 Core Rule

```text
Child Effective Authority
=
minimum(
  Parent Mission Authority,
  Child Agent Definition,
  Task-specific Grant,
  Tool Policy,
  Environment Policy
)
```

子 Agent 的有效权限不得高于任何上层约束。

### 7.2 Required Envelope

```yaml
child_agent_id: string
parent_mission_id: string
parent_agent_id: string
agent_type: string
purpose: string

allowed_capabilities:
  read: []
  analyze: []
  propose: []
  write: []
  execute: []
  network: []

prohibited_capabilities: []

resource_budget:
  token_budget: string
  time_budget: string
  tool_call_budget: integer
  concurrency_limit: integer

workspace:
  allowed_paths: []
  protected_paths: []
  isolated_branch: string
  temporary_workspace: string

output_contract:
  expected_artifacts: []
  evidence_required: []
  acceptance_criteria: []

failure_policy:
  retry_limit: integer
  escalation_to: string
  safe_stop_conditions: []
  cleanup_required: boolean
```

### 7.3 Mandatory Inheritance

子 Agent 必须继承：

- Mission state；
- planning boundary；
- prohibited actions；
- declared write set；
- network restrictions；
- evidence obligations；
- risk class；
- Founder Gate；
- protected paths；
- external communication restrictions。

### 7.4 Delegation Rules

1. 子 Agent 不得自行生成权限更高的孙 Agent。
2. 子 Agent 不得修改自己的 Capability Envelope。
3. 任何权限扩张必须返回父 Mission，并形成新的 decision record。
4. 探索型 Agent 默认只读。
5. 写入型 Agent 应使用隔离分支或临时 workspace。
6. 子 Agent 输出必须由父 Mission 验收后才可进入正式成果。

---

# Part E — GOVERNED_TOOL_DISPATCH_ENVELOPE_RFC

## 8. Governed Tool Dispatch Envelope

### 8.1 Purpose

每一次高影响 Tool、MCP、Shell、GitHub、文件、网络或外部系统调用都应具有统一的调用信封。

### 8.2 Required Envelope

```yaml
dispatch_id: string
mission_id: string
actor_id: string
agent_id: string
stage: string

tool:
  registry_id: string
  name: string
  version: string
  provider: string

intent:
  purpose: string
  expected_result: string
  necessity: string

scope:
  read_targets: []
  write_targets: []
  network_targets: []
  external_recipients: []

risk:
  risk_class: LOW | MEDIUM | HIGH | CRITICAL
  reversible: boolean
  side_effects: []
  failure_modes: []

permission:
  policy_id: string
  approval_record: string
  expires_at: datetime

evidence:
  expected_evidence: []
  output_capture: string
  provenance_required: boolean

recovery:
  rollback_action: string
  compensating_action: string
  escalation_owner: string
```

### 8.3 Dispatch Decision

Tool Dispatch Runtime 应返回：

```text
ALLOW
ALLOW_WITH_CONDITIONS
REQUIRE_APPROVAL
DENY
QUARANTINE
```

### 8.4 High-impact Actions

以下调用默认至少为 `REQUIRE_APPROVAL`：

- 合并 PR；
- push 到受保护分支；
- 删除文件或数据；
- 发布网站、模型、报告或政策结论；
- 发送邮件或外部消息；
- 修改日历、第三方平台或生产系统；
- 调用真实设备、传感器、基础设施或现场执行系统；
- 更改 Agent、Skill、MCP、权限或安全配置；
- 导出敏感数据；
- 触发不可逆自动化。

### 8.5 Tool Registry Relationship

Matrix 中每个 Tool/MCP 应登记：

- identity；
- owner；
- version；
- input/output schema；
- permission class；
- side-effect class；
- supported rollback；
- evidence behavior；
- known failure modes；
- deprecation state。

---

# Part F — PROTECTED_WRITE_BOUNDARY_RFC

## 9. Protected Write Boundary

### 9.1 Purpose

保护边界必须覆盖所有写入路径，而不只是标准编辑工具。

### 9.2 Write Channels in Scope

- File edit/create/delete；
- Shell redirection；
- scripts and subprocesses；
- Git operations；
- MCP writes；
- database writes；
- API mutations；
- Hooks；
- plugins；
- subagents；
- generated code execution；
- external cloud or SaaS writes。

### 9.3 Required Controls

1. **Declared Write Set**：执行前声明允许修改的路径、资源和系统。
2. **Protected Paths**：主线 Runtime、密钥、治理文件和关键数据默认受保护。
3. **Workspace Isolation**：高风险任务在分支、沙箱或临时工作区执行。
4. **Command Classification**：Shell 命令按只读、可逆写入、高风险写入分类。
5. **Pre-action Snapshot**：高风险写入前生成检查点。
6. **Post-action Diff**：执行后检查 Git diff、文件变化和外部系统结果。
7. **Unexpected Write Detection**：发现未声明写入时立即停止并进入 `BLOCKED` 或 `RECOVERING`。
8. **Rollback Contract**：每个高风险写入必须声明回滚或补偿动作。
9. **No implicit privilege restoration**：退出规划或验证阶段后，不自动恢复高权限。
10. **Audit Record**：记录 actor、time、scope、reason、result 和 evidence。

### 9.4 Protected Categories

```text
P0_PROTECTED:
- main / production branches
- security and permission policy
- identity and credential material
- authoritative evidence records
- production datasets
- release and deployment configuration

P1_PROTECTED:
- Runtime contracts
- model and source registries
- MCP and tool registry
- automated hooks
- public reports and websites

P2_CONTROLLED:
- research notes
- RFC drafts
- non-authoritative prototypes
- temporary outputs
```

---

## 10. Founder and Human Gate Model

### 10.1 Gate Types

```text
RESEARCH_GATE
PLAN_GATE
ARCHITECTURE_GATE
DATA_GATE
MODEL_GATE
FIELD_GATE
SECURITY_GATE
RELEASE_GATE
FOUNDER_GATE
```

### 10.2 Decision Types

```text
APPROVE
APPROVE_WITH_CONDITIONS
REQUEST_REVISION
DEFER
REJECT
CANCEL
```

### 10.3 Decision Record

```yaml
decision_id: string
mission_id: string
gate_type: string
decision: string
decided_by: string
decided_at: datetime
scope: []
conditions: []
evidence_reviewed: []
expires_at: datetime
supersedes: string
```

条件性批准必须转换为可验证的 acceptance criteria，不能只留作自然语言备注。

---

## 11. Risk Classification

### LOW

- 可逆；
- 无外部副作用；
- 不影响权威数据或主线；
- 不需要敏感权限。

### MEDIUM

- 有限写入；
- 可通过 Git 或版本恢复；
- 对局部项目产生影响；
- 需要标准验证。

### HIGH

- 跨仓库或跨 OS；
- 影响主线 Runtime、公开成果、政策结论或重要数据；
- 使用子 Agent、MCP、Shell 或外部系统写入；
- 需要 Founder 或专业人员验证。

### CRITICAL

- 不可逆现实影响；
- 涉及人身安全、基础设施、环境行动、法律合规、敏感身份或重大财务；
- 需要多重审批与独立验证；
- 自动执行默认禁止。

---

## 12. Integration with Existing ClimateOS Practices

| Existing capability | Mission Runtime integration |
|---|---|
| ACTP | Human-readable Checkpoint Bundle |
| Handoff.md | Thread migration and recovery layer |
| Context Packet | Mission context snapshot |
| Founder Review | Founder Gate implementation |
| Draft PR | Isolated execution and review surface |
| Git commit | Repository state checkpoint component |
| Evidence Object | Mission evidence obligation |
| Source Registry | Research basis and provenance |
| Model Registry | Model identity and version control |
| Adapter Runtime | Governed external tool/data interface |
| Hybrid Orchestrator | Future governed dispatch participant |
| Trust Runtime | Identity, authority, evidence and audit foundation |
| Radar | Recurring research Mission source |
| Human validation queue | `AWAITING_HUMAN_VALIDATION` state |

本 RFC 的方向是统一这些能力，而不是重新创建平行体系。

---

## 13. Non-goals

本 RFC 不授权：

- 复制 Grok Build 代码；
- 采用 Grok 模型；
- 替换现有 ACTP/Handoff；
- 修改当前 ClimateOS 主线 Runtime；
- 自动创建新的 Task 编号；
- 自动启用多 Agent 写入；
- 自动开启 always-approve；
- 自动部署或发布；
- 将所有任务强制变成复杂状态机；
- 在没有 Founder Gate 的情况下进入生产实现。

---

## 14. Proposed Prototype Sequence

### Phase 0 — Specification Validation

交付：

- Schema review；
- State transition review；
- Existing ACTP/Handoff mapping；
- Security threat review；
- Founder feedback record。

### Phase 1 — Documentation-only Prototype

交付：

- `mission.yaml` example；
- `checkpoint.yaml` example；
- `capability-envelope.yaml` example；
- `tool-dispatch.yaml` example；
- Markdown rendering；
- no runtime enforcement。

### Phase 2 — Validator Prototype

交付：

- schema validation；
- invalid transition detection；
- missing approval detection；
- declared write set validation；
- checkpoint completeness report。

### Phase 3 — Read-only Mission Runtime Prototype

交付：

- Mission loading；
- state display；
- recovery instruction generation；
- context reminder generation；
- no autonomous writes。

### Phase 4 — Controlled Sandbox Enforcement

交付：

- protected path enforcement；
- isolated branch/workspace；
- post-action diff；
- child capability inheritance；
- human approval simulation。

### Phase 5 — Candidate Integration

仅在 Founder 明确批准后，选择一个低风险、非主线案例进行试点。

---

## 15. Candidate Pilot

建议首个试点不要选择高风险 ClimateOS 主线，而选择：

```text
PILOT TYPE: Documentation and research Mission
SCOPE: Grok Build research continuation
WRITE AREA: docs/mission-control/research/grok-build/
EXTERNAL SIDE EFFECTS: none
RUNTIME CHANGE: none
```

试点验证：

- Mission state 是否清晰；
- Checkpoint 是否足够恢复；
- Founder Gate 是否产生过多负担；
- Tool dispatch envelope 是否过重；
- ACTP/Handoff 是否能平滑映射；
- 手机端参与是否仍然容易。

---

## 16. Success Criteria

本 RFC 成功需满足：

1. 任何新线程能够在不依赖聊天记忆的情况下恢复 Mission；
2. 计划、批准、执行、验证和完成状态可机器读取；
3. 子 Agent 无法绕过父 Mission 权限；
4. Shell、MCP、Hooks 和外部 API 写入均受统一边界治理；
5. 每个高影响动作可追溯至身份、授权、目的、范围与证据；
6. 现有 ACTP、Handoff、Evidence 和 Trust Runtime 被整合而非废弃；
7. 低风险任务不会因治理框架变得笨重；
8. Founder 可以清楚知道什么已经完成、什么需要自己验证、什么尚未获准；
9. ClimateOS 保持独立于任何单一模型或 Agent 平台；
10. Runtime 能够支持未来 BuildingOS、WaterOS、EnergyOS 和 WorldOS。

---

## 17. Open Questions

1. Mission truth 的权威存储应位于 Git、SQLite、JSON/YAML 文件还是组合结构？
2. Matrix Registry 与各 Domain OS Registry 的边界如何划分？
3. 哪些低风险 Mission 可以获得预批准？
4. Founder Gate 如何避免审查疲劳？
5. 多人、多 Agent 环境中的 decision authority 如何委派？
6. 如何对外部 SaaS 和不可回滚 API 实现补偿事务？
7. 真实环境任务应如何接入专业人员签字和现场证据？
8. Mission State Machine 是否需要 event-sourced ledger？
9. 手机端应呈现完整状态还是简化 Observer Card？
10. 如何在不泄露敏感信息的情况下共享 Mission Checkpoint？

---

## 18. Threat Model Summary

| Threat | Proposed mitigation |
|---|---|
| Child agent bypass | Mandatory parent envelope inheritance |
| Shell write bypass | Sandbox + declared write set + post-run diff |
| MCP external mutation | Governed Tool Dispatch Envelope |
| Stale approval | Approval revision binding and expiry |
| Context loss | Durable checkpoint and state reminder |
| Permission rebound | Recalculate authority at every transition |
| Hidden side effects | Tool registry side-effect classification |
| False completion | Acceptance criteria and evidence obligations |
| Human review fatigue | Risk-proportional gates and pre-approved low-risk classes |
| Framework lock-in | Model- and platform-neutral contracts |

---

## 19. Decision Request

Founder is asked to choose one of:

```text
A. APPROVE_FOR_PROTOTYPE_DESIGN
B. APPROVE_WITH_CONDITIONS
C. REQUEST_REVISION
D. DEFER
E. REJECT
```

Recommended:

```text
A. APPROVE_FOR_PROTOTYPE_DESIGN
```

This approval would authorize only Phase 0–2 documentation and validator design.

It would not authorize:

- mainline Runtime modification；
- autonomous Agent execution；
- production enforcement；
- public release；
- deployment；
- merge into protected runtime paths。

---

## 20. Proposed Next Deliverables

Upon approval for prototype design:

1. `MISSION_RUNTIME_SCHEMA_V0.1.yaml`
2. `MISSION_CHECKPOINT_SCHEMA_V0.1.yaml`
3. `PARENT_CHILD_CAPABILITY_ENVELOPE_SCHEMA_V0.1.yaml`
4. `GOVERNED_TOOL_DISPATCH_SCHEMA_V0.1.yaml`
5. `MISSION_RUNTIME_EXAMPLE_GROK_RESEARCH_V0.1.yaml`
6. `MISSION_RUNTIME_VALIDATOR_REQUIREMENTS_V0.1.md`
7. `MISSION_RUNTIME_THREAT_MODEL_V0.1.md`

No Task numbers should be assigned until Mission Control checks the authoritative current task ledger.

---

## 21. Status

```text
RFC: MISSION_RUNTIME_RFC_V0.1
STATUS: DRAFT_FOR_FOUNDER_REVIEW
RUNTIME_CHANGE: NONE
MAINLINE_CHANGE: NONE
IMPLEMENTATION_AUTHORITY: NOT_GRANTED
RECOMMENDED_DECISION: APPROVE_FOR_PROTOTYPE_DESIGN
NEXT: SCHEMA_AND_VALIDATOR_DESIGN_AFTER_FOUNDER_GATE
```

---

## 22. CRP Harvest Block

### 核心知识点

- Mission Runtime 的核心不是 Agent UI，而是状态、权限、证据、恢复和责任链。
- ClimateOS 已拥有 ACTP、Handoff、Evidence、Trust、Registry 等大量基础能力。
- 外部框架值得借鉴的是持久化状态和工程纪律，而不是平台绑定实现。

### 想法点

- 将 ACTP 与 Handoff 升级为 Human-readable + Machine-readable 双层 Checkpoint。
- 将 Matrix 建设为 Agent、Skill、Tool、MCP、权限和版本注册中心。
- 将 Mission Control 建设为跨 Domain OS 的 Harness。

### 愿望点

- 手机端只需看到清晰状态、下一步和需要 Founder 处理的事项。
- 长期任务可以跨线程、跨 Agent、跨模型持续推进。
- ClimateOS 能吸收全球优秀 Agent Engineering，而保持自主架构。

### 推理点

- 单纯 Plan Mode 无法治理 Shell、MCP、Hooks 和子 Agent，因此必须升级为 Runtime Policy。
- Git commit 不能独立承担完整 Mission Checkpoint。
- 权限必须随阶段重新计算，不能自动回弹。

### 关键决策

- 六项核心规范统一进入一个 Mission Runtime RFC。
- 当前仅建议批准原型设计，不授权主线实现。
- 父 Mission 政策必须强制覆盖所有子 Agent 与写入通道。

### 未解决问题

- Mission truth 的权威存储形式。
- Matrix 与 Domain Registry 的边界。
- Founder Gate 的负担控制。
- 外部系统不可逆写入的补偿机制。

### 下一步行动

- Founder Review。
- 获批后生成四个 YAML Schema、示例 Mission、Validator Requirements 和 Threat Model。

### 项目关联关键词

`Mission Runtime` `Mission Control` `Matrix` `PRI` `ACTP` `Handoff` `Checkpoint` `Founder Gate` `Agent Harness` `Capability Envelope` `Tool Dispatch` `Protected Write Boundary` `ClimateOS` `BuildingOS` `WaterOS` `EnergyOS`
