# Future restricted reproducibility protocol v0.1 — NOT EXECUTED

Earliest candidate: **Rockhampton 25 November 2018 daily-Tmax source/quality replay**, with Cooma16 January2019 as a separate follow-on. Rockhampton is prioritised because station metadata was readable, not because a methane response is expected. This first potential experiment is meteorological evidence validation only; any coupled gas experiment is a separate, presently blocked proposal. No processing run, threshold classification, model fit, flux conversion or simulation is performed now.

## Proposed definitions for review

- Fixed screening rule: a daily station Tmax **at least35.0 degC** is a hot-day candidate. This is a convenient analyst-defined screen, not a BOM heatwave definition, physiology threshold or site-response coefficient. These two dates were already known from summaries, so selection is retrospective and biased; no confirmatory prevalence or causal inference permitted.
- A run of at least3 consecutive eligible hot days may be labelled a study-specific hot spell only, never automatically an official heatwave. No run has been checked. Formal percentile/heatwave studies require a separately frozen seasonal climatology and qualified event definition.
- Proposed windows: t−7 through t−1 descriptive antecedent, t0 event date, t+1 through t+30 follow-up. Rockhampton labels2018-11-18 to2018-12-25; Cooma2019-01-09 to2019-02-15. No numeric date conversion to UTC until clock evidence exists.
- Future process lag bins proposed: 0–1 days (immediate operating response), 2–7 days (short residence/transport response), 8–30 days (slower moisture/substrate/storage response). These are exploratory reporting bins, NOT validated kinetic delays. A process with longer residence or gas-transport time invalidates this design and requires re-review, not silent truncation. No gas results used to pick bins.
- Before gas work, match within-facility controls by season, load, treatment state and maintenance; do not treat Cooma versus Rockhampton as interchangeable treatment/control units. No comparison based only on regional temperature difference.

## Deterministic future steps, all pending approval

1. Obtain authorised BOM daily maximum export with native station/product identifiers, dates, QC dictionary, accumulation spans, issue/retrieval/version and source bytes/hash. Raw here means provider daily observations, not instrument high-frequency telemetry; do not mislabel a summary or homogenised series as such.
2. Freeze a manifest and read-only source copy (local-only if redistribution rights require). Preserve all missing, duplicate and QC states. Do not splice neighbouring stations or a current record into history.
3. For this deliberately strict small replay, require every expected date in the proposed window to have one QC-completed, single-day observation and resolved clock support. Otherwise STOP the replay; report gaps rather than impute. This100% rule is a proposed design gate, not a BOM standard. No current completeness percentage is calculated.
4. Resolve event-era moves/instrument transitions and uncertainties. Unresolved discontinuity or unknown temperature uncertainty blocks threshold certification. A measurement whose stated uncertainty interval overlaps35.0degC is indeterminate for the proposed screen. Do not invent instrument uncertainty.
5. Once separately authorised, compare event-day value to archived summary with the declared source rounding/version rules; any unresolved mismatch stops admission. Record discrepancies rather than force equality. Later repeat the same frozen process independently for Cooma.
6. Record only weather/QC replay outputs. Gas endpoints remain null. Coupling requires measured process, calibrated flux and operating controls, matched time/space, permissions, specialist review and separate Founder approval.

## Units, uncertainty and forbidden shortcuts

Tmax degC; daily precipitation mm over its own9am interval if separately acquired. Do not add rain to this temperature-only replay by filling missing values. Store temperature measurement uncertainty in degC, timing uncertainty in duration, position uncertainty in metres only when supported. Distinguish measurement/QC, rounding, metadata, sampling, missingness, spatial representativeness, structural confounding and model-form uncertainty. No uncertainties added numerically in this batch.

For a later gas protocol, retain CH4/N2O/CO2 mass species; flux mg species m−2 h−1 and collected gas flow at declared temperature/pressure/moisture. N2O-N is not N2O; kgC is not kgCO2; ppmv is not mass flux. Energy kWh, fuel units and factor year/grid remain explicit. No GWP, emission factor, Arrhenius/Q10 coefficient or AWT formula is evaluated or modified.

Stop for access denial, missing rights, incomplete/ambiguous QC, multi-day accumulation, unresolved clocks/moves, unit ambiguity, absent process data or absent Founder approval. Do not buy data or bypass access. Protocol changes require a new version before inspecting outcome data. Reuse existing CarbonOS evidence manifests and ClimateOS/EcoEngine time semantics once verified; no new pipeline, database, GIS or agent infrastructure.
