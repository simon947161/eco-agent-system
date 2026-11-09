# H_IPCC2019｜2019 Refinement to the 2006 IPCC Guidelines, Volume5 Chapter3 Solid Waste Disposal

[返回研究索引](../../README.md) · [机器知识包](package.json)

## SOURCE_MASTER

出版者：IPCC / IGES。版本：2019 Refinement Vol5 Ch3。层级：INTERNATIONAL_INVENTORY_REFINEMENT。

[官方入口](https://www.ipcc-nggip.iges.or.jp/public/2019rf/pdf/5_Volume5/19R_V5_3_Ch03_SWDS.pdf)；阅读级别：TARGETED_SECTIONS_WITH_LOCAL_BYTES。IPCC版权；不重发布PDF或表格全文。

- [H_IPCC2019收据](../../source_receipts/H_IPCC2019.json)：ACQUIRED；SHA-256 `bb779852f7206c102cd37a4eced1de9e2e1aaec1b770f3c8abb35b214dcca49f`；原件位置 `runtime_data/au_landfill_methods/H_IPCC2019.pdf`。

## SECTION_MAP

- p3.5 mapping/no refinement
- pp3.6–3.9 FOD restatement and aeration context
- Table3.0 p3.12 DOCf
- Table3.1 p3.13 MCF
- Tables3.3/3.4 pp3.16–17 k/half-life
- Table3.5 p3.20 uncertainty
- Appendices3A.1/2 pp3.23–24 future scope

## KNOWLEDGE_CORE / EQUATION_EXTRACT

2019为2006的配套修订，有机碳可分解比例、管理类型/MCF及不确定性表需留版本，未修订处仍读2006。通气/渗滤液影响说明不能变成未经校准的统一减排因子。

- **H-refinement** — Eq3.1–3.6 and Table3.0/3.1/3.5：`core FOD structure retained; parameter and management mapping refined`。变量：per-source waste/management categories, not mixed generic defaults。域：consult mapping tables; no parameter substitution in frozen PR143。

## SKILL_PROCEDURE

1. 先定位2006对应章节与2019映射。
2. 登记表号、废物与管理类型，再决定是否可用替代参数。
3. 保持旧计算的参数版本可复现，不静默更新。
4. 新适用域需观测与独立校验，未授权不做数值研究。

## CASE_EVIDENCE

只做版本对照，无真实场址计算；N2O/active aeration附录只作未来索引。

## METHOD_LIMITATIONS

- 默认不确定性范围不是场址统计CI
- 没有为本任务取值或运行新模型
- 不能以2019出版较新就认定澳洲法规自动采用所有表

## CONNECTIONS

P3版本比较；P4气候参数仍待标定；N2O仅FUTURE_SCOPE。

详见[物料账图](../../LANDFILL_PHYSICS_AND_MASS_BALANCE.md)与[条款crosswalk](../../SECTION_AND_EQUATION_CROSSWALK.md)。

## LEARNING_PATH_ZH

1. 2019是否整套替换2006？

   参考答案：不是；按映射表和No refinement标记配套阅读。

2. 为什么保存DOCf表版本？

   参考答案：相同垃圾输入配不同参数会改变结果，需可追溯且适用。

3. 默认不确定性就是本场址置信区间吗？

   参考答案：不是；需场址观测、误差和统计设计。

## UPDATE_LEDGER

|日期|记录|后续动作|
|---|---|---|
|2026-11-09|首次有界提取；阅读/缺口层级如上|以后追加版本、页条、SHA、解释变化与审查人，不覆盖旧条目|

个人学习进度未读取/修改；正式Enotebook接入PENDING_INTEGRATION。
