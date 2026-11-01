# P04 same-cell daily/monthly reproduction — 2026-10-31

**PARTIAL batch; soil comparison PASS; rainfall comparison BLOCKED; cross-source numerical join remains BLOCKED.** This is an empirical product check, not formal publisher semantics, catchment admission, environmental analysis or complete ClimateOS delivery. Continues Draft PR #129 from `67bc471ebeaab02cd09b0ee9dd8edd917483f3fc`.

## What this run answered

For one grid cell at **36.25°S, 149.10°E** (zero-based latitude index 525, longitude index 742), in **July 2000**, the exact NCI monthly `sm_pct` agrees with the arithmetic mean of all 31 daily values within the predeclared Float32 rounding tolerance. It does **not** agree with the final-day value.

| Raw fraction-of-fullness quantity | Value |
|---|---:|
| Official monthly `sm_pct` | 0.13241834938526154 |
| Mean of 31 official daily `sm_pct` values | 0.13241835275003988 |
| Official July 31 daily `sm_pct` | 0.10436807572841644 |
| Monthly minus daily mean | -0.000000003364778344838726 |
| Monthly minus final day | 0.028050273656845093 |

Both candidate comparisons were specified before the final binary capture. Tolerance is `max(1e-7, abs(reference) * 2e-6)` for raw soil fractions, an allowance for Float32 rounding, not measurement uncertainty. Mean tolerance is 0.0000002648367055000798; month-end tolerance is 0.0000002087361514568329. The agreement is clear for this sample. This **narrows the earlier month-end hypothesis**: the drought-map presentation cannot be assumed to define this exact NCI monthly product. A single sample does not prove the reducer for every cell, month or revision.

The same-cell monthly `rain_day` value is **11.300000190734863 mm**, decoded from Float32. No matched daily rainfall series was obtained, so there is no rainfall sum, mean or equality result. Missing daily data is not zero.

## Exact sources and negative evidence

All sources are public Bureau of Meteorology AWO historical v1 / AWRA-L v7 data distributed by NCI. The captured collection licence is CC BY 4.0. Attribution: Bureau of Meteorology, Australian Landscape Water Balance AWRA-L; NCI distribution; ClimateOS extraction and calculations.

- Daily soil: [`processed/values/day/sm_pct_2000.nc`](https://thredds.nci.org.au/thredds/catalog/iu04/australian-water-outlook/historical/v1/AWRALv7/processed/values/day/catalog.html); indices 182–212, inclusive.
- Monthly soil: [`processed/values/month/sm_pct.nc`](https://thredds.nci.org.au/thredds/dodsC/iu04/australian-water-outlook/historical/v1/AWRALv7/processed/values/month/sm_pct.nc.html); index 1074.
- Monthly rain: [`processed/values/month/rain_day.nc`](https://thredds.nci.org.au/thredds/dodsC/iu04/australian-water-outlook/historical/v1/AWRALv7/processed/values/month/rain_day.nc.html); index 1074.
- [Official README](https://thredds.nci.org.au/thredds/fileServer/iu04/australian-water-outlook/historical/v1/README.md) gives annual daily filenames and the top-level directory convention. Its convention-derived `AWRALv7/rain_day_2000.nc.dds` returned **HTTP 404**, with exact 84-byte error body preserved. This is an unverified candidate, not a claimed existing product.
- The captured [top-level AWRA catalogue](https://thredds.nci.org.au/thredds/catalog/iu04/australian-water-outlook/historical/v1/AWRALv7/catalog.html) and processed daily catalogue contain no `rain_day_2000.nc`. The latter lists only five soil variants for 2000. This establishes the inspected endpoint gap, **not** that no official daily rainfall source exists anywhere.

**Exact missing fact:** a publicly accessible daily rainfall product with documented lineage to the exact NCI monthly `rain_day.nc`, providing the same cell's complete July 2000 calendar labels and values. An unrelated gridded rainfall product or another provider service is not silently substituted. No provider enquiry was sent.

## Reproducibility and provenance

Machine-readable result: [P04_AWRA_REPRODUCTION_RESULT_20261031.json](P04_AWRA_REPRODUCTION_RESULT_20261031.json). Exact source bodies, request URLs/constraints, UTC retrieval timestamps, HTTP status/selected headers, byte lengths and SHA256 receipts: [evidence manifest](evidence/p04_awra_20261031/manifest.json).

The final reproducible acquisition ran **2026-10-31 08:17:18–08:17:31 UTC**: 21 HTTP requests, 402,356 response-body bytes (including catalogue metadata and the 404 body). Physical subset responses total only **1,517 bytes**: 629 daily soil, 441 monthly soil, 447 monthly rainfall. They contain 33 physical scalar values in total. These totals describe the final acquisition; earlier bounded catalogue discovery and ASCII probes are additional local diagnostic traffic. No national physical array or full NetCDF file was downloaded.

| Source | HTTP Last-Modified, stable before/after | Full source size from HEAD, not bytes downloaded |
|---|---|---:|
| Daily soil 2000 | 2021-10-01 05:07:14 GMT | 330,799,618 |
| Monthly soil | 2026-10-30 14:00:33 GMT | 1,354,589,298 |
| Monthly rainfall | 2026-10-30 13:59:40 GMT | 704,425,413 |

Each successful source was bracketed by HEAD requests with unchanged Last-Modified, Content-Length and ETag (where supplied). Exact product-global creation/modification attributes are retained in DAS and result JSON. These header checks do not supply an immutable revision or eliminate a possible stale service cache. Daily and monthly source revision timestamps differ. No whole-file SHA256 is claimed; SHA256 identifies each captured response body. DAP2 is a server-produced subset of the native product, not a native NetCDF byte range.

`tools/reproduce_awra_month.py` uses only Python's standard library. It decodes the DAP2 binary arrays directly, preserving IEEE Float32 values without decimal-rounding inference. It accepts only the fixed source/query plan, blocks redirects, limits the batch to 32 requests / 2 MiB body bytes, limits each data/metadata response, refuses full-file GETs and refuses to overwrite a capture directory. HTTP errors retain bounded response bytes and status. No credentials or paid service are used.

Time checks require exactly 31 unique consecutive daily labels, 36706–36736 (`days since 1900-01-01`, Gregorian), monthly label 36736, and monthly bounds [36706, 36737]. The actual coordinate values must match in each source. These are product calendar labels: no UTC offset, hydrological-day alignment or HRS interval interpretation is inferred. July has no Sydney DST transition; a second month is unnecessary for this reducer comparison.

Fill/mask policy: `_FillValue = -999`, finite values only, no negative rain, raw soil fractions within 0–1. All 31 daily soil values and both monthly samples were valid; zero fill/nonfinite values. Any missing day, duplicate date, unexpected cell, new packing/mask attribute, changed unit/calendar, changed revision, fill or nonfinite value blocks the affected comparison. No zero-fill, dropped-day mean, interpolation, reprojection or unit conversion is performed. Basin masks and numeric completeness remain untested.

Replay with no network:

```bash
python -B tools/reproduce_awra_month.py
python -B -m unittest tests.test_p04_awra_reproduction tests.test_p04_semantics tests.test_p04_spatial_admission tests.test_p04_preflight
```

A new explicit live capture requires a new, unused local directory:

```bash
python -B tools/reproduce_awra_month.py --fetch --directory .local/p04-new-capture --result .local/p04-new-result.json
```

Later source revisions or availability may differ. Existing captures are not overwritten. The rainfall sum branch is tested with explicitly synthetic values solely in a unit test; that fixture is not placed in the evidence package or represented as rainfall observations.

## Validation and generated-output inventory

- 15 new offline tests pass, covering real replay, binary decoding, missing rainfall, fill/nonfinite/out-of-domain values, dates/cells/bounds, units/calendar/packing, revision changes, tampering, safe fetch bounds and explicit synthetic rainfall arithmetic.
- Combined P04 suite: **35 run, 31 passed, 4 skipped** for unavailable optional GIS audit dependencies. The four skips are existing geometry tests, not new test failures; geometry was not redone.
- Full repository suite in an isolated copy: **533 run, 529 passed, 4 skipped**, exit 0. Generated baseline outputs stayed inside the isolated copy. Python 3.12.14. No new dependency installed.
- Evidence replay and committed result are checked for exact structural equality. Source hashes/lengths are verified on every replay. Passing tests establish implementation behavior, not scientific admission.

Committed outputs are the evidence directory (producer: explicit `--fetch`, exact live public response bodies and manifest; capture creation only), result JSON (producer: offline script `--result`, overwrites the explicitly chosen result path), this report, runtime checkpoint, execution state and handoff. Consumers are P04 evidence review and regression tests; no site or operational runtime consumes these arrays. The result always keeps `scientific_admission=false` and `cross_source_numeric_join=BLOCKED`. Source unavailability produces missing evidence and a partial/blocked result. Local discovery probes, regression copy and logs are ignored `.local` diagnostics, not deployed artifacts. Rollback is a normal revert of this batch; no database migration or site rollback is involved.

## Remaining gates and next action

1. Rainfall reducer: **BLOCKED**, pending the exact matched daily source/lineage above.
2. Soil reducer: **PASS empirical mean agreement for this sample**, general publisher contract still unproven.
3. HRS daily/DST interval alignment: **UNRESOLVED**, untouched by this AWRA-only test.
4. HRS monthly quality/completeness and terminal-month omission: **UNRESOLVED**, daily QC remains required.
5. Catchment-grid mask/completeness and scientific-equivalence admission: **BLOCKED**, no catchment arrays or numerical join computed.

The next bounded action is to identify an officially documented daily rainfall counterpart for this monthly product (or obtain a product-specific clarification if Founder separately authorizes outreach). Reuse this frozen soil result; do not repeat the HRS sum review, soil scale review, P02/P03, geometry or Sites work. No DST sample is requested until a real time-boundary question requires it.

Existing owner-private ClimateOS Sites v2 remains the historical HRS website. This engineering evidence has **not** been deployed there. P03 local retrospective links, WaterNSW's zero authenticated requests / missing credential binding, and the absence of unattended updating remain unchanged. PR #130 is a different workstream and was not edited. No Founder credential, file transfer or new taskbook is needed for this batch.
