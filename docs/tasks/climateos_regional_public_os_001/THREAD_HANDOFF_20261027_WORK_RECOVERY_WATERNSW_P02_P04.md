# ClimateOS THREAD HANDOFF — Work 对话恢复、WCOS 衔接、WaterNSW 旧 API、P02–P04 实施与下一步

> 归档日期：2026-10-27（Australia/Sydney）  
> 文档类型：**本 ChatGPT 对话的结构化续接交接包（HANDOFF / ACTP）**，并非逐字会话导出  
> 归属：**ClimateOS**（历史仓库名 `eco-agent-system`）；WCOS / Cooma Water Compliance 仅为问题及专业学习的来源  
> 父任务：`CLIMATEOS-REGIONAL-PUBLIC-OS-001` / [GitHub Issue #128](https://github.com/simon947161/eco-agent-system/issues/128)  
> 既有实施：[`codex/regional-public-os-001-taskbook` / Draft PR #129](https://github.com/simon947161/eco-agent-system/pull/129)  
> 编排关联：Issue #126；独立 Council Bridge PR #127 应维持自身授权边界  
> 写入前核对的 PR #129 HEAD：`2e59f8a415f45d04c7ae8d56b64c912ce51adf24`（可能继续变化；下次启动以**实际最新 HEAD**为准）

## 0. 读者先看：状态和一条恢复指令

**目的**：将此次“原 ChatGPT Work 研究线程不可见”的恢复及其后数轮 ClimateOS 科研和 Codex 工程续作，保存在 GitHub 中，方便在 ClimateOS 项目新对话中完整衔接。不得把讨论中已被后续验收取代的状态当成最新状态。

**当前事实**（以 2026-10-27 提交前 GitHub 状态为准）：

| 事项 | 状态 | 证据/解释 |
|---|---|---|
| 原始 Work 会话 | **NOT RECOVERED** | 原会话仍未通过聊天记录恢复；已有研究代码/文档在 GitHub 可继续，并已申请支持排查（是否已正式建立工单未核实） |
| 旧 Work 本地原型、两份中文稿与 11 项测试 | **PARTIAL / NOT RECOVERED** | 历史工作树中发现脚手架，但未确认旧原型内容；不得重建后称为原文件 |
| P02 历史流量链路及私有 Sites | **VERIFIED** | 410033 HRS 固定历史快照、Owner-Private v2、桌面/移动、服务端权限和回滚记录 |
| P03-A 月度研究证据侧车引用 | **VERIFIED** | 关联 2026-07 既有月度周期，未篡改原审查及凭证 |
| P03-B 近期 WaterNSW | **BLOCKED_LOCAL_CREDENTIAL_CONFIGURATION** | 既有订阅/旧代码和历史 HTTP200 已找到；当前本机密钥配置及最新授权读取未恢复 |
| P04 CASE001 研究 | **PARTIAL；NUMERIC_JOIN_BLOCKED** | 官方 Geofabric V3.3 站点流域几何、AWRA-Lv7 产品/原生 NetCDF 元数据已核查；月统计、HRS 时区/日界、质量与等价性尚未闭合 |
| P06 无人值守 | **NOT VERIFIED** | 无已验收的合法自动抓取→写入→读回→失败处理；不因网站上线就宣布自动化成功 |
| PR #129 | **OPEN / DRAFT / NOT MERGED** | 交接不等于授权合并、公开发布或后台启动 |

**下一执行者一句话：**先核对最新 `EXECUTION_STATE.json`、Issue #128、PR #129 和工作树，再从 P04 **官方数据产品语义/时界澄清**与 P03-B **本地订阅密钥恢复闸门**继续；不重做已通过的 P02/P03/流域几何，不在科学准入前计算跨源相关性。

---

## 1. 本线程发生了什么：恢复失踪的 Work 研究会话

1. 用户此前在 ChatGPT Work 中开展围绕 Snowy Monaro 的 CSP 2035、LSPS 2040、生态文明区域研究、三个主题比较和 Codex 实施工作。将 Work 对话移入 ClimateOS Project 后换电脑，原对话在界面中不可见；用户担心研究及多年 ClimateOS 连续性丢失。
2. 提供了疑似工作交接的线程标识 `01a17697-77ff-72e2-ba2a-78e719bf3383` / `codex://threads/...`，**无法证实它是原 ChatGPT Work 会话 ID**，可能只是相关 Codex 线程。
3. 对 OpenAI 支持的回复建议确认账号、workspace、全局/项目/归档/锁定/Codex 历史等；用户明确要求升级支持，已准备给技术支持的升级说明。**助手未读取 OpenAI 账户后台，不能确认会话服务器状态，也不能保证已创建支持工单。**
4. GitHub 恢复最初核验：既有 Taskbook、`EXECUTION_STATE.json`、政策研究和 Console 代码、八题评分、三研究线和 PR #129 都存在；因此可让 Codex 在不等待恢复聊天的情况下继续，条件是先审计工作树、保留未同步文件和旧原型。
5. Codex 后续真实执行、测试、推送了 P02、P03、P04，多轮结果记录在同一 Issue #128 / PR #129。遗失的原始聊天与遗失的本地 Work 原型**仍不可假称恢复**，但主要研究决策和部分工程工作已通过 GitHub 连续传承。
6. GitHub 交接文件**不会自动搬移这个 ChatGPT 对话到 ClimateOS Project，也不会自动触发 Codex**。用户在 ClimateOS 新对话引用本文件及 Issue #128 即可接续。

## 2. 总体研究理论与战略决策：从 WCOS 问题进入 ClimateOS

本研究在 Cooma Water Compliance / WCOS 对话中发源，但归属私人 **ClimateOS**；不要将其缩减为某个 Council 业务软件或内部合规项目。

**核心问题**：在气候变化、旱灾、区域增长与能源转型条件下，水、土地、土壤、植被、能源、碳、公共基础设施、社会经济与治理如何联动？能否利用透明公共证据、物理科学和 AI 工作流，形成可核验的区域生态韧性及“旱地生态文明”研究与应用能力？

用户特别纠正过“先花十年学业务，十年后再战略研究”的节奏：
- **现在**建立跨系统知识框架、问题、资料、假设、反证和工程基础；
- **未来 1–2 年**通过公开数据研究与不涉密的专业实践检验可行性；
- **约十年**是科学积累、可转移方案、职业发展、合作和潜在产品的长期视野，不是推迟起步十年。

政策与科学边界：
- CSP 2035：社区公共目标、指标和策略基准；不是未经核实的当前 Council 成效承诺。
- LSPS 2040：土地利用、空间结构和规划措施；不是法定开发审批或自动实施的项目。
- DP/OP：资源、行动、预算和实施路径的**版本化**资料；已有旧版基线，**2026 当前版全文仍待单独核验**。
- 气候、流域、行政区、城镇供水服务区、模型网格必须分开；同一地点名称不能证明空间边界相同。
- 区分资料事实、政府政策意图、模拟结果、假设、反证、推断、情景及科学/行政正式批准。缺项用 UNKNOWN/null，不允许静默填补。

### 2.1 八题比较与三条并行主线

早期研究八个候选，优先分数（**主观、可修订，不是科学概率**）：
- **T3 区域证据与情景治理：90/100**；
- **T1 水务韧性与水—能—碳：85/100**；
- **T2 土壤—植被—流域韧性：80/100**；
- 其余分布式能源、旅游/住房压力、资源循环、碳信用 MRV、旱地综合示范均保留为子题或远期候选，不能因此抢占主线。

**T1**：水文及服务系统韧性、需求、污水/水能耗和可控碳排，区分自然河流流量和城镇供水容量。  
**T2**：降雨—土壤湿度—植被—土地利用—蒸散—径流与旱地生态，采用可证伪假设和竞争解释；模型/遥感不等于现场实测或因果结论。  
**T3**：公共政策—科学证据—版本—指标—反证—治理情景—研究机会的审计式链路；Run Receipt、Evidence Passport、SourceRevision、Review/Scenario 等服务于所有主题。

**T1/T2/T3 是长期并行研究主题；P00–P10 是工程交付包，两者不能混为“做完 T1 再做 T2”。** 工程各 P 包应服务整体战略，不另建 OS、团队或第二套无证据来源的网站。

## 3. 可续接工程：P02 真数据固定快照和私人站点

规范数据：BoM Hydrologic Reference Stations（HRS）/ WaterNSW；`410033` Murrumbidgee River at Mittagang Crossing。官方历史日报：
- `https://www.bom.gov.au/water/hrs/content/data/410033/410033_daily_ts.csv`
- 22,645 日记录，1964-03-01 至 **2026-02-28**；**September 2026 是版本标签，不是最新观测日期**；
- HRS 质量 A=12,058、B=7,192、C=160、E=3,235、G=0。E 为不可靠，G 为模型填补，不能因为日期完整就认为质量可信；
- 原始 SHA256：`78e8188f3f445afa33ad466dd0554e653761ef617832b6df3a9eac6b1240ca1a`；
- 版权/许可：WaterNSW 产品特定 **CC BY 3.0 AU**，保留 BoM/HRS 来源及修改说明；
- CSV 有 `Flow (ML)` 与 `ML/day` 描述并存、9am local 前24h 与提取时间/单位歧义；不强行同义转换。

原有研究 Console 已增加数据校验、原始/解析版本、SQLite、日期查询、SVG 图表、质量标识、Evidence Passport 和 Run Receipt；2016（更正：**2026**）年 2 月 28 条记录经过本地和私有部署读回，原报告所称 493 项回归通过、1 skip。页面仅展示可追踪**历史**数据，不能直接推断当前水情、水质、供水容量或因果关系。

私有网址：`https://climateos-snowy-monaro.minshu.chatgpt.site`；Owner-Private v2，记录有拒绝匿名访问、授权访问、移动/桌面及回滚/恢复验收。未经用户批准不得公共部署、修改受众或合并。

**P02 原任务已 VERIFIED；不要以一个未自动更新的历史快照为由重建 P02。**

## 4. P03-A 证据侧车和 P03-B 近期流量来源

**P03-A VERIFIED**：将上面 HRS 固定快照、Receipt 和 Passport，以**事后只读补充引用**关联到原有 `2026-07` 月度研究周期。引用 `HRS-CYCLE-LINK-5786CE400E77B343`、周期 `COOMA-CYCLE-5B67DD16E0116301`；不修改原六表、原审阅内容或凭证；损坏/缺失须回退 UNKNOWN。关联发生在月度审核**之后**，不能假称 7 月审核当时已经使用这个新增证据。关联见 `P03_ACCEPTANCE_20261026.md`，记录的 499 项完整测试通过、1 skip。

**P03-B BLOCKED for present runtime**：
- WaterNSW 官方 Developer Portal 需要已订阅产品的密钥、条件及端点身份；2026-10 当时 Codex 环境无有效本地 secret binding，未进行真实授权 API 请求。既有 WaterNSW 账号和成功读取历史已有证据，不应要求用户重注册。
- 公开 NSW WaterInsights ArcGIS 对 410033 查到 288 行，最新 2022-12-14；缺产品特定单位、QC 和自动访问许可，**不能代表 WaterNSW 经授权 API 的时效**。
- HRS 每隔一段时间发布历史产品，不是天然实时来源。可调查 BoM WDO、获准 WaterNSW API，但不能用付费 AI 网页抓取、绕过 403 或公共页面有数据就替代科学授权。
- 自动更新需另过 P06：经过允许的周期查询、请求频率/配额、增量持久化、来源时间与抓取时间分开、错误退避、连续验收读回、报警、成本和权限审计。

## 5. 对话关键纠错：原 WaterNSW API **以前真实使用过**

用户指出此前在 ClimateOS 已注册 WaterNSW Developer Portal 并操作过 API；后经旧 GitHub 和用户原始资料核实：

- 2026-07-28 曾建立/使用私人 WaterNSW `Water Data` 产品订阅，通过 `Surface Water Data API` 获得 `410033 / FlowRate` 数据成功响应。
- 必须区别两份旧样本：**Daily / Combined / FlowRate，2026-07-28 09:00 AEST，198.639 ML/day，WaterNSW QC 125（Auto QC - Passed）**；另一条 **194.296 ML/day / 19:45 AEST** 是不同采样上下文，不可静默替换。
- 过去用户提供 2026 年 1–7 月结构化日数据文字，以及 `HYDROLOGY_PROFESSIONAL_REVIEW_CARD_V0_1.md`。这些是**结构化转录/报告**，并非严格保留的 HTTP 原始字节；不能制造原始 SHA256 或宣称新证据正式准入。
- 旧 [PR #111](https://github.com/simon947161/eco-agent-system/pull/111)：HRS 历史流量特征；[PR #112](https://github.com/simon947161/eco-agent-system/pull/112)：八维科学可比性门；[PR #113](https://github.com/simon947161/eco-agent-system/pull/113)：API exact-byte evidence admission。三 PR 历史上均已合并，现有代码路径 `cczps_lite/integration/waternsw_near_current_evidence_admission.py`。
- 旧 #112 的站点与名义 ML/day 单位通过，但参数物理意义、日聚合、9am 日界、DST 时区、QC=125 对 A/B/C/E/G 映射、原始响应凭证未通过；因此状态 **NOT_COMPARABLE_YET**，不得计算历史百分位或“现在偏高/偏低”。
- 旧 #113 在当时因缺原始 body/当轮配置被阻断；2026-10 Codex 再次核对授权工作区，没有找到密钥绑定、原命名 `WATERNSW_410033_DAILY_FLOWRATE_CAPTURE_2026-08-04.json` 或旧本地分支。**这只是有限工作区的找不到，不代表密钥永久遗失，更不证明历史 API 没接通过。**
- 对外报告和本交接不包含密钥值、订阅标识或私密凭证，严禁把 API key 贴入 GitHub/ChatGPT；不盲搜浏览器/密码库、不动 Council 授权。
- 固定恢复逻辑：用户/获授权主机在正式门户核实零额外费用、产品操作与许可 → 把**已有**密钥置于经批准本地秘密配置 → 一次有界、只读、官方 410033 Daily 请求 → 本地 Git-ignored 原始字节和脱敏回执 → 经过 #113 准入 → 独立经过 #112 物理语义可比门。任何环节不明就保持 BLOCKED，P04 不依赖这把密钥。

旧连接恢复及校正文件：`WATERNSW_PRIOR_API_ACCESS_RECOVERY_20261026.md`、`WATERNSW_RECOVERY_VALIDATION_20261026.md`；最新有关提交 `891d8a9a1893a3b0280672166fbfef973de1e9f6`，专项 19 项通过；这**不是**一次新成功认证请求。

## 6. P04 第一项“水—土—气候”科学研究：实际推进到哪里

研究案例：`P04-WATER-SOIL-CLIMATE-001`。初步研究问题为：在站点 410033 的*真实上游流域*内，降水异常与前期土壤湿度是否与低流量月份存在可复核的关联，在季节和竞争解释下是否仍成立？这是**拟议的关联研究，不是已经发现关联，更不是因果证明**。

### 6.1 基础统计与质量

2000-01-01 至 2025-12-31，312 个月标签、HRS 原始 9,497 日记录；A=3,266、B=3,460、C=10、E=2,761；216 个月所有日记录为非空 A/B，但仍需预注册对 QC/样本选择的敏感性处理。此处只做可用性预检，未做跨源数值拼接。

### 6.2 410033 上游流域几何

官方 production **BoM Geofabric V3.3**，站点 410033，Network HydroID `43408271`、StationCatchments HydroID `43677907`；官方 MultiPolygon，2 parts/2 holes，拓扑有效；GDA94/EPSG:4283 → Australian Albers/EPSG:3577 面积 **1,902.459811 km²**，相较 HRS `1,889.8 km²` **+0.669902%**。发布方 confidence=Good，站点关联验证，未随意修复/吸附、未拿 Council 行政区边界代替。

**重要保留**：发布者多边形几何真实且有效 ≠ 与较早 HRS 采用的旧版流域定义科学等价。HRS 资料涉及 Geofabric V2.1，版本差可能解释面积，但**未证明其确切原因**；需要流域出口/版本/面积复核。

### 6.3 AWRA-Lv7 产品和原生月度 NetCDF（最新至 2026-10-27）

- 版权路线：BoM/AWO 所核产品 **CC BY 4.0**（如无另行声明）；官方 NCI catalogue、NetCDF/CSV/AWDS 数据路径。许可≠当前产品科学意义已通过全部准入。
- 月度渲染函数 `precip_month`、`smpfull` **并非真实变量名**；实际月度产品变量 `rain_day`（雨量字段单位 mm）、`sm_pct`（0–100 cm 根区土壤水，`fraction of fullness`）。AWRA 土壤湿度是模型估计，且受模型降雨输入驱动，不能把降雨与土壤湿度当两套独立观测。
- 官方服务标有 2000–2025 的全部 312 月标签；**标签完整不代表全部网格有有效数值**。产品源网格约 0.05°、WGS84，NoData 屏蔽和流域加权还未验收。
- 2026-10-27 最新实测的技术审查 [P04_SEMANTICS_ACCEPTANCE_20261027.md](./P04_SEMANTICS_ACCEPTANCE_20261027.md)：通过 NCI 官方月度 `rain_day.nc`、`sm_pct.nc` 有界 HTTP206 各取十个 8 KiB 分块，总 160 KiB，**没有下载整份大文件，也没有读取物理变量数组**。变量 Float32、`_FillValue=-999`，无 `scale_factor`/`add_offset`/`cell_methods`。NoData 与早期渲染服务哨兵值须分别按具体产品解释。
- 时间坐标 Gregorian、days since 1900-01-01；样本 2000 年 1/2/3 月的 `time_bounds` 是月初到次月月初，二月闰年 29 天，标签为月底；**这只是时间坐标，不证明月度值究竟是总和、平均或月底状态，也不证明 HRS 的 9am 日界与其一致**。
- `sm_pct` 变量记载 fraction of fullness，但原始物理数值存储范围、是否 UI 仅乘 100、月均还是月底仍缺权威产品定义；`rain_day` 在月度文件究竟累计雨量还是均值待确认。禁止拍脑袋乘以 100 或直接把 mm 当月合计。
- 下载面板提供 HRS 官方**按月总量**文件；实际查过 410033 **2 月** CSV：1965–2025 共 61 条 `ML/month`、无 QC 列，**缺 2026-02**，尽管日度 HRS 已记录到 2026-02-28；且 extraction date `4/06/2024` 与最新发布标签冲突。该月产品可作为未来对照候选，不能直接替代带 QC 的日原始值。
- HRS 日文件表述前24h、上午 9 点 local；**夏令时、一天的起止/归属、月边界、ML/day 对 Flow(ML) 和 cubic-metres 提取注释的具体来源转换仍未获站点产品的权威定义**。不能直接套用 BoM Water Data Online 另一套午夜规则。
- 未做跨源子集、数值联结、相关性、低流量异常分类、因果、供水安全或公众水情结论，状态 `PARTIAL / BLOCKED_NUMERIC_JOIN`。
- 最新 Codex 回报：NetCDF/时间语义专项 **19/19** 通过，隔离全套 **518 次，517 通过，1 跳过**；这验证软件与受控证据，不是科学结论。
- 书面澄清问题已形成 **`P04_UNSENT_TECHNICAL_QUESTIONS_20261027.md`**，尚未寄发 BoM/WaterNSW；不得擅自对外联络。

主要记录：`P04_CASE001_ADMISSION_VALIDATION.md`、`P04_SPATIAL_ADMISSION_RESULT.json`、`P04_CASE001_READINESS.json`、`P04_SEMANTICS_ACCEPTANCE_20261027.md`、`P04_SEMANTICS_RESULT_20261027.json`。源文件、几何和校验摘要见相应 `evidence/p04_*` 子目录。

## 7. GitHub 重要历史节点（便于恢复，不必重复执行）

| 节点 | SHA / 文件 | 历史意义 |
|---|---|---|
| 政策来源研究 | `42e8df72a549752a7f15a64f0ba6c58c1f11f49d` | CSP/LSPS/DP 来源、初轮研究矩阵 |
| Console 三研究线 | `11327bc70ba1fa4c2ff995b604acbca48622a3d4` | 现有页面和政策 API |
| P02 HRS 本地 | `6ca8f9d913e99ba66d4743790b2e4f0df11cf571` | 真数据持久化与图表 |
| P02 私有 Sites | `6a5c3b88af4536066fbc66f379decd74318e6571` | 网站 Owner-Private v2 |
| WCOS→ClimateOS 战略交接 | `67eb5574851844bbd4d6d187fbe4afd000aaa754` | 原理论/三主线/执行链 |
| P03 证据侧车 | `2f680be34eda1f18bc140726cd6d8d1fe3d338f6` | 7 月研究周期引用、来源可行性 |
| WaterNSW 旧 API 追溯 | `609e94cd93881aec3ec7137c96b809ad66726ab4` | 历史接入及恢复方案 |
| WaterNSW 恢复检查 | `891d8a9a1893a3b0280672166fbfef973de1e9f6` | 当前密钥配置受阻，不影响 P04 |
| P04 几何/产品准入 | `7ade6e625982c3e8bc6f11713b1536503ac09981`；后修 `f5967f25d2829183b8fb60cd3cc178c3927f1a75` | Geofabric 官方有效流域与 AWRA 元数据 |
| P04 原生语义 | `de73aafb2de0d3db93d4c9d68ee375da61b251e7` | NetCDF 小范围元数据和 HRS 官方月度候选 |
| 另一个早期政策线程 handoff | `2e59f8a415f45d04c7ae8d56b64c912ce51adf24` | `smrc_policy_console/CONVERSATION_HANDOFF_20261027.md`，**覆盖其原政策线程，不等于本线程全记录** |

**同目录还存有** `CLIMATEOS_WCOS_CSP_LSPS_HANDOFF_20261026.md` 和 `WATERNSW_PRIOR_API_ACCESS_RECOVERY_20261026.md`。它们仍有价值，但属于较早节点；必须用最新状态覆盖其尚未完成事项，不能照旧执行 P03-A、重复访问控制测试或从头重建站点。

## 8. 最小下一步：精确行动而非再建框架

### A. P04 — 第一优先级，独立于 WaterNSW 密钥

1. **先读已形成的未发送问题单** `P04_UNSENT_TECHNICAL_QUESTIONS_20261027.md`，逐条匹配官方技术文档、元数据和 NCI 产品源；仅在得到用户明确同意后以**个人/研究身份**向相关机构发出必要的专业询问。
2. 重点关闭 `rain_day.nc` 月度和/均、`sm_pct.nc` 物理范围/UI 百分比、土壤水时段聚合、模型数据版次/缺失标记、HRS 410033 9am local/DST/日期与月归属、2026-02 官方月总量缺失原因及质控继承问题。
3. 对每条给出来源 URL/资料版本/时间/哈希、原文语义、准入判定 `VERIFIED / PARTIAL / UNRESOLVED / BLOCKED`；不以月份标签、服务接口软件版本、UI 百分比代替正式数据产品定义。
4. 若科学与授权门通过，再挑**一个完整月 + 一个 DST 转换月**做**有界复现与逐日质控一致性检查**，保存原始与派生数据、空间加权、时间归属、差异、Receipt/Passport。若任一门未过则继续 BLOCKED，不计算相关性或区域环境结论。
5. 随后形成独立、可证伪的 T1×T2 研究协议并进入合适的水文学专业复核。对流域 V2.1/V3.3 的 0.67% 差额保留敏感性/边界版本审查。

### B. P03-B / P06 — 不阻碍主线的授权与自动更新

1. 不再盲搜密钥或重注册；现有 WaterNSW 个人开发订阅通过用户/获授权本机安全渠道恢复。需要用户实际登录/批准时集中一次要求，不能请其手动逐条敲 PowerShell。
2. 条款、零额外费用、端点、流量、单位和质量约束逐项核实后，一次合法有界 API 读取；保存原响应（不提交）与脱敏摘要；使用现有 #113，再过 #112 可比性门。未通过不得并入 HRS 历史。
3. P06 自动任务至少需要真实合法连续取数、写库、读回、异常退避、运行记录和错误通知。历史 HRS 的 403、WaterNSW 密钥空缺、无 P06 实测不可说自动化已实现。
4. 将实时站点观测与 HRS 的历史基线严格分开，并明确 `observed_at`、`retrieved_at`、数据版本、临时/最终 QC；避免“有 AI 抓取工具就能随意抓”误区。

### C. P05 与十年战略的回归

- 将 CSP/LSPS/DP/OP 的**版本对照与反证**接入已有 Console（当前 2026 DP/OP 原件内容仍需核验），将 P04 水—土—气候基础研究服务于 T1/T2，T3 管理研究与治理情景。
- 不以 P02 图表数量衡量成果；目标是让 ClimateOS 对真实区域问题给出**可定位证据、可重复步骤、边界清楚、不确定性说明和替代解释**，并在合理阶段接受科研/行业专业复核。
- KITTY 作为组织和汇总层可协调 Codex，但本 GitHub 交接**本身不触发** KITTY/Codex 运行。没有核验的后台持续性不能描述成已部署。
- 零新增外部费用、无 Council 内部数据、无公开网站发布、无自作主张合并 PR #127/#129、无擅自对政府机构发函。

## 9. 权限、保密、恢复边界

- Council 是雇主/政府主体：LTW/backflow 和 WCOS 中的客户、地址、内部资产细节、工作照片/录音、设备/业务记录、投诉、内部 CRM/文档和未公开政策不得流入私人 ClimateOS。
- 从工作中可抽象研究方法和**确属公开且许可清晰**的数据；个人研究结果不代表 Council 批准或背书；专业角色、雇主潜在利益冲突、对外联络、兼职和知识产权另行核验。
- 数据获取遵守提供方授权及配额，不绕开 403/429、不传播 API key、不支付未授权费用。不能把版权许可误当产品测量解释或 API 调用授权。
- 科学审查待完成不等于失败：`UNKNOWN`、`BLOCKED` 是诚实且可操作的状态。不要把软件测试通过提升为结论可靠或“实时监控完成”。
- 旧 ChatGPT Work 对话的排查继续由平台支持处理；原会话本身未恢复、身份标识不确定；不要清理可能尚有本地原型的旧工作目录、浏览器历史或相关记录。
- 四份历史回归报告的未提交改动曾由 Codex 保留，应在每轮开工检查及保护，不能为了干净状态强制重置。

## 10. 新 ClimateOS 线程的推荐阅读顺序和开工提示

**推荐阅读**：
1. 实际 GitHub 最新 PR #129 Head/Issue #128 最近反馈与审批界限；
2. `docs/tasks/climateos_regional_public_os_001/EXECUTION_STATE.json`；
3. 本 `THREAD_HANDOFF_20261027_WORK_RECOVERY_WATERNSW_P02_P04.md`；
4. `P04_SEMANTICS_ACCEPTANCE_20261027.md` 和 `P04_UNSENT_TECHNICAL_QUESTIONS_20261027.md`；
5. `WATERNSW_RECOVERY_VALIDATION_20261026.md` 和 `P03_ACCEPTANCE_20261026.md`；
6. 历史政策线程交接 `smrc_policy_console/CONVERSATION_HANDOFF_20261027.md`、`CLIMATEOS_WCOS_CSP_LSPS_HANDOFF_20261026.md`、`TASKBOOK.md`，核对当时有效的仓库规则及当前用户授权。

**可以粘贴到 ClimateOS 新会话的最短续接文本：**

> 请接收本线程 ClimateOS HANDOFF：`docs/tasks/climateos_regional_public_os_001/THREAD_HANDOFF_20261027_WORK_RECOVERY_WATERNSW_P02_P04.md`。仓库 `simon947161/eco-agent-system`，沿用 Issue #128、Draft PR #129。先核验最新 HEAD、`EXECUTION_STATE.json` 和 2026-10-27 P04 NetCDF/HRS 语义验收，不要重复 P02/P03-A/Geofabric 已完成工作。主要推进 P04 产品月统计与 HRS 日界/夏令时/官方月总量不一致的证据闭合；WaterNSW 旧订阅密钥恢复独立待授权。保持 Owner-Private Sites v2、无新增成本、无涉密 Council 数据、无越过科学审核的数值联结。返回实际证据、测试、GitHub 记录和下一最小动作；不要只写规划。

**最终声明**：这是本 ChatGPT 线程的完整工作决策和工程验收**摘要**，不是原始逐字记录；具体提交、验收、状态必须以仓库实时版本为准。文件上传 GitHub 不等于 ChatGPT Project 移动、不等于自动派工或公开发布。
