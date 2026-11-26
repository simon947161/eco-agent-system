# HEAT–001 ARCH–P0｜三维空间语义与多物理场架构只读评估

**状态：只读研究 · 2026-11-26 · 无安装、模拟或真实数据。** 授权与范围：[Issue #178](https://github.com/simon947161/eco-agent-system/issues/178)。上级科学基线：[Issue #173](https://github.com/simon947161/eco-agent-system/issues/173)、[Draft #174](https://github.com/simon947161/eco-agent-system/pull/174)。空间设计：[Issue #175](https://github.com/simon947161/eco-agent-system/issues/175)、[Draft #177](https://github.com/simon947161/eco-agent-system/pull/177)，固定 HEAD **369ee6b9703fedb54ca4da684920e6c23825d6ca**。获批 P1 合成账本：[Issue #176](https://github.com/simon947161/eco-agent-system/issues/176)、[Draft #179](https://github.com/simon947161/eco-agent-system/pull/179)，固定 HEAD **5a2039a2753142b2eb17665da2dba6c4a8648b14**。本分支独立基于 main SHA **9eb7577e145e76161f9f1cd8509348b19c2904cc**，不改写现有 Draft。

## 结论摘要

1. 保持规范 A–C–B：A 为虚构稳定低/中温废热源，B 为聚合季节性建筑服务，C 为热泵及可选水罐连接站。每种布局仅有 A–C、C–B 两条输热边；T 图中的第三边不是管线或新用户。
2. 空间图、热流和数值场是不同对象。3D 坐标说明对象位置和几何；压力/流量/输送延迟需要 1D 水力热模型；局部热场需要边界、材料和求解；受体结论需要独立观测及阈值。
3. 当前计算基线为 P1 L1 配对能量账。只有当输送延迟、闭环压力或管/水热容可能改变预注册决策，才提出 L2 瞬态 1D；本文件没有运行 L2。
4. QGIS、Blender、EnergyPlus、Modelica/OpenModelica、OpenFOAM 和 FMI 分工互补，尚无安装或集成承诺。FMI 是接口规范，不是物理求解器。
5. GPU01 资源为 **NOT_VERIFIED**。只读 Windows CIM 查询返回“Access to a CIM resource was not available to the client”；CPU/GPU、RAM 和磁盘均无法核验。未以设备名称或旧记忆猜测。

## 1. 固定 P0-A 设计依赖

本研究复用 [Draft #177 固定提交](https://github.com/simon947161/eco-agent-system/tree/369ee6b9703fedb54ca4da684920e6c23825d6ca/docs/tasks/climateos_heat_001) 的五份设计文档和五幅研究图。入口：[实验设计](https://github.com/simon947161/eco-agent-system/blob/369ee6b9703fedb54ca4da684920e6c23825d6ca/docs/tasks/climateos_heat_001/MVTEE_EXPERIMENT_DESIGN.md) · [空间布局](https://github.com/simon947161/eco-agent-system/blob/369ee6b9703fedb54ca4da684920e6c23825d6ca/docs/tasks/climateos_heat_001/MVTEE_SPATIAL_LAYOUT_CONCEPT.md) · [五账边界](https://github.com/simon947161/eco-agent-system/blob/369ee6b9703fedb54ca4da684920e6c23825d6ca/docs/tasks/climateos_heat_001/MVTEE_BOUNDARY_AND_LEDGERS.md) · [失败矩阵](https://github.com/simon947161/eco-agent-system/blob/369ee6b9703fedb54ca4da684920e6c23825d6ca/docs/tasks/climateos_heat_001/MVTEE_FAILURE_MODES.md) · [图组源文件](https://github.com/simon947161/eco-agent-system/tree/369ee6b9703fedb54ca4da684920e6c23825d6ca/docs/tasks/climateos_heat_001/figures)。

|项|锁定定义|
|---|---|
|节点|A 热源、C 热泵/水罐连接站、B 建筑服务端；L/T 之间稳定 ID 不变。|
|L 紧凑线性|A–C 低温段 80 m、C–B 高温段 40 m 单程沟长；相对标高 A/C/B 为 0/+2/+3 m。|
|T 错位三角|低温段 120 m、高温段 180 m 单程沟长；相对标高 0/+6/+3 m。|
|空间解释|概念沟长，不是 GIS 实测。图示 A–B 直距 100 m 仅为示意。每段有供/回管；不可混淆单程沟长与两根管的总实长。T 无 A–B 第三条管。|
|受体|R人、R水和沿线土壤类别沿用 #177；真实位置、响应和阈值未知。|
|服务对照|R0 锅炉、R1 本地空气源热泵、L/T 联网臂；逐时同温级服务、可靠性代理和匹配期末库存。|

固定图只表意，不是比例图、测绘成果或物理场。闭环静水压在上升与下降段可抵消净静扬程，但不代表可忽略高点压力、充水、局部损失、摩擦或瞬态压力波；这些是未来物理层需求，不是本报告的计算结果。

## 2. 最小 3D 物理场景图提案

场景图只承载拓扑、几何、语义和资料护照。求解器网格、状态和边界作为单独版本化结果，避免把可视化模型包装为“数字孪生”。

|对象|最低字段|规则|
|---|---|---|
|Scene|scene_id、schema_version、design_version、geometry_status、来源提交、CRS、垂直基准、坐标轴/单位、时间基准|概念场景可用任意右手局部 XYZ 米制；没有真实 CRS 时不得伪装为经纬位置。|
|Node|stable_id、角色、x/y/z、位置状态、端口、设备温度边界、来源/许可/误差|网络仅 A/C/B 三节点；受体锚点不自动成为热用户。|
|PipeSegment|segment_id、transfer/edge ID、from/to port、layout、沟长、中心线顶点、供回管、介质、管径、保温层、弯阀、沿线环境|明确每条供/回物理管或双管封装含义；标清每管热损还是管对热损。|
|Equipment|设备 ID/类型、热流/电/质量端口、位置、能力和曲线来源、运行状态|合成值标 SYNTHETIC；厂家/实测参数须另有权利与验证记录。|
|Receptor|ID、空气/水/土/人类别、范围、断面/时段、目标终点、引用证据、阈值状态|没有观测、覆盖域或阈值，效果标 UNKNOWN 而不是 0；排热量与受体响应分开。|
|Boundary|控制体、边界方向、介质、交换位置、初末库存归属、外部条件|每个物理转移只有一个全局 ID；相邻控制体引用同一 ID，合并时对消。|
|Passport|SYNTHETIC/MEASURED/DERIVED/UNKNOWN、来源 URI/提交/哈希、所有者、许可用途、有效时间、不确定度、评阅状态|无来源权利与准许用途的真实数据不进入场景。|

真实坐标需水平 CRS/历元、垂直 CRS 或基准、轴序、精度与测量日期；局部设计坐标须标明任意原点。QGIS 文档区分 CRS 与垂直参考/高程钳制；显示配置不构成测绘精度保证。几何路线中心线应与 CFD 网格分别版本化。

最小字段示例（提案而非现行软件契约）：

    schema_version: heat-scene/0.1-proposal
    scene_id: HEAT-001-SYNTHETIC-MVTEE
    design_commit: 369ee6b9703fedb54ca4da684920e6c23825d6ca
    geometry_status: SYNTHETIC_CONCEPTUAL
    coordinate_frame:
      kind: local_cartesian
      axes: right-handed XYZ; z up
      length_unit: m
      origin: arbitrary A reference; not georeferenced
      vertical_datum: null
    nodes:
      A: synthetic_waste_heat_source
      C: heat_pump_storage_station
      B: aggregated_seasonal_building_demand
    edges:
      A-C-L: low-temperature pair; trench 80 m; CONCEPTUAL
      C-B-L: high-temperature pair; trench 40 m; CONCEPTUAL
      A-C-T: low-temperature pair; trench 120 m; CONCEPTUAL
      C-B-T: high-temperature pair; trench 180 m; CONCEPTUAL
    receptors:
      R-person: response UNKNOWN
      R-water: response UNKNOWN

示例路线 XY 未从沟长反算，不声明平面几何与沟长相符。不得用此提案重新生成或覆盖 #177 图组。

## 3. 物理层级与保真度门

|层级|用途与限制|升级证据|
|---|---|---|
|L0 概念拓扑|讨论节点和路线，不算输热、温升或收益。|真实坐标需有数据权利、精度、测量来源。|
|L1 P1 配对账|已获批逐时合成能量/火用/损失/经济/碳账；可查守恒和假设下敏感性。不能解压力瞬态、实际土壤热场或受体响应。|只有 L1 不确定区间跨过一个预注册决策界线，且遗漏物理有可能改变决策，才考虑 L2。|
|L2 候选瞬态 1D|压力/摩擦/流量、输送时间、供回温、管水与材料热容、保温到环境换热、泵曲线与高点压力。回答 L/T 是否改变排序。|需固定边界、工质、解析基准、误差容限和决策目标；另需 Founder 批准。|
|L3 局部 3D 热流/地层|仅针对 L2 无法表示且会改变决策的局部设备、弯头、空气/水羽流或地层热扩散。|需真实授权几何/边界/材料依据、网格和时间步收敛、解析或实验基准、校准与独立验证。网格通过不等于模型获验证。|
|L4 微气候/生态/人体|连接热场与具体人群或生态指标。|需界定空间覆盖、时段、受体终点、混杂、合法监测、阈值来源和专业独立复核。|

“需要升级”先定义决策问题、最小有意义差异 δ_decision（连同单位）、输入误差和可接受模型误差。若 L1 配对差区间离决策线很远，L2 缺少决策价值；若跨线，需判断遗漏物理的量级能否超过 δ_decision。阈值须在看输出前由 Founder/领域评阅人冻结，本报告不臆造数字。

## 4. 候选工具兼容性矩阵

|工具|建议角色|候选接口|限制与当前决定|
|---|---|---|---|
|QGIS|具 CRS、线路、地形/垂直参考、受体图层的空间数据来源与 3D 检查。|输出授权的中心线、高程、受体图层到场景图；带来源、CRS、精度和许可。|官方 3.44 手册提供 3D Map View、地形高程栅格/网格与垂直参考。仅可视化和数据治理，不解流体/热。未查本机安装。|
|Blender|场景表达、几何沟通和资产交换。|接收 QGIS 导出的通用 3D 对象；经 glTF/GLB 交付几何/属性。|手册支持 Metric 单位显示与 glTF 场景/网格/材质/动画；unit scale 不代表物理仿真。不是测绘 CRS 或热求解。|
|EnergyPlus|建筑围护结构、HVAC、热水需求与建筑侧服务边界。|未来可在 B 表口与系统主时钟交换服务/状态。|25.2 外部接口指南描述 FMI Co-Simulation FMU 导入/导出；建筑侧模型不能代替区域管网水力。|
|Modelica Buildings/OpenModelica|潜在 L2 一维动态流体、区域供热、建筑/储热系统。|以一套动态模型承载 A/C/两段管/B 边界，必要时与 EnergyPlus 单独耦合。|Buildings v14.0.0 于 2026-10-05 发布，含 DHC、Fluid、ThermalZones；发布页称在 OpenModelica 1.26.3 等环境测试。OpenModelica 当前指南列 FMI 2.0 supported、FMI 3.0 experimental。未验证具体组合/许可/本机安装。|
|OpenFOAM|有明确重要局部问题时的 L3 CFD 后备。|只为特定局部问题接收经过版本化的边界。|官方文档要求案例、网格、物理边界、模型和网格质量核查。收敛不等于真实验证。当前不运行/安装。|
|FMI|FMU 模型交换/联合仿真接口层。|约定 variable、unit、causality、端口方向、时间通信、状态、错误和求解器责任。|3.0.2 规范定义 Model Exchange、Co-Simulation、Scheduled Execution；接口不保证不同工具版本支持同一能力，也不是主控器或物理模型。|

官方技术来源：[QGIS 3.44 3D View](https://docs.qgis.org/3.44/en/docs/user_manual/map_views/3d_map_view.html) · [QGIS CRS/Vector Properties](https://docs.qgis.org/3.44/en/docs/user_manual/working_with_vector/vector_properties.html) · [Blender Scene Units](https://docs.blender.org/manual/en/latest/scene_layout/scene/properties.html) · [Blender glTF 2.0](https://docs.blender.org/manual/en/latest/addons/scene_gltf2.html) · [EnergyPlus 25.2 External Interfaces](https://bigladdersoftware.com/epx/docs/25-2/external-interfaces-application-guide/introduction.html) · [Modelica Buildings](https://simulationresearch.lbl.gov/modelica/) · [v14 下载/兼容信息](https://simulationresearch.lbl.gov/modelica/download.html) · [OpenModelica FMI 指南](https://openmodelica.org/doc/OpenModelicaUsersGuide/latest/fmitlm.html) · [FMI 3.0.2 规范](https://fmi-standard.org/docs/3.0.2/) · [OpenFOAM 用户指南](https://www.openfoam.com/documentation/user-guide) · [OpenFOAM 网格要求](https://www.openfoam.com/documentation/user-guide/4-mesh-generation-and-conversion/4.1-mesh-description)。

仓库方向将 GIS/CFD/数字空间接口列为未来路线；CCZPS-Lite 是证据和决策支持底座，现有 Boundary Interface Layer 是气候边界分类原型，不是热网求解器。因此建议加接口/证据适配，而非重复建设通用热引擎。核查入口：[README](https://github.com/simon947161/eco-agent-system/blob/9eb7577e145e76161f9f1cd8509348b19c2904cc/README.md) · [ROADMAP Phase 5](https://github.com/simon947161/eco-agent-system/blob/9eb7577e145e76161f9f1cd8509348b19c2904cc/ROADMAP.md) · [CCZPS-Lite](https://github.com/simon947161/eco-agent-system/blob/9eb7577e145e76161f9f1cd8509348b19c2904cc/cczps_lite/README.md) · [现有空间边界示例](https://github.com/simon947161/eco-agent-system/blob/9eb7577e145e76161f9f1cd8509348b19c2904cc/boundary_interface_layer/README.md)。

## 5. 时间、空间与物理接口契约

|合同域|必须冻结|无效/未决条件|
|---|---|---|
|时钟|UTC、区间 [t_start,t_end)、dt、历法/闰年、时区来源与转换版本。|重复/缺失小时未处理或采样规则未知，不能配对。P1 是合成非闰年 8760 小时。|
|单位与方向|功率 W、能量 J、温度 K（展示可换 °C）、温差 K、压力 Pa（绝压/表压注明）、质量流 kg/s 或体积流 m³/s 及密度；流入控制体为正。|变量缺单位、量纲类别或符号时拒绝。区分通量和库存，不能用 kW 代 kWh。|
|物理边|唯一 transfer_id、起止端口、介质、值/单位、适用时段、边界温度与误差。相邻控制体复用同一 ID。|重复边、边失踪或重复发电损失时拒收。水泄漏/补水是质量与焓边，不是“管损”。|
|空间|坐标系/历元/垂直基准、几何来源/精度/许可，端口引用稳定 node/edge；网格与中心线分开版本化。|概念几何不能覆盖真实中心线；缺垂直基准的 Z 不当绝对高程。|
|状态/边界|罐温层、管/水热容、设备状态、源可用性、泵控制、初始状态和边界热流。|相邻时步库存不连续、边界交换未闭合则停止。|
|耦合|主时钟/主模拟器、通信步、事件时序、代数环策略、状态回滚能力、FMI 能力位、错误中止传播。|不同步、耦合不收敛或变量方向不一致，禁止只看年度合计。|
|误差/数据权利|测量误差、模型形式、时间/网格误差、不确定性相关性、来源与使用权。|未知变量写 null 和原因，不当零；精度不足以分辨目标差异就保留未决。|

## 6. 候选 L2 设计协议（仅思想实验，本轮未运行）

**问题：** 在 P1 固定输入和 L/T 几何之上，增加管内输送延迟、管/水热容和高点压力约束，会否改变 L/T 相对 R0/R1 的服务及配对排序？

1. 固定 P1 HEAD 5a2039a…、P0-A HEAD 369ee6b…、同一 UTC 输入和 A–C/C–B 沟长，所有新参数仍须明确标 SYNTHETIC。
2. 使用一个 1D 水力—热模型表达供/回管；逐段算流量、压降、温度、延迟、管水/材料库存。闭环静压沿上/下段抵消；分别验最低压力、摩擦和局部损失。
3. 一次改变一个因素：输送延迟、管热容、高点压力裕度；再做有限预登记交互。不要同时改变路长、土温、保温和泵曲线后归因于高程。
4. 四臂 R0/R1/L/T 保持服务与库存匹配；输出逐时服务、备用、压力边界、段损失、泵电、库存、残差、L/T 排名和是否跨决策线。
5. 核验需有解析管段基准、质量/能量守恒、时间步减半收敛、独立重建与故障记录；运行前冻结误差和 decision threshold。
6. 停止条件：边界/参数/接口不足、出现非物理压力或库存、服务不等、残差超限或时间步细化导致排名不稳定时，标 INVALID/UNRESOLVED。

这不是代码或模拟结果；没有生成新输入、安装或运行 Modelica、EnergyPlus、QGIS、OpenFOAM。

## 7. 验证与 GPU01 资源状态

未来验证须分层：解析/极限算例；节点、边和总控制体守恒；网格/时间步收敛；用校准数据拟合、用独立留出观测验证；跨求解器只比较共有边界与接口误差；受体站点/日期独立保留。CFD 网格通过质量检验不是现场预测验证。

**本机资源审计：NOT_VERIFIED。** Windows CIM 查询在此宿主被拒绝，CPU 型号/线程、显存、可用 RAM、磁盘容量/余量都没有读到。没有检查候选软件版本，不假定装有任何求解器。官方文档未给出一组可直接套用到本机、网格规模和时间步均未知的统一 CPU/GPU/RAM/disk 指标。若日后 Founder 先批 L2/L3，需由在场用户控制下只读收集硬件，再按实际模型做小型 profiling 后写资源预算；在那之前平台可行性仍 NOT_VERIFIED。

本会话 P1 复放只用 Python 标准库，34/34 测试通过；这仅说明合成账可重放，不推断任何多物理求解器能在 GPU01 运行。

## 8. 限制、来源和 CRP

**硬边界：** 本分支只有文档；无真实场址/区域数据、环境效益主张、CFD/GIS/微气候运行、软件安装或部署。P2 NO-GO。#174/#177/#179 仍是独立 Draft，不在此分支修改或合并。

|CRP 项|冻结记录|
|---|---|
|Knowledge|拓扑≠3D 几何≠水力/热输运；空间、热、碳和受体是不同账。|
|Idea|定义规范 A–C–B 场景与边/时间契约，再按决策需要选物理保真度。|
|Vision|让模型结果成为可复核、有人类审阅的环境决策证据。|
|Reasoning|先 L1；只有输送延迟/压头/热容可能改变决策才考虑 L2，受体判断独立验证。|
|Decision|ARCH–P0 完成只读评估；L2/L3 未批准。|
|Unresolved|GPU01 资源、软件版本/许可、真实空间数据权利、物理参数、受体阈值/观测。|
|Next|Founder 选 APPROVE L2 BOUNDED DESIGN / REQUEST EVIDENCE / HOLD。|
|Keywords|HEAT–001、MVTEE、A–C–B、3D scene graph、transient 1D、FMI、QGIS、OpenFOAM。|

**审阅即停止。** 本报告不申请安装或运行任何软件；真实数据、模型实施和环境结论都需另行审批。
