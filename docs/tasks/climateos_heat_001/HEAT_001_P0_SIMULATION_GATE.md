# HEAT–001｜现有能力、证据缺口与模拟准入

2026-11-26（悉尼）。**P0 仅文档。P1 待 Founder 决定；真实场址数据 DATA_NOT_READY；P2 NO-GO；独立科学评审 PENDING。** [任务书](https://github.com/simon947161/eco-agent-system/issues/173) · [三条假设及反例](HEAT_001_P0_THERMAL_NETWORK_HYPOTHESES.md)

## 仓库盘点

主仓库默认分支 main = [9eb7577e145e76161f9f1cd8509348b19c2904cc](https://github.com/simon947161/eco-agent-system/commit/9eb7577e145e76161f9f1cd8509348b19c2904cc)。读取主树、贡献约定、开放 PR 列表、相关分支和任务索引。从该 main 独立分支提案，研究材料集中在既有 `docs/tasks/` 结构。主树完整列表未见名为 `INDEX.md` 或 `NEXT_SESSION.md` 的全库研究入口。下列其他研究的索引及交接属于其各自草稿；本包将导航和 CRP 交接放入[中文评审末页](HEAT_001_P0_FOUNDER_REVIEW_CN.md)，以固定版本链接回原入口。

|领域及证据状态|可复用的科学、数据或工程能力|进入 HEAT 还缺什么|
|---|---|---|
|CarbonOS #131 / Draft #132|P1-A 方法来源、D/D3 否证与资料准入；D3 三候选停止，零原始观测文件。可沿用来源/用途/时钟/QC/人工审查字段|历史科学准入仍待定。甲烷浓度与气体通量不能直接填入热通量，旧候选不重新开跑。[任务 #131](https://github.com/simon947161/eco-agent-system/issues/131) · [CarbonOS 索引](https://github.com/simon947161/eco-agent-system/blob/2ec66ae41ae2e1d4a0f1aaa92aa98c9f0ff4c5b0/docs/research/carbonos/INDEX.md) · [交接](https://github.com/simon947161/eco-agent-system/blob/2ec66ae41ae2e1d4a0f1aaa92aa98c9f0ff4c5b0/docs/research/carbonos/NEXT_SESSION.md)|
|AWT #162 / Draft #163、#165|已读任务书、历史交付回执、资产审计及 P4 停止报告。合成 1,000 t 四情景分开记录观测、物理估计、反事实与主张。复用证据护照和“缺项即未决”|P4 最终 NO_SUITABLE_DATASET。已有实验与识别的许可条件属于 AWT，不给热研究授权或实测热源。[任务 #162](https://github.com/simon947161/eco-agent-system/issues/162) · [资产审计](https://github.com/simon947161/eco-agent-system/blob/9aea387a4261b913163b3be3197597089d9e9414/docs/tasks/climateos_awt_001/EXISTING_ASSETS_AND_GAPS.md) · [P4 停止记录](https://github.com/simon947161/eco-agent-system/blob/75efe58b2443faf22446c6209216e0ef5cf56784/docs/tasks/climateos_awt_001/p4/README.md)|
|EcoEngine 主线适配器、#122 与 Draft #153|兼容本地 JSON 记录的字段映射；既有四站任务注明 Open-Meteo 现况/预报为模式产品。公开成对对照有四组输入治理可比、两组元数据不兼容|无共同预测真值、实测辐射/热通量或场址热暴露验证。历史派工不能证明今天的采集器或接口运行。[主线适配器](https://github.com/simon947161/eco-agent-system/blob/9eb7577e145e76161f9f1cd8509348b19c2904cc/cczps_lite/integration/ecoengine_v192b_adapter.py) · [四站来源](https://github.com/simon947161/eco-agent-system/issues/122) · [成对对照](https://github.com/simon947161/eco-agent-system/blob/fcea1629d345596cb4094a1a6686d5e6750c2304/docs/tasks/ecoengine_v200_private_method_comparison_001/PAIRWISE_RESULT_PUBLIC_ZH.md)|
|独立公开 BuildingOS 主线|已核对冻结的 Evidence、Claim、Review、Lifecycle、Ledger 标准及 ClimateOS → BuildingOS 跨域证据接收契约。适合把设备、服务、证据批次与人的批准关联|该契约是文档。缺设备曲线、BMS 时序、现场调试和热工校准证据。[规范索引](https://github.com/simon947161/BuildingOS/blob/b0329def1a870483e8fd9b4f4de4e2413fd08fca/docs/BUILDINGOS_SPECIFICATION_INDEX.md) · [跨域契约](https://github.com/simon947161/BuildingOS/blob/b0329def1a870483e8fd9b4f4de4e2413fd08fca/docs/BUILDINGOS_CLIMATEOS_CROSS_DOMAIN_EVIDENCE_INTAKE_CONTRACT.md)|
|Energy 主线研究；建筑/社区能源韧性 Draft #171 的公开摘要|澳洲能源系统档案区分电网、调度、储能及证据等级。能源韧性摘要区分杜博、鲍勒尔节费与停电保供；历史本地 INDEX v0.3 有 11 类资料缺口|本轮直接读取公开摘要，原本地索引及附件未核。两地节费、备用回路、关键服务时长、停电试验均未验证。还缺可授权的逐时热负荷及边际供热替代。[澳洲 Energy 研究](https://github.com/simon947161/eco-agent-system/blob/9eb7577e145e76161f9f1cd8509348b19c2904cc/research/australia-renewable-energy-system-interface-analysis.md) · [建筑能源摘要，energy 条目](https://github.com/simon947161/eco-agent-system/blob/055af110423a4759a88b01896e1813ede4abe50b/cczps_lite/dashboard/science/content.js)|
|Public Strategy Atlas Draft #130；EcoChain / E4 Draft #145|Atlas 核实到模块及公开来源层级。#145 有可审查的 evidence schema、角色和版本摘要；可借用主张与证据对应关系|未读取受限 Atlas 资料。#145 自报 ECOCHAIN_CANONICAL_NOT_FOUND；权威 E4 接入、独立审签、正式登记位置未验证。[Atlas 模块](https://github.com/simon947161/eco-agent-system/blob/e3d8f074e0e1ba5e9614c3f4c5a2b973746b2ab7/apps/public-strategy-atlas/README.md) · [EcoChain 审计入口](https://github.com/simon947161/eco-agent-system/blob/ae1050a621ac794e447f9ac047865d90b2f04b03/docs/tasks/climateos_global_method_evidence_ecochain_001/README.md)|
|跨研究索引 Draft #169、#171|已读统一科学任务索引和 29 项来源映射；能引用各阶段冻结版本、合成/真实标签、许可/停止条件|水文路线拓扑未验证，既有合成水热耦合成果不能当作实测街区输热模型。索引、软件与科学准入的状态分别保留。[统一索引](https://github.com/simon947161/eco-agent-system/blob/b143485ed0db7af48ecd19aa7b93c5f234cede46/docs/tasks/climateos_science_handoff_20261124_001/UNIFIED_TASK_INDEX.md) · [跨研究来源映射](https://github.com/simon947161/eco-agent-system/blob/055af110423a4759a88b01896e1813ede4abe50b/docs/tasks/climateos_explainable_science_web_001/SOURCE_MAP.md)|

## P1 候选｜合成能量账

建议批准的最小任务是指定 **一个虚构余热源、一处等服务热需求、一个热泵和可选储罐**，做离线能源会计，含对照、逐边审计和反例。只允许使用作者编制且逐项标为 SYNTHETIC 的能量流、设备参数和时间窗。先冻结功能单位、一次能源折算、库存归属、符号与单位；可用合成碳因子演示 H1 的账本边界，不对真实减排给结论。

|待审批的验收项|预期可检查结果|停止条件|
|---|---|---|
|对照与反例|同一服务/起末态的基线与方案；至少覆盖无需求旁路、跨时段库存、另计泵电、重复转移编号，以及用电代价使净收益反号|工作负荷/服务不等、反弹未定义或真实资料混入，则停止比较|
|守恒与重放|每个设备、管网和合并系统均出区间残差；未舍入的合成数以事先确定的单位精度闭合，误差容限、算例与重放结果可复核|漏列热源/受纳方、重计、kW/kWh 混用、负库存、越容、无源 COP、缺量被当零，应拒绝输入或标记未决|
|解读|分列终端供热、取走的环境热、附加一次能源、电耗、假定碳因子及净值范围；报告对替代基线/季节错配的敏感性|恒等式通过只接受为工程会计检验；不能签发环境效益。P1 完成即停审|

## P2 候选｜场址或区域微气候的单独准入

现阶段各项未形成**同一场址、同一时间窗、具备权利且可独立验证**的证据包。下表是未来可审查的最低输入。先提交目录及权利证明，再由 Founder 确定是否授权采集。以下没有任何区域模拟结果。

|门|必须呈交的证据与质控|缺失的后果|
|---|---|---|
|权利与责任|每份气象、地表、能源、生态、人口资料的所有者、版本、用途、下载/派生/再发布权限、保存期限；去标识化与审批责任人；获准接入时记录文件哈希|公开网页、论文 CC BY 或旧项目授权不能代替数据许可；维持 METADATA_ONLY。任何 Council 资料另行授权|
|逐时天气与地表|温湿、风速风向及高度、短/长波、降水、混合条件；地形、建筑高度/形态、覆盖、反照率、热参数、土湿/水分可用性。记录分辨率、时区/DST、坐标、缺测和仪器校准|无法区分热源、风场和辐射贡献；日均或邻站资料未经证实不能填补小时/微尺度|
|源—管网—需热端|逐时源热量、温级、介质、高度、工艺负载、排放几何；供回水温和流量、辅机电表、储量、旁路、备用、基线服务量与用热时钟一致|年能耗不能给出热浪时段源强；排热格网只能作为带误差的先验|
|人群与生态受体|受体位置、暴露时段及获准的聚合权重；上/下风和未干预对照；上下游水温、流量、溶氧、生态敏感期；地下储热另需土壤/地下水约束|无下风/下游或脆弱群体覆盖，无法排除风险转移，H2 停止|
|独立验证|事先锁定同传感器等级的对照与留出站点/日期，涵盖昼夜、极端热及正常期；源强与温湿度分别验证，保留仪器高度、校准、漂移和观测误差|同一数据调参又验收、仅以地表遥感温度代替 2 m 气温或以天气模型输出充当现场真值，均不得进入效益判定|
|不确定度与决策|预注册效应指标、允许误差和最小可辨效应、样本/天气覆盖、边界和参数敏感性、误差相关性；按留出站/事件报告偏差、RMSE、极值/区间覆盖，和简单基线比较；独立热工/微气候/生态审查|观测与结构误差足以淹没目标效应，或相反结果未能解释，保留 INCONCLUSIVE。数值阈值需依据仪器与当地受体先行批准|

**决策顺序。** Founder 可选 `APPROVE P1 SYNTHETIC ENERGY LEDGER`、`REQUEST DATA` 或 `HOLD`。若选择 REQUEST DATA，建议先要 v2 可合法审阅的 PDF、v1 表 1 的 IEA 流映射、候选场址资料目录/权利说明；联系第三方、获取受限或付费数据须另批。P2、任何实际模型开发/CFD/区域气候模拟、现场试点、环境效益宣称、部署或合并均需新的明确决定；本 P0 不授予这些权限。
