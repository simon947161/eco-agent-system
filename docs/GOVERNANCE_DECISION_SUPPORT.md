# Internal Governance Decision Support Layer

This layer organizes existing CCZPS-Lite traceability, hypothesis, validation,
expert-review, and planning-support artifacts for internal human review.

It produces:

- `cczps_lite/output/governance_decision_records.json`
- `cczps_lite/output/governance_decision_records.md`

Allowed internal statuses are:

- `not_decided`
- `requires_further_review`
- `conditionally_supported_for_internal_planning`
- `not_supported_by_current_evidence`
- `deferred`

These statuses are not approvals. Every generated record keeps
`external_approval_status` as `not_ready_for_approval`, and requires both human
and professional review.

The runtime is deterministic and local-only. It performs no scenario
comparison, prioritization, professional conclusion, GIS or DEM operation,
simulation, forecast, external API request, or LLM call.
