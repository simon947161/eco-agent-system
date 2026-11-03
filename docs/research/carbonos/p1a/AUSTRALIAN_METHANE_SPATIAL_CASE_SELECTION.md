# 澳大利亚区域候选：Cooma 与 Rockhampton

2026-11-04 · **选择研究背景对照，不宣称已经得到同工艺设施配对实验。** 优先比较同类填埋过程；污水塘只作另一独立候选，不能把两地不同工艺排放直接相减。

## 两个区域及公开背景

| 项目 | Cooma / Snowy Monaro | Rockhampton |
|---|---|---|
| 背景气象站 | Cooma Airport AWS 070217 | Rockhampton Aero 039083 |
| 站点坐标/海拔 | −36.29°,148.97°；930m | −23.38°,150.48°；10m |
| 月平均最高气温（1月/7月） | 26.6 /10.3°C | 32.1 /23.3°C |
| 月平均最低气温（7月） | −2.0°C | 9.8°C |
| 气温表期 | all-record，1990–2026，36年可用 | all-record，1939–2026，87年可用 |
| 雨量背景 | 年平均537.5mm，1982–2026，35年可用 | 年平均802.9mm，1939–2026，84年可用 |
| 同类固废设施线索 | Cooma landfill：官方EMP/2024 flaring公告索引；本轮直接获取403，未取得当前运行记录 | Lakes Creek Road官方设施页列landfill zones；可经web读正文，直接下载403；flare页面只能确认公开项目线索 |
| 污水线索 | The Glen环保资料目录：官方搜索可见；原文抓取403；工艺/塘体状态不据此认定 | 不用未经核实的地图/二手资料指定塘体类型；需另核官方工艺 |

来源：[BOM Cooma](https://www.bom.gov.au/climate/averages/tables/cw_070217.shtml)、[BOM Rockhampton](https://www.bom.gov.au/climate/averages/tables/cw_039083.shtml)、[Rockhampton facility](https://www.rockhamptonregion.qld.gov.au/CouncilServices/Rockhampton-Regional-Waste-and-Recycling/Landfill-and-Waste-Facilities/Lakes-Creek-Road-Waste-Management-Facility)、[Cooma EMP官方链接](https://www.snowymonaro.nsw.gov.au/files/assets/public/v/1/environment-and-waste/waste-amp-recycling/documents/cooma-landfill-emp-final.pdf)。气象原始页面、解析表及hash已本地保存；设施失败/摘要与完整正文分开记录。网页“拟安装”/新闻“已推出”不能证明今天的捕集效率或设备状态。

上述坐标/海拔是**气象站**，不是设施点。气象统计区间不同，不是1991–2020共同气候常值；资料截止表为2026-10-31。表中monthly mean Tmax/Tmin不是日均温，不计算两者平均冒充Tmean，也不输入甲烷模型。气候差异支持候选筛选，不支持甲烷效应量或气候变化归因。

## 公开空间与过程资料的可得性

- 气象：BOM月统计可读/已捕获；日序列、质量旗标、站迁/测法及共同时间窗尚未准入。无需另建采集系统。
- 蒸发/RH/土壤水分：源目录可以作为候选；本轮没有可与设施配对的全套时间序列。沿用AWRA既有metadata与有限soil evidence，不新增或替换受阻降雨来源。
- 地形/海拔/坡度：GA ELVIS/DEM目录已定位，具体tile、datum、grid、工程surface和提取尚未完成。[GA](https://www.ga.gov.au/scientific-topics/national-location-information/digital-elevation-data)。
- 土壤：CSIRO/TERN Soil and Landscape Grid约90m产品是自然土壤背景，不能当engineered landfill cover、填埋体或塘底泥参数。[CSIRO官方说明](https://www.csiro.au/en/news/All/News/2014/November/Australias-living-skin-bared)。
- 气候区：BOM分类产品与技术说明已定位；具体facility overlay未做，不凭经纬度猜一个Köppen代码。[BOM技术说明](https://www.bom.gov.au/climate/maps/averages/climate-classification/files/climate-classification-maps-technical-details.pdf)。
- 流域：现有HRS410033 station-node-catchment绑定及保存几何可复用；它不是Council边界/设施服务区，Cooma厂点和排放点与流域的join仍UNKNOWN。
- 处理量/排放：没有准入的可比两地逐期tonnage、组成、实际CH4 flux、meter气量、collection/destruction或泄漏数据。旧规划capacity/处置收费/减排新闻不得填进运行量；未发现不能等同公开资料从不存在。

## 研究选择与混杂控制

**建议：Cooma为主背景、Rockhampton为温暖低地背景，设施层保持候选。** 先做已存在同类landfill过程的可得性/测量设计对照；不是把Cooma当冷温度“处理组”、Rockhampton当热温度“实验组”。纬度/海拔仅定位/背景，参数必须来自过程观测或独立校准。

配对前必须核对：废物组成/年龄/填埋历史、fill区大小/深度、覆盖材料与裂隙、含水率/回流、gas wells/抽气/flare运行、测量method/footprint及季节窗口。设施管理的差异足以混杂气候对照，甚至改变净排放方向。现场状态未知时不排序“哪地甲烷更多”。

作为科学机制的澳洲对照，CSIRO/MLA Darling Downs单塘2012–13研究与Victoria2024曝气lagoon研究可用于设计问题；它们不是Cooma/Rockhampton的替代实测，更不建立同类工艺匹配。自然厌氧塘、曝气lagoon、landfill与covered digester各自分组。

## 下一步可执行范围与停止门槛

仅在后续批准后，利用现有工具准备共同时间窗的公开站点背景、明确数据/许可/质量标记和空间层版本，列出设施点/边界及过程变量缺口。原始设施量测不公开时，可以讨论无真实地点外推的合成结构实验，但不能用气候站值替换塘水/填埋体温度来输出真实排放。当前无新GIS平台、无场地接洽、无非公开数据获取、无新碳模拟。
