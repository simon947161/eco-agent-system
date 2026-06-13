# Scenario Comparison Runtime

Comparison support only. Records expose local evidence coverage, risk, uncertainty, and review status without ranking scenarios, selecting a best option, making a final recommendation, or claiming approval readiness.

## Cross-Scenario Summary

Groups describe current evidence coverage and review needs only. They do not order scenarios or identify a preferred option.

- Medium evidence coverage: Batlow, Iraq, Baiyangdian-Xiong'an
- Low evidence coverage: Kunlun
- High uncertainty: Batlow, Kunlun, Iraq, Baiyangdian-Xiong'an
- GIS/DEM or spatial validation required: Batlow, Kunlun, Iraq, Baiyangdian-Xiong'an
- Expert review required: Batlow, Kunlun, Iraq, Baiyangdian-Xiong'an
- Complete eight-category traceability: Batlow, Kunlun, Iraq, Baiyangdian-Xiong'an

## Comparison Table

| Scenario | Comparison status | Evidence | Uncertainty | Risk | Hypothesis | Traceability | Governance | Expert review | Approval support |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Batlow | requires_professional_review | medium | high | high | requires_validation | available | requires_further_review | not_reviewed | not_ready_for_approval |
| Kunlun | requires_spatial_validation | low | high | medium | requires_validation | available | requires_further_review | not_reviewed | not_ready_for_approval |
| Iraq | requires_professional_review | medium | high | medium | concept_level | available | requires_further_review | not_reviewed | not_ready_for_approval |
| Baiyangdian-Xiong'an | requires_professional_review | medium | high | medium | concept_level | available | requires_further_review | not_reviewed | not_ready_for_approval |

## Batlow

- Environmental signal: `context_documented_requires_validation`
- Water signal: `rainfall_increasing;humidity_increasing;hydrology_requires_review`
- Land signal: `requires_gis_dem_validation`
- Energy signal: `context_relevant_requires_review`
- Spatial transect: `valid_configured`
- GIS/DEM requirement: `planning_only_not_acquired`
- Human review required: `True`
- Professional review required: `True`

Comparison notes:

- Comparison is based on local generated evidence only.
- Signals are descriptive evidence readings, not forecasts or causal findings.
- No scenario rank, winner, statutory approval, or implementation recommendation is produced.

## Kunlun

- Environmental signal: `context_documented_requires_validation`
- Water signal: `rainfall_stable;humidity_stable;hydrology_requires_review`
- Land signal: `requires_gis_dem_validation`
- Energy signal: `not_explicitly_documented`
- Spatial transect: `configured_with_missing_data`
- GIS/DEM requirement: `planning_only_not_acquired`
- Human review required: `True`
- Professional review required: `True`

Comparison notes:

- Comparison is based on local generated evidence only.
- Signals are descriptive evidence readings, not forecasts or causal findings.
- No scenario rank, winner, statutory approval, or implementation recommendation is produced.

## Iraq

- Environmental signal: `context_documented_requires_validation`
- Water signal: `rainfall_stable;humidity_decreasing;hydrology_requires_review`
- Land signal: `requires_gis_dem_validation`
- Energy signal: `not_explicitly_documented`
- Spatial transect: `valid_configured`
- GIS/DEM requirement: `planning_only_not_acquired`
- Human review required: `True`
- Professional review required: `True`

Comparison notes:

- Comparison is based on local generated evidence only.
- Signals are descriptive evidence readings, not forecasts or causal findings.
- No scenario rank, winner, statutory approval, or implementation recommendation is produced.

## Baiyangdian-Xiong'an

- Environmental signal: `context_documented_requires_validation`
- Water signal: `rainfall_increasing_and_stable;humidity_increasing;hydrology_requires_review`
- Land signal: `requires_gis_dem_validation`
- Energy signal: `not_explicitly_documented`
- Spatial transect: `valid_configured`
- GIS/DEM requirement: `planning_only_not_acquired`
- Human review required: `True`
- Professional review required: `True`

Comparison notes:

- Comparison is based on local generated evidence only.
- Signals are descriptive evidence readings, not forecasts or causal findings.
- No scenario rank, winner, statutory approval, or implementation recommendation is produced.
