# 测试、来源和版本证据

实际执行：evidence/tests.txt，30 tests / OK：新增11项、P1 GasTests8项、PR142回归11项。测试数量不是科学发现数量。新测试包含多组子情形。

新链独立手算比对；中心差分核查解析Jacobian；x=0/e=0极限；质量不守恒故障注入；mg/L/ppb/湿ppm等错误单位；CO2/N2O/水相拒绝；缺P/T/e/校准/来源；未知参数和文本；负/NaN/Inf/布尔/越包络；无来源参数；错误模型/实际观测请求；时空基准；不合法相关系数；缺依赖/环路/未批准节点；排放与气候请求阻塞。PR142代码保持不变。

输入/输出与新旧代码哈希见evidence/manifest.json。仓库文本按CRLF→LF规范化，原始物理数值未变；manifest本身由Git commit固定。复核脚本验证登记来源、图谱节点/边、路径、哈希以及链A重放相等；runtime计时不要求逐字复现。所有原观测数据均未下载或改写。

GitHub CI结果见最终精确HEAD交接评论；不能由本地OK推断远程通过。既有CI可能自动跑仓库合成回归，这不是新的现场/气候实验。无新重型依赖、无服务或UI变更，不伪造浏览器截图。资源记录仅execute耗时和Python跟踪分配峰值；总内存、硬件成本、研发总时长UNKNOWN。

公式完整性不是独立现场验证。部分来源只读元数据或搜索片段；具体缺口见SOURCE_REGISTER。审查者尚未独立复算，状态REVIEW_READY / NOT_SENT_TO_CHATGPT。P1-A PENDING及既有科学门不变。
