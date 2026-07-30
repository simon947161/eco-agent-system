# Cooma First Scientific Assessment Selection

## Selected assessment

**Mittagang 410033 Historical Daily Streamflow Characterisation v0.1**

Proposed question:

> What does the admitted 1964-03-01 to 2024-02-29 daily streamflow record for
> Murrumbidgee River at Mittagang Crossing show about historical coverage,
> seasonality, interannual variability, missingness and source quality, and
> what does it not establish about current Cooma water conditions?

## Why this is first

- it uses one official, long-duration, bounded real dataset;
- PR #108 already verifies identity, units, quality codes, coverage and digest;
- it supports honest L2 descriptive indicators without requiring a water
  security conclusion;
- it creates a reusable baseline for later near-current comparison;
- it exercises evidence identity, method, uncertainty, answer validity and
  human review in one vertical slice;
- it avoids mixing drinking-water quantity, water quality, wastewater
  operations and public safety.

## Minimum analysis

- calendar and quality-code profile;
- monthly/seasonal distributions;
- annual completeness and variability;
- declared handling of A/B/C/E/G quality codes;
- sensitivity with and without modelled/gap-filled categories where the source
  definition supports that distinction;
- robust high/low-flow descriptive percentiles;
- change-point or trend exploration only with method and multiple-testing
  caution;
- explicit statement that the record ends in February 2024.

## Required outputs

1. method and data-boundary note;
2. reproducible analysis code and tests;
3. L2 Run Receipt;
4. charts/tables with units and period;
5. Time-Bounded Environmental Answer;
6. Evidence Passport with limitations;
7. qualified hydrology review gate before any L3 promotion.

## What it may conclude

- descriptive historical patterns for the admitted gauge and period;
- data coverage, quality composition and calculated indicators;
- whether later near-current evidence is above, below or within a declared
  historical distribution after equivalent-method checks.

## What it may not conclude

- current 2026 flow from a series ending in 2024;
- Cooma drinking-water sufficiency or safety;
- reservoir storage or demand balance;
- causal attribution to ENSO, climate change or local intervention;
- engineering, wastewater or public-safety status;
- catchment-wide behaviour without spatial fitness review.

## Path to near-current assessment

```text
historical characterisation
→ admit authorised near-current gauge observations
→ check method/unit comparability
→ add rainfall, snow and climate-driver context
→ add declared catchment/storage/demand boundary
→ issue expiring L2 indicators
→ triangulate and obtain review for any L3 assessment
```

PR #108 is an evidence-ingestion prerequisite, not the assessment itself.

