# D_NSW｜Environmental Guidelines: Solid Waste Landfills

[返回研究索引](../../README.md) · [机器知识包](package.json)

## SOURCE_MASTER

出版者：NSW Environment Protection Authority。版本：2nd edition April2016 EPA2016/0259。层级：ENVIRONMENTAL_ENGINEERING_GUIDELINE。

[官方入口](https://www.epa.nsw.gov.au/sites/default/files/solid-waste-landfill-guidelines-160259.pdf)；阅读级别：TARGETED_WEB_TEXT_ONLY_RAW_DOWNLOAD_BLOCKED。封面版权说明允许有条件教育/非商业使用并有图片例外；本轮仍不复制PDF或图。

- [D_NSW收据](../../source_receipts/D_NSW.json)：BLOCKED；SHA-256 `UNKNOWN`；原件位置 `NOT_ACQUIRED`。

## SECTION_MAP

- PartA pp1–2 regulatory context
- s5.2 p33 surface gas monitoring
- s5.3 pp34–35 subsurface gas
- s5.5–5.6 combustion/biocovers navigation only

## KNOWLEDGE_CORE / EQUATION_EXTRACT

地表扫描用于发现热点并采取纠正行动，具体许可条件可能不同。浓度扫描不提供面积/风场或通量，不能直接变kg/h。

- **D-screen** — s5.2 p33/PDF37：`500ppmv investigation/action level;25m grid;5cm height`。变量：concentration, distance; not mass-flow variables。域：specified intermediate/final cover monitoring, weather and EPA variation apply。

## SKILL_PROCEDURE

1. 先查看设施实际EPL和覆盖区边界。
2. 登记网格、探头高度、裂缝凹陷和天气。
3. 校准/归零仪表，保留原始读数和纠正行动。
4. 若要排放率另设计通量测量；禁止用500ppm直接乘面积。

## CASE_EVIDENCE

反例：两块地表同500ppm，若空气输送/测量高度不同，源率可能不同；本轮不计算真实场址。

## METHOD_LIMITATIONS

- 直接下载403；SHA UNKNOWN，之前web解析可读s5.2/5.3，未取可重算字节
- 指南不等于具体EPL条件
- 本轮未完整复核每章/全部后续法定变更

## CONNECTIONS

E07覆盖路径；未来QGIS扫描足迹；气象条件是采样限制而非产气乘子。

详见[物料账图](../../LANDFILL_PHYSICS_AND_MASS_BALANCE.md)与[条款crosswalk](../../SECTION_AND_EQUATION_CROSSWALK.md)。

## LEARNING_PATH_ZH

1. 500ppm代表多少kg/h？

   参考答案：信息不足。需流场/通量与空间时间边界。

2. 25m网格可替代NGER4m格吗？

   参考答案：不可以，适用任务不同。

3. 指南是否等于每个EPL？

   参考答案：不等；必须单独查具体许可证。

## UPDATE_LEDGER

|日期|记录|后续动作|
|---|---|---|
|2026-11-09|首次有界提取；阅读/缺口层级如上|以后追加版本、页条、SHA、解释变化与审查人，不覆盖旧条目|

个人学习进度未读取/修改；正式Enotebook接入PENDING_INTEGRATION。
