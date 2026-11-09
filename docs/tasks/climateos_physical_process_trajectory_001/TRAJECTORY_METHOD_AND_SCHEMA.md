# 轨迹方法与字段

任务局部投影版本 `physical-trajectory/1`，不是 Evidence Passport、CCZPS 或 Public Strategy Atlas 的替代规范。机器记录见 [TRAJECTORIES.json](TRAJECTORIES.json)，语义检查在 [薄适配器](../../../cczps_lite/integration/physical_process_trajectory.py)。

每段固定包含任务书全部24字段，并加 `from_node`、`edge_type`。量、单位、相态、时空支持、边界、来源版本及定位、许可、输入/输出、残差、反证、校准、模型验证、缺口均显式保存。`null` 表示没有数值，不能当0；`next_missing_input` 描述最小补齐条件。

| 信息类别 | 本包解释 |
|---|---|
| 观测 | NOAA公布的网络聚合丰度、重建SST指数；HRS继承记录，不冒充本轮独立测量 |
| 假设 | 合成水量、误差独立性、块平稳性、二元评分规则，逐项标注 |
| 解释 | 文献机制与受限样本统计，不能自动作为因果结论 |
| 预测 | 本轮没有新预测；BoM页面的预测段落不进入历史数据 |
| 建议 | 最小下一输入，须待评审和授权 |

状态白名单：EXACT_PHYSICS_CALCULABLE、OPEN_DATA_RECALCULATED、SYNTHETIC_TESTED、CONDITIONAL_STATISTICAL_ESTIMATE、STRUCTURAL_QC_ONLY、BLOCKED_MISSING_DATA、BLOCKED_MODEL_VALIDATION、NOT_INFERABLE。数学规律可成立而输入仍是合成，所以A2标SYNTHETIC_TESTED，不把其整段标成现场可算。

边白名单遵循任务书七类。顺序边只表示研究推进；**A3采用独立全球输入，不是把A2局地浓度传入全球公式；C3是Cooma审计旁例，不是尼罗河下游节点**。`trace()`附带原Atlas拓扑，但不将定性路径解释为数值依赖DAG。B1机制反馈与B3统计关系分开，不对反馈环做无验证迭代。

预先登记见 [ANALYSIS_PROTOCOL.json](ANALYSIS_PROTOCOL.json)：三轨迹、10个新增主要来源主题；A/B/C数据候选分别1/2/1，无新增GIS。B候选2未取得资料后按预设回退做指数持续性；不是挑选一个显著区域或窗口。完整数据权限、失败和原始哈希分别见 [来源](SOURCES.json)、[下载收据](evidence/acquisition.json)、[访问限制](evidence/access-limits.json)。

实施澄清（不覆盖冻结协议）：三节点例子有两条共享内部流量q12/q23；协议中单数“one shared internal flow”指共享变量原则，实际扩为三节点所需的两条，全部保留同变量协方差。BoM许可复核确认研究用途获允许，实际阻塞是未取得payload；不将原先较保守的“开放再发布待核”误写为研究被禁止。没有更改数值窗口、阈值、种子或挑选结果。

接口仅接受固定example、版本、授权与范围四项；额外政策分数、自由来源、任意公式、预报或认证字段被拒绝。哈希验证的信任锚是本次Git树，**不是外部签名或法定证据认证**。
