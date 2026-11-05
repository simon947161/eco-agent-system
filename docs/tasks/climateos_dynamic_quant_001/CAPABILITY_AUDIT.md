# 有界能力审计

2026-11-05；代码基线main `9eb7577e145e76161f9f1cd8509348b19c2904cc`。只读跨PR，不拼接或覆盖未合并成果。DOCUMENTED、IMPLEMENTED、TESTED、RUNNING、SCIENTIFICALLY_VALIDATED是不同证据轴；RUNNING在本表指本轮观察到执行，不表示常驻运行；“未建立”不表示外部一定不存在。范围以唯一任务书为准，不全盘重做多年科学审查。

|模块及可复核路径|实现、入口和依赖|测试/运行证据及综合状态|科学上限|
|---|---|---|---|
|历史Core Alpha `docs/climateos-core-alpha-status.md`|文档记录2026-06-02在D:\\eco_engine_v200运行run_validation.py，分类/风险/报告；不是本轮观测|历史文档有运行记载；本轮目录Test-Path=False，当前运行BLOCKED/UNKNOWN|软件validation输出不等于独立实测科学验证，不把历史Alpha降成纯设计，也不宣称当前运行|
|EcoEngine桥 `cczps_lite/integration/ecoengine_v192b_adapter.py`|本地JSON字段映射；没有import真实EcoEngine、GIS或live服务|IMPLEMENTED；`tests/test_ecoengine_v192b_bridge.py`；测试结果见执行报告，IMPLEMENTED_AND_TESTED|兼容映射不是EcoEngine物理验证|
|四场景/多地点气象 `cczps_lite/engine/meteorology_connector.py`, `meteorology_runtime.py`, `location_meteorology_pipeline.py`|配置Batlow/Kunlun/Iraq/Xiong'an；下载NASA、缓存/时序/阈值趋势；网络与预算约束|IMPLEMENTED_AND_TESTED，相关meteorology测试；新真实回放单列|来源名不能把网格变站点；短期阈值不是气候趋势归因|
|旧主机四站 `D:\EcoEngine`，任务上下文 `docs/context-packets/2026-09-28_ECOENGINE_CLIMATEOS_CODEX_KITTY_DISPATCH.md`|既有Issue122要求检查采集及调度器；配置场景与真正站点不是一回事|本轮Test-Path=False；BLOCKED/当前运行UNKNOWN；没有启动或修改调度器|不宣称四站仍持续采集，历史任务书不是当日运行证据|
|风场/顺风追索 `docs/tasks/task1500_1700_environmental_coupling_layer/SCALE_AWARE_WIND_CLAIM_EVIDENCE_PROTOCOL_V0_1.md`、Bondo/Tumut测量协议/站点资格表|高度、时窗、代表性、证据门；已有小样本报告可检索|DOCUMENTED协议与历史研究；本轮未重算三维风场，IMPLEMENTED_NOT_VALIDATED作为总体边界|日阵风/9点15点/单点风不能生成连续三维风或甲烷源强|
|甲烷D1/P1-A及D3；PR132 `2ec66ae41ae2e1d4a0f1aaa92aa98c9f0ff4c5b0` 的 `docs/research/carbonos/NEXT_SESSION.md`|三个候选已耗尽，原气体文件0；方法科学审查PENDING|BLOCKED/DATA_NOT_READY；未重试、未运行反演|没有可确认的排放/GWP/年化结果，代码或方法草案不能填补数据门|
|GIS `cczps_lite/qgis_local_spatial_foundation/` project_builder/terrain/hydrology/integrated packs|既有契约、注册表、QGIS项目构建与图层路径；需要QGIS及本地栅格运行|IMPLEMENTED_AND_TESTED软件契约；`tests/test_qgis_*`；本轮未打开QGIS项目|Task2061已确认SPATIAL_ORIENTATION_READY / ENVIRONMENTAL_CONCLUSIONS_NOT_ESTABLISHED；不是水量/火险求解器|
|水文/生态/土地模块；Task2061闭合清单与本轮科学分解|既有地形与水系证据可供上下文；独立过程模型及同期观测仍需准入|IMPLEMENTED_NOT_VALIDATED/RESEARCH_CANDIDATE|地图连通性不是流量、热量或生态改善|
|Atlas PR130 `e3d8f074e0e1ba5e9614c3f4c5a2b973746b2ab7`|未合并网页开发；本轮只读PR身份|不在main执行，当前线上状态UNKNOWN|界面展示不升级科学证据；本轮不改界面|
|生态信用PR133 `813eb2571c5605a5aafaf754e71c7ed545fdac18` / PR134 `1070fa5578375be8f042bd84ff084919fa6dc566`|基础与科学法律研究；保留ADMITTED WITH GAPS及后续限定；相关NEXT_SESSION保留原分支|DOCUMENTED_ONLY知识；未部署计算器|生态调查/VI不等于BAM-C法定信用；法律/模板缺口不由气象工具弥补|
|ACCU/AWTM与生态市场|既有研究与制度概念；本轮未重新核查全部资格/最新规则|DOCUMENTED_ONLY，本轮法规模块NOT_ASSESSED|不得混用吨CO2e、生态信用、垃圾处理量或市场价；AWTM身份和适用方法须独立核实|
|Harness/Mission Control `docs/mission-control/research/grok-build/CLIMATEOS_EXISTING_CAPABILITY_CROSSWALK_V0.1.md`|ACTP/handoff、来源与模型注册、checkpoint文档模式；MCP列PLANNED|DOCUMENTED_PATTERN/PARTIAL；不宣称通用服务已建成|治理格式不是验证过的专业智能体|
|DeepSeek `docs/reviews/DEEPSEEK_WEEKEND_REVIEW_EXTREME_EVENT_COMPLIANCE_RESILIENCE_2026-08-23.md`；KITTY上述dispatch|研究/协调意向及主机任务；旧dispatch明确HOST EXECUTION NOT YET VERIFIED|DOCUMENTED_ONLY；本轮没有连接其API或验证远端进程|不把任务派发当执行，不把模型名称当科学资质|
|新Environmental Evidence Agent v0.1 `cczps_lite/integration/dynamic_quantification.py`|一个控制器、六函数、五步实际路径；复用parse_observation，无网络和新依赖|本轮真实站点回放RUNNING（单次）；IMPLEMENTED_AND_TESTED|SCIENTIFICALLY_VALIDATED未建立；描述统计，不是完整耦合模型|
|MatrixOne|官方README/许可/GIS文档索引；无本地实例与账号操作|RESEARCH_CANDIDATE / NOT_BENCHMARKED|存储查询与向量检索不能代替物理/法定验证|

关键发现：NASA现有fetch没有time-standard参数，parse_nasa_power_daily却加UTC日期标签；官方默认LST，存在日界误标风险。本轮隔离回放不走该下载解析路径，未改旧函数以免扩大回归范围。旧connector还会将naive时间视UTC，并接受float的NaN/Inf；新门拒绝非有限值，不给NOAA日期制造UTC时刻。未来统一旧源适配必须先修复这些语义与回归用例，再接自动化。

未证明：旧主机常驻运行、QGIS图层本轮渲染、Atlas部署、通用LLM/MCP、独立生态/热/水文/甲烷耦合验证。检索到的本地历史目录若不在main Git跟踪，不能当作main已接纳成果。执行与测试不跨越这些边界。
