# CCZPS-Lite Codex Task Queue 23-30

## Queue Rules

Execute tasks in numerical order unless the repository owner explicitly reorders them. Follow `docs/CODEX_EXECUTION_PROTOCOL.md` for every task. Each task requires its own branch and Draft pull request.

## Task 23 - Commit Refreshed Meteorology Outputs Safely

### Purpose

Validate `commit_outputs=true` workflow behaviour and ensure refreshed meteorology outputs can safely update repository data and trigger dashboard deployment.

### Scope

- Review the manual meteorology refresh workflow's commit path.
- Verify branch targeting, permissions, bot identity, empty-change handling, and push behaviour.
- Confirm only `meteorology_evidence.json` and `meteorology_cache.json` are committed.
- Confirm a committed refresh can trigger the existing dashboard deployment.
- Add tests or workflow validation for commit-mode behaviour.
- Document a safe manual verification procedure.

### Safety Boundaries

- Keep refresh manual; add no schedule or cron.
- Do not bypass Usage & Cost Governance or Budget Guard.
- Do not commit unrelated generated files.
- Do not require a live request in unit tests.

### Verification

- Run `python -m unittest discover`.
- Verify the workflow avoids empty commits.
- Verify artifact mode still works when commit mode is false.

### Delivery

Provide the Draft PR URL, workflow behaviour tested, changed files, generated outputs, and test results.

## Task 24 - Dashboard Meteorology Evidence Panel

### Purpose

Improve dashboard presentation of meteorology evidence, including scenario, location, observation date, retrieval status, temperature, rainfall, humidity, wind, solar radiation, cache status, and Budget Guard status.

### Scope

- Improve the static meteorology evidence panel.
- Present missing values explicitly and accessibly.
- Distinguish success, cache, blocked, missing-data, and retrieval-failure states.
- Retain responsive, static-file behaviour.
- Update dashboard structural tests and documentation.

### Safety Boundaries

- Read local generated JSON only.
- Do not call NASA POWER or any external service from browser code.
- Do not add forecasts, predictions, scoring changes, or recommendations.

### Verification

- Run `python -m unittest discover`.
- Run JavaScript syntax validation when available.
- Verify no NASA POWER endpoint appears in dashboard scripts.

### Delivery

Provide the Draft PR URL, panel example, changed files, and test results.

## Task 25 - Time-Series Meteorology Store

### Purpose

Create a persistent `meteorology_timeseries.json` output so repeated manual refreshes append observations instead of only overwriting latest evidence.

### Scope

- Define a versioned time-series schema.
- Append successful observations by scenario, location, and observation date.
- Prevent duplicate location/date entries.
- Define deterministic update and ordering behaviour.
- Integrate the manual refresh workflow's commit and artifact paths.
- Preserve `meteorology_evidence.json` as the latest-reading output.
- Add migration or empty-file handling.

### Safety Boundaries

- Do not add a database, cloud storage, scheduler, or browser-side writes.
- Do not invent missing observations.
- Keep live requests behind governance and Budget Guard.

### Verification

- Test append, deduplication, ordering, missing data, and repeated refreshes.
- Run `python -m unittest discover`.

### Delivery

Document the schema, append behaviour, changed files, generated outputs, Draft PR URL, and test results.

## Task 26 - Meteorology Trend Reading

### Purpose

Add conservative rule-based trend readings using stored time-series data. No forecasting. No prediction. Only evidence trend signals.

### Scope

- Define minimum observation counts and comparable periods.
- Add deterministic trend classifications for supported variables.
- Represent insufficient data explicitly.
- Include observation window, sample count, and rule explanation.
- Integrate trend readings into local reports and dashboard output where appropriate.

### Safety Boundaries

- Do not forecast future weather or climate.
- Do not use machine learning, anomaly claims without explicit rules, or autonomous recommendations.
- Do not change scenario scores unless separately authorised.

### Verification

- Test increasing, decreasing, stable, missing, and insufficient-data cases.
- Run `python -m unittest discover`.

### Delivery

Provide rule examples, generated output fields, changed files, Draft PR URL, and test results.

## Task 27 - Spatial Context & Transect Runtime

### Purpose

Introduce a generic spatial transect framework allowing user-selected core locations to be interpreted through upstream, downstream, upwind, downwind, highland, lowland, and lateral reference points.

### Scope

- Define provider-agnostic transect configuration and output schemas.
- Support core and reference-point roles.
- Preserve coordinates, direction, distance, elevation context when supplied, source, confidence, and missing-data status.
- Add deterministic relationship validation.
- Produce local transect readings without GIS automation.

### Safety Boundaries

- Do not automatically select points.
- Do not call GIS, mapping, DEM, weather, or simulation services.
- Do not infer hydrology or wind direction when inputs are absent.
- Do not generate design or construction recommendations.

### Verification

- Test role validation, missing coordinates, duplicate points, direction labels, and scenario compatibility.
- Run `python -m unittest discover`.

### Delivery

Document schemas, example transect, limitations, changed files, Draft PR URL, and test results.

## Task 28 - Transect Scenario Pack

### Purpose

Apply Spatial Context & Transect Runtime to Batlow, Kunlun, Iraq, and Baiyangdian-Xiong'an as configured scenario examples.

### Scope

- Add transparent local transect fixtures for all four scenario contexts.
- Include upstream, downstream, upwind, downwind, highland, lowland, or lateral points only when supported by declared configuration.
- Add scenario reports and dashboard-compatible local outputs.
- Clearly label illustrative or unvalidated reference points.

### Safety Boundaries

- Do not claim field validation.
- Do not make live GIS calls or automate point selection.
- Do not produce environmental, engineering, or planning conclusions.

### Verification

- Test scenario coverage, schema validity, role consistency, and missing-data handling.
- Run `python -m unittest discover`.

### Delivery

Provide scenario examples, changed files, generated outputs, Draft PR URL, and test results.

## Task 29 - GIS-Assisted Reference Point Selector Planning

### Purpose

Create a planning document for future GIS-assisted point selection using Google Earth, DEM, watershed analysis, wind corridor data, ENVI-met, Fluent, and other spatial computation tools. No implementation yet.

### Scope

- Document candidate data sources and tools.
- Define a future user-controlled point-selection workflow.
- Describe provenance, licensing, confidence, coordinate, elevation, watershed, wind, and review requirements.
- Describe governance, Budget Guard, cache, and approval integration.
- Identify privacy, cost, reproducibility, and validation risks.
- Separate lightweight reference selection from simulation workflows.

### Safety Boundaries

- Planning document only.
- Do not add APIs, dependencies, credentials, GIS code, simulations, or browser integrations.
- Do not imply endorsement or availability of commercial tools.

### Verification

- Run `python -m unittest discover`.
- Verify only planning or documentation files changed.

### Delivery

Provide the planning document path, changed files, Draft PR URL, and test results.

## Task 30 - CCZPS-Lite v1.0 Demonstrator Report

### Purpose

Create a formal v1.0 demonstrator report summarising runtime chain, governance, Budget Guard, NASA POWER integration, manual refresh workflow, dashboard, scenario validation, transect logic, limitations, and next development roadmap.

### Scope

- Describe the complete runtime chain and evidence boundaries.
- Summarise Tasks 18-29 as implemented in the repository.
- Include governance, cost ownership, Budget Guard, NASA POWER, cache, manual workflow, dashboard, validation, and transect sections.
- State which sources are live, scaffolded, mocked, cached, or planned.
- Include reproducible commands, test status, limitations, and roadmap.
- Use only claims supported by repository implementation and evidence.

### Safety Boundaries

- Do not claim regulatory, scientific, financial, engineering, forecasting, or autonomous-decision readiness.
- Do not introduce runtime or dashboard features unless explicitly required to generate the report.
- Do not include credentials or confidential data.

### Verification

- Run `python -m unittest discover`.
- Verify links, commands, output paths, and implementation claims.
- Render or inspect the report format when applicable.

### Delivery

Provide the report path, changed files, Draft PR URL, test results, and a short list of documented limitations and next steps.
