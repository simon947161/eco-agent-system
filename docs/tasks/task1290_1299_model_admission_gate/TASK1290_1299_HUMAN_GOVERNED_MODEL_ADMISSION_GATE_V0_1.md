# ClimateOS Task1290-1299 Human-Governed Model Admission Gate v0.1

Date: 2026-07-12

Status: IMPLEMENTED_FOR_FOUNDER_REVIEW

Baseline: `313f0faaaae364ea527af8e0784f447191ec8891`

## Purpose

Aggregate the Task1200-1289 assurance foundations into a bounded, auditable
procedure for future model admission decisions. Admission is never a universal
model verdict. It is scoped to an exact model version, source revision, use,
variable, region, forecast horizon, evidence snapshot, licence and review date.

## Task Map

- Task1290: authorization, baseline and recovery preflight.
- Task1291: authority and non-authority boundary.
- Task1292: Model Evidence Passport aggregation contract v0.2.
- Task1293: completeness and blocker rules.
- Task1294: licence, provenance, cost, dependency and exit review.
- Task1295: statistical, physical, extreme-event and regional reconciliation.
- Task1296: uncertainty, dispute, counter-evidence, revision and audit.
- Task1297: human admission states, expiry and re-review.
- Task1298: tiny synthetic cases and refusal tests.
- Task1299: closure and Task1300 preflight readiness review.

## Human Authority

The system may assemble evidence, identify omissions and return eligible
candidate states. It must not assign an admission state to a real model. A real
record requires an explicit human decision plus reviewer identity, decision
reason, scope, evidence snapshot, expiry and audit entry. Missing evidence is
never converted into a favourable assumption.

No real model is admitted by this batch. Synthetic fixture decisions are test
data only and cannot be represented as scientific findings.

## Admission States

- `ADMITTED_FOR_RESEARCH`
- `ADMITTED_WITH_LIMITATIONS`
- `REQUIRES_FURTHER_EVIDENCE`
- `NOT_ADMITTED`
- `LICENCE_OR_PROVENANCE_BLOCKED`

No state is a score or ranking. Production, public forecasting, public safety,
compliance, legal and investment uses remain outside authority.

## Evidence Reconciliation

The aggregation contract requires registry identity, licence and provenance;
statistical evidence; physical-consistency evidence; extreme-event and regional
fitness evidence; OOD and non-stationarity limits; missing evidence; disputes;
revision history; and human responsibility. Evidence sections may disagree.
Disagreement is preserved and escalated rather than averaged into false
certainty.

## External Resource And Commercial Access Continuity

ClimateOS is not restricted to internally created or free resources. External
models, commercial software, hosted services and paid APIs are legitimate
future ClimateOS capabilities. They may be connected when a later task
authorises the integration and the Founder approves any chargeable commitment
after receiving the repository-required paid decision brief.

The long-term architecture may provide governed access, orchestration,
provenance, audit, usage metering and a ClimateOS platform or service charge on
top of third-party costs. End users may fund approved third-party usage. Pricing,
billing, resale rights, provider terms, taxes, service levels and consumer
obligations require a separate commercial gate.

The current batch makes no purchase and creates no paid commitment. This is a
batch boundary, not a permanent ban on paid APIs, external models or commercial
integration.

## Verification Boundary

The implementation provides deterministic structural validation and refusal
logic with tiny synthetic cases. It performs no external download, model run,
real-model evaluation, automatic real-model decision or Task1300 work.
