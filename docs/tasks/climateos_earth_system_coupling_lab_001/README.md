# Earth System Coupling Lab — Issue #150

从[中文Founder报告](FOUNDER_REPORT_ZH.md)和[12页离线展示](slides.html)开始。所有局地计算为声明合成模型；正式科学准入PENDING。

|研究索引|内容|
|---|---|
|[唯一任务书](TASKBOOK_ZH.md)、[复用审计](REUSE_AUDIT.md)|父PR149、旧架构与真实能力|
|[方法研究](MECHANISM_RESEARCH.md)、[来源登记](SOURCE_REGISTER.json)|官方方法、版权与反证|
|[状态模式](SHARED_STATE_SCHEMA.json)、[接口](MODEL_INTERFACE.md)、[耦合设计](COUPLER_DESIGN.md)|真实源码入口与限制|
|[公式和假设](NUMERICAL_METHODS_AND_ASSUMPTIONS.md)、[实验矩阵](EXPERIMENT_MATRIX.md)|物理量、设计、参数与预注册|
|[主批结果](EXPERIMENT_RESULTS.json)、[分类表](summary.csv)、[诊断](evidence/diagnostics.json)|10008实际记录、完整轨迹与联合反例|
|[失败](COUNTEREVIDENCE_AND_FAILURES.md)、[权利](DATA_AND_MODEL_RIGHTS.md)、[科学门](PHYSICAL_AND_STATISTICAL_GATES.md)|拒绝、许可与UNKNOWN|
|[QA](QA_AND_VALIDATION.md)、[治理交接](CCZPS_ECOCHAIN_HANDOFF.md)|测试、hash、决策边界|
|[交接协议](CRP_HANDOFF.md)、[下次入口](NEXT_SESSION.md)|精确R/D见HANDOFF_STATUS.json|

源码：仓库cczps_lite/integration/earth_system_coupling；测试：tests/test_earth_system_coupling.py。无需安装依赖。运行入口见MODEL_INTERFACE.md。仅独立Draft PR，未合并/部署，未触碰私人EcoEngine v200。
