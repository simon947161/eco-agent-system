# B_NGER｜National Greenhouse and Energy Reporting (Measurement) Determination 2008; 2026 amendment and explanatory statement

[返回研究索引](../../README.md) · [机器知识包](package.json)

## SOURCE_MASTER

出版者：Federal Register of Legislation / DCCEEW。版本：F2026C00720 C21 2026-07-01; F2026L00855 2026-06-29。层级：STATUTORY_DETERMINATION_PLUS_EXPLANATORY_STATEMENT。

[官方入口](https://www.legislation.gov.au/F2008L02309/latest/details)；阅读级别：TARGETED_SECTIONS_WITH_LOCAL_BYTES。法规和说明书公开；本包不依赖全文再分发许可，只存来源/哈希/少量数学转录和自有解释。

- [B_NGER收据](../../source_receipts/B_NGER.json)：ACQUIRED；SHA-256 `457fe122a68cca5760b2d9fcb96e526b57126c212531dd45e6bad6fdaf1a49ce`；原件位置 `runtime_data/au_landfill_methods/B_NGER.html`。
- [B_AMENDMENT收据](../../source_receipts/B_AMENDMENT.json)：ACQUIRED；SHA-256 `a8648478bfd2b483697e4c8494f6cc6b86b0c6e143f335e4d3378b91e8d0bbd9`；原件位置 `runtime_data/au_landfill_methods/B_AMENDMENT.html`。
- [B_ES收据](../../source_receipts/B_ES.json)：ACQUIRED；SHA-256 `119c42d85227a09a4c9f014ee24d6f7b418dcf795e29c974bfb328cd6cc815d9`；原件位置 `runtime_data/au_landfill_methods/B_ES.pdf`。

## SECTION_MAP

- s2.32(7) dry standard conditions
- s5.4D annual generation
- s5.15 zone emissions
- s5.17A–D zone/collection
- s5.17F–K scan, flux, weather, frequency
- s5.17L–M averaging and calibration
- amendment items55–87 and98
- ES pp46–51 corresponding amendments

## KNOWLEDGE_CORE / EQUATION_EXTRACT

法定报告公式与现场瞬时通量是不同量。当前方法2将地上设备漏排Qlost单列，不能先对它施加覆盖氧化。现场数据用于代表区生成参数校准，不能自动证明独立预测正确。

- **B-Ejz** — s5.15(1)(b)：`Ejz=[CH4genz−Qlostz−gamma(Qcapz+Qflaredz+Qtrz)](1−OF)+Qlostz`。变量：Ejz/CH4genz/Qlostz:tCO2-e；Qcapz/Qflaredz/Qtrz:m3CH4 standard dry；OF=.1；gamma=6.784e-4×GWPmethane。域：method2 zone, not combustion emissions。
- **B-flux** — s5.17H(2)：`Qflux_i=V(dc/dt)/A`。变量：mgCH4/m2/s;V m3;dc/dt mg/m3/s;A m2。域：calibrated flux chamber plus spatial design。
- **B-k** — s5.17M step4：`kiadj=kidef(1+incr%)`。变量：k:yr^-1;increment<=1%;match to Qz within .001 tCO2-e per source。域：regulatory calibration, no independent validation。

## SKILL_PROCEDURE

1. 核报告年、方法和子分区，保存场图/独立专家报告。
2. 收集至少12月可校准的井流量与组分，确保单位状态一致。
3. 按5.17F–K扫描、通量箱、井漏和天气条件分类；不使用NSW500ppm代替。
4. 按5.17L分别汇总地表与地上设备量，按5.17M校准k；真实执行前另核site-plan附件和未决条款。

## CASE_EVIDENCE

自有通量例：.1m3/.2m2×2mg/m3/s=1mg/m2/s。属于AUTHOR_DERIVED_SYNTHETIC_EXAMPLE，未作现场测量。

## METHOD_LIMITATIONS

- s5.17K至少4次但5.17L分母4，多于4次解释未解决
- 5.17M Step2交叉引用保留原文，未自行修法规
- 特定合规检测技术不代表任意遥感方法合法认可
- 注册/设施阈值与Site-plan附件未形成完整法律适用审计

## CONNECTIONS

E06须区分NGER1.336与IPCC16/12；E07漏排路径；QGIS仅未来场图工具。

详见[物料账图](../../LANDFILL_PHYSICS_AND_MASS_BALANCE.md)与[条款crosswalk](../../SECTION_AND_EQUATION_CROSSWALK.md)。

## LEARNING_PATH_ZH

1. 25ppm与500ppmv为何不能互换？

   参考答案：前者是2026NGER代表区分类，后者NSW2016工程行动线，目的/布点不同。

2. Qlost能用kg/h直接代公式吗？

   参考答案：不能；s5.15要求tCO2-e/报告年，须完整时间和单位转换。

3. 调k吻合当年观测就算预测验证吗？

   参考答案：不是；需要独立留出数据与不确定性检查。

## UPDATE_LEDGER

|日期|记录|后续动作|
|---|---|---|
|2026-11-09|首次有界提取；阅读/缺口层级如上|以后追加版本、页条、SHA、解释变化与审查人，不覆盖旧条目|

个人学习进度未读取/修改；正式Enotebook接入PENDING_INTEGRATION。
