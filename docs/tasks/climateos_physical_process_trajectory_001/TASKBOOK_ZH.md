# CLIMATEOS-PHYSICAL-PROCESS-TRAJECTORY-001
## Codex 执行任务书｜全球环境过程主干—支流渐进推演、定量验证、反证与治理接口
日期：2026-11-10 Australia/Sydney
Founder明确授权立即执行有界研究与小型离线科学计算；不需再次问是否开始。
仓库 simon947161/eco-agent-system
工作分支 research/climateos-physical-process-trajectory-001
冻结父HEAD PR146 1e6b13e2b80c50e6d20e05a4e88819eb0de93488
前置科学基线PR143/144/145/146及其ChatGPT评审回执；先核远程状态、NEXT_SESSION和旧架构，不覆盖/合并旧PR。
目标：**从地球自然过程的主干开始，沿着有依据的机制和观测逐段推进，形成真正可复算、可反证、可解释的三条环境过程轨迹；把可计算与不可计算的断点精确标出来；最终回到EcoEngine→CCZPS→ECOChain证据治理。** 不开发另一个Atlas网站，不把国家政策评分当物理参数，不追求把每片叶子/每条支流都测尽。

## 0. 必须先审计并复用
- PR146 Global Natural Systems Evidence Atlas：M49身份/25单元/7边/三路径/0%真实GIS几何、query/trace/validation、Scorecard元数据、A/B/C评审。
- PR143甲烷14公式与机制图、P1气体状态、PR144甲烷生成/捕集/燃烧/氧化四边界质量账、PR145跨法域证据审查；既有D3、P1-A、PR140/141科学闸门保持。
- 原有CCZPS分区/可能性计算、EcoEngine差异场/强迫、GIS/QGIS水文及天气采集、Public Strategy Atlas；仅在现有兼容接口增加薄计算/验证，不重建竞争schema。
- 逐条识别旧代码、已运行结果、合成输入、真实观测、文献方法和缺失变量；不要将“关系图可查询”说成“物理链可计算”。

## 1. 统一的科学轨迹与逐段推进协议（核心）
每条轨迹用固定结构记录：
PROCESS_ID, NODE_ID, EDGE_ID, physical_quantity, unit, medium/phase, spatial_domain, temporal_support, mechanism, equation_id, assumptions, boundary, inputs, observed_or_derived, source_version_locator, data_rights, uncertainty, calibration, counterevidence, model_validation, numerical_output, residual, status, next_missing_input。
边必须分类：CONSERVATION_LAW / PHYSICAL_MECHANISM / EMPIRICAL_RELATION / STATISTICAL_TELECONNECTION / MODEL_ASSUMPTION / HYPOTHESIS / GOVERNANCE_CONTEXT；**不能把概率相关性画成确定性因果，也不能把数学上可运行当作真实验证**。
逐段状态：EXACT_PHYSICS_CALCULABLE / OPEN_DATA_RECALCULATED / SYNTHETIC_TESTED / CONDITIONAL_STATISTICAL_ESTIMATE / STRUCTURAL_QC_ONLY / BLOCKED_MISSING_DATA / BLOCKED_MODEL_VALIDATION / NOT_INFERABLE。允许不同阶段分别拥有不同状态，不能一条链的局部通过让整条链通过。
遵循：先主干物理和可观察量→关键支流/反馈→逐段数值/量纲/守恒→不确定性传播→外部反证→停止或进入下一段。每个断点给出“具体缺哪个参数、观测、模型、空间/时间边界，最小可修复条件是什么”。避免无限探索。

## 2. 轨迹A：甲烷源→大气负荷→辐射→气候响应
A1 源与汇：自然/人为生成、氧化、捕集、OH及其他汇，源率kgCH4/time、库存kgCH4；复用PR143/144，不把合成填埋账当实测全球排放。
A2 大气：观测混合比ppb/ppm、气体状态/湿干基准、质量库存、输送混合、寿命与化学损失；区分局地浓度、全球平均、全球负荷、全球排放源强，必须有代表性/时间尺度转换条件。
A3 辐射：NOAA AGGI/IPCC AR6等权威公开方法核实CH4丰度→辐射强迫/有效辐射强迫的公式、背景气体、重叠吸收、时间/基线、单位W/m2；如果许可可读且输入充分，运行**小型已发表关系的解析复算**，否则只给带单位的方程与明确BLOCKED，不自造气候灵敏度。
A4 响应：响应核/能量平衡/反馈、全球平均温度与区域降尺度分别列门；不得把W/m²直接当°C，不自定高度GWP修正，不声称某吨甲烷的地域性气候影响已证实。
A5 必须给出一张可执行性阶梯：现在PR143/144已算到哪、全球开放数据能补哪一步、到气候响应还缺什么。至少一个实际可复算的有界片段（可继承且复核旧结果）；是否完成新的辐射片段取决于权威公式和输入准入，禁止硬接。

## 3. 轨迹B：ENSO海气耦合→Walker/环流→区域天气概率→环境风险
B1 机制：热带太平洋SST梯度、信风、温跃层/上升流、对流/Walker环流、Bjerknes反馈、热力学与动力学基本量；用权威文献和明确方向/反馈区分，不能用“ENSO一定导致某地干旱”。
B2 指数：ONI/RONI/Niño3.4、SOI、时间窗、基准期、指数修订、异常定义；核实官方最新版本，不把不同指标直接拼成同一历史序列。
B3 观测：最多选一个合法开放的历史ENSO指数与最多两个区域气象序列（澳大利亚与印尼/其他有代表性地区），固定时间、许可、空间代表性、缺测与QC；如数据访问受阻，只运行有清楚来源的最小已发布数值例子/合成检验，不虚构相关系数。
B4 有界计算：条件概率/分组差异/时间滞后、季节分层、基准期与样本数、置信区间/自相关与非平稳性检查；明确相关≠因果。**至少做一个可以重算的历史统计检验（前提是真实合法数据已准入），否则BLOCKED并给最小输入清单**。
B5 反证：比较相反事件、其他模态IOD/SAM/季风、季节、长期变暖、区域差异、观测/模型外推限制；对照独立文献的机制与效果范围。将物理机制与统计推断分开。
B6 输出中文：某一ENSO状态会如何改变某区域天气概率、什么时候可能不成立、哪一步还无法定量；不要提供伪精确天气预报。

## 4. 轨迹C：流域上游→支流/水库/蒸发/取水→下游流量
C1 以PR146尼罗河路径为定性案例，确认NBI官方站点方向和边界，按河网拓扑和控制体建立逐节点质量守恒：dS/dt=Qin+Qlateral+P_area−Qout−abstraction−evap−other_losses；严格统一m3/s、mm、m2、时区与采样间隔，允许地下水、回归流与库容变化未知。
C2 从主干到支流的**渐进式**计算：先2–4个关键节点的合成守恒与误差传播，再尝试最多一个合法开放的同时间窗实测站点/水库/降水片段；不能要求测完所有小支流或叶片。
C3 如真实水文数据可用，进行上/下游时间滞后、质量收支与残差分析；残差不是自动等于蒸发，可能是未测取水/支流/地下水/库容/误差。
C4 分清物理上必然的流向、动态调度/传输时滞和水权/责任的行政判断。不得把流量差直接归因某国、某坝或某企业。
C5 输出“可计算的主干、不可测的支流、守恒残差和下一站最小观测需求”；至少运行合成小链，真实部分视数据准入而定。

## 5. 三条轨迹之间找规律，但禁止伪统一
研究共同结构：源/汇/库存/通量、输送、反馈、滞后、边界、尺度、非线性、不确定性与可识别性。
必须分别回答：
- CH4与ENSO：温室气体长期背景强迫与ENSO内部变率的区别，是否存在文献支持的调制关系、因果识别困难、不能把两者直接互相归因；
- ENSO与河流：ENSO通过区域降雨/蒸发影响径流的条件机制；尼罗河流域的实际ENSO遥相关需**专门区域证据**，不能直接用澳洲关系外推；
- CH4与流域：甲烷排放/湿地水位/降雨/温度的可能耦合、跨时间尺度，不能将全球CH4浓度直接转成河流流量。
形成3x3关系矩阵：KNOWN_MECHANISM / OBSERVED_ASSOCIATION / CONDITIONAL / NOT_IDENTIFIED / BLOCKED；每条关系提供来源和反证。比较动力学、热力学、统计学和治理学的解释层次。禁止用一套未验证的全球影响积分混算所有环境变量。

## 6. Climate Scorecard 澳大利亚评分问题｜独立专项核查（Founder需可对外提醒）
读取PR146 SCORECARD_METHOD_AND_COVERAGE.md所记具体冲突：澳大利亚卡将43%目标基年写为2030，而官方Climate Change Act 2022 s10(1)(a)写为2005。**这是待独立复核的线索，不是已最终裁决的编辑错误**。
直接核对原站现行卡的确切句子、上下文、发布日期/修改日/缓存版本与官方澳洲法律原文（条款、汇编版本、生效时点），并检查是否为笔误、表述歧义或另有政策年份。保存精确定位、必要的短引文、截图/合法页面收据或访问受阻记录；如果当前页面已更正，区分历史版本与现行版本。
同时核实其评分“五项×20”的真实方法、是否可复算50分以及该处笔误是否实际影响评分；**不能未经重算就说评分错了**。
单独生成 SCORECARD_AU_CORRECTION_BRIEF_ZH.md 与 EDITOR_NOTE_EN_DRAFT.md：后者礼貌、客观、可供Founder作为国家经理自行审核后联系编辑，**不自动发邮件/评论/联系机构**。清楚标“事实”“解释”“需要编辑确认”。不因一个文本问题否定整个Scorecard网站或其贡献。

## 7. 真实来源与选择性复算
最多12个新增主要权威来源主题、3条主轨迹、每轨迹最多2个开放数据候选；优先官方NOAA/WMO/IPCC/BOM/NBI/UNFCCC及可信学术原始研究，核版本、许可、时空、QC、哈希和原文公式；无许可不提交原始文件。403/499/防护页不绕过，不使用私人Council数据、付费API、外部联系。
数据可得性不决定科学真理；模型可运行不等于因果证实。允许少量合成守恒/统计反例，但必须与真实数据复算分离。
每条轨迹都要至少一项实际执行的数字检查；其中B优先真实历史统计，A优先权威辐射公式局部复算，C优先合成水文守恒+公开水文片段。无法合法完成时如实记录DATA_NOT_READY和最小缺口，不无限扩展。
反证研究必须主动寻找与简单解释相矛盾的实测或文献，按SOURCE_SUPPORTS/SOURCE_CONTRADICTS/NOT_COMPARABLE分类，不为迎合Founder强行证明假设。

## 8. 可运行代码、接口与验收
优先复用PR146的cczps_lite/integration/global_natural_systems_atlas.py、PR143–145的机制/计算/证据接口，增加最小trajectory query/evaluate/trace功能。每段输出inputs、公式、单位、时空边界、来源、结果、误差/残差、断点和人话解释。
至少三个端到端示例：CH4、ENSO、水文；一个交叉关系解释示例；一个Scorecard文本纠错审查样例。分别测试单位、气体相态、质量/能量守恒、时间滞后、未知支流、样本外推、气候因果夸大、政策分数充当物理参数、证据缺失、来源版本、假引用和越权认证。所有测试记录实际运行日志与可复算SHA，不仅文档。
结果路由：EcoEngine负责物理/环境过程，CCZPS负责条件情景比较与权衡，ESG++翻译Scorecard等制度资料，ECOChain记录证据审查、反证和版本；人类最终决定。不要建新网站、另一个地图数据模型或生产认证平台。
所有科学闸门保持原状态，除非经Founder单独授权和独立科学验收；本轮任何局部真实统计通过不自动升级PR143/144/145/146全链科学状态。

## 9. GitHub交付
目录 docs/tasks/climateos_physical_process_trajectory_001/
TASKBOOK_ZH.md、README.md、FOUNDER_REPORT_ZH.md、TRAJECTORY_METHOD_AND_SCHEMA.md、TRAJECTORY_CH4.md、TRAJECTORY_ENSO.md、TRAJECTORY_HYDROLOGY.md、CROSS_PROCESS_CAUSAL_MATRIX.md、COUNTEREVIDENCE_REGISTER.md、OPEN_DATA_AND_SOURCE_REGISTER.md、QUANTITATIVE_RECALC_RESULTS.md、MODEL_GAPS_AND_NEXT_INPUTS.md、SCORECARD_AU_CORRECTION_BRIEF_ZH.md、EDITOR_NOTE_EN_DRAFT.md、CCZPS_ECOCHAIN_HANDOFF.md、QA_AND_VALIDATION.md、NEXT_SESSION.md、CRP_HANDOFF.md、REVIEW_REQUEST.json、HANDOFF_STATUS.json、必要的scripts/tests/evidence。
Founder中文报告优先回答：三条科学主线各推到哪一站？真正算出的数是什么？从哪里来的？还能往前推吗？为什么卡住？什么关系是真实规律、什么只是相关？甲烷到辐射到气候还缺哪几个环节？ENSO的概率怎样从观测得来？尼罗河守恒残差如何解释？Scorecard澳洲问题到底在哪里、是否影响评分？
创建独立stacked Draft PR，基线为本分支冻结父HEAD；精确R/D和CI真实状态，附源码、来源、测试、中文Founder报告、独立评审请求。不要合并、部署、发法定认证、联系Scorecard编辑、申请私人数据、购买、启动长期自动采集或扩大实验。Founder把PR+HEAD转交ChatGPT后由ChatGPT独立只读科学评审，评审后再决定下一阶段。

## 成功判据
不是资料数量，而是：3条主干能逐段追踪与计算/拒绝；每段都有可查来源与反证；至少实际执行每条主线的有界数字验证或如实说明阻塞；Scorecard澳洲问题有可对外核查的事实报告；明确CH4-ENSO-流域跨过程哪些规律成立、哪些仍不可识别；可回到CCZPS/ECOChain的科学治理主线，不陷入无限地图建设。
