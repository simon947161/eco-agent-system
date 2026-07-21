# Task2029 — Spatial Observation Template

Use one copy per human observation. Do not record Council-internal, customer,
personal-location or non-public infrastructure information.

```yaml
observation_id: QGIS-OBS-YYYYMMDD-NNN
date: YYYY-MM-DD
map_extent:
  west: null
  south: null
  east: null
  north: null
visible_layers: []
scale: null
crs: null
source_versions: []
human_observation: ""
interpretation_status: UNVERIFIED_SPATIAL_OBSERVATION
scientific_conclusion: NONE
limitation: ""
next_question: ""
```

## Separation rule

`human_observation` records what the reviewer can see at the stated extent,
scale and layer state. It must not silently become a causal, predictive,
compliance, engineering or operational statement. A separate evidence and
scientific review is required before any stronger status is considered.
