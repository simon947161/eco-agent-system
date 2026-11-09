# 来源、版本、权限及有限研究预算

机器唯一登记：[SOURCES.json](SOURCES.json)，含URL、locator、版本、权利、阅读级别、原始SHA或null、用途限制。12个新主题（同一Scorecard或NOAA GML产品家族的子页分别列记录），12深入案例，3深入机制，0新GIS数据集；[预算](BUDGET.json)不以下载页数或文件数量偷换主题预算。

| 主题 | 版本/尺度 | 权利与读取状态 |
|---|---|---|
| UN M49 | 2026-11-09英文在线表快照；统计标识 | 本轮只归档事实代码/名称及哈希。未找到可直接适用于此页面的开放再分发条款，不套用UNdata条款。完整HTML不分发 |
| Climate Scorecard | 固定评分HTML、报道索引、两个报道样本 | All Rights Reserved；事实标签/自写分析/链接；原站全文不分发 |
| Natural Earth | 1:10m/50m/110m产品族；精确产品版本未下载 | [官方条款](https://www.naturalearthdata.com/about/terms-of-use/)称public domain；仅核许可，不称边界已获/可用于地籍 |
| Köppen-Geiger | GloH2O V3索引，Beck2023；1km；历史与未来产品分离 | [作者页](https://www.gloh2o.org/koppen/)索引称CC BY4.0；直开超时，payload许可/文件版本未核，不做地理归类 |
| HydroBASINS | v1，12级，约15角秒父数据 | [产品页](https://www.hydrosheds.org/products/hydrobasins)的自定义HydroSHEDS许可，技术条款未完整读取，不称CC BY；无polygon下载 |
| IUCN GET | 冻结2.0/2020六层分类，非宣称最新 | [官方工具](https://iucn.org/resources/conservation-tool/iucn-global-ecosystem-typology)可读；完整出版物/边界再分发权未审计，只元数据 |
| NBI | undated station-purpose page快照 | [站点表](https://nilebasin.org/hydromet/map)定性拓扑；许可UNKNOWN，不复制地图、坐标或水文记录 |
| NOAA ENSO | 2026-11-09页面、2026-02-01 RONI过渡说明 | [官方科普与技术链接](https://www.noaa.gov/understanding-el-nino)；只发布事实解释，第三方图不复制 |
| IPCC AR6 | WGI2021 Ch6，Table6.2定位 | 原页403；BLOCKED。既有PR143引用只作继承；没有重新获得全文或可运行响应参数 |
| NOAA GML/AGGI | CH4 citation2026-10；AGGI2025更新 | 全球派生观测与经验辐射方法分别登记；本轮未下载新序列，未导入表中数值作计算 |
| UNFCCC NDC | 四国NDC3.0提交元数据 | 官方web可见行；直接获取HTTP200实际是防护页，212字节，不当成完整registry或开放数据包 |
| 澳联邦Climate Change Act | C2025C00153，2025-02-20，s10 | [固定法条](https://www.legislation.gov.au/C2022A00037/2025-02-20/2025-02-20/text/original/epub/OEBPS/document_1/document_1.html)用于查基年；只事实定位，不作法定认证 |

既有PR140 BRW、PR143公式、PR145审查器与本轮任务书仅引用当前Git树原件；`sha_if_downloaded`对继承文本明示LF归一化，HTTP原件哈希则为精确字节。许可证、校准、源率等原门不因引用而升级。

## 原始取得与失败

[acquisition.json](evidence/acquisition.json)记录4地址各一次：M49 1,721,575字节；scorecard 113,041；reports 91,778；NDC 212字节。每份原始响应有精确SHA；[content-checks](evidence/content-checks.json)独立区分HTTP成功与内容成功。网页原件留在git-ignored `runtime_data/global_natural_atlas_metadata`，不承诺其他机器拥有这些缓存。

另有一次UN通用terms页403、IPCC页403、NOAA旧反证文章机器人验证；均不再重试或改URL绕过。Scorecard首页与Köppen页面超时保留缺口；IUCN初始域名不正确，使用检索确认的正式iucn.org工具页，这不是绕过受限来源。

可离线复查已提交的事实摘录/机器记录/代码/哈希；不能仅凭这些摘录声称已独立验证未分发的全部网页原件。哈希证明固定字节身份，不证明许可、科学有效性或发布者真实性；来源归属另由官方URL/章节与人工审查建立。
