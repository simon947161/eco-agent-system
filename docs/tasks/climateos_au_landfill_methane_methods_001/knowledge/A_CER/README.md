# A_CER｜CER Estimating emissions and energy from solid waste and landfill biogas management guideline

[返回研究索引](../../README.md) · [机器知识包](package.json)

## SOURCE_MASTER

出版者：Clean Energy Regulator。版本：July2026 / reporting2025–26。层级：ADMINISTRATIVE_GUIDANCE。

[官方入口](https://cer.gov.au/document_page/estimating-emissions-and-energy-solid-waste-and-landfill-biogas-management-guideline)；阅读级别：TARGETED_SECTIONS_WITH_LOCAL_BYTES。官网政府指南；本轮未完成逐附件全文再发布权利判定。仅外链/哈希/自有释义，不入库PDF。

- [A_CER_GUIDE收据](../../source_receipts/A_CER_GUIDE.json)：ACQUIRED；SHA-256 `900b1a753b5abb29c49010902be6459b3729f32c9b370327ab127cdd76ae31ca`；原件位置 `runtime_data/au_landfill_methods/A_CER_GUIDE.pdf`。

## SECTION_MAP

- p6 disclaimer
- p7 2025–26 updates
- pp12–13 facility configurations
- pp22–27 waste classifications/diversion
- pp27–30 DDOC/k/collection limits
- pp31–33 biogas combustion and measurement
- pp34–40 legacy waste, combustion and energy

## KNOWLEDGE_CORE / EQUATION_EXTRACT

按设施边界记录废物、集气、燃烧和能源。指南能解释报告流程，但封面发布时间不等于适用报告年。2026–27法律修订与本指南不一致的地方必须回FRL。

- **A-collection-limit** — p30 collection efficiency limit：`(A3×.60+A4×.75+A5×.95)/(A2+A3+A4+A5)`。变量：A2/A3/A4/A5为指南定义各类覆盖面积，同一面积单位；无面积信息旧指南给75%。域：2025–26旧方法2指导；2026修订删除5.15A–C，禁止当前直接复用。

## SKILL_PROCEDURE

1. 先核设施与报告年；不要用封面年份代替报告年。
2. 按p22–27记录进场、分流、实际填埋量和废物组成，避免转运算填埋。
3. 将集气供燃烧、火炬、外送分开，并标明表计位置。
4. 对照B现行条款；本轮不按旧指南计算当前报告。

## CASE_EVIDENCE

官方p27有received/diverted、p31有燃烧示例、p40有发电例；本包只定位不复制官方数字。自有例见crosswalk，不冒充这些原例。

## METHOD_LIMITATIONS

- 不是法律；不作为2026–27方法2最新要求
- 方法1/2的收集限值不能因名称相似混用
- 未进行真实设施边界和审计资格判定

## CONNECTIONS

PR143 E06/E07 → 废物史/回收边界；P1 → 表计状态换算。

详见[物料账图](../../LANDFILL_PHYSICS_AND_MASS_BALANCE.md)与[条款crosswalk](../../SECTION_AND_EQUATION_CROSSWALK.md)。

## LEARNING_PATH_ZH

1. 为什么不能按2026封面认定服务2026–27？

   参考答案：文件内部明确2025–26，版本要同时记录发布时间和报告年。

2. 进场垃圾全等于填埋量吗？

   参考答案：不等；分流、转运等需分开并保存凭证。

3. 旧p30公式可直接替代现行方法2吗？

   参考答案：不可；2026修订已删除相关5.15A–C。

## UPDATE_LEDGER

|日期|记录|后续动作|
|---|---|---|
|2026-11-09|首次有界提取；阅读/缺口层级如上|以后追加版本、页条、SHA、解释变化与审查人，不覆盖旧条目|

个人学习进度未读取/修改；正式Enotebook接入PENDING_INTEGRATION。
