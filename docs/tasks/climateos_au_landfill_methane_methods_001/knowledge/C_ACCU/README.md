# C_ACCU｜Carbon Credits (Carbon Farming Initiative—Reducing Methane Emissions from Landfill Gas) Methodology Determination 2025

[返回研究索引](../../README.md) · [机器知识包](package.json)

## SOURCE_MASTER

出版者：Federal Register of Legislation / Clean Energy Regulator。版本：F2025L01430 registered2025-11-28; in force confirmed2026-11-09。层级：STATUTORY_METHOD_PLUS_ES。

[官方入口](https://www.legislation.gov.au/F2025L01430/asmade)；阅读级别：TARGETED_SECTIONS_WITH_LOCAL_BYTES_AND_VISUAL_EQUATIONS。只外链/本地字节收据/自有中文笔记；不提交法定PDF或ES全文。

- [C_ACCU收据](../../source_receipts/C_ACCU.json)：ACQUIRED；SHA-256 `8cdc30e2a2c17fcc182928b8242cac8b9596e85de459b8d4e0970ba80a708a52`；原件位置 `runtime_data/au_landfill_methods/C_ACCU.pdf`。
- [C_ES收据](../../source_receipts/C_ES.json)：ACQUIRED；SHA-256 `11bd6b5d9f1ff0f60b22d5e9aa03db4012c059d09b0d01fed2bef4a7b4f5a0e9`；原件位置 `runtime_data/au_landfill_methods/C_ES.pdf`。

## SECTION_MAP

- s2 commencement; s5 duration; s6–7 definitions
- s13–30 activities/types/eligibility
- s37–51 conversion and baseline
- s42 Eq9–11 pp31–33
- s43 Eq12–14 pp33–35
- s44 Eq15 p36
- s70–79 reporting/monitoring pp59–67
- Schedule1 regulatory proportion; Schedule2 revocation
- ES pp31–32 device/operation explanation

## KNOWLEDGE_CORE / EQUATION_EXTRACT

项目净减排是规定的反事实比较。装置送入量、毁灭量、基线、近地表本会氧化量和项目排放各有规则。监管默认设备效率不等于现场真实毁灭率。

- **C-eq10** — s42(3) Eq10 p32/PDF38：`MCom,h=MSent,h(1−PLh)(1−TLh)DECom`。变量：M:m3CH4；PL/TL/DE:fraction；DEengine=1,others=.98；PL/TL按设备/升级/运输类型。域：specified boiler/controlled flare/engine/upgrading cases。
- **C-eq11** — s42(4) Eq11 p33/PDF39：`MCom,h=DECom sum_a(Oh,a MSent,h,a)`。变量：M:m3CH4；O:0/1；a:hour；DE:fraction。域：other combustion devices; not blanket hourly algorithm for every type。
- **C-eq15** — s44 Eq15 p36/PDF42：`MCom,Ox=MCom,NCT OF(1−WB)`。变量：M:tCO2-e；OF:NGER5.4(1)；WB:baseline combustion fraction。域：counterfactual oxidation deduction, not physical double oxidation。
- **C-baseline** — s48 Eq17 p39/PDF45；s49 Eq18 p40/PDF46：`AB=MCom,NCT WB`；新项目`WB=max(WB,Reg,WB,Def)`。AB/M单位tCO2-e；WB无量纲，Reg依Schedule1，Def依项目类型/年次；不得任意选择更小的基线。

## SKILL_PROCEDURE

1. 先区分项目类型、碳税废物和non-legacy资格。
2. 将设备类型对应s42路线，不把所有装置统一套Eq11。
3. s78流量/组成同条件同窗口；Eq11运行标志每分钟检查、整小时判定。
4. 缺测回s79及报告/审计要求；本程序直接拒绝，不计算信用。

## CASE_EVIDENCE

合成60分钟全合规则O=1；一条False则0；缺条拒绝。原页Eq10/11/15已本地渲染核查，未把PDF图片再发布。

## METHOD_LIMITATIONS

- 许可证/注册/额外性/完整报告与审计资格未判定
- CERS工具页面当次提示calculator under development，不声称已复现官方工具
- s6装置定义与s42(4)other-devices的具体应用需评审，不自行扩大适用
- s79缺测替代不是本工具实现范围

## CONNECTIONS

E07 physical DRE vs regulatory DE；CCZPS只保留证据/审查身份，不批准ACCU。

详见[物料账图](../../LANDFILL_PHYSICS_AND_MASS_BALANCE.md)与[条款crosswalk](../../SECTION_AND_EQUATION_CROSSWALK.md)。

## LEARNING_PATH_ZH

1. 98%是否代表全场收集效率？

   参考答案：否；装置完整燃烧定义和DE默认与捕集路径不同。

2. 一分钟失败为何不能把物理排放写0？

   参考答案：Oh,a=0是规则中的合规运算标志，气体仍需物理去向账。

3. Eq15为什么含(1−WB)？

   参考答案：扣除相对于无项目基线本会近表面氧化的部分，不对所有已燃烧量作第二次氧化。

## UPDATE_LEDGER

|日期|记录|后续动作|
|---|---|---|
|2026-11-09|首次有界提取；阅读/缺口层级如上|以后追加版本、页条、SHA、解释变化与审查人，不覆盖旧条目|

个人学习进度未读取/修改；正式Enotebook接入PENDING_INTEGRATION。
