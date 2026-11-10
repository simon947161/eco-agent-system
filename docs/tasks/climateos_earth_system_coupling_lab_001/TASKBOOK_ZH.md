# CLIMATEOS-EARTH-SYSTEM-COUPLING-LAB-001
## Founder总主线｜寻找 ClimateOS 多变量时空协调、差异场计算、物理耦合与可能性推演的可执行机制
版本：执行任务书 v1（2026-11-10 Australia/Sydney）
授权：Founder 明确要求 Codex 开始研究与编程、试验、反复证伪；不要停留在术语解释、架构图、下一轮“小流域审查”或另一个门户网站。
仓库：simon947161/eco-agent-system
工作分支：research/climateos-earth-system-coupling-lab-001
冻结父提交：PR149 D ea6fd79b41138cbcb16f9bd1aadd68f6a4b771df。保持PR143–149全部Draft及科学状态。
**唯一北极星**：使 ClimateOS 有能力将多个来源、时空尺度、空间支撑及不同物理意义的环境变量带入共享环境状态，以可组合的科学机制进行多方向耦合/反馈计算，在大量可重现的实验和反证中寻找环境变化的显化条件、敏感点、传播路径与情景可能性，最终辅助AI+人类理解环境和选择行动。**不把任务降格成 ENSO 气象站、甲烷公式、单一流域或某个数据API的修补。**

## A. 先回到最初源头，不再偏航
第一步必须审阅：
1. docs/00_MASTER_ARCHITECTURE/SYSTEM_RELATIONSHIP_MAP.md，ECOENGINE_V2_SYSTEM_DEFINITION.md，CCZPS_LITE_V0_4_REVIEW.md，历史 CCZPS Possibility Computing / differential field / forcing layer / climate-zonal governance 原始研究，EcoEngine、ClimateOS v2、Weather/WaterOS/LandOS/BioOS/Hydrology、GIS/QGIS模型与测试。
2. PR143–149：甲烷物理公式/辐射强迫0.569344413968403W/m2、合成物料账、全球自然系统证据Atlas及关系图、60年RONI、合成水量守恒、PR149 Wagga 46个合格春季的真实历史条件频率及缺测；全部仅在原适用域使用，不因接入中枢自动推为现实耦合定律。回看PR149评审 https://github.com/simon947161/eco-agent-system/pull/149#issuecomment-6764046885。
3. 目前哪些真实数据/模型/接口可直接复用、哪些是定性联系、哪些仅合成；形成 EXISTING_CAPABILITY_MAP，逐项提供精确源码路径/函数/证据和验证状态。
4. 回溯 CCZPS 原始分区、时空积分、动态模拟、Differential Field Inference，“差点/差异场/差分计算”的作者语义；不能擅自认定“差点计算法”只有一种数学含义。分别研究空间差、时间差、物理梯度/散度、有限差分、扰动敏感性和可辨识性。科学上适用哪一种必须标明，不能用名称代替公式。

## B. 研究对象不是“单链”，而是共享环境状态和相互作用
建立**一个最小且可运行的共享时空环境状态（Space-Time Environmental State）**，优先兼容已有schemas而非竞争替代：
- 唯一 field identity / CF standard_name（若适用）、单位/量纲、phase（气/液/土壤）、参考条件，intensive vs extensive、instantaneous vs accumulated、flux vs state、observed vs derived vs modelled vs synthetic；
- geometry/CRS/grid or point/area/vertical support、cell bounds、coordinate transformation, overlap weights, conservative vs nonconservative remapping; country只是治理映射而非物理网格；
- time bounds/UTC+local clock/season/calendar/timestep/support interval、lag and tendency；月累计不得直接代小时通量；不同步则拒绝或有解释地聚合/插值；
- source version/license/byte hash/QC/uncertainty/covariance/missing value/method/version/evidence-level；
- 共享 state 的多版本快照、历史追溯和可逆的状态差异，不抹掉原观测和独立来源。
优先实现7~10种共享场：temperature, pressure, wind vector, humidity, precipitation rate/accumulation, radiation forcing, soil moisture, evaporation, runoff/streamflow, CH4 concentration/burden等；缺真实数据可在**标注合成的耦合实验**中提供这些字段，但不冒充已经取得的多变量实测。
重要：允许存在**稀疏、不完整的环境状态**。缺一个变量时只阻断依赖它的计算边，不阻断所有独立模型；某条边仅候选或诊断，不强行形成数值交互。

## C. 可组合模型与耦合机制（要比较多种方案）
设计**最小可控 Model Component 接口**（initialize / required_fields / provided_fields / units / grid / current_time / step(dt) / inspect / checkpoint / reset / evidence），优先评估兼容CSDMS BMI v2、ESMF/NUOPC clock/connector/mediator的概念；参考 CF/NetCDF 用于变量语义。只借鉴，不引入沉重依赖、不迁移仓库、不声称它们自动给科学结论。
至少在同一小型运行时演示 4 类可互换组件：
(1) 环境场与物理驱动（温度/气压/风/湿度/辐射），明确哪些关系是理想化假设；
(2) 水分与能量交换（降雨、蒸发、土壤水、地表状态），有明确守恒/库存/通量；
(3) ENSO等边界/条件性统计驱动（仅外部forcing/统计条件，不把SON指数当实时预报或因果项）；
(4) CH4全球丰度→ERF已发表函数（独立较慢的全球尺度，不得直接把它耦合成Wagga地区次日温度/降雨）。
实现 **Coupler/Field Mediator**：字段和单位匹配、时空overlap及面积权重、clock synchronization、简单单向/双向反馈、显式推进 vs 固定点迭代或松弛、守恒残差与收敛门槛、失败时回滚。
至少比较 3 种策略：independent baseline（单组件无交换）；one-way coupling（受控边界强迫）；two-way iterative coupling（有限次交换与收敛，数值不稳定就显式失败）。
先选少量可解释的**理想化但物理量纲自洽**耦合组件，已发表或基础守恒方程优先；不得把气压梯度、湿度、风速、地表通量“凭直觉加权成全球危害分”。任何人为设定响应系数必须带ASSUMED_NOT_VALIDATED标签并做敏感性分析。
实现按不同时间尺度共存：大气快时钟、地表/水慢时钟、季节ENSO指数、全球CH4年尺度。不可直接对不同时间粒度插值创造虚假因果或把“同刻”概念偷换。
原始数据和模拟态不可无声混入一个等权模型；区分 OBSERVED_STATE / CONSTRAINED_ESTIMATE / SIMULATED_STATE / HYPOTHESIS_SCENARIO。

## D. 差异场、扰动、反馈与“显化点”
建立至少5种可测试的操作（物理一致性优先）：
1. baseline→scenario 的差异场 ΔX(s,t) 与对照域差值，清楚声明参考状态；
2. 空间梯度/时间变化率/通量散度的有限差分，边界条件、网格大小、收敛阶与单位；
3. 单变量/多变量联合扰动的有限差分敏感度、交互项（不能简单等同真实因果效应）；
4. feedback gain、正负反馈、时滞、非线性阈值与滞回的诊断，检查数值稳定/可识别性；
5. uncertainty ensembles / Monte Carlo / parameter sweeps，保留相关误差与缺失条件，不将算法频率冒充真实事件发生概率。
显化结果定义为：在给定边界、时间尺度、模型及其输入假设下某个被声明的环境状态/风险阈值的超越概率、敏感区域、领先指标、滞后传播与鲁棒性；**这是条件性模型结果，只有经过独立观测验证才能声称区域预测技能**。
至少对一个可解释实验得到随时间的多变量曲线、两种空间格点（或点与区域）对照、耦合vs非耦合差异、敏感度热图或同等数值输出，以及一个“多变量同时变化后风险阈值出现不同结论”的可复算反例。没有必要为展示单独建设花哨门户。
可模拟一个高温/水汽/风/土壤干燥联合条件的**合成阈值场景**；它不能被包装为Wagga真实概率，也不能把CH4 ERF无凭据映射局地温升。

## E. 多规模验证与科学对照，真正找机制
建立**系统化实验矩阵**，不要仅写一千条同一断言：
- physical invariants：质量、能量、非负库存、维度、边界通量、数值残差；
- discretisation/stability：dt减半、dx减半、收敛/发散、Courant等适用条件；
- spatiotemporal mapping：点到面误用、面积守恒、月/日错位、不同CRS、分辨率/时间聚合；
- causality/leakage：后验数据泄漏、错误中介、伪因果/多重比较、合成→真实标签越界；
- coupling strategy：无耦合/单向/双向/迭代，循环依赖与收敛、误差传播；
- extreme/edge：缺值、样本少、零风、异常边界、强迫超域、突变与滞后；
- counterevidence：已发表其他机制/模型方向相反时，登记对照与拒绝无依据结论。
**建设可生成、可复现、可比较的10,000+实验运行能力**（seed、配置散列、证据等级、运行状态、误差指标、失败分类、对照组、资源成本）。第一批先运行数百~千个差异化smoke案例，再按真实成本在有界预算内运行≥10,000个参数/场景/模型耦合测试（不是等价于10000个独立科学实验）；将来可组织更多批次，**不得自动无限循环或创建常驻机器人**。
成本护栏：第一批单机总实验壁钟不超过20分钟、单批数据不超过200MB、无外部付费API、不得因模拟生成大体量原始文件；环境/额度不足可早停并如实记录已运行次数、原因与单位计算耗时，且保留可继续的runner。将固定种子和新种子分开，不准为了看起来好调整参数后隐瞒负例。
输出比较报告必须回答：哪种耦合策略在何种已声明假设下更稳定、保守、可复现；哪些场景反而劣于独立模型；哪些敏感点受缺测/时空尺度影响最大。**科学上的“不知道”与工程上的“代码通过”分开**。

## F. 至少一个端到端 ClimateOS 研究问题
题例：“给定 ENSO 状态、区域气温、湿度、气压/风、降雨与地表水分状态，变化过程怎样相互推动，哪些组合下季节性水分压力/热风险更易显化？模型输出如何随物理参数、时滞和空间支持改变？”
必须以同一研究执行链完成：
问题 → 当前可取得的多变量资料目录 → 共享时空状态 → 单组件&耦合模型 → 差异场/敏感度/阈值 → 证据/反证/误差 → CCZPS多未来比较 → ECOChain审查记录建议 → 人类决策门。
如果现有真实数据不足，必须**并行**提供 (a) 基于实际PR147/149观测的只读基线/历史统计证据，和 (b) 清楚标记的合成/理想化多变量耦合演示；绝不跨越真实-合成边界做伪“验证”，也不因此放弃耦合机制实现。
最重要的可验收事实：能够在同一接口实际调度≥3类不同物理变量及≥2种互相影响的组件、运行≥2种耦合策略与反事实场景，输出单位正确且有证据边界的数字差异。

## G. 对照世界科学实践，既吸收也质疑
只读调查并制作“ADOPT / WRAP / DEFER / REJECT”比较：
- CF Conventions climate/forecast metadata, CSDMS BMI, ESMF/NUOPC, ESMF regridding；
- 现有生态/气象/水文耦合方法、reanalysis vs observations、过程模型校准与数据同化方法；
- agentic实验管理、hypothesis testing、ensemble sensitivity、ODE/finite volume工具候选。
优先查看官网和原始论文、固定版本和开源许可；**不要因为发现成熟工具就立即迁移平台或引入重依赖**。研究它们如何实现时空同步、字段交换、守恒、求解器调度及实验评估，并以可运行最小机制对照。也要寻找不支持Founder初始假设的物理/统计反证。
权威方法参照：
https://cfconventions.org/
https://github.com/csdms/bmi
https://earthsystemmodeling.org/nuopc/
https://earthsystemmodeling.org/regrid/
以上均为候选，不是默认技术栈许可/兼容批准。

## H. 架构、连续学习与治理
坚持 ClimateOS原层次：
Observation/Source Connectors → Shared Environmental State → EcoEngine physical runtime + optional external solvers → CCZPS Possibility Computing → ESG++ institutional translation → ECOChain evidence history → Human governance → feedback。
“学习”本轮指**实验记录、校准提案、反证、模型版本、参数搜索和审查后的改进**；不允许偷偷在线自修改科学公式、自动将合成参数升为权威或不经人审通过治理建议。
Agent只负责规划运行、寻找可合法读取数据、组合模型、比较假设、生成反证、记录失败；不得成为公权力和科学认证者。
所有结果对齐可追溯Evidence Passport：输入hash, model version, hypotheses, parameters, spatial/time boundaries, uncertainty, quality gates, trace IDs, test evidence, outcome, decision maker, rollback.
继续维持 PR143–149物理结果、草稿和科学门；不能将甲烷PR147公布值或Wagga 76.5%当成共享状态的新区域气候耦合参数。ECOChain canonical仍NOT_FOUND，Enotebook仍PENDING。

## I. 交付而非只写方案
目录 docs/tasks/climateos_earth_system_coupling_lab_001/
- TASKBOOK_ZH.md；REUSE_AUDIT.md；MECHANISM_RESEARCH.md；SHARED_STATE_SCHEMA.json；MODEL_INTERFACE.md；COUPLER_DESIGN.md；NUMERICAL_METHODS_AND_ASSUMPTIONS.md；EXPERIMENT_MATRIX.md；EXPERIMENT_RESULTS.json/summary.csv；COUNTEREVIDENCE_AND_FAILURES.md；DATA_AND_MODEL_RIGHTS.md；PHYSICAL_AND_STATISTICAL_GATES.md；FOUNDER_REPORT_ZH.md；CCZPS_ECOCHAIN_HANDOFF.md；QA_AND_VALIDATION.md；NEXT_SESSION.md；CRP_HANDOFF.md；REVIEW_REQUEST.json；HANDOFF_STATUS.json，以及真实代码/tests/fixtures。
- **实际可运行最小耦合软件**，不能只有JSON和Mermaid；优先加到现有cczps_lite/integration或原EcoEngine兼容目录。CLI：validate-state、list-components、run-baseline、run-coupled、compare-scenarios、sweep-experiments、explain-failure（名字可与现有规范协调），每个命令都须有真正输出和可重放测试。
- ≥3个有实际输入输出的模型组件、≥2种耦合方式（最低），单/双向对照最好齐备；一项可计算的环境状态差异场与联合扰动，数据可追溯，明确合成vs真实；大量运行报告给真实run_count、通过率、失败分布、参数空间、样本/对照平衡、性能。
- 中文Founder大字/Slides式展示**首先说明：目前我们到底发现了什么可复用“多物理耦合机制”，什么验证被阻塞，如何在十万次迭代中继续进化**；不报告“地球气候已解决”或虚构未来预测。要给一个可执行的下一迭代计划，但不得未经批准自动启动第二长期研究。
- 独立stacked Draft PR，父为冻结PR149 HEAD，附精确R/D/CI/测试结果/适用边界，PR保持Draft，Founder转交后ChatGPT复核。不合并、不部署、不付费、不联系第三方、不运行长期后台代理、不改生产模型/环境。

## J. 绝对反偏航验收
以下任一情况视为没有完成：
- 只写一个“地球系统架构说明”没有可运行跨物理模型协调和比较；
- 以某一站点/流域/某个NOAA接口作为**下一轮唯一主线**；
- 仅做ENSO单变量统计，或把CH4/Wagga/水文硬拼成虚假因果模型；
- 运行万次相同公式而没有独立场景、物理残差、数值稳定、反例与不确定性；
- 合成数据冒充实测、统计关联冒充物理因果、AI得分冒充真实风险或认证；
- 发生数据阻塞后改为继续无限爬源，而不利用合成但有物理标识的沙盒推进耦合机制；
- 无真实GitHub源码、可重放实验与科学失败报告。
执行目的：**找出让AI+人类能够逐渐掌握跨时间、跨空间、跨介质的环境动力变化与选择可能性的工程-科学机制**。科学严谨不等于只许做最小局部验算；有界物理耦合实验与不断反证才是本任务主线。
