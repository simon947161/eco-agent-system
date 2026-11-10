# 来源、许可和实际访问

核查日2026-11-10。七个平台做官方元数据调查；实际仅一个产品、三份文件、420750字节。网页浏览摘记是元数据核查，不冒充保存下来的原始HTTP响应；未将其计为下载数据文件。所有真正GET数据文件均在DOWNLOAD_RECEIPTS.json。首次站点HEAD200检查大小不含载荷；失败旧归档从未重试。

| 平台 | 来源 | 许可/再利用 | 实际访问 | 未选或替代理由 |
|---|---|---|---|---|
| Australia Queensland SILO | [官方入口](https://www.longpaddock.qld.gov.au/silo/about/access-data/) | CC-BY-4.0 | METADATA_READ; identity/email required; no data request | AUTH_REQUIRED contact identity; public 14MB annual monthly grids would require too many files for 60y; no global download |
| Australia BoM | [官方入口](https://www.bom.gov.au/climate/austmaps/about-agcd-maps.shtml) | raw product redistribution not established from map page | METADATA_READ; no bounded current point payload identified; old blocked CGI not retried | LICENCE_UNCLEAR for proposed raw redistribution and no bounded selected payload; current NOAA panel fits original support |
| NOAA NCEI | [官方入口](https://www.ncei.noaa.gov/products/land-based-station/global-historical-climatology-network-monthly) | CC0-1.0 listed in official product Data.gov record; cite Applequist/Durre/Vose2024 DOI10.25921/67zp-5m03 | HEAD200 first station; three GET200 station CSV files, 420750 bytes | Current small station access replaces only failed archive access; preserves original Wagga support and no result-driven selection |
| NASA POWER | [官方入口](https://power.larc.nasa.gov/docs/services/api/temporal/monthly/) | NASA open data; product rights not separately archived, no payload redistribution | METADATA_READ; obsolete precipitation methodology URL404 not retried; no data request | TIME_SUPPORT_MISMATCH: only10 baseline years versus fixed24 minimum; not downloaded after NOAA admitted |
| Copernicus CDS | [官方入口](https://cds.climate.copernicus.eu/datasets/reanalysis-era5-single-levels-monthly-means?tab=download) | CC-BY listed; terms must be accepted in account | METADATA_READ; login/license acceptance required; skipped | AUTH_REQUIRED; no credentials created or inspected |
| China CMA National Meteorological Science Data Center | [官方入口](https://data.cma.cn/) | UNKNOWN product-level reuse not verified | Official root web-reader timeout; old2014 official catalog searchable, current product terms UNKNOWN | LICENCE_UNCLEAR and non-Australian support; cross-region future candidate only |
| China CAS CASEarth | [官方入口](https://data.casearth.cn/?locale=zh) | UNKNOWN; no blanket open license inferred | root unavailable; data portal no readable lines; official search-index descriptions readable; no product data | LICENCE_UNCLEAR and no qualified product; future ecosystem gateway only |

## 选定产品的许可判断与矛盾

[Data.gov产品记录](https://catalog.data.gov/dataset/global-historical-climatology-network-ghcn-monthly-precipitation-version-4) 的 License/Additional Metadata列CC0-1.0，Direct Download指向本次长路径。相同记录仍含accessLevel=non-public、rights=otherRestrictions及异常单日1697时间字段；这些矛盾没有被删除。不能只由HTTP200推断开放许可，也不将NOAA总域名视为所有国际资料的再分发授权。

[NCEI产品元数据C01657](https://www.ncei.noaa.gov/access/metadata/landing-page/bin/iso?id=gov.noaa.ncdc:C01657) 的Use/Access Constraints要求引用并说明不保证准确性/适用性，本轮没有读到额外禁止研究或要求登录的条款。综合**该产品明确CC0记录、NCEI产品约束和实际公开单站入口**，本包将三份小文件作为本轮研究材料归档，保留署名、版本、原字节和上述目录矛盾；这是有依据的研究许可判断，不是商业使用法律认证。评审若发现具体相反条款，应停止进一步再利用并隔离受影响载荷。

引用：Applequist, Durre & Vose (2024), GHCN-Monthly precipitation version4，NOAA NCEI，[DOI 10.25921/67zp-5m03](https://doi.org/10.25921/67zp-5m03)。本轮使用2026-11-05更新的三个文件，下载于2026-11-10；不冒充2024静态发布字节。

## 官方核查位置与失败分层

- SILO：[Access data](https://www.longpaddock.qld.gov.au/silo/about/access-data/)列CC-BY4；[API guide](https://www.longpaddock.qld.gov.au/silo/api-documentation/guide/)要求联系邮箱。没有填假邮箱或使用用户身份。AUTH_REQUIRED/USER_ACTION_REQUIRED后跳过。
- BoM：[AGCD说明](https://www.bom.gov.au/climate/austmaps/about-agcd-maps.shtml)说明基于站点的分析及2020年业务切换。未取得满足本预算的60年单点原始包；网页可读不能证明任意原数据再分发权。
- NASA：[Monthly API](https://power.larc.nasa.gov/docs/services/api/temporal/monthly/)及[Communities methodology](https://power.larc.nasa.gov/docs/methodology/communities/)说明气象覆盖1981起，1961–90只有10年。即使许可补齐也不能过24年门。自动门当前先报LICENCE_UNCLEAR（未归档产品权利），科学适配另报TIME_SUPPORT_MISMATCH。旧precipitation文档404不重试。
- Copernicus：[ERA5月资料](https://cds.climate.copernicus.eu/datasets/reanalysis-era5-single-levels-monthly-means?tab=download)有1940起资料、许可和登录提示；[API说明](https://confluence.ecmwf.int/pages/viewpage.action?pageId=726487525)需要账户及接受条款。未创建/查找凭据、未请求全球切片。
- CMA：根入口网页读取超时，不等于HTTP403。只见[2014年科技部目录](https://www.most.gov.cn/ztzl/kjzykfgx/kjzygjjctjpt/kjzyptml/201407/W020140716589850004914.pdf)的历史产品描述；不能替代当前版本/许可。中国站点不能作为澳洲同地观测。
- CASEarth：[官方门户](https://portal.casearth.cn/)及[数据平台](https://data.casearth.cn/?locale=zh)搜索索引有资料说明，但读取没有可用产品条款，逐产品许可UNKNOWN。不推断平台全部开放。
- NCEI当前doc目录可见readme文件名；直接readme网页工具不可读、FullText元数据返回invalid id，均未重试。CSV字段解释复用PR148已归档格式审计并以实际11列结构交叉核验；不声称本轮重新完整读取readme。

软件fallback仅产生决定轨迹，network_executed=false。真实获取由单独有限白名单脚本执行，本轮人工按该决定转向当前NOAA单站，不存在自动遍历全球端点的网络服务。测试中的404/403/499为明确夹具，不能冒充本轮实际HTTP收据。
