# P04 CASE001 — public-document semantic review (2026-10-27)

Status: **EVIDENCE NARROWED; NUMERIC JOIN REMAINS BLOCKED**

Scope: continuation from `THREAD_HANDOFF_20261027_WORK_RECOVERY_WATERNSW_P02_P04.md` and `P04_SEMANTICS_ACCEPTANCE_20261027.md`. This review does **not** repeat P02, P03, Geofabric catchment geometry, Sites deployment, WaterNSW credential recovery, or any previous numerical work. No provider enquiry was sent. No paid service, private Council record, whole national NetCDF download, basin array extraction, correlation, environmental conclusion, or causal conclusion was performed.

Baseline checked before this review: Draft PR #129 was open, unmerged and mergeable at HEAD `564b9f830efadc07341e2eeee9c33a181b5e6382`.

## New evidence and status changes

### 1. HRS monthly streamflow aggregation — publisher documentation now resolves the basic reducer

The Bureau Hydrologic Reference Stations product page describes **Monthly data** as monthly total flow in `ML/month`: the gap-filled daily data are split into 12 months and summed for each month separately, with partial months at the start or end of the time series excluded.

Source:
- https://www.bom.gov.au/water/hrs/

**Assessment: VERIFIED for the HRS published monthly product.** The earlier question “sum versus some other monthly statistic” is no longer a blocker for HRS monthly totals. This does not remove daily quality-code requirements, prove the exact implementation of the 2026 terminal-month exclusion, or prove UTC/DST alignment to AWRA.

The same HRS glossary states that discharge data are accumulated to a daily total at 9am for the previous 24 hours.

Source:
- https://www.bom.gov.au/water/hrs/glossary.shtml

**Assessment: VERIFIED declaration; exact civil/standard-time and DST physical interval still unresolved.** The text does not establish a station-specific UTC offset policy for 410033 across DST transitions.

### 2. February 2026 HRS monthly omission — discrepancy narrowed, not closed

The already-captured February monthly file ends in 2025 even though the accepted daily file extends through 2026-02-28. The HRS product documentation explicitly excludes partial months at the start and end of a time series.

This gives a plausible publisher-side explanation for why a terminal month may be withheld, but the documentation does not state whether February 2026 is intentionally classified as a partial terminal month in this release, nor why the monthly file's extraction metadata is stale.

**Assessment: NARROWED / STILL UNRESOLVED.** Do not synthesize February 2026 into the official monthly product.

### 3. AWRA-L `sm_pct` raw scale — official cross-service evidence supports a 0–1 fraction

The Bureau's official AWRA historical monthly ImageServer describes `sm_pct` as root-zone soil moisture (0–100 cm), unit **fraction of fullness**, with service statistics bounded approximately 0–1. The official daily service uses the same variable name/unit and likewise reports values up to 1.

Sources:
- https://image.wsapi.cloud.bom.gov.au/arcgis/rest/services/awra_historical/physical_month_crf_multivariable_all_data/ImageServer/multiDimensionalInfo
- https://image.wsapi.cloud.bom.gov.au/arcgis/rest/services/awra_historical/physical_day_crf_multivariable_latest_data/ImageServer/multiDimensionalInfo

The Bureau drought page explains the public presentation of root-zone soil moisture as a percentage of available water content relative to total soil water-holding capacity.

Source:
- https://www.bom.gov.au/climate/drought/

**Assessment: RAW SCALE SUPPORTED AS FRACTION 0–1; presentation percent is a display conversion.** This is strong same-provider, same-variable corroboration of the native NCI attribute `fraction of fullness`; it is not a reason to mutate stored source values. Persist raw fractions, and multiply by 100 only in an explicitly labelled percent display/derived field.

### 4. AWRA-L monthly rainfall reducer — strong independent corroboration, provider contract still incomplete

The Bureau monthly ImageServer exposes `rain_day` in `mm`, and its monthly-service statistics reach values consistent with monthly accumulation rather than typical single-day rainfall. In addition, a current hydrology teaching workflow using the exact NCI path
`.../AWRALv7/processed/values/month/rain_day.nc`
states that each time step is a monthly rainfall total and warns that the inherited `long_name=Daily Rainfall` is misleading.

Independent reproduction reference:
- https://watercourse.earth/content/AssignmentOne/index.html

**Assessment: STRONG CORROBORATION, NOT YET PROMOTED TO PROVIDER-CONTRACT VERIFIED.** The NCI native variable still lacks `cell_methods`, and this review did not run a same-cell daily-vs-monthly numerical reproduction. Therefore the cross-source numerical join remains blocked.

### 5. AWRA-L monthly soil statistic — month-end is plausible but exact NCI product equivalence is not proven

The Bureau drought page says its soil-moisture maps use the **last day of the calendar month**, using daily AWRA-L data. That supports a month-end interpretation for a Bureau monthly soil-moisture presentation, but it does not explicitly state that the exact NCI `processed/values/month/sm_pct.nc` is generated by selecting the final daily state rather than by another reducer.

**Assessment: CORROBORATING ONLY; NCI monthly statistic remains unresolved.**

## Revised blocker boundary

The P04 blocker is now narrower than the previous handoff:

**Resolved / materially narrowed**
- HRS monthly product reducer: sum of gap-filled daily data grouped by month.
- HRS daily declaration: 9am accumulation for preceding 24 hours.
- AWRA `sm_pct` storage scale: raw fraction-of-fullness is supported as 0–1; percentage is presentation.
- February 2026 omission has a plausible terminal-partial-month mechanism, but is not formally explained.

**Still blocks a scientific numerical join**
1. Direct product-contract or bounded empirical verification that the exact NCI monthly `rain_day.nc` values are sums of the corresponding daily product.
2. Direct product-contract or bounded empirical verification whether exact NCI monthly `sm_pct.nc` is month-end, mean, or another statistic.
3. HRS 410033 DST/standard-vs-civil-time treatment and exact interval/date assignment if AWRA daily boundaries are used for direct day-level reconciliation.
4. HRS monthly quality/completeness semantics: the official monthly CSV has no QC column, so daily A/B/C/E/G screening must remain traceable.
5. Basin-grid numeric completeness/masking and the existing scientific-equivalence review before any basin statistic is admitted.

## Next executable step without external contact

Do **not** send the prepared provider questions without separate owner instruction.

The next no-contact P04 action is a deliberately bounded same-grid-cell reproduction using official AWRA daily and monthly products:
- choose one complete non-DST-sensitive month and one DST-transition month only if time-boundary comparison is required;
- fetch only the minimum daily values and corresponding monthly value for the same grid cell(s);
- test `monthly rain_day ~= sum(daily rain_day)`;
- test `monthly sm_pct` against both final-day `sm_pct` and mean daily `sm_pct`;
- preserve fill/mask handling and exact source/revision timestamps;
- treat agreement as empirical reproducibility evidence, not proof of the publisher's general contract;
- do not proceed to basin-wide join, correlation, low-flow classification, or causal interpretation until the remaining admission gates are closed.

If this bounded reproduction cannot be obtained reliably from the official endpoints, the correct state remains `BLOCKED_NUMERIC_JOIN` and the existing unsent provider questions are the next escalation path.

## CRP checkpoint

- Core knowledge: HRS monthly reducer is now publisher-documented; AWRA soil raw scale is strongly resolved; AWRA monthly reducers remain the key scientific semantics gap.
- Decision: keep P04 numerical join blocked, but narrow the blocker rather than restarting prior work.
- Idea: use a same-cell daily/monthly reproduction as an independent semantic oracle before provider outreach.
- Wish: reach a reproducible basin-month comparison without silently inventing units, reducers, DST rules or QC.
- Reasoning: cross-source correlations are invalid if one monthly value is a sum while another is a state/mean or if day boundaries differ materially.
- Key decisions: no P02/P03/geometry redo; no provider contact; no public release/merge; no WaterNSW-key dependency for this P04 step.
- Unresolved: exact NCI monthly rain/soil reducer; HRS DST interval; monthly QC/completeness; basin numeric mask completeness.
- Next action: bounded same-cell daily/monthly AWRA reproduction, then update the semantic matrix.
- Keywords: ClimateOS, P04, AWRA-L v7, HRS 410033, monthly reducer, sm_pct, rain_day, DST, QC, Evidence Passport.


## 2026-10-31 continuation

The bounded reproduction has now run. See [P04_AWRA_REPRODUCTION_20261031.md](P04_AWRA_REPRODUCTION_20261031.md): one July2000 NCI monthly soil sample matches the daily mean, not the final day; matched daily rainfall is unavailable at the inspected endpoint (HTTP404). This narrows the historical hypotheses above without claiming general semantics or reopening the blocked cross-source join.
