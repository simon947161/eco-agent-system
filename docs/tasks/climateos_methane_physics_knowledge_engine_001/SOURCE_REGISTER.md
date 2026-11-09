# 来源登记与引用层级

本轮8个主要外部来源主题（含访问失败），低于12上限；S00为既有代码/作者推导。未下载数据候选，未绕过认证。访问日2026-11-09。只做有限段落释义，不再发布完整版权正文。永久公式定义与当前法定效力分离；没有法定计算资格。

|ID|原始来源/版本|实际阅读层级与定位|
|---|---|---|
|S01|[NASA Glenn Equation of State](https://www.grc.nasa.gov/www/k-12/airplane/eqstat.html)；2021-05-13|BODY_READ；pV=nRT and absolute temperature paragraphs|
|S02|[NOAA CarbonTracker CH4 glossary](https://gml.noaa.gov/ccgg/carbontracker-ch4/glossary.html)；web snapshot 2026-11-09|BODY_READ；Mole Fraction; Flux; Methanogenesis; Model-Data Mismatch|
|S03|[IPCC 2006 Volume 5 Chapter 3](https://www.ipcc-nggip.iges.or.jp/public/2006gl/pdf/5_Volume5/V5_3_Ch3_SWDS.pdf)；2006|PDF_SECTIONS_READ；printed pp3.8-3.10 Eq3.1-3.6; section3.2.3; no 2019 defaults mixed|
|S04|[Sander Henry compilation and publisher-maintained CH4 table](https://henrys-law.org/henry/casrn/74-82-8)；5.0.0 / 2023 DOI10.5194/acp-23-10901-2023|AUTHOR_DATABASE_BODY_READ；CH4 table column H_s^cp, mol/(m3 Pa), reference298.15K; notes; publisher article timed out|
|S05|[NIST combining uncertainty](https://physics.nist.gov/cuu/Uncertainty/combination.html)；web snapshot 2026-11-09|BODY_READ；Eq6 first-order Taylor and covariance; uncorrelated simplified product|
|S06|[EPA CMAQ overview of science processes](https://www.epa.gov/cmaq/overview-science-processes-cmaq)；2026-05-13|BODY_READ；Advection; Turbulent Dispersion; overview; conceptual processes not exact CH4 solver validation|
|S07|[NASA JPL chemical kinetics evaluation](https://jpldataeval.jpl.nasa.gov/)；JPL19-5 official search metadata|OFFICIAL_SEARCH_METADATA_ONLY；direct page502; no OH coefficient/table imported|
|S08|[IPCC AR6 WGI Chapter7](https://www.ipcc.ch/report/ar6/wg1/chapter/chapter-7/)；AR6 2021; current errata NOT_VERIFIED|OFFICIAL_SEARCH_EXCERPT_ONLY；direct403 stopped; search excerpt Table7.15 and supplementary metrics; no numeric GWP imported|
|S00|[Frozen ClimateOS P1 and own algebra](repository:cczps_lite/integration/physics_validation.py)；PR138 f9016aa4cdc728728a1a5dece0b947b1c2e5e7bc inherited unchanged|SOURCE_CODE_READ；gas_properties; reference_dry_volume; declared constants; own derivative and bookkeeping derivations|

S00的repository:标识为机器来源标识，源码在仓库根cczps_lite/integration/physics_validation.py；不代表外部文献。

S03确认年度FOD和未捕集部分氧化的边界；E07设备未完全破坏的附加项是本任务记账扩展，不冒称IPCC Eq3.1原文。未将2019默认参数混入2006版本。

S04出版社论文URL https://acp.copernicus.org/articles/23/10901/2023/ 首次超时，未反复重试；读取作者维护的甲烷表及notes，确认H_s^cp单位及298.15K参考。原始测量论文未逐篇阅读，任何表中系数都未准入计算；污水盐度、温度与平衡条件仍需核查。

S07主页502后停止，只有官方搜索元数据支持其化学评估资料身份；CH4+OH质量作用式是候选机制表达，k(T)、温区和测量误差未核验，不数值运行。S08正文403后停止；搜索原始官方PDF片段仅作指标上下文，不绕行下载；现行勘误未核验，因此不引用数值GWP或寿命。

S06支持输送、湍流、化学与时空变化概念；E10是作者写的守恒型示意式，不是从该页提取的CMAQ算法。E09液膜闭合和E12恒寿命线性脉冲、E13指标/温度卷积均候选，未获取完整权威求解实现。E14是作者条件记账，不提供干预因果效应。

反证和可证伪边界：压力变化可在相同摩尔比例下改变质量浓度而不改变同份气体的甲烷总质量；本轮守恒测试直接检验这一点。真实源率可能随压力而变，但必须有通量/边界观测才能区分。Henry平衡不保证动态逸散，需两侧浓度及通量验证；局部OH时间不等于全球扰动寿命。若未来独立共址观测与预测不符，需检验模型结构/参数/测量偏差，不为原假说挑样本。
