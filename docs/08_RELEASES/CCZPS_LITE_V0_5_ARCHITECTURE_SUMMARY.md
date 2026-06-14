# CCZPS-Lite v0.5 Architecture Summary

## System Boundary

CCZPS-Lite v0.5 is a deterministic, local-first planning-support foundation.
Each layer exposes its source basis, uncertainty, and human-review boundary.
The package does not provide professional certification or approval.

## Layered Architecture

| Layer | Inputs | Outputs | Boundary |
| --- | --- | --- | --- |
| Scenario Layer | local scenario options, location profiles, representative context | comparison matrix, scenario report, validation packs | indicative configured scenarios; not approved plans |
| Evidence Layer | local evidence profiles and generated observations | evidence strength, source basis, uncertainty, review flags | evidence classification does not prove scientific validity |
| Meteorology Layer | cached or previously governed observations and local scenario mappings | evidence, cache, time series, trends | trends are descriptive; no forecast or causal claim |
| Spatial Context Layer | configured scenario points and relationships | spatial transects and scenario packs | no live GIS, DEM, mapping, or spatial inference |
| Planning Hypothesis Layer | scenario, meteorology, trend, and transect context | testable hypotheses, indicators, failure conditions | hypotheses are not recommendations |
| Validation Support Layer | hypotheses and planning-only GIS/DEM requirements | access plan, validation interface, expert records, approval-support report | templates are not completed professional findings |
| Evidence Traceability Layer | generated scenario and validation artifacts | trace records linking claims to local artifacts | traceability creates no new conclusion |
| Internal Governance Decision Support Layer | traces, hypotheses, review templates, approval support | internal support records, gaps, required human actions | internal status is not external approval |
| Scenario Comparison Layer | evidence, traceability, hypotheses, reviews, governance records | cross-scenario evidence and uncertainty comparison | no ranking, winner, or final recommendation |
| Dashboard / Reporting Layer | local generated CSV, JSON, and Markdown | static browser presentation and reports | presentation only; no browser-side analytical service |
| Governance and Budget Guard Layer | usage profiles, budget profiles, manual workflow inputs | warnings, stop conditions, manual confirmation records | governed retrieval only; no automatic approval |

## End-to-End Flow

```text
Local Inputs
  -> Deterministic Runtime
  -> Evidence and Trend Records
  -> Planning Hypotheses
  -> Validation Support
  -> Traceability
  -> Internal Governance Support
  -> Scenario Comparison
  -> Static Reports and Dashboard
  -> Human and Professional Review
```

## Input Families

- `cczps_lite/input/`: scenario, evidence, meteorology, usage, and budget profiles
- `cczps_lite/config/`: configured spatial and runtime settings where present
- existing generated outputs used by downstream local layers

## Output Families

- machine-readable JSON for evidence, validation, traceability, governance, and
  comparison
- Markdown reports for human review
- CSV for the legacy scenario comparison matrix
- static dashboard assets under `cczps_lite/dashboard/`

See the [output inventory](CCZPS_LITE_V0_5_OUTPUT_INVENTORY.md) for file-level
details.

## Governance Boundary

Every downstream validation, governance, and comparison view preserves
mandatory human review. Existing approval-support records remain
`not_ready_for_approval`. No layer can turn a configured scenario, evidence
record, hypothesis, template, or comparison into statutory approval.
