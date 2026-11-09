# METHOD_CROSSWALK：保留制度差异

来源ID与法律/访问等级见 [GLOBAL_SOURCE_REGISTER](GLOBAL_SOURCE_REGISTER.md)。四个对照范围：AU、US、EU、NZ；NZ因403只有限摘录，不能称四国法规均完整核查。国际框架没有被算作第五个法域。

|统一字段|Australia（继承PR144）|United States G01|European Union G02|New Zealand G03|
|---|---|---|---|---|
|version / reporting_year|NGER C21 2026-07-01；2026–27；CER旧指南2025–26分离；ACCU2025项目期另列|eCFR页面时点2026-11-02/10-30；年度T；申报适用年需重核|1999/31/EC合并2024-08-04；运行/后期照管；成员国报告期另核|索引2023-01-01；本轮不能确认之后所有修订|
|activity / purpose|填埋年度清单、项目减排信用和NSW许可监测三者不同|MSW landfill GHGRP年度温室气体报告|填埋场安全、环境控制/监测、成员国许可|废物经营参与者ETS排放申报（摘要范围）|
|system_boundary|物理body/pipe/device/cover；NGER某条排除设备燃烧排放；ACCU含反事实|HH-1废物历史；HH-6模型与HH-8回收气反推两路线；装置损失另入对应项|场址/分区；许可规定监测代表性；不提供统一GHG总账|各设施/各废物类别当年处置净吨数；不是当年实测羽流|
|CH4 / C / CO2e basis|IPCC GgCH4/GgC；NGER tCO2e、标准m³分别标识；GWP必须版本固定|HH变量以metric tons CH4；CO2e汇总另需适用GWP|气体组分、压力及监测语义；没有Annex统一CO2e公式|reg5 E单位tonnes；CO2e解释链本轮未完整取得，保留待核|
|wet/dry / volume_reference|湿废物DOC分母；NGER干15°C/101.325kPa；勿默认Nm³=0°C|HH-1 W as-received wet waste；回收气标准状态依原式/监测条款，本文未独立图读全部参考值|按具体监测/许可，不能自行填同一参考态|吨数称量口径、气体状态对照 UNKNOWN；不得借AU值|
|temporal / spatial support|年度FOD vs分区测量 vs小时装置监测；不能无声相连|处置年x至报告T；回收气计量位置和装置对应|AnnexIII§3按分区代表；运营/照管不同频率及许可调整|年度×设施×废物类；无现场气体时序准入|
|formula_id|IPCC Eq3.1–3.6；NGER5.4D、5.15、5.17H/L/M；ACCU Eq10/11/15/17/18|98.343 HH-1/4/5/6/7/8；本轮不转录未目视核对的公式图片|AnnexI§4、AnnexIII§2–3属于义务，不伪造排放公式|reg5：E=(A−B)C；A毛吨数，B分流吨数，C默认或EPA批准UEF（索引摘录）|
|parameter provenance|各法表/专家测量；1.336与16/12来源不同|HH表与监测；HH-8收集效率估计不是全场直接量测|许可、监测计划、设备与气体管理记录|默认1.023或批准UEF；禁止自选优化因子|
|uncertainty|合成算术精确不等于现场低不确定性；k/OX/采样代表性留缺口|FOD参数、回收/收集率、装置运行与仪表误差；本轮未做量化|空间代表性、采样频率、许可条件；不把频率视为不确定性值|默认因子代表性与UEF证据 UNKNOWN；未计算|
|instrument QC / calibration|NGER通量箱/扫描、ACCU运行/组成/气量；继承PR144测量表|98.344(a)称重、(b)组成校准、(c)流量计；具体频次保留法规条件|AnnexIII监测方案；仪器校准/具体程序需成员国与许可补足|reg4/UEF相关测量校准原文未取得|
|independent verification|NGER专家/审计及ACCU审计各有权责，程序不替代|EPA报告审查不等于本工具获授权独立认证；本轮未核完全部Part98程序|主管机关/成员国许可；不推定任意AI为核验机构|EPA批准UEF不等于本程序可签发；完整核验制度 UNKNOWN|
|permissible defaults|仅对应方法/条件；默认值非现场实测|相应HH表与法规限定；无跨法域借值|无通用本任务排放默认值|reg5索引默认1.023；单位与适用条件完整链待核|
|missing-data rules|ACCU s79参数专属；本原型更窄：拒绝缺数|98.345按参数用质量合格的前后/可用邻值；废物量有同周日规则；不是一律0|监测/许可补证，不假设统一GHG插补|UNKNOWN；403后停止|
|evidence requirements|废物历史、组成、P/T/水汽、气量、运行、校准、原始文件与报告期|历史处置、气量/组成、校准和装置映射；缺测替代标识|许可、分区代表性、气体管理、监测/照管记录|称量/分流/分类和UEF批准文件；全条件未取得|
|recognition authority|澳洲相应监管机关/合法审计机制；非ClimateOS|US EPA及适用法规程序；非ClimateOS|成员国主管机关；非统一AI签发|NZ EPA/适用法规程序；非ClimateOS|

程序实现范围比上述法规窄：仅 `AUTHOR_LEDGER_V1_NOT_NGER_NOT_ACCU` 合成守恒账。任何方法ID、法域、版本或报告年移花接木均拒绝。没有把NZ摘录或US未图读公式写进法定求解器。

科学机制统一的是物理量、边界与证据字段；制度判定允许不同。合成账的四接口为：

```text
S0 + G + I = S1 + C + K + L
C = D + P + ΔSpipe
D = X + slip
K = O + surface
E_inside = surface + P + slip
S0 + G + I = S1 + ΔSpipe + E_inside + L + X + O
```

所有项均为同一区间 kgCH4；L横向离界去向未知，不自动归入已避免排放。反应耗掉的CH4用44/16转为CO2仅作C元素账；不是甲烷分子仍守恒，更不是CO2e或净减排。既有公式/常数与不确定性推导继续引用 [PR143注册表](../climateos_methane_physics_knowledge_engine_001/EQUATION_REGISTRY.json) 和 [PR144物料账](../climateos_au_landfill_methane_methods_001/LANDFILL_PHYSICS_AND_MASS_BALANCE.md)。
