# CCZPS-Lite Codex Task Queue 31-40

## Queue Rules

Execute tasks in numerical order unless the repository owner explicitly reorders them. Follow `docs/CODEX_EXECUTION_PROTOCOL.md` for every task. Each implementation task requires its own branch and Draft pull request.

## Task 31 - Batch Meteorology Refresh Workflow

### Status

Planning brief only. Do not implement Task 31 as part of the Task 30 / PR #23 documentation update.

### Purpose

Allow GitHub Actions Manual Meteorology Refresh to process multiple observation dates in one manually initiated workflow run while preserving Usage & Cost Governance, Budget Guard, explicit manual approval, cache-first behavior, and safe output commits.

### Safe Input Design

The implementation should select and document one of these input patterns:

Option 1:

```yaml
observation_dates: "20250501,20250508,20250515"
```

Option 2:

```yaml
start_date: "20250501"
end_date: "20250515"
interval_days: 7
```

The selected pattern must produce a deterministic, validated, de-duplicated list of observation dates. Invalid dates, malformed ranges, non-positive intervals, reversed ranges, and empty date lists must fail before any external request.

### Required Scope

- Extend the manual `workflow_dispatch` meteorology refresh path to accept a bounded batch of dates.
- Keep `manual_approval` required for the run and for every date that may use an external resource.
- Pass every date independently through Usage & Cost Governance and Budget Guard before any live request.
- Preserve cache-first behavior for each scenario, location, and observation date.
- Keep `commit_outputs` optional and default it to the existing safe behavior.
- When `commit_outputs=false`, upload all generated meteorology outputs for the batch as workflow artifacts.
- When `commit_outputs=true`, stage and commit only the explicitly allowed meteorology output files.
- Preserve empty-change handling, branch validation, deterministic output updates, and safe push behavior.
- Add a clear maximum date-count guard, with a default maximum of 10 dates per workflow run.
- Fail before live retrieval if parsed input exceeds the maximum date count.
- Document partial-failure behavior so successful cached or retrieved dates remain distinguishable from blocked or failed dates without inventing observations.

### Safety Boundaries

- No scheduled cron trigger.
- No automatic refresh.
- No browser-side API calls.
- No uncontrolled API use.
- No bypass of Usage & Cost Governance or Budget Guard.
- No date may share or inherit another date's guard result.
- `manual_approval` must remain required.
- `commit_outputs` must remain optional.
- Do not add forecasts, simulations, autonomous scheduling, credentials, billing, or unrelated APIs.
- Do not commit logs, temporary files, arbitrary generated files, or files outside the meteorology output allowlist.

### Output And Commit Requirements

When `commit_outputs=false`:

- upload all batch meteorology outputs as artifacts;
- include enough date-specific status information to identify successful, cached, blocked, failed, and missing-data results;
- do not push repository changes.

When `commit_outputs=true`:

- commit only the allowed meteorology output files used by the existing workflow and time-series/trend pipeline;
- reject unexpected staged paths before commit;
- skip the commit when there are no allowed output changes;
- preserve safe branch targeting and bot identity behavior.

The implementation PR must explicitly enumerate and test the output allowlist.

### Verification

- Test that the workflow has `workflow_dispatch` and no `schedule` trigger.
- Test parsing and normalization for the selected date input pattern.
- Test invalid dates, duplicates, ordering, empty input, and malformed ranges where applicable.
- Test the maximum date-count limit, including acceptance at 10 dates and rejection above 10 dates.
- Test that every date passes through Usage & Cost Governance and Budget Guard.
- Test that manual approval remains required and cannot bypass `stop_required`.
- Test cache-first behavior across multiple dates.
- Test artifact mode when `commit_outputs=false`.
- Test the commit output allowlist and rejection of unrelated staged files when `commit_outputs=true`.
- Test empty-change behavior and partial failures.
- Run `python -m unittest discover`.
- Unit and workflow tests must not make live external requests.

### Delivery

Provide the Draft PR URL, selected input pattern, maximum date count, per-date governance behavior, cache behavior, artifact and commit behavior, explicit output allowlist, changed files, and test results.
