# 气候引导发展智能体：填埋场与污水设施真实空间证据续作

2026-11-05 UTC；接续同一总任务 CLIMATEOS-DYNAMIC-QUANT-001。父基线为 PR #135 的 `2dea3defbb843cfcd8792751ffc21f31fa241616`；隔离分支 `research/climateos-facility-evidence-002`。本轮完成可执行的小型真实空间案例，部署仍未完成。

## 实际成果

复用 Task2041–2050 的 Cooma 范围常量、原主机已经下载的 Geofabric V3.3 河网及既有 10km 研究多边形。新增一个小型离线设施证据接入口，没有新建平台或改动 no-run 科学合同。通过 GA 官方服务有界查询取得 5 条垃圾设施和 1 条污水处理设施记录，保存原始响应、查询 URL、UTC 获取时间、SHA-256、原字段和元数据。获取时间不是设施测量时间。

|提供方记录|资料类别|既有研究多边形内|距归档最近水系线的平面距离（约米）|
|---|---|---|---|
|COLES SUPERMARKET|软塑料投放点|是|265|
|COOMA SCRAPMART|reuse shop|是|655|
|COOMA LANDFILL|易腐垃圾填埋场|是|655|
|WOOLWORTHS SUPERMARKET|软塑料投放点|是|90|
|COOMA COMPOSTING FACILITY|有机物回收设施|是|655|
|The Glen|污水处理厂|是|43|

填埋场、reuse shop、堆肥设施的注册点完全重合：保留三种功能记录，但不能将它们当作三个独立坐标场址。两个超市记录也不能算填埋场。Operational 是提供方注册属性，不是本轮现场确认；软塑料业务是否仍实际开展没有复核。

距离是 EPSG:7855 下点到归档线的二维欧氏距离，四舍五入到米不代表米级准确性。点不等于设施边界、出水口或排放源；线也不等于同期流水。没有判断下游关系、水力连接、污染暴露、受纳水体或甲烷源强。本轮仅用河网几何，未把河网属性的流向当作真实输送模型。

## 时间、坐标与科学边界

GA 查询输入范围为 WGS84，输出为 GDA2020 EPSG:7844。河网档案为 GDA94 EPSG:4283，研究多边形为 MGA2020 zone 55 EPSG:7855。实际用既有 PyProj 3.7.2 / PROJ 9.8.1 转至 EPSG:7855，关闭网络格网下载，禁止 ballpark 转换；转换名称和软件提供的 accuracy 字段归档。accuracy=-1 是未知，0.01 是坐标操作元数据，二者都不是地图或设施位置精度证明。原始空间 confidence 代码保留，没有自行转成概率。

废物数据产品有 2025 年修订记录；污水产品有 2026 年更新声明。污水记录的 feature_source_date 和 attribute_source_date 是不同资料字段，不应当作同一天的设施观测。Geofabric 是静态制图资料。未建立共同观测时窗，故拒绝跨源时间趋势、气象驱动、因果与效果比较；没有把 NOAA 纽约三日数据拼接进 Cooma。

历史 Task1200–1499 为模型评价路线，Task1500–1700 保留跨尺度科学路线。PR135 复核确认的 EnergyPlus 风驱动、WRF、PALM、HYSPLIT、UniCM/NeuralGCM 是方法和研究依据；本轮没有运行这些求解器。`environmental_coupling.py` 的合成关系校验和 `mechanism_return_gate.py` 的 no-run 边界未改变。D3 仍 DATA_NOT_READY；没有重试被拒的气体下载，也没有排放/GWP/减排信用结果。

## 核查与验证

- 新接入口及既有动态量化定向测试：10 tests，全部通过。包括真实归档回放、共址记录、截断/提供方错误、错误 CRS、无穷/缺失/布尔坐标、越界和重复 ID 拒绝。
- 完整测试：492 tests，OK，1 skipped（Windows 符号链接）。首次沙箱执行有 8 个本机 HTTP socket WinError10013；在获准的扩大执行环境重跑通过，未改测试或服务配置。
- 空间脚本首轮拒绝不同 CRS 名称表达（EPSG:4283 与 URN）；修正为 PyProj 标准 CRS 等价比较后实际执行成功。显式设置本次进程 PROJ_DATA，未改全局配置。
- 既有测试生成的四个输出文件已还原，未作为本轮成果提交。空间层只复制到隔离工作区的 git-ignored runtime_data，不改原主机 QGIS 工程或原始层。

证据：[原始响应与收据](facility_evidence/receipts.json)、[设施离线回放](facility_evidence/actual-facility-replay.json)、[实际空间比较](facility_evidence/spatial-comparison.json)。本地原水系和多边形的 SHA 已固定；不随本 PR 重分发，因此全新机器需要同字节的既有本地层才能重跑空间比较。设施回放和单元测试独立于 GIS 依赖。

运行：`python -m cczps_lite.integration.facility_spatial_evidence`；`python -m unittest tests.test_facility_spatial_evidence tests.test_dynamic_quantification -v`。空间比较使用既有 `D:/apps/Python312/python.exe compare_facility_spatial.py`，本次进程环境 `PROJ_DATA=D:/share/proj`、`PROJ_NETWORK=OFF`；输入放 `runtime_data/facility_spatial/`，文件名和 SHA 见实际比较 JSON。缺文件、错误 CRS 或字节变化均拒绝执行。

## MatrixOne 与主机状态

电脑画面入口 `cua.getState()` 等待 300 秒后超时，未取得页面状态，无法确认当前登录、余额、资源、模型或部署。没有创建密钥、上传项目、充值、下单或调用付费模型。MatrixOne 保持 NOT_BENCHMARKED；无需用户再次粘贴任务书或发送密钥。之后需恢复电脑控制连接，再只读检查已登录工作区和报价；旧 Genesis 免费时段不作为依据。

本轮发现 `D:/eco_engine_v200`、`D:/EcoEngine` 和原 QGIS 层确实存在，与旧报告另一环境的 Test-Path=False 不同。目录存在不等于进程、调度器或采集任务正在运行；本轮不宣称四站采集已验证。进程查询未返回可用的目标状态，也未重启任何服务。

已读取本机 Codex AGENTS、仓库指导及外部记忆 context-load；记忆中 ClimateOS 项目状态文件缺失，不补造。Simon Memory 写回需保持项目证据优先；本轮在当前工作区留下待协调记录，不修改原记忆库或 Founder Decisions。

## 下一步与交接

1. 将本次设施证据能力纳入现有智能体工具编排，并以真实设施身份和来源日期核查作为下一考核题；当前仍是确定性工具，不声称 LLM 智能体团上线。
2. 优先取得公开且有许可的设施边界、出水口、运行数据或同期气体观测，独立核验设施身份。具备资料后再选水处理/气体方法；不先安装全部物理模型。
3. 恢复 MatrixOne 只读界面，评估工作区、工具调用、运行环境、导出及预算；未知成本、密钥创建、持久权限扩张仍暂停。

发布状态：本地实现与提交已完成。`git push -u origin research/climateos-facility-evidence-002` 被自动审批拒绝且未执行；理由是远程发布需要更明确的用户授权。随后读取用户历史，未取得实质新增发布授权，因此没有重试、没有创建远程分支或新 PR，也没有改用连接器绕过。可审查补丁和 PR 草稿说明保存在当前任务的 review 目录。

知识：注册点、实际设施、出水口、排放源是不同对象。决定：先复用现有空间底座做真实位置证据。风险：共址误计、注册时效、坐标误认、地图邻近被误作输送。开放问题：同期观测、设施边界与 MatrixOne 运行条件。关键词：ClimateOS、Cooma、landfill、wastewater、Geofabric、methane、MatrixOne。

## 公开来源与许可

- [GA Waste Management Facilities 官方图层](https://services.ga.gov.au/gis/rest/services/Waste_Management_Facilities/MapServer/0)，原始响应归档。
- [GA 产品目录及许可](https://ecat.ga.gov.au/geonetwork/srv/api/records/495820b9-4a56-4409-9d1b-950589b50936?language=eng)：CC BY 4.0；含 G-NAF 来源附加署名说明。本次查询排除地址/G-NAF 字段。© Commonwealth of Australia (Geoscience Australia) 2025；产品贡献方 Australian Government Department of Fisheries and Forestry（原 DAWE）；Incorporates or developed using G-NAF © Geoscape Australia, licensed by the Commonwealth under the Open G-NAF EULA。
- [GA Wastewater Treatment Facilities 官方图层](https://services.ga.gov.au/gis/rest/services/Wastewater_Treatment_Facilities/MapServer/0)：© Commonwealth of Australia (Geoscience Australia) 2026，CC BY 4.0。
- 本地河网沿用既有 Geofabric V3.3，© Commonwealth of Australia (Bureau of Meteorology) 2022，CC BY 4.0。新脚本导出的结果为加工结果，不是提供方原结论，不暗示官方认可。
