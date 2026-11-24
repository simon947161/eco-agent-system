# 既有能力复用审计

2026-11-24 · READ_ONLY；确切Git文件内容SHA-256、函数、imports见 [reuse_manifest.json](reuse_manifest.json)。没有下载既有Git仓库之外的原始观测，没有调用科学计算或采集入口。

|资产 / 固定版本|实查接口与兼容性|实际处理|
|---|---|---|
|Hydrology PR129 `987cc1dc7170204e5eab3d1750590ba463ea9d08`|`cczps_lite/qgis_local_spatial_foundation/hydrology_contract.py` / `hydrology_source_registry.json`：GeofabricV3.3、源EPSG4283、目标EPSG7855、图层6/31/33/27、约1:100000基础制图。`hydrology_pack.py`：load_source_registry、_validate_geojson、retrieve、derive、verify等；存在urllib及QGIS依赖|复用来源/CRS/版本分离思想；没有调用retrieve/derive/verify，没有将旧获批extent或服务授权转为新许可。几何不是观测流态|
|CarbonOS PR132 `2ec66ae41ae2e1d4a0f1aaa92aa98c9f0ff4c5b0`|`docs/research/carbonos/batch-d3/DATA_ADMISSION_REPORT.md`及INDEX；D3三候选全部未准入，原件hash=null，HTMLhash不可冒充数据hash|继承许可/原件/时间/QC独立门槛；不复制旧数据、不重试403，不借甲烷计算权限执行WHH|
|甲烷账 PR144 `77a35e2723372a290579e4549a86781e2be65c04`|`docs/tasks/climateos_au_landfill_methane_methods_001/mass_balance.py`：evaluate、generation_from_decomposed_carbon、flow_mass、flux_chamber、operation_hour等|读源码结构和imports，守恒思想可参考；CH4/碳因子/1000t/GWP与水质健康不兼容，NOT_REUSED_NUMERICALLY|
|Evidence PR145 `ae1050a621ac794e447f9ac047865d90b2f04b03`|`docs/tasks/climateos_global_method_evidence_ecochain_001/reviewer.py`：schema_check、check_sources、review、verify_events等；依赖特定CH4账本逻辑|复用证据、主张、缺口、审查者分离思想；不能直接导入作为WHH通用准入器，未复制运行模块|
|main Bondo Evidence Passport|`cczps_lite/contracts/bondo_evidence_passport.schema.json`：claims/supporting_evidence_ids、version_conflicts、gaps、human_review；有项目特定限制|沿用字段语义与人工评审约束，不宣称本包JSON已通过该不同用途schema，不创建新证据平台|
|NatureHash|当前公开README实读，Git blob `9eb5bc0a1ee22141f1058a847c13f6dae6b2ce38`，[入口](https://github.com/simon947161/naturehash-lab/blob/main/README.md)|v0.1概念研究，明确不是完成密码算法。空间/时间/观测/治理语境可借鉴；运行接口与代码许可REUSE_UNVERIFIED，因此只引用，不移植|
|EcoChain|精确PR145 `EXISTING_ECOCHAIN_AUDIT.md` / `ECOCHAIN_INTEGRATION_STATUS.md`；main的SYSTEM_RELATIONSHIP_MAP也区分证据层与治理权威|历史审计为ECOCHAIN_CANONICAL_NOT_FOUND，本轮未新搜私人库或宣布全局不存在；保留PENDING_CANONICAL_ECOCHAIN_INTEGRATION，未建立替代主库或签发权|
|已有双向交接|PR142产生、在上述PR145固定树可读的 `docs/tasks/climateos_client_ai_science_integration_001/HANDOFF_PROTOCOL.md`|Founder提示触发的读取/回执/评审可复用；没有已核实后台订阅机制。本次直接主机接收已真实ACK，自动队列仍DELIVERY_CHANNEL_UNVERIFIED|

仓库根LICENSE为MIT。该软件许可不覆盖第三方数据、论文、照片、NatureHash其他仓库或监管授权。未把本轮9个门户复制成新数据库；仅编写小型可审元数据登记与一次性离线验证。

现有主分支未包含这些未合并研究分支的全部运行实现，故按精确提交链接，不cherry-pick。现有任务索引保持不变，本包UNIFIED_TASK_INDEX作为唯一新增总入口，链接已有CarbonOS索引与AWT停止结论。
