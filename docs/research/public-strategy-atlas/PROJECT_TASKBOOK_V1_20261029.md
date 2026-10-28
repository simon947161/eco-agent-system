# ClimateOS — 公共战略关系图谱（Public Strategy Knowledge Atlas）
## Founder 工程任务书 v1.0 — 2026-10-29

**任务性质：** 私人 G0 公开资料研究 + 可运行的本地交互式研究样件。此次指令允许 Codex 在隔离的个人仓库工作区开展有界工程实施；**不是 Council 项目、P1/正式 G2 授权、供应商采购或 Sites 部署批准**。  
**所在仓库：** `simon947161/eco-agent-system`。独立分支：`research/public-strategy-atlas-20261029`（基于 main）；与现有 ClimateOS Issue #128 / Draft PR #129 及 P04 水文研究隔离。  
**技术资产：** 优先只读审查现有 ClimateOS 的 evidence/source revision/run receipt/passport、公开政策 Console；如本机可合法读取 `D:\Codex\CoomaWorkOS\cooma-water-compliance-workos\docs\research\council-strategic-operational-p0\` 和 `...p05\` / `...p05-closeout\`，只作参考，不复制 Council 内部资料、不修改其原件；找不到不要假称已读取。  
**研究目的：** 用公开资料解释“战略目标、实施计划、土地利用规划、法律工具、年度行动、公开指标和来源证据之间**哪些关系是有据可查的，哪些只是合理推断，哪些根本无法证明**”。不作法律意见或 Council 绩效结论。

## 1. 核心产品定位

**不是**大型政府业务系统，不替代 Council QSP/绩效管理/档案系统，不接其真实活动记录。  
**是**一个可以互动浏览、搜索、双向追溯、按时间/地区/来源查证的公开政策与规划知识图谱。Founder 首先独立学习，日后是否向 Michele/QSP/CEO 展示，需另行完成个人身份/利益冲突检查及分享许可。

用户主要任务：点击 CSP 目标看官方 DP/OP 关联；点击具体公开行动反查上游战略；查看 LSPS 与 LEP/DCP/SEPP 的**不同性质**规划关系；任意连接点击后打开原文片段、具体页码、文件版次、证据强度和审查状态；看到计划时限与证据缺口，不虚构执行绩效。

**重要科学/法律建模原则**：
- `CSP → DP → OP` 是 NSW 综合规划报告体系中有明确定义的实施链；具体某行与某行的联系仍要逐条核实。
- `LSPS ↔ LEP/DCP/SEPP` 属土地利用规划和规划法律适用网络，并非简单地挂在 CSP 下面的下级工作事项。LEP/SEPP 是法定规划工具；DCP 是详细规划指导，不能把全部 DCP 条款称为直接法定义务。
- Snowy Monaro 官网仍列原 Bombala / Cooma-Monaro / Snowy River 三套 LEP 和多个 DCP，另有 Jindabyne 2024 DCP、Snowy Mountains SAP 适用例外；任何空间适用声明必须有辖区/地块/生效时点及证据。
- QSP 是另一个组织绩效/流程视角：没有官方公开引用不得假装它是正式法规或已建成的集成模块。
- 公开规划提及项目 ≠ 项目已开工；OP 计划量 ≠ 完成量；完成一项检查 ≠ 证明总体合规或环境改善。

## 2. 第一批权威资料及真实版本（必须按读到的文件校验）

| 文档家族 | 官方入口 | 研究定位 |
|---|---|---|
| CSP 2035 | https://www.snowymonaro.nsw.gov.au/Council/Integrated-Planning-and-Reporting | Council 官网称 2025-05-01 通过；以具体文件为准 |
| Delivery Program 2025–2029（2026 Revision） | 同上 | 官网页面称 2026-06-26 通过；必须取**adopted**版本而非 2026-04 draft |
| Operational Plan 2026–2027 | 同上 | 官网页面称 2026-06-26 通过；不要静默使用 2025/26 或 draft 数值 |
| LSPS 2020 | https://www.snowymonaro.nsw.gov.au/Building-and-Planning/Strategic-Planning/Land-Use-Planning | 2020-05-21 通过；12 项规划优先事项和城镇结构章节 |
| LEP / DCP / SAP | https://www.snowymonaro.nsw.gov.au/Building-and-Planning/Development | 三个原辖区 LEP、不同 DCP、Jindabyne DCP 和特殊规划适用；转到 legislation.nsw.gov.au 核即时/历史版 |
| NSW OLG 综合规划指南 | https://www.olg.nsw.gov.au/councils/policy-and-legislation/integrated-planning-and-reporting | 规划体系法定职责、目标—行动逻辑 |
| NSW Planning | https://www.planning.nsw.gov.au/plans-in-nsw/local-planning-and-zoning/making-and-amending-leps | LEP 规划效力；DCP 不可当作与 LEP 同等级的法规 |
| QSP / 持续改进 | https://www.snowymonaro.nsw.gov.au/News-and-Media/News-articles/Council-meeting-recap-Thursday-16-October-2025 | 只作 Council 公开宣布的计划背景；核验实际文件前不制造完成状态 |

**抓取闸门**：只访问公开且有合法使用权的资料；优先官方 HTML/PDF 与法规官方整合版本；检查 robots/访问限制、许可/条款、文件大小/费用，遇 403/429 不绕过；来源无权全文再发布时存元数据、允许的最短引文、原始链接及文件 SHA（若获准保存本地），不要公开发布整份受版权保护 PDF。对含实时法条的文档保留 as-of 日期及适用范围。OCR 非必需不做。

## 3. 资料、条款、关系的统一模式

**DocumentRevision**
`doc_id, title, family, publisher, source_url, source_sha256?, retrieved_at, adopted_at?, effective_from?, effective_to?, geographic_scope, licence, official_status, extraction_method, snapshot_ref?`

**Clause / Goal / Action / Indicator / EvidencePlaceholder**
`node_id, node_type, parent_id?, document_revision_id, clause_or_strategy_code, short_label, excerpt_short?, page_or_section, source_anchor_url, valid_from?, valid_to?, region_tags[], status, synthetic:boolean`

至少包含：
`CSP_GOAL, CSP_STRATEGY, LSPS_PRIORITY, LSPS_ACTION, LEP_PROVISION, DCP_CONTROL, SEPP_PROVISION, DP_ACTIVITY, OP_ACTION, KPI_DEFINITION, PUBLIC_EVIDENCE, SYNTHETIC_ACTIVITY`。

**RelationshipAssertion (一级对象，而非无证据的普通线条)**
`edge_id, source_node, target_node, relationship_type, basis, evidence_anchors[], as_of, geographic_scope, version_compatibility, review_status, reviewer_note, synthetic:boolean`。

关系类型举例：
- `CONTAINS`（同一文件确定层级）
- `EXPLICITLY_LINKS_TO`（文件明确交叉引用）
- `IMPLEMENTS_STRATEGY`（有官方条款支持）
- `GUIDES_PLANNING`（规划指导，不自动法定从属）
- `APPLIES_TO_AREA`（有地域与法律效力的证据）
- `MEASURES`（有指标定义或报告依据）
- `EVIDENCES`（有可审查的公开指标或记录）
- `RELATED_BY_RESEARCH`（研究推断，必须显式区分）
- `POSSIBLE_LINK_UNVERIFIED`（候选关联，不能冒充审定）。

`basis` 必须区分 `DIRECT_OFFICIAL`、`INDIRECT_RESEARCH`、`SYNTHETIC_DEMO`、`UNKNOWN`；所有 `DIRECT_OFFICIAL` 必须给出真实片段与来源锚点，版本一致性及证据链；AI 自动建议默认 `PENDING_HUMAN_REVIEW`。不得把两条存在的关系**自动传递推断**出第三条“已确认关联”。允许多对多及环路，但层级视图须受控折叠。

任何涉及虚构 LTW/Backflow 检查的节点与连线必须显著标记“虚构”，且与公开原件分开查询/导出；不存在的证据永远显示 `UNKNOWN`，不得填 0、填百分比或生成虚假页面引用。

## 4. 核心界面：五层泳道 + 分支树 + 证据抽屉

**桌面默认布局**
- 顶部：`ClimateOS / Public Strategy Atlas / 个人公开资料研究`、文档版本/核验截点、全局搜索、研究主题（环境/水务/土地利用等）和地区/年份筛选。
- 左栏（可折叠）：CSP 目标树、LSPS 规划优先事项树、来源家族选择；层级树仅表示**文件本身的确定从属**。
- 中央主画布（主要体验）：从左到右 `战略与目标 | DP/OP / 规划行为 | 具体公开行动或条款 | 指标/证据` 分泳道；LSPS—LEP/DCP/SEPP 为可切换横向规划支路，不把法规塞进 OP 的子节点。选中一个节点才显现其 1–2 跳关系，其他节点收起；支持轻量平移、缩放、聚焦、反向回溯和路径高亮。
- 右侧证据抽屉：简明节点描述、关系类型、证据判定、**短引文 + 原始官方链接 + PDF 页码/条号 + 文档版次/核验时间**；点击再展开全文上下文或在原网站打开。关闭后还原清爽画布。
- 底部微型时间条和图例：显示来源状态/更新快照、已核验关系数与缺口数；不展示所有文字。

**移动端**：改为目标列表 → 纵向可展开路径 → 证据抽屉，不强制使用大幅复杂网络；键盘可访问、触屏可用、支持“减少动态效果”。关系类型不能只用颜色区别，必须同时有图例和文字标签。

**设计语言**：克制、专业、留白充分；节点默认仅有名称/编号/来源标签/一项证据状态；点击或滚动到该节点时按需显示详情。经过证实的线为实线，研究推断为虚线，缺口为中断线，失效版本淡化。可切换“从目标往下”“从活动往上”“查看版本变化”“仅显示已核实官方关系”。

**进度可视化不是一个综合分数**：
1. `TIME_ELAPSED` 时间经过：只有已知计划起止才计算，注明“期限已过比例≠实际完成”；
2. `MAPPING_COVERAGE` 条款映射进展：仅在样本总数和已逐条审查数已知时显示已审查/总数；不可将样本覆盖率冒充全 Council 覆盖率；
3. `KPI_RESULT` 真实绩效：必须有公开同口径实际值、分母、日期和审核状态才显示目标达成；否则显示 `未核实／暂无公开数据`，不可画 0% 或假造进度。

可先用简洁 SVG/HTML 可交互画布，在 UI 性能证据出现前**不预设 Neo4j、GraphQL、昂贵插件或新的 OS**。优先复用现有 React/网页结构、静态 JSON / SQLite、已核验的许可兼容库；独立离线加载和运行，不要求专用图数据库。

### 原型页面最少三个

1. **总览 Atlas**：选择 CSP 6.1、8.2 或 LSPS 某个规划优先事项，沿上下游展开 1–2 跳。
2. **来源与证据 Explorer**：逐条官方引文、版本、原件链接、断点/冲突、按关系类型过滤。
3. **版本与进度 Timeline**：2025/26→2026/27 OP 版本差异和本研究的资料审查覆盖；仅在有实际公开 KPI 的情况下绘真实绩效。

## 5. 第一版数据量与三条必测真实查询

**范围有界，深度优先**。第一版目标：6 个公开文档家族至少有可核验代表条款，约 **25–60 个节点、30–80 条含审查状态的关系**。这些是工程目标，不是已经核实的数据量。优先真实引用而非自动填满。LEP/DCP 覆盖只是样例地域/条款；绝不写“已建立完整 Snowy Monaro 法规图谱”。

**查询 A（自上向下）**：`CSP 6.1 / 8.2 → adopted DP/OP 中与 LTW/Backflow 相关的实际条款 → 公开指标定义`。若现行 OP 正文取不到或条款不能直接对应，链路必须中断并明确显示 `UNRESOLVED`；允许附带**虚构**检查样本但不能混为真实证据。

**查询 B（自下向上）**：点击虚构 `SYN-LTW-01` 或 `SYN-BF-01`，反查能确证的正式来源；对未经证实的 OP/CSP 跳转标注推断。反向也应能从 CSP 查看其研究候选，但不能提升为官方映射。

**查询 C（跨规划 + 时点）**：`LSPS → 某地的 LEP/DCP 相关条款及版本`；至少选一个有官方资料的城镇（如 Berridale）展示规划方向与法律规划工具的**不同效力**，在地域/时点不匹配时断开、显示原因。增加一次 OP 文件修订或法律变更的假设模拟，验证旧断言自动降为待复核，不擅自迁移。

每条查询结果必须显示路径逐步经过的关系类型、基础证据和断点；支持点击导出带原始来源的简明研究说明。没有确证关系时，**正确结果应是“不知道”，而不是为了好看的图去编线**。

## 6. Codex 实施顺序和真实验收门

**阶段 A：前置核验与数据账本（先做）**
- 检查新独立分支与仓库已有代码、当前进展及可用的 P0/P0.5 研究原件；读取合法可用来源，核对 adopted/draft 与时点；不得直接导入内部 WCOS/Council 数据。
- 输出 `SOURCE_REGISTER.md` + 机器可读 `source-register.json`、版本/地域矩阵、许可、缺口列表；提取少量引用锚点，建 25–60 节点样本目标，先逐条验收证据，不允许先让 LLM 生成整张未经核对的关系网。
- 保证每条已确认关系至少有官方来源；没有官方证据的研究候选不可混入已确认统计。构建可运行的离线断言检查和三个查询，附合成反例。
- **A 门**：可重复运行，缺项不会造假，来源链接正确，版本/地域不匹配可以复现拒绝。

**阶段 B：交互 UI MVP（A 通过后）**
- 用现有前端资产构建三页轻量本地网站；固定样本可离线展示。
- 必须完成：点击节点展开、关系路径双向追溯、规划支路切换、证据侧栏、版本时间线、不同真实/推断/虚构状态、手机纵向模式、键盘/屏幕阅读器基本操作、导出来源引用。
- 设计时控制长标签溢出、重叠线、回环、误导性的完成率；大图性能评估用合成数据，不额外抓取大规模政府资料。
- **B 门**：用户 3 步以内可定位任一示范节点的原始来源；从任一示例操作能向上追溯、向下探索；证据未知或时点不符时 UI 明确显示断点；所有交互真实可用，不是按钮摆设。

**阶段 C：视觉与科学/法律抗错审核（只读）**
- 至少测试：同一行动多目标、多来源对应一条关系、断章取义、版本冲突、适用区域错误、法规和 DCP 等级混淆、CSP 期望被误称绩效、OP 草案被冒充正式版、合成数据混入、公文链接更换、移动布局、键盘与减少动态效果。
- 输出测试命令、实际成功/失败数、来源核查清单、截图（真实运行界面）、`VALIDATION.md`、`LIMITATIONS.md`、Founder 审核所需简明演示说明。
- **C 门**：任何“已核实”陈述均能点到具体来源；所有不明的法规效力与绩效继续 BLOCKED/UNKNOWN；可安全回滚。

**阶段 D：Site 预览（独立批准后，非本任务自动授权）**
- 首先运行在私有本地 localhost；若需要用 ChatGPT Sites 展示，**单独申请 Founder 确认**具体目标与权限。
- 默认继续保持已有 Owner-Private ClimateOS Sites v2 不变；不得覆盖其数据、用户权限、版本或现有 P04 水文案例。发布新私人研究预览如需另一个 site/资源，先说明真实成本、治理、访问控制和零成本条件。
- 研究预览包含“独立私人研究、非 Council 官方、不可作法律依据”明显说明。向 Michele、CEO 或其他人演示之前，需另核个人员工 G1 利益冲突/知识产权/工作资源边界；不自动对外发邮件或共享链接。

## 7. 技术与成本原则

采用 `官方文档 → 本地受控提取 → 源条款 → 关系候选 → 人工核验 → 版本化图谱 → 可交互前端` 的流水线。公开数据的 AI 检索/抽取可以辅助，但不得自动把语义相似关系当正式法律链接。第一版不需要 Matrix of Origin 身份确认、不购买服务、不上云端向量数据库、不使用 Council 内网。预计新增采购现金目标 `AUD 0`，但不能据此保证没有个人时间、现有 AI 额度或后续专业复核成本；如超出既有免费资源，先停下报告。

优先开放、简单、可测试、可被别的工程师接手；用 Git SHA、源文件哈希、可重复的测试、清楚的目录与回滚说明维护可信度。不要把 P0/P0.5 历史报告或 `COST_CALCULATIONS.xlsx` 复制到公开仓库，除非逐个检查其来源与内容许可；不处理其未完成的原生 Excel 验收作为本项目的先决条件。

## 8. 本次最终交付与继续门

Codex 完成 A/B/C 后，应返回：可运行本地站点的**精确路径与启动命令**、页面截图、来源登记、关系数据、实际查询结果、测试和证据缺口、代码变更与提交 SHA、回滚方式，以及是否达到“私有预览候选”标准。提交仅在隔离分支；不要新建大量重复 Issue、不要直接合并 main、不要触碰 PR #129 / 原 Sites。

**完成定义**：至少 3 条双向/跨法定规划示例可真正点击和核验；官方和推断关系可区分；可依据官方原件复查；进度条不伪造绩效；界面有信息收放层次；所有内容仅涉及公开授权资料与明确虚构样本。

**Stop/No-Go**：现行文件无法合法读取、许可无法保证、正文未核实、模型将旧版条款误称现行、法规效力不清、无法保全原数据与其他 worktree、需要 Council 内部权限或新增付费服务、无法保证私有预览权限。停时提交可复现的障碍和最佳合法替代方案，不为满足节点数量虚构引用。

## 9. 开工口令（供 Codex）

> 读取本任务书并执行阶段 A 的真实资料及关系模型核验，在 A 门通过后继续阶段 B/C 的本地 UI 研究样件；用已有 ClimateOS 资产，不重建大型平台，保留所有未验证和未知关系，输出源码、真实页面、截图、测试与复现实录。**本轮允许本地私人公开资料研究样件，但禁止 Sites 部署、Council 数据接入、供应商采购、对外分享、合并及改动现有 PR #129。** 工作量过大时先交付一个有完整来源链的垂直片段及已通过的测试，不要只写一份更大的规划。
