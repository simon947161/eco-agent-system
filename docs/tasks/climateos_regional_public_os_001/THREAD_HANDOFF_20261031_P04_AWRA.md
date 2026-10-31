# ClimateOS PR #129 — continuation handoff, 2026-10-31

Continue existing `codex/regional-public-os-001-taskbook`, not PR #130. Baseline
for this batch was `67bc471ebeaab02cd09b0ee9dd8edd917483f3fc`; main independently
remained `9eb7577e145e76161f9f1cd8509348b19c2904cc`. Read current remote HEAD before
resuming; the enclosing commit contains the implementation and captured evidence.

Read `P04_AWRA_REPRODUCTION_20261031.md`, its result JSON and evidence manifest.
Actual isolated runtime: `/workspace/climateos-pr129`. The original Council
checkout `/workspace/eco-agent-system` was not edited.

**Done:** bounded same-cell July2000 AWRA test; 31 complete daily soil values
and matching monthly soil/rain samples; exact DAP2 bytes, timestamps, metadata,
hash receipts, replay code and 15 new passing tests. Monthly `sm_pct` agrees
with daily mean (difference -3.36e-9) and not final day (difference +0.02805).
This is sample-specific empirical evidence, not a general product contract.

**Blocked action:** test monthly rain against daily sum. Exact target is the
matched daily counterpart of NCI `AWRALv7/processed/values/month/rain_day.nc`.
Official catalogue inspection found no daily rainfall file; the official
README-convention candidate `AWRALv7/rain_day_2000.nc.dds` returned HTTP404.
Daily soil/monthly products succeeded. This is a confirmed source-availability
failure, not permission denial or an uncertain write. The missing fact is
accessible, documented matched daily product/lineage for this cell/month.
Do not fabricate samples or substitute AGCD/another service as equivalent.

**Next bounded task:** find product-specific official documentation identifying
that daily rainfall counterpart or directly specifying the exact monthly
reducer. Preserve this soil result and the already verified HRS monthly sum /
AWRA soil scale reviews. Existing provider questions stay UNSENT unless
Founder explicitly authorizes outreach. No DST month is needed until there is
a specific time-boundary question.

**Independent open gates:** HRS station410033 DST/interval/date alignment;
monthly QC/completeness and terminal-month omission; catchment-grid numeric
mask/completeness and scientific equivalence. Cross-source numerical join
remains BLOCKED. No basin arrays, correlations, causal or current-condition
conclusions were produced.

**Validation:** 35 targeted tests run, 31 passed, 4 optional-GIS skips. Full
suite in isolated copy: 533 run, 529 passed, same 4 skips. Offline result
reproduces from committed evidence. No new runtime dependency.

**Website and other work:** existing owner-private ClimateOS Sites v2 is the
historical HRS interface. No site source/version/access/deployment changed or
retested. P03 local retrospective links remain undeployed. WaterNSW stays
BLOCKED for local credential binding, zero authenticated requests. No automatic
updates were established. No merge, new PR, paid service, private Council files
or PR #130 edit.

Founder does not need to locate files, transfer taskbooks or supply credentials
for this completed batch. This is one engineering batch within ongoing
ClimateOS work; it is not full product delivery. End human reports explicitly
with “本次汇报讲完了；ClimateOS 整体工程尚未完成。”
