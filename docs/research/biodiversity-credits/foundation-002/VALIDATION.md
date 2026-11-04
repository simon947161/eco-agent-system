# 验证范围与复现

本包检查结果：[VALIDATION_RESULTS.json](VALIDATION_RESULTS.json)。仓库回归：[REPOSITORY_TEST_RESULTS.json](REPOSITORY_TEST_RESULTS.json)。

仓库标准命令：`python -m unittest discover`。实际使用Codex捆绑Python，最后一次将tempfile.tempdir设为独立工作区目录并获准沙箱外执行。482测试、0失败/错误、1平台symlink跳过。前两次沙箱PermissionError已记录，不计通过；未修改测试或放宽断言。

包检查：`node docs/research/biodiversity-credits/foundation-002/validate-package.cjs`。不提供环境变量时只执行自包含文档/引用/结构检查，结果明确标记原件和原生合同检查NOT_RUN；不能覆盖归档结果后再声称完整通过。完整复现需要：

- `CLIMATEOS_BIO_RAW_DIR` 指向已下载并按manifest文件名保存的原件目录。
- `CLIMATEOS_ATLAS_CONTRACT_DIR` 指向从 `e3d8f074e0e1ba5e9614c3f4c5a2b973746b2ab7:apps/public-strategy-atlas/` 按字节提取的`atlas-model.js`、`atlas-domain.js`、`atlas-data.js`。文件SHA先与contract receipt核对。

`build-atlas-candidate.cjs`是离线候选构建器，只写本目录JSON，不连接服务、不导入Atlas、不执行信用计算。已有candidate固定baseDigest/实体/断言/修订/事件。检查使用真正的固定版本AtlasDomain.validate及AtlasModel哈希/事件函数；不是自建替代校验器。负面测试覆盖非法准入、悬空端点、错误端点修订和内容篡改。

工作簿用ZIP/XML检查全部worksheet、标准和扩展命名空间验证、全部关系文件、drawing文字与customXml。未执行宏、外链、重算、编辑或提交；原件校验在包检查中重复。原件扫描结果经长文本摘要转换后归档，不把逐字提取公开。

没有UI/运行时修改，浏览器回归不适用。完整Atlas verify/import、sourceCatalogue正式准入、专业科学/法律审查、交易核验及生态结果验证均未执行。测试通过不提升这些状态。

`authored-manifest.json`仅列本目录其他归档文件的SHA，不包含自己，以避免自引用；它不是官方文档哈希或签名。官方原件哈希仅在download-manifest中。
