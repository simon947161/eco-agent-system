# 实际质量验证

本轮本地 **77项测试通过**：47项新审查/数据/生命周期测试，11项PR144物料账测试，19项PR138 GasTests及PR143知识引擎回归。完整命令、Python版本、时间、各退出码见 [tests.txt](evidence/tests.txt)。这是作者本地复跑，不声称ChatGPT独立执行。

[replay.json](evidence/replay.json)记录两次实际离线运行，review-results、chain-a-replay、open-fragment-results三份输出逐字节相同；输入/输出/源码/文档hash由 [manifest.json](manifest.json)固定。真实原ZIP按字节，文本按LF规范化；交接两JSON和manifest自身不进入自引用hash。

原始数据核验：一个合法开放候选、记录页+文件各一次取得；发布者MD5与SHA一致；23行原始XLSX字段/非负/缺失检查、PR139转录交叉核对与精确单位反算。未运行真实排放计算、FOD、回归、反演或气候实验。时间/空间/校准未知仍未知。

错误与缺证据验证：B触发单位/相态/双氧化/离界/守恒/原输入矛盾；C在算术可复算时仍拒绝证据通过。其他负例包括自改payload后重算SHA、换代码hash、校准/许可缺失、角色自审、未经授权的EFFECT_VERIFIED/法定认证、时区/空间/版本/报告年错误、NaN/未知字段、事件重排/删除/撤回后重审等。

原件/范围保护：任务书和memo与起始commit保持一致；PR144质量账、CCZPS物理/知识核心和旧任务树未改。所有新增内容仅本任务目录。没有修改旧PR、生产网站、凭证、权限或私有知识库。未读取/发布私人Council数据。私有Knowledge Garden审计只记录必要路径/版本/成熟度，不复制正文。

来源失败：NZ直接正文403，停止；沿用PR144四个NSW403和既有NASA限制，不重试。ISO只有公开元数据；US公式图片未完整图读；未取得源码/文档的字节不得填SHA。详见 [source-review-receipts](evidence/source-review-receipts.json)。

验证器检查：任务文件哈希、schema/三包输出、来源预算、77测试日志、本地Markdown链接、明显凭证模式、冻结文件Git差异。没有新增UI或部署，未做浏览器测试并不声称做过。GitHub Actions/combined status只以最终D的远程回执为准；无已观察检查时标NOT_TRIGGERED/NOT_VERIFIED，不能写CI PASS。

风险：程序只支持作者合成fixture的封闭合同；角色表是测试而非真实身份认证；hash链无外部锚不可抗整体重写；包通过不证明输入的科学真实性；法律/地方许可完整适用需专业审查。所有这些限制进入Founder报告和评审请求。
