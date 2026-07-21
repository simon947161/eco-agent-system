# Grok Build Source Register and Architecture Map v0.1

**Project:** ClimateOS / Mission Control / PRI  
**Status:** FIRST-PASS RESEARCH BASELINE  
**Date:** 2026-07-22  
**Mode:** EVIDENCE-BASED / READ-ONLY / RFC-ONLY

---

## 1. Purpose

本文件建立 Grok Build 研究的第一版来源登记与架构地图，用于支持后续 ClimateOS、BuildingOS、CarbonOS、WaterOS、EnergyOS、WorldOS、Mission Control、Matrix 与 PRI 的跨系统对照。

本文件不是采纳决定，不授权修改任何 Runtime。

---

## 2. Source Register

### S-001 — SpaceXAI 官方开源公告

- URL: https://x.ai/news/grok-build-open-source
- Publisher: X.AI LLC / SpaceXAI
- Published: 2026-07-15
- Source type: Official announcement
- Evidence grade: A1 — 官方一手来源
- Confirmed claims:
  - Grok Build 是 coding agent、agent harness 与 terminal UI。
  - 公开范围包含 agent loop、tools、TUI 与 extension system。
  - Extension system 明确提及 skills、plugins、hooks、MCP servers、subagents。
  - 支持 local-first，可从源码编译，并可指向本地 inference。
- Limitations:
  - 公告属于产品概览，不能单独证明每个模块的完整实现、稳定性或生产边界。
- Research use:
  - 建立正式研究范围。
  - 不能作为采纳结论的唯一依据。

### S-002 — Grok Build 官方 GitHub 仓库

- URL: https://github.com/xai-org/grok-build
- Owner: xai-org
- Source type: Official public source repository
- Evidence grade: A1 — 官方一手源码
- Confirmed claims:
  - Rust 为主要语言。
  - 提供 terminal-based coding agent、fullscreen TUI、headless execution 与 ACP editor embedding。
  - Repository README 列出核心 crate 分层。
  - 仓库是从 SpaceXAI monorepo 周期同步的公开切片。
  - 根目录 `SOURCE_REV` 记录对应 monorepo revision。
  - First-party code 使用 Apache-2.0；第三方代码保留原许可证。
  - 外部贡献目前不接受。
- Critical limitation:
  - 公开仓库是周期同步切片，不应假定等同于完整内部生产系统。
- Research use:
  - 作为架构与实现核验的主要来源。
  - 所有代码层结论需记录具体路径、revision 与证据状态。

### S-003 — Repository README / Layout

- URL: https://github.com/xai-org/grok-build#repository-layout
- Source type: Official repository documentation
- Evidence grade: A1
- Confirmed structure:
  - `crates/codegen/xai-grok-pager-bin` — composition root / binary
  - `crates/codegen/xai-grok-pager` — TUI
  - `crates/codegen/xai-grok-shell` — agent runtime, leader, stdio, headless entry points
  - `crates/codegen/xai-grok-tools` — tool implementations
  - `crates/codegen/xai-grok-workspace` — filesystem, VCS, execution, checkpoints
  - remaining codegen crates — config, MCP, markdown, sandbox and supporting runtime
  - `third_party/` — vendored upstream source
- Research use:
  - 形成首版模块地图。

### S-004 — Official Documentation Index

- URL: https://docs.x.ai/build/overview
- Source type: Official product documentation
- Evidence grade: A1
- Expected coverage from official repository index:
  - getting started
  - shortcuts and slash commands
  - configuration
  - theming
  - MCP servers
  - skills
  - plugins
  - hooks
  - headless mode
  - sandboxing
- Status: REGISTERED / DEEP REVIEW PENDING
- Research use:
  - 第二轮逐模块核验行为、配置与权限边界。

### S-005 — In-repository User Guide

- Path: `crates/codegen/xai-grok-pager/docs/user-guide/`
- Source type: Version-coupled official documentation
- Evidence grade: A1
- Research value:
  - 与公开源码 revision 绑定，优先级高于未注明版本的二手教程。
- Status: REGISTERED / FILE-LEVEL INDEX PENDING

### S-006 — License and Third-party Notices

- URLs / paths:
  - https://github.com/xai-org/grok-build/blob/main/LICENSE
  - https://github.com/xai-org/grok-build/blob/main/THIRD-PARTY-NOTICES
  - `crates/codegen/xai-grok-tools/THIRD_PARTY_NOTICES.md`
- Source type: Legal / dependency evidence
- Evidence grade: A1
- Confirmed concern:
  - 工具实现中包含来自 Codex 与 OpenCode 的移植或上游实现。
  - “学习架构”必须与“复制实现”严格分离。
- Research use:
  - 许可风险、来源追踪、实现原创性边界。

---

## 3. Evidence Classification

| Grade | Meaning | Allowed use |
|---|---|---|
| A1 | 官方源码、官方文档、官方公告 | 可支持事实判断 |
| A2 | 官方演示、changelog、issue 回复 | 可支持行为判断，需注意版本 |
| B1 | 高质量第三方源码分析 | 可辅助解释，不可替代官方证据 |
| B2 | 社区教程、视频、博客 | 仅用于发现线索 |
| C | 未核验宣传、转载、推测 | 不进入架构结论 |

原则：每一项 Adopt / Adapt 结论至少需要一个 A1 证据；高风险功能需要两个相互独立的官方证据或源码核验。

---

## 4. Preliminary Architecture Map

```text
Operator / Editor / CI
        |
        +--> TUI / CLI / ACP / Headless Entry
                    |
                    v
             Agent Shell Runtime
                    |
        +-----------+-----------+
        |           |           |
        v           v           v
 Context Assembly  Planning   Response Parsing
        |           |           |
        +-----------+-----------+
                    |
                    v
               Tool Dispatch
                    |
     +--------------+---------------+
     |              |               |
     v              v               v
 File / Search   Terminal / Exec   Web / External
     |              |               |
     +--------------+---------------+
                    |
                    v
             Workspace Runtime
       Filesystem / VCS / Checkpoints
                    |
                    v
     Extension and Governance Surface
 Skills / Plugins / Hooks / MCP / Subagents
                    |
                    v
       Config / Sandbox / Permission Boundary
```

该地图是基于官方公告与 README 的第一版逻辑抽象，不代表源代码调用图。

---

## 5. Module-to-ClimateOS Crosswalk v0.1

| Grok Build area | ClimateOS / PRI direction | Initial judgment | Reason |
|---|---|---|---|
| Agent shell runtime | Mission Control Runtime | Adapt | ClimateOS 需要领域治理与证据约束，不能直接采用编码 Agent 的通用循环 |
| Context assembly | Knowledge Runtime / ACTP / CRP | Adopt concept | 当前已有上下文包与交接机制，但需统一 provenance、expiry 与 conflict handling |
| Plan review | Mission Planning Runtime | Adopt concept | 可降低 Founder 持续推动负担，但必须保留阶段 Gate |
| Tool dispatch | Adapter Runtime / MCP Strategy | Adapt | 环境、建筑、水、能源工具需要 capability contract 与证据等级 |
| Workspace checkpoints | Runtime recovery / project state | Adopt concept | 与 ACTP、handoff、Git evidence 可形成统一恢复点 |
| Skills | Runtime Skills | Adapt | 需要跨 OS 的 Registry、版本、权限和退役机制 |
| Plugins | Governed Extension Runtime | Observe | 扩展性高，但依赖、权限和供应链风险较大 |
| Hooks | Automation Runtime | Adapt | 先用于验证、文档与证据捕获，不先用于高风险自动执行 |
| MCP servers | External Provider Adapter Contract | Adapt | 与现有 Adapter 思路高度相关，但需 ClimateOS trust/evidence envelope |
| Subagents | Multi-Agent Framework | Adapt | 需父子责任、预算、隔离、冲突解决和 Founder escalation |
| TUI | Mission Control Operator Interface | Observe | 值得学习交互，不应优先于 Runtime 治理 |
| ACP | External Agent Interface | Observe / Adapt later | 有助编辑器和外部 Agent 接入，但应在核心合同稳定后推进 |
| Headless mode | PRI autonomous execution | Adapt | 适合受控批处理；禁止默认无人监管地改主线 |
| Sandbox | Security Runtime | Adopt concept | 是未来工具和 Agent 扩展的基础能力 |

---

## 6. First Architecture Findings

### Finding F-001 — 真正值得研究的是 Harness，不是模型

Grok Build 官方将 agent loop、context assembly、tool dispatch、workspace、extension system 与 UI 分开公开。这说明可迁移价值主要位于模型之外。

**Initial decision:** ADOPT AS RESEARCH PRINCIPLE

### Finding F-002 — Workspace checkpoint 可能比“长期记忆”更优先

对 ClimateOS / PRI 而言，可恢复的项目状态、Git revision、任务 Gate、证据包，往往比模糊的自然语言长期记忆更可靠。

**Initial decision:** ADAPT

候选方向：

- Mission Checkpoint
- Runtime Checkpoint
- Evidence Checkpoint
- Founder Decision Checkpoint

### Finding F-003 — Extension surface 必须由治理包围

Skills、Plugins、Hooks、MCP、Subagents 共同构成扩展面，也共同构成供应链和权限风险面。

**Initial decision:** ADAPT WITH GOVERNANCE FIRST

ClimateOS 需要的不是“插件越多越好”，而是：

```text
Capability
+ Permission
+ Provenance
+ Evidence
+ Audit
+ Revocation
+ Recovery
```

### Finding F-004 — Mission Control 应发展为跨 OS Harness，而非单一聊天协调器

候选目标：Mission Control 负责计划、分派、恢复、审查、证据和跨系统协调；各 OS 保留自己的领域 Runtime、数据合同与判断边界。

**Initial decision:** ADAPT

### Finding F-005 — 公开仓库不是完整生产真相

由于仓库是从 monorepo 周期同步，必须记录 SOURCE_REV，避免把缺失模块误判为不存在，也避免把公开实现误判为当前生产版本。

**Initial decision:** ADOPT AS SOURCE GOVERNANCE RULE

---

## 7. Proposed PRI / Matrix Position

```text
PRI
 |
 +-- Mission Control Harness
 |     +-- Planning Runtime
 |     +-- Dispatch Runtime
 |     +-- Recovery Runtime
 |     +-- Review / Founder Gate
 |     +-- Evidence Capture
 |
 +-- Matrix
 |     +-- Capability Registry
 |     +-- Skill Registry
 |     +-- Agent Registry
 |     +-- Tool / MCP Registry
 |     +-- Policy and Permission Matrix
 |
 +-- Domain OS Runtimes
       +-- ClimateOS
       +-- BuildingOS
       +-- CarbonOS
       +-- WaterOS
       +-- EnergyOS
       +-- future WorldOS
```

设计原则：

- Mission Control 管理任务与 Agent，不替代领域科学判断。
- Matrix 管理可发现能力、规则、身份与权限，不成为万能数据库。
- 各 Domain OS 保留独立数据、证据、模型与决策合同。
- 跨 OS 共享 Harness，不共享未经治理的结论。

---

## 8. Immediate Candidate RFCs

### RFC-GB-001 — Mission Checkpoint Contract

定义任务恢复点：任务状态、Git revision、证据、未解决问题、下一动作、Founder Gate。

Status: CANDIDATE / ADAPT

### RFC-GB-002 — Cross-OS Skill Contract

定义 Skill metadata、input/output、permissions、version、dependencies、evidence requirements、deprecation。

Status: CANDIDATE / ADAPT

### RFC-GB-003 — Governed Tool Dispatch Envelope

在每次工具调用外增加 purpose、scope、permission、expected evidence、failure mode、rollback。

Status: CANDIDATE / ADAPT

### RFC-GB-004 — Agent Parent–Child Accountability

定义 delegation、budget、workspace isolation、result validation、escalation 和 termination。

Status: CANDIDATE / ADAPT

### RFC-GB-005 — Repository Rule Precedence

定义 global → repository → folder → task → local override 的规则层级与冲突处理。

Status: CANDIDATE / OBSERVE-THEN-ADAPT

---

## 9. Risks Identified v0.1

| Risk | Severity | Control |
|---|---:|---|
| 把编码 Agent 架构直接套入环境决策系统 | High | 领域 Runtime 与 Harness 分层 |
| 插件、Hook、MCP 扩大供应链攻击面 | High | allowlist、sandbox、权限、审计、撤销 |
| Subagents 放大错误与成本 | High | parent accountability、budget、checkpoint、validation |
| 自动计划削弱 Founder 控制 | Medium-High | Founder Gate、stage review、stop conditions |
| 长期记忆污染项目事实 | High | provenance、expiry、correction、Git-backed checkpoint |
| 公开同步仓库与生产系统不一致 | Medium | SOURCE_REV、date、version、evidence grade |
| 为追求 TUI 体验而忽略 Runtime | Medium | Runtime-first roadmap |
| 复制上游代码引入许可证与维护负担 | High | architecture-only research、independent implementation |

---

## 10. Next Research Pass

1. 对 `xai-grok-shell` 建立文件级 Agent Harness 索引。
2. 对 user guide 的 Plan、Skills、MCP、Hooks、Subagents、Sandbox 分别登记配置入口与权限行为。
3. 对 `xai-grok-workspace` 核验 checkpoints、VCS 与 recovery 的真实边界。
4. 建立 `CLIMATEOS_EXISTING_CAPABILITY_CROSSWALK_V0.1.md`。
5. 形成首版 `ADOPTION_MATRIX_V0.1.md`。
6. 将候选 RFC 映射到 PRI、Matrix 与各 Domain OS，不立即进入代码任务。

---

## 11. Mission Control Resume Instruction

下一线程读取本目录时：

1. 先读取 `MISSION_GROK_BUILD_RESEARCH.md`。
2. 再读取本文件。
3. 从 Section 10 继续执行。
4. 保持 `RESEARCH-ONLY / RFC-ONLY / NO RUNTIME CHANGE`。
5. 不重复创建本任务，不重新讨论是否研究 Grok 模型。

---

## CRP

### 核心知识点

Grok Build 公开架构可初步分为入口层、Agent Shell Runtime、Context/Planning、Tool Dispatch、Workspace、Extensions、Config/Sandbox 七个区域。

### 想法点

将 Mission Control 建设为跨 OS Harness，将 Matrix 建设为 Capability / Skill / Agent / Tool / Policy Registry，各 Domain OS 保留领域判断权。

### 关键决策

首轮候选均保持 RFC 状态；优先研究 Checkpoint、Tool Dispatch Envelope、Skill Contract 与 Parent–Child Accountability。

### 未解决问题

尚未完成文件级源码索引；Plan Mode、Memory、Hooks 与 Subagents 的真实实现边界仍需核验。

### 下一步行动

进入 Agent Harness 与 Plan Mode 的源码级对照，随后生成 ClimateOS Existing Capability Crosswalk 和 Adoption Matrix。

### 项目关键词

`Grok Build` `Source Register` `Architecture Map` `Mission Control Harness` `PRI` `Matrix` `Checkpoint` `Skill Contract` `Tool Dispatch` `MCP` `Subagents` `Governance` `ClimateOS` `BuildingOS` `WaterOS` `EnergyOS`
