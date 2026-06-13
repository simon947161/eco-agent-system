# CCZPS-Lite Codex Task Queue 31-40

## Queue Rules

Execute tasks in numerical order unless the repository owner explicitly reorders them. Follow `docs/CODEX_EXECUTION_PROTOCOL.md` for every task. Each implementation task requires its own branch and Draft pull request.

---

# Task 31 — Batch Meteorology Refresh Workflow

## Status

Ready for implementation as the next task.

Do not implement Tasks 32-40 in this PR.

---

## Repository

Repository: `simon947161/eco-agent-system`

Base branch: `main`

Work branch: `task31-batch-meteorology-refresh-workflow`

---

## Objective

Extend the existing Manual Meteorology Refresh workflow to support multiple observation dates within a single GitHub Actions execution.

The purpose is to accelerate evidence accumulation for CCZPS-Lite while preserving all existing governance controls.

This task must not introduce uncontrolled API usage.

All meteorology retrievals must remain governed by:

- Usage & Cost Governance Runtime
- Budget Guard Runtime
- Manual Approval requirements
- Existing cache-first logic

---

## Background

Current workflow supports:

```text
Single Date
↓
NASA POWER Fetch
↓
Evidence Output
↓
Time-Series Update
↓
Dashboard
```

To build meaningful trend analysis and future validation capability, multiple historical observations must be collected efficiently.

The current workflow requires repeated manual execution.

Task 31 introduces controlled batch execution.

---

## Supported Input Modes

The implementation should support at least one of the following safe input patterns.

### Mode A — Explicit Date List

Example:

```text
20250501,20250508,20250515
```

Workflow input:

```yaml
observation_dates:
```

### Mode B — Date Range

Example:

```yaml
start_date: 20250501
end_date: 20250515
interval_days: 7
```

Generated dates:

```text
20250501
20250508
20250515
```

The selected input mode must produce a deterministic, validated, de-duplicated list of observation dates.

Invalid dates, malformed ranges, non-positive intervals, reversed ranges, and empty date lists must fail before any external request.

---

## Governance Requirements

The workflow must continue to require:

```yaml
manual_approval: true
```

No automatic approval.

No hidden execution.

Every requested date must be handled as its own governed activity.

No date may inherit another date's governance result.

---

## Budget Guard Requirements

Every date execution must pass through:

- Usage & Cost Governance Runtime
- Budget Guard Runtime

A batch request must never bypass governance checks.

If any individual date is blocked, the output must clearly preserve its date-specific status.

---

## Stop Conditions

If:

```text
stop_required
```

is returned by Budget Guard,

remaining dates must not execute unless the existing runtime explicitly supports safe date-specific continuation.

The preferred first implementation should terminate safely and clearly report the stop reason.

---

## Cache Requirements

Existing cache logic must remain active.

For each requested date:

```text
Cache Exists
↓
Use Cache
↓
No NASA Request
```

Only uncached dates may trigger retrieval.

A cache hit must still be recorded clearly in the output.

---

## Maximum Date Limit

Introduce a hard safety limit.

Default:

```text
max_dates_per_run = 10
```

If exceeded:

```text
workflow failure
```

with a clear explanation.

Purpose:

Prevent accidental mass retrieval.

Tests must verify acceptance at 10 dates and rejection above 10 dates.

---

## Output Requirements

### Time-Series Store

Append successful observations to:

```text
cczps_lite/output/meteorology_timeseries.json
```

Rules:

- No duplicates.
- No overwriting existing valid observations.
- Deterministic ordering must be preserved.

### Evidence Output

Update:

```text
cczps_lite/output/meteorology_evidence.json
```

with the latest retrieval set or clear batch output status.

### Cache

Update:

```text
cczps_lite/output/meteorology_cache.json
```

for successful readings.

### Trend Outputs

If the existing runtime regenerates trend outputs, include:

```text
cczps_lite/output/meteorology_trends.json
cczps_lite/output/meteorology_trends.md
```

without changing their trend logic.

---

## Commit Behaviour

Support existing option:

```yaml
commit_outputs
```

### commit_outputs = true

Commit only approved output files:

```text
cczps_lite/output/meteorology_evidence.json
cczps_lite/output/meteorology_timeseries.json
cczps_lite/output/meteorology_cache.json
cczps_lite/output/meteorology_trends.json
cczps_lite/output/meteorology_trends.md
```

Reject unexpected staged files before committing.

Skip commit when there are no allowed output changes.

Preserve safe branch targeting, commit identity, and existing push behavior.

### commit_outputs = false

Do not commit.

Upload outputs as workflow artifacts only.

Artifact output must include all meteorology output files needed to inspect the batch result.

---

## Dashboard Compatibility

Existing dashboard must continue to function.

No dashboard redesign is required.

The trend runtime should automatically benefit from larger time-series datasets.

Dashboard must continue reading local generated files only.

No browser-side API call is allowed.

---

## Partial Failure Behaviour

The batch output must distinguish between:

- success
- from_cache
- blocked_by_budget_guard
- missing_data
- retrieval_failed
- invalid_date
- not_retrieved

Do not invent observations.

Do not convert failed or missing records into successful evidence.

---

## Safety Constraints

Do NOT implement:

- cron schedules
- automatic daily collection
- unattended recurring execution
- browser-side API calls
- unlimited retrieval loops
- bypass of Budget Guard
- bypass of Manual Approval
- forecasts
- simulations
- autonomous recommendations
- credentials
- billing
- payment logic
- unrelated APIs

---

## Testing

Add or update tests covering the following.

### Date Parsing

- explicit date list
- date range generation if implemented
- interval handling if implemented
- duplicate removal
- deterministic ordering
- invalid date handling
- empty input handling
- malformed range handling where applicable

### Governance

- manual approval requirement
- Usage & Cost Governance remains in the path
- Budget Guard remains in the path
- no date bypasses governance
- stop_required handling

### Limits

- maximum date count
- acceptance at 10 dates
- rejection above 10 dates

### Cache

- cache hit
- cache miss
- cache prevents repeated NASA request

### Output Integrity

- duplicate prevention in `meteorology_timeseries.json`
- artifact generation when `commit_outputs=false`
- commit allowlist when `commit_outputs=true`
- rejection of unexpected staged files
- empty-change behavior
- partial failure status preservation

### Workflow Safety

- `workflow_dispatch` exists
- no `schedule` trigger
- no browser-side live API call
- no new external service dependency

All existing tests must continue to pass.

---

## Commands

Run:

```bash
python -m unittest discover
```

If relevant:

```bash
python cczps_lite/engine/meteorology_runtime.py
```

Do not require live NASA POWER calls in CI.

Unit and workflow tests must not make live external requests.

---

## Delivery

Create Draft Pull Request.

Provide:

- PR URL
- selected input pattern
- maximum date count
- per-date governance behavior
- cache behavior
- artifact behavior
- commit behavior
- explicit output allowlist
- changed files summary
- test results

Do not merge automatically.
