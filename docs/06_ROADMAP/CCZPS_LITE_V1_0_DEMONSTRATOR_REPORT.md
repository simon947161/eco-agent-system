# CCZPS-Lite v1.0 Demonstrator Report

## Executive Summary

CCZPS-Lite v1.0 is a transparent, file-based environmental governance demonstrator. It combines configured scenario reasoning, evidence metadata, concept-level validation, human review routing, resource governance, Budget Guard controls, optional NASA POWER observations, local meteorology storage and trends, dashboard presentation, and configured spatial transects.

The demonstrator is not a regulatory, scientific, financial, engineering, forecasting, construction, or autonomous-decision system. Its outputs are evidence and governance readings for human review.

## Demonstrator Boundaries

CCZPS-Lite v1.0:

- uses deterministic Python rules and local JSON configuration;
- exposes evidence strength, uncertainty, validation gaps, review needs, and governance fields;
- permits an explicit, manually approved NASA POWER request path;
- stores successful observations in local cache and time-series files;
- produces conservative trend signals without forecasting;
- presents local generated outputs in a static dashboard;
- supports configured spatial transect roles without automatic GIS inference;
- keeps external resource ownership and cost responsibility visible.

CCZPS-Lite v1.0 does not:

- forecast weather, climate, hydrology, ecology, fire, or project outcomes;
- use machine learning for prediction or autonomous decisions;
- provide regulatory, scientific, engineering, financial, design, or construction approval;
- automatically select GIS reference points;
- make browser-side external API calls;
- perform billing, payments, invoicing, subscriptions, crypto, token, or marketplace functions;
- silently consume paid or external resources.

## Runtime Chain

The scenario runtime is orchestrated by `cczps_lite/engine/scenario_compare.py`.

The implemented chain is:

1. Scenario inputs and local evidence profiles.
2. Runtime field derivation and rule-based scenario scoring.
3. Differential Field Runtime.
4. Forcing Layer Runtime.
5. Evidence Layer.
6. Validation Layer.
7. Review Loop Runtime.
8. Adaptive Response Runtime.
9. Response Prioritisation Runtime.
10. Usage & Cost Governance Runtime.
11. Budget Guard Runtime.
12. Meteorology evidence, cache, time-series, and trend outputs.
13. Spatial Context & Transect Runtime and scenario pack.
14. Static dashboard and Markdown/CSV/JSON reports.

The forcing, validation, response, and prioritisation outputs remain candidate concept-level readings. They require human review and local checking.

## Evidence And Validation

The Evidence Layer converts local scenario records and meteorology readings into transparent evidence fields. Meteorology is supporting evidence only and does not directly change scenario scores.

The Validation Layer combines runtime, differential, forcing, and evidence fields; generates a concept-level validation score and status; lists validation gaps; preserves requirements for local, technical, and human review; and does not claim scientific validation.

The Review Loop routes scenarios toward evidence collection, technical review, local review, or concept review. The Adaptive Response and Response Prioritisation runtimes produce candidate review options and ordering, not final implementation instructions.

## Environmental Planning Workflow Alignment

Task 29.5, the Environmental Planning Workflow Alignment Review, assesses CCZPS-Lite v1.0 against ten stages of a mature environmental planning and design workflow. The full review is recorded in `docs/07_VALIDATION/ENVIRONMENTAL_PLANNING_WORKFLOW_ALIGNMENT_REVIEW.md`.

### Covered At Concept Or Demonstrator Level

- Problem identification is covered at concept level through the Differential Field Runtime, Forcing Layer Runtime, Evidence Layer, and Validation Layer.
- Scenario or intervention concept generation is covered at concept level through the Scenario Pack, Adaptive Response Runtime, Response Prioritisation Runtime, dashboard, and reports.
- Supporting demonstrator capabilities also cover transparent evidence structuring, review routing, Usage & Cost Governance, Budget Guard control, local generated reports, and dashboard presentation.

These capabilities identify candidate environmental signals and response concepts. They do not establish professionally verified diagnoses, approved interventions, or implementation instructions.

### Partially Covered

- Geographic context review.
- Regional and site background analysis.
- Climate and environmental condition analysis.
- Terrain, watershed, wind, elevation, and spatial-pattern analysis.
- Planning hypothesis or design assumption formation.
- Fit assessment between hypotheses and evidence.
- Iterative refinement and re-validation.

These stages have useful configured inputs, meteorology evidence, spatial transects, validation fields, reports, and review-loop support. They remain partial because the system does not yet provide comprehensive site data acquisition, professional GIS and spatial analysis, explicit versioned planning hypotheses, formal fit criteria, persistent iteration history, multidisciplinary review, or professional sign-off.

### Not Yet Covered

- Professional simulation and tool-based validation is not implemented.
- There is no dedicated Planning Hypothesis Runtime.
- There is no Simulation Validation Interface.
- There are no live GIS, DEM, watershed, wind-corridor, ENVI-met, Fluent, or CFD connector pathways.
- There is no dedicated Iteration and Fit Assessment Runtime or formal professional approval workflow.

### Demonstrator Suitability And Professional Boundaries

CCZPS-Lite v1.0 is suitable as a demonstrator because it presents a coherent and transparent chain for configured case exploration, evidence structuring, rule-based environmental signals, uncertainty and gap disclosure, review routing, guarded observation retrieval, resource and cost governance, dashboard communication, and configured spatial context. It is useful for demonstrating how these workflow layers may connect while keeping assumptions, provenance, missing data, guard decisions, and human review needs visible.

It is not yet a final professional planning approval, engineering, or simulation system. It lacks comprehensive and professionally validated site evidence; regulatory and standards-based assessment; implemented GIS, DEM, watershed, wind, microclimate, and CFD analysis; explicit hypothesis and iteration lifecycle management; calibrated model execution; field validation; multidisciplinary expert review; community and stakeholder approval processes; and auditable professional sign-off. Its outputs remain concept-level evidence and governance readings for qualified human review.

## Tasks 18-29.5 Implementation Summary

### Task 18: Meteorology Connector Scaffold

Task 18 introduced source definitions, parsing structures, scenario compatibility, and meteorology evidence fields. It was clarified as a connector scaffold rather than live retrieval.

Source definitions exist for BOM, NASA POWER, NOAA Climate Data Online, and ERA5.

### Task 19: Usage & Cost Governance Runtime

Task 19 introduced idea, research, project, agent, and enterprise usage modes; external resource ownership and cost-bearer visibility; estimated external resource cost classifications; platform service and fee classifications; budget warnings and approval classifications; agentic consumption risk; and governance summaries.

The core ownership principle is that external resource costs belong to the resource consumer. The platform does not silently assume external API or compute costs.

### Task 20: Budget Guard Runtime

Budget Guard classifies declared resource requests as `within_budget`, `warning`, `approval_required`, or `stop_required`.

It evaluates configured call, cost, and agent-run limits before live resource use. A `stop_required` result blocks the external call. Manual approval does not override hard stop conditions.

### Task 21: NASA POWER Live Fetcher

NASA POWER is the only implemented live meteorology retrieval path. It uses the public NASA POWER Daily Point API and requires an explicit `--live` command.

Unit tests use injected fixtures and do not make live NASA POWER requests.

### Task 22: Manual Meteorology Refresh Workflow

The GitHub Actions workflow `.github/workflows/manual-meteorology-refresh.yml` uses manual `workflow_dispatch` only; accepts observation date, manual approval, force refresh, and commit-output inputs; runs the NASA POWER runtime explicitly; runs the full unit test suite; and commits only allowed meteorology outputs or uploads them as an artifact.

There is no scheduled or autonomous refresh trigger.

### Task 23: Safe Refreshed-Output Commit Workflow

The manual workflow validates the branch target, stages an allowlisted set of meteorology files, rejects unexpected staged files, skips empty commits, and pushes only when `commit_outputs=true`.

### Task 24: Dashboard Meteorology Evidence Panel

The static dashboard displays local meteorology evidence fields, including scenario, location, observation date, temperature, rainfall, humidity, wind, solar radiation, retrieval status, cache state, confidence, and Budget Guard state.

Dashboard JavaScript reads repository-generated local files. It does not call NASA POWER directly.

### Task 25: Time-Series Meteorology Store

Successful live or cached observations may be stored in `cczps_lite/output/meteorology_timeseries.json`. The store uses scenario, location, and observation date as its unique key, appends successful observations, avoids duplicates, and excludes blocked, failed, scaffold, and missing-data records.

### Task 26: Meteorology Trend Reading

The runtime generates `cczps_lite/output/meteorology_trends.json` and `cczps_lite/output/meteorology_trends.md`.

Trend readings require at least three successful observations for the same scenario and location. They compare earliest and latest stored non-missing values and classify conservative evidence signals such as increasing, decreasing, stable, insufficient data, or missing data.

These readings are not forecasts, predictions, recommendations, or automated scoring changes.

### Task 27: Spatial Context & Transect Runtime

The generic runtime supports configured core, upstream, downstream, upwind, downwind, highland, lowland, and lateral points.

It preserves supplied coordinates, direction, distance, elevation context, source, confidence, and missing-data status. It does not automatically select points or infer watershed and wind relationships when inputs are absent.

### Task 28: Transect Scenario Pack

The configured scenario pack covers Batlow, Kunlun, Iraq, and Baiyangdian-Xiong'an.

Reference points are explicitly labelled as configured, illustrative, user-defined, unvalidated, or missing-data records. The scenario pack does not claim field validation.

### Task 29: GIS-Assisted Selector Planning

Task 29 defines future required spatial-intelligence capabilities, including Google Earth and mapping review; DEM and watershed analysis; upstream/downstream suggestions; prevailing-wind and wind-corridor suggestions; highland/lowland/lateral suggestions; local, regional, and 1000 km+ context; ENVI-met microclimate assessment; Fluent or CFD-style wind and turbulence assessment; and other appropriate spatial computation tools.

No live GIS or model automation is implemented in v1.0. Future external calls must use Usage & Cost Governance, Budget Guard, and explicit user approval.

### Task 29.5: Environmental Planning Workflow Alignment Review

Task 29.5 compares the implemented demonstrator with a mature environmental planning workflow. It identifies concept-level coverage in problem identification and scenario generation; partial coverage across geographic, background, climate, spatial, hypothesis, fit, and iteration stages; and missing professional simulation, dedicated hypothesis management, formal fit assessment, and expert approval layers.

The detailed assessment and readiness judgement are documented in `docs/07_VALIDATION/ENVIRONMENTAL_PLANNING_WORKFLOW_ALIGNMENT_REVIEW.md`.

## Meteorology Source Status

| Source | Current status | Live retrieval | Test data | Internet required |
| --- | --- | --- | --- | --- |
| NASA POWER | Implemented optional live connector | Yes, only with explicit live execution and guard approval | Injected fixtures in unit tests | Only for live uncached retrieval |
| NOAA Climate Data Online | Source definition and field mapping | No | No live unit-test request | No for current scaffold |
| ERA5 | Reference source definition and field mapping | No | No live unit-test request | No for current scaffold |
| BOM | Source definition and field mapping | No | No live unit-test request | No for current scaffold |

The default meteorology command does not retrieve live data.

## NASA POWER Execution And Safety

Example live command:

```bash
python cczps_lite/engine/meteorology_runtime.py --live --date 20250501 --manual-approval
```

Optional cache bypass:

```bash
python cczps_lite/engine/meteorology_runtime.py --live --date 20250501 --manual-approval --force-refresh
```

Behavior:

- without `--live`, the runtime produces transparent scaffold readings and makes no network request;
- without required approval, guarded requests are recorded as `blocked_by_budget_guard`;
- if Budget Guard returns `stop_required`, NASA POWER is not called;
- successful cached data is reused for the same scenario/location/date unless `--force-refresh` is supplied;
- `--force-refresh` bypasses cache reuse but does not bypass Budget Guard or approval;
- successful live or cached observations may update the time-series store;
- technical failures remain visible rather than being replaced with invented observations.

## Cache And Generated Meteorology Outputs

| Output | Producer | Behavior |
| --- | --- | --- |
| `cczps_lite/output/meteorology_evidence.json` | Meteorology runtime | Overwrites the latest evidence set |
| `cczps_lite/output/meteorology_cache.json` | Successful live runtime | Stores reusable successful readings |
| `cczps_lite/output/meteorology_timeseries.json` | Successful live/cached runtime | Appends unique successful observations |
| `cczps_lite/output/meteorology_trends.json` | Meteorology runtime | Overwrites deterministic trend readings |
| `cczps_lite/output/meteorology_trends.md` | Meteorology runtime | Overwrites the human-readable trend report |

The manual workflow can commit these files only when `commit_outputs=true`; otherwise, it uploads them in the `meteorology-refresh-output` artifact.

## Usage, Cost, And Approval Governance

The Usage & Cost Governance Runtime exposes usage mode, external resource owner, external cost bearer, platform service recipient, estimated cost level, estimated external resource cost, platform service model, platform service fee model and estimate, budget warning, user approval requirement, agentic risk and consumption risk, and governance summary.

The runtime classifies governance. It does not bill, invoice, collect payment, create subscriptions, or execute resource purchases.

## Budget Guard

Budget Guard is a pre-execution control for live or potentially expensive resource use. It considers monthly qualitative budget limit, daily call limit, agent-run limit, estimated calls, estimated external cost, agentic consumption risk, and manual confirmation requirements.

Live spatial, AI, satellite, GIS, sensor, or model connectors should reuse this guard in future versions.

## Dashboard

The dashboard is a static HTML/CSS/JavaScript interface backed by local generated files.

It displays scenario comparison, runtime chain and scenario detail, Usage & Cost Governance readings, Budget Guard readings, meteorology evidence, meteorology trend readings, and validation and capability documentation.

The dashboard does not initiate NASA POWER, NOAA, ERA5, BOM, GIS, satellite, AI, or simulation requests from the browser. The GitHub Pages workflow stages local files into the deployed site.

## Scenario Validation

The scenario comparison and validation pipeline generates:

- `cczps_lite/output/comparison_matrix.csv`;
- `cczps_lite/output/scenario_report.md`;
- `cczps_lite/output/governance_summary.md`;
- `cczps_lite/output/scenario_validation_pack.md`;
- `docs/CCZPS_LITE_SYSTEM_VALIDATION_REPORT.md`;
- `cczps_lite/output/runtime_capability_map.md`.

These reports support concept review. They do not prove field performance or remove the need for local data, professional review, community consultation, and site-specific validation.

## Spatial Transect Outputs

| Output | Purpose |
| --- | --- |
| `cczps_lite/output/spatial_transects.json` | Structured configured transect readings |
| `cczps_lite/output/spatial_transects.md` | Human-readable transect summary |
| `cczps_lite/output/spatial_transect_scenario_pack.json` | Dashboard-compatible four-scenario pack |
| `cczps_lite/output/spatial_transect_scenario_pack.md` | Human-readable scenario pack report |

Current spatial outputs are local configured fixtures. They are not live GIS results, DEM-derived results, watershed-model results, wind-corridor results, ENVI-met results, Fluent results, or field-validated points.

## Reproducible Commands

```bash
python cczps_lite/engine/scenario_compare.py
python cczps_lite/engine/meteorology_runtime.py
python cczps_lite/engine/usage_cost_governance.py
python cczps_lite/engine/budget_guard.py
python cczps_lite/engine/spatial_transect_runtime.py
python -m unittest discover
```

## Test Status

At Task 30 preparation, the local regression suite completed successfully with 113 tests.

The tests cover the core scenario runtimes, evidence and validation layers, governance, Budget Guard, meteorology parsing and guarded live-fetch behavior, manual workflow scope, cache/time-series/trend behavior, dashboard boundaries, transect validation, and scenario-pack compatibility.

Live NASA POWER requests are not performed by unit tests.

## Limitations

The v1.0 demonstrator has the following material limitations:

- scenario scoring is concept-level and based on local configured rules;
- evidence quality depends on supplied records and is not externally verified by default;
- NASA POWER is the only live observation connector;
- NOAA, ERA5, and BOM remain source definitions;
- meteorology trend logic is simple earliest-to-latest comparison, not statistical climate analysis;
- cache and time-series storage are local JSON files, not a production data platform;
- dashboard outputs are read-only;
- transect points are configured fixtures, not automatically derived spatial intelligence;
- GIS, DEM, watershed, wind corridor, ENVI-met, Fluent/CFD, satellite, sensor, and AI integrations remain future work;
- field validation, professional judgement, local consultation, and governance review remain necessary.

## Next Development Roadmap

1. Review and stabilize the v1.0 schemas and generated-output contracts.
2. Add provider-agnostic local fixtures for future DEM, watershed, wind, and mapping connectors.
3. Add governance and Budget Guard preflight schemas for future spatial connectors.
4. Pilot selected live connectors behind explicit user approval, caching, provenance, and cost controls.
5. Add user-reviewed GIS-assisted reference point suggestions.
6. Separate lightweight spatial suggestion workflows from microclimate and CFD simulation workflows.
7. Add reproducibility, licensing, source-audit, and validation reports.
8. Continue strengthening dashboard visibility without browser-side external calls.

## Conclusion

CCZPS-Lite v1.0 demonstrates a transition from reasoning-only environmental scenarios toward observation-supported, resource-governed, spatially structured evidence workflows.

Its value is transparency: inputs, rules, evidence status, resource ownership, guard decisions, missing data, and limitations remain visible. The demonstrator is ready for review and further controlled development, not deployment as an autonomous or authoritative decision system.
