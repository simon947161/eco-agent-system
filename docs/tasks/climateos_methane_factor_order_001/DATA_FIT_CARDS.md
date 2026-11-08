# 三候选数据适配卡（调查已停止）

2026-11-08 UTC获取；完整字节哈希、HTTP记录见[evidence/source_manifest.json](evidence/source_manifest.json)和acquisition.json。仅候选1下载数值产品。所有数值均为真实发布记录，未补值。候选数按独立产品/站点组合计，不按页面数计。

## 1 NOAA GML BRW 2024：RAW_PRODUCT_ACQUIRED / QC_LOCAL_VERIFIED / NOT_COMPARABLE

- [CH4 ZIP](https://gml.noaa.gov/aftp/data/trace_gases/ch4/in-situ/surface/ch4_brw_surface-insitu_ccgg_text.zip)、[发布者SHA](https://gml.noaa.gov/aftp/data/trace_gases/ch4/in-situ/surface/ch4_brw_surface-insitu_ccgg_text.zip.sha256)、[方法README](https://gml.noaa.gov/aftp/data/trace_gases/ch4/in-situ/surface/README_ch4_surface-insitu_ccgg.html)。版本2026-08-11，DOI [10.15138/ve0c-be70](https://doi.org/10.15138/ve0c-be70)，Pétron等/NOAA GML，CC0。
- [2024气象原件](https://gml.noaa.gov/aftp/data/meteorology/in-situ/brw/met_brw_insitu_1_obop_hour_2024.txt)、[数据页](https://www.gml.noaa.gov/data/dataset.php?item=brw-met-hourly-2024)、[气象README](https://gml.noaa.gov/aftp/data/meteorology/in-situ/README)。数据页标CC0、更新2026-01-09；旧README请求发表前联系。此处仅公开数据研究与署名，不联系第三方，不宣称合作或认可。
- 原ZIP 7,041,741 bytes；SHA `2fcf772a81598f5fcfcde63af56e822905f518a24d4efd681cfc5b3e564b0cce` 与发布者相同。气象611,733 bytes；SHA `38150a86d6f95a375757fc39173036b1f75950ed29f265f03bfa4404ee77fbe1`（仅本地指纹，非发布者独立校验）。
- ZIP包含小时/日/月产品；只读小时成员。归档2024甲烷子集保留原头部和行值，LF规范化，哈希不等于原ZIP。气象字节原样归档。原件为小时发布产品，不是秒级传感器信号。
- CH4字段：干摩尔分数nmol/mol、std_dev、value_unc、nvalue、UTC、midpoint、经纬度、altitude/elevation/intake_height、仪器和3字符QC。尺度CH4_X2004A；2024仪器LGR-5，进气高度实际为9.9/35.05m；标称地面高程11m，纬度71.323、经度约−156.611。不能用站点标称高度覆盖逐行高度。
- 气象14字段：站点/年/月/日/小时、风向°、风速m/s、steadiness、实际站压hPa、T2m/T10m/Ttower℃、RH%、降水mm/h。UTC小时起点，与CH4标签定义一致；没有逐行气象QC。README说明自动和人工筛查，但不能称每行均质量通过。
- CH4负填充值或nan排除；头部value填充值−999.999与README通用−999.99存在表述差别，脚本均以非负有限值为条件。气象T−999.9、P−999.90、RH−99等排除。气象45小时没有行、降水所有8739行缺测；不将其解释为零雨。
- value_unc含重复性/再现性/校准不确定度；不能把行内std/sqrt(n)当全部误差。气象P/T/RH仪器精度、RH水/冰定义及传感器完整高度未知，未建立与CH4采样高度的代表性误差。2024避免2025仪器变更时间资料差异，但不消除其他缺口。
- BRW背景选择含风向020–110°及风速条件。`.C.`不是无效测量；本轮只选`...`是保守背景筛选，不是独立风效应证据。完整行3340，但科学配对0。

## 2 ICOS Cabauw 207m：METADATA_ONLY / NOT_ADMITTED

- [官方记录](https://meta.icos-cp.eu/objects/NL-p6ji6ALoP8lUoCeugwODX)，页面实际HTTP200、归档指纹；不是403。
- 文件名`ICOS_ATC_NRT_CBW_2025-04-01_2026-04-16_207.0_970-1113_CH4.zip`，Level1 NRT，页面标Deprecated data。生产2026-04-17。所列9144行/135940字节是**发布者声明，未下载核实**。
- ICOS CC BY4.0；经纬度51.9703/4.9264，标称地面0m、采样207m；Picarro CO2/CH4/H2O。字段UTC、Flag、NbPoints、CH4干nmol/mol、Stdev，不含配对P/T/e。元数据R/U/O等标记，不能把未审核标记当科学通过。
- 发布者声明SHA `34bfa9ea38ba00ba0ff25528029837aa298a46edfd134c8b0b91f823a36c46c1` **不采用**：以归档页面原字符串为准，未下载故不建立本地原件SHA。机器manifest只对HTML计算哈希。
- 处理：NOT_ATTEMPTED_FIT_SCREEN（近实时已替代产品、完整同期气象配对和误差未证实），不假称全站必须认证。[官方使用说明](https://www.icos-cp.eu/data-services/data-portal/how-to-use)区分网页与程序访问；本轮未申请账户、未接受额外服务或扩展到第四候选。

## 3 WMO/GAW WDCGG Ispra 40m：METADATA_ONLY / NOT_ADMITTED

- [官方记录](https://gaw.kishou.go.jp/search/file/0162-6272-1002-02-01-6041)，HTTP200；版本2026-08-27-0001，更新2026-09-24。
- 产品`ch4_ipr6272_tower-insitu_162_6041-9999_hourly`；目录时段2017-12-10至2026-07-24 UTC，ppb，X2004A，40m，45.8030014038/8.626999855。Picarro G2401；原生采样频率UNKNOWN，小时为发布频率。
- ICOS CC BY4记录及GAW使用政策需共同核对；页面请求重大使用时联系/协作，不代替科学验证。只登记元数据，不联系PI或接受新授权。
- 质量包含历史PI审核、Level2、Fast Track及NRT等不同阶段，不能全称最终版；U/N/O/K/R/H说明存在。气象可用性栏目未明确，视UNKNOWN，不断言全球目录不存在气象。
- 没下载数值原件、无本地数值SHA、无字段实检或时间连接。目录DOI [10.18160/K54N-TNWH](https://doi.org/10.18160/K54N-TNWH)不代表本轮所有数据已准入。停止于METADATA_ONLY。

## 获取异常与透明性

网页工具对部分URL返回不可访问/cache miss，不是HTTP403；随后合法直接请求成功。noaa-discovery.json有一条status=null：文件写入后控制台cp1252无法打印字符，原记录保留；这是输出编码失败，不能记作下载被拒。纠正依据为已写HTML、SHA和后续解析，不重复获取。既有Council/EPA等受阻入口未重试。
