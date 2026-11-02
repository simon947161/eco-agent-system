# CSP 公开来源补齐与逐项核验

这次工作是**重新从已登记的官方原件补做、并复核当前可访问审计清单**，不是找回此前未提交的 Phase2 文件。原审计中已经交付的报告、Excel、44 策略清点与 63 指标目录在 `qa/remediation/audit-baseline/` 可检查；它们描述旧提交的缺口，不能当成本次网站已完成的证明。

本次重新取得官方 CSP 2035 完整 PDF：24,842,203 字节，36 页，SHA-256 与历史登记一致。封面为 2025 revision；第35页版本表记录 v3.0、2025年5月1日、73/25。当前受控版本仍为 UNKNOWN，没有访问 Council 内网。

已形成可供原有模型注册的 **127 个 CSP 研究记录**：1文档、5主题、14目标、44策略、63指标。这与旧 Atlas 的127条内容不是同一统计。每个记录带来源版本、页码、页摘要散列和区域坐标；每条策略保留原表的 Council 角色和伙伴列；五个主题还保留18次来源列出的支持文件名称引用。支持文件的版本及实际实施关系仍 UNKNOWN，不生成官方关系。

指标保留原表的四列、原始数值、倍率、单位、来源年标签、趋势和条件。29.9 指区域人均排放来源值，7519 CO2eq 的完整质量单位仍未明示；两者年份和边界不同，不能自动求水务贡献。公共交通2.1与3.1两个原表值分别保留，不按同名合并。其他缺百分号的比率、缺币种的金额、没有匹配原始分母的指标也没有补造单位或计算结果。所有实际结果 UNKNOWN，独立重算 NOT_COMPUTABLE。

## 怎样核验

`tools/build-csp-knowledge.py` 使用 pdfplumber 的表格坐标读取事实列，并输出作者自己的短摘要。独立 `tools/verify-csp-knowledge.py` 不导入构建脚本，而是使用 PyMuPDF 从原PDF再读单元格和策略列；pypdf 用于页摘要散列。

本次通过：63个指标共252个原表单元格、44策略的角色/伙伴列、14目标/44策略编号和层级、5主题、全部支持文件名称清点。12个故意损坏或缺失样例均拒绝，涉及漏指标、漏支持文件、改原件版本、错误页码、改数值、伪造7519吨单位、挪单元格、假角色/伙伴、晋升实际结果、删去冲突、删去领导可见性限定。独立语义复核发现12.1摘要原先漏掉“可见”，现已恢复与“可接近”并列，新增明确限定检查和负例。

`original-verification.json` 与 `negative-results.json` 是实际结果。页码或散列相同本身不证明摘要语义；短摘要另做了 AI 辅助逐项原文对照，这不等于获授权人工法律审查。

## 全文件范围及仍未完成的事

`page-coverage.json/csv` 对36页逐页列出内容、检查方法、记录覆盖和缺口。核心目标、策略及进展指标表已进行有界结构化；背景叙述、人口图表、参与数据、缩略词、伙伴总表等已作为文档上下文检查，**没有宣称全部原文逐句进入知识图谱**。照片/儿童画/个人署名和联系方式没有再发布。

本次明确保留的来源问题：

- 目录把第15页列为 SDG 内容，但视觉检查该页为照片；没有虚构 SDG 映射。
- 第3页出现“18年”表述，与2025修订和2035标题存在未解释的时间口径问题。
- 第28页说明指标用于社区进展观察，不能作为 Council 实绩的替代。
- 第23/25页的区域规划名称写法不同，支持文件只保留各页实际名称，未强行合并版本。
- 第35页指向内网受控文档，公开文件当前性不能自动确认。

`item-coverage.json/csv` 有127行，逐项列出提取、来源验证、实现状态与缺口。当前 `implementation=PENDING_PARENT_INTEGRATION` 是有意保留的状态：此研究子任务没有改共享模型、网页、缓存或部署；父任务实际整合及浏览器验收后才能更新软件实现状态。这份报告也不代表 Council 全部文书或80项工程任务全部完成。

## 复现

从 `apps/public-strategy-atlas` 运行，原件仅放临时目录：

```sh
python3 tools/build-csp-knowledge.py /tmp/csoi-strategy-completion-20261101/csp.pdf
python3 tools/verify-csp-knowledge.py /tmp/csoi-strategy-completion-20261101/csp.pdf sources/csp-public-knowledge.json --out qa/strategy-completion/csp/original-verification.json --negative-out qa/strategy-completion/csp/negative-results.json
python3 qa/strategy-completion/csp/build-coverage.py /tmp/csoi-strategy-completion-20261101/csp.pdf
```

来源不可用或字节变化时应报告实际结果，不能用新内容冒充上述版本。原PDF、全文抽取和页面图片不提交；这里仅保留有界事实元数据、自己的摘要、定位证据和校验工具。
