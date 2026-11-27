# 只读审计包

先读《中文审计报告.md》，然后查《审计矩阵.xlsx》或各CSV。所有统计固定GitHub PR130提交 `744ab46b2bec2ad601da0c4ae528694a4c982154`，日期为2026年10月31日，用户时区Australia/Sydney。

本包是审计文档、自己的核验脚本、公开来源元数据、短事实摘要和本地界面截图。**不包含原始PDF／HTML、受保护Council数据、凭据或整个项目代码**。原件在临时目录进行对照，没有再发布。

复现时先在Linux隔离临时目录建立同样布局（脚本保留实际审计路径以便检查）：

```sh
mkdir -p /tmp/csoi-integrity-audit-20261031
git clone --depth 1 --branch feature/public-strategy-atlas-web-mvp-20261029 --filter=blob:none --sparse https://github.com/simon947161/eco-agent-system.git /tmp/csoi-integrity-audit-20261031/readonly-head
git -C /tmp/csoi-integrity-audit-20261031/readonly-head sparse-checkout set apps/public-strategy-atlas docs/research/public-strategy-atlas
git -C /tmp/csoi-integrity-audit-20261031/readonly-head fetch --depth 1 origin 744ab46b2bec2ad601da0c4ae528694a4c982154
git -C /tmp/csoi-integrity-audit-20261031/readonly-head checkout --detach 744ab46b2bec2ad601da0c4ae528694a4c982154
git -C /tmp/csoi-integrity-audit-20261031/readonly-head rev-parse HEAD
```

若分支已前进，必须另取上述固定提交；不能用新的HEAD冒充本次输入。将本包的scripts/coverage/relationships/carbon/e2e/clause-semantics放在审计根目录下。Python需pypdf6.10.0、pdfplumber、Playwright及系统Chromium，模型脚本需Node；未要求安装到原仓库。

```sh
python3 /tmp/csoi-integrity-audit-20261031/scripts/recover_originals.py
python3 /tmp/csoi-integrity-audit-20261031/scripts/csp_strategy_census.py
node /tmp/csoi-integrity-audit-20261031/scripts/export_audit_input.cjs
python3 /tmp/csoi-integrity-audit-20261031/coverage/reproduce-coverage.py
node /tmp/csoi-integrity-audit-20261031/relationships/relationship-audit.cjs
python3 /tmp/csoi-integrity-audit-20261031/relationships/refine-matrix.py
node /tmp/csoi-integrity-audit-20261031/relationships/lineage-gap-check.cjs
node /tmp/csoi-integrity-audit-20261031/carbon/reproduce-carbon.cjs
python3 /tmp/csoi-integrity-audit-20261031/carbon/verify-carbon-original.py
node /tmp/csoi-integrity-audit-20261031/e2e/audit-model.cjs
python3 /tmp/csoi-integrity-audit-20261031/e2e/audit-originals.py
python3 /tmp/csoi-integrity-audit-20261031/e2e/audit-browser.py
node /tmp/csoi-integrity-audit-20261031/e2e/audit-note-binding.cjs
```

E2E浏览器脚本自带临时HTTP服务，使用127.0.0.1:8891并在结束时关闭；不要同时启动其他8891服务。浏览器脚本只读页面，不调用追加、保存或导入。不要运行会把结果写回项目QA目录的原有harness。PDF原文将来如变化，收据不匹配必须报告，不能更新本次审计输入以掩盖差异。

语义评估来自AI辅助逐项原文对照，不是获授权人工法律审查。token或hash检查只能复现定位与字节，不能自动证明摘要、条件、例外的全部语义。失败／UNKNOWN是审计结果的一部分。运行“负例接受”的复现应重现缺陷，而不是被理解为负例通过了安全要求。修复任务书仅为下一阶段提案，没有在本次执行。
