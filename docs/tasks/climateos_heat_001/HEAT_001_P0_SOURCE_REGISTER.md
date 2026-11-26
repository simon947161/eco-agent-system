# HEAT–001｜来源、版本与证据登记

2026-11-26（悉尼） · [任务书 #173](https://github.com/simon947161/eco-agent-system/issues/173) · [Founder 评审](HEAT_001_P0_FOUNDER_REVIEW_CN.md)

## 原件和版本

|记录|核查深度|能确认的内容|尚缺的证据|
|---|---|---|---|
|Fraley v1，2026-04-17；ESS Open Archive；未同行评议；CC BY 4.0|Founder 提供的 10 页 PDF，逐页读取，目视核对表 1。按 PDF 物理页计数，含平台封面。原件 SHA-256 `1b57a0ae2c0a07c44fd56576d6f491f76fe33056c11b7b6d69f3d5227558c65c`|p.1 状态和摘要；pp.2–4 论点与分母；p.5 表 1；pp.6–8 归因、增长与政策；pp.9–10 数据说明与十条参考文献|作者的 IEA 提取表、流量口径映射、逐项不确定度、独立归因分析。[v1 DOI](https://doi.org/10.22541/essoar.15002155/v1)|
|Fraley v2，2026-07-30；同题|平台版本历史及两笔 Crossref 登记；两个登记摘要逐字一致，均为 posted-content|可核实的最新版本仍在摘要中使用约 18 TW、46 TW、39% 和 1.5–2%/年。作者 ORCID 检索出现两条该题预印本记录；另两篇微波题录是其他作品|全文入口返回 HTTP 403，未取得 v2 PDF。无页级差异、表 1 或文末校订的证据。登记未显示已同行评议的期刊对应版本。审计不把 v1 页码外推给 v2。[v2 DOI](https://doi.org/10.22541/essoar.15002155/v2) · [v1 登记](https://api.crossref.org/works/10.22541/essoar.15002155/v1) · [v2 登记](https://api.crossref.org/works/10.22541/essoar.15002155/v2) · [作者登记查询](https://api.crossref.org/works?filter=orcid%3A0009-0000-1780-8864)|

v1 p.9 仅将表 1 追溯到 IEA (2023) 并说明未生成新观测。p.10 留有投稿前核查文献的编者提示。正文未提供部门原始记录、数据版本、逐项分配算法或平滑气温序列的来源与处理方法。不得将这份原件或工作站文件路径随本包归档。取得合法 v2 原件后，应记录字节 SHA、页数、修订日期，逐页对照 §2、表 1、§4、数据声明和十条引文，登记增删及其是否改变以下判断。

## v1 文末十项逐条核对

核查深度按项给出。DOI 能定位文献，不等于文献支持引用它的推论。十项中九项可核对 DOI 登记，一项 IEA 条目的原始版本及表格未核实。

|p.9–10 引文|实际可支持的命题|限度与核对位置|
|---|---|---|
|1 · Dong / Varquez / Kanda 2017|公开原研究以自上而下方法分配国家能耗到约 30 角秒、小时格点，支持排热的空间和时间异质性|pp.276–294，摘要、方法。代理分配无法独立校核 Fraley 2022 年六行，更不构成大气储热测量。[原文](https://doi.org/10.1016/j.atmosenv.2016.11.040)|
|2 · Flanner 2009|非可再生能释放的热在研究时标内构成直接输入。2005 年全球均值约 0.028 W/m²，欧洲西部约 0.68 W/m²|p.1 摘要及 §§1–2；pp.3–5 模式结果。现期和 2040 情景未检出显著的洲尺度年均增温，另有局部信号；2100 为特定情景。该研究已经讨论气候尺度。[作者 PDF](https://flanner.engin.umich.edu/wp-content/uploads/sites/544/2021/09/Flannr09.pdf)|
|3 · IEA，Key World Energy Statistics 2023|v1 p.5 报告 2022 年 580 EJ；p.9 给出题名和网页|原引地址读取返回 403，书目缺表号、流代码与提取版次。官方 WEO 2023 表 A.6 给出同年全球总能源供应 632.0 EJ，仅作不同出版物的交叉检查。免费查阅与获准重分发须分开核实。[原引入口](https://www.iea.org/reports/key-world-energy-statistics-2023) · [WEO 原表](https://iea.blob.core.windows.net/assets/42b23c45-78bc-4482-b0f9-eb826ae2da3d/WorldEnergyOutlook2023.pdf) · [数据产品条款入口](https://www.iea.org/data-and-statistics/data-product/world-energy-statistics-balances)|
|4 · IPCC AR6 WGI 2021|第 7 章执行摘要与 §7.3 定义有效辐射强迫（ERF）。1750–2019 总人为 ERF 为 2.72 [1.96, 3.48] W/m²，充分混合温室气体项为 3.32 [3.03, 3.61] W/m²|v1 p.1 的“2023 温室气体约 2.7”缺相应年度与类别的引文。此评估无法支持把 ERF 当作观测储热率。[第 7 章](https://www.ipcc.ch/report/ar6/wg1/chapter/chapter-7/)|
|5 · Jin et al. 2019|研究按国家能耗和空间代理建格网，含历史和情景年份|摘要、Methods 与表 1。首作者为 Kai Jin，文末写作 Jin, L.；网格估值不能验证 2022 年现场排热或 39%。[数据论文](https://doi.org/10.1038/s41597-019-0143-1)|
|6 · Khanh et al. 2025|量纲分析和数值试验说明混合层高度、风速及城市面积会调节近地温度响应|作者单位摘要；首作者 Do Ngoc Khanh，v1 写作 N. Q.；只能约束局地因子，正文未用它验证全球份额。[作者单位记录](https://shibaura.elsevierpure.com/en/publications/impact-of-anthropogenic-heat-on-air-temperature-a-first-order-est/)|
|7 · Li et al. 2024|城市冠层参数化不同，模拟冠层空气温度对排热的敏感度可相差一个数量级；2 m 温度敏感度另议|摘要及结果。正式反对把单一排热量换算成通用街区温升。文末列出，未见 v1 正文将结果纳入不确定度。[作者论文](https://doi.org/10.1029/2024MS004431)|
|8 · Trenberth / Fasullo / Kiehl 2009|p.311 摘要、全球预算图；2000-03 至 2004-05 的 CERES 大气顶通量经调整，对应约 0.9 W/m² 的净不平衡|支持区分通量与残差；文中预算无法推出非海洋部分全部进大气。v1 引至 p.323，Crossref 登记末页 324。[作者 PDF](https://staff.cgd.ucar.edu/trenbert/trenberth.papers/10.1175_2008BAMS2634.1.pdf)|
|9 · Varquez et al. 2021|约 1 km、逐时排热清单，包含现状和未来情景|摘要、Methods、Technical Validation。可以提出时空先验；特定地方、日期及排热高度需要独立验证。没有同时控制城市 CO₂、形态和天气的交互归因。[数据论文](https://doi.org/10.1038/s41597-021-00850-w)|
|10 · von Schuckmann et al. 2023|p.1675 摘要、§6 与图 8–9；1971–2020 全球热增量 381±61 ZJ，海洋约 89%、陆地 6%、冰冻圈 4%、大气 1%|直接反证 v1 p.4 对剩余热量的分配。各项是给定时段的储热变化，无法识别某个热源的贡献。[原文](https://doi.org/10.5194/essd-15-1675-2023)|

## 超出原引文的独立对照

|证据|可检验什么|适用范围|
|---|---|---|
|Forster 等 2026，§6、表 4、图 7|更新到 2006–2025 的全球总储热率估计为 1.04 [0.82, 1.25] W/m²。热含量法与卫星约束各有不确定度|检查分母的时期、面积和物理量；该结果不能提供 AHR 专属分母。[原文](https://doi.org/10.5194/essd-18-3889-2026)|
|高性能计算设备热回收实测，2021|流量、供回水温和压缩机电耗可分别计量，实际热泵能将低温余热送入热网|证明设备级检验可行；需要当地反事实与生命周期账才能推断净减排。[原文](https://doi.org/10.1016/j.egyr.2021.09.038)|
|Salamanca 等 2014，Phoenix|十日极端热期，耦合城市与建筑的模拟显示部分地点夜间空调排热可抬升 2 m 气温约 1°C|属于特定天气和情景的模拟，支持 H2 的研究动机；不借用该效应量做澳洲预测。[原文](https://doi.org/10.1002/2013JD021225)|
|Raptis 等 2016|温排水的全球河网研究表明热扰动受流量、季节和受纳水体控制|用于预注册下游风险；需要当地水温、溶氧、生物敏感期及合法限制。[作者 PDF](https://pure.iiasa.ac.at/13989/1/erl_11_10_104011.pdf)|

[逐项能量复算](HEAT_001_P0_DIMENSIONAL_AUDIT.md) · [能力与许可清单](HEAT_001_P0_SIMULATION_GATE.md)
