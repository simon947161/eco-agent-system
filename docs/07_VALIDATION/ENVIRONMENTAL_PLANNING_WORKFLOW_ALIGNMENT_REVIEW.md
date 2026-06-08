# Environmental Planning Workflow Alignment Review

## Purpose

This document reviews how the current CCZPS-Lite implementation aligns with a mature environmental planning and design workflow.

It is a planning-validation review only. It does not add runtime logic, dashboard behavior, workflows, APIs, external connectors, simulations, or autonomous decision capabilities.

CCZPS-Lite is currently a transparent, rule-based demonstrator. It is not a final planning approval system, professional engineering system, scientific simulation platform, or substitute for qualified human review.

## Assessment Method

Each workflow stage is classified as:

- **Covered**: the repository contains an implemented capability that materially supports the stage.
- **Partially covered**: the repository supports part of the stage, but important professional data, tools, validation, or workflow controls are absent.
- **Missing**: the stage does not yet have a dedicated implemented layer.

## Overall Alignment Matrix

| Mature workflow stage | Current alignment | Current CCZPS-Lite capabilities | Main gaps |
| --- | --- | --- | --- |
| 1. Geographic context review | Partially covered | Scenario Pack; Spatial Context & Transect Runtime; Reports; Dashboard | No live mapping review, GIS layers, automated scale selection, or professional spatial review workflow |
| 2. Regional and site background analysis | Partially covered | Scenario Pack; Evidence Layer; Spatial Context & Transect Runtime; Reports | Background datasets are configured and limited; no systematic regional/site data acquisition or provenance review |
| 3. Climate and environmental condition analysis | Partially covered | Meteorology Connector; Time-Series Store; Trend Reading; Evidence Layer; Dashboard | NASA POWER is the only optional live source; NOAA, ERA5, and BOM remain scaffolded; no comprehensive environmental condition model |
| 4. Terrain, watershed, wind, elevation, and spatial-pattern analysis | Partially covered | Spatial Context & Transect Runtime; configured reference roles; Task 29 planning | No implemented GIS, DEM, watershed, wind-corridor, ENVI-met, Fluent, or CFD analysis |
| 5. Problem identification | Covered at concept level | Differential Field Runtime; Forcing Layer Runtime; Evidence Layer; Validation Layer | Outputs remain rule-based candidate signals, not professionally verified diagnoses |
| 6. Planning hypothesis / design assumption formation | Partially covered | Scenario Pack; Forcing Layer; Adaptive Response Runtime; Reports | No dedicated Planning Hypothesis Runtime; assumptions are not managed as explicit testable hypotheses |
| 7. Scenario or intervention concept generation | Covered at concept level | Scenario Pack; Adaptive Response Runtime; Response Prioritisation Runtime; Dashboard; Reports | Concepts are configured/rule-based and are not professional designs or implementation plans |
| 8. Professional simulation and tool-based validation | Missing | Governance and Budget Guard can govern future tool use; Task 29 defines planned connector pathway | No Simulation Validation Interface; no ENVI-met, Fluent/CFD, GIS, DEM, watershed, or professional model execution |
| 9. Fit assessment between hypothesis and evidence | Partially covered | Evidence Layer; Validation Layer; Review Loop; scenario comparison reports | No dedicated Iteration and Fit Assessment Runtime linking explicit hypotheses to validation evidence |
| 10. Iterative refinement and re-validation | Partially covered | Review Loop; Adaptive Response Runtime; Response Prioritisation; repeated meteorology observations; Reports | No persistent hypothesis/version lifecycle, iteration history, formal re-validation state machine, or expert sign-off process |

## Stage Review

### 1. Geographic Context Review

**Alignment: Partially covered**

Current support:

- The Scenario Pack provides named contexts for Batlow, Kunlun, Iraq, and Baiyangdian-Xiong'an.
- The Spatial Context & Transect Runtime represents a user-selected core point and configured upstream, downstream, upwind, downwind, highland, lowland, and lateral reference points.
- Dashboard and reports expose local scenario and spatial context outputs.

Current limitations:

- Reference points are configured fixtures rather than GIS-derived suggestions.
- There is no Google Earth or mapping-based review interface.
- There is no automated local-to-regional scale selection.
- There is no professional spatial-review record or map annotation workflow.

### 2. Regional And Site Background Analysis

**Alignment: Partially covered**

Current support:

- The Scenario Pack and local input profiles provide basic regional and site context.
- The Evidence Layer exposes source basis, evidence strength, uncertainty, and human review requirements.
- Reports consolidate configured scenario information.

Current limitations:

- Background analysis is not assembled from a comprehensive provider-agnostic data acquisition layer.
- Land use, ecology, infrastructure, social context, regulatory constraints, and historical site records are not systematically integrated.
- Provenance and licensing are not yet enforced across a professional background-analysis workflow.

### 3. Climate And Environmental Condition Analysis

**Alignment: Partially covered**

Current support:

- The Meteorology Connector standardises temperature, rainfall, humidity, wind, solar radiation, and evaporation fields where available.
- NASA POWER has an optional explicit live retrieval path.
- NOAA, ERA5, and BOM have source definitions and field mappings.
- The Meteorology Time-Series Store retains successful observations.
- Meteorology Trend Reading produces conservative rule-based evidence signals.
- Meteorology evidence is exposed in the Dashboard and Evidence Layer.

Current limitations:

- NOAA, ERA5, and BOM do not have implemented live retrieval.
- Trend readings are not forecasting or statistical climate analysis.
- Broader environmental conditions such as soil, water quality, biodiversity, pollution, and land-cover change are not comprehensively integrated.
- Observations remain supporting evidence and do not establish causation.

### 4. Terrain, Watershed, Wind, Elevation, And Spatial-Pattern Analysis

**Alignment: Partially covered**

Current support:

- The Spatial Context & Transect Runtime preserves configured coordinates, direction, distance, elevation context, source, confidence, and missing-data status.
- The Transect Scenario Pack demonstrates configured spatial roles across four contexts.
- Task 29 defines a future GIS-assisted and model-assisted connector architecture.

Current limitations:

- No live GIS or mapping integration.
- No DEM-derived elevation or terrain analysis.
- No watershed delineation or flow-direction computation.
- No prevailing-wind or wind-corridor analysis.
- No automatic reference point suggestion.
- No ENVI-met microclimate assessment.
- No Fluent or CFD-style wind and turbulence assessment.
- No implemented local, regional, corridor, watershed, or 1000 km+ spatial analysis engine.

### 5. Problem Identification

**Alignment: Covered at concept level**

Current support:

- Differential Field Runtime identifies configured water, heat, vegetation, and fire gradient signals.
- Forcing Layer Runtime derives transparent candidate environmental pressures.
- Evidence Layer identifies evidence quality and uncertainty.
- Validation Layer identifies gaps and cautious validation status.

Current limitations:

- Problem statements are derived from local rules and configured inputs.
- Candidate forcings are not causal proof.
- Professional diagnosis, field evidence, and specialist review remain required.

### 6. Planning Hypothesis / Design Assumption Formation

**Alignment: Partially covered**

Current support:

- Scenario definitions contain concept assumptions.
- Forcing Layer outputs provide candidate explanations.
- Adaptive Response Runtime translates validation and review signals into candidate response options.
- Reports preserve reasoning summaries.

Current limitations:

- There is no dedicated Planning Hypothesis Runtime.
- Hypotheses are not explicit versioned objects with assumptions, evidence requirements, falsification conditions, confidence, owners, and review state.
- Design assumptions are not linked to professional standards or simulation requirements.

### 7. Scenario Or Intervention Concept Generation

**Alignment: Covered at concept level**

Current support:

- Scenario Pack provides configured pathway concepts.
- Adaptive Response Runtime produces candidate concept-level responses.
- Response Prioritisation Runtime orders candidate responses for review.
- Dashboard and reports compare scenarios and expose evidence limitations.

Current limitations:

- Outputs are not final designs, plans, specifications, or construction recommendations.
- Scenario generation is rule-based and configured rather than a complete participatory planning process.
- Feasibility, compliance, engineering, social, and financial validation remain outside the current system.

### 8. Professional Simulation And Tool-Based Validation

**Alignment: Missing**

Current support:

- Usage & Cost Governance can classify future external resource use.
- Budget Guard can protect future live or cost-bearing calls.
- Task 29 defines the planned GIS/DEM/watershed/wind/ENVI-met/Fluent pathway.

Required future capability:

- A Simulation Validation Interface that can register model purpose, inputs, boundary conditions, provider, version, execution status, cost owner, Budget Guard status, outputs, uncertainty, and expert review.
- Provider-agnostic GIS, DEM, watershed, wind, ENVI-met, Fluent/CFD, and other professional tool connectors.
- Separation between lightweight spatial suggestions and computational simulation.
- Explicit user approval before live, paid, cloud, or compute-intensive execution.

### 9. Fit Assessment Between Hypothesis And Evidence

**Alignment: Partially covered**

Current support:

- Evidence Layer exposes evidence strength and uncertainty.
- Validation Layer produces validation scores, statuses, and gaps.
- Review Loop assigns review actions, priorities, owners, and triggers.
- Reports compare scenario evidence and validation.

Current limitations:

- There is no dedicated Iteration and Fit Assessment Runtime.
- Current validation assesses scenario readiness, but does not formally compare a versioned planning hypothesis against expected and observed evidence.
- Contradictory evidence, residual mismatch, acceptance criteria, and hypothesis retirement are not managed explicitly.

### 10. Iterative Refinement And Re-Validation

**Alignment: Partially covered**

Current support:

- Review Loop identifies next review action and owner.
- Adaptive Response Runtime proposes candidate response options.
- Response Prioritisation Runtime orders review attention.
- Meteorology Time-Series Store supports repeated observations.
- Reports can be regenerated after input changes.

Current limitations:

- There is no persistent iteration history for planning hypotheses and scenarios.
- There is no formal re-validation state machine.
- The system does not track which evidence or simulation result caused a revision.
- There is no implemented professional sign-off, multidisciplinary review, community review, or approval workflow.

## Current Capability Map

### Covered At Demonstrator Level

- Scenario Pack.
- Concept-level problem identification.
- Differential Field Runtime.
- Forcing Layer Runtime.
- Evidence Layer.
- Validation Layer.
- Review Loop.
- Adaptive Response Runtime.
- Response Prioritisation Runtime.
- Usage & Cost Governance.
- Budget Guard.
- Dashboard presentation.
- Local generated reports.

### Partially Covered

- Geographic context review.
- Regional and site background analysis.
- Climate and environmental condition analysis.
- Meteorology observation history and trend evidence.
- Spatial transect context.
- Planning assumption formation.
- Fit assessment.
- Iterative review and re-validation.
- Human review routing.

### Missing As Dedicated Professional Layers

- Planning Hypothesis Runtime.
- Simulation Validation Interface.
- Live GIS / DEM / watershed / wind / ENVI-met / Fluent connector pathway.
- Iteration and Fit Assessment Runtime.
- Formal human expert review and approval process.

## Future Required Layers

### Planning Hypothesis Runtime

This layer should create explicit, versioned planning hypotheses with problem statement, proposed mechanism, design or planning assumptions, expected evidence, contradictory or falsifying evidence, spatial and temporal scope, confidence, evidence gaps, simulation requirements, review owner, status, and revision history.

It should not convert hypotheses into approved plans automatically.

### Simulation Validation Interface

This interface should connect hypotheses and scenarios to professional tools without hard-coding one provider.

It should support model purpose and suitability; input and boundary-condition declarations; provider, software, and version; execution provenance; cost ownership; Usage & Cost Governance reading; Budget Guard status; explicit user approval; cached or live execution status; output uncertainty and limitations; and professional reviewer sign-off.

### GIS / DEM / Watershed / Wind / ENVI-met / Fluent Connector Pathway

The future pathway should support:

- Google Earth and mapping-based spatial review;
- DEM-derived elevation, slope, terrain, and watershed context;
- upstream and downstream point suggestion;
- prevailing-wind and wind-corridor analysis;
- upwind and downwind point suggestion;
- highland, lowland, and lateral comparison point suggestion;
- local, watershed, corridor, regional, and 1000 km+ analysis scales;
- ENVI-met microclimate assessment;
- Fluent or CFD-style wind and turbulence assessment;
- other spatial computation tools where appropriate.

These tools should be enabled responsibly, not treated as unnecessary or prohibited. Live and cost-bearing use must remain provider-agnostic, governed, guarded, approved, and transparent.

### Iteration And Fit Assessment Runtime

This layer should compare expected hypothesis evidence with observations and simulations; record matches, mismatches, unknowns, and contradictory evidence; calculate transparent fit classifications without claiming scientific proof; identify required revisions; preserve version and review history; trigger re-validation after material changes; and keep human approval separate from automated assessment.

### Human Expert Review Process

A mature workflow requires an explicit human process involving relevant disciplines.

The future process should support named review roles and responsibilities; local and community knowledge; environmental science review; GIS, hydrology, microclimate, wind, engineering, planning, and governance review where applicable; evidence and simulation review; conflict and uncertainty records; approval, rejection, revision, and escalation decisions; and auditable sign-off without implying that CCZPS itself grants professional approval.

## Governance Alignment

Usage & Cost Governance and Budget Guard are important strengths in the current demonstrator.

Future GIS, DEM, watershed, wind, satellite, ENVI-met, Fluent/CFD, cloud, AI, sensor, and third-party services should expose external resource owner, external cost bearer, provider and service, estimated cost intensity, estimated calls or compute, approval requirement, Budget Guard status, cache status, provenance, licensing constraints, and execution or retrieval status.

If Budget Guard returns `stop_required`, the external action must not execute. Cost-bearing or live actions requiring approval must wait for explicit user approval.

## Readiness Judgement

### Suitable As A v1.0 Demonstrator

Yes.

CCZPS-Lite is suitable as a v1.0 demonstrator because it shows a coherent, transparent workflow for scenario exploration, evidence structuring, rule-based environmental signals, validation gaps, review routing, resource governance, guarded observation retrieval, dashboard presentation, and configured spatial context.

### Suitable For Case Exploration, Evidence Structuring, And Workflow Demonstration

Yes.

The current system is suitable for exploring configured environmental cases; organising observational and concept-level evidence; demonstrating how environmental reasoning layers may connect; making uncertainty, governance, cost ownership, and review needs visible; and testing future workflow and connector architecture.

### Suitable As A Final Professional Planning Decision System

No.

CCZPS-Lite is not yet suitable as a final professional planning decision system because it lacks a dedicated Planning Hypothesis Runtime; professional GIS and spatial-analysis connectors; DEM, watershed, and wind analysis; ENVI-met and Fluent/CFD-style simulation interfaces; formal fit and iteration management; multidisciplinary expert review and sign-off; and regulatory, scientific, engineering, planning, financial, and site-specific validation.

## Conclusion

CCZPS-Lite aligns with the early and middle stages of a mature environmental planning workflow at a demonstrator level. It is strongest in transparent scenario comparison, evidence structuring, rule-based problem signals, review routing, cost governance, Budget Guard control, and workflow communication.

Its largest gaps are explicit hypothesis management, professional spatial intelligence, simulation validation, formal fit assessment, persistent iteration, and human expert approval.

The appropriate readiness position is:

- suitable as a v1.0 demonstrator;
- suitable for case exploration, evidence structuring, and workflow demonstration;
- not yet suitable as a final professional planning decision system.
