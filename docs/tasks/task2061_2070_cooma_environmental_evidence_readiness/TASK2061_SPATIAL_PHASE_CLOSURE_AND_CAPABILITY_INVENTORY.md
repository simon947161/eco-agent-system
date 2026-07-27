# Task2061 Spatial Phase Closure and Capability Inventory

## 1. Authoritative closure

The evidence-readiness batch starts from:

`main@2c41a8a95deb166f64f18252c28185cd3624a28c`

This baseline inherits the merged Terrain, Hydrology and Integrated QGIS work
from PR #95, PR #96 and PR #101. The accepted daily spatial entry point remains:

`runtime_data/qgis/cooma_spatial_foundation/project/Cooma_Spatial_Foundation_v0_4_integrated.qgz`

The project contains the accepted locality, terrain, hydrology, road and
optional imagery layers. It is not modified by Task2061–2070.

Phase result:

```text
COOMA_SPATIAL_FOUNDATION_PHASE_CLOSED
/ ONE_PROJECT_MANY_LAYERS
/ SPATIAL_ORIENTATION_READY
/ ENVIRONMENTAL_CONCLUSIONS_NOT_ESTABLISHED
```

## 2. What the current map can support

| Capability | Present use | Maximum safe interpretation |
|---|---|---|
| Official locality boundary | locate the administrative locality | spatial identity only |
| DEM, hillshade and slope | inspect terrain form and relative elevation | terrain description only |
| Watercourses and catchment context | inspect mapped hydrological relationships | mapped-source relationship only |
| Named water features | locate named source features | source identity only |
| Official roads | orient settlements and access context | mapped road identity only |
| Optional imagery | visual orientation when online | undated visual context unless capture metadata is admitted |
| Bookmarks and layer controls | repeat spatial views | interface reproducibility, not analytical reproducibility |

The map cannot by itself establish rainfall amount, snow storage, reservoir
volume, evapotranspiration, streamflow, extraction, leakage, water quality,
wastewater capacity, overflow, fire likelihood, asset safety or planning
compliance.

## 3. Reusable ClimateOS capability crosswalk

The next Cooma stage should orchestrate existing work instead of starting a
separate intelligence stack.

| Existing capability | Reuse for Cooma | Present readiness boundary |
|---|---|---|
| `COOMA-WATER-FIRE-WASTEWATER-WATCH` persistent monthly program | preserve questions, cycles, observations, reviews and annual inventory | monitoring record exists; it is not a water-balance engine |
| Official-source allowlist and metadata contracts | control publisher, retrieval and change-candidate provenance | a changed digest is not a changed condition |
| Local private continuity | preserve Founder-controlled research records | not a public evidence publication channel |
| QGIS v0.4 integrated foundation | spatially orient evidence and later indicators | no QGIS-derived conclusion in this batch |
| Evidence Passport and Claim Graph patterns | bind evidence, gaps, contradictions and permitted claims | existing Bondo examples do not transfer scientific conclusions to Cooma |
| Evidence admission and public claim contracts | stop unsupported real-place inference | admission must be repeated for each Cooma object |
| Model/source registries and adapter readiness | identify potential forecast and observation interfaces | registered or synthetic readiness is not operational current-data evidence |
| Hybrid forecast orchestration and model divergence logic | later compare scenario/model outputs | requires admitted inputs, aligned variables and uncertainty treatment |
| WeatherBench reference and tiny synthetic adapter | later support evaluation design | synthetic fixtures cannot validate Cooma predictions |
| Mechanism Scientist Runtime contracts | hypothesis, reproducibility, failure, licence, sandbox and human review governance | documentation readiness does not equal a completed experiment |
| Regional wind evidence protocols | inform height, representativeness, QC and uncertainty questions | regional wind samples cannot establish Cooma water loss or local fire state |
| Monthly/annual Receipt and Passport outputs | package reviewed cycles and missing evidence | inventory output is not an L3/L4 conclusion |

## 4. Capability assembly

The intended composition is:

```text
Persistent question program
→ source and evidence admission
→ QGIS spatial alignment
→ reproducible indicator/model run
→ Evidence Object and Claim Graph
→ conclusion-level gate
→ human review
→ Passport and monthly/annual update
```

This makes ClimateOS capable of asking the same disciplined question repeatedly,
while preserving what changed, what did not change, what remains unknown, and
what language remains prohibited.

## 5. Stage boundary

Task2061 closes an interface phase, not a science phase. No old Founder QGIS
review is reopened. No existing model, source registry or synthetic fixture is
promoted into real Cooma evidence by this inventory.
