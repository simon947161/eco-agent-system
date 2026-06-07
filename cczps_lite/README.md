# CCZPS-Lite â€” Batlow Runtime Demonstrator

CCZPS-Lite is a small, file-based demonstrator for comparing possible environmental resilience pathways. It supports the EcoEngine Runtime Core idea that scenario assumptions should move through evidence, runtime interpretation, reasoning, and governance review before being treated as decision-support output.

Batlow, NSW is used as the first demonstrator because it provides a clear rural resilience context: orchard water security, energy continuity, ecological recovery, bushfire resilience, and community safety can be compared without building a large platform.

## Runtime Flow

```text
Scenario
    â†“
Evidence Profile
    â†“
Runtime Fields
    â†“
Runtime Reasoning
    â†“
Evidence-Aware Governance Output
```

## How to Run

From the repository root:

```bash
python cczps_lite/engine/scenario_compare.py
python cczps_lite/engine/meteorology_runtime.py
python cczps_lite/engine/usage_cost_governance.py
```

The scripts use only the Python standard library. Meteorology transport is
injected by the caller and disabled for generated fixtures, so routine tests do
not call weather APIs. The runtimes do not use forecasting, machine learning,
autonomous recommendations, GIS services, databases, or world models.

## Input Files

- `input/location_profile.json` describes the Batlow location profile.
- `input/scenario_options.json` describes three indicative future pathways.
- `input/evidence_profile.json` describes the first evidence layer for water, energy, ecology, and fire assumptions.
- `input/meteorology_sources.json` defines documented public observation sources and field mappings.
- `input/meteorology_scenarios.json` defines the Batlow, Kunlun, Iraq, and Baiyangdian-Xiong'an observation requests.
- `input/usage_cost_profiles.json` declares proposed usage, ownership, automation, budget-control, and service-model assumptions.

## Generated Output Files

- `output/comparison_matrix.csv` contains scenario scores, runtime fields, evidence fields, recommendation classes, and usage governance readings.
- `output/scenario_report.md` provides a readable scenario comparison report.
- `output/governance_summary.md` provides a short governance-oriented summary, including evidence and usage assessment.

## Meteorology Connector Runtime

### Current Status: Connector Scaffold Only

Task 18 does not retrieve live meteorology data. It provides source
definitions, field mappings, payload standardisation, missing-data handling,
and an injected `fetcher` interface for future transport implementations.

There is currently no built-in HTTP client, provider endpoint construction,
API authentication, ERA5/CDS client, BOM downloader, or scheduled retrieval.
Running `meteorology_runtime.py` without an externally supplied fetcher creates
local records with null observation values and
`"retrieval_status": "not_retrieved"`.

The NASA POWER values used in tests are a hard-coded parsing fixture. They are
not remotely retrieved observations. NOAA, ERA5, and BOM have source
definitions only and no provider-specific retrieval implementation.

The connector standardises air temperature, rainfall, relative humidity, wind
speed, wind direction, solar radiation, and evaporation when those values are
available from a configured source payload. Every reading exposes its source,
observation timestamp, retrieval status, and evidence confidence.

Meteorology is supporting evidence only. Missing values remain explicit, and
the connector does not change validation scores or produce conclusions unless a
future task introduces and documents an explicit rule.

## Usage & Cost Governance Runtime

Run `python cczps_lite/engine/usage_cost_governance.py` after scenario
generation. It adds a usage and cost governance reading to every scenario
through eight explicit CSV fields and appends readable sections to the
scenario, governance, and system validation reports.

Cost levels are qualitative governance bands, not currency estimates. The
runtime performs no external API calls, metering, billing, payments,
subscriptions, invoicing, crypto payments, token operations, or marketplaces.
An approval requirement is visible but is never granted automatically.

## Methodology Boundary

This prototype is not a final environmental model, regulatory-grade planning tool, financial assessment, or scientific simulation. It is a methodology demonstrator using indicative values only.

Low evidence means higher uncertainty and triggers human review. High evidence means comparatively higher confidence, but it does not remove the need for local consultation, professional judgement, or site-specific validation.

## Connection to CCZPS 2.0 and EcoEngine

CCZPS compares possible futures. EcoEngine runtime logic helps describe how scenario assumptions translate into operational signals. This CCZPS-Lite version introduces the first evidence layer so that governance outputs can show where assumptions come from, where uncertainty is highest, and which pathways require human review.
