# 自然环境甲烷文献研究

2026-11-04 · 结构化范围检索（scoping review），不是穷尽性系统综述或meta-analysis。研究对象、来源深度、时空尺度、参数及缺口分别登记；没有运行文献模型或将其用于真实设施。

## 检索与纳入规则

在本次日期检索原始同行评审研究、IPCC、澳洲政府/CSIRO及大学原始研究。查询组包括 temperature/methanogenesis、lagoon seasonal stratification、landfill moisture/rainfall/generation、cover oxidation、Q10/Arrhenius、wetland microbial warming及Australian site data。完整操作范围与失败在 [检索日志](SEARCH_PROTOCOL_AND_SOURCE_INDEX.md)，机器表见 [LITERATURE_EVIDENCE_REGISTER.csv](LITERATURE_EVIDENCE_REGISTER.csv)。

优先纳入有明确方法、对象/尺度、观测或实验条件的primary research。全文可访问与仅摘要分层；评论/新闻/二手转述仅作发现线索。已发表论文优先于同一研究preprint，不重复计数。没有使用商业数据库完整索引、预注册检索或独立双人筛选，不能据此声称覆盖全部研究。原始个体数据、补充材料和全文未取得的字段保留UNKNOWN，不从作者单位推断实验地点。

## 综合判断：观察、解释与限制

**观察。** CSIRO/MLA的单塘全年监测同时看到水温、季节、降雨带入底物与排放变化；Bai2026将水样、溶解CH4及运行与通量一起测量；Lam2026分开操纵温度和WFPS；Kim2026结合季节观测和本地模型校准。这些方法测到或估算的对象不同，不能直接合并成一个温度效应量。

**解释。** 产甲烷过程受底物与群落状态制约；净排放还经过氧化、存储、溶解/逸出、迁移和捕集。air temperature既不是反应层实际温度，也不足以代表这些过程。季节变化和雨后通量变化可同时包含来料、曝气、气压、扩散与采样footprint效应。

**模型证据。** IPCC2006 Ch3采用FOD和按气候/废物类别的k选择；2019 refinement更新DOCf等，不能静默替换AWT法定引用。IPCC2019 Ch6§6.2.2.1的分散系统温度讨论也明确温度依赖因子证据不足；其中针对septic等系统的温度描述不能用作所有污水塘统一停产阈值。[IPCC2006 Ch3](https://www.ipcc-nggip.iges.or.jp/public/2006gl/pdf/5_Volume5/V5_3_Ch3_SWDS.pdf)、[2019 Ch6](https://www.ipcc-nggip.iges.or.jp/public/2019rf/pdf/5_Volume5/19R_V5_6_Ch06_Wastewater.pdf)。

**尚未证明。** 本轮没有气候变化→Cooma/Rockhampton局部甲烷变化的因果证据；没有共同基线、同工艺、同底物、同捕集条件的区域配对观测。温度/Q10/氧化最佳值只能作为文献范围或待校准参数，不是区域设施默认值。潜在未来影响应先作为预登记假设，区分气候趋势、天气事件、操作变化和测量偏差。

## 逐文献提取

以下字段对应当前取得的原文/摘要，不将全文未读的研究列为FULL_REVIEW。FULL_RELEVANT_SECTIONS_REVIEWED指已读相关正文段落，不声称每份补充材料或原始数据均已复核。

### L_YVON2014 · 跨微生物至生态系统温度依赖

- 文献：Yvon-Durocher et al.，2014；10.1038/nature13164。[原始来源](https://carbbas.uqam.ca/upload/files/PDF/yvon-durocheretal2014.pdf)
- 对象/地点/气候：跨微生物至生态系统温度依赖；多站点/多类生态系统；非单一设施。
- 周期与方法：季节与培养研究汇总；各原始研究窗口不一；温度与CH4过程meta-analysis。
- 变量与公式/参数：T、CH4生成/通量、尺度；Arrhenius型温度关系；平均Ea约0.96eV为文献汇总值。
- 已验证应用范围：湿地/水体/稻田与培养系统；不是本项目科学准入。
- 不确定性/外推限制：不直接用于废物设施；站点差异/底物/氧化与长期适应限制外推。
- 本轮阅读深度：`WEB_PRIMARY_TEXT_PARTIAL; LOCAL404`。

### L_MLA2013 · Darling Downs饲养场沉淀塘

- 文献：Allingham et al.; CSIRO/Feedlot Services Australia，2013；B.FLT.0362。[原始来源](https://www.mla.com.au/globalassets/mla-corporate/research-and-development/final-reports/2019/b.flt.0362-final-report.pdf)
- 对象/地点/气候：Darling Downs饲养场沉淀塘；澳大利亚QLD；暖湿夏季/凉干冬季。
- 周期与方法：2012-04-27至2013-04-26；650cycles/161日均记录；浮箱、气体传感、水柱温度、气象；RF/GAM。
- 变量与公式/参数：水柱T、7日雨、来料、排放、面积；季节GAM；无跨场地可直接采用的单一温度系数。
- 已验证应用范围：单塘田野；非municipal污水/AWT适用性证明；不是本项目科学准入。
- 不确定性/外推限制：降雨同时带入粪料；历史VS/排放面积不确定，非单独温度因果。
- 本轮阅读深度：`FULL_RELEVANT_SECTIONS_REVIEWED`。

### L_BAI2026 · Victoria城市污水曝气lagoon

- 文献：Bai, de Jong, Tao, Chen，2026；10.5194/amt-19-5157-2026。[原始来源](https://amt.copernicus.org/articles/19/5157/2026/)
- 对象/地点/气候：Victoria城市污水曝气lagoon；澳大利亚Victoria；实际水温/运行与气象分开。
- 周期与方法：2024-02-08至03-12；08-15至10-05；三OPL+backward Lagrangian inverse dispersion；水样。
- 变量与公式/参数：溶解CH4、流量、曝气、COD/BOD、T/DO/Eh；IDM Eq1；不是独立产甲烷反应动力学。
- 已验证应用范围：单一厂内、covered anaerobic pot下游pond；不是本项目科学准入。
- 不确定性/外推限制：两campaign非全年监测；风向过滤/空间异质性；年度化是作者估计。
- 本轮阅读深度：`FULL_RELEVANT_SECTIONS_REVIEWED`。

### L_KIM2026 · Sudokwon两关闭填埋区

- 文献：Kim et al.，2026；10.5194/acp-26-7789-2026。[原始来源](https://acp.copernicus.org/articles/26/7789/2026/)
- 对象/地点/气候：Sudokwon两关闭填埋区；Incheon韩国；温带季节性。
- 周期与方法：废物1998–2021；气体季节2005–2021；季节气体回收/燃烧/通量+FOD/CLEEN/RF校准。
- 变量与公式/参数：T/P、组成、L0、k、gas pathways；CLEEN_opt；见§2.3；完整回归系数未移植。
- 已验证应用范围：两相邻fill区的本地校准；不是本项目科学准入。
- 不确定性/外推限制：OX=0.10是模型假设；拟合不等于气候因果/跨区域验证。
- 本轮阅读深度：`FULL_RELEVANT_SECTIONS_REVIEWED`。

### L_LAM2026 · 填埋覆盖土CH4氧化

- 文献：Lam et al.，2026；10.3389/fenvs.2026.1960703。[原始来源](https://www.frontiersin.org/journals/environmental-science/articles/10.3389/fenvs.2026.1960703/full)
- 对象/地点/气候：填埋覆盖土CH4氧化；Southern Ontario加拿大土样；实验室。
- 周期与方法：20组温湿组合；1/15/25/35°C；20–100%WFPS；完整培养日期未提取；均质表土培养+反应扩散模型。
- 变量与公式/参数：CH4消耗、O2、T、WFPS、孔隙/扩散；Q10分湿度；反应扩散，参数见Tables1–4。
- 已验证应用范围：单一来源土的实验窗口；不是本项目科学准入。
- 不确定性/外推限制：重复注气不是独立设施复制；均质土不能直接代表原位覆盖层。
- 本轮阅读深度：`FULL_RELEVANT_SECTIONS_REVIEWED`。

### L_CLEEN2015 · 雨温/组成驱动填埋模型

- 文献：Karanjekar et al.，2015；10.1016/j.wasman.2015.07.030。[原始来源](https://pubmed.ncbi.nlm.nih.gov/26346020/)
- 对象/地点/气候：雨温/组成驱动填埋模型；实验+11个高收入国家conventional landfill；逐址清单未取得。
- 周期与方法：逐站观测周期UNKNOWN_ABSTRACT_ONLY；实验生成率回归及field scale-up。
- 变量与公式/参数：年降雨、ambientT、组成、k、L0；FOD/CLEEN；回归系数未从全文核对。
- 已验证应用范围：原始实验/校准样本范围；不是本项目科学准入。
- 不确定性/外推限制：不可复制未读系数；gas recovery受collection效率混杂。
- 本轮阅读深度：`ABSTRACT_ONLY`。

### L_POND2014 · 串联厌氧/兼性/成熟塘

- 文献：Hernandez-Paniagua et al.，2014；10.1080/09593330.2013.848910。[原始来源](https://pubmed.ncbi.nlm.nih.gov/24645453/)
- 对象/地点/气候：串联厌氧/兼性/成熟塘；标题subtropical；具体站点/气候代码未从摘要建立。
- 周期与方法：观测日期/时长UNKNOWN_ABSTRACT_ONLY；三塘温室气体通量及COD质量平衡。
- 变量与公式/参数：COD、表面负荷、塘类型、CH4/CO2；负荷/CH4相关；不是可直接用的通用气温公式。
- 已验证应用范围：处理agricultural wastewater的该系统；不是本项目科学准入。
- 不确定性/外推限制：不把后续文章的地理转述当原文证据；非澳洲市政塘通用因子。
- 本轮阅读深度：`ABSTRACT_ONLY`。

### L_WETMETH2021 · 自然湿地过程模型

- 文献：Nzotungicimpaye et al.，2021；10.5194/gmd-14-6215-2021。[原始来源](https://gmd.copernicus.org/articles/14/6215/2021/)
- 对象/地点/气候：自然湿地过程模型；全球/高纬湿地；Earth-system尺度。
- 周期与方法：多个年代；如2001–2004空间对照；非设施观测；UVic ESCM过程建模+观测/模型集合对照。
- 变量与公式/参数：土层T/C、水位、深度、氧化；Eq1及AppendixA：温度依赖Q10；生产/氧化分开。
- 已验证应用范围：原论文湿地/ESM验证尺度；不是本项目科学准入。
- 不确定性/外推限制：氧化/湿地面积/参数不确定；不能用于厂级污水/填埋直接预测。
- 本轮阅读深度：`FULL_RELEVANT_SECTIONS_REVIEWED`。

### L_ARCTIC2015 · Arctic泥炭微生物增温响应

- 文献：Tveit et al.，2015；10.1073/pnas.1420797112。[原始来源](https://pmc.ncbi.nlm.nih.gov/articles/PMC4434766/)
- 对象/地点/气候：Arctic泥炭微生物增温响应；Svalbard北极泥炭；实验室培养。
- 周期与方法：2010年8月采土；1–30°C缺氧microcosm，26–39天；温度梯度与群落/代谢分析。
- 变量与公式/参数：T、底物、微生物群落、CH4；代谢/营养互作；无拟移植的设施动力学系数。
- 已验证应用范围：该泥炭与培养体系；不是本项目科学准入。
- 不确定性/外推限制：群落转变/限速步骤可改变表观温度关系；不推广为污水塘效应量。
- 本轮阅读深度：`FULL_RELEVANT_SECTIONS_REVIEWED`。

### NSW_BIOFILTER2010 · 被动排气与生物过滤原始研究/手册

- 文献：UNSW / DECCW NSW，2010；DECCW2010/141。[原始来源](https://www.epa.nsw.gov.au/sites/default/files/100141-biofiltration.pdf)
- 对象/地点/气候：被动排气与生物过滤原始研究/手册；Sydney/NSW温带试验支撑；场地结构特定。
- 周期与方法：报告基于多年试验；不同子试验窗口须逐项查原页；田野试验及设计/监测指南。
- 变量与公式/参数：loading、CH4/O2、T、水分、覆盖结构；CH4氧化/氧传输/负荷关系；不是法定AWT新公式。
- 已验证应用范围：其材料、结构、gas loading范围；不是本项目科学准入。
- 不确定性/外推限制：工程手册非通用项目保证；不移植所列最佳效率作为默认值。
- 本轮阅读深度：`OFFICIAL_PRIMARY_TECHNICAL_REPORT`。

## 校准与下一步文献缺口

需要现场测量/专业校准：反应层温度、水分/水位、有效HRT/SRT、organic load、覆盖层孔隙/裂缝/氧扩散、实际gas collection与destruction、温度响应范围及速率常数。实验瓶的重复注气不能当独立场地复制，单季/单塘的回归不能自动用于另一气候区。冻土自然湿地、feedlot manure pond、市政曝气塘与填埋体不得混为一类。

下一轮应补齐摘要-only论文全文/原始表格（只能通过正常公开授权路径），核查现场跨季、跨址验证、参数可识别性及独立holdout；先审已有raw evidence可得性，再决定是否做受限科学实验。访问拒绝保留为缺口，不绕过认证或付费。来源和hash状态见source_receipts；文件下载目录年份不作为出版年份（MLA报告正文为2013，URL包含2019）。
