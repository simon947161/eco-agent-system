# ClimateOS Task1590 — Closure and Next Gate Brief

Date: 2026-07-14  
Status: TASK1581_1590_CLOSED / FOUNDER_REVIEW_REQUIRED / HARD_STOP  
Branch: `agent/task1581-1590-wind-scale-evidence-protocol`

## 1. Closure result

Task1581–1590 is complete as a documentation-only evidence protocol for the
single selected claim class `SCALE_AWARE_WIND_TRANSLATION`.

Created:

1. `TASK1581_1590_SCALE_AWARE_WIND_CLAIM_EVIDENCE_PROTOCOL_FORMAL_BRIEF.md`;
2. `SCALE_AWARE_WIND_CLAIM_EVIDENCE_PROTOCOL_V0_1.md`;
3. this Task1590 closure record.

## 2. What is now controlled

- planetary circulation, model fields, ADFD forecast grids, station
  observations, reanalysis and site/design wind are separate objects;
- wind components, speed, direction, sustained wind, maximum sustained wind
  and gust are not interchangeable;
- height, averaging period, unit, valid time and spatial support are mandatory;
- Australia, state, region, locality and site support boundaries are explicit;
- Sydney, Alice Springs, Snowy Valleys and Riverina remain non-executable
  examples;
- validation measures, stratification, uncertainty and failure gates are
  designed but not run;
- scientific, domain, licence, security, financial and Founder roles are named.

## 3. Verification

| Requirement | Result |
|---|---|
| PR #42 Founder-authorized merge | COMPLETE; merge SHA `5950f293550c6f461836dad53d1692fabc100d30` |
| Dedicated post-merge branch | COMPLETE |
| Single claim class selected | COMPLETE: SCALE_AWARE_WIND_TRANSLATION |
| Official wind metadata pinned | COMPLETE WITH PRODUCT-SPECIFIC BLOCKERS |
| Height/unit/time/statistic schema | COMPLETE |
| Scale-support matrix | COMPLETE |
| Alignment and validation plan | COMPLETE; NON-EXECUTED |
| Human and governance gate | COMPLETE; NO REVIEWER APPOINTED |
| Model/data/API/FTP/cloud access | NOT PERFORMED |
| Calculation, evaluation, regridding or downscaling | NOT PERFORMED |
| Current/regional/site wind conclusion | NOT PERFORMED |
| GraphCast | REMAINS LATER |

## 4. Decision

`TASK1581_1590_CLOSED / WIND_PROTOCOL_READY / EXECUTION_BLOCKED`

## 5. Candidate next gate — not authorized

`Task1591–1600 — Single-Region Wind Evidence Acquisition and Validation Brief`

Before that task can start, the Founder must select exactly one region and one
claim/statistic. The brief must then pin products, stations, period, licence,
access method, storage, cost ceiling and accountable scientific reviewer.

Possible regions remain:

1. Sydney coastal-metropolitan wind process;
2. Alice Springs arid-locality representativeness;
3. Snowy Valleys complex-terrain wind;
4. Riverina production-landscape wind.

The next task should still prepare an acquisition brief before retrieving any
data. Engineering/site values remain outside that gate.

## 6. Hard stop

Task1581–1590 closes here. Task1591+, data acquisition, live-source use,
validation execution, regional conclusions, GraphCast and merge of the new
Draft PR do not start automatically.
