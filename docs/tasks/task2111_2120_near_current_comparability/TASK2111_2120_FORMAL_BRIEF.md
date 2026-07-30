# Task2111–2120 — Mittagang Near-Current Comparability Gate

## Authority

Founder decisions received 2026-07-31:

```text
FOUNDER_ACCEPT_MITTAGANG_L2_HISTORICAL_BASELINE
AUTHORISE_TASK2111_2120_NEAR_CURRENT_COMPARABILITY_GATE
DEFER_FORMAL_TREND_UNTIL_HYDROLOGY_REVIEW
```

## Question

Can the available WaterNSW near-current `FlowRate` observation for station
`410033` be compared lawfully and scientifically with the accepted BoM HRS
historical daily-streamflow baseline?

## Method

The gate checks station identity, measurement meaning, unit, aggregation
window, reporting-day boundary, timezone, quality semantics and provenance.
Every dimension must pass before any historical percentile is calculated.

## Real evidence presented to the gate

- Historical product: BoM HRS daily streamflow, previous 24 hours reported at
  09:00 local time, `ML/day`, quality scheme A/B/C/E/G.
- Near-current sample recorded from the WaterNSW Surface Water Data API:
  station `410033`, parameter `FlowRate`, `194.296 ML/day`, displayed time
  `2026-07-28 19:45 AEST`, quality code `125`.
- The near-current sample has not yet been admitted with exact response bytes,
  SHA-256 identity, parameter metadata or a quality-code mapping.

## Result

```text
NOT_COMPARABLE_YET
/ S0 EVIDENCE_PREPARATION
/ L1 MAXIMUM
/ NO_PERCENTILE_CALCULATED
/ NO_CURRENT_CONDITION
/ TREND_DEFERRED
```

Station identity and canonical unit pass. Measurement equivalence,
aggregation, day boundary, timezone, quality semantics and provenance remain
blocked.

## Boundary

The value `194.296 ML/day` is retained only to identify the evidence needing
admission. It is not compared with the historical distribution and is not
described as high, low, normal, unusual, safe or unsafe.
