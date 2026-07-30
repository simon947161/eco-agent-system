# Task2101–2110 — Mittagang 410033 Historical Characterisation

Date: 2026-07-30  
Status: `PHASE_II_BATCH_01 / FOUNDER_AUTHORISED / IMPLEMENTED / REVIEW_GATE`

## Authority

Founder approvals:

```text
APPROVE_V2_NORTH_STAR
APPROVE_EARLY_WARNING_OPTION_B
APPROVE_MITTAGANG_HISTORICAL_CHARACTERISATION
APPROVE_PR_DISPOSITION_PACKAGE
APPROVE_GOOGLE_EARTH_VISUAL_REFERENCE
APPROVE_PHASE_II_BATCH_01_AFTER_GATES
```

Authoritative implementation baseline:

```text
main@0a62a85570f436c65f732b12a8dbb1bf285f1b95
PR #110 merged as aceceff7bef1c1ed7dc091f3195c76e6b69b3c9f
PR #108 merged as 0a62a85570f436c65f732b12a8dbb1bf285f1b95
```

## Purpose

Complete the first vertical slice from an admitted official historical dataset
to a reproducible, quality-aware, time-bounded L2 answer.

## Task map

| Task | Deliverable | State |
|---|---|---|
| 2101 | dual-axis conclusion/evidence-state schema | complete |
| 2102 | time-bounded answer schema | complete |
| 2103 | validated raw-observation parser | complete |
| 2104 | quality-code profile and A+B sensitivity method | complete |
| 2105 | monthly, seasonal and annual distributions | complete |
| 2106 | versioned SVG charts and CSV tables | complete |
| 2107 | L2 characterisation receipt | complete |
| 2108 | first Time-Bounded Environmental Answer | complete |
| 2109 | Evidence Passport and retrospective plan | complete |
| 2110 | Founder Evidence Gate | open |

## Scientific boundary

The question is:

> What does the admitted 1964-03-01 to 2024-02-29 daily streamflow record for
> Murrumbidgee River at Mittagang Crossing show about historical coverage,
> seasonality, variability and source quality?

The output is:

```text
S0 BASELINE_MONITORING / L2 DESCRIPTIVE_INDICATOR
```

It is not a current-condition assessment. It does not evaluate water supply,
drinking-water safety, storage, extraction, demand, causality, engineering,
wastewater or public safety.

## Method choices

1. The exact BoM HRS bytes must retain the accepted SHA-256.
2. All source-published rows form the primary descriptive series.
3. A+B rows form a visible sensitivity screen, not a replacement dataset.
4. C, E and G classifications are never silently relabelled or dropped.
5. Cross-year comparison uses complete calendar years only.
6. Quantiles use deterministic linear interpolation.
7. v0.1 issues no trend or change-point result.
8. Any L3 promotion requires qualified hydrology review and additional
   fit-for-purpose evidence.

## Outputs

Principal output directory:

`cczps_lite/output/mittagang_410033_historical_characterisation/`

It contains:

- method and results note;
- characterisation and run receipts;
- Time-Bounded Environmental Answer;
- Evidence Passport;
- monthly and complete-year CSV tables;
- monthly distribution, annual median and quality-composition SVG charts.

## Stop rule

Task2110 stops at Founder evidence review. It does not authorise:

- a public warning;
- a current 2026 flow statement;
- an L3 assessment;
- a formal trend claim;
- a Cooma safety, sufficiency or engineering conclusion;
- Google Earth automation;
- a new radar or GEGG task.
