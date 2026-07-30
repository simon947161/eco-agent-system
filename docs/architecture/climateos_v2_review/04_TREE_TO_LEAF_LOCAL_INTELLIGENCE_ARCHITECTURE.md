# Tree-to-Leaf Local Environmental Intelligence Architecture

## Architecture

```text
GLOBAL DRIVER
ENSO · IOD · SAM · MJO · climate trend
        ↓ mechanism, lag, season and uncertainty
REGIONAL RESPONSE
rainfall · temperature · snow · wind · circulation · drought indices
        ↓ spatial and temporal fitness
LOCAL SYSTEM
terrain · catchment · stream · vegetation · storage · infrastructure
        ↓ exposure, vulnerability and dependency
LOCAL CONSEQUENCE
water-accounting stress · fire-weather concern · operational constraint
        ↓ consequence, reversibility and lead time
INTERVENTION WINDOW
observe · inspect · prepare · maintain · escalate · decide
        ↓
OUTCOME AND RETROSPECTIVE VALIDATION
```

## Required object chain

| Object | Required content | Must not imply |
|---|---|---|
| `GLOBAL_DRIVER_STATE` | provider, variable, period, confidence, alternatives | local impact |
| `REGIONAL_RESPONSE_SIGNAL` | mechanism link, season, lag, model/observation agreement | site consequence |
| `LOCAL_SYSTEM_CONTEXT` | boundary, terrain, hydrology, land cover, assets, data gaps | current risk by presence alone |
| `LOCAL_EVIDENCE_BUNDLE` | observations, models, history, quality and conflicts | causal certainty |
| `LOCAL_CONSEQUENCE_HYPOTHESIS` | mechanism, exposure, severity, alternatives | reviewed assessment |
| `TIME_BOUNDED_ASSESSMENT` | conclusion level, maturity stage, validity and reviewer | permanent truth |
| `INTERVENTION_OPTION` | action class, lead time, cost, reversibility and owner | automatic execution |
| `OUTCOME_OBSERVATION` | what happened, when and evidence identity | proof of prediction skill alone |
| `RETROSPECTIVE_VALIDATION` | hit/miss/false alarm, calibration and lessons | silent model promotion |

## Translation gates

### Global → regional

- mechanism is scientifically plausible and cited;
- season and hemisphere are explicit;
- time lag is a range, not a hidden constant;
- model disagreement remains visible.

### Regional → local

- local boundary is declared;
- variable is spatially representative or its weakness is stated;
- terrain, catchment and exposure are not skipped;
- local observations can confirm, weaken or contradict the regional signal.

### Local evidence → consequence

- alternative explanations are recorded;
- baseline and anomaly periods are fit;
- missing critical evidence can limit conclusion level;
- consequence severity is separated from probability.

### Consequence → intervention

- action authority is based on consequence and reversibility;
- low-regret reversible actions can occur earlier;
- high-cost, irreversible, legal, engineering or public-safety actions require
  stronger evidence and accountable review;
- no data product directly executes an intervention.

## QGIS role

QGIS is the governed local spatial workbench and evidence-alignment surface:

- accepted boundary and coordinate reference system;
- terrain, hydrology, settlement, roads and official layers;
- evidence-object locations and dates;
- spatial relevance and coverage gaps;
- versioned assessment maps.

QGIS does not supply causal inference by itself. v0.4 remains the accepted
foundation. A future v0.5 should add evidence objects only after their source,
licence, date and conclusion level are admitted.

## Minimal v2 service boundary

The first implementation needs only four connected services:

1. Evidence admission and identity;
2. Local system graph and spatial alignment;
3. Convergence, disagreement and time-bounded answer builder;
4. Human review, release, expiry and retrospective ledger.

A new autonomous multi-agent layer is not a prerequisite.

