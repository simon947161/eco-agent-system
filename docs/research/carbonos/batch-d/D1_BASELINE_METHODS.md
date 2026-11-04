# D1 — 历史规则与动态基线
2026-11-04 · 公式转录供研究设计，未计算。来源ID见[SOURCES](SOURCES.json)。

## A：保留历史AWT2015
沿用冻结的[P1-A公式登记](../p1a/AWT_FORMULA_REGISTER.csv)，本轮不修改其20条记录。版本为F2015L00060 as-made 2015-01-19；不作当前适用资格结论。官方原文：[历史PDF](https://www.legislation.gov.au/F2015L00060/asmade/2015-01-19/text/original/pdf)。

| 原式/位置 | 表达式与单位 | 审计含义 |
|---|---|---|
| §19 Eq2，PDF页15 | A_Y=(E_B−E_P)/7 [tCO₂e] | 法定分期不是现场年度气体衰减轨迹；例外/资格仍须遵原文 |
| §22 Eq3，页16 | E_B=(1−W_LFG) M_B (1−OF_LF) GWP_CH4 | 基准反事实而非实测场址通量；回收比例与氧化比例不同 |
| §23 Eq4，页17 | M_B=Σ_w(WM_w DOC_w DOC_F,w) MCF W_LFG,CH4 F_C_to_CH4 [tCH₄] | 潜力式；法定F_C_to_CH4=1.336。不能用16/12替换，也没有新增天气乘数 |

外部引用参数须按适用法律版本冻结。参数引用和州别分类不是逐日气候响应。项目排放和特殊条件请追溯原登记，以上不是完整计算指南。

A-factor仅是拟议研究基线：M_A=Σ_i EF_i A_i；EF单位必须与活动A相消得到kgCH₄，且明确毛产生或净大气排放、累计或年度。对于多年遗留库存，不允许把“当年入场量×终生潜力”冒充当年排放。当前无匹配的独立EF，故该分支 DATA_NOT_READY。训练期均值可做附加无技巧基线，但不得称为法定A。

## B：IPCC2006 FOD原式
[IPCC2006 Vol5 Ch3](https://www.ipcc-nggip.iges.or.jp/public/2006gl/pdf/5_Volume5/V5_3_Ch3_SWDS.pdf)，印刷页3.8–3.10，单位原文Gg；以下库存记号保持原文：

| 原式 | 表达式 |
|---|---|
| Eq3.2 | DDOCm = W DOC DOCf MCF |
| Eq3.4 | DDOCma_T = DDOCmd_T + DDOCma_(T−1) exp(−k) |
| Eq3.5 | DDOCm_decomp_T = DDOCma_(T−1) [1−exp(−k)] |
| Eq3.6 | CH4_generated_T = DDOCm_decomp_T F (16/12) |
| Eq3.1 | E_T = [Σ_x CH4_generated_(x,T) − R_T] (1−OX_T) |

W为废物质量，DOC为碳/废物质量分数；DOCf、MCF、F、OX无量纲，k为yr⁻¹，一步一年。该简式假定次年1月1日起衰减；其它延迟见Annex3A.1，不能混用。F为气体CH₄体积分数。参数/初始库存/回收记录的不确定性必须传播。Table3.3含气温及湿润气候分类，传统FOD已经动态，不能构造“传统完全不看气候”的论点。

原式清单回收/燃烧部门归属与整场大气目标不完全相同；设备滑脱等边界桥接见D0/D2，不悄悄改原式。连续或月度FOD若将来使用，必须单列其积分与延迟约定，不能称原年度表直接提供事件峰。

## 2019版本管理
[2019 Ch3](https://www.ipcc-nggip.iges.or.jp/public/2019rf/pdf/5_Volume5/19R_V5_3_Ch03_SWDS.pdf)与[Annex1映射](https://www.ipcc-nggip.iges.or.jp/public/2019rf/pdf/5_Volume5/19R_V5_x_An1_Mapping.pdf)共同使用。方法选择仍保留FOD；新增Table3.0 DOCf分类、更新Table3.1 MCF和Table3.5不确定性；不将2019所有表误称全部新参数。拟议B2006和B2019分别登记，不跨版本拼参数。执行前还需下载合法原件、SHA及参数选用逐行审查；本轮只有浏览核查，原件摘要非文件哈希。

## 既有气候响应对照
CALMIM不是ClimateOS发明。USDA的2011更新草案手册描述覆盖层传输与氧化、土壤温湿和典型年度气候；原论文DOI10.1029/2011JG001741。它适合提醒C必须与既有过程模型比较，但不自动提供任意事件或全场全部排放的验证。CLEEN/Kim2026另见D2。无充分输入时，不为凑三方法排名强行运行。
