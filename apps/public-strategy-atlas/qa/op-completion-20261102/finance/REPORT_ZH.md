# OP 财务与收入政策原件阅读记录（PDF 107–142）

本部分已完成指定原件末尾 36 页的作者阅读、数据提取和独立语义复核。成果是可核对的研究资料，尚不能据此说网站已完成集成、浏览器验收或发布。主任务另行记录这些工程结果。

本次只使用已登记的 2026–2027 OP：142 页，37,500,187 字节，SHA-256 `4e0b6440768c6bb902628ec36e43757366be470f583169834a4c7c3d4cf54fd2`。文件名的 v3.1、主文件内部 1.3、收入政策附录表内 1.2 已采用记录，以及仍保留的 working draft 文字分别保存；没有据其中一个标签裁定今天有效的正式版本。

实际交付 [finance-author.json](finance-author.json) 含 **428 个研究单元**，不是 428 个 Council 项目：

| 内容 | 本部分实际范围 |
|---|---:|
| PDF 107–110 资本支出续表 | 41 条项目行；不是全 OP 资本项目分母 |
| PDF 112–117 服务预算 | 19 张表，155 条分项/合计行 |
| PDF 120–121 基金报表 | 30 条财务行，保留合并列及四基金列 |
| PDF 122–123 术语 | 49 条缩写 |
| PDF 118–119 | 4 张预算图，逐张读实际像素 |
| PDF 132 | 4 个税率类别示意地图面板，没有 Mining 面板 |
| 收入政策、版本、费率、减免、目录和结尾 | 其余 145 个单元，包含逐项条件及明确的外部文件缺口 |

完整 [36 页处置表](page-coverage.csv) 和 [428 单元覆盖表](unit-coverage.csv) 标明提取、作者/独立复核和待主任务集成状态。原始 PDF、全文和裁图只留在 `/tmp`；仓库中保存自写摘要、简短事实格及来源坐标/指纹。为保持现有应用治理边界，P142 的公开 Council 邮箱只记录联系方法存在及原件位置，不复写非必要地址；来源锚和明确省略状态保留。原文提及 CSP 的公开文件入口不等于具体策略行动关系，故没有虚构 CSP/LSPS 活动链接或预算分配。

**预算数字没有被悄悄“修好”。** [finance-diagnostics.json](finance-diagnostics.json) 保留 17 条诊断：8 条服务表显示数加总差异、4 条基金现金净变动实质不一致、以及 5 条版本或政策内差异。服务表的 ±1 千元差异可能与显示精度等有关，但原件未说明原因，不能断言只是四舍五入。PDF 121 的 General/Water/Sewer/Waste 净变动印为 585/616/616/616（$000），与本页期末减期初得到的 2,935/−4,880/−262/1,783 不同；原印值和计算检查并存。合并列 −424 没有这项差异，融资行破折号也未被当成零。

资本表中的 swimming-pool carryover 项目值为空，三个资金来源格为 0；空白项目值没有改为零。Wastewater 资产组下出现 Water Mains/Water Treatment 名称的原始分类张力也保留。Fleet and Plant 的 Materials & Contracts（含 recharges）为 `(1,331)`，保持负值。图中的 Other 26.94 M 是 Sewer 14.46 M 与 Waste 12.48 M 的组合，不能作为第五个基金重复相加。`$`、`$'000`、`$000`、`M` 与年度均逐格保存，币种代码没有从地理位置推断为 AUD，年度项目值没有解释成全生命周期成本。

**政策条件与金额一起保存。** 包括燃油附加费尚未启用、四年 52.48% SRV 已包含 rate peg、旧 Snowy River 换桶附加费的 Council 决议前提、多单元 FOGO 自愿加入、Council 主动换桶免该项费用、商业收费由月发票改为年度评税账单、雨水费只限指定旧区域且有服务条件、OSSM 年费排除初装/转移/复查等费用、养老金 ordinary rates 与 domestic waste 合计共用最高 $250 年度减免、受限用途基金内部借款须先获部长批准，以及 CEO 仅在请求后调整 non-legislated fees 的范围。

原件的两组 FOGO 范围/频率差异、商业回收 360L 的两个价格行和正文频率、以及一处 Act 1933/1993 年份冲突均显式列出，未替 Council 选择“正确答案”。水、污水、liquid trade waste 等另行 Schedule of Fees and Charges 在本文件仅被引用，本次未取回，因此不能说所有收费金额已覆盖。评级地图只说明原页红色类别分布，不提供 GIS 坐标、单地块分类、现行费率准入或新税单计算。

PDF 111 的可见页面是设施照片，native text 中的脚注被照片遮挡。已把它单列为 `HIDDEN_OR_OCCLUDED_TEXT_LAYER` 观察；其 `printedPage` 留空，不能以文字层 hash 证明可见脚注或项目交付。

验证命令（仓库根目录）：

```sh
python apps/public-strategy-atlas/qa/op-completion-20261102/finance/build_finance.py
python apps/public-strategy-atlas/qa/op-completion-20261102/finance/verify_finance_author.py
```

[原件验证回执](finance-source-verification.json) 重读 1,576 个文字锚、543 个直接数值格、9 个逐裁图独立打开原件生成的 v2 像素锚；155 条服务预算行另按原件 Income Total 的实际纵向位置检查收入/支出角色。17 个负例涵盖改金额、基金列互换、千元变元、年份反转、负值变正值、空白补零、跨收入合计错分类、隐藏字当可见证据、删除政策限制、重复加算 Other、压掉冲突及缺失源行，均被拒绝。这些检查证明限定的来源/数值/语义断言，**不把 hash 或计数当成全文理解的证明**。

独立审读者实际读过全部 428 单元，发现最初作者稿的 14 处问题：4 条服务行收入/支出误分、基金 Net Gains/结果/余额的角色或语境继承错误，以及隐藏脚注可见性误述。作者修复后重新计算诊断；首次缺陷保留在 [author-findings.json](../independent/author-findings.json)，最终读回见 [finance-readback-review.json](../independent/finance-readback-review.json)。另见 [cashflow-source-check.json](../independent/cashflow-source-check.json)。截至该次作者稿读回，无尚未解决的作者语义误述被识别；这不是对源文件本身矛盾的消除，也不是对未来漏项作绝对保证。

下一步由主任务把这些单元映射到原应用，验证真实模型投影、搜索/阅读/导入导出、撤回等负例，以及桌面和手机显示，再按授权发布原 Council 私人站点。本子任务没有提交、合并或部署，没有访问私人账簿、Council/customer 数据或修改另一个 ClimateOS 水文站。当前法律适用性、正式来源准入、现时金额与实际执行仍为 UNKNOWN；本研究不生成 Council 的正式义务或个人账单。
