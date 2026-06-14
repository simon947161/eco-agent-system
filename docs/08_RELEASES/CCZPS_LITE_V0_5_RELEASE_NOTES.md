# CCZPS-Lite v0.5 Release Notes

## Release Purpose

CCZPS-Lite v0.5 packages the existing deterministic, local-first environmental
intelligence and planning-support foundation as a coherent public demonstrator.
It connects evidence, planning hypotheses, validation support, traceability,
internal governance support, scenario comparison, reporting, and mandatory
human review.

This release adds documentation and packaging only. It does not add analytical
runtime capability.

## Major Features

- transparent scenario and evidence runtime
- cached meteorology evidence, time-series storage, and trend readings
- configured spatial context and transect records
- testable planning hypotheses with explicit failure conditions
- GIS/DEM access planning without live acquisition
- professional-validation and expert-review record templates
- planning-approval support reports that remain `not_ready_for_approval`
- evidence traceability linking outputs to local supporting records
- internal governance decision support with mandatory human review
- cross-scenario evidence comparison without winner selection
- static dashboard and GitHub Pages packaging
- usage, cost, budget-guard, cache-first, and manual-approval controls

## Architecture Summary

```text
Scenario Layer
  -> Evidence and Meteorology Layers
  -> Spatial Context Layer
  -> Planning Hypothesis Layer
  -> Validation Support Layer
  -> Evidence Traceability Layer
  -> Internal Governance Decision Support Layer
  -> Scenario Comparison Layer
  -> Dashboard and Reporting
  -> Human and Professional Review
```

The [architecture summary](CCZPS_LITE_V0_5_ARCHITECTURE_SUMMARY.md) describes
the inputs, outputs, and boundaries of each layer.

## Runtime Overview

The Python runtimes under `cczps_lite/engine/` read repository-local JSON and
produce inspectable JSON, CSV, and Markdown under `cczps_lite/output/`. The same
inputs produce the same outputs. External services are not required for the
packaged demonstration.

The four demonstration contexts are:

- Batlow
- Kunlun
- Iraq
- Baiyangdian-Xiong'an

## Validation Workflow

```text
Evidence
  -> Planning Hypothesis
  -> Professional Validation Template
  -> Expert Review Record
  -> Planning Approval Support
  -> Evidence Traceability
  -> Internal Governance Support
  -> Scenario Comparison
  -> Human Review
```

Incomplete or missing evidence remains visible. Professional and expert review
templates are not treated as completed findings.

## Dashboard Overview

The static dashboard in `cczps_lite/dashboard/` reads generated local outputs.
It presents the runtime matrix, meteorology, planning hypotheses, governance
support, and scenario comparison without browser-side environmental API calls.

## Demonstration Scenarios

- **Batlow:** water, heat, fire, ecology, and continuity context.
- **Kunlun:** dryland water limitation, ecological buffering, and incomplete
  spatial context.
- **Iraq:** agricultural recovery, heat, water scarcity, soil, and shelterbelt
  context.
- **Baiyangdian-Xiong'an:** headwater, wetland, downstream, and watershed
  continuity context.

These are demonstrator contexts, not approved plans or implementation designs.

## Known Limitations

- evidence is limited, uneven, and not a substitute for field validation
- meteorology trends are descriptive stored-observation readings, not forecasts
- spatial transects are configured relationships, not live GIS analysis
- GIS/DEM data is planned but not acquired or processed
- professional-validation and expert-review records remain incomplete
- all planning-approval support records remain `not_ready_for_approval`
- comparison groups describe evidence coverage; they do not rank options
- CI verifies deterministic behavior, not scientific or regulatory validity

## Safety Boundaries

CCZPS-Lite v0.5 is not:

- a statutory planning approval tool
- an engineering approval tool
- an environmental approval authority
- a construction decision system
- a legal compliance determination system
- a professional certification system
- a financial or investment recommendation system

Human and professional review remain mandatory. No output grants planning,
engineering, environmental, regulatory, construction, legal, financial, or
investment readiness.

Task 40 adds no external API, no LLM call, no GIS/DEM runtime, no simulation,
no approval logic, and no automated recommendation capability.

## Future Roadmap

Future work should prioritize professional review, field evidence, versioned
schemas, broader fixtures, accessibility, and pilot evaluation before adding
operational integrations. GIS, simulation, external data, or automated workflow
capabilities require separate governed tasks.

## Relationship to ClimateOS

CCZPS-Lite v0.5 is a small, deterministic foundation, not a complete ClimateOS.
It demonstrates an inspectable evidence-to-review chain that a future ClimateOS
may reuse and extend under stronger data, validation, security, and governance
requirements.

## Future Application Layers

CCZPS-Lite v0.5 provides the environmental intelligence kernel and
governance-support foundation that future application-layer systems may reuse.
FarmerOS, GardenOS, WaterOS, and ClimateOS are future application-layer
directions, not implemented in this release.
