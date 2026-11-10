# 失败、反证及不能据此宣称的结论

主批实际分布：

|状态|条数|含义|
|---|---:|---|
|COMPLETED|5145|完成声明模型推进|
|DIFFUSION_CFL|693|按门限拒绝，详见原run_id/config/failure|
|MISSING_DEPENDENCY|556|按门限拒绝，详见原run_id/config/failure|
|NON_CONVERGENCE|278|按门限拒绝，详见原run_id/config/failure|
|SPATIAL_MISMATCH|834|按门限拒绝，详见原run_id/config/failure|
|SYNTHETIC_AS_OBSERVATION|834|按门限拒绝，详见原run_id/config/failure|
|TIME_MISMATCH|834|按门限拒绝，详见原run_id/config/failure|
|UNIT_MISMATCH|834|按门限拒绝，详见原run_id/config/failure|

missing_q族中独立地表可完成，两交换策略阻塞；iteration_limit族的单/独立可完成、双向拒绝；stiff族由CFL而非名称决定拒绝。正常五族共4170条，准确范围见原始矩阵。失败初始化与失败步回滚分别记录stage，未初始化时不谎称发生过步回滚。

反证1：零风条件使三策略相同，反驳“耦合必然带来差异”。反证2：Ce×U不可辨识，反驳“同一输出唯一确定机制”。反证3：联合热旱与单独扰动结论不同，反驳单变量排序可解释所有阈值。反证4：双向需要额外迭代与观测变量，迭代耗尽或缺湿度时比独立模型更脆弱。反证5：Guillod2015显示土壤水分—降雨的时空关联符号可不同，不能把本模型内反馈方向普遍化。

当前局部Jacobian范数与松弛界见diagnostics.json；只是局部充分界。决策记忆不证明物理滞回。rho变化导致输出散布变化，但不是现实置信区间。所有负例保留，不调参掩盖。缺乏观测误差对照，不能排名真实准确率。

发布前仍需科学评审：理想气柱、无凝结、固定参考液体焓、空间代表性、未知参数、现有观测权利与缺测。当前软件验收不关闭这些门。
