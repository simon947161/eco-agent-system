# CCZPS-Lite â€” Batlow Runtime Demonstrator

## Minimum Human–AI Scientist Runtime (Task2000 checkpoint)

The repository includes a dependency-free, localhost-only supervised Runtime
demonstration under `cczps_lite/scientist_runtime/`. It uses one fixed,
repository-authored fictional scalar fixture to exercise:

`question -> structured hypothesis -> human approval -> local run -> receipt -> quarantined passport -> human review`

Start it from the repository root:

```bash
python run_scientist_runtime.py
```

Then open `http://127.0.0.1:8765`. Runtime state is written beneath the ignored
`runtime_data/` directory. The demonstration makes no environmental or regional
claim, uses no external service, and cannot execute arbitrary code.

CCZPS-Lite is a small, file-based demonstrator for comparing possible environmental resilience pathways. It supports evidence, runtime interpretation, reasoning, governance review, and pre-execution resource guards.

## How to Run

```bash
python cczps_lite/engine/scenario_compare.py
python cczps_lite/engine/meteorology_runtime.py
python cczps_lite/engine/usage_cost_governance.py
python cczps_lite/engine/budget_guard.py
python cczps_lite/engine/planning_hypothesis.py
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

Successful live or cached readings are also appended to the versioned
`output/meteorology_timeseries.json` store. The unique key is scenario,
location, and observation date. Repeated refreshes do not create duplicates,
and observations are ordered by date, scenario, then location. Blocked,
missing-data, failed, and scaffold records are not added.

The runtime also writes `output/meteorology_trends.json` and
`output/meteorology_trends.md` from the local time-series store. Trend readings
require at least three successful observations for the same scenario and
location, compare the earliest and latest stored non-missing values, and report
only conservative evidence signals. They do not forecast, predict, recommend,
or change scenario scores.

The live fetcher uses the public NASA POWER endpoint without authentication or API keys. It does not add OpenAI, NOAA, ERA5, BOM, GIS, satellite, paid-service, database, cloud-storage, or scheduled-refresh integrations.

## Manual Meteorology Refresh Workflow

Open the repository's **Actions** tab, select **Manual Meteorology Refresh**, and choose **Run workflow**. The workflow is manual only and has no schedule or cron trigger.

- `observation_dates` accepts a comma-separated list of NASA POWER dates in `YYYYMMDD` format.
- Range mode uses `start_date`, `end_date`, and a positive `interval_days` value when `observation_dates` is blank.
- `manual_approval` must be explicitly true before a live batch starts.
- `force_refresh` bypasses an existing location/date cache entry, but it does not bypass Budget Guard.
- `commit_outputs` commits the allowlisted meteorology output files to the selected branch. Empty commits are skipped.

When `commit_outputs` is false, download the `meteorology-refresh-output` artifact from the completed workflow run. It contains `meteorology_evidence.json`, `meteorology_cache.json`, `meteorology_timeseries.json`, `meteorology_trends.json`, and `meteorology_trends.md`.

The workflow runs the complete unit test suite after refresh. Blocked requests and NASA `missing_data` responses remain valid transparent outputs; technical errors and test failures fail the workflow.

### Safe Commit Verification

To validate repository updates:

1. Run **Manual Meteorology Refresh** on a review branch first.
2. Set `manual_approval=true`, choose a historical date list or range, and set `commit_outputs=true`.
3. Confirm the workflow stages only the five allowlisted meteorology output files.
4. Confirm the bot commit uses `Refresh batch meteorology evidence`.
5. Repeat on `main` only after reviewing the branch result.

The workflow rejects non-branch refs, refuses unexpected staged files, and skips the commit when no meteorology output changed. Branch protection can still prevent a direct push; in that case, report the blocked workflow rather than weakening repository protections.

## Planning Hypothesis Runtime

A planning hypothesis is a testable assumption connecting observed conditions, an identified problem, possible intervention logic, an expected effect, validation indicators, and explicit failure conditions. It is not a final recommendation, design, engineering solution, or planning approval.

Generate the local hypothesis outputs with:

```bash
python cczps_lite/engine/planning_hypothesis.py
```

The runtime reads existing local scenario, validation, meteorology trend, and spatial transect records. It makes no live API, GIS, simulation, or language model call. Outputs are written to `output/planning_hypotheses.json` and `output/planning_hypotheses.md` for Batlow, Kunlun, Iraq, and the Baiyangdian-Xiong'an watershed context.

Statuses are deliberately conservative: `concept_level`, `evidence_supported`, `requires_validation`, `not_supported`, and `insufficient_evidence`. Every generated hypothesis defaults to human review because evidence support at concept level does not replace field validation, professional planning review, engineering assessment, community consultation, or statutory processes.

Generated output behaviour:

- `meteorology_evidence.json` is the latest generated reading set.
- `meteorology_cache.json` stores successful location/date readings.
- `meteorology_timeseries.json` persistently appends successful observations without duplicates.
- `meteorology_trends.json` and `meteorology_trends.md` store conservative trend readings.
- `planning_hypotheses.json` and `planning_hypotheses.md` store testable concept-level assumptions and their validation boundaries.

## Methodology Boundary

This prototype is not a final environmental model, regulatory-grade planning tool, financial assessment, or scientific simulation. Human review and site-specific validation remain required.
