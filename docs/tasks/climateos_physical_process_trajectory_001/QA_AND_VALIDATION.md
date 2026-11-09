# QA、实际执行与可复算证据

执行命令：`python -X utf8 docs/tasks/climateos_physical_process_trajectory_001/run_validation.py --record`；下游复核去掉`--record`，不修改归档。Python标准库，无新安装依赖。

本轮新增测试覆盖：NOAA公布结果取整锚点、前工业零点、域/单位/相态拒绝、解析导数与独立中心差分、模型误差不冒充测量CI、合成能量守恒及不闭合反例；旧甲烷质量/碳账；RONI原字节哈希、缺季/重复/哨兵、独立条件计数、固定时滞、bootstrap复现/退化；水量维度、共享通量协方差、未知支流/储量、非零残差不归因；HRS不可靠标记；评分诊断与未发送；假引用/版本/缺证据、政策分数、样本外推、因果和审批越权。

实际通过 **120项限定测试**（27项新增+93项继承），分组62+47+11，全部退出码0。同时重跑原Atlas、CCZPS情景、PR143甲烷、PR144账本、PR145审查测试。原Atlas50文件清单保持完整。五个端到端样例（CH4、ENSO、HYDRO、CROSS、SCORECARD）及三条trace两次运行一致；结果逐项与归档数值比较。

实际计数、退出码、Python版本和时间以 [tests.txt](evidence/tests.txt)、[validation.json](evidence/validation.json)为准。结果是作者本地验证，不冒充ChatGPT独立重跑或CI。GitHub的R与D各自CI须查精确SHA，记录在PR最终交接评论及交接元数据；无检查不写PASS。

哈希：下载原字节在 [acquisition.json](evidence/acquisition.json)；仓库清单在 [manifest.json](evidence/manifest.json)。除RONI保留原字节，文本以LF规范化。元数据R/D与执行日志不进入自引用清单；其完整性由最终Git提交保证。清单不是外部签名，不能证明来源真实或人员独立。

安全审查：只归档公开数值、短引文、作者摘要和继承公共HRS；完整网页缓存在ignored runtime_data；不提交凭证、私人数据库或私人Council材料。Scorecard403、Nature身份页、BoM页面工具不可达均停止，无绕过。无网络的evaluate/query/trace不会取得新数据或改变旧门。

验证限制：没有独立仪器校准、真实流域闭合、区域雨量统计、气候响应验证、官方评分细则确认或法定认证。真实科学结论与监管适用性仍待人类评审。
