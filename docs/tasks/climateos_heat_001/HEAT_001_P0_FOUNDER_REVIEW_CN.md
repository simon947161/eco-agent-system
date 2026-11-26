# HEAT–001｜人类热生态网络：Founder 科学评审

2026 年 11 月 26 日 · P0 文档审计 · [正式任务书 #173](https://github.com/simon947161/eco-agent-system/issues/173)

## 第 1 页｜建议先批准一次合成热账核验

一座建筑把余热送给邻近用户，能否少烧燃料？原先排热的街道是否更凉？下游河道是否承受更多热量？这三个问题都能检验，也可能得到不同答案。建议先验证第一本能量账能否闭合，并保留净收益为负的情景。街区降温、生态改善和全球减缓均等待各自证据。

## 第 2 页｜18 TW 的换算成立，热源清单仍缺原表

Fraley v1 第 5 页将 2022 年 580 EJ/年换成约 18.4 TW。六行相加确为 580 EJ/年；原表没有给出行业购电和发电损失的对应关系。IEA 另一张同年官方表列出全球总能源供应 632.0 EJ。决定哪一口径适用，要先追到能源品种、非能源用途及转化损失。18.4 TW 不能直接用作可回收热量。[六行逐项核算](HEAT_001_P0_DIMENSIONAL_AUDIT.md) · [IEA 表 A.6](https://iea.blob.core.windows.net/assets/42b23c45-78bc-4482-b0f9-eb826ae2da3d/WorldEnergyOutlook2023.pdf)

## 第 3 页｜46 TW 的分配与观测冲突，39% 的归因不成立

v1 第 4 页以 0.9 W/m² 乘地球面积得约 460 TW，将海洋之外的 10% 全给大气。被引热库存研究在 1971–2020 年的分配约为海洋 89%、陆地 6%、冰冻圈 4%、大气 1%。把陆地升温与融冰的能量移到大气一栏，改变了分母的物理意义。

18 ÷ 46 约为 39%，18.4 ÷ 46 为 40%。一股总排热功率除以大气净储热率，无法辨识它导致了多少升温。换用 1% 重算也不能解决归因。7 月的 v2 登记摘要仍保留 39%；其正文修订尚未获得页级核验。[观测原文及图 8–9](https://doi.org/10.5194/essd-15-1675-2023) · [两版本及十条引文](HEAT_001_P0_SOURCE_REGISTER.md)

## 第 4 页｜从余热出口跟踪到最终受体

锅炉、工业设备或数据中心排出热量 → 换热器截取可用部分 → 热泵消耗电力将温度提升 → 热网即时配送或储罐延迟释放 → 用户获得相同服务 → 余热和管损最终进入空气、水或土壤。温室气体另通过对外长波辐射影响地球收支。太阳、风、水和环境热也各有原本的去向。

收支检查从一台热泵开始：热端交付量等于冷端取热加电功（理想边界、近稳态）。跨过建筑边界后，继续追踪发电地、下风受体及下游水体。[可展开的物理机制图与六层账本](HEAT_001_P0_THERMAL_NETWORK_HYPOTHESES.md)

## 第 5 页｜哪些结果足以否决方案

|问题|支持继续的结果|会改变决策的结果|
|---|---|---|
|H1：等服务回收供热|一次能源和全生命周期排放均降低，舒适度、可靠性及生态护栏通过|新增泵电、管损或施工使其中一项反升；合理基线下变号则保留未决|
|H2：移开夏季排热|脆弱人群热暴露下降，全域暴露无增，生态护栏通过|热转给下风居民、夜间或枯水期河流；单个测点变凉仍须否决有害方案|
|H3：仅凭搬热能否推断全球降温|内部边对消，无可识别的全球移热收益|若能独立证明出射辐射、净能输入或排放改变，新机制才有单独检验的依据|

工程实测支持对热回收进行计量；气候和河网研究支持正视局地热负担。两类证据都没有证明任何 ClimateOS 场址已经获益。[热回收实测](https://doi.org/10.1016/j.egyr.2021.09.038) · [城市排热](https://doi.org/10.1002/2013JD021225) · [假设及判据](HEAT_001_P0_THERMAL_NETWORK_HYPOTHESES.md)

## 第 6 页｜已有能力能追溯证据，现场验证还缺配对资料

CarbonOS/AWT 可借用反事实、证据护照和缺项停止规则。EcoEngine 有字段适配和输入质量对照。BuildingOS 已有跨项目证据接收规范。Energy 研究提供电网与调度背景；建筑韧性公开摘要中的节费、停电保供仍待现场核验。

关键缺口是同一时钟上的热源温级、流量、泵电、需求和热储量，以及独立的气象、下风暴露、受纳水温与溶氧观测。现有研究索引能够定位来源，没有为本任务授予真实数据使用权。[固定版本资产清单与 P2 六道门](HEAT_001_P0_SIMULATION_GATE.md)

## 第 7 页｜Founder 的三个选择

|可审批方案|本次建议的边界|交回 Founder 的成果|
|---|---|---|
|**APPROVE P1 SYNTHETIC ENERGY LEDGER**（建议）|单一虚构源—需网络，固定服务、时间窗与库存；只批准合成能源会计|基线与方案、守恒残差、双计拒绝记录、净收益反号案例、独立复核入口|
|**REQUEST DATA**|先索取合法 v2 原件、IEA 部门映射、场址数据目录和使用权；应写明责任人、对象和权限|版本差异清单、可用/受限/缺失表；联系第三方或实际接入另批|
|**HOLD**|冻结本次结论，等待新材料或先请独立科学评阅人审稿|保留全部反证与重开条件|

三个选项均不会自动启动 P2。真实数据接入、现场或区域模拟、正式生态/减排主张、主线合并及部署分别提交审批。[详细准入标准](HEAT_001_P0_SIMULATION_GATE.md)

## 第 8 页｜研究索引与下一次交接（CRP）

|交接字段|冻结记录|
|---|---|
|知识|总耗散功率、大气储热率、TOA 净通量、ERF 及人群热暴露是不同的量。|
|想法|用同一转移编号连接来源、换热、输配、储存、用户和最终受体。|
|愿景|让建筑及产业用热与人、生态受体共同接受可复核的净效益检验。|
|推理|以等服务反事实核算替代，以控制体消除双计，以脆弱人群和下游护栏防止负担转移。|
|决定|冻结为 P0 文档；退回 39% 归因；保留 H1、H2、H3 及其反证；待 Founder 和独立评阅。|
|未解问题|v2 是否修正正文？580 EJ 如何与 IEA 流代码衔接？哪项热服务真实被替代？谁能合法提供匹配的受体观测？|
|下一步|Founder 记录三个选项之一；若仅批准 P1，先冻结合成功能单位、唯一流 ID、库存终态和拒绝规则，再开始账本工作。|
|关键词|人为排热、地球能量不平衡、储热、热泵、热网、反事实、局地暴露、水热生态、资料准入|

本包入口：[来源及版本](HEAT_001_P0_SOURCE_REGISTER.md) · [数字审计](HEAT_001_P0_DIMENSIONAL_AUDIT.md) · [机制图和假设](HEAT_001_P0_THERMAL_NETWORK_HYPOTHESES.md) · [仓库盘点和准入](HEAT_001_P0_SIMULATION_GATE.md)。既有 [CarbonOS 索引](https://github.com/simon947161/eco-agent-system/blob/2ec66ae41ae2e1d4a0f1aaa92aa98c9f0ff4c5b0/docs/research/carbonos/INDEX.md) · [综合科学任务交接](https://github.com/simon947161/eco-agent-system/blob/b143485ed0db7af48ecd19aa7b93c5f234cede46/docs/tasks/climateos_science_handoff_20261124_001/UNIFIED_TASK_INDEX.md) · [跨研究来源映射](https://github.com/simon947161/eco-agent-system/blob/055af110423a4759a88b01896e1813ede4abe50b/docs/tasks/climateos_explainable_science_web_001/SOURCE_MAP.md)。

**P0-A｜最小热生态网络实验（MVTEE，设计稿）。** [任务 #175](https://github.com/simon947161/eco-agent-system/issues/175) 承接 [#173](https://github.com/simon947161/eco-agent-system/issues/173)。[中文验收报告与 CRP](MVTEE_ACCEPTANCE_REVIEW_CN.md) · [实验设计与资料权限](MVTEE_EXPERIMENT_DESIGN.md) · [空间布局与敏感性](MVTEE_SPATIAL_LAYOUT_CONCEPT.md) · [五项账本](MVTEE_BOUNDARY_AND_LEDGERS.md) · [反证与阈值](MVTEE_FAILURE_MODES.md)。P1 合成会计待 Founder 单独批准。

**P1｜合成能源会计，等待 Founder 验收。** [#176 的正式决定](https://github.com/simon947161/eco-agent-system/issues/176) 更新了上述 P0/P0-A 交接时的审批状态。[中文验收报告与 CRP](p1/P1_FOUNDER_ACCEPTANCE_CN.md) · [冻结边界](p1/P1_SYNTHETIC_ENERGY_LEDGER_SPEC.md) · [空间与反号案例](p1/P1_SPATIAL_SENSITIVITY.md) · [离线测试及证据](p1/P1_FALSIFICATION_AND_TEST_RECEIPTS.md)。本包停在 ACCEPT P1 / REQUEST REPAIR / HOLD；P2、真实资料、合并及部署仍需另批。
