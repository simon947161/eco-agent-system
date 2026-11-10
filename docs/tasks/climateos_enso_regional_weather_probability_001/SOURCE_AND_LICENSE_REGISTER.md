# 来源、权利和证据登记

查阅日期2026-11-10；浏览器文本/元数据可读与原始文件下载成功分开记录。无在线凭证、Council资料或外部联络。没有宣称获得法律意见或商业再分发授权。

| ID | 官方来源/版本/定位 | 权利及范围 | 取得与使用状态 |
|---|---|---|---|
| BASE | [PR147 D](https://github.com/simon947161/eco-agent-system/tree/48d0f576e651cd5072e6319ea1539ffa5ba02936)、[最新评审](https://github.com/simon947161/eco-agent-system/pull/147#issuecomment-6756526286) | 用户授权仓库研究；只增量，不改冻结成果 | 原审查全文及143–147 HEAD见 baseline-and-review.json |
| RONI | PR147 `evidence/RONI.ascii.txt` 与 `roni-metadata.json` | 沿用原NOAA来源、许可、ERSSTv6和1991–2020基准 | 原SHA冻结 `1297887f581b6190e459cbbf8bdec9a703ff65c1a229e2de4dd94285254f35c8`；不再次下载 |
| BOM-AGCD | [AGCD说明](https://www.bom.gov.au/climate/austmaps/about-agcd-maps.shtml)，月/日格点产品 | 不将网页许可泛化成全部格点再分发权；本轮仅文档调查 | 天气产品候选1；未取新序列，PR147受阻动态URL未重试 |
| PRCP-V4 | [NCEI产品](https://www.ncei.noaa.gov/products/land-based-station/global-historical-climatology-network-monthly)，[C01657元数据](https://www.ncei.noaa.gov/access/metadata/landing-page/bin/iso?id=gov.noaa.ncdc:C01657)，[DOI](https://doi.org/10.25921/67zp-5m03) | Applequist, Durre, Vose (2024), GHCN Monthly Precipitation V4，注明子集和访问日；月观测汇编非均一化实测仪器原记录 | 天气候选2，选择v4.00.00；产品页简介另有beta字样，不能隐去版本成熟度差异 |
| INV | [官方库存](https://www.ncei.noaa.gov/data/ghcnm/v4/precipitation/doc/ghcn-m_v4_prcp_inventory.txt) | 数据集元数据摘录，保留署名；全12MB不入Git | HTTP200，Last-Modified 2026-11-05；原字节SHA `c1311f7300ad9ea80830ff1c1f30d9a803c4c3674644339cd290e4004702e219` |
| RAIN | [请求的固定归档](https://www.ncei.noaa.gov/data/ghcnm/v4/precipitation/archive/ghcn-m_v4.00.00_prcp_s16970101_e20260930_c20261004.tar.gz) | 仅拟作署名、非商业研究；未取得内容；无已准入雨量或授权泛化 | HTTP404，零载荷，SHA UNKNOWN；网页目录曾显示该版本，不保证实时文件存在；不重试 |
| FORMAT | [PRCP readme](https://www.ncei.noaa.gov/data/ghcnm/v4/precipitation/doc/ghcn-m_v4_prcp_readme.txt)，[GHCN国家码](https://www.ncei.noaa.gov/pub/data/ghcn/daily/ghcnd-countries.txt) | 官方格式说明；仅归档自写字段摘要/短引文 | 首轮格式可读；后续web工具提示不可访问，未作网络下载重试；国家码AS=Australia、AU=Austria已核验 |
| RIGHTS | [NCEI Open Data Policy 2022-12-14 §4(a–c)](https://www.ncei.noaa.gov/sites/default/files/2023-12/NCEI%20PD-10-2-02%20-%20Open%20Data%20Policy%20Signed.pdf)，[GHCN-D说明§I](https://www.ncei.noaa.gov/pub/data/cdo/documentation/GHCND_documentation.pdf) | 联邦产物US public domain；第三方权利可能保留。GHCN-D上游提示部分非US数据有WMO商业再出口限制；GHCN-M专属元数据未列具体CC许可证 | 可进行本轮非商业研究和元数据引用；**不声明整包CC0，不发行完整原档，商业复用/再分发仍需产品级复核**。GHCN-D不自动等同月产品条款 |
| DMI | [PSL DMI元数据](https://psl.noaa.gov/data/timeseries/month/DMI/)、[计算代码](https://psl.noaa.gov/data/timeseries/month/DMI/dmi.ncl)、[PSL政策](https://psl.noaa.gov/disclaimer/) | NOAA派生指数，源HadISST1.1；源数据权利不能仅凭NOAA域名判断。代码指向月气候态但未在所读代码中注明其基年 | 官方文本预览可读，未保存本地原字节、未准入、未分层；指数基年UNKNOWN |
| AAO | [CPC AAO](https://www.cpc.ncep.noaa.gov/products/precip/CWlink/daily_ao_index/aao/aao_body.html)、[NWS政策](https://www.weather.gov/disclaimer) | NWS public domain除另注明；署名、不暗示官方背书；SAM相关但不是Marshall站压SAM | 1979起月指数；原ASCII在web工具为不支持的MIME400，非权限拒绝；未本地下载、未准入 |
| BOM-HIST | [ENSO事件历史](https://www.bom.gov.au/climate/history/enso/) 2023–24段 | 官方解释/回顾，引用链接及摘要；不复制图片，不当序列 | SOURCE_CONTRADICTS“厄尔尼诺必旱”；与本地1961–2020试验NOT_COMPARABLE |
| BOM-2023 | [年度声明2023](https://www.bom.gov.au/climate/current/annual/aus/2023/) Australian climate influences / Southern Hemisphere mid-latitudes | 2024-02-08发布的历史回顾，不是预测 | SOURCE_SUPPORTS 多模态与天气系统共同影响；非九站降雨观测 |
| PAPER | [GHCN-M v4论文DOI](https://doi.org/10.1038/s41597-024-03457-z) | 只登记题录/DOI，未归档全文 | Nature转身份服务不可访问，不重试，不能声称全文方法独立审读 |

GHCN-M推荐引用：Applequist, Scott; Durre, Imke; Vose, Russell (2024), *Global Historical Climatology Network Monthly Precipitation, Version 4*, NOAA NCEI, DOI 10.25921/67zp-5m03，本站仅使用九站库存元数据摘录，访问2026-11-10。

## 字段与质量（格式说明而非已验雨量）

库存为固定宽度：ID1–11；纬度13–20；经度22–30；高程32–37；名称42–79；WMO81–85；首年87–90；末年92–95。WMO99999缺失，高程−999.9缺失。首末年不证明中间完整。库存位置是最新记录，不能证明1961–2020固定站址。

PRCP固定宽度格式标明年月、十分之一mm、M/Q/S标志、源索引。trace=-1；M=A至E为1–5缺日；M空白可能日完整也可能月源未知。Q D/K/L/O/R/S/T/W分别涵盖重复、恒定串、孤立、离群、纪录值/负值、空间湿日、空间总量、国家相邻月同值问题。S D/H/M/R/S/W/Z映射日档/USHCN/月世界气候/国际集合/GSOD/世界天气纪录/修订来源。详见预登记拒绝规则。不得把所有空标志宣布为“原始日质量通过”。

没有原始雨量就没有校准、完整性、变化点或站址迁移的实证核验。上述待验项目都保留PENDING。
