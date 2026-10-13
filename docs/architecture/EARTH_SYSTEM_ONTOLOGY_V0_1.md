# Earth System Ontology v0.1

Status: DRAFT_FOR_FOUNDER_REVIEW  
Parent: Issue #97 / CII Phase 0  
Scope: static architecture only

## 1. Purpose

This ontology establishes the minimum shared vocabulary for ClimateOS Earth-system reasoning. It prevents direct, unsupported jumps from a global climate signal to a local hazard, observed impact, governance decision or building conclusion.

The canonical reasoning chain is:

`GlobalClimateDriver → RegionalClimateResponse → EnvironmentalCondition → HazardCandidate → Exposure → Vulnerability → ObservedImpact → Evidence → GovernanceContext`

Every transition must remain explicit, evidence-linked, uncertainty-bearing and bounded by spatial and temporal applicability.

## 2. Design principles

1. **One Earth system, differentiated regional responses.** Physical laws are shared globally; responses vary by region, season, hemisphere, lag and compound drivers.
2. **Probabilistic, not deterministic.** A driver may condition or modulate a tendency; it does not automatically produce a hazard or impact.
3. **Object separation.** Driver, response, hazard, exposure, vulnerability, impact and evidence are distinct objects.
4. **Provider neutrality.** BoM, ECMWF, NOAA, ACCESS, NARCliM, GraphCast, MAZU, FengHe and FengYun remain external providers described through common references.
5. **Evidence before governance.** Administrative, legal or compliance conclusions require jurisdiction-specific evidence and review.
6. **No silent uncertainty loss.** Confidence, uncertainty, lag, seasonality, validation and validity periods survive every handoff.

## 3. Core objects

### 3.1 EarthSystemContext

Defines the planetary and analytical context in which an assertion is made.

Minimum fields:

- `context_id`
- `hemisphere`
- `season_definition`
- `analysis_window`
- `spatial_scope`
- `baseline_reference`
- `version`

### 3.2 GlobalClimateDriver

Represents a large-scale oceanic, atmospheric or coupled state that may influence regional climate.

Examples: ENSO, IOD, SAM, MJO, subtropical ridge, monsoon, jet stream.

Minimum fields:

- `driver_id`
- `canonical_name`
- `aliases`
- `driver_class`
- `state_or_phase`
- `index_reference`
- `observation_window`
- `forecast_window`
- `spatial_scale`
- `temporal_scale`
- `hemisphere_context`
- `mechanism_references`
- `confidence`
- `uncertainty`
- `validation_status`
- `provider_references`
- `version`

A `GlobalClimateDriver` must not contain a local impact conclusion.

### 3.3 TeleconnectionRelationship

Represents an evidence-linked relationship between two objects.

Minimum fields:

- `relationship_id`
- `source_object_id`
- `target_object_id`
- `relationship_type`
- `direction_vocabulary`
- `strength_vocabulary`
- `seasonality`
- `lag_window`
- `spatial_applicability`
- `temporal_validity`
- `mechanism_references`
- `evidence_references`
- `confidence`
- `uncertainty`
- `validation_status`
- `competing_hypothesis_ids`

### 3.4 RegionalClimateResponse

Represents a regional tendency conditioned by one or more drivers.

Examples: rainfall tendency, blocking tendency, storm-track displacement, heat tendency, dryness tendency.

Minimum fields:

- `response_id`
- `response_type`
- `region_reference`
- `season_context`
- `hemisphere_context`
- `driver_relationship_ids`
- `direction_vocabulary`
- `magnitude_vocabulary`
- `lag_window`
- `confidence`
- `uncertainty`
- `evidence_references`
- `validation_status`

A response is a tendency, not a guaranteed event.

### 3.5 EnvironmentalCondition

Represents a measurable environmental state relevant to hazard formation.

Examples: soil moisture deficit, elevated fuel dryness, high sea-surface temperature, saturated catchment, persistent heat load.

Minimum fields:

- `condition_id`
- `condition_type`
- `measurement_or_proxy`
- `spatial_boundary`
- `observation_window`
- `threshold_reference`
- `provider_references`
- `confidence`
- `uncertainty`

### 3.6 HazardCandidate

Represents a potential hazard state that has not yet been confirmed as a local event or impact.

Examples: elevated flood potential, elevated bushfire-weather potential, tropical-cyclone steering corridor, drought candidate.

Minimum fields:

- `hazard_candidate_id`
- `hazard_type`
- `location_or_boundary`
- `validity_window`
- `triggering_condition_ids`
- `supporting_response_ids`
- `confidence`
- `uncertainty`
- `status`

Allowed status vocabulary:

- `hypothesised`
- `supported`
- `observed_event_pending`
- `rejected`
- `expired`

### 3.7 Exposure

Represents people, ecosystems, infrastructure, buildings or assets located within a relevant hazard boundary.

Minimum fields:

- `exposure_id`
- `exposure_type`
- `asset_or_population_reference`
- `spatial_boundary_version`
- `time_validity`
- `source_reference`

Exposure alone does not imply damage.

### 3.8 Vulnerability

Represents susceptibility to harm under a specified hazard or environmental condition.

Minimum fields:

- `vulnerability_id`
- `subject_reference`
- `hazard_type`
- `vulnerability_factor`
- `assessment_method`
- `jurisdiction_context`
- `validity_window`
- `confidence`
- `uncertainty`
- `evidence_references`

### 3.9 ObservedEvent

Represents a verified local meteorological, hydrological, ecological or geophysical event.

Minimum fields:

- `event_id`
- `event_type`
- `location_or_boundary`
- `start_time`
- `end_time`
- `observation_references`
- `quality_flags`
- `verification_status`

### 3.10 ObservedImpact

Represents documented consequences associated with an observed event and exposed subject.

Minimum fields:

- `impact_id`
- `event_id`
- `exposure_id`
- `impact_type`
- `observation_or_assessment_method`
- `time_recorded`
- `evidence_references`
- `attribution_status`
- `confidence`
- `uncertainty`

Attribution status vocabulary:

- `not_assessed`
- `associated`
- `partially_attributed`
- `formally_attributed`
- `contested`

### 3.11 EvidenceReference

Represents provenance and evidentiary context for any assertion.

Minimum fields:

- `evidence_id`
- `provider_reference`
- `product_or_document_id`
- `evidence_type`
- `method_scope`
- `spatial_boundary_version`
- `temporal_validity`
- `model_or_method_version`
- `calibration_or_validation_reference`
- `quality_flags`
- `uncertainty`
- `licence_and_access_status`
- `transformation_provenance`
- `retrieved_or_recorded_at`

### 3.12 ProviderReference

Represents a provider without embedding provider-specific runtime logic.

Minimum fields:

- `provider_id`
- `provider_name`
- `provider_type`
- `jurisdiction_or_scope`
- `credential_status`
- `capability_reference`
- `access_state`
- `licence_state`
- `verification_date`

### 3.13 GovernanceContext

Represents jurisdiction-specific review, legal, administrative or policy context.

Minimum fields:

- `governance_context_id`
- `jurisdiction`
- `authority_reference`
- `legal_or_policy_instrument`
- `effective_period`
- `review_status`
- `human_decision_required`
- `evidence_references`

No climate object may directly generate a governance conclusion without this layer.

## 4. Relationship vocabulary

Canonical relationship types:

- `DRIVES` — reserved for strongly established physical mechanisms; requires high evidentiary support.
- `MODULATES` — changes probability, intensity, timing or spatial expression.
- `INFLUENCES` — supported directional relationship with material uncertainty.
- `CONDITIONS` — establishes background state affecting later processes.
- `AMPLIFIES`
- `SUPPRESSES`
- `SHIFTS`
- `CONSTRAINS`
- `CO_OCCURS_WITH` — explicitly non-causal.
- `OBSERVED_AS`
- `EXPOSES`
- `AFFECTS`
- `SUPPORTED_BY`
- `CONTESTED_BY`
- `VALID_WITHIN`
- `GOVERNED_BY`

Relationship types must not be selected solely for rhetorical strength.

## 5. Confidence and uncertainty

### Confidence vocabulary

- `very_low`
- `low`
- `medium`
- `high`
- `very_high`

### Validation status

- `hypothesis`
- `literature_supported`
- `observationally_supported`
- `model_supported`
- `multi_source_supported`
- `validated_for_scope`
- `contested`
- `rejected`

### Uncertainty dimensions

- measurement uncertainty
- model uncertainty
- scenario uncertainty
- spatial-transfer uncertainty
- temporal-transfer uncertainty
- attribution uncertainty
- provider or transformation uncertainty

Confidence never substitutes for evidence references.

## 6. Prohibited shortcuts

The runtime must reject or flag:

- `ENSO → Australia drought`
- `ENSO → house cracking`
- `Subtropical ridge → cyclone landfall`
- `Remote-sensing signal → contamination confirmed`
- `AI output → legal or compliance conclusion`
- `Provider announcement → verified open-source availability`

Valid chains require intermediate objects and evidence.

## 7. Minimum valid examples

### Example A — Australian dryness pathway

`ENSO state → RegionalClimateResponse(dryness tendency) → EnvironmentalCondition(soil moisture deficit) → HazardCandidate(drought) → Exposure(site) → Vulnerability(reactive soil/building system) → ObservedImpact(crack evidence)`

The chain stops at any stage where evidence is absent.

### Example B — Tropical-cyclone steering pathway

`Subtropical ridge state + monsoon flow + mid-latitude trough → steering-flow response → HazardCandidate(track corridor) → ObservedEvent(track)`

The ridge is an important influence, not the sole cause.

## 8. Versioning and extension

New drivers, providers, regions and hazard types must be added through registries and controlled vocabularies. Core object boundaries may only change through an explicit architecture revision.

## 9. Acceptance checklist

- [ ] Global driver is separate from regional response.
- [ ] Regional response is separate from hazard candidate.
- [ ] Hazard candidate is separate from observed event and impact.
- [ ] Exposure and vulnerability are explicit.
- [ ] Every relationship carries season, lag, confidence, uncertainty and evidence.
- [ ] Provider references are neutral.
- [ ] Governance conclusions require human review and jurisdiction context.
