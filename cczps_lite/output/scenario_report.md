# CCZPS-Lite v0.4 — Batlow Scenario Report

This is a methodology demonstrator using indicative values only.
It is not a final planning, engineering, financial, or regulatory assessment.

## Location Profile

- Location: Batlow, NSW
- Location ID: batlow_nsw_001
- Region type: dry_inland_orchard_town
- Climate regime: west_dry_inland_transition
- Key climate risks:
- drought
- heat
- evaporation_pressure
- bushfire
- water_security

## Scenario Comparison Summary

| Scenario | Risk-adjusted score | Differential status | Evidence strength | Validation status | Human review required | Recommendation |
| --- | ---: | --- | --- | --- | --- | --- |
| Water Priority Pathway | 5.69 | water_advantage_with_heat_relief | Medium | Validated Enough for Concept Review | False | Promising but Requires Validation |
| Energy Resilience Pathway | 4.83 | mixed_or_neutral_differential | Low | Insufficient Evidence | True | Moderate Priority |
| Ecology / Fire Buffer Priority Pathway | 5.53 | elevated_fire_exposure | Medium | Requires Technical Validation | False | Promising but Requires Validation |

## Scenario A: Water Priority

Focuses on water retention, orchard resilience, irrigation timing, runoff capture, and drought adaptation.

### Interventions
- retention basins
- irrigation timing
- soil moisture protection
- runoff capture
- drought resilience planning

### Runtime and Evidence Fields

- Runtime reasoning: This pathway emphasises water security and drought resilience. The runtime signal is stabilising for water balance and moderate for ecological resilience; it has moderate demonstrator confidence.
- Risk index: 3.33
- Confidence level: medium
- Validation required: False
- Evidence strength: Medium
- Source basis: Local Observation
- Uncertainty notes: Further hydrological validation recommended.
- Human review required: False

### Validation Layer Runtime

- Validation score: 8.0
- Validation status: Validated Enough for Concept Review
- Validation gaps: No major validation gap identified at concept level
- Validation summary: Validation layer cautiously considers this pathway sufficient for concept-level review (score 8.0), but local consultation and site checks remain necessary.

### Differential Field Runtime

- Differential status: water_advantage_with_heat_relief
- Water gradient: 2.67 (strong_positive)
- Heat gradient: -5.33 (strong_negative)
- Vegetation gradient: 0.33 (neutral)
- Fire gradient: -0.33 (neutral)
- Differential summary: Differential field cautiously indicates water advantage with reduced heat pressure compared with representative Batlow context (water=strong_positive, heat=strong_negative, vegetation=neutral, fire=neutral).
- Reference record count: 3

### Forcing Layer Runtime

- Primary forcing: Microclimate Buffer Support
- Forcing candidates: Microclimate Buffer Support
- Forcing priority: Medium
- Forcing summary: Forcing layer cautiously identifies microclimate buffer support as a possible protective influence.

## Scenario B: Energy Resilience

Focuses on renewable energy, battery storage, microgrid logic, cooling demand reduction, emergency energy support, and energy-water coordination.

### Interventions
- renewable energy
- battery storage
- microgrid logic
- cooling demand reduction
- emergency energy support

### Runtime and Evidence Fields

- Runtime reasoning: This pathway emphasises energy continuity and emergency support. The runtime signal is watch for water balance and moderate for ecological resilience; it requires validation.
- Risk index: 5.0
- Confidence level: low
- Validation required: True
- Evidence strength: Low
- Source basis: Concept Study
- Uncertainty notes: Concept-level assumptions only.
- Human review required: True

### Validation Layer Runtime

- Validation score: 1.0
- Validation status: Insufficient Evidence
- Validation gaps: Need stronger field evidence or technical assessment
- Validation summary: Validation layer cautiously rates this pathway as insufficient evidence because evidence is low and candidate assumptions remain unresolved.

### Differential Field Runtime

- Differential status: mixed_or_neutral_differential
- Water gradient: -0.33 (neutral)
- Heat gradient: -2.33 (strong_negative)
- Vegetation gradient: -0.67 (neutral)
- Fire gradient: -0.33 (neutral)
- Differential summary: Differential field cautiously indicates mixed or neutral gradients compared with representative Batlow context (water=neutral, heat=strong_negative, vegetation=neutral, fire=neutral).
- Reference record count: 3

### Forcing Layer Runtime

- Primary forcing: Mixed / Unclear Forcing
- Forcing candidates: Mixed / Unclear Forcing
- Forcing priority: Low
- Forcing summary: Forcing layer does not identify a dominant candidate driver from the current representative gradients.

## Scenario C: Ecology / Fire Buffer Priority

Focuses on vegetation restoration, fire-buffer corridors, ecological recovery, landscape resilience, heat reduction, and community safety.

### Interventions
- vegetation restoration
- fire-buffer corridors
- ecological recovery
- landscape resilience
- heat reduction

### Runtime and Evidence Fields

- Runtime reasoning: This pathway emphasises ecological recovery and fire-buffer resilience. The runtime signal is watch for water balance and strong for ecological resilience; it requires validation.
- Risk index: 3.67
- Confidence level: low
- Validation required: True
- Evidence strength: Medium
- Source basis: Mixed Sources
- Uncertainty notes: Regional evidence available but site-specific validation required.
- Human review required: False

### Validation Layer Runtime

- Validation score: 5.0
- Validation status: Requires Technical Validation
- Validation gaps: Need bushfire exposure and vegetation management review; Need ecological condition and canopy-cover review
- Validation summary: Validation layer cautiously rates this pathway as requiring technical validation due to medium evidence and unresolved candidate forcing assumptions.

### Differential Field Runtime

- Differential status: elevated_fire_exposure
- Water gradient: 0.67 (neutral)
- Heat gradient: -3.33 (strong_negative)
- Vegetation gradient: 2.33 (strong_positive)
- Fire gradient: 1.67 (moderate_positive)
- Differential summary: Differential field cautiously indicates elevated fire exposure compared with representative Batlow context (water=neutral, heat=strong_negative, vegetation=strong_positive, fire=moderate_positive).
- Reference record count: 3

### Forcing Layer Runtime

- Primary forcing: Fire Exposure
- Forcing candidates: Fire Exposure; Vegetation Stress
- Forcing priority: Medium
- Forcing summary: Forcing layer cautiously identifies fire exposure, vegetation stress as candidate drivers behind the observed differential field.

## Notes on Confidence and Validation

Low evidence indicates higher uncertainty and requires human review before decisions are advanced.
High evidence indicates comparatively higher confidence, but it does not remove the need for local consultation, professional judgement, or site-specific validation.
Differential field gradients are indicative comparisons against representative context records, not validated field measurements.
Forcing layer outputs identify candidate pressures only and do not prove causality.

## Methodology Boundary

CCZPS-Lite v0.4 uses local JSON inputs, transparent rules, and generated text outputs only.
It does not connect to weather APIs, GIS services, databases, machine learning models, or world models.
