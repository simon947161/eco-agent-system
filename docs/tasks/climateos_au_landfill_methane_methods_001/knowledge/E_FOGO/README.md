# E_FOGO｜Emissions impacts of food waste recovery technologies: composting and landfill fact sheets

[返回研究索引](../../README.md) · [机器知识包](package.json)

## SOURCE_MASTER

出版者：NSW EPA。版本：March2024 P4523 and P4522; landing updated2024-09-06。层级：SCENARIO_MODELLING_FACT_SHEETS。

[官方入口](https://www.epa.nsw.gov.au/Your-environment/Recycling-and-reuse/business-government-recycling/Food-organics-and-garden-organics/Emissions-impacts-of-food-waste-recovery-technologies)；阅读级别：P4523_TARGETED_WEB_TEXT_P4522_LIMITED_RAW_BLOCKED。网页公开不等于全部数据自由再发布；只保留外链和自有笔记。

- [E_COMPOST收据](../../source_receipts/E_COMPOST.json)：BLOCKED；SHA-256 `UNKNOWN`；原件位置 `NOT_ACQUIRED`。
- [E_LANDFILL收据](../../source_receipts/E_LANDFILL.json)：BLOCKED；SHA-256 `UNKNOWN`；原件位置 `NOT_ACQUIRED`。

## SECTION_MAP

- P4523 pp1–3 introduction/Fig1/Fig2
- P4522 landfill comparison metadata; no new numeric extraction

## KNOWLEDGE_CORE / EQUATION_EXTRACT

96%来自特定食物废物净温室气体情景比较；包括收运/处理和堆肥应用碳抵扣，不能当甲烷捕集或毁灭效率。图2对比200km堆肥与平均/高回收填埋和不同收运。

- **E-scenario** — P4523 p3 Fig2 caption：`relative reduction =1−scenario_net_GHG/baseline_net_GHG (author interpretation of 25-fold statement)`。变量：common functional unit:kgCO2-e/t food recovered;not kgCH4。域：scenario boundary only; not universal .96 emission factor。

## SKILL_PROCEDURE

1. 先核功能单位、食物废物与运输路线。
2. 分别列过程排放、能源和应用抵扣，不借用为物理CH4通量。
3. 查原Blue Environment2023模型的假设/不确定性（本轮尚未取得）。
4. 作为未来有机物模块的研究线索，不在填埋账填96%。

## CASE_EVIDENCE

Fact sheet Fig2为模型案例，非现场试验；不计算本项目真实减排。

## METHOD_LIMITATIONS

- 原PDF直接403，只有web文本；原始模型/数据未取得
- P4522只登记和定位，不声称完整精读
- 不同废物/工艺/气候不能外推96%

## CONNECTIONS

未来堆肥/FOGO与碳边界；不接E07 DRE。

详见[物料账图](../../LANDFILL_PHYSICS_AND_MASS_BALANCE.md)与[条款crosswalk](../../SECTION_AND_EQUATION_CROSSWALK.md)。

## LEARNING_PATH_ZH

1. 96%能否填DRE字段？

   参考答案：不能；相对情景净GHG与装置CH4毁灭率不是同一量。

2. 为什么运输距离重要？

   参考答案：它在模型边界内贡献排放并影响情景可比性。

3. 现场管理不好会怎样？

   参考答案：可能产生CH4/N2O；该事实表的情景结论不能替代现场观测。

## UPDATE_LEDGER

|日期|记录|后续动作|
|---|---|---|
|2026-11-09|首次有界提取；阅读/缺口层级如上|以后追加版本、页条、SHA、解释变化与审查人，不覆盖旧条目|

个人学习进度未读取/修改；正式Enotebook接入PENDING_INTEGRATION。
