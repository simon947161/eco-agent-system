# CCZPS-Lite Demonstration Dashboard

## What It Is

The CCZPS-Lite Demonstration Dashboard is a static presentation layer for the existing generated scenario outputs. It compares Batlow, Kunlun, Iraq, and Baiyangdian-Xiong'an and exposes the current evidence, differential, forcing, validation, review, adaptive response, prioritisation, and system-validation readings.

The dashboard adds no runtime logic. It does not recalculate scores, forecast conditions, or make decisions.

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

On every push to `main`, GitHub Actions:

1. checks out the repository;
2. refreshes the existing generated scenario outputs;
3. stages `cczps_lite/dashboard/` as the website root;
4. copies the comparison matrix, system validation report, and runtime capability map into the site's local `data/` directory;
5. uploads the static Pages artifact; and
6. deploys it with the official GitHub Pages action.

The workflow does not commit generated files and does not run an application server.

## GitHub Pages

After the deployment workflow is enabled for GitHub Pages and a commit reaches `main`, the expected project-site address is:

`https://simon947161.github.io/eco-agent-system/`

The exact deployment URL is also recorded by the `github-pages` environment in the workflow run.

## What It Can Show

- four headline scenario contexts;
- side-by-side validation, priority, risk, and readiness fields;
- outputs from every current runtime stage;
- selectable scenario details;
- the three Baiyangdian-Xiong'an watershed validation points;
- the system validation report; and
- the runtime capability map.

## What It Cannot Do Yet

- edit or submit scenario inputs;
- run the CCZPS-Lite engine in the browser;
- provide live environmental data;
- use GIS, forecasting, machine learning, or external services;
- create review tasks or approval workflows;
- replace local evidence, professional judgement, community consultation, or regulatory review; or
- make autonomous decisions.

All displayed results remain indicative and concept-level.
