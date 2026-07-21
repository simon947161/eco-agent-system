# Teleconnection Evidence Graph v0.1

Status: DRAFT_FOR_FOUNDER_REVIEW  
Parent: Issue #98  
Base dependency: Earth System Ontology v0.1

## 1. Purpose

The Teleconnection Evidence Graph represents climate relationships as explicit, probabilistic, evidence-linked paths. It prevents direct jumps from a large-scale driver to a local hazard, impact or governance conclusion.

Canonical path:

`GlobalClimateDriver → circulation/ocean mechanism → RegionalClimateResponse → EnvironmentalCondition → HazardCandidate → ObservedEvent → ObservedImpact`

Any path may branch, terminate, compete with another hypothesis or remain unresolved.

## 2. Node classes

Allowed node classes:

- `GlobalClimateDriver`
- `CirculationMechanism`
- `OceanState`
- `RegionalClimateResponse`
- `EnvironmentalCondition`
- `HazardCandidate`
- `ObservedEvent`
- `Exposure`
- `Vulnerability`
- `ObservedImpact`
- `EvidenceReference`
- `ProviderReference`
- `GovernanceContext`

## 3. Edge contract

Every edge must contain:

- `edge_id`
- `source_object_id`
- `target_object_id`
- `relationship_type`
- `mechanism_reference`
- `seasonality`
- `hemisphere_context`
- `lag_window`
- `direction_vocabulary`
- `strength_vocabulary`
- `spatial_applicability`
- `temporal_validity`
- `confidence`
- `uncertainty`
- `evidence_references`
- `validation_status`
- `competing_hypothesis_ids`
- `compound_driver_ids`

## 4. Graph rules

1. A driver node cannot connect directly to `ObservedImpact`.
2. `HazardCandidate` cannot be promoted to `ObservedEvent` without observation evidence.
3. A path may contain multiple drivers.
4. Contradictory or regionally divergent edges are allowed and must remain visible.
5. Season, hemisphere and lag are required for all climate-response edges.
6. Provider disagreement must be represented through separate evidence references.
7. Governance nodes are terminal review contexts, not physical causes.

## 5. Relationship semantics

- `DRIVES`: strongly established physical mechanism; use sparingly.
- `MODULATES`: alters likelihood, intensity, timing or spatial expression.
- `INFLUENCES`: supported directional relationship with material uncertainty.
- `CONDITIONS`: establishes background state.
- `AMPLIFIES` / `SUPPRESSES`: modifies an existing tendency.
- `SHIFTS`: displaces circulation, track or spatial distribution.
- `CONSTRAINS`: restricts plausible pathways.
- `CO_OCCURS_WITH`: association only.
- `OBSERVED_AS`: links a candidate or process to verified observation.
- `SUPPORTED_BY` / `CONTESTED_BY`: evidence relationship.

## 6. Divergent ENSO response fixture

The same ENSO phase may support different regional tendencies.

### Eastern Australia pathway

`ENSO(el_nino)`
→ `MODULATES WalkerCirculation`
→ `INFLUENCES EasternAustraliaRainfallTendency`
→ `CONDITIONS SoilMoistureDeficit`
→ `SUPPORTS DroughtHazardCandidate`

Required qualifiers:

- season-specific
- region-specific
- lag-specific
- compound-driver-sensitive
- no automatic observed drought or damage conclusion

### Western Australia pathway

`ENSO(el_nino)`
→ `INFLUENCES IndianOceanPacificBackgroundState`
→ `MODULATES WesternAustraliaRainfallTendency`

This path may differ in sign, strength or confidence from eastern Australia and must not reuse the same edge without regional evidence.

### China pathway

`ENSO(el_nino)`
→ `MODULATES WesternPacificOceanAtmosphereState`
→ `INFLUENCES MonsoonAndSubtropicalRidgeConfiguration`
→ `INFLUENCES RegionalRainfallOrTyphoonEnvironmentTendency`

The path must preserve season, lag, region and competing drivers. It cannot conclude rainfall, landfall or impact at a specific location without local evidence.

## 7. Tropical-cyclone steering fixture

Valid multi-driver pathway:

`SubtropicalRidgeState`
+ `MonsoonFlowState`
+ `MidLatitudeTroughState`
+ `DeepLayerWindField`
→ `MODULATES TropicalCycloneSteeringEnvironment`
→ `SUPPORTS TrackCorridorHazardCandidate`
→ `OBSERVED_AS TropicalCycloneTrack`

Guardrails:

- subtropical ridge is important but not unique;
- genesis, intensification and steering remain separate processes;
- track corridor is probabilistic;
- landfall requires observed or forecast-specific evidence;
- impact requires exposure, vulnerability and observation evidence.

## 8. Compound-driver model

A graph may combine drivers using an explicit `CompoundDriverContext` containing:

- participating driver IDs
- interaction type
- compatible time windows
- regional applicability
- evidence references
- confidence and uncertainty
- whether interaction is additive, amplifying, suppressing, offsetting or unresolved

The graph must not assume that two individually supported relationships remain valid when combined.

## 9. Competing hypotheses

Competing paths are first-class graph objects.

Example:

- H1: rainfall tendency primarily modulated by ENSO-related circulation
- H2: rainfall tendency primarily modulated by IOD
- H3: local blocking and synoptic variability dominate during the event window

Each hypothesis carries evidence, scope and validation status. The runtime may rank but must not silently delete alternatives.

## 10. Stop conditions

A path must stop when:

- evidence is absent;
- spatial transfer exceeds validated scope;
- temporal validity has expired;
- provider outputs conflict without resolution;
- uncertainty exceeds the configured decision threshold;
- the next node would require a legal, compliance or administrative conclusion.

## 11. Acceptance tests

The implementation must reject:

- `ENSO → ObservedImpact`
- `ENSO → HouseCrack`
- `SubtropicalRidge → CycloneLandfall`
- `HazardCandidate → GovernanceDecision`

The implementation must support:

- one driver branching to multiple regional responses;
- multiple drivers converging on one response;
- opposite or conflicting tendencies by region or season;
- explicit lag and validity periods;
- competing hypotheses;
- evidence-backed termination at `HazardCandidate`.

## 12. Founder review gate

Founder review is required before:

- connecting live provider data;
- executing forecasts;
- using real project or property data;
- producing governance, compliance or damage conclusions.
