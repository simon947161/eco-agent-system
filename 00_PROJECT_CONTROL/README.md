# Project Control Layer

This folder is the human-readable control layer for the ClimateOS /
eco-agent-system repository.

It controls the roadmap, task index, Codex batch queue, repository rules,
future agent templates, and architecture decisions.

Use it as the starting point before creating a new ClimateOS, CarbonOS,
EnergyOS, ParkOS, ESGOS, GISOS, or demonstration task.

## Queue Management

- [Queue Dashboard](QUEUE_DASHBOARD.md)
- [Queue Status](QUEUE_STATUS.md)
- [Queue Rules](QUEUE_RULES.md)
- [Task Dependencies](TASK_DEPENDENCIES.md)
- [Task Pipeline](TASK_PIPELINE.md)
- [Completion Log](COMPLETION_LOG.md)
- [Task Request Template](TASK_REQUEST_TEMPLATE.md)
- [Task Review Template](TASK_REVIEW_TEMPLATE.md)

The dashboard is the quickest starting point. Queue Status records the live
task stages, while the templates keep future requests and reviews consistent.

## Agent Factory Standard

- [Agent Standard](AGENT_STANDARD.md)
- [Agent Lifecycle](AGENT_LIFECYCLE.md)
- [Agent Checklist](AGENT_CHECKLIST.md)
- [Agent Catalog](AGENT_CATALOG.md)
- [Repository Maturity](REPOSITORY_MATURITY.md)
- [Agent Template](templates/agent_template.md)
- [Scenario Template](templates/scenario_template.md)
- [Validation Template](templates/validation_template.md)

The existing root-level `AGENT_TEMPLATE.md` remains available for backward
compatibility. New agent specifications should use the templates directory and
the official Agent Standard.

## Repository Baseline

- [Baseline Release V1](BASELINE_RELEASE_V1.md)
- [Baseline Summary](BASELINE_SUMMARY.md)
- [Repository Status](REPOSITORY_STATUS.md)
- [Release Notes V1](RELEASE_NOTES_V1.md)

ClimateOS Repository OS v1.0 is the documented checkpoint for the repository
control, master directory, queue, and Agent Standard layers. It adds no new
runtime or subsystem capability.
