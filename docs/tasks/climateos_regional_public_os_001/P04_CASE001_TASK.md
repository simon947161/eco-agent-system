# P04 first water–soil–climate case: executable preparation

Case: `P04-WATER-SOIL-CLIMATE-001`. State: **PREPARED_NOT_SCIENTIFICALLY_EXECUTED**. Continue #128 / PR #129; no new project or website.

Research question: within the verified upstream catchment of HRS 410033, do precipitation anomalies and antecedent soil moisture align with low-flow months after accounting for seasonality and competing explanations? This is a proposed association study, not a causal conclusion or a town supply assessment.

## Work actually completed

`tools/p04_water_soil_climate_preflight.py` validates the accepted package and counts original calendar labels/quality codes for 2000–2025. It has been run: 312 months, 9,497 records, zero missing labels, zero null values; A=3,266, B=3,460, C=10, E=2,761. 216 months contain only non-null A/B records. These are availability counts, not evidence that all those records are scientifically fit for an intended calculation. No values are interpolated or converted, no monthly discharge statistic or correlation is computed. Summary: [P04_CASE001_READINESS.json](P04_CASE001_READINESS.json).

Reproduce from repository root:

```powershell
python -B tools/p04_water_soil_climate_preflight.py --output .local/p04-water-soil-climate-preflight.json
python -B -m unittest discover -s tests -p test_p04_preflight.py -v
```

## Next minimum executable task: input admission manifest

Inspect official public metadata for **one catchment polygon, one precipitation product and one soil-moisture product**, covering the same basin and a documented overlap with 2000–2025. Use free, explicitly licensed sources; BOM Water Data Online / landscape water balance and NSW SEED are candidates, not accepted datasets. Record exact product/version URLs and terms before numeric download. Do not require a paid service, register accounts, or work around access restrictions.

For each candidate persist an admission record containing: publisher, product/version, licence and attribution, transformation/publication restrictions, cost and automated-access terms, retrieval timestamp/hash, geographic coverage/grid/CRS, measurement/model distinction, time basis and aggregation interval, unit, soil depth where relevant, quality codes, missingness, latest observation and documented update frequency. Confirm station-to-upstream-catchment alignment; council boundaries are not an acceptable substitute. Rejected candidates retain their explicit rejection reasons.

Acceptance: all three inputs have documented compatible spatial/temporal definitions and explicit permitted use, or a precise blocked record with source evidence and an alternative. Do not join numeric series while the HRS CSV header/daily interval/UTC ambiguity remains unresolved. Obtain authoritative product clarification rather than inventing a conversion.

## Scientific execution gate

Before numerical analysis, review the water quality exclusions, catchment alignment, time aggregation, soil depth, model uncertainty and study protocol. Predeclare seasonal baseline, low-flow definition, plausible antecedent windows, minimum completeness and sensitivity treatment of C/E/G records. Distinguish observations from model estimates. Assess drought/rainfall, upstream abstractions, storage, vegetation/land use and measurement changes as competing explanations; absence of those data limits interpretation.

Once those gates pass, run one reproducible basin/month comparison with separate raw and derived stores, input digests, Run Receipt and Evidence Passport. Report missing/expired/rejected inputs and uncertainty. Retain scientific review pending until actually reviewed. No causal, drinking-water, pollution, or current-condition conclusion is authorized by this preflight.

Current blockers are concrete missing scientific inputs and unresolved time semantics, not a lack of a new OS or website. No recent operational series was admitted in P03. No schedule, unattended run or new deployment is part of this preparation.
