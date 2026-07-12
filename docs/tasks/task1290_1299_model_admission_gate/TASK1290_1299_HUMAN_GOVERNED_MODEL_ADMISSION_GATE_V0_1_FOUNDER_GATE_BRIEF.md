> Historical Founder Gate Brief. Its authorization question was answered and Task1290-1299 was subsequently implemented and validated on PR #49. Retained for audit; not executable.

# ClimateOS Task1290-1299 Human-Governed Model Admission Gate v0.1

Date: 2026-07-12

Status: DRAFT_FOR_FOUNDER_REVIEW

Authorization: NOT_EXECUTABLE

Required baseline: `313f0faaaae364ea527af8e0784f447191ec8891`

## Gate Question

Should ClimateOS combine the Task1200-1289 evidence foundations into a
human-governed Model Evidence Passport and Model Admission Gate v0.1 without
automatically admitting, ranking or rejecting a real model?

## Purpose

Define a reviewable decision procedure for whether evidence is sufficient to
allow a model into a declared ClimateOS research use. Admission is scoped to a
model version, purpose, variable, region, forecast horizon, evidence snapshot,
licence and review date. It is not a permanent or universal model verdict.

## Proposed Task Map

| Task | Proposed output |
| --- | --- |
| Task1290 | Founder authorization, authoritative baseline and recovery preflight |
| Task1291 | Admission purpose, authority and non-authority boundary |
| Task1292 | Model Evidence Passport aggregation contract v0.2 |
| Task1293 | Required evidence, completeness rules and blocking conditions |
| Task1294 | Licence, provenance, cost, dependency and exit-path review |
| Task1295 | Statistical, physical, extreme-event and regional evidence reconciliation |
| Task1296 | Uncertainty, dispute, counter-evidence, revision and audit preservation |
| Task1297 | Human-governed admission states, expiry and re-review rules |
| Task1298 | Tiny synthetic admission cases, refusal cases and automated tests |
| Task1299 | Model Assurance closure, Task1300 readiness review and hard stop |

## Candidate States

- `ADMITTED_FOR_RESEARCH`
- `ADMITTED_WITH_LIMITATIONS`
- `REQUIRES_FURTHER_EVIDENCE`
- `NOT_ADMITTED`
- `LICENCE_OR_PROVENANCE_BLOCKED`

These states may be recorded only with a declared evidence snapshot and human
authority. `ADMITTED_FOR_RESEARCH` does not authorize production, public
forecasting, public safety, autonomous action, compliance, legal or investment
use. `NOT_ADMITTED` means not admitted for the declared use on the reviewed
evidence; it is not a permanent claim that the model has no scientific value.

## Required Admission Record

- model registry identity, exact version and source revision;
- declared purpose, variables, region, forecast horizons and users;
- licence, provenance, access, cost and dependency status;
- statistical evidence and baselines;
- physical-consistency evidence and tolerance status;
- extreme-event, regional-fitness, sample and non-stationarity evidence;
- OOD status and applicability limits;
- missing evidence and blocking conditions;
- disputes, counter-evidence and unresolved expert questions;
- revision, expiry, re-review trigger and audit history;
- named or declared responsible human reviewer;
- decision reason and non-authority boundary.

## Human Authority Rules

- the system may assemble evidence and identify blockers;
- the system must not automatically assign an admission state to a real model;
- a human may refuse to decide and use `REQUIRES_FURTHER_EVIDENCE`;
- every decision is revisable and must preserve prior revisions and challenges;
- consequential or contested cases require domain-expert escalation;
- evidence absence cannot be converted into a favourable assumption;
- no admission state becomes a model score or ranking.

## Resource And Cost Rule

The repository-wide Founder Resource and Cost Control Principle applies.
Free, open, inspectable and controllable evidence is preferred. No purchase,
subscription, chargeable trial, paid API, metered overage or other paid
commitment may occur without explicit prior Founder approval supported by a
cost-and-alternatives brief.

## Proposed Executable Scope

If separately authorized, Task1290-1299 may create:

- aggregation and admission contracts;
- evidence completeness and blocker logic;
- human decision, expiry and re-review records;
- tiny synthetic complete, limited, disputed and blocked fixtures;
- automated structural and refusal tests;
- Task1299 closure and Task1300 readiness documentation.

## Excluded Unless Separately Authorized

- downloading, integrating or running an external model;
- large real-data acquisition or computation;
- new real-model statistical or physical evaluation;
- automatic real-model admission, rejection, score or rank;
- production connection or public forecast;
- public-safety, compliance, legal or investment conclusion;
- access to Founder-reserved private EcoEngine assets;
- PR merge;
- Task1300 or later work.

## Founder Decision Options

1. Approve the bounded human-governed foundation as written.
2. Revise its evidence, real-data or human-review scope before authorization.
3. Defer Task1290-1299 and carry the Task1200-1289 foundations without an
   admission gate.

No option is selected by this Brief.
