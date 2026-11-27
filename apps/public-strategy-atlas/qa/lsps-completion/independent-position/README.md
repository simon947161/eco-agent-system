# LSPS 原件位置与覆盖核验

本目录的结果验证固定版本原件、来源位置、逐项覆盖及进入应用时的传输完整性。它不把页面哈希一致当作全部语义正确，也不证明现行法律适用性、实际实施或官方认可。

复验命令（原件仅放在本机临时目录，不进仓库）：

```sh
python tools/verify-lsps-context.py --pdf /tmp/csoi-lsps-completion-20261102/lsps.pdf
```

脚本要求原件 SHA256 为 `9bf75ec6fb98f1d03bad47f5b9cda44e6ffadce3bf452eb5a343b394322f8f47`，共 118 页；使用 PyMuPDF 1.26.6 与 pypdf 6.10.0。每次裁图均从已核对的原件字节新开独立 Document，精确使用已记录的 bbox、RGB、100 dpi；不接受旧版渲染契约或备用哈希。渲染契约修正的实际重现证据保存在 `renderer-contract-resolution.json`。

分母分别记录，不能互相替代：

- 原始布局：118 页、1,124 个非空原生文字块、27,376 个可提取词位置、234 个嵌图块。
- 作者文字清单：1,384 个布局分段，分别标明自写解读、既有行动、表格上下文、标题、导航、页码等。
- 合并后的解读：491 个文字单元及 21 个非空间视觉单元，共 512 个。视觉单元可拆分一幅复合图，因此不等于原文图表数。
- 地图：27 个地图出现位置；正文与附录中的重复出现分别保留来源锚点。
- 既有核心：原 114 个记录保留，包括 83 条实施表行动和另 18 个叙述冲突记录；不把两者合称 101 个已实施项目。

查看证据时优先使用：

| 文件 | 能证明什么 |
| --- | --- |
| `verification.json` | 本次完整结果、精确输入哈希、检查时间、限制与实际负例 |
| `negative-cases.json` | 错页、错框、删条件、改图例、缺/坏原件、丢行动上下文等是否真正被拒绝 |
| `page-coverage-matrix.csv` | 全部 118 页可提取词位置是否有明确归属 |
| `inventory-position-matrix.csv` | 1,384 个文字分段的位置与分类 |
| `semantic-unit-position-matrix.csv` | 512 个自写解读单元与原件锚点、条件证据关联 |
| `map-position-matrix.csv` | 27 张地图及各自图例的原始像素锚点 |
| `source-reading-context-matrix.csv` | 应用中的阅读上下文连接，不能当作官方行动关系 |
| `original-source-census.json` | 从原件独立提取的布局、嵌图及哈希清单，不含原文正文或图片 |
| `existing-core-source-verification.json` | 对既有实施表、叙述出现位置及勾选图列的本轮原件复验 |
| `existing-actions-baseline.json` | 原 114 个记录及其中 101 个 ACTION 记录的保存检查 |

`verification-before-relation-linkage.json` 是补齐应用阅读连接之前的检查快照，绑定它自己记录的旧输入哈希；不能用于声称后续版本已经验收。带 `incremental` 的文件也是过程中保留的草稿检查，最终结果以 `verification.json` 为准。

语义和地图解读另见相邻的 `independent-narrative` 与 `independent-visual` 目录。本脚本只对选定的原文条件及图例语义做可复验断言；全部解读仍属于独立 AI 审读，正式人工/专业准入为 PENDING，现行法律及实际执行保持 UNKNOWN。
