# 既有能力与复用审计

唯一任务书为本目录 TASKBOOK_ZH.md，初始任务提交 c18ffaae0928de044e1a2442e53fd61e1c26299d；科学父为 PR149 D `ea6fd79b41138cbcb16f9bd1aadd68f6a4b771df`。以下旧文件均按此父树读取，未修改。逐文件 Git blob 见 evidence/reuse-blobs.json。

| 权威路径／函数 | 已有能力与真实状态 | 本次处理 |
|---|---|---|
| docs/00_MASTER_ARCHITECTURE/SYSTEM_RELATIONSHIP_MAP.md | 环境运行、可能性比较、制度翻译、证据历史、人类治理分层 | 保留顺序，新增运行层不成为审批者 |
| docs/00_MASTER_ARCHITECTURE/ECOENGINE_V2_SYSTEM_DEFINITION.md | v0.1架构定义，模型后果不等于公共价值 | 复用边界，不称旧运行时已实现新耦合 |
| docs/00_MASTER_ARCHITECTURE/CCZPS_LITE_V0_4_REVIEW.md | 小型演示与完整科学系统有距离 | 原分数模块保持原适用域 |
| docs/03_RUNTIME_LAYER/DIFFERENTIAL_FIELD_INFERENCE.md | 时空、地形、历史、环境邻近的差异推断，候选机制需验证 | 区分作者语义与数学算子，不发明唯一“差点法” |
| docs/03_RUNTIME_LAYER/FORCING_LAYER.md | 气候、地形、植被、水文、人类等候选强迫 | 定性关系不自动成为有单位的源项 |
| docs/02_GOVERNANCE_LAYER/POSSIBILITY_COMPUTING_FRAMEWORK.md | 多未来与取舍、人类选择 | 接收带边界的情景结果，不授予决策权 |
| docs/02_GOVERNANCE_LAYER/CLIMATE_ZONAL_RESPONSIBILITY_METHOD.md | 分区治理与责任概念 | 国界不替代物理网格，未找到可直接复用的时空积分求解器 |
| docs/architecture/climateos_v2_review/02_V1_CAPABILITY_AND_DEBT_MAP.md | 时间窗口评估与GIS基础，未形成运行中的多物理耦合 | 沿原目录增量，不新建GIS/数据库 |
| cczps_lite/engine/differential_field.py::calculate_gradient, derive_differential_field | 情景分数相减／上下文均值，非有单位空间梯度 | 完全保留；新算子用K/m、K/s、W/m² |
| cczps_lite/engine/forcing_layer.py::derive_forcing_candidates | 规则候选标签，非动力学力 | 不直接作为物理源项 |
| cczps_lite/integration/environmental_coupling.py | 静态合成关系图，model_executed=false约束 | 保留该旧契约；新运行时独立命名空间 |
| cczps_lite/integration/ecoengine_v192b_adapter.py::map_ecoengine_to_runtime_fields | 仓库公开薄适配器，不能证明源模型正确 | 可作为后续证据投递接口，不加载任何私人旧系统 |
| cczps_lite/integration/physical_process_trajectory.py::ch4_erf, phase, parse_roni, radiation, water_balance | PR147全球CH4函数、60年RONI、理想水账 | 实际调用原全球函数和RONI解析；不引入局地因果边 |
| cczps_lite/integration/multisource_data_admission.py::verify | PR149观测输入及结果完整性 | 只读校验、读取既有衍生统计，不复制三份原始CSV |
| cczps_lite/integration/physics_validation.py::storage_run, fod_run | PR143/144物料账、公式与合成验证 | 旧测试回归；不重写、不提高科学准入 |
| cczps_lite/integration/global_natural_systems_atlas.py | PR146可查询关系图及证据等级 | 保留候选关系与已计算关系的区别 |
| cczps_lite/integration/dynamic_quantification.py | 六工具研究契约、证据准入与拒绝 | 复用人工决策门，不建立另一套智能体基础设施 |
| docs/tasks/task2021_2030*、task2031_2040*（见blob清单） | 历史GIS/QGIS/地形成果 | 仅公共仓库记录；本轮小矩形网格不冒充真实流域 |

新增能力在 `cczps_lite/integration/earth_system_coupling/`：state为共享语义/保守映射；models为四类组件与水热交换；ports为统一step(dt)适配；diagnostics为差分/扰动/反证；experiments为有界运行器。原任务 #150 云端声称的 d7445cd214a9b41e29ca55407790de9118d280e8 不在本地可取得Git对象中，本次没有据其声称的3403次失败复制结论。当前实际结果独立产生、完整归档。

私人 EcoEngine v200：**未读取、未搜索目录内容、未导入、未复制、未上传**。本任务只建立后续独立研究入口，不以私人旧代码填补主线。
