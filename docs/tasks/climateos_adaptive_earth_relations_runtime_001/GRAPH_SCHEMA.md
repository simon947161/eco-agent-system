# 图契约与调度

`graph.py`定义冻结Node/Edge数据类，节点和边表为只读MappingProxy；改边须调用with_edge返回新图，避免边表与邻接表失配。SHA绑定完整声明。最多256节点、1024边。

节点包括强迫、模型场、物理过程、统计上下文、诊断、决策问题。OBSERVATION为保留类型，本轮未提供新的观测加载执行操作；不能伪称已实现任意观测插件。操作白名单与节点种类必须匹配。

边记录：source/target、source_field/target_field、源/目标单位与范围、clock、lag_steps、conversion、evidence、source_ref、applicability、numeric、enabled、revoked、required、ledger。字段端点须命中操作契约。当前只支持identity转换；不同单位即使可换算也拒绝，须另经显式适配扩展。required标记用于说明，实际最低依赖由操作注册表强制约束，不能通过改为false删掉必需条件。

五类边：PHYSICAL_FLUX、DECLARED_PROCESS_DEPENDENCY、STATISTICAL_ASSOCIATION、HYPOTHESIS_CANDIDATE、DIAGNOSTIC_DERIVATION。统计/候选边可作为CONTEXT_ONLY存在，不能向数值模型传力。即使把统计节点边改成普通依赖，也会被CONTEXT_CANNOT_FORCE拒绝。执行准入只意味合成沙盒契约满足；正式科学准入始终PENDING。

`coupled`是包含空气与地表的原子因子。内部蒸发/潜热和显热边绑定固定双边账本；任一交换被撤销时整个因子拒绝。q反馈按声明lag调用原模型；初始不足历史时使用明确登记的初态延拓。它不是可随意添加的普通自环。所有其余未注册环拒绝。

选择性计划：从目标迭代计算上游闭包，每个共享节点每时钟最多执行一次；拓扑排序不枚举路径，O(V+E)。反馈求解成本另为O(时间步×固定点迭代×网格数)，不能算进“图线性”保证。计划每次重新计算，不做跨运行缓存或未声明的自适应物理步长。

同一land interval内原空气组件有两次dt/2子步。季节/年度节点各按原时段独立计算一次。lag_water输出前一个已完成水库存，不插值成未知历史。每步回执记录执行节点、条件关闭、实际边、ledger、时间、rollback。

反向追踪返回去重节点/边、深度、来源、拒绝候选；路径计数封顶1,000,000且不展开路径。它是计算依赖追踪，不是由结果唯一反演自然原因。联合情景差是同模型下的数值差，不自动赋予因果含义。
