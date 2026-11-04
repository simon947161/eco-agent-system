# Batch C2 — raw-weather quality and multi-gas measurement readiness

2026-11-04 · Issue131 / DraftPR132 · **PREPARATION_ONLY / P1-A scientific admission PENDING**.

Responds to [ChatGPT review6627021081](https://github.com/simon947161/eco-agent-system/pull/132#issuecomment-6627021081) of exact Batch C HEAD `00a3fdb3b7fb16de7215c068e7efc3720e75c2a0`, accepted with limits. No experiment authorised by that review or this package.

Two selected exemplars retain prior summary values; raw daily exports and event QC were **not obtained**. BOM product-level QC/time documentation and selected station metadata improve readiness, not source-series validation. Search-only metadata, unavailable tool routes, an interactive timeout and unvalidated URL probes are separately recorded. Nothing is described as a verified403 unless a403 was actually returned. No fabricated daily rows, completeness or UTC conversion.

Deliverables: [quality audit](OBSERVATION_QUALITY_AUDIT.md), [event register](EVENT_QUALITY_REGISTER.json), [source ledger](SOURCES.json), [attempt receipt](ACCESS_ATTEMPTS.json), [evidence matrix](EVIDENCE_MATRIX.md), [measurement checklist](FIELD_MEASUREMENT_CHECKLIST.md), [machine-readable requirements](MEASUREMENT_READINESS.json), [future protocol](FUTURE_REPLAY_PROTOCOL.md), [10-page Slides](index.html), [handoff](NEXT_SESSION.md).

Twelve measurement requirements cover actual process temperature/moisture, organic/nitrogen loading, treatment controls, species-specific atmospheric flux, dissolved gas, collection/destruction, carbon origin and energy/refrigerants. These are requirements, not acquired measurements or fieldwork approval. IPCC inventory context and US EPA monitoring checklist are not substituted for Australian statutory AWT or a professionally approved sampling procedure.

Earliest proposal is a Rockhampton weather-only quality replay; all gas coupling remains blocked. A35degC analyst screen, antecedent/follow-up windows, lag candidate bins and strict completeness/uncertainty stops are specified for review only. Known-case selection is acknowledged; no claims of causality or representative extreme-event frequency.

## Review questions

1. Are acquisition failures and raw-data absence distinguished correctly from access denial and true missing observations?
2. Does product-level QC documentation remain separate from unknown event-level flags and whole-record metadata completeness?
3. Is the proposed fixed-temperature screen useful for a weather-only reproducibility exercise, with retrospective selection and non-heatwave status explicit?
4. Are lag bins, unit conventions and uncertainty/clock/station-history stops sufficiently conservative and testable?
5. Which field requirements need specialist revision before any later permission request? No field measurements or gas experiment is ready now.

## Conversation Radar

- Knowledge: a daily summary, raw daily export, product QC legend and station metadata are different evidence layers.
- Idea: earliest viable replay should test weather provenance before coupling gases.
- Decision: cap raw-data attempts; preserve gaps; specify but do not execute the replay.
- Risks: expired exports, ambiguous accumulation/DST, station changes, whole-record versus local completeness, concentration/flux confusion, selection bias.
- Open: actual daily files/flags, calibration uncertainty, event-era metadata, permissions and process/gas records.
- Next: ChatGPT review; then approved public-data path planning, not repeated failed probes. Separate Founder approval for experiments.
- Keywords: ClimateOS, CarbonOS, EcoEngine, BOM, Cooma, Rockhampton, QC, CH4, N2O, CO2, MRV.
