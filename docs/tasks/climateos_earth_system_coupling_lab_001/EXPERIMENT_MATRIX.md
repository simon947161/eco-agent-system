# 固定设计、实际批次与版本记录

原始PRE_RUN_PROTOCOL.md在首次数值执行前固定，保留其原hash。seed20261110、3336配置×3策略=10008主执行；每个family有278配置，即834条运行记录。12族：nominal、heat_dry、rain_pulse、zero_wind、lagged、stiff、missing_q、unit、time、iteration_limit、synthetic_as_observed、global_to_local。

每族内部轮换2/4格与dt450/900/1800秒六种组合，6小时总时窗；固定种子的正态温湿参数相关rho−0.6，范围与逐条配置在runs.jsonl。温度286–314K、q .002–.018kg/kg、风.2–10m/s、水15–120kg/m²、Rn50–400W/m²、雨0–5e−5kg/m²/s、Cs1e6–3e6J/m²/K、柱高60–180m、Ce .0005–.004、kappa0–2m²/s。热旱/强雨/零风/延迟/高扩散/迭代1次/错误标签族按生成器显式覆盖。雨族为固定强雨边界，并非真实降雨过程记录。所有系数均ASSUMED。

首300次冒烟发现family索引与网格/步长绑定，会混杂比较。因此改为family内部六种组合，保留`evidence/smoke_initial_receipt.json`中初版hash与结果，且不把该初版计入主批。没有用结果优化参数或隐藏失败。修正后再300冒烟，然后10008主运行、同seed完整重放、seed20261111的300新运行；新seed不拼入主10008。固定例子另有120次rho−0.6/0成对不确定性诊断(seed20261112)、步长/网格/滞后/扰动与解析解，均单列。

第一次完整批次结束前增加统一ModelPort接口（未改物理方程/参数），初批收据保留`pre_interface_batch_receipt.json`。最终冻结全套源码后重新运行完整批次；主runs哈希必须与初批相同。最终源码hash包括ports.py。两完整批次、首冒烟与最终重放的实际墙钟累加列于QA，而非把两次主矩阵冒称两组独立科学证据。初版冒烟源文件hash留作历史收据；现行代码不能冒称可逐字复放那个旧版。

负例要求：错单位/时间/空间/合成冒观察在三策略均拒绝；missing_q只拒绝依赖湿度的两策略；iteration_limit只使双向不收敛；零风三策略应相同；stiff按真实CFL判断，允许较粗格/较短步长合法。通过率必须区分正常运行与有意注入的拒绝，不能作为准确率。

另测：面积与协方差重映射；DST/时间缺口/未来支撑错位；可逆差异与错误基准hash；解析空间二阶/时间一阶；联合热旱阈值；Ce×U不可辨识；独立ENSO/全球ERF仍可运行。具体断言见 tests/test_earth_system_coupling.py。

成本上限：单批总实验1200s、证据200MB、每运行≤96步/80次迭代/16格。输出明确completed_runs/early_stop/bytes/elapsed/config_hash，拒绝无限循环。将来10万次需重新批次设计、独立留出和Founder授权，不由当前runner的容量上限推定授权。
