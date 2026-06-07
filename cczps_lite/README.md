# CCZPS-Lite â€” Batlow Runtime Demonstrator

CCZPS-Lite is a small, file-based demonstrator for comparing possible environmental resilience pathways. It supports evidence, runtime interpretation, reasoning, governance review, and pre-execution resource guards.

## How to Run

```bash
python cczps_lite/engine/scenario_compare.py
python cczps_lite/engine/meteorology_runtime.py
python cczps_lite/engine/usage_cost_governance.py
python cczps_lite/engine/budget_guard.py
```

The default meteorology command is safe scaffold mode and makes no network request.

## Input Files

- `input/location_profile.json` describes the Batlow location profile.
- `input/scenario_options.json` describes indicative future pathways.
- `input/evidence_profile.json` describes the evidence layer.
- `input/meteorology_sources.json` defines documented public observation sources and field mappings.
- `input/meteorology_scenarios.json` defines safe scaffold requests.
- `input/meteorology_locations.json` defines coordinates for explicit NASA POWER live requests.
- `input/usage_cost_profiles.json` declares usage, ownership, automation, and service-model assumptions.
- `input/budget_profile.json` declares local qualitative budget and execution limits.

## Meteorology Connector Runtime

The default runtime remains a safe connector scaffold. Task 21 adds an explicit NASA POWER Daily Point API pathway only. NOAA, ERA5, and BOM remain source definitions only. There is no scheduled retrieval, authentication, browser-side transport, or autonomous refresh.

Running `meteorology_runtime.py` without `--live` creates local records with null observation values and `"retrieval_status": "not_retrieved"`. Unit tests use injected NASA POWER fixtures and do not make network calls.

Meteorology remains supporting evidence only. Missing values remain explicit, and observations do not change validation scores or produce conclusions.

## Usage & Cost Governance Runtime

The usage runtime identifies resource owners, external cost bearers, platform service recipients, qualitative cost, approval requirements, and agentic consumption risk. External resource costs belong to the resource consumer; the platform does not silently absorb API costs.

## Budget Guard Runtime

The guard classifies declared resource requests as `within_budget`, `approval_required`, `warning`, or `stop_required`. Hard call, cost, and agent-run limits cannot be overridden by manual approval.

## NASA POWER Live Fetcher

Live retrieval is explicit:

```bash
python cczps_lite/engine/meteorology_runtime.py --live --date 20260606 --manual-approval
```

Use `--force-refresh` only when a cached location/date reading should be replaced. Without the required governance confirmation, requests are recorded as `blocked_by_budget_guard` and NASA POWER is not called.

Successful readings are stored in `output/meteorology_cache.json`. Requests for the same location and date reuse that cache unless `--force-refresh` is provided. The dashboard reads local `meteorology_evidence.json` only and never calls NASA POWER from the browser.

The live fetcher uses the public NASA POWER endpoint without authentication or API keys. It does not add OpenAI, NOAA, ERA5, BOM, GIS, satellite, paid-service, database, cloud-storage, or scheduled-refresh integrations.

## Manual Meteorology Refresh Workflow

Open the repository's **Actions** tab, select **Manual Meteorology Refresh**, and choose **Run workflow**. The workflow is manual only and has no schedule or cron trigger.

- `observation_date` is the NASA POWER observation date in `YYYYMMDD` format.
- `manual_approval` adds the explicit approval required for a live request. When false, Budget Guard may emit `blocked_by_budget_guard` without calling NASA POWER.
- `force_refresh` bypasses an existing location/date cache entry, but it does not bypass Budget Guard.
- `commit_outputs` commits the evidence and cache JSON files to the selected branch. Empty commits are skipped.

When `commit_outputs` is false, download the `meteorology-refresh-output` artifact from the completed workflow run. It contains `meteorology_evidence.json` and `meteorology_cache.json`.

The workflow runs the complete unit test suite after refresh. Blocked requests and NASA `missing_data` responses remain valid transparent outputs; technical errors and test failures fail the workflow.

## Methodology Boundary

This prototype is not a final environmental model, regulatory-grade planning tool, financial assessment, or scientific simulation. Human review and site-specific validation remain required.
