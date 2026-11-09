# CLIMATEOS-CLIENT-AI-SCIENCE-INTEGRATION-001
## 唯一总任务书｜科学成熟度核验 + 环境专业平台兼容层 + GitHub 双向交接
创建日期：2026-11-09（Australia/Sydney）
状态：FOUNDER_AUTHORISED_BOUNDED_AUDIT_AND_PROTOTYPE
仓库：simon947161/eco-agent-system
本任务分支：research/climateos-client-ai-science-integration-001
冻结基线：PR #141当前HEAD e25ffe3e34829d9146628a7c72a363c35d8ec151；PR #141原研究HEAD 1daa3a15b698c5a9216e7286cf1243ef0cf870dc；PR #140 16f0b59dab966f0b66d91b7c28135e8fce9e4cc1
前置科学审查：https://github.com/simon947161/eco-agent-system/pull/141#issuecomment-6726949537
全部新内容优先放在 docs/tasks/climateos_client_ai_science_integration_001/；必要的最小可执行验证代码须按现有模块结构管理，严禁修改冻结物理核心、旧 PR、旧科学结果。

## I. Founder 目标及不可曲解的关系
Founder 希望 ClimateOS 成为「Client AI：面向客户、可理解环境专业需求、连接合法数据和经过验证的专业模型、生成可审计结果的科学计算与治理服务层」。
参照 Senversa 的公开 Data Intelligence、Geospatial、Portal、水管理、环境尽调及 PFAS 地下水风险建模服务，**不是**复制 Senversa 私有 Portal、声称具有其 API 或访问其客户数据，也不是将其用作无授权数据提供商。
目标同时覆盖：(A) 现有 ClimateOS 科学研究究竟已经验证到哪一步；(B) 如何在其上构建真正可以被将来客户调用的受控能力；(C) Codex ↔ ChatGPT 通过 GitHub 任务、提交、回执及审核包完成可追溯的异步交接，由 Founder 只需传递简短 PR/HEAD 链接，而不是长文本复制。
明确：GitHub 留言/文件提交≠ ChatGPT 已自动收到或执行；只有连接到真实轮询/事件订阅和回执的运行系统才可声称自动完成。禁止编造 AI 已读、后台接单和部署状态。

## II. 先实际审计已有工程（强制入口）
开始前核对当前远程 HEAD、分支、TASKBOOK、PR #138–141 精确科学结论、已归档评审回执、NEXT_SESSION；扫描实际现有功能和测试，而不是根据旧文档预设。
最低覆盖：cczps_lite/integration/physics_validation.py 的 P1–P4；PR139本地甲烷/污水证据；PR140 NOAA BRW；PR141 AirCore；EcoEngine 气象采集能力；QGIS 及地形水文模块；Public Strategy Atlas；已有知识/证据台账与 agent/harness/Kitty/Mission Control 相关模块（存在则读，不存在则标 UNKNOWN）。
逐能力出具 CAPABILITY_REALITY_MATRIX：路径、版本/commit、实际运行证据、最小复现命令、依赖、访问许可、物理适用性、输入输出、测试/CI、是否外部采用、成熟度。成熟度至少区分 CONCEPT / IMPLEMENTED_SYNTHETIC_TESTED / REAL_DATA_STRUCTURAL_QC / SCIENTIFICALLY_VALIDATED / PRODUCTION_ADOPTED；后两级无证据不得使用。
必须单独写：P1参考数学测试并非观测准入；PR139水相mg/L不能充气相ppm；PR140 3340结构匹配但科学配对0；PR141 2137 L2气体/5457气象结构审计且定量NO_VALID_VERTICAL_PROFILE、Stage3 METHOD_READY_NOT_VALIDATED；D3 DATA_NOT_READY，P1-A PENDING；航空总体气候效应不是直接CH4/CO2同质量排放高度因子。保留旧阻塞、绝不在本任务自动重跑受阻科学实验。
发现 repo 状态不同于任务书，停在事实核对层并写差异；不悄悄覆盖。

## III. Senversa 公开行业对标（仅公开资料）
限定公开案例，不联系 Senversa、不调用其私有 API、不推断 Portal 的内部数据许可。
必核原始公开页：
1. https://senversa.com.au/solution/data-intelligence-analytics
2. https://senversa.com.au/solution/geospatial
3. https://senversa.com.au/project/environmental-due-diligence-portal
4. https://senversa.com.au/project/water-management-program-dashboard
5. https://senversa.com.au/project/groundwater-flow-and-pfas-risk-modelling
对每项标注 SOURCE_CONFIRMED / INFERENCE / NOT_PUBLIC；公司营销项目叙述≠独立算法精度/客户绩效验收。
深入提取它对「多场址数据、监测位置/结果、GIS受体邻近、历史匹配、粒子追踪、集合风险、更新和报告」的工作流结构，并对照 ClimateOS 真实现状。市场可用性、API授权、客户合同和价格若无证据，标 UNKNOWN。
设计两种独立模式：PUBLIC_OPEN_DATA_ADAPTER（本轮可验证），CUSTOMER_AUTHORISED_ADAPTER（只设计契约、不读取实际客户资料）。对 Senversa 仅列 CONDITIONAL_PARTNER_ADAPTER（需要授权，不能声称可接）。

## IV. 数据、模型与客户权限的可落地接口契约
设计一个尽量小的、与具体提供商无关的环境项目服务契约，至少覆盖：
- Project / Site / Asset / Monitoring Point / Observation / Sample / Laboratory Result / Geo Layer / Source Receipt / Licence / QA Status / Model Run / Review Decision。
- 客户身份与数据所有权、租户隔离、角色授权、最小权限、合法使用目的、敏感/商密分类、保留/删除、完整审计日志；不将 Council 内部邮件、非公开数据、第三方客户监测结果或工作身份采购线索用作私人项目输入。
- 原始数据不变；来源URI/时间、文件SHA/版本、许可、CRS/datum/经纬、时区、采样起止、单位和基准、QC/LOD/LOQ、检测方法/校准、缺失码、不确定性和空间代表性；外部CSV/GeoJSON/GeoPackage/实验室CSV等格式按现有环境与许可选择，不能为追求格式而安装庞大依赖。
- 环境主题路由：PFAS水/土、CH4大气、CH4溶解态、填埋场生成/逸散、水文/地下水各自物理语义隔离；不同单位/相态不自动换算或套错模型。
- 输出审计包：input hashes, schema+method version, calculation status, scientific evidence grade, validation holds, reviewer, limitations, rejected rows & reasons, visualization/report links；未知=UNKNOWN，不以0替代。
- 工具/智能体只允许调用登记且准入的模型；审计/结构分析可读，未科学准入不得触发排放、健康风险、法律合规或信用结论。
- 与现有 GitHub Evidence Reader、Founder Cockpit/Kitty 适配时采用只读契约，只有实际存在且有证据的接口才写 IMPLEMENTED。

## V. 最小真实端到端 vertical slice（本任务要求实际可运行，不是再写纸上架构）
从合法公开、不含 Council 私有材料的一项真实环境场址/监测数据选择**一个**。优先使用已准入且可合法重用的真实公开环境数据；若现有数据只有科学结构QA资格，可选择“公开监测数据质量与空间证据筛查”而不能做排放/污染风险推断。允许选择公开环境监测位置和对应读数，以清楚授权的数据为前提；只做一个场址/数据集，最多两个候选，防无限搜索。
必须运行可复核的端到端路径：
用户问题文本→问题类别与科学权限路由→合法公开数据载入/身份与结构检查→空间/时间/单位和质量校验→现成已批准安全的分析（例如数据覆盖与空间邻近、属性筛查、简单描述统计，不能伪装为地下水污染迁移或法定限值判定）→结果状态与来源说明→客户可读中文解释、最少一个地图或可复算空间结果及可机读审计包。
应使用既有代码和轻量脚本/测试，避免另起数据库、复杂 Web 管理台、生成式模型服务或未经验证数值求解器。若开源GIS依赖在环境中缺失，可生成 GeoJSON + 明确坐标/可视化说明/静态地图候选，不得声称浏览器图已测试。
如果未获得可合法、充分的公开实例，选择 fail-closed 的示例录入演示（明确 SYNTHETIC_DEMO），输出 BLOCKED_NOT_REAL_DELIVERY；不能伪造实际服务验证。真实数据质量/完整率可以报告；无真实业务 ground truth 则不宣称客观提升准确率或效率。
测试必须包含：正常输入、单位混淆（mg/L vs ppm、不同基准）、时间/CRS错误、缺来源或许可、缺字段、恶意文件/路径、缺少模型批准、跨租户访问模拟、数据篡改、AI幻觉推断阻断。负例要拒绝而不是补默认值。所有数据及其原始来源留有 SHA 和许可台账。

## VI. 正向工程优先级与资源治理
基于 ACTUAL_REUSE_LEDGER 列出：REUSE_NOW / ADAPT_MINIMALLY / RESEARCH_ONLY / DO_NOT_BUILD。已有成熟工具优先复用，不得重复开发 GIS/数据库/气候模型；不得因 Senversa 公开展示了 Portal 就复制其版面、文案或专有工作流实现。
开发上限：一个研究目录、一个可运行最小实例、必要的小型集成脚本和回归/失败保护测试；真实浏览器验收仅在确有应用改动时进行。保留其他项目与PR，不部署、不合并、不更改科学准入标签、不申请购买或任何商业 API/PI 联系。
加入 Reality Check：完成度按源文件/测试/模型验证/客户采用分四层；记录真实耗时/软件依赖/硬件成本（可测则测，不可得UNKNOWN），避免无依据节省百分比/盈利承诺。可与Senversa合作是OPTIONAL FUTURE, not secured.

## VII. GitHub 双向交接协议（必须可操作，避免复制粘贴）
在本目录提供 HANDOFF_PROTOCOL.md 和机器可读 HANDOFF_STATUS.json / REVIEW_REQUEST.json；定义：
- source_pr, scientific_baseline_sha, taskbook_sha, working_head_sha, reviewed_head_sha, review_receipt_commit_sha, status, stage, evidence_uri, blockers, owner, next_action, authorized_scope, no_run_flags, review_actor, response_delivery_state。
- 每次提出“ChatGPT只读评审”必须固定精确HEAD、PR、文件入口、测试范围、未复核情况；使用GitHub PR描述/单一评论 + 文档证据指针；不复制整篇报告到聊天。
- 从对话向Codex传输：Founder可复制一句“请读取 GitHub [path] 执行，回报 PR+HEAD”；从Codex向ChatGPT：Founder可复制一句“请只读审阅 PR #N 精确HEAD，按README和REVIEW_REQUEST阅读”。两端均利用GitHub连接器读取原文，而非神秘自动同步。
- 如果现有真实运行时有机器人轮询/订阅，可只读审计其触发和回执路径，状态 MUST differentiate SENT/QUEUED/ACKNOWLEDGED/EXECUTING/REVIEW_READY/REVIEWED；不要在缺运行证据时声称已自动闭环。本轮不新增远程自动化，不修改KITTY/Harness任务权限，不替Founder审批。
- 给 Founder 至少两条不超过220字的短句：Codex启动和ChatGPT回读。今后短句只含PR/HEAD/入口，完整证据从GitHub拉取。

## VIII. 预期交付、验收与停止
目录 docs/tasks/climateos_client_ai_science_integration_001/ 最少：
README.md（唯一入口）；
FOUNDER_REPORT_ZH.md（面向Founder的“科学到哪、客户能力到哪、最值得做什么、没做什么”）；
SCIENTIFIC_BASELINE_AND_GATES.md；
CAPABILITY_REALITY_MATRIX.md；
SENVERSA_PUBLIC_BENCHMARK.md（官方公开链接+证据等级）；
CLIENT_AI_ARCHITECTURE_AND_CONTRACT.md；
ACTUAL_REUSE_LEDGER.md；
PILOT_CASE_AND_RESULTS.md（真正可运行路径或明确阻塞）；
QA_AND_VALIDATION.md；
HANDOFF_PROTOCOL.md、HANDOFF_STATUS.json、REVIEW_REQUEST.json；
NEXT_SESSION.md、CRP_HANDOFF.md；
可复算程序、脱敏/公开输入、hash台账、单元/集成测试与截图（若涉及UI）。
报告必须清楚划分：真实交付完成 vs 已实现软件 vs 结构数据QA vs 合成测试 vs 研究提案；每条有证据路径。给出不超过3个科学阻塞、不超过3个工程阻塞、不超过3个外部授权/商业阻塞，不让Founder陷入大量手工协调。
先补合法公开数据的来源/许可和QA，之后实现最小客户工作流，测试后提交一个**新的独立Draft PR**，保持与本分支的合理stacked关系；推送远程并核对PR HEAD/远程HEAD/本地HEAD一致。Codex不得合并、部署、不拓展新科学计算、不动旧PR或私有Council数据。回传给Founder仅：PR链接、HEAD、入口README、Founder报告、研究/原型状态、下一条ChatGPT短句。
科学评审主体仍为ChatGPT独立只读审查；本任务的测试通过不能提升D3 DATA_NOT_READY、P1-A PENDING、PR140 NO_VALID_PAIR、PR141 NO_VALID_VERTICAL_PROFILE与Stage3 METHOD_READY_NOT_VALIDATED。

## IX. 成功判定
成功不是建出另一款Portal，更不是“已经接入Senversa”。成功需要证明：
(1) 能诚实解释现有ClimateOS真实能力与欠缺；
(2) 已建立有版本、许可、科学闸门的数据/模型适配最小实现；
(3) 一个公开案例可以从客户问题走到可复算审计结果，或按质量门诚实阻塞；
(4) GitHub能够让Founder用短句分别交Codex执行和交ChatGPT审查，不冒充自动读取/自动审批。
FOUNDERSHIP：可扩展的环境科学服务层，第三方平台通过未来明确授权进行连接；一切正式模型、法律结论、现场治理、市场承诺均须独立证据。
