# D3真实观测数据准入 — DATA_NOT_READY
2026-11-05（Australia/Sydney） · CARBONOS-D3-DATA-ADMISSION-001

按[Founder任务书6641339661](https://github.com/simon947161/eco-agent-system/pull/132#issuecomment-6641339661)和[Batch D评审6640903352](https://github.com/simon947161/eco-agent-system/pull/132#issuecomment-6640903352)执行。基线SHA：534728d77d84da336b51440519e0fc900041ffd1。最终SHA见本目录所属Git提交及PR评审请求。

**有界任务已完成；没有数据集获准入。** 三候选上限已用完，取得原始观测文件0个。实际尝试公开原件下载，并保存成功元数据及失败记录；不是只写计划。三个REJECTED均指本轮准入条件未满足，不表示数据在全球不存在、科学错误或永久不可用。

| 候选 | 实际结果 | 停止理由 |
|---|---|---|
| C1 NY移动CH₄ / Dryad | 官方HTML取得；官方Data.zip链接返回HTTP403 | 停止整候选，没有再试README或替代端点 |
| C2 Victoria污水塘 / Bai2026 | 原文数据可得性为按请求提供 | 未联系作者；无合格公开原件URL/数据许可 |
| C3 Egypt卫星 / Mendeley | web可读官方元数据；HTTP原页取回403 | 未获得文档化文件链接；不猜API或绕过 |

[准入报告](DATA_ADMISSION_REPORT.md) · [许可/原件摘要清单](LICENCE_AND_SHA256_MANIFEST.json) · [失败证据](FAILURES_AND_STOPS.json) · [字段时间审计](SCHEMA_AND_TIME_AUDIT.json) · [质量缺口](QC_MISSINGNESS_AUDIT.md) · [测量算子](MEASUREMENT_OPERATOR_AUDIT.md) · [D1/D3决策](D1_D3_DECISION.md) · [12页离线Slides](index.html)。

原始观测SHA、行数、QC、缺失率、时间与空间范围均为null。唯一取回文件的SHA属于官方**元数据HTML**，不能冒充气体数据摘要。该原件在本地仓库外只读保留，不上载页面正文。GitHub仅提交原创报告、来源定位、许可说明、失败与检查记录。

范围：本轮允许的结构/质量检查因无原件而未能执行；已执行的是工件与来源收据检查。本地UI PASS不是原始QC或科学验证。没有回归、排放估计、反演、GWP转换、模型/气候实验、年化、气象复算、联系作者、付费、认证绕过、私有Council访问、合并或部署。

**P1-A科学准入PENDING；全A/B/C继续DATA_NOT_READY。** 已停止寻找第四候选。不建议再自动开启同类文书批次；待ChatGPT审阅和Founder决定是否提供合法原件或暂停该路线。
