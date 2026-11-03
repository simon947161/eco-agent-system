# 检索方法、来源清单与证据状态

2026-11-04 · 本轮为有记录的结构化范围检索；不是声称穷尽所有论文的PRISMA综述。原始来源、文献提取、失败与阅读深度分开保存。

## 检索组与筛选

| 查询组 | 本轮使用的检索方向 | 采用/排除原则 |
|---|---|---|
| 温度/微生物 | methane Yvon-Durocher temperature dependence；Arctic peat warming；Arrhenius/Q10 | 采用原始meta-analysis、原始培养研究；不以综述引用替代未读原论文 |
| 塘体/季节 | Australian waste stabilisation pond seasonal temperature stratification；CSIRO feedlot methane | MLA/CSIRO原始报告、Bai2026等；不同废水/工艺分层 |
| 填埋/雨水 | landfill methane rainfall moisture generation CLEEN；meteorological impacts landfill | 区分generation、surface flux、recovery；采用已发表Kim2026，不再重复计其preprint |
| 氧化 | landfill cover oxidation moisture temperature；Sydney biofilter field；scaling lab to field | Lam2026、NSW2010原始技术报告；付费/拒绝全文只能摘要层 |
| 自然湿地 | WETMETH1.0；microbial warming wetland/peat | 记录模型尺度与现场适用边界，不移植参数到设施 |
| 官方方法 | AWT Register、ARRC remake、IPCC2006/2019、CER audits | 法律/咨询/清单/技术指导分开；复用P0字节不伪装新抓取 |
| 区域/空间 | BOM070217/039083；Cooma landfill/The Glen；Lakes Creek；GA DEM；CSIROsoil | 小型公开页面/目录；不调用已被ArcGIS499拒绝的接口，不抓国家数值grid |

入选条件：原始研究或官方来源、有可描述的对象/方法/范围；发布日期不晚于研究as-of日期。全文访问受限、未知窗口/地点/参数保留UNKNOWN。新闻、评论、社交页面及二手数据库不作为数值/因果证据。没有全文/原始数据的地方不假称完成全文复核。

机器清单：[SOURCE_CATALOG.csv](SOURCE_CATALOG.csv)；请求/复用记录：[source_receipts.json](evidence/source_receipts.json)；10份重点研究提取：[LITERATURE_EVIDENCE_REGISTER.csv](LITERATURE_EVIDENCE_REGISTER.csv)。这些行数不是独立论文数量：同篇的publisher失败、作者稿线索及官方书目可为不同receipt。

## 关键来源定位

- 历史法律：AWT2015 F2015L00060，§5/8/9–15/17–46，39页；20式及单位在公式登记，Part4 legacy适用性另保留。
- 2026咨询：ARRC October2026 26页，§4.2–4.15；不当成生效方法或最终ERAC草案。
- 官方科学：IPCC2006 Vol5 Ch3/Ch6，IPCC2019 refinement Ch3/Ch6（官网说明Ch6等有July2023勘误）；两代来源并存，不拼接为一套未经标注的新算法。[IPCC2019目录](https://www.ipcc-nggip.iges.or.jp/public/2019rf/vol5.html)。
- 原始科学：CSIRO/MLA B.FLT.0362（正文2013，不是URL的2019）；Bai2026 §2–3；Kim2026 §2.1–2.4及讨论；Lam2026 §2–4/Tables1–4；Tveit2015 Results/Methods；WETMETH2021 §3–5/AppendixA。完整定位见提取表。
- 区域：BOM站点页/气候表、GA DEM目录、CSIRO Soil and Landscape Grid原始发布说明及BOM分类技术文件。数据目录可用≠tile提取/设施join已完成。

## 失败、访问深度与不确定性

P0的8份官方原始字节被重新校验后复用，保留原2026-11-03 UTC取回时间；本轮新请求另存实际UTC时间。HTTP200只表示取得body，不自动表示科学验证或全文可用。原始body位于忽略目录 `.local/`，避免把完整版权论文重新公开。

大学作者稿Yvon2014本地请求404，web曾返回原文片段/书目，故只记partial web review；Nature publisher跳身份页，不认证。CLEEN2015及Hernandez2014只按原始摘要提取，未知参数/地点/窗口不补造。Scaling2011出现browser challenge、Sydney2011 publisher403，均不按完整论文使用；NSW公开手册为独立识别的官方原始技术来源，不冒充被拒论文全文。

Cooma EMP/污水目录及Rockhampton页面直接body下载403；Rockhampton设施页通过web可读的官方正文与本地下载失败分别记录，不宣称已保存该网页原字节。Cooma flaring公告只可确认搜索线索，当前投运/流量/效率UNKNOWN。拒绝请求没有token查找、付费或认证绕过。

本轮没有取得真实设施过程观测，也没有运行新排放/气候模型。全文可读不等于原始数据可复算；研究证据成熟度与ClimateOS `scientifically_admitted` 分开，后者仍false。

## 公式审计方法

先核对P0 hash，再提取PDF文本并渲染页14–29（PDF1起）。抽取器报告旋转文本不全，公式以渲染图交叉核对；20式、§号、单位与条件在CSV保留。仅由本研究执行者复核，未冒充两位独立专家。源/产物hash和视觉检查receipt用于追溯，不是法律或科学认证。
