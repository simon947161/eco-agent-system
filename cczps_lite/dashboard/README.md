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
- meteorology evidence from local generated or cached JSON;
- system validation and capability documentation.

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
