# 工作包验收：2026-10-26

- `python -B -m unittest discover -s tests -p test_smrc_policy_console.py -v`：5/5通过。覆盖缺原件可见、匹配/不匹配摘要、未知摘要不可自动准入、私有类别与路径穿越拒绝、错误摘要与重复身份拒绝。
- `python -B tools/smrc_policy_console.py`：在用户提供的公开PDF本地目录实际运行。LSPS、2025DP、CSP均为 `MATCHED_RECORDED_VERSION`；2026DP与2026–27OP保持 `MISSING_LOCAL_COPY`。未联网，未改变原件。
- LSPS完整文本已读取可用并检查关键行动表。CSP摘要与前轮一致。DP版本表核实v1.6发布日期为2025-11-11，保留其历史身份。
- 当前DP/OP的精确链接由Council官网索引发现，web读取失败，未提供哈希或虚构其完整内容。
- `.local/`已列入忽略范围；本机来源目录只存在于私人交接/忽略配置。提交范围不含PDF、提取全文、SQLite、密钥或Council内部数据。

以上是本工作包的脚本与资料验收。尚未执行全仓库测试、Council Console界面集成、Sites部署或canonical KITTY主机验收。未来执行者不得将5项检查当作父任务P00–P10全部通过。


## Console integration checkpoint — 2026-10-26

- Integrated the policy context into existing `/program.html` and `/api/policy-context`; no second Console, no Bridge PR merge. Five policy version cards and three research lines share the existing monthly workflow.
- Seven targeted checks passed, including real HTTP serving and unavailable-evidence propagation without promotion. Full regression: 489 tests, OK, one skipped. A pre-existing test now reads the bilingual HTML explicitly as UTF-8 on Windows. JavaScript syntax and diff whitespace checks passed.
- Desktop in-app browser verified source/version selection, land/catchment and evidence/scenario switching, and navigation to linked CSP. Screenshot retained locally, not published. Mobile viewport was not checked.
- Repeated the read-only local resolver with permission-enabled execution: all three original recorded PDFs match; current DP/OP remain missing. The normal sandbox correctly returns inaccessible rather than claiming success. No originals were changed or uploaded.
- Retried both current DP/OP candidate URLs through the web tool; content remained inaccessible. No candidate hash or authority was invented.
- Policy packet digest is an integrity checksum, not an assessment Receipt/Passport or scientific conclusion. Existing monthly compilation/review remains the path to research Receipts/Passports.
- Sites deployment, unattended scheduling, canonical KITTY readback and parent P02 real-data/chart slice remain unverified. Parent mission remains in progress.

