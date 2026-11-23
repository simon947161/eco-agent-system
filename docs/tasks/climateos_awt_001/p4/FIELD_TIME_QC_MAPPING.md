# P4 字段、时间、QC 与九类护照映射

评估日期：2026-11-24（Australia/Sydney）｜`READ_ONLY`｜`NO_RAW_DATA_DOWNLOADED`

授权：[Issue #164](https://github.com/simon947161/eco-agent-system/issues/164)。引用父级 [schema](../CLAIM_PASSPORT_SCHEMA.json) 的九类实体，**不生成真实passport，不改仅接受SYNTHETIC的运行器**。字段分级是对发布者文档的描述，绝非本轮独立实测验证。C01 [S02](https://cer.gov.au/markets/reports-and-data/safeguard-data/2024-25-baselines-and-emissions-data)；C02 [S04](https://www.transport.nsw.gov.au/operations/roads-and-waterways/environment-and-heritage/environmental-compliance/environment)；C03 [S06](https://zenodo.org/records/14165793) [S07](https://zenodo.org/records/14197882)；C04 [S09](https://datadryad.org/dataset/doi:10.5061/dryad.ht76hdrtc)。

## 原始语义和拟映射

DIRECT_MEASURED=文档描述的直接观测渠道；CALCULATED=平均/反演/库存估计；REPORTED=发布者陈述；MISSING=目标证据在已审材料未建立；UNKNOWN=未能查明。MISSING不证明原作者手里没有该项。没有实测原始行进入本仓库。

|来源字段/目标|级别|单位 / 时间支持|拟映射与局限|
|---|---|---|---|
|C01 facility、responsible emitter|REPORTED|标识；财年|未来dataset.spatial_scope关联候选；不当作批次标识|
|C01 covered emissions|REPORTED|tCO2e；2024–25|库存上报值；不是直接仪器测量。各气体栏的准确单位未读文件，UNKNOWN，不自行除GWP|
|C01 baseline / unit surrender|REPORTED|法规报告期；具体字段单位待核实|权益重叠提示，不是有项目/无项目物理对照|
|C02目录与PDF索引|UNKNOWN|采样日期、点位、单位未核实|403 STOP；不把浓度或监测点转作排放量/设施数|
|C03 plant characteristics、condition|REPORTED|厂级/工况，时间窗UNKNOWN|混合一手二手资料；逐行来源未验证|
|C03 methane-loss factors|CALCULATED|% methane produced；kg CH4/人口当量/年|因子不是直接测量的1000t批次累计排放；禁止跨厂拼成反事实|
|C04 instantaneous CH4 channel|DIRECT_MEASURED|文档称甲烷摩尔分数；原始通道未读取|来源声称移动观测；ppm不是kgCH4/day|
|C04 receptor CH4 ppm / Ubar / Wbar / Tbar / n|CALCULATED|ppm；m/s；°C；计数；窗口平均|由测量派生的统计量；不是未处理传感器原件|
|C04 Campaign / Month / Year / TIMESTAMP|REPORTED|TIMESTAMP为平均窗口末端|起始时刻、窗口长度、时区、DST、同步UNKNOWN|
|C04 CH4 / Low.CH4 / High.CH4|CALCULATED|kgCH4/day及研究给出的区间；campaign|扩散模型输出而非独立质量通量；不能与同一模型自我验证|
|C04 MOLength|UNKNOWN|README称unitless|名称和维度说明有疑点：先核查变量定义/归一化，不能直接套公式或自行纠正|
|三项详细候选的1000t湿重、DOC、批次ID|MISSING|t wet、kgC/kg wet、共同时间窗|没有同一物料批次链；不能用父合成值填空|
|产生/捕集/输送漏损/销毁/氧化的独立测量|MISSING|分别kgCH4或有基准状态的流量/组分|浓度×任意体积不是排放；体积须温压、干湿基、标况定义和流量同步|
|消化残渣湿重、碳、去向、后续CH4/N2O|MISSING|t wet、kgC、kgCH4、kgN2O及末端时间|未来必须区分N2O与N2O-N；未建立完整碳账|
|进口电、燃料、出口能量、运输|MISSING|kWh、燃料质量/热量、运输活动及计量期|计量边界和替代电源未知；不能用总CH4推定全部可售能量|

## 时间与QC深审

|问题|C01|C03|C04|
|---|---|---|---|
|时间尺度|财年报告；小时/日数据UNKNOWN|工况汇总；各测量起止UNKNOWN|安装前后campaign；末端平均时间已定义，具体时段未读|
|时区/DST/时钟同步|UNKNOWN|UNKNOWN|UNKNOWN；不能自行设PST/PDT|
|实际缺失率/行数|未读，null|未读，null；发布者声明行数不是本轮计数|未读，null；n/a、空单元语义由README描述|
|版本|报告年明确；表修订日期UNKNOWN|v1与新记录分开；不混用文件大小/摘要|2026-02-19展示版；记录URI固定，文件级revision UNKNOWN|
|仪器/校准/QC标记|未取得底层测量证书|方法名不能替代逐仪器校准|移动观测/扩散方法说明；校准证书、完整剔除规则未取得|
|气象共址|UNKNOWN|UNKNOWN|README明示June2022采用机场气象，其他为场址；需保留替代来源标记|
|空间/物料联结|设施年报≠1000t cohort|跨设施、混合证据不能无条件池化|同一匿名场址≠同一批次；不得重识别|

C02受阻后不做第三项详细测量审查之外的扩展，相关字段全部UNKNOWN。

## 九类实体逐一对照

|父schema实体|C01|C02|C03|C04|
|---|---|---|---|---|
|OBSERVATION|REPORTED库存上报；直接通道UNKNOWN|UNKNOWN|REPORTED方法/工况，原件UNKNOWN|DIRECT_MEASURED通道为来源陈述；平均值CALCULATED|
|PHYSICAL_ESTIMATE|REPORTED，计算方法未知|UNKNOWN|CALCULATED整场损失因子|CALCULATED扩散反演kgCH4/day|
|BASELINE_COUNTERFACTUAL|MISSING物理基线；监管限额不同|UNKNOWN|MISSING同cohort对照|REPORTED前后设计；MISSING可交换的同物料反事实|
|PROJECT_EMISSIONS|REPORTED年报，边界不匹配|UNKNOWN|CALCULATED片段，MISSING全项目边界|CALCULATED液体粪污储存片段；MISSING能源/残渣全链|
|LEAKAGE|MISSING共同边界|UNKNOWN|MISSING完整外移/末端路径|MISSING外移残渣及其他间接排放|
|NET_ABATEMENT_ESTIMATE|MISSING / 本轮不算|UNKNOWN|MISSING / 本轮不算|CALCULATED原研究变化量未重算；不可直接移植AWT|
|ADDITIONALITY_AND_ELIGIBILITY|MISSING个案适用证据|UNKNOWN|MISSING澳洲注册/方法证据|MISSING澳洲注册/方法证据|
|CLAIM_AND_CREDIT_RIGHTS|REPORTED交还单位线索≠完整权利|UNKNOWN|MISSING|MISSING|
|ASSURANCE_STATUS|UNKNOWN现场独立审计|UNKNOWN|UNKNOWN现场独立审计|UNKNOWN现场独立审计|

所有候选：SCIENCE=PENDING，REAL_DATA=DATA_NOT_READY，CREDIT=NOT_DETERMINED，原始哈希=null。字段接口可复用不等于可直接导入现有冻结schema。将来时间支持须覆盖具体测量窗与残渣末端，绝不把campaign日率线性扩展为百年cohort或监管crediting period。
