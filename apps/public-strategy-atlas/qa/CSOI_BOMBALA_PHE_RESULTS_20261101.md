# Bombala PHE historical review batch — 1 November 2026

This bounded engineering batch extends the existing PR #130 app. Full CSOI acceptance remains **PARTIAL**, with **49 VERIFIED / 28 PARTIAL / 3 BLOCKED** engineering tasks. No task status or source admission is promoted by this batch.

## Founder-facing result

这批把已经核过来源的 Bombala 历史材料，接进了现有“现场污水知识 → 自己安排复核 → 工作卡 → 年度日历”的流程。原来的六张 Snowy/Cooma 阅读卡保留，新增五张 Bombala 阅读卡，共十一张。你可以分别查看 subdivision 与 rural-development 的材料、原文页码、适用前提和版本，再选择自己的阅读复核日期。

页面新增两项明确的缺口：**现行规则及地块适用性**、**现行检查策略**。历史资料、个人复核日期都不能补上这两个缺口，也不会自动生成 Council 检查义务、责任人或法定检查期限。土壤证据卡现在直接显示它继承的“没有管网污水服务”前提，避免只看到叶子条目而漏掉上级条件。

这批只更新原有 Draft PR。现有仅本人可访问的试用网站仍是此前发布的 v1，**尚未包含本批或后续的 P0/P1 修正**；本批没有部署，也没有更改另一个 ClimateOS 水文网站。可先查看下方本次真实浏览器截图。发布范围须由父任务复核确认后再推进。

## Reconciliation and scope

The clean canonical checkout `/workspace/eco-agent-system` started at `744ab46b2bec2ad601da0c4ae528694a4c982154`. Remote had advanced to `ad203014caa2fb2c67b7457b2d720b528baa6a7a`; it was fast-forwarded before edits. All P0/P1 append-only corrections from `cca314ce244235895779676a222e22537949dcc8` are preserved, including corrected Snowy §4.2 drainage, original withdrawn §4.1 history, AMP PDF13, 25 pinned source notes and the ≥110 minimum.

Latest NEXT_SESSION also describes a larger CSP/LSPS/OP follow-up with allegedly uncommitted source data and verifiers. Those files are absent from this checkout. The still-open COI-043 next action and the parent's direct delegation support this independent Bombala batch. The larger follow-up remains pending; its source records were not invented or rebuilt here. Intake evidence: [execution-intake.json](bombala-phe/execution-intake.json).

The five curated selections reuse existing identifiers, pages, registry and source receipts:

| Existing Bombala branch | Purpose | Original PDF page |
| --- | --- | --- |
| 3.1.5 P1 | Subdivision network availability and land capacity | 54 |
| 3.1.5 A8 | Conditional R5 connection and network capacity | 55 |
| 3.1.5 A9 soil facet | Soil evidence when reticulated sewerage is unavailable | 55 |
| 4.5.4 A2 | Rural disposal envelope and soil report | 85 |
| 4.5.4 A3 | Historical rural waterway-distance reference | 85 |

Adjacent performance criteria and acceptable solutions are not automatically paired. Parent context carries exact revisions, page anchors, conditions and exceptions. Bombala/Snowy and Bombala/Cooma comparison links retain geographic CONFLICT and UNKNOWN admission. Own-date review tasks use the existing model/calendar and exact source/clause pins; planned hours are ASSUMED, actual hours/spend/outcomes UNKNOWN, Council assignments NOT_CREATED. Gap cards are reading aids, not graph entities or claimed current sources.

No new corpus records or facts: **137 domain entities / 48 assertions / 127 legacy items / 15 stations**; **74 DCP observations, 73 active + one withdrawn**; **52 source records / 31 families / 33 byte receipts**. Default digest is unchanged:

`sha256:53841d668ffdb78a42edb9ad515a64dcb6956dd390b6c777531f2c4d72311375`

## Source and negative evidence

The exact registered Bombala lead was fetched using the existing bounded inherited-HTTPS tool. One selected attempt, two HTTP exchanges including the official-host redirect, final HTTP200; 3,644,692 bytes / 108 pages. SHA-256 `91375ba17012f891593bb200a533d3de12e6e48e579b1d7e9212af0be66a7ee6` matches the retained historical receipt. All ten original page anchors pass again; four deliberately corrupted raw/page/bounds/token manifests reject. See [access receipt](bombala-phe/source-access.json), [page checks](bombala-phe/original-page-verification.json) and [negative checks](bombala-phe/original-page-negative.json). Original PDF remains temporary and is not committed. The existing 2012-cover/2014-directory, historical amendment wording and discontinuous pagination conflicts remain.

Native and browser negatives distinguish withdrawing the subdivision parent from withdrawing the entire Bombala source. Existing plans/history remain readable; stale contexts cannot create new plans; unrelated rural or Snowy/Cooma branches stay usable as appropriate. Wrong-page, foreign-source and missing-record contexts reject. A personal review does not resolve current-rule or inspection-strategy gaps. Exported snapshots and path proofs are independently revalidated.

## Validation

**PASS 42/42 native files and 17 real Chromium leaf suites on final application code.** The browser count is one new Bombala PHE suite, nine affected existing suites, all six legacy suites and one P0/P1 remediation suite. Desktop 1440×900/mobile 390×844, 24 registered routes × five viewports, explicit export/import, parent/source withdrawal, local save/load and conflict regressions pass. The remediation browser rechecks original histories, all 25 source-note pins, corrected drainage, AMP and ≥110 behavior. The native cache test passes full default and synthetic-fixture equivalence.

Machine packet: [results.json](bombala-phe/results.json); [native results](bombala-phe/native-results.json); [new browser results](bombala-phe/browser-results.json); [aggregate browser log](bombala-phe/browser-regression.log); [remediation results](bombala-phe/remediation-regression/phase1-browser-results.json). Fresh aggregate outputs are archived under `bombala-phe/regression/`; prior tracked evidence was restored rather than silently relabelled.

The first new browser attempt failed because its assertion expected JSON punctuation in a definition-list value. The assertion was corrected to inspect the exact `dt`/`dd` value; application behavior and timeouts were not relaxed. [Initial log](bombala-phe/target-browser-initial.log) and [passing target log](bombala-phe/target-browser.log) remain separate. Existing PHE tests now expect eleven cards, existing Bombala/Cooma browser census checks use the remediated 137-entity/74-clause baseline, and the legacy reconstructed default applies the existing remediation stage while preserving its original legacy-base digest test. Historical fixture-only native output may still describe its deliberately unremediated 135/72 fixture; that is not the default app census.

Node coverage was **not rerun**. Real Chromium viewport emulation is not physical-device, cross-browser or professional screen-reader certification. No independent CI pass is inferred from local results. Code/evidence commit `129b35d2e400f5fd372f5eafac3b3a5048f1bb53` is pushed and matches both git remote and GitHub PR #130 head, OPEN/DRAFT/unmerged. [Readback](bombala-phe/pr130-readback.json) returned no commit statuses or PR-triggered workflow runs. A subsequent documentation-only checkpoint records this result.

## Actual screenshots and next work

- [Desktop evidence gaps](bombala-phe/evidence-gaps-1440.png)
- [390px Bombala soil conditions](bombala-phe/bombala-soil-390.png)
- [Desktop rural-development reading](bombala-phe/bombala-rural-1440.png)
- [390px review calendar](bombala-phe/bombala-calendar-390.png)
- [390px source withdrawn, historical work retained](bombala-phe/bombala-withdrawn-390.png)

The test server is temporary loopback only; it is not a preview URL reachable from the Founder's PC. The published private trial remains the separate, previously documented version. No Sites management, deployment, access or water-site calls were made in this batch; this is an absence-of-mutation statement, not a fresh live metadata comparison.

Next: reconcile the missing source-primary CSP/LSPS/OP files with their original task before integrating verified originals through the existing knowledge/cache/UI contracts. Current-rule, inspection-strategy and parcel/authority admission remain separate evidence work. Private WCOS tasks COI-002/031/040 remain deferred. No merge, deployment, private-data import, purchase, new credentials or permission expansion occurred.
