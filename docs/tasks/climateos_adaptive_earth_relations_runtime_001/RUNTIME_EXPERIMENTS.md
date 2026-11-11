# 实际执行结果

协议EXPERIMENT_PROTOCOL.json在主批运行前固定。最终源码锁定于RESULTS.json；seed=15420261111。120配置×2模式×3重复=720次调用。三次轮换执行顺序，逐模式确定性hash相同。前期可变图实现的首批保留在evidence/benchmark；修复邻接表一致性风险后重跑在evidence/benchmark_final。三批不拼为更多独立样本；第二批保留在evidence/benchmark_before_endpoint_hardening。最终还检查了物理账本必须绑定当前因子、慢域节点不能被改标签为局地。

有效配置50，故意破坏的配置70；对应最终批300次完成、420次拒绝。失败不是预测误差，通过比例不是科学准确率。

|拒绝类别|配置数|
|---|---|
|COMPLETED|50|
|MISSING_DEPENDENCY|10|
|UNIT_MISMATCH|10|
|TIME_MISMATCH|10|
|SPATIAL_MISMATCH|10|
|NON_CONVERGENCE|10|
|DIFFUSION_CFL|10|
|PHYSICAL_CLOSURE_REQUIRED|10|

相同条件下输出/最终物理场/拒绝完全一致，最大差0。每模式每个有效配置取一次的执行数：选择性2165、完整安全5044，减少57.1%；物理ModelPort调用各11662，未节省守恒所需计算。计入三次重复时这些计数乘3，不能混淆。

选择性/完整耗时比中位0.929250，范围[0.8029083486288641, 1.1385561279657288]；13/50有效配置选择性更慢。此为本机小任务实测，三次重复不足以证明稳定跨机器加速。请求全部结果时双方122次节点执行，无剪枝收益。

最大水残差1.4432899e-14 kg/m²；能量6.0346792e-08 J/m²。另有逐单元库存与全域焓的独立测试，未只断言回执自称守恒。

最终批4.292秒，原始记录5210372字节；未触发20分钟/200MB门。三批各自低于门槛；旧10008批未作为本研究重跑，完整仓库回归仍会执行其已有测试。

## 三个实际纵向情景

|情景|空气K|地表K|水库存kg/m²|比湿kg/kg|合成诊断|
|---|---|---|---|---|---|
|BASELINE|298.642917|300.481785|49.929541|0.01045760|{'hot_dry': [False, False], 'saturated': [False, False]}|
|HEAT_DRY_WIND|305.927167|307.406057|19.884056|0.01080925|{'hot_dry': [True, True], 'saturated': [False, False]}|
|RAIN_HEAT|304.487858|305.652732|149.355312|0.01517234|{'hot_dry': [False, False], 'saturated': [True, True]}|

两单元初始地表温度不同；雨脉冲前两个时段分别按1.0、1.2倍降雨输入，之后为0。所有驱动为合成。heat/dry和rain/heat为至少两个联合扰动；差分见evidence/scenarios.json。
