# 法规／方法版本与保守筛查 · 核查2026-11-23

这是可审阅研究筛查，不是法律意见或合规决定。来源读到哪一层、许可及空原件哈希见 [sources.json](sources.json)。本轮没有取得或再发布外部数据原件，网页可读不等于开放数据准入。

|来源／版本|法效与适用边界|实现和缺口|
|---|---|---|
|[AWT2015 F2015L00060](https://www.legislation.gov.au/F2015L00060/asmade/downloads)，2015-01-19–2025-03-31|已到期。§5/9/11–13废物流及项目类别；§17–38核算；§45–46监测。混合固废和源头分选有机物不能混为一类|本轮只用已核实到期规则判断“到期后新注册该方法路径NOT_ELIGIBLE”。不据此否定所有旧项目；逐项目注册/crediting/外部参数链未知。|
|[DCCEEW方法页](https://www.dcceew.gov.au/climate-change/emissions-reduction/accu-scheme/methods-closed/alternative-waste-treatment)及[tracker](https://www.dcceew.gov.au/climate-change/emissions-reduction/accu-scheme/methods/current)|官方说明旧项目可能继续至crediting period末，新AWT仍Under development；SSOW2016于2026-03-31到期|不能把“在开发”标记为现行可用方法；不证明任何具体设施合格。|
|[ARRC](https://ausrrc.com.au/awt-remake/) October2026咨询及26页论文|提案者咨询，截止2026-11-29 23:59 AEST；不是部长批准文书|针对性读取捕集率、残渣、Safeguard讨论。未宣称审完56题、未投稿或联系机构。提案立场不能编码成权利。|
|[NSW EPA FOGO说明](https://www.epa.nsw.gov.au/Your-environment/Recycling-and-reuse/business-government-recycling/Food-organics-and-garden-organics/fogo-mandates-and-rollout)|家庭有council残余垃圾服务的收集义务起点2030-07-01，商业按阶段；对象和[豁免](https://www.epa.nsw.gov.au/Your-environment/Recycling-and-reuse/business-government-recycling/Food-organics-and-garden/FOGO-mandates-and-rollout/exemptions)需查|代码仅实现家庭日期/范围/豁免的保守筛查。商业容积组合、其他法域、实际豁免和具体处理路径不硬编码。2030是按2026资料作条件演练，届时必须重新核法。|
|NSW POEO Act Part5.8A／相关过渡条款|原法是权威来源|现行HTML403后停止，全文NOT_VERIFIED。EPA可读指导不替代逐条法规和现场许可。不得从“分收义务”直接推出“必须AD”或“项目不具额外性”。|
|[NGER C21 F2026C00720](https://www.legislation.gov.au/F2008L02309/latest/details)，2026-07-01|登记显示In force；报告义务和设施适用另判|继承PR144对2026修订和s5.17L/M解释缺口；不实现法定求解器。CER July2026指南只适用2025–26，不能因封面年份混用。|
|ACCU landfill gas2025 / Safeguard|不同监管机制，不能由同一质量数推断同一权利|这里只检测batch+period+quantity-boundary候选重合。登记、项目权属、baseline调整和是否已签发均未知；不判欺诈或自动双重扣除。|
|IPCC2006、AR6研究指标|科学库存／物理参照，不自行赋予AU法效|16/12物理计量与AWT1.336法定常数分别保留；27.2/273固定研究GWP，未替换法定因子。|

## C情景逐项解释

- **可读事实**：EPA列家庭2030起点、商业分期及豁免；并说明未限制其他循环使用方式。
- **合成假设**：家庭批次有红桶服务，测试日期2030-07-01，并假设无豁免。并非现实Council记录。
- **筛查解释**：collection=CONDITIONALLY_IN_SCOPE，具体AD路径未建立；未来法效需复核。
- **未知**：没有项目时的合法、实际处理路径，剩余处理排放、技术选择、额外性和权利。
- **决策**：可展示相同物理算术，但反事实/法定准入INSUFFICIENT_EVIDENCE，credit NOT_DETERMINED。

本包不接受由输入文本或LLM宣布“通过”。真实科学与监管结论必须另经有权限的人类评审。
