# 实际复用台账

|分类|资产|实际使用/边界|
|---|---|---|
|REUSE_NOW|integration/dynamic_quantification.py及旧NOAA归档|execute实际调用原有run_agent，后者调用meteorology_connector；原始字节单份，原代码不改|
|REUSE_NOW|GitHub任务目录/精确SHA/评审回执模式|沿用PR140/141流程，新建本任务入口和机器交接合同|
|ADAPT_MINIMALLY|client_ai_evidence.py|只加闭集路由、固定文件信任根、相态和租户模拟策略，输出单点GeoJSON|
|RESEARCH_ONLY|physics_validation P1–P4、PR139/140/141|审计及P1参考回归；不进入排放或高度试算|
|RESEARCH_ONLY|QGIS地形水文、EcoEngine天气|读取实现/契约并跑离线契约测试；未加载现场/私有数据，未重建GIS或启动预测|
|RESEARCH_ONLY|Bondo Passport、Atlas快照|复用证据设计思想；本slice没有调用Bondo或Atlas运行时，不虚称集成|
|RESEARCH_ONLY|Kitty/Harness/Mission Control|文档与规则代理可审计，未验证主动投递/接单运行时|
|DO_NOT_BUILD|新GIS/数据库/气候模型/门户/生成式服务|无本轮必要性或授权；无Senversa私有连接器|

新增只有一个task目录、一个小型integration模块和一份测试。未改冻结核心、旧科学结果、其他PR或服务配置。资源记录来自一次execute调用，依赖Python标准库+本仓库；硬件成本、开发总耗时、规模性能、效率改善均UNKNOWN。
