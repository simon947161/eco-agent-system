# ClimateOS Master Directory Map

## Purpose

This document maps the long-term ClimateOS repository scaffold. The folders are
documentation-only extension points. They do not add runtime, scientific,
simulation, GIS, API, dashboard, approval, ranking, recommendation, payment, or
AI capability.

## Repository Tree

```text
00_PROJECT_CONTROL/
01_CLIMATEOS_CORE/
  runtime/
  evidence/
  validation/
  governance/
  ontology/
  interfaces/
02_CARBONOS/
  green_power_agent/
  carbon_accounting_agent/
  carbon_budget_agent/
  carbon_verification_agent/
  carbon_market_agent/
  product_carbon_passport_agent/
03_ENERGYOS/
  renewable_energy_agent/
  energy_storage_agent/
  grid_connection_agent/
  energy_scenario_agent/
04_WATEROS/
  water_balance_agent/
  watershed_agent/
  flood_resilience_agent/
  water_quality_agent/
05_LANDOS/
  land_use_agent/
  soil_health_agent/
  desertification_agent/
  land_restoration_agent/
06_BIODIVERSITYOS/
  species_agent/
  habitat_agent/
  ecological_corridor_agent/
  ecosystem_health_agent/
07_PARKOS/
  zero_carbon_park_agent/
  industrial_park_agent/
  infrastructure_agent/
08_ESGOS/
  disclosure_agent/
  esg_audit_agent/
  scorecard_agent/
  materiality_agent/
09_GISOS/
  mapping_agent/
  spatial_analysis_agent/
  site_selection_agent/
  evidence_mapping_agent/
10_SCENARIOOS/
  baseline_scenarios/
  future_scenarios/
  policy_scenarios/
  risk_scenarios/
11_VALIDATIONOS/
  evidence_review/
  assumption_tracking/
  uncertainty_analysis/
  verification_workflows/
12_GOVERNANCEOS/
  policy_layer/
  decision_layer/
  stakeholder_layer/
  audit_layer/
13_BUSINESS_LAYER/
  REVENUE_MODEL.md
  PARTNERSHIP_MODEL.md
  OPEN_SOURCE_POLICY.md
  MARKETPLACE_VISION.md
14_DEMONSTRATIONS/
  batlow_energy_hub/
  shanghai_carbon_control/
  datong_zero_carbon_park/
  climate_scorecard/
15_DOCUMENTATION/
  architecture/
  concepts/
  policies/
  tutorials/
  case_studies/
```

Every listed directory contains a README describing its intended purpose,
future scope, example future agents or responsibilities, and current status.

## System Descriptions

| Directory | Role |
| --- | --- |
| `00_PROJECT_CONTROL/` | Roadmap, task index, Codex queue, rules, agent template, and architecture decisions |
| `01_CLIMATEOS_CORE/` | Shared runtime, evidence, validation, governance, ontology, and interface contracts |
| `02_CARBONOS/` | Documented foundation for green-power evidence, carbon accounting, budgets, verification, and product carbon passports; no calculations or operational agents yet |
| `03_ENERGYOS/` | Renewable energy, storage, grid, and energy scenario agents |
| `04_WATEROS/` | Water balance, watershed, flood resilience, and water-quality agents |
| `05_LANDOS/` | Land use, soil health, desertification, and restoration agents |
| `06_BIODIVERSITYOS/` | Species, habitat, corridor, and ecosystem-health agents |
| `07_PARKOS/` | Zero-carbon park, industrial park, and infrastructure agents |
| `08_ESGOS/` | Disclosure, audit-support, scorecard, and materiality agents |
| `09_GISOS/` | Governed mapping and spatial evidence interfaces; no GIS runtime yet |
| `10_SCENARIOOS/` | Baseline, future, policy, and risk scenario records |
| `11_VALIDATIONOS/` | Evidence review, assumptions, uncertainty, and verification workflows |
| `12_GOVERNANCEOS/` | Policy, human decision, stakeholder, and audit layers |
| `13_BUSINESS_LAYER/` | Planning-only revenue, partnership, open-source, and marketplace concepts |
| `14_DEMONSTRATIONS/` | Bounded multi-system demonstration cases |
| `15_DOCUMENTATION/` | Architecture, concepts, policies, tutorials, and case studies |

## Subsystem Relationships

```text
Project Control
  -> defines tasks, rules, templates, and architecture decisions

ClimateOS Core
  -> provides shared Scenario, Evidence, Hypothesis, Review, and Report concepts

CarbonOS / EnergyOS / WaterOS / LandOS / BiodiversityOS / ParkOS / ESGOS
  -> provide domain-specific agent families

GISOS
  -> may provide governed spatial evidence interfaces after future approval

ScenarioOS
  -> organises bounded scenarios and assumptions

ValidationOS
  -> organises evidence, uncertainty, and verification review

GovernanceOS
  -> records policy, stakeholder, audit, and human decision boundaries

Business Layer
  -> documents operating concepts without transactions

Demonstrations
  -> combine reviewed subsystem outputs in bounded examples

Documentation
  -> explains the architecture and its limits to users and contributors
```

Subsystem agents should reuse ClimateOS Core conventions rather than creating
parallel evidence, validation, or governance architectures.

## CarbonOS Foundation

CarbonOS is the first subsystem with a documented foundation. Its
`02_CARBONOS/` documents define scope, conceptual layers, data entities,
workflow, governance, an official planned-agent catalog, and a phased roadmap.
The existing agent directories remain extension points for later approved
tasks.

`Foundation Established` is a documentation status. It does not mean CarbonOS
has implemented carbon calculations, external data connections, automated
decisions, professional verification, certification, or operational agents.

## Compatibility Note

An earlier local repository-control scaffold created placeholder directories
such as `04_PARKOS/`, `05_ESGOS/`, `06_GISOS/`, `07_DEMOS/`, and `08_DOCS/`.
They are retained to comply with the rule against deleting or renaming existing
folders. The numbered structure in this document is the Task47 master
directory scaffold for future work. A later explicitly approved migration task
may reconcile legacy placeholders after review.
