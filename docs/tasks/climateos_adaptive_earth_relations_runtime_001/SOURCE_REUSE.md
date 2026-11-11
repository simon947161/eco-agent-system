# 来源与复用

父PR152固定HEAD `cf91e4a061341bc33d16400bcf4c6a2c2817aa65`；工作任务书提交`274f4d20f2049413cb87be7c31e6477aa08a1ebf`。

|来源|实际复用|边界|
|---|---|---|
|`earth_system_coupling/state.py`|原Field、State、Grid、TimeSupport、单位/缺测/时空门、checkpoint|未另建环境状态存储|
|`models.py`|原Atmosphere、Surface、fluxes、advance固定点、双边水焓账、context_state|仅advance增加可选mapper参数和调用点；默认映射与所有公式不变|
|`ports.py`|实际ModelPort.step提案驱动；每次迭代恢复旧clock|只有耦合器在收敛后提交库存|
|`diagnostics.py`|原联合阈值含义、Ce×U不可辨识反例|不提升为自然因果|
|PR147 / PR149已存公共结果|全球ERF与季节ENSO独立端口，保留原空间/时间支撑|不抓取新数据，不转成局地强迫|
|`docs/00_MASTER_ARCHITECTURE/SYSTEM_RELATIONSHIP_MAP.md`|运行、解释与人类治理职责分离|不新建治理/认证基础设施|

原父分支及所有旧研究工件保持原样。当前分支的`models.py`增量不是宣称父工件hash未变；原始hash见父PR152固定结果，历史实现hash见RESULTS.json；本次修复hash见evidence/review_closure.json。26项新增测试中，原advance默认路径和真实端口映射在相同输入下逐字段完全一致。没有读取PR153之外的私人资产，也没有借用私人实现。

公开技术资料（2026-11-11查阅；仅用于机制设计，不宣称实现标准认证）：
- [CSDMS BMI](https://csdms.colorado.edu/wiki/BMI)：明确组件时间、变量与单位接口。
- [preCICE隐式耦合](https://precice.org/couple-your-code-implicit-coupling.html)：同一时间窗的checkpoint、迭代与回滚。
- [preCICE加速配置](https://precice.org/configuration-acceleration)：收敛仍需各参与者内部求解成立；本实现未集成preCICE。

研究选择：外围依赖DAG＋不可拆开的已注册反馈因子。物理反馈交给原数值求解；图只组织计算与证据，不产生新物理定律。
