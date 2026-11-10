# 公共测试与保密边界

执行环境确认为LOCAL_WINDOWS；旧源代码执行0次。目标方法尚未定位，因此没有安全执行旧模块、取得旧法输入输出或完成双边对照的声明。定位详单、源码片段、原件hash与完整私人阶段报告均不进入此Git工作树。

公共侧固定PR152源码hash，复跑其65项测试。8组控制先写PUBLIC_CASE_PROTOCOL.json再执行，每组三策略并逐字重复一次；见evidence/public_controls.json。public_execution_count=48，legacy_execution_count=0，paired_comparison=NOT_EXECUTED，winner=UNKNOWN。运行时间只记录新方成本，不用于新旧速度胜负。

新增验证检查条数、配置冻结、已声明失败、重复hash、水热残差与导出白名单。公开runner不接收私人目录参数，没有旧程序加载器，没有私有算法或可逆向夹具。CI只能验证公开代码与公共侧证据，不能复跑本机私人定位，更不能认证旧法。

每台主机内重复要求结果完全相同；与归档跨平台比较保留状态/拒绝原因相同，数值允许1e−10绝对或1e−12相对差异，以免不同数学库末位舍入被误判为科学失败。此容差不替代原有守恒门或真实观测验证。

保密检查仅针对本次新增公共文件；上游V2任务书原样保留，不重写历史。新摘要不包含旧实现名称、函数、私有路径、源码/专有公式、原始旧输入输出或私人hash清单。私人报告的位置只在用户私人回复中提供。

公开复现：`python docs/tasks/ecoengine_v200_private_method_comparison_001/scripts/public_controls.py`，默认输出至忽略的runtime_data，不覆盖归档；全套旧测试和新对照不自动启动万次实验。

状态为阶段性PARTIAL，不是完成的旧新方法科学比较。远程HEAD与CI由实际Draft PR交付回执固定；本地测试不能代替远程CI。
