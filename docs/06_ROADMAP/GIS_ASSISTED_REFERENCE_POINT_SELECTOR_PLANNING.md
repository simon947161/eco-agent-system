# GIS-Assisted Reference Point Selector Planning

## Purpose

This document defines the future GIS-assisted and model-assisted reference point selector for CCZPS-Lite spatial intelligence.

Task 29 is planning only. It does not implement GIS automation, mapping integration, DEM processing, watershed modelling, wind-corridor analysis, ENVI-met integration, Fluent or CFD integration, external APIs, credentials, browser automation, simulation workflows, or autonomous recommendations.

Future CCZPS spatial intelligence should support advanced spatial computation tools responsibly. These tools are not unnecessary; they are future required capabilities for higher-quality upstream, downstream, upwind, downwind, highland, lowland, and lateral reference point selection.

## Future Required Capabilities

Future versions should support:

- Google Earth and mapping-based spatial review for user-visible spatial context and manual validation.
- DEM-based elevation and watershed analysis for highland, lowland, upstream, and downstream context.
- Upstream and downstream reference point suggestion from watershed and drainage evidence.
- Prevailing wind and wind-corridor reference point suggestion for upwind and downwind context.
- Highland, lowland, and lateral comparison point suggestion from topography, landform, corridor, and distance constraints.
- Watershed-scale and corridor-scale analysis from local site context to regional and 1000 km+ contexts where the project requires that scale.
- ENVI-met for future microclimate-scale assessment.
- Fluent or CFD-style tools for advanced wind, turbulence, and flow assessment where warranted.
- Other spatial computation tools where appropriate, subject to provenance, licensing, governance, and Budget Guard checks.

The system should enable advanced tools responsibly. It should not silently block them, silently consume them, or treat them as free.

## Future Connector Architecture

The future selector should remain provider-agnostic and modular:

1. Core Location Input

   The user supplies or confirms a core location with coordinates, scenario identity, spatial scale, intended analysis purpose, and acceptable cost/risk mode.

2. Spatial Context Connectors

   Separate connectors may support mapping review, DEM/elevation analysis, watershed analysis, wind/corridor analysis, microclimate analysis, CFD-style flow assessment, and other spatial computation sources.

3. Candidate Point Generator

   A deterministic candidate generator may propose upstream, downstream, upwind, downwind, highland, lowland, and lateral reference points only from declared data inputs. Suggestions must expose the rules, source, distance, direction, coordinates, confidence, missing data, and limitations.

4. Human Review Gate

   Suggested points remain proposals until the user accepts, edits, rejects, or replaces them. CCZPS should preserve user-selected points and avoid presenting suggestions as field-validated truth.

5. Evidence Output Layer

   Accepted or proposed points should be written into the existing spatial transect schema with source, confidence, provenance, retrieval status, cost governance status, and Budget Guard status.

## Required Data Inputs

Future implementations may require:

- Core location coordinates, coordinate reference system, location name, scenario id, and user-supplied context.
- Target spatial scale, such as site, local corridor, watershed, regional corridor, or 1000 km+ analysis.
- DEM or elevation data with source, resolution, vertical datum, coverage, licensing, and uncertainty.
- Watershed or hydrology data with drainage network, catchment boundary, flow direction, and source metadata.
- Wind data with prevailing direction, seasonal variation, elevation context, and confidence.
- Landform, land cover, corridor, boundary, or infrastructure context where relevant.
- Mapping imagery or base-map references for human review.
- Optional microclimate or CFD model input requirements, including boundary conditions, mesh/domain assumptions, and model limitations.
- Governance profile, usage mode, resource owner, expected external resources, estimated cost intensity, and approval status.

## Governance Requirements

External resource costs belong to the resource consumer. If external tools, APIs, cloud services, satellite services, GIS providers, DEM services, model services, or third-party compute systems are used, the cost must be governed by the existing Usage & Cost Governance Runtime and Budget Guard Runtime.

Future selector outputs should expose:

- external_resource_owner;
- external_cost_bearer;
- provider or data source;
- estimated_external_resource_cost;
- estimated call count or compute intensity;
- platform_service_fee_model when applicable;
- budget_warning;
- requires_user_approval;
- Budget Guard status;
- retrieval or execution status;
- cache status;
- confidence and provenance;
- licensing and usage constraints.

No payment processing, subscriptions, invoicing, token systems, crypto, or marketplace logic should be introduced by the selector.

## Budget Guard Requirements

Budget Guard must protect any live or cost-bearing spatial resource call.

Before execution, the future selector should determine:

- whether the requested spatial scale is low, medium, high, or very high cost intensity;
- whether the workflow is one-time, repeated, scheduled, or agentic;
- whether external calls, model runs, or cloud compute are required;
- whether cached data can satisfy the request;
- whether daily call, monthly budget, or agent-run limits may be exceeded;
- whether `stop_required`, `approval_required`, `warning`, or `within_budget` applies.

If Budget Guard returns `stop_required`, the selector must not call the external tool or model. If the guard requires approval, the selector must wait for explicit user approval.

## User Approval Requirements

Future GIS-assisted and model-assisted point selection must require explicit user approval before:

- live GIS, mapping, DEM, watershed, wind, satellite, or model service calls;
- paid API calls;
- cloud compute or model execution;
- ENVI-met or Fluent-style simulation setup or execution;
- repeated or scheduled spatial analysis;
- writing accepted suggested points into project outputs when that action changes repository or dashboard evidence.

Approval should identify the resource owner, expected external resource use, estimated cost intensity, data source, provider, and action being approved.

## Provider-Agnostic Design

The selector should avoid hard-coding one mapping, DEM, weather, hydrology, microclimate, or CFD provider. Provider adapters should translate provider-specific data into a common internal spatial evidence format.

The common format should preserve:

- point role;
- coordinates;
- coordinate reference system;
- direction and distance from core;
- elevation and elevation context;
- watershed or corridor relationship;
- source;
- retrieval or execution timestamp;
- provenance;
- confidence;
- missing-data status;
- governance status;
- Budget Guard status;
- limitations.

## Suggested Reference Point Workflow

For a user-selected core location, a future workflow may:

1. Validate the core coordinates and spatial scale.
2. Run Usage & Cost Governance and Budget Guard checks.
3. Ask for user approval if live or cost-bearing resources are required.
4. Retrieve or use cached mapping, DEM, watershed, wind, corridor, or model evidence.
5. Generate candidate upstream and downstream points from declared watershed evidence.
6. Generate candidate upwind and downwind points from declared wind or corridor evidence.
7. Generate candidate highland and lowland points from DEM or elevation evidence.
8. Generate candidate lateral points from configured distance, corridor, boundary, or comparison rules.
9. Attach source, confidence, missing-data, governance, and limitation fields to every candidate.
10. Present candidates for human review.
11. Store only accepted or explicitly retained candidates in the spatial transect outputs.

The selector must not infer watershed or wind relationships when the required source data is absent.

## Staged Implementation Roadmap

Stage 1: Planning and schema alignment

- Keep Task 29 as planning only.
- Confirm schema fields needed for source, confidence, provenance, licensing, governance, Budget Guard, cache, and missing data.
- Define provider-agnostic adapter interfaces.

Stage 2: Local fixture expansion

- Add non-live sample fixtures for DEM, watershed, wind corridor, and mapping review outputs.
- Test point suggestion rules using local fixtures only.
- Preserve no-field-validation labels.

Stage 3: User-controlled connector scaffolds

- Add disabled-by-default connector definitions for mapping, DEM, watershed, wind, ENVI-met, Fluent or CFD-style systems, and other spatial computation tools.
- Add governance and Budget Guard preflight records.
- Add explicit user approval gates.

Stage 4: Live retrieval pilots

- Enable selected public or user-provided services only behind manual approval and Budget Guard.
- Cache retrieved spatial data where licensing permits.
- Expose retrieval status, provenance, and confidence.

Stage 5: Model-assisted assessment

- Add microclimate or CFD-style workflows only when users provide required model inputs and approve cost-bearing compute.
- Keep simulation outputs separate from lightweight reference point suggestions.
- Require human review and explicit limitations.

Stage 6: Review, validation, and audit

- Add reproducibility reports, source audits, licensing checks, and validation notes.
- Preserve clear boundaries between suggested points, accepted points, field-validated points, and model-derived evidence.

## Safety Boundaries

Future development must preserve these boundaries:

- Do not make live GIS, DEM, mapping, watershed, wind, ENVI-met, Fluent, CFD, satellite, cloud, or paid API calls without explicit task scope, Usage & Cost Governance, Budget Guard checks, and user approval.
- Do not claim field validation unless field validation evidence is supplied and reviewed.
- Do not claim regulatory, scientific, engineering, construction, or planning readiness.
- Do not treat generated reference points as autonomous decisions.
- Do not convert spatial evidence into design or construction recommendations.
- Do not hide external costs or resource ownership.
- Do not embed credentials or provider-specific secrets.
- Do not imply endorsement or guaranteed availability of any commercial tool.

## Task 29 Status

This document is the Task 29 deliverable. It defines the future GIS-assisted and model-assisted reference point selector architecture and governance plan. It does not implement runtime features.
