# 验证记录与实际边界

本轮55项新增检查通过、152项继承检查通过；[机器验证记录](evidence/validation.json)、[新增日志](evidence/tests-new.txt)、[旧回归日志](evidence/tests-pr148-regression.txt)。新结果重复离线执行完全一致，`independent_audit.py`直接读整数原文件，用Fraction独立实现季节/阈值/相位/k/n，未调用主解析器或统计函数，全部一致；这是第二实现核算，不是第二个人独立科学评审。

负例覆盖：404决定转下源、403/499无绕过、缺凭据、未知许可、中国区域误映射、版本/单位/时间/季节错配、缺测填零、插值/合成冒充观测、静默换源、样本太少/缺相位、因果/认证越权、源哈希错配、重复月份、未知QC。夹具明确合成，真实网络只有收据中的三次200。年块连续性/保留缺槽、真实反例1992、留出训练泄漏、Brier逐行重算及原JJA阻塞均有测试。

首次测试失败是编写中的manifest文件数尚不足任意阈值20；移除该无科学含义的数量断言，改为检查三份原CSV均列入byte_exact并验证全部清单。不改变任何科学参数或结果。

旧PR148 31文件哈希及旧结果SHA `3ff13534e28825ae932694589ccb61ad180d176c5dfff4afc63040737355edfd` 保持；旧PR147结果SHA `279d823da5ee835a9b3e889a0e4777ff0ee0be9be813c8a992ef62aedcada28a`、47文件与Atlas50文件由继承validator检查。所有新文件清单见manifest，原CSV及获取前协议按原字节哈希；其余文本LF标准化。manifest/validation与两个R/D交接元数据排除自引用，不意味着科学资料可静默修改。

复现命令见README；默认不联网，不覆盖归档。提交前本地离线重放，Git diff检查仅新任务、新模块、新测试及根README增量；任务书恢复仓库原始字节（初始Windows换行经-text属性呈现差异，无内容改写）。新PR最终D独立CI另在PR回执提供精确run，不以本地207项等同仓库全量CI数量。

12页静态中文展示使用本包真实结果；桌面/手机可用性测试及截图登记于[evidence/slides-validation.json](evidence/slides-validation.json)。这只验证离线展示，不代表生产网站、访问权限或科学结论通过。

工程LOCAL_VERIFIED；数据OPEN_DATA_RECALCULATED；scientific_admission=PENDING，forecast_validation=PENDING，causal_identification=NOT_ESTABLISHED，DEPLOYED=false。没有扩大权限、部署、合并或科学认证。

最终适配器检查发现既有通用构建器会把所有雨量标成recent rainfall；新适配器将本轮指标标签明确改为historical seasonal rainfall，旧函数不动，并新增回归测试。主概率不变。分数核算也覆盖20/80阈值相等边界。浏览器首次受Windows沙箱进程限制；经本地测试权限复核后，已安装Edge无头运行成功，无外网页面请求。
