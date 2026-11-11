# PR155 最小工程修复 · 2026-11-11

对应 ChatGPT 评论 #6791516840，原审查 HEAD `256f950685c0eafd3771ff1c1c8fe696de6f5d1d`。
本文件是作者修复回执，不是独立科学接受。PR 保持 Draft / SCIENCE_PENDING。

1. `runtime.py` 将 checkpoint 前移到本时段降雨写入之前，并将 forcing 同步放入 try。
   合约 `WHOLE_STEP_BEFORE_FORCING_SYNC`：失败恢复全部 Field 值及元数据、State revision、
   水热库存、rain、时间支撑、两组件时钟；此前成功时间步保留。清空失败交换缓存。
   补测初步 pulse + NON_CONVERGENCE，及第三步雨脉冲结束后已实际提交物理量再注入异常；
   比对完整 inspect/hash，而非只看异常文字。恢复后的下一次物理求解与同状态干净副本逐项相同。
2. `comparison_metrics` 独立减算最终 ta/ts/q/water，每字段保留单位、有效配对数、缺失数。
   不把不同量纲求一个最大值；空状态不报告虚假的零。严格相等断言单列。
   注入 1.25 K 和 0.5 kg/m² 差值的测试证明它能查出非零；非有限数拒绝、缺失显式记录。
3. `scripts/review_closure.py` 从原始 JSONL 重算 120 组已存配对，并核原 SHA256。
   没有重新运行720次，也没有覆盖计时、13/50更慢、物理调用未减和全目标无剪枝反例。
   历史 RESULTS.json/max_output_delta 保留原记录，明确它原来是 EQUALITY_ASSERTED 回执。
   旧 source_hashes 仍属于旧 HEAD；新源码 hash 单列在 review_closure.json，未冒称旧实验绑定新代码。

复核：`python docs/tasks/climateos_adaptive_earth_relations_runtime_001/scripts/review_closure.py`；
`python -m unittest tests.test_earth_relations`（29项）。全套及远程CI以本次精确HEAD回执为准。
初次编写回归时发现旧失败样本有 None，差分器已显式保留缺失；后期回滚测试最初捕获了内部
checkpoint，已改为同时核时钟和时间支撑定位整步边界。这些是修复过程中的测试失败，未隐藏。

没有扩展模型/科学授权，没有改 PR152 分支及其物理源码；不合并、不部署。
