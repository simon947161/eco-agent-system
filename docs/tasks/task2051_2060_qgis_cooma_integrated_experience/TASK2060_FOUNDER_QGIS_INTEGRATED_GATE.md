# Task2060 Founder QGIS Integrated Gate

## Current status

```text
IMPLEMENTED_ON_DRAFT_BRANCH
/ TECHNICAL_VALIDATION_REQUIRED
/ FOUNDER_REVIEW_NOT_YET_STARTED
/ NOT_MERGE_AUTHORIZED
```

## Required technical evidence

Before Founder review begins, the branch must demonstrate:

- focused Task2051–2060 tests pass;
- complete repository tests do not regress;
- Python compilation passes;
- PowerShell launcher plan/retrieve/derive/build/verify sequence passes on the
  established Windows QGIS 3.44.11 environment;
- generated v0.4 QGZ reopens with zero broken local layers;
- the only online provider is the exact NSWWebImagery service;
- official roads are bounded to the accepted Cooma +10 km extent;
- runtime source, derived and QGZ files remain untracked;
- `prototype/` remains untouched.

## Required Founder experience evidence

1. `INTEGRATED_ONE_PROJECT_COMPLETE_PASS`
2. `INTEGRATED_LAYER_ORDER_VISIBILITY_PASS`
3. `INTEGRATED_IMAGERY_ROADS_PASS`
4. `INTEGRATED_TERRAIN_HYDROLOGY_PASS`
5. `INTEGRATED_BOOKMARK_CRS_OFFLINE_CORE_PASS`

Only then record:

```text
FOUNDER_QGIS_INTEGRATED_REVIEW_PASS
```

## Interpretation boundary

The integrated project supports spatial learning and source-backed observation.
It does not establish current imagery capture date, road accessibility, route
safety, flood risk, water quality, supply security, slope stability, development
feasibility, ecological condition or any other scientific or engineering
conclusion.

## Gate

```text
READY_FOR_FOUNDER_QGIS_INTEGRATED_REVIEW
/ ONE_PROJECT_MANY_LAYERS
/ TERRAIN_HYDROLOGY_ROADS_OFFLINE_CORE
/ NSWWEBIMAGERY_ONLINE_OPTIONAL
/ BOUNDED_PUBLIC_DATA
/ NO_SCIENTIFIC_CONCLUSION
/ DO_NOT_AUTO_MERGE
```
