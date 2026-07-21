# MISSION_GROK_BUILD_RESEARCH.md

**Project:** ClimateOS / BuildingOS / Mission Control  
**Status:** RESEARCH APPROVED  
**Priority:** HIGH  
**Owner:** Mission Control  
**Date:** 2026-07-22  
**Execution Mode:** RESEARCH-ONLY / RFC-ONLY / NO MAINLINE CHANGE

---

## Mission

对 Grok Build（官方定位为终端式 AI 编码 Agent、Agent Harness 与 TUI）开展系统性研究，提炼其中能够提升 ClimateOS、BuildingOS、CarbonOS 及未来 WorldOS 的工程思想，形成可复用架构，而不是复制其具体实现。

本任务以学习 **Agent Engineering** 为目标，不以迁移到 Grok 模型为目标。

---

## 一、研究原则

- 学习架构，不照搬代码。
- 学习工作流，不绑定模型。
- 学习思想，不依赖平台。
- 保持 ClimateOS 独立演化路线。
- 优先研究公开文档、公开源码、官方说明与可验证行为。
- 将“框架设计”和“模型能力”严格分开评估。

重点关注 Grok Build 的工程设计，而非 Grok 模型本身。

---

## 二、重点研究内容（P0）

### 1. Agent Harness

研究 Agent 生命周期、Task Dispatch、Context Management、Tool Routing、Error Recovery、Planning Runtime、Headless / Interactive Execution Boundary、Human Approval Boundary。

输出：《ClimateOS Agent Harness 对照分析》

### 2. Plan Mode

分析复杂任务拆分、执行计划、阶段验收、任务恢复、中断与回滚、计划与实际执行偏差。

输出：《Mission Planning Runtime Proposal》

### 3. Skills System

研究 Skill 定义、生命周期、Registry、Discovery、Versioning、Dependency、Permission Boundary、Evaluation 与 Deprecation。

输出：《ClimateOS Skills Runtime v1》

### 4. AGENTS.md / Repository Rules

分析 Repository Rule、Folder Rule、Project Rule、Local Rule、Rule Precedence、Conflict Resolution 与 Human Override。

适用对象：ClimateOS、BuildingOS、CarbonOS、Dryland、Kunlun EPI。

输出：《Repository Governance Proposal》

### 5. MCP

研究 Tool Adapter、MCP Server、Context Sharing、External Tool Contract、Capability Discovery、Trust Boundary、Failure Isolation 与 Auditability。

输出：《ClimateOS MCP Strategy》

### 6. Memory

分析 Session Memory、Long Memory、Project Memory、Agent Memory、Evidence Memory、Decision Memory、Expiry、Correction 与 Provenance。

重点比较：Mission Control Memory vs ClimateOS Runtime Memory。

输出：《Memory Runtime Review》

### 7. Hooks

研究自动触发、Git Hook、Review Hook、Validation Hook、Documentation Hook、Security Hook、Evidence Capture Hook 与 Founder Approval Hook。

输出：《Automation Hook Proposal》

### 8. Sub Agents

分析并行 Agent、Delegation、Recovery、Coordination、Workspace Isolation、Shared Context Boundary、Conflict Resolution 与 Parent–Child Accountability。

输出：《Multi-Agent Runtime Proposal》

---

## 三、P1 研究内容

- Headless Runtime
- Terminal UI
- CLI UX
- Plugin System
- Config Runtime
- Local-first Workflow
- Remote Workflow
- Security Model
- Agent Client Protocol（ACP）
- Editor Integration
- CI / Automation Integration
- Observability and Execution Trace

---

## 四、禁止事项

Mission Control 不应：

- 复制 Grok Build 代码。
- 将 ClimateOS 绑定到 Grok 模型。
- 因学习新框架而推翻现有架构。
- 引入未经验证的依赖。
- 修改当前主线 Runtime。
- 在研究阶段创建自动合并 PR。
- 将官方宣传直接视为架构事实。
- 将模型表现误判为 Harness 能力。
- 在没有许可、来源和安全审查的情况下运行未知插件、Hook 或 MCP Server。

所有建议均应以 RFC 形式提出，经 Founder 审核后再进入正式路线图。

---

## 五、与 ClimateOS 的对应关系

| Grok Build | ClimateOS 对应方向 |
|---|---|
| Plan Mode | Mission Runtime |
| Skills | Runtime Skills |
| MCP | Adapter Runtime |
| Memory | Knowledge Runtime |
| Hooks | Automation Runtime |
| Agent Harness | Mission Control |
| Sub Agents | Multi-Agent Framework |
| Repository Rules | Governance Runtime |
| Headless Runtime | Mission Execution Runtime |
| ACP | External Agent Interface |
| TUI / CLI | Operator Interface |
| Plugin System | Governed Extension Runtime |

原则：学习优秀设计，但保持 ClimateOS 自主架构演进。

---

## 六、预期成果

1. Grok Build Architecture Review
2. ClimateOS Gap Analysis
3. Candidate Features List
4. Adoption Matrix
5. Risk Assessment
6. Recommended Roadmap
7. Evidence and Source Register
8. Existing Capability Crosswalk
9. RFC Backlog

所有建议均标注：Adopt / Adapt / Observe / Reject，并注明证据来源、现有模块映射、新增复杂度、安全风险、维护成本、模型依赖程度和 Founder Gate。

---

## 七、成功标准

研究完成后，应回答：

1. 哪些设计值得长期借鉴？
2. 哪些设计已在 ClimateOS 中具备雏形？
3. 哪些能力仍存在明显差距？
4. 哪些能力应进入 Task 1500+、1700+ 或更长期路线图？
5. 如何在保持独立性的前提下持续吸收全球 Agent Engineering 实践？
6. 哪些属于真正 Runtime 能力，哪些只是界面或模型效果？
7. 哪些能力能降低 Founder 人工审查负担而不降低治理质量？
8. 哪些能力适合跨 ClimateOS、BuildingOS、CarbonOS、WaterOS、EnergyOS、Dryland 与 Kunlun EPI 复用？

最终目标是建设自主、可持续演进的 **ClimateOS Agent Engineering Framework**。

---

## 八、研究执行顺序

### Phase 0 — Source Baseline

核验官方仓库、文档、许可证、版本与发布日期；建立源码模块地图与文档索引；区分官方功能、实验功能、社区扩展与宣传描述。

### Phase 1 — Architecture Decomposition

Agent Harness → Plan Mode → Context / Memory → Tool Routing / MCP → Skills / Plugins → Repository Governance → Hooks → Sub Agents。

### Phase 2 — ClimateOS Crosswalk

与 Mission Control、Runtime、Adapter、Knowledge、Governance、Automation 等体系逐项对照，标注已有、部分已有、缺失、重复、冲突。

### Phase 3 — Adoption Review

形成 Adopt / Adapt / Observe / Reject 矩阵；不直接进入开发；候选项先形成 RFC。

### Phase 4 — Founder Review

Founder 审核研究结论并决定是否进入任务路线图。未获批准的建议保持研究状态。

---

## 九、首轮研究边界

允许：阅读公开资料与源码、建立模块地图、形成对照分析、编写 RFC 草案、提出受控实验建议。

禁止：修改 ClimateOS / BuildingOS 主线、安装到生产环境、接入真实项目数据、开启远程自动执行、运行未经安全审查的插件/Hook/MCP Server、创建自动合并 PR。

---

## 十、Mission Control Intake Decision

**Decision:** MISSION_ACCEPTED_FOR_RESEARCH  
**Runtime Impact:** NONE  
**Mainline Change:** PROHIBITED  
**Required Output Mode:** EVIDENCE-BACKED RFC  
**Founder Gate:** REQUIRED BEFORE ADOPTION

研究目录：`docs/mission-control/research/grok-build/`

下一步读取顺序：

1. `MISSION_GROK_BUILD_RESEARCH.md`
2. `SOURCE_REGISTER_AND_ARCHITECTURE_MAP_V0.1.md`
3. 后续 `CLIMATEOS_CROSSWALK.md`
4. 后续 `ADOPTION_MATRIX.md`
5. 后续 `RISK_REGISTER.md`
6. 后续 `RFC_BACKLOG.md`

---

## CRP

### 核心知识点

Grok Build 的研究价值主要在 Agent Harness、计划、技能、MCP、记忆、Hooks、子 Agent 和仓库治理；研究对象是可验证工程机制，而非模型品牌。

### 关键决策

任务状态为 RESEARCH APPROVED；研究阶段只读、只分析、只形成 RFC；禁止修改当前主线 Runtime；所有采纳必须经过 Founder Gate。

### 下一步行动

建立官方来源登记、生成模块地图、完成 Agent Harness 与 Plan Mode 首轮对照、建立 Existing Capability Crosswalk、输出第一版 Adoption Matrix 与风险登记。

### 项目关键词

`Grok Build` `Agent Harness` `Mission Control` `PRI` `Matrix` `Plan Mode` `Skills Runtime` `MCP` `Memory Runtime` `Hooks` `Sub Agents` `ClimateOS` `BuildingOS` `CarbonOS` `WaterOS` `EnergyOS` `WorldOS` `RFC`
