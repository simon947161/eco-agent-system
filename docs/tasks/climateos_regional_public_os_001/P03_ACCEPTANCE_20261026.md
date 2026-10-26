# P03 monthly evidence and source feasibility acceptance

Date: 2026-10-26. Parent #128; existing Draft PR #129. Recovery baseline: `67eb5574851844bbd4d6d187fbe4afd000aaa754`.

**P03-A VERIFIED. P03-B feasibility checks completed; operational data admission BLOCKED.** This bounded delivery does not complete all broader P03 taskbook/RADAR scope. No recent-data adapter or automatic update is claimed.

## Existing monthly cycle: actual result

The existing July 2026 MONTHLY cycle `COOMA-CYCLE-5B67DD16E0116301` was found in the original project's local runtime database. It remains `CYCLE_REVIEWED_ACCEPTED_AS_RESEARCH_RECORD`. No new cycle was created. A separate `research_evidence_references` table stores reference `HRS-CYCLE-LINK-5786CE400E77B343`; this is an explicit **posthoc reference, not evidence included in the original July review**.

All six original project tables were hashed before and after: unchanged. Repeating attachment returned the same reference. The reviewed cycle's original Receipt, Passport and decision were not amended. Existing `/program.html` now displays the supplementary reference read-only; browser verification found its posthoc label and the original disabled compile control. Browser testing used a database copy. No original observations or private local paths are included in this repository's acceptance artifacts.

The reference resolves the accepted HRS 410033 package, verifies the pinned index and shard SHA256 values, and exposes source Receipt `HRS-RECEIPT-E70B4670978ABFD6` and Passport `HRS-PASSPORT-3CCD749190E38305`. Source SHA256: `78e8188f3f445afa33ad466dd0554e653761ef617832b6df3a9eac6b1240ca1a`. Detailed digests and actual acceptance are in [P03_MONTHLY_REFERENCE_ACCEPTANCE.json](P03_MONTHLY_REFERENCE_ACCEPTANCE.json).

Coverage remains 1964-03-01–2026-02-28; September 2026 is a dataset version, not a last observation date. CC BY 3.0 AU and BOM/WaterNSW attribution remain attached. E quality records and time/header ambiguity remain preserved. This does not establish current conditions, drinking-water adequacy, pollution or causality. Scientific review is pending. Original Python automatic retrieval remains HTTP 403; no automatic updates were established.

## Parallel official source checks

| Check | WaterNSW Water Data API | Public WaterInsights ArcGIS river layer |
|---|---|---|
| Access observed | Official portal requires registration, login, product subscription and key | Unauthenticated metadata and bounded one-station query returned HTTP 200 |
| Station | 410033 coverage cannot be confirmed without product access | 410033, Murrumbidgee River at Mittagang Crossing; 288 rows, not truncated |
| Latest observation | Unverified | **2022-12-14 00:00 UTC**, unsuitable as recent operational observation |
| Publication timestamp | Unverified | `2022-12-14 15:10`, string timezone unspecified |
| Units and quality | Product schema unverified | No explicit flow/level unit or quality-code field; geometry `esriMeters` is not a flow unit |
| Licence | General WaterNSW copyright/attribution exists; product terms still required | Layer copyright blank; item metadata returned HTTP 200 with JSON error 403; exact-layer licence unverified |
| Automated access | Account/key and product conditions required | One-off public query success does not establish automatic-use permission |
| Fees, quotas, update frequency | Unverified; no purchase or subscription made | No fee incurred for these probes; no confirmed automation quota or update guarantee |
| Decision | Block adapter until entitlement, terms, costs, schema and freshness are confirmed | Do not admit as recent data; stale and missing unit/QC/licensing evidence |

Primary sources checked:

- [WaterNSW API portal](https://api-portal.waternsw.com.au/), [attribution](https://api-portal.waternsw.com.au/data-attribution), [general copyright](https://www.waternsw.com.au/copyright). General permission to copy/distribute with attribution is not proof of product access, price, quota or permission for all transformations.
- [Public river layer](https://portal.data.nsw.gov.au/arcgis/rest/services/Hosted/WaterInsights_Data_Public/FeatureServer/1?f=pjson). Query predicate `station_id='410033'`, `outFields=*`, `returnGeometry=false`; separate latest-date query ordered `date_ DESC`, limited to one row. The full bounded station query confirmed no truncation.
- [Data.NSW surface water monitoring catalogue](https://data.nsw.gov.au/data/en/dataset/surface-water-monitoring-streams). Its general CC attribution label does not resolve the exact ArcGIS item's terms or units.

Probe timestamps, response SHA256 values and sanitized metadata are in [P03_PUBLIC_SOURCE_CHECK.json](P03_PUBLIC_SOURCE_CHECK.json). Raw responses remain local because the exact layer licence is unresolved. No credentials were requested, no 403 bypass attempted, and no unlicensed numeric series was committed or merged with HRS. Quotas for other NSW API products were not transferred to these endpoints.

Alternatives: obtain owner-authorized WaterNSW product terms/key with confirmed zero cost; or assess a separately licensed BOM Water Data Online product. Neither is silently substituted or described as verified. Separate station identity, time, units, quality, rights and freshness gates must pass before implementing a recent-observation adapter. Future records must use a separate append-only operational store with observation and retrieval timestamps, source revisions and digests; never overwrite the HRS archive.

## Tests and reproduction

Run from repository root (PowerShell); `$ResearchDb` is the owner's existing local runtime database path, intentionally not published here:

```powershell
python -B tools/link_hrs_monthly_evidence.py --db $ResearchDb --cycle-id COOMA-CYCLE-5B67DD16E0116301
python -B -m unittest discover -s tests -p test_monthly_evidence_links.py -v
python -B -m unittest discover -s tests -p test_p04_preflight.py -v
python -B tools/p04_water_soil_climate_preflight.py
python -B -m unittest discover -s tests -v
node --test apps/regional-public-os/tests/worker.test.mjs
```

Actual results: monthly reference tests **5 passed**, P04 preflight **1 passed**; full Python suite **499 run, OK, 1 skipped** (56.766 s); existing Sites Worker **8 passed**. The full Python suite ran in an isolated local copy to protect four pre-existing generated-report edits. JavaScript syntax passed. Tests cover idempotence, nonmutation, corrupted/missing source, tampered reference, cycle scope, sidecar-only rollback, calendar coverage and no scientific conclusions. Unknown/mismatched evidence degrades to `UNKNOWN_REFERENCE_REVALIDATION_REQUIRED` rather than silently promoting evidence.

## Private deployment and rollback

Sites current version remains **2**, project `appgprj_6adefcfe720881918b4e32874f12dd86`. This turn's control-plane check confirmed owner caller, custom access, one viewer, zero groups and zero external users. No deployment or access-policy mutation occurred. Earlier hosted access/browser/rollback acceptance remains in [P02_SITES_PRIVATE_ACCEPTANCE.md](P02_SITES_PRIVATE_ACCEPTANCE.md); it is not represented as a fresh hosted UI test of this local P03 change.

Rollback only the supplementary link:

```powershell
python -B tools/link_hrs_monthly_evidence.py --db $ResearchDb --cycle-id COOMA-CYCLE-5B67DD16E0116301 --remove-reference-id HRS-CYCLE-LINK-5786CE400E77B343
```

This deletes only the matching sidecar row. Original records remain intact; sidecar deletion is covered by tests. A local pre-attachment database backup exists but is not published. Revert the P03 implementation commit to undo code; do not reset the worktree or overwrite the four unrelated reports. No Sites rollback is needed because no new deployment occurred.

## Conversation Radar / handoff

- Knowledge: source accessibility, freshness and research admissibility are different checks; the public layer is demonstrably stale for this station.
- Idea: stable, integrity-checked supplemental references preserve original reviewed monthly records.
- Decision: historical HRS and recent operational observations remain separate; fail closed on evidence corruption.
- Risks: API terms unknown; ArcGIS missing unit/QC/rights; unresolved source time interpretation and scientific review.
- Open questions: zero-cost WaterNSW entitlement; licensed spatially compatible precipitation/soil-moisture inputs.
- Next action: execute the metadata admission task in [P04_CASE001_TASK.md](P04_CASE001_TASK.md).
- Keywords: ClimateOS, T1, T2, T3, WaterNSW, HRS410033, Evidence Passport, Run Receipt, monthly research, catchment, soil moisture.
