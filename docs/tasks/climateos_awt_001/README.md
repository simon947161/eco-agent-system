# CLIMATEOS–AWT–001 · 可信甲烷减排与环境主张验证试点

唯一正式任务：[Issue162](https://github.com/simon947161/eco-agent-system/issues/162) / [原文](TASKBOOK.md)。2026-11-23，独立stacked Draft，父基线PR145 `ae1050a621ac794e447f9ac047865d90b2f04b03`。P0–P3为有界合成教学原型，科学PENDING，真实主张DATA_NOT_READY。

先读[中文12页验收报告](FOUNDER_ACCEPTANCE_CN.md)，或下载整个仓库后本地打开[index.html](index.html)。GitHub源码页不会执行翻页；网页无后端、无自动外连，未部署。

- [已有资产与缺口](EXISTING_ASSETS_AND_GAPS.md)
- [1000t四情景、公式与敏感性](COUNTERFACTUAL_CASE_1000T.md)
- [法规版本](LEGAL_METHOD_VERSION_REGISTER.md) / [来源登记](sources.json)
- [护照schema](CLAIM_PASSPORT_SCHEMA.json) / [兼容映射](PASSPORT_INTEGRATION.md)
- [测试与保证边界](ASSURANCE_DECISION_TESTS.md) / [实际输出](evidence/results.json)
- [下一轮](NEXT_SESSION.md) / [科学评审请求](REVIEW_REQUEST.md) / [CRP](CRP_HANDOFF.md)

## 离线复算（仓库根目录，Python3标准库）

```sh
python docs/tasks/climateos_awt_001/engine.py
python -m unittest tests.test_awt_claims -v
python docs/tasks/climateos_awt_001/verify_package.py
```

改动本目录源代码后才运行 `build_examples.py` 更新有明确新版本的作者fixture及代码hash，再运行 `engine.py`、`run_validation.py` 和 `build_report.py`。不要把重新生成hash当作原始材料未经改动的证明。正常审阅先verify，不重新封存manifest。全部目录必须在仓库中，核心实际调用PR144/145已有模块，不能只复制此目录脱离父依赖运行。

本轮没有实现法定碳计算器、生产接入或独立审核角色系统。FOGO具体法条/豁免、合格废物流、遗留项目状态、真实capture及digestate端点均须专业证据。敏感性可变负值；全部credit_quantity为NOT_DETERMINED。PR132独立索引保持原样，本分支经既有PR145知识索引和NEXT_SESSION关联，不合并历史分支。
