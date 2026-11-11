# 验证证据

- 26项新增行为/数值测试覆盖任务书A–J：共享祖先、真实端口与原路径逐值相等、独立水焓库存、零通量解析极限、普通异常及不收敛回滚、整组物理边撤销、真实前态延迟、单位/时空/语义门、统计边不能伪装、非有限/缺测、参数不可辨识、完整/选择性一致、无收益反例、30层菱形及非法环、条件阈值。
- 本机完整回归765项，764通过、1项Windows symlink权限跳过（最终运行时间见evidence/test-results.json）。首次旧localhost测试8项因WinError10013失败；允许回环后通过。不是新图算法失败；没有把初次失败抹掉。
- 原始结果在evidence/benchmark_final，初版在evidence/benchmark，中间版在evidence/benchmark_before_endpoint_hardening；三批seed相同，但不同源码版本，不能合并为独立科学样本；前两批为历史记录，当前HEAD直接复现最终批。
- RESULT文件与代码hash可按evidence/benchmark_final/summary.json复核。计时不能逐字节复现；每模式数值/审计记录去除seconds后重复hash相同。
- 展示验收见evidence/ui/qa.json；浏览器证据完成前该项不视为通过。
- 原PR152仅本分支models.advance新增可选mapper，不改变默认公式；父分支、旧报告和科学状态保持。没有访问私人旧资产。
- GitHub CI与精确远程HEAD见最终PR回执；本地通过不代替远程通过。
