# 科学与工程能力现实矩阵

除另列版本外，仓库源码均固定于 PR141 e25ffe3e34829d9146628a7c72a363c35d8ec151（本任务未改旧代码），SHA清单见evidence/manifest.json。N=本轮执行；H=历史归档声明；R=源码/文档只读检查。实际运行证据与未来复现入口分列，不暗示所有命令本轮执行。

|能力 / 路径|输入→输出；物理边界|运行、测试/CI及复现入口|依赖、许可/访问|成熟度/外部采用|
|---|---|---|---|---|
|P1 `cczps_lite/integration/physics_validation.py`|干摩尔分数/P/T/水汽→浓度/参考体积；理想气体，非源强|N 8 GasTests通过；`python -m unittest tests.test_physics_validation.GasTests`；CI历史PR138评论|stdlib；仓库代码权限不等于数据/科学准入|IMPLEMENTED_SYNTHETIC_TESTED；采用UNKNOWN|
|P2 同文件 storage_run|假设容器库存/阀门→合成时间序列；非真实塘/填埋场|H PR138合成测试；复现入口StorageTests，**本轮不运行**|stdlib；参数无现场许可/校准证据|IMPLEMENTED_SYNTHETIC_TESTED；UNKNOWN|
|P3/P4 同文件|FOD年度库存及假设温湿响应；不是正式AWT修正|H PR138 README/测试；`tests/test_physics_validation.py` 对应类仅审阅，未来须授权运行|stdlib；现场参数/法定采用无证据|IMPLEMENTED_SYNTHETIC_TESTED；UNKNOWN|
|PR139 `docs/tasks/climateos_local_case_method_intake_001/validate_intake.py`|Zenodo17718964 v1 CCBY4.0 Excel水相CH4/流量→结构QA；非气相/排放|H evidence/test-run.txt、offline-retest.txt；命令入口validate_intake.py（须原ZIP）；本轮未重取/重算|openpyxl、原始ZIP；原始字节位于旧外部runtime_data，不保证新checkout可跑|REAL_DATA_STRUCTURAL_QC；UNKNOWN|
|PR140 `docs/tasks/climateos_methane_factor_order_001/audit_observations.py`|NOAA BRW→3340结构配对/0科学配对|H README/test_audit.py/评审回执；复现入口test_audit.py，原ZIP前置，未重下载|stdlib及README数据合同；NOAA具体receipt权利范围，不能泛化|REAL_DATA_STRUCTURAL_QC；NO_VALID_PAIR；UNKNOWN|
|PR141 `docs/tasks/climateos_spatial_ghg_hypothesis_validation_001/audit_profile.py`|AirCore L2与气象→元数据闸门；非因果高度效应|H 5审计+8P1测试见回执；test_audit_profile.py；未独立重跑ZIP|按该目录来源/许可账本；版本尺度/垂直datum未齐|REAL_DATA_STRUCTURAL_QC；NO_VALID_VERTICAL_PROFILE；UNKNOWN|
|天气原型 `cczps_lite/integration/dynamic_quantification.py`|NOAA三日→描述均值/质量/来源|N 5回归+新11测试、run_pilot.py真实运行|stdlib；NOAA US public domain限定，详PILOT；离线|REAL_DATA_STRUCTURAL_QC；无客户采用|
|EcoEngine bridge `cczps_lite/integration/ecoengine_v192b_adapter.py`|本地类EcoEngine JSON→内部字段；不连EcoEngine或GIS|R源码与tests/test_ecoengine_v192b_bridge.py；复现`python -m unittest tests.test_ecoengine_v192b_bridge`未在本轮执行|stdlib；合成/本地记录许可逐条核实|IMPLEMENTED_SYNTHETIC_TESTED（历史）；UNKNOWN|
|`D:/eco_engine_v200/weather_client.py`|Open-Meteo forecast/modelled current→WeatherBundle；不是官方站原始观测|R实际源码SHA见external-source-audit；run_validation.py是合成场景，**未执行**|stdlib/network；外部API商业许可本轮未准入|CONCEPT（当前科学交付等级；源码已实现但本轮运行UNKNOWN）；采用UNKNOWN|
|`D:/EcoEngine/four_site_weather/collect_four_site_weather.py`|公开天气预测/模型当前值→CSV历史归档|R源码及2026-09-29审计：108模型当前行、756预测行是旧报告数，不是本次全量盘点；未跑采集|stdlib/network；当前scheduler/live status UNKNOWN|CONCEPT（本次科学等级）；历史工程运行有本地报告，独立观测准入无|
|QGIS `cczps_lite/qgis_local_spatial_foundation/`|workspace/project_builder合成教学层；terrain/hydrology契约分离位置、地形、流域|N 基础20+水文29契约测试；`python -m unittest tests.test_qgis_local_spatial_foundation tests.test_qgis_cooma_hydrology_pack`；terrain_pack.py代码仅R|合约tests标准库；真项目需QGIS/PyQGIS；水文GeofabricV3.3CCBY4.0、源EPSG4283/项目7855；不重试接口|IMPLEMENTED_SYNTHETIC_TESTED（本轮契约层），真实GIS显示/模型未复验；UNKNOWN|
|Public Strategy Atlas `apps/public-strategy-atlas/README.md`、`verify-snapshot.cjs`（仅PR130分支）|公开策略快照/哈希→一致性检验；非法规意见|R exact e3d8f074e0e1ba5e9614c3f4c5a2b973746b2ab7；verify-snapshot blob39ee3c9250ac4a6be0bdb86258df0142c713d29a；命令node verify-snapshot.cjs FILE.json [expected]未运行|Node、该分支数据许可；私站未访问；README称privatev8，PRbodyv4版本差异|IMPLEMENTED_SYNTHETIC_TESTED（历史README收据）；owner trial≠PRODUCTION_ADOPTED；UNKNOWN|
|Evidence `cczps_lite/engine/evidence_traceability.py`、`integration/bondo_passport_ledger.py`|静态证据→trace/状态/手动哈希链；不评分或通知|N Bondo8测试；`python -m unittest tests.test_bondo_passport_ledger`；traceability代码R|stdlib；仅repo静态/合成许可|IMPLEMENTED_SYNTHETIC_TESTED；UNKNOWN|
|Agents `eco_agent_system/agents/`、`orchestrator/orchestrator.py`|JSON→顺序调用固定规则代理；默认缺值为0可能掩盖缺失，不用于本slice|R planning_agent和orchestrator；run_simple_check.py只是原演示入口，未执行|stdlib/localJSON；非LLM专业判断许可|CONCEPT（科学能力）；源码IMPLEMENTED；UNKNOWN|
|Harness/Mission Control `docs/mission-control/research/grok-build/CLIMATEOS_EXISTING_CAPABILITY_CROSSWALK_V0.1.md`|研究工作流→RFC映射|R文档自标RFC-ONLY、DOCUMENTED_PATTERN/PARTIAL；无可证明收发运行命令|文档；无客户数据输入|CONCEPT；自动接单UNKNOWN|
|Kitty `docs/context-packets/2026-09-28_ECOENGINE_CLIMATEOS_CODEX_KITTY_DISPATCH.md`|任务书/issue指令→待主机验证|R自标HOST EXECUTION NOT YET VERIFIED；未运行Task Scheduler/Kitty|主机授权依赖，不新增权限|CONCEPT（本次连接能力）；UNKNOWN|
|GitHub Evidence Reader / Founder Cockpit|本分支扫描未找到可确认的同名读写服务接口；Atlas相关文档不等于本分支实现|UNKNOWN；复现rg文件名/源码搜索，不声称全组织不存在|未来只读adapter、无新服务|CONCEPT；UNKNOWN|

成熟度阶梯：CONCEPT；IMPLEMENTED_SYNTHETIC_TESTED；REAL_DATA_STRUCTURAL_QC；SCIENTIFICALLY_VALIDATED；PRODUCTION_ADOPTED。这是按当前可交付科学证据保守分级，不否认源码存在。后两级本审计没有足够证据授予任何能力。CI历史与本次分开，当前结果以新PR workflow记录为准。

当前主机EcoEngine路径存在，推翻旧主机“不存在”快照。四站旧审计明确293占位行、245硬编码合成行和14预测有效日不得混成观测；本轮只审阅这份报告，不重做全盘恢复，不发布内部路径里的原始数据。许可/生产状态未知不通过补默认值解决。
