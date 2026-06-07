# CCZPS-Lite Demonstration Dashboard

## What It Is

The CCZPS-Lite Demonstration Dashboard is a static presentation layer for the existing generated scenario outputs. It compares Batlow, Kunlun, Iraq, and Baiyangdian-Xiong'an and exposes the current evidence, differential, forcing, validation, review, adaptive response, prioritisation, and system-validation readings.

The dashboard adds no runtime logic. It does not recalculate scores, forecast conditions, or make decisions. Meteorology views read local generated output files and never call NASA POWER directly.

## Open Locally

1. Refresh the generated outputs from the repository root:

   ```text
   python cczps_lite/engine/scenario_compare.py
   ```

2. Stage or serve the dashboard with its local data files. The GitHub Pages workflow shows the exact copy layout used for deployment.
3. Open `index.html` through any static file server.

No application backend, Node process, npm build, database, or external API is required. Browsers commonly restrict `fetch` requests from direct `file://` pages, so a basic static server is recommended for local viewing.

## Deployment

The dashboard is deployed through `.github/workflows/deploy-dashboard-pages.yml`.

On every push to `main`, GitHub Actions checks out the repository, refreshes generated outputs in safe local mode, stages the static dashboard and local data, uploads the Pages artifact, and deploys it. The workflow does not commit generated files or run an application server.

## GitHub Pages

The expected project-site address is `https://simon947161.github.io/eco-agent-system/`. The exact deployment URL is recorded by the `github-pages` environment.

## What It Can Show

- headline scenario contexts;
- validation, priority, risk, and readiness fields;
- outputs from current runtime stages;
- selectable scenario details;
- meteorology evidence cards for each configured scenario, including location,
  observation date, retrieval state, temperature, rainfall, relative humidity,
  wind speed and direction, solar radiation, cache state, confidence, and
  Budget Guard status;
- system validation and capability documentation.

## Meteorology Evidence Panel

The panel reads only `cczps_lite/output/meteorology_evidence.json`, produced by
`python cczps_lite/engine/meteorology_runtime.py` or the manual meteorology
refresh workflow. The latest evidence file is overwritten by each runtime
execution and can be committed explicitly or distributed as a workflow
artifact.

Values may be live NASA POWER observations, cached successful observations, or
local scaffold records. Missing observations are shown as **Not available**;
the dashboard does not invent values. Retrieval states distinguish successful,
cached, Budget Guard blocked, missing-data, failed, and not-retrieved records.
Budget Guard status and summaries are displayed when present in the generated
record.

The browser reads this local JSON file only. It does not initiate retrieval,
write cache data, or call NASA POWER or another external service.

## What It Cannot Do Yet

- edit or submit scenario inputs;
- run the CCZPS-Lite engine in the browser;
- initiate live environmental data requests;
- call NASA POWER directly;
- use GIS, forecasting, machine learning, or other external services;
- create review tasks or approval workflows;
- replace professional judgement or regulatory review;
- make autonomous decisions.

All displayed results remain indicative and concept-level.
