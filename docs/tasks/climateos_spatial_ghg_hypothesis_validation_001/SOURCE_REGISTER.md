# 来源与访问证据登记

检索/读取日期 2026-11-09 Sydney（原件下载 UTC 2026-11-08）。`FULL_METHOD`、`ABSTRACT`、`INDEX_ONLY` 和 `ORIGINAL_BYTES` 不能互换。未将网页索引片段写成全文复核。下列为有界检索结果，不宣称系统综述或穷尽反证。

| ID | 官方/原始来源、版本 | 读取层级与具体定位 | 用途及限制 |
|---|---|---|---|
| S1 | [NASA ESPO ATom merged landing](https://espo.nasa.gov/step/content/ATom_Merged_Atmospheric_Chemistry_Trace_Gases_and_Aerosols)，2018 v1 DOI 10.3334/ORNLDAAC/1581；[v2 catalog](https://www.earthdata.nasa.gov/data/catalog/ornl-cloud-atom-merge-v2-1925-2.0)，DOI 10.3334/ORNLDAAC/1925 | v1 landing 实际200；v2只有官方搜索索引。v2目录记载2021-08-26发布、2024-05-02更新、2016–18任务及多时间聚合 | 版本不能混写；未取得数值飞行文件。v1 landing SHA有本地回执，页面非数据集 |
| S2 | McKain/Sweeney [NOAA-Picarro ATom1234 instrument README](https://espoarchive.nasa.gov/sites/default/files/archive_docs/NOAA-Picarro_ATom1234_readme.pdf) | FULL_METHOD，6页，仪器/采样时滞/标定及 §5误差 | G2401m、干摩尔分数及校准；分析1σ不是完整气象/代表性预算 |
| S3 | Baier et al. (2021) [NOAA AirCore](https://www.gml.noaa.gov/data/dataset.php?item=Aircore-balloon)，DOI [10.15138/6AV0-MY81](https://doi.org/10.15138/6AV0-MY81)，v20210813 | ORIGINAL_BYTES，[README](https://www.gml.noaa.gov/aftp/data/AirCore/Readme_20210813.txt)、[ZIP](https://www.gml.noaa.gov/aftp/data/AirCore/NOAA_AirCore_data_v20210813.zip)实际200；landing更新时间2021-08-16 | landing明确CC0并要求引用致谢；归档一个剖面原始成员。README声明159 flight days，不当成本次计数 |
| S4 | [WDCGG Jungfraujoch CH4](https://gaw.kishou.go.jp/search/file/0023-6036-1002-01-01-9999)，版本2025-07-08-1503，更新2025-07-10 | METADATA_ONLY，measurement information、quality、data files、policy | UTC+01:00、进气口10mAGL、X2004A；固定高山站不是垂直剖面。未同意数据政策或取得数值文件 |
| S5 | IPCC AR6 WGI 最终 [Chapter 7](https://www.ipcc.ch/report/ar6/wg1/chapter/chapter-7/)、[Chapter 6](https://www.ipcc.ch/report/ar6/wg1/chapter/chapter-6/)、[SPM](https://www.ipcc.ch/report/ar6/wg1/chapter/summary-for-policymakers/) | INDEX_ONLY：官方索引涉及well-mixed GHG、OH/CH4、ERF分类。最终第7章PDF索引定位§7.3.2/7.3.4/7.3.5，未阅读全文确认上下文 | 网页访问403；不引用未核实表格数值，不把草案当最终版。全文核验仍缺口 |
| S6 | Grewe et al. 2014, Aircraft routing with minimal climate impact: REACT4C climate cost function modelling approach (V1.0), [DOI10.5194/gmd-7-175-2014](https://gmd.copernicus.org/articles/7/175/2014/)；[PDF](https://gmd.copernicus.org/articles/7/175/2014/gmd-7-175-2014.pdf)，CC BY3 | FULL_PAPER，§3.2.1 Tables2–3 p182–183、§3.3.3 Eq47 p187、Table7 p189、Fig14 p194 | 成熟已发表位置/时间脉冲设计；气体种类边界见反事实报告；未独立复跑，未取得完整输入/代码环境 |
| S7 | Joos et al. 2013, Carbon dioxide and climate impulse response functions for the computation of greenhouse gas metrics: a multi-model analysis, [DOI10.5194/acp-13-2793-2013](https://acp.copernicus.org/articles/13/2793/2013/) | ABSTRACT，期刊原始论文摘要 | CO2背景/脉冲/时域影响；不是不同排放高度的控制试验。不将大脉冲试验直接等同1吨实验 |
| S8 | Lee et al. 2021, The contribution of global aviation to anthropogenic climate forcing for 2000 to 2018, DOI10.1016/j.atmosenv.2020.117834；[NOAA作者稿记录及摘要](https://repository.library.noaa.gov/view/noaa/45026) | ABSTRACT/METADATA；出版者DOI403后未取全文；机构页面摘要可读，不下载替代全文 | 航空CO2/非CO2分类证据，不给“纯CO2每吨高空放大倍数”；机构所列PDF hash不是本地验证hash |
| S9 | Frömming et al. 2012, Aviation-induced radiative forcing and surface temperature change in dependency of the emission altitude, [DOI10.1029/2012JD018204](https://doi.org/10.1029/2012JD018204) | ABSTRACT_INDEX_ONLY，完整页面未成功读取 | 航空高度情景线索，含燃油与非CO2变化，不能声称固定纯气体质量的完整验证 |

## 访问失败及停止账本

| 入口 | 实际观察 | 处理 |
|---|---|---|
| https://doi.org/10.3334/ORNLDAAC/1581 | web工具报告403 | 一次后停止，不换镜像 |
| https://www.earthdata.nasa.gov/data/catalog/ornl-cloud-atom-merge-v2-1925-2.0 | web工具报告403；搜索索引可见 | 不重试数值下载；索引只作元数据 |
| IPCC AR6 chapter7、chapter6、SPM最终网页 | web工具报告403 | 停止该入口；未把搜索结果中的FOD/SOD草案纳入最终证据 |
| https://www.ipcc.ch/site/assets/uploads/2018/02/WG1AR5_Chapter08_FINAL.pdf | web工具报告403 | 停止；有关位置不敏感的索引句子不作已读全文证据 |
| https://doi.org/10.1016/j.atmosenv.2020.117834 | web工具报告403 | 不取替代全文，仅保留已有机构摘要层级 |
| AirCore README/ZIP web工具 | 工具解析400（文本编码/二进制格式），不是认证403 | 官方公开URL由urllib直接取得200；没有登录或令牌；字节回执归档 |
| WDCGG政策入口 | 需要政策确认，未进行数值下载 | metadata后停止；不把它误记为403或“数据必然私人” |

Web工具报告是当次访问观察，不是归档服务器响应头；仅AirCore/ESPO实际下载有本地HTTP/字节回执。没有对403入口重试、镜像、凭证获取、PI联系或付费。候选总数3，不新增第4个。

## 数据引用与再分发范围

AirCore 原件按 NOAA CC0 声明归档，署名 Baier、Sweeney、Newberger、Higgs、Wolter及NOAA GML。README按原始字节保存，个别重音字符不是UTF-8；脚本不改写它。仪器标识/校准瓶编号是公开科学元数据，不是访问密钥。未归档私人资料、Cookie或凭证。其余论文只保存原创摘要和链接，不整篇复制或再次分发未核实许可的内容。
