# V2.1测试与保密边界

旧候选执行由本地主机完成；公共证据等级为LOCAL_ATTESTATION_NOT_PUBLIC_REPRODUCTION。7个原生案例+3个边界案例，每例重复一次。计数与所有失败在本机详细记录中核对，旧原件及隔离副本内容未改。科学准入PENDING。

公开只保存闭合字段白名单内的聚合计数、粗粒度结果与局限，不含旧实现名称、函数、公式、私有位置、原始输入输出、源文件hash清单或可逆向旧夹具。完整私人报告不在Git工作树。上游任务书原样保留，本次不另行发布私人位置。

公开导出门拒绝额外字段、非空私人载荷、胜负或科学准入升级、删去失败和错误计数。它不能证明私人实验真实或全面排除一切泄密；本次仍逐项审查实际变更及文件清单。新增测试含这些负例，而不是把私人结果伪装成CI测得。

本轮两个公共输入门检查直接使用PR152冻结源文件，检查非有限坐标及配置；不运行物理轨迹。原8组48次公共控制与结果hash保持原样，未为了本轮研究重新运行；全库CI仍会正常执行既有回归测试。

旧端安全执行采用：限定纯Python依赖闭包、只读原件、独立工作副本、进程内socket/子进程/动态库和目录外写入拒绝、自检与事后hash核验。不宣称整机断网，也不宣称这是针对任意恶意本地代码的OS级沙箱。最初4次输出记录器不兼容失败已保留，不能当作旧方法缺陷。

复核公共门：`python docs/tasks/ecoengine_v200_private_method_comparison_001/scripts/public_boundary_checks.py`。

复核本轮公开导出：`python -m unittest discover -s tests -p test_ecoengine_candidate_summary.py -v`。

复核保密标签：`python docs/tasks/ecoengine_v200_private_method_comparison_001/scripts/privacy_gate.py`。

远程HEAD/CI以PR实际交付回执为准。本机通过不能代替远程CI；远程CI不能审私人算法。
