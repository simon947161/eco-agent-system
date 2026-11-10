# 最小组件协议

`ports.ModelPort(kernel).initialize(state, config)`统一包装 Atmosphere、Surface、ENSOContext、MethaneERF。属性required_fields/provided_fields/units/grid/current_time，方法step(dt)/inspect/checkpoint/reset/evidence。实际四组件输入输出见 evidence/component-interface.json；测试`test_uniform_ports_all_four_execute`。

物理kernel计算候选值，不自行写入共享库存。局地port需先提供同一exchange通量，然后step(dt)返回`proposal, committed=false`。总耦合器models.advance负责依赖检查、迭代和守恒门后统一提交。ENSO和全球ERF在自己的季节/年支撑上输出衍生证据；任意小时步长被拒绝。共享接口不是可任意互换所有物理过程的承诺，变量、尺度及单位仍必须匹配。

| 组件 | 读 | 写/提案 | 时钟与证据 |
|---|---|---|---|
| 大气交换/柱 | Ta、Ts、p、u/v、q、W及耦合器提供P | H、E、Ta、q；显热/水汽边界 | 每慢步两次快子步；合成理想柱 |
| 地表水热 | Ts、W、P、Rn及H/E | Ts、W、R | 慢步；零侧边热通量 |
| ENSO上下文 | 2012 SON RONI | 冷/中性/暖相、既有统计 | 季节诊断；无局地降雨函数 |
| 全球CH4 ERF | 2025全球CH4/N2O | 全球年ERF | 保持PR147公式域与原证据 |

声明的required_fields是共享状态依赖；物理交换输入通过exchange端口明确注入。本轮固定四种组件，非动态插件平台、无自动下载或执行第三方模型。CF/BMI/NUOPC只借鉴语义，不声明认证。

CLI（仓库根，Python标准库）：

```text
python -m cczps_lite.integration.earth_system_coupling validate-state
python -m cczps_lite.integration.earth_system_coupling list-components
python -m cczps_lite.integration.earth_system_coupling run-baseline --output runtime_data/baseline.json
python -m cczps_lite.integration.earth_system_coupling run-coupled --strategy two_way --output runtime_data/coupled.json
python -m cczps_lite.integration.earth_system_coupling compare-scenarios --output runtime_data/comparison.json
python -m cczps_lite.integration.earth_system_coupling sweep-experiments --count 300 --seed 20261110 --output runtime_data/sweep
python -m cczps_lite.integration.earth_system_coupling explain-failure --code NON_CONVERGENCE
```

七入口均有实际输出及子进程测试。完整万次复算需显式`python docs/tasks/climateos_earth_system_coupling_lab_001/scripts/run_batch.py --execute`，正常导入和CI不启动万次批次。该命令会覆盖本任务同名生成证据；复核冻结包通常先运行validate.py及测试，不应无意重写归档。
