# 实际验证与保证边界

本地执行2026-11-23，Python3.14.6/Windows。源代码、输入、输出的实际字节及LF哈希在manifest；不能由软件测试推定真实场址科学或监管认可。

|检查|真实结果|证据|
|---|---|---|
|本任务单元/语义schema/独立oracle|26项通过，0失败0错误0跳过|[JSON](evidence/unit-tests.json)、[逐项日志](evidence/unit-tests.txt)、`tests/test_awt_claims.py`|
|全仓库回归|570项，0失败0错误，1项旧Windows symlink权限跳过|[记录](evidence/full-suite.json)、[真实日志尾](evidence/full-suite-tail.txt)；完整本机日志在忽略的runtime_data|
|确定性重放|三个输出文件前后字节SHA一致|[replay](evidence/replay.json)|
|有界计算|4中心情景；384个角点，D阻止完整计算|[实际结果](evidence/results.json)、[角点输入输出](evidence/sensitivities.json)|
|审查规则案例|8个记录案例；没有真实主张获批|[decision-cases](evidence/decision-cases.json)|
|桌面/手机|1440×1000与390×844，各12页；按钮、键盘、来源展开、hash重载通过；0 JS错误、0自动HTTP请求|[浏览器QA](evidence/ui/qa.json)，同目录8张代表截图；Chromium模拟视口，不是所有浏览器或实机保证|
|Git与保密|仅显式任务目录、单元测试、已有索引/交接及CI受控改动；旧测试生成的四文件已还原|最终PR diff与package-validation；没有旧私有源码、原始版权PDF、数据库、凭证或Council私密记录|
|远程CI|等待本交付SHA的实际GitHub回执，不以前述本地结果冒充|最终PR评论绑定HEAD、workflow和job；未触发部署|

## 规则结果应如何读

- 物理有效：A/B/C质量账闭合，标记COHERENT_WITHIN_SYNTHETIC_CH4_BOUNDARY；不等于完整废物LCA或观测拟合。
- 物理错误：capture=1.2拒绝CONDITIONS_NOT_MET；不可展示净减排结果。
- 缺基线/残渣/QC：INSUFFICIENT_EVIDENCE，完整净值null；未知气体不默认0。
- 新注册已到期AWT2015：仅该路径NOT_ELIGIBLE。旧项目、咨询版、豁免不明及其他适用范围继续INSUFFICIENT_EVIDENCE/UNKNOWN。
- 候选权利重合：只标记潜在风险，未识别已发行信用、欺诈或真实冲突。
- 所有合成包：没有现场证据，assurance始终INSUFFICIENT_EVIDENCE，credit NOT_DETERMINED，scientific admission PENDING。

## 测试局限

哈希清单由本作者Git树封存，不是独立证明；公钥签名、可信时钟与真实评审角色尚未建立。测试不核验假设参数在现场成立。现场浓度/流量/源强、N2O、残渣长期端点、合法反事实、方法适用期与独立审计均待证据。七维情景范围不含GWP或所有结构不确定性。

复算命令见README。运行run_validation会记录当前机器测试结果；正常独立审阅先verify_package，避免先重写hash或结果掩盖差异。外部原件没有本轮byte hash的条目明确为空，不能把作者笔记的hash当其原始数据摘要。
