# P04 CASE001: native monthly metadata and HRS semantics acceptance

2026-10-27 Australia/Sydney. Baseline `f5967f25d2829183b8fb60cd3cc178c3927f1a75`; responds to [Issue128 comment6426885565](https://github.com/simon947161/eco-agent-system/issues/128#issuecomment-6426885565). Outcome: **PARTIAL; numerical join BLOCKED**. No environmental or causal result.

## Actual execution and provenance

Reused the accepted Geofabric V3.3 boundary and existing historical Receipt/Passport references in `P04_CASE001_READINESS.json`. No geometry rebuild, Sites deployment, P02/P03 rerun, WaterNSW credential search or paid operation.

Read the official [NCI monthly catalogue](https://thredds.nci.org.au/thredds/catalog/iu04/australian-water-outlook/historical/v1/AWRALv7/processed/values/month/catalog.html), followed its fileServer and OPeNDAP links, and captured native NetCDF4/HDF5 metadata plus coordinate samples for `rain_day.nc` and `sm_pct.nc`. Each native file required ten HTTP206 ranges of8192 bytes: 81920 bytes each, 163840 total. Full file sizes were702814481 and1347725821 bytes respectively; neither whole file was downloaded. No precipitation/soil array was indexed, no basin subset or numerical join computed. Block alignment can include adjacent bytes; this is not a claim that every received byte was metadata.

`evidence/p04_semantics_20261027/manifest.json` contains exact SHA256 values and source URLs for each saved DAS, DDS, coordinate response, licence, monthly CSV and derived native-header JSON. Native JSON also records range offsets/digests, capture timestamp and HTTP Last-Modified. Exact range bytes remain in ignored local storage, not the repository. Full-file SHA256 is deliberately null. Native metadata excludes HDF5 internal dimension-reference attributes and `_NCProperties`; these are not science attributes. Independent DAP snapshots agree on units, types, dimensions and sampled coordinates.

Reproduce the bounded read with Python plus optional isolated `h5py==3.15.1` / `numpy==2.5.4`:

```powershell
python -B tools/inspect_awra_netcdf_header.py --variable rain_day --output .local/p04-native-header
python -B tools/inspect_awra_netcdf_header.py --variable sm_pct --output .local/p04-native-header
python -B tools/verify_p04_semantics.py
```

The live tool permits only these two official URLs, refuses redirects/full responses, caps reads at512KiB/64 successful requests per file and checks file size/Last-Modified consistency. Last-Modified is not a cryptographic immutable revision: exact bytes and response digests identify this capture only. Later requests can differ as the publisher updates its files. No core runtime dependency was added.

## Acceptance matrix

| Item | Status | Observed evidence and limitation |
|---|---|---|
| Native variable storage | VERIFIED | Both Float32, shape1389×681×841, fill value−999. `rain_day` units mm; `sm_pct` units fraction of fullness and rootzone0–100cm description. |
| Packing attributes | VERIFIED absence | No scale_factor/add_offset, missing_value, valid_range or cell_methods on either physical variable. Do not invent those attributes or infer a percent conversion from an interface label. |
| Soil physical scale | UNRESOLVED | File declares fraction of fullness, not percent. No physical values sampled or empirical range checked; no multiply/divide by100 applied. Publisher contract still required for stored range/meaning. |
| Monthly statistic | UNRESOLVED | Filename path says month, while rain long_name remains Daily Rainfall. Bounds alone do not establish sum versus mean. Soil monthly mean versus month-end state and partial-month treatment are not specified in captured native attributes. |
| Calendar and coordinate units | VERIFIED | Gregorian, days since1900-01-01; time points to time_bounds. No explicit time-zone offset in units. |
| Sampled month boundaries | VERIFIED | Jan/Feb/Mar2000 labels are month-end dates. Bounds run first of month to first of next month, lengths31/29/31days. Latest label2026-09-30 has bounds2026-09-01 to2026-10-01. These are coordinate bounds, not proof of complete valid daily cells or physical UTC/local alignment. |
| File revision | VERIFIED with limits | HTTP last-modified26Oct2026 13:54:45GMT rain,13:55:37GMT soil. Native global date_created/date_modified remain September2021. Do not call either timestamp the last observation time. Model path AWRALv7; Conventions CF-1.6/ACDD-1.3. Immutable scientific revision not supplied. |
| Licence | VERIFIED | Catalogue-linked collection licence is CC BY4.0; source attribution retained in manifest. This covers obtained metadata, not scientific validity. |
| HRS provider monthly product | VERIFIED candidate | Official station download panel describes month-wise sums of gap-filled daily records, excluding partial first/last months. One actual February CSV captured:61rows,1965–2025, ML/month, no quality column. |
| HRS version/coverage | UNRESOLVED | Monthly CSV says September2026 but stops2025; source extraction-date text is4/06/2024. Accepted daily file ends2026-02-28. No silent fill, regeneration or assumption that all12 monthly files have identical coverage. |
| HRS reporting interval | VERIFIED declaration only | Daily and monthly headers declare a9am local report for the preceding24hours; extraction describes cubic metres while output columns use ML. Conversion provenance is not resolved by a dimensional conversion fact. |
| HRS DST/month assignment | UNRESOLVED | No explicit station-specific standard/civil-time choice, DST transition handling or interval-end/start month rule was found in reviewed header/download/FAQ/QC material. Annual water year Mar–Feb does not settle calendar month membership. No WDO midnight rule transferred. |
| Cross-product temporal compatibility | BLOCKED | Numeric calendar bounds do not resolve HRS hydrological-day offset or AWRA underlying daily accumulation window. |
| Basin numeric completeness/QC | BLOCKED | No physical arrays read; existing boundary review remains separate. Daily E/C/G flags cannot be discarded simply because a monthly total exists. |

Native coordinate results are machine-readable in `P04_SEMANTICS_RESULT_20261027.json`. Only sampled months were decoded; this is not a full1389-month continuity validation. No unsupported assumption was promoted to VERIFIED.

## HRS monthly reuse decision

The official [410033 download panel](https://www.bom.gov.au/water/hrs/#id=410033&panel=data-download) offers twelve monthly files. The actual [February CSV](https://www.bom.gov.au/water/hrs/content/data/410033/410033_monthly_total_02.csv) is preserved with original header and source licence attribution. Prefer publisher totals as a candidate reference after resolving coverage and aggregation membership. They could avoid rebuilding all totals, but cannot replace daily quality screening: this sample has no QC column. No daily/monthly numerical reconciliation was performed while the unit/time contract is unresolved.

Supporting literature: [Fowler et al., CAMELS-AUS2021, §3.5.2](https://essd.copernicus.org/articles/13/3847/2021/essd-13-3847-2021.html) discusses NSW9am consistency and time-zone/DST limitations. It supports the need for caution, not a station410033 September2026 product guarantee. [HRS QC documentation](https://www.bom.gov.au/water/hrs/qc_doc.shtml) describes E as accuracy not known and notes provisional WaterNSW quality mappings. Preserve original codes and existing display warnings; do not recode them from this review.

## Validation and rollback

Test results are in `P04_SEMANTICS_TESTS_20261027.md`. Offline acceptance checks authenticate saved evidence, reject changed unit/calendar/bounds, and retain the join gate. HTTP guard tests reject full/oversized/wrong-range responses and changed file size. These tests establish implementation behavior, not scientific truth. Full regression runs in an isolated copy so four pre-existing generated-report edits remain untouched and unstaged.

Rollback: revert this implementation commit on the same branch; no database migration, source-record mutation or deployment requires rollback. Native fetch outputs are ignored local research evidence. The source manifest pins baseline and tool path; the enclosing Git commit pins tool/evidence/state together. Site remains existing owner-private v2, unchanged and not re-tested in this round.

## Conversation Radar and next executable work

- Knowledge: native bounds and units are now observed; publisher monthly flow sums exist.
- Decision: retain accepted geometry and keep numerical join BLOCKED.
- Idea: reuse official monthly totals with daily QC retained, subject to product-contract acceptance.
- Risk: stale extraction metadata, incomplete monthly coverage, ambiguous aggregation/scale and DST alignment can create false comparability.
- Open questions: see `P04_UNSENT_TECHNICAL_QUESTIONS_20261027.md`; no message sent to providers.
- Next action: obtain provider documentation or written clarification for those specific product paths and410033 version; then test one complete month plus one DST-transition month with an explicit day-membership/QC rule before admitting any basin values. Sending provider questions needs a separate user instruction; Issue128 reporting is already authorized.
- Keywords: ClimateOS, CASE001, AWRA-Lv7, HRS410033, time_bounds, cell_methods, monthly semantics, Evidence Passport, Run Receipt.
