# 端到端问题与治理交接

研究问题：在指定的温度/湿度/风/降雨/土壤库存及边界条件下，水热交换如何改变地表与空气状态，哪些联合条件使合成热旱阈值出现？

执行路径：来源目录(SOURCE_REGISTER及旧PR147/149manifest) → state字段和各自时空支撑 → 四组件调度 → 无交换/单向/双向对照 → 差异/灵敏度/阈值/失败 → evidence主记录与hash → CCZPS情景比较建议 → ECOChain候选审查记录 → Founder与独立科学评审。

两种证据并列：(a) evidence/baseline.json包含原全球ERF与RONI/46年历史统计的只读复用；(b) evidence/main/runs.jsonl及diagnostics.json为合成多变量耦合。原SON统计不进入局地P或参数，全球ERF不进入局地Rn。它们共享证据接口，不被拼成全球至地方的定量因果链。

候选Evidence Passport最小内容：run_id/scenario_id/seed/config_hash/model_version、源文件hash、假设与参数、网格与时间界、方法版本、QC/缺值/协方差、守恒/收敛结果、反例、status/failure、回滚与需决策事项。完整metadata在fixture-state/diagnostics，主批用config+hash压缩保留可重建的支撑。

CCZPS可比较“无交换、规定边界、有限反馈”及所需证据成本，不排序现实政策收益。ESG++只能翻译证据限制，不能将输出变成实际减排量。ECOChain canonical仍NOT_FOUND，Enotebook仍PENDING；本目录是提议的可审查知识包，不声称已经写入权威链或完成认证。

人为决策门：ChatGPT独立复核实现/证据；Founder决定是否采用该机制、增加哪一种实际测量/模型对照、批准下一受限批次。无人自动提升SCIENCE状态。Issue150主线交付完成后，旧系统独特方法及其关系作为独立任务先研究公开/已授权材料，本轮不访问私人EcoEngine v200。
