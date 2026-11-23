# P4 验证范围与复核方法

评估日期：2026-11-24（Australia/Sydney）｜`READ_ONLY`｜`NO_RAW_DATA_DOWNLOADED`

授权：[Issue #164](https://github.com/simon947161/eco-agent-system/issues/164)。只校验作者编制的文档/元数据，不运行任何物理或排放模型。

在仓库根运行：

```powershell
python docs/tasks/climateos_awt_001/p4/validate_metadata.py
```

脚本仅使用Python标准库读取本目录JSON/Markdown及Git，不访问网络、不下载、不导入父引擎。stdout即[本轮回执](validation_results.json)。检查4候选/3详审限制、七闸门、许可与结果不矛盾、原始字段null、日期及边界标记、本地链接、来源引用、敏感凭证特征、所有父封条文件和五个复用组件LF哈希，以及Git相对冻结HEAD的变更只能在p4。

**限制**：脚本不是法律/科学判定器，也不能单靠仓库证明外部世界从未下载。无原始下载的依据是实际工具调用范围与[source_register](source_register.json)的操作记录；校验仅确认交付包没有第三方数据文件和冒充原件的哈希。

旧[verify_package.py](../verify_package.py)会递归枚举整个AWT目录且调用引擎；新p4文档不在旧manifest中。因此本轮不运行它，不重封冻结manifest，不声称旧全包验证通过。新脚本只读取旧manifest列出的文件，检查其字节规范化哈希没有变化。这是文档增量边界核对，不是绕过某个失败的实际科学测试。

工作流的paths仅覆盖cczps_lite、tests及该workflow，p4文档不匹配；预期本PR CI NOT_TRIGGERED。最终实际GitHub运行/状态以精确HEAD回执为准，不冒用父PR成功结果。未触发main push、workflow_dispatch或部署，未改workflow。
