# G_IPCC2006｜2006 IPCC Guidelines for National Greenhouse Gas Inventories, Volume5 Chapter3 Solid Waste Disposal

[返回研究索引](../../README.md) · [机器知识包](package.json)

## SOURCE_MASTER

出版者：IPCC / IGES。版本：2006 Vol5 Ch3。层级：INTERNATIONAL_INVENTORY_GUIDELINE。

[官方入口](https://www.ipcc-nggip.iges.or.jp/public/2006gl/pdf/5_Volume5/V5_3_Ch3_SWDS.pdf)；阅读级别：TARGETED_SECTIONS_WITH_LOCAL_BYTES。IPCC版权保留；链接/本地缓存校验、自有释义，不复制整章。

- [G_IPCC2006收据](../../source_receipts/G_IPCC2006.json)：ACQUIRED；SHA-256 `1850dc17af0a2d51efdbc7d1e737b609e50d7ed12d07a913bfb4d68948efcc91`；原件位置 `runtime_data/au_landfill_methods/G_IPCC2006.pdf`。

## SECTION_MAP

- pp3.8–3.10 Eq3.1–3.6
- §3.2.3 parameters
- §3.3 measurement
- §3.7–3.8 uncertainty/QAQC

## KNOWLEDGE_CORE / EQUATION_EXTRACT

FOD把可分解碳库按年度衰减并按F和16/12分到甲烷。它是库存参数化，不是把现场温度逐时输入的反应器；浓度/源率与库存排放必须分开。

- **G-DDOC** — Eq3.2 p3.9：`DDOCm=W DOC DOCf MCF`。变量：Gg C;wet waste W Gg;fractions。域：waste history and method-defined factors。
- **G-FOD** — Eq3.4–3.6 pp3.9–3.10：`A_T=D_T+A_(T−1)exp(−k);Ddec=A_(T−1)(1−exp(−k));G=Ddec F16/12`。变量：annual;GgC to GgCH4;k yr^-1。域：annual indexing/deposition convention explicit。
- **G-E** — Eq3.1 p3.8：`E=(sum G−R)(1−OX)`。变量：GgCH4/year;OX fraction;R recovered。域：inventory boundary; do not double subtract combustion。

## SKILL_PROCEDURE

1. 先声明报告年、废物史、DOC/DOCf/MCF和生成延迟。
2. 核DDOC单位为碳、甲烷单位需F16/12转换。
3. 回收只扣一次，氧化仅作用允许剩余路径。
4. 用独立观测核查参数，保留未测去向；本轮仅做单位与合成账。

## CASE_EVIDENCE

作者12kg分解碳、F=.5→8kgCH4；冻结PR138有年度合成验证，本轮不重跑时间模型。

## METHOD_LIMITATIONS

- 固定参数不是逐时气候响应
- DDOC库存不是孔隙甲烷库存
- 未量测设备滑漏不能据Eq3.1视为0

## CONNECTIONS

E06/E07直接来源；P3只读复用；P2组成/时窗桥接仍阻断。

详见[物料账图](../../LANDFILL_PHYSICS_AND_MASS_BALANCE.md)与[条款crosswalk](../../SECTION_AND_EQUATION_CROSSWALK.md)。

## LEARNING_PATH_ZH

1. 12kg分解碳F=.5得多少CH4？

   参考答案：8kg，甲烷碳6kg；不是12kg湿垃圾。

2. G与E为什么不相等？

   参考答案：回收、氧化及完整物理账的库存/迁移均影响大气排放。

3. k yr^-1能直接用于小时指数吗？

   参考答案：不能；必须统一时间且说明年内模型，不擅改年度索引。

## UPDATE_LEDGER

|日期|记录|后续动作|
|---|---|---|
|2026-11-09|首次有界提取；阅读/缺口层级如上|以后追加版本、页条、SHA、解释变化与审查人，不覆盖旧条目|

个人学习进度未读取/修改；正式Enotebook接入PENDING_INTEGRATION。
