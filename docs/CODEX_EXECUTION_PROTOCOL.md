# CCZPS-Lite Codex Execution Protocol

## Purpose

This protocol governs execution of the CCZPS-Lite task queue. It keeps each change reviewable, testable, and consistent with the system's safety and governance boundaries.

## Branch And Pull Request Rules

1. Use one task per branch.
2. Use one task per pull request.
3. Create every pull request as Draft initially.
4. Do not merge automatically.
5. Base each task branch on the current requested base branch.
6. Keep changes limited to the task scope. Do not bundle unrelated cleanup.

## Verification And Delivery

1. Run the task's required tests before delivery.
2. Run the existing regression suite unless the task explicitly narrows it.
3. Report test results accurately, including tests that could not be run.
4. Document all changed files in the delivery summary.
5. Document new generated outputs, their producers, and whether they are committed, cached, or uploaded as artifacts.
6. Keep the pull request open for review unless the user explicitly requests a later merge action.

## Safety Boundaries

1. Preserve existing safety boundaries.
2. Do not introduce live API calls unless the task explicitly requires them.
3. The dashboard must not perform browser-side external API calls.
4. Budget Guard must protect live external resource calls.
5. Live calls must remain explicit, controlled, and visible.
6. Do not introduce hidden resource consumption, autonomous spending, payment processing, subscriptions, invoicing, crypto, token, or RWA systems.
7. Do not convert observational evidence into forecasts, predictions, or autonomous recommendations unless a future task explicitly authorises that capability.

## Generated Outputs

For every new or modified generated output, document:

- file path;
- generating command or workflow;
- source data and whether it is live, mocked, cached, or local;
- overwrite or append behaviour;
- missing-data behaviour;
- governance and Budget Guard fields;
- dashboard or report consumers;
- whether the output is committed or distributed as an artifact.

## Blocked Work

If a task is blocked:

1. report the blocking condition clearly;
2. describe the investigation already completed;
3. identify the missing input, permission, dependency, or external state;
4. do not guess, invent data, or silently broaden scope;
5. leave the branch and pull request in a reviewable state when possible.

## Completion Checklist

- Task scope is implemented and no later queue task is included.
- Required tests pass.
- Existing regressions pass.
- Safety boundaries remain documented.
- Changed files and generated outputs are listed.
- Draft pull request is created.
- Pull request is not merged automatically.
