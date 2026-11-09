# CCZPS 全球研究范围与证据分类规范｜研究框架 v0.1
日期：2026-11-09
状态：FOUNDER_SCOPE_PROPOSAL / NOT_ENGINEERING_TASK / NOT_SCIENTIFIC_ADMISSION
冻结基线：PR145 ae1050a621ac794e447f9ac047865d90b2f04b03
原则：从地球自然过程出发，再映射国家行为、责任和治理。不是国家排行榜，也不是全球单一评分。

## 1. 原有架构优先
源：docs/00_MASTER_ARCHITECTURE/SYSTEM_RELATIONSHIP_MAP.md；ECOENGINE_V2_SYSTEM_DEFINITION.md；CCZPS_LITE_V0_4_REVIEW.md。
CCZPS：Computable Climate & Civilization Possibility System，气候分区责任、可能性计算、情景比较与人类治理决策支持；不是物理引擎。
EcoEngine：物理环境响应/差异场/强迫与不确定性；World Model：条件仿真；ESG++：制度语言翻译；ECOChain：证据/贡献/信任的长期记录，不是法定认证或治理权威。
PR143–145的甲烷公式、物料账、方法评审是共享科学/证据服务，不能重定义CCZPS为甲烷求解器或ECOChain为认证机构。

## 2. 全球覆盖与研究单元
GLOBAL COVERAGE REGISTER：全球陆地、海洋、冰冻圈、主要生态区与所有国家/地区，按ISO3166或联合国M49固定版本登记国家/地区；无数据标UNKNOWN，不虚构。物理研究的主单元不是国家：
- Atmosphere：气候带、气团、环流/输送区、边界层；跨境长寿命温室气体全球混合；
- Ocean：洋盆、洋流、海温、海洋热量、海平面与珊瑚/沿岸系统；
- Hydrology：流域、子流域、上下游、地下水与跨境水文；
- Terrestrial ecosystems：生物群区、森林/湿地/泥炭地/冻土/干旱区/农业生态区；
- Cryosphere：冰川、积雪、海冰、永久冻土；
- Human systems：能源、产业、农业、废物、贸易、供应链、土地利用、人口与暴露；
- Governance：国家、地方、国际机制、法规与报告制度。
每个研究单元有 geometry_ref, geometry_source, CRS, scale, period, classification_version, coverage, uncertainty, boundary_mismatch，跨图层用可追溯overlay/映射而不是国家强行替代自然边界。

## 3. 关系类型不得混淆
PHYSICAL_TRANSPORT（风/水/洋流）、BIOGEOCHEMICAL_CYCLE（碳/水/氮等）、ECOLOGICAL_DEPENDENCY、CLIMATE_TELECONNECTION（遥相关需来源和统计/动力学证据）、SUPPLY_CHAIN_FLOW、EMISSION_RESPONSIBILITY、EXPOSURE_VULNERABILITY、POLICY_DEPENDENCY、OBSERVATION_SUPPORT、HYPOTHESIS_ONLY。
每条关系记录 from/to、机制、方向、时间滞后、空间支持、因果/相关/假说级别、方法、证据、反证与版本。上下游仅用于确实有方向性的流/供应链；长期GHG不按简单上风向归责。
积分必须带变量/单位/时间空间域和守恒边界：排放通量时间积分≠空气浓度积分≠辐射强迫积分≠治理综合评分。

## 4. 国家选择不能随意
所有国家进入全覆盖登记，深研候选由可解释的分层抽样与目的选择确定，而非简单四国或按人口排名。
至少覆盖：东亚（中国）、南亚（印度）、东南亚热带（马来西亚/印尼）、高纬度欧亚（俄罗斯）、非洲至少一跨境流域及一干旱区、南美热带（巴西）、北美、欧洲、澳大利亚与太平洋、小岛屿国家、极地/无主权海域。国家仅为案例候选，须核官方资料和生态区交叉映射。评分维度：科学过程代表性、全球影响/暴露、跨境关系、数据可用性、制度差异、弱势/遗漏风险、验证成本。权重可调整且做敏感性分析；无全球因果强弱的虚假绝对排名。

## 5. Climate Scorecard来源与证据边界
官方入口 https://www.climatescorecard.org/ 、https://www.climatescorecard.org/scorecard/ 、https://www.climatescorecard.org/reports/ ，需后续逐页确认可访问性、当前版本、评分对象、维度、时间、更新日期、覆盖国别、作者、原始政策/统计来源、评分规则及版权。
作为POLICY_ASSESSMENT/COUNTRY_CASE_STUDY，**不**直接作为观测气温、GHG排放量、甲烷源强或CCZPS物理系数。评分和国家报告分开；评分与实际执行/结果分开；每次报告/评分绑定发布日期及评估年份。无该国评分=NOT_COVERED，不能猜分数。
从既有 Climate Scorecard 投稿/研究知识入口建立只读索引，私人Gmail稿件或未授权内容不得推送公开Git。

## 6. 证据分类与最小统一记录
每条claim须有：
claim_id, claim_type, process_domain, geographic_unit, time_support, observation_or_model, source_id, source_version, source_locator, rights, raw_sha_if_available, unit, method_id, method_version, uncertainty, independent_check, provenance, contradictions, applicability, review_state。
分类：
- PHYSICAL_OBSERVATION：原始观测、仪器、QC、校准、时空代表性；
- DERIVED_DATA：可复算转换、插值、聚合、统计；
- MODEL_OUTPUT：公式、边界、参数、校准与验证范围；
- SCIENTIFIC_LITERATURE：原文/章节/假说/反证；
- LEGAL_METHOD：法规法域/版本/生效/报告年/适用活动；
- POLICY_COMMITMENT：国家承诺与行动计划；
- POLICY_ASSESSMENT：Scorecard等外部评价及其规则；
- ECOLOGICAL_OUTCOME：实际生态结果与归因条件；
- GOVERNANCE_DECISION：机构授权/人工决策与异议；
- SYNTHETIC_TEST：作者合成输入与软件测试。
状态分别表示 SOURCE_VERIFIED、RECALCULATED、MODEL_VALIDATED、EVIDENCE_INSUFFICIENT、MATERIAL_CONTRADICTION、NOT_ASSESSED、BLOCKED；不得把一个状态提升为另一状态。区分method aligned、算术复算、输入可信、效果证实、法定认证。每条主张可有多个维度而非总分。

## 7. 分层输出与接口
A Global Natural System Index（地球物理/生态空间分区）
B Process & Relation Atlas（机制/上下游/反馈）
C Country/Institution Mapping（治理实体与自然单元映射）
D Evidence Registry（来源、许可、版本、误差、反证）
E Climate Scorecard Policy Lens（外部政策评分与国家专题）
F CCZPS Scenario Comparison（可能性、权衡、人类决策）
G ECOChain Evidence Record（技术评审记录/版本/撤回/贡献，非认证）。
所有输出要保留人能读懂的“什么影响什么—为什么—证据是什么—不知道什么”。禁止在一个“全球综合指数”中无声混合物理量和政策评分。

## 8. 验收与下一轮Codex任务的决策门
本文件仅为研究范围/证据分类规范，不授权新一轮全球爬取、下载、模拟或开发。
下一步先审查：
(1) 原有CCZPS分区与本规范是否冲突；
(2) Climate Scorecard评分方法/覆盖/版权实际原文；
(3) 可复用全球GIS/生态区/气候带分类版本；
(4) ECOChain原权威目录及审批者仍未确认；
(5) 选择一个跨边界自然过程作有界验证（例如流域水文、热带泥炭/甲烷或全球CH4大气混合），再决定任务书与预算。
必须由Founder批准下一阶段工程任务；PR145和旧科学状态不变。

## CRP
核心：自然过程优先，国家制度映射其次；证据分层。
想法：全球分区—过程—政策—证据—治理关系图。
愿望：跨地域可复核、可理解的环境科学与文明治理体系。
决策：停止随机选国/单一排名；先形成全球范围与证据分类。
未决：原有分区、Scorecard方法精确版本、ECOChain canonical、全球边界分类。
下一步：Founder审阅此研究规范，再授权有界Codex任务。
关键词：ClimateOS/CCZPS/EcoEngine/Climate Scorecard/ECOChain/Global Biogeography/Climate Zones/Evidence Governance。
