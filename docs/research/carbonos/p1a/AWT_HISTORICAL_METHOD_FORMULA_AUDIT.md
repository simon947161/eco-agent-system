# AWT2015 历史方法公式与证据审计

`CLIMATEOS-CARBON-P1A-001` · 2026-11-04 · 历史文本研究，非当前项目合资格/法律意见或碳核算服务。**20个主计算公式已对原始PDF渲染逐项交叉核对；独立专业复核仍PENDING。** 没有运行排放计算、改动原方法或填入真实项目输入。

## 版本、适用性与勘误

主来源 [F2015L00060 as-made](https://www.legislation.gov.au/F2015L00060/asmade/2015-01-19/text/original/pdf)，39页，2015-01-19至2025-03-31；11月4日 [Register](https://www.legislation.gov.au/Series/F2015L00060)仍显示No longer in force。原始字节复用P0并复核SHA；路径及检索时间在 [source receipts](evidence/source_receipts.json)。旧项目延续权利必须另核其登记/crediting period，不能据到期方法开展新项目注册。

§5及§9–13规定mixed solid waste、技术与项目类别。源头分选有机物、biosolids等排除项不能因“可产甲烷”被纳入；污水塘/自然湿地不是该方法自动适用的设施。市政固废、粪肥、污水与digestate保持独立边界。§15的气体/源清单及Part4决定核算边界，不能以扩展环境研究替代。

**对P0的明确勘误：Eq1位于§17，而非P0摘要中的§18。** 这份新报告纠正引用，不修改冻结P0。还须保留§23的法定 `F_C→CH4=1.336`，不能“精确化”为16/12。§35的 `CE=0.98` 为消化器沼气collection效率，不是燃烧destruction效率。这些均从PDF正文/公式视觉核对，不能靠常识替换。

## 20个公式的逐条登记

完整表达式、条款、PDF页码、输出单位、条件和气候角色见 [AWT_FORMULA_REGISTER.csv](AWT_FORMULA_REGISTER.csv)。ASCII变量是排版转写，不是可执行代码。原文对E_Compost按气体j描述，本登记不自行省略CH4或N2O。

| 公式 | § / PDF页（1起） | 作用与关键条件 |
|---|---|---|
| 1 | 17 /14 | `A_N=A_0+A_Acc`，含到期且未重复使用的历史部分额；transitioning legacy独立 |
| 2 | 19 /15 | `(E_B-E_P)/7`形成A0–A6；PW为零/非crediting period等按§19(2)归零；§20例外保留 |
| 3 | 22 /16 | baseline `(1-W_LFG) M_B (1-OF_LF) GWP_CH4`；不能把潜力全部当净排放 |
| 4 | 23 /17 | 组分质量×DOC×DOCf，再乘MCF、气体CH4份额及1.336；无年度FOD k |
| 5–8 | 24–27 /18–20 | eligible组成、PW、EW、历史24个月HW；PW负值按§25(2)取零，不能泛化为所有量的默认填零 |
| 9 | 29 /21 | `E_P=(PW/EW)(E_F+E_EP)+E_PW`；不能漏分配比例或自行除零 |
| 10–11 | 30–31 /22 | 燃料量/能量×排放因子；购电kWh×kgCO2e/kWh÷1000；气体种类和版本须匹配 |
| 12–13 | 32–33 /23–24 | `E_PW=(PW/TPW)(E_Compost+E_AD+E_Com)`；TPW与eligible EW不同 |
| 14–15 | 34 /25 | composting系数法/直接测量法；CH4/N2O同一submethod；生物过滤RE=10%或0，不是现场保证 |
| 16 | 35 /26 | `gamma[(1/CE−1)ΣM_Sent+ΣM_Vent]`；收集损失与major venting分开 |
| 17–18 | 36 /27 | 气量×CH4份额，或仅对内燃机以MWh、3.6GJ/MWh、EE及EC反推CH4量；不能把发电量当气量 |
| 19 | 37 /28 | `(MS_BCS+FR_q t_q) W_BG,CH4`；storage m³、FR m³/day、t whole days及major-event定义 |
| 20 | 38 /29 | CH4送燃烧量×气体能值×CH4/N2O残余排放因子÷1000；不是简单“捕集即全部销毁” |

Part4 Division4 §39–41是transitioning legacy额处理，已检查其存在及边界，但未把旧CFI项目重算逻辑转成通用执行器。项目特定旧determination、历史已计额/未计额不在本研究输入中。20式登记不表示覆盖一切项目资格/报告规则。

## 变量、单位与版本纪律

- WM、PW、EW、HW、TPW与各Q质量：t，保持来源湿/干基；不能用污水m³替换。DOC来源及量纲按对应NGER版本；DOCf、MCF、gas fraction为无量纲，percent必须正确转换。
- W_LFG：§22州/领地及transitioning/other类别的规范表值，例如NSW24%/37%、QLD16%/30%。这是历史法定取值，**不是**由该地区当日气候反演的实测捕集率。
- gamma：NGER§5.4(1)所指标准状态m³CH4→tCO2e转换；实际温压、干湿气基准属于计量一致性，不是可额外添加的气候效益系数。
- Q_EP为kWh；Q_EG为MWh；EC_BG为GJ/m³；EF燃料/残余气为kgCO2e/GJ。GWP/因子所用报告期法律版本必须记录，不能从论文中的旧GWP数字取得当前信用因子。
- §8一般规则引用**reporting period结束时**有效的外部文本，另有例外；§31购电EF有特定relevant day并排除§8。以“全部用2015版”或“全部用2026最新值”都不正确。完整外部NGER逐报告期编纂对照仍需另审。

## 气候已包含在哪里、没有包含在哪里

检查范围为这份AWT2015原文20式及其参数定义：没有直接的air/water temperature、season、rainfall、latitude、altitude、Arrhenius Ea或Q10输入，也没有通用温度修正函数。州/领地W_LFG和购电grid因子具有地理差异，但不等于设施生物反应气候模型。直接监测气量/排放会反映实际条件，但不意味着可改写法定公式。

外部NGER的参数引用必须按有效期单独核对，本结论不声称“所有澳洲法律都没有气候因素”。IPCC清单FOD的climate-dependent k与2019污水温度讨论属于另一来源/方法体系；不自动进入AWT式4。**研究中的温度/水分响应只在独立scientific lane，不能乘入历史信用公式。**

## 监测、缺失与审计

§43要求报告适用的外部版本/使用时段/例外原因，以及缺测参数、期间、原因和替代确定方法。§45包括称重、fuel/electricity、biogas、CH4份额、venting等及设备校准要求；连续浓度与气量必须配对，不能用不同时段均值相乘。§46提供参数特定缺测规则，不授权统一填零/插值；例如部分参数涉及3个月阈值及1.1/1.5保守处理，适用条件必须整条读取，不能到处套用。

独立核证由适用项目制度及当前audit schedule决定，不由本地测试或源文件hash取代。[CER reporting and audits](https://cer.gov.au/schemes/australian-carbon-credit-unit-scheme/how-to-participate-accu-scheme/project-reporting-and-audits)。本轮无项目申请、审计委任或费用。

## 2026咨询与历史方法的差异

[ARRC October2026 paper](https://ausrrc.com.au/download/609/?tmstv=1793152433)，26页，§4.2–4.15：讨论extended accounting period、技术资格/composting、SSOW活动、捕集率与因子、crediting period、biomethane、digestate及transition/deferral等。它是proponent第一轮咨询，不是现行方法或ERAC已发布determination。具体提案尚可变化；不把期限或捕集率方案硬编码为新法律。[官方入口](https://ausrrc.com.au/awt-remake/)与保留P0文件可交叉核对。

区别矩阵：2015固定规则/已有crediting安排 → 2026提出修改的议题 → 最终法律状态UNKNOWN。咨询截止沿用官方11月29日23:59AEST；若准备任何后续外部动作必须再次核对，本轮不提交意见。缺少气候修正项不构成研究者自行补入的授权。

## 审计成熟度

原文、视觉公式、单位/版本及条件做了本地单研究者交叉核对；PDF抽取曾遗漏旋转公式，因此以渲染页复核，不能把纯文本抽取当完整公式。独立专业转写审核、外部法律编纂全量对照与真实项目输入仍PENDING。该状态不改变ClimateOS科学准入。
