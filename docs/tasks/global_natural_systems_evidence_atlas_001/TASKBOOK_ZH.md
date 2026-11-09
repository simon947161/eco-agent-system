# GLOBAL-NATURAL-SYSTEMS-EVIDENCE-ATLAS-001｜Codex唯一执行任务书
日期：2026-11-09 Australia/Sydney
Founder授权：**现在执行**。不是等待再次批准或仅写设计文件。
仓库 simon947161/eco-agent-system
工作分支 research/global-natural-systems-evidence-atlas-001
冻结父提交 3bb71785ad2705823a78748c9ba4cd5003becb41
必须完整阅读 docs/research/cczps-global-scope/CCZPS_GLOBAL_SCOPE_EVIDENCE_STANDARD_V0_1_ZH.md；该文件只是v0.1研究范围基线，不是已通过的科学准入或已完成全球图谱。旧PR145科学基线 ae1050a621ac794e447f9ac047865d90b2f04b03；PR143–145保持Draft、不合并。
目标：**交付真实可查询、可检索、可追溯的全球自然系统—科学证据—国家治理映射Atlas研究批次**，并形成回到ClimateOS/CCZPS/EcoEngine/ECOChain科学与治理主线的清晰接口。禁止把本任务降格为只写规范或静态设计。

## 0. 先审计，不重建竞争系统
读取上述v0.1规范、docs/00_MASTER_ARCHITECTURE/SYSTEM_RELATIONSHIP_MAP.md、ECOENGINE_V2_SYSTEM_DEFINITION.md、CCZPS_LITE_V0_4_REVIEW.md、现有CCZPS空间/气候分区、Public Strategy Atlas PR130、GIS/QGIS/Hydrology PR129、EcoEngine/CCZPS研究、PR143–145方法与证据评审、ECOChain旧角色和Evidence Passport、ClimateOS Knowledge Garden及Enotebook相关索引。检查远程当前状态与代码可复用位置。严格区分已有功能/文档/想法/未实现；不得重写旧权威schema或改动旧PR。ClimateOS分层：World Model模拟；EcoEngine解释环境物理；CCZPS比较可能未来；ESG++翻译制度；ECOChain记录证据与生态贡献，人类治理作最终决策。

## 1. 全球范围，不按任意国家名单选样
先以固定版本的UN M49或ISO3166建立全球国家/地区coverage register，包含无数据标记；另列海洋、公海、极地、跨境自然单元，不能将其硬塞入单一国家。重点建立可复用的自然系统分类：
- 大气：气候区、环流、边界层、气候遥相关；
- 海洋：洋盆、洋流、热量、海平面、珊瑚与沿岸；
- 水文：流域/子流域/上下游、跨境河流；
- 陆地生态：生物群区、森林、湿地、泥炭地、冻土、干旱区、农业生态区；
- 冰冻圈：冰川、海冰、积雪、永久冻土；
- 人类系统：能源、工业、废物、土地利用、农业、贸易与供应链；
- 治理：国家、地方、国际条约、许可与核算方法。
使用权威公开版本化分类（如Köppen-Geiger气候区、WWF生态区、HydroBASINS/HydroSHEDS流域、FAO/UNEP/UNESCO/UNFCCC、WMO、IPCC、Natural Earth、UN M49等候选）前先核许可证、数据版本、空间精度、适用性；**不得假定所有候选均开放再分发**。优先复用已有仓库数据和许可；需要新增下载时仅选可合法使用的轻量样本，记录字节哈希、许可和来源。无法获得的全球边界保留元数据/外部链接/缺口，不得伪造全球几何覆盖。
各自然单元/国家记录id、source、version、geometry_ref、CRS、valid_time、scale、coverage、confidence、uncertainty、license、status。多对多overlay，跨国流域不得变成按国籍拆分的虚假自然过程。

## 2. 全球关系图：先机制再国家
明确边类型：PHYSICAL_TRANSPORT / BIOGEOCHEMICAL_CYCLE / ECOLOGICAL_DEPENDENCY / CLIMATE_TELECONNECTION / SUPPLY_CHAIN_FLOW / EMISSION_RESPONSIBILITY / EXPOSURE_VULNERABILITY / POLICY_DEPENDENCY / OBSERVATION_SUPPORT / HYPOTHESIS_ONLY。
每条边必须有from/to、过程、方向、空间/时间尺度、源证据、假设、是否因果/相关/待验证、反证、适用边界、版本。风/河流/供应链上下游分开；长寿命温室气体全球混合不可简化为上风向责任。跨时空积分要显式单位、测量支持和守恒；禁止未经验证的全球单一生态综合指数或GWP高度修正。
**必须做3条有证据的跨边界示例路径**，分别代表：水文上下游（跨国流域）、大气/海洋遥相关（如ENSO及跨区影响，区分统计与因果）、全球CH4排放—混合—气候影响的科学层级（不能从局地ppm直接推全球效果）。每条路径都提供原始权威出处、关系图、可证伪条件、哪些可计算/不可计算。

## 3. Climate Scorecard正式证据层
官方 https://www.climatescorecard.org/ ; https://www.climatescorecard.org/scorecard/ ; https://www.climatescorecard.org/reports/ 。
逐页核查评分方法、维度、分值、覆盖国别、时间与更新日期、作者、来源和版权；将COUNTRY_POLICY_SCORE、POLICY_COMMITMENT、COUNTRY_REPORT、OBSERVED_OUTCOME区分为不同类型。网站评分不是物理观测/科学因果系数；如方法过时或页面日期不明确，明确标记。
做可检索country-to-natural-region-to-scorecard映射样本，至少涵盖中国、俄罗斯、印度、马来西亚、印尼、巴西、澳大利亚、美国、欧洲代表、非洲代表、小岛屿代表；不强求网站必须覆盖所有样本，缺失标NOT_COVERED并由其他官方来源补足治理背景。**不要按国家大小排序**；选择应覆盖气候区/生态机制/地理连通/脆弱性/制度差异，公开选择理由和遗漏风险。
不得将私人Gmail稿件、未授权订阅内容或个人隐私推送公开Git；Climate Scorecard只保存允许引用的公开事实/短摘录/链接及版本收据。

## 4. 证据分类规范转成可用数据
至少实现下列typed records：
PHYSICAL_OBSERVATION、DERIVED_DATA、MODEL_OUTPUT、SCIENTIFIC_LITERATURE、LEGAL_METHOD、POLICY_COMMITMENT、POLICY_ASSESSMENT、ECOLOGICAL_OUTCOME、GOVERNANCE_DECISION、SYNTHETIC_TEST。
claim_id、source_id、version、source_locator、rights、sha_if_downloaded、geographic_support、time_support、method_id、unit、uncertainty、calibration/QA、review_state、contradictions、not_inferable_from。SOURCE_VERIFIED/RECALCULATED/EVIDENCE_INSUFFICIENT/MATERIAL_CONTRADICTION/NOT_ASSESSED/BLOCKED分别输出，不能将Policy Scorecard评分与真实气候影响混算。保留PR145的A/B/C分层评审语义和内部合成算术限制；不是法定认证。可按自然系统、国家、过程、时间、证据类型查询并追踪来源，输出“什么影响什么、为什么、证据在哪、还不知道什么”。

## 5. 必须有运行的Atlas最小成果
在现有Public Strategy Atlas/知识检索/GIS组件中选择**最小兼容接入点**；不得为此新建大平台、重复Atlas数据模型或仅生成静态网页。
交付至少：
A) 一个机器可读的全球coverage register（覆盖所有UN M49国家/地区，数据缺口显式；海洋/跨境单元另外登记）；
B) 一套版本化自然单元与关系边的schema及至少3个跨境机制示例；
C) 一个可运行的离线query/validation程序，演示自然单元→国家/地区→政策Scorecard/其他来源→科学证据→CCZPS情景/PR145审查接口；
D) 一份中国/俄罗斯/东南亚/巴西/澳大利亚/非洲/小岛屿等代表样本的非任意选择矩阵；
E) 溯源、许可证、单位/时空/几何冲突、假说误当因果、评分误当物理观测的负例测试；
F) 中文Founder大字/Slides式验收报告（Markdown可视化与简明页面优先，不强制做PPT），明确真实完成/研究待办/缺口。
仅当已有Atlas组件可无破坏复用且有充分时间，才可做轻量可浏览地图/路径视图；否则可运行离线图谱查询优先。禁止无限抓取所有国家文章、无界大文件GIS下载、付费API、真实设施反演和大气气候模拟。
数据预算：最多15个新增权威来源主题、最多3条深入跨境机制、最多12个国家/地区深入案例（全覆盖只做登记），最多3个新增轻量GIS数据集。若数据授权/来源阻塞，先交付可信schema/关系/查询与真实缺口，不无限扩大研究。

## 6. 与原有CCZPS和ECOChain主线闭环
最终必须给出可运行或可审计的接口映射：
Global Natural System Index → EcoEngine物理/观测证据 → CCZPS Scenario Comparison（现有路径和治理约束） → ESG++政策/Scorecard翻译 → ECOChain claim/evidence审查与长期记录。
至少一个端到端**只读/合成示例**：选一条已登记自然过程，关联公开来源、政策评价、一个可比较情景和PR145审查结果，清楚分开物理、政策、技术审查与人类决策。不能把Scorecard评分当作模型参数或将ECOChain当作批准者。
明确回到主线的NEXT_DECISION：哪条科学/治理连接最值得下一轮验证、为什么；**不得把后续目标设为继续无界扩充Atlas**。
ECOChain canonical仍ECOCHAIN_CANONICAL_NOT_FOUND、Enotebook PENDING_INTEGRATION，除非有可核查的正式授权接纳回执；不伪称接入成功。PR143–145科学状态不提升。

## 7. 交付/测试/回执
新增目录 docs/tasks/global_natural_systems_evidence_atlas_001/
TASKBOOK_ZH.md、README.md、FOUNDER_REPORT_ZH.md、GLOBAL_COVERAGE_REGISTER.(csv/json)、NATURAL_SYSTEM_TAXONOMY.md、DATA_SOURCE_AND_LICENSE_REGISTER.md、RELATION_GRAPH.(json)、CROSS_BOUNDARY_CASES.md、SCORECARD_METHOD_AND_COVERAGE.md、COUNTRY_NATURE_POLICY_CROSSWALK.md、EVIDENCE_SCHEMA.json、ATLAS_QUERY_RESULTS.md、CCZPS_ECOCHAIN_HANDOFF.md、QA_AND_VALIDATION.md、NEXT_SESSION.md、CRP_HANDOFF.md、REVIEW_REQUEST.json、HANDOFF_STATUS.json、必要的代码/fixtures/tests/evidence。实际文件格式可与已有仓库一致，但须有唯一入口与真实复现命令。
代码检查：全球登记完整性（按固定M49版本）、自然单元多对多映射、GIS/CRS/时区/单位不一致、来源许可、错误因果边、虚假Scorecard分数、错误法域版本、跨境方向、断链、合成数据误认实测、PR145角色越权；测试结果与CI真实状态逐项归档。无需为了测试数量做无意义用例。
创建独立stacked Draft PR（父基线为上述固定提交，若base分支尚未PR化，先核GitHub可选base与stacked策略，不覆盖父任务分支）；提交研究R与交付D、固定精确HEAD，核对PR open/draft/unmerged，报告来源许可、真实几何覆盖比例、查询结果和不足。不能合并、部署、修改旧PR、接触私有Council数据或购买/联系第三方。完成后在PR评论给ChatGPT只读审查请求；Founder转交后才视为收到，不假装自动监听。
成功标准：真正建立可查的自然过程优先全球证据图谱，能解释国家/生态关系与Scorecard差异，提供可运行查询与可追溯源，并给出回到CCZPS/ECOChain治理主线的具体下一步；不以地图华丽程度、国家数量或文档页数代替科学与工程成果。
