# Planner Cycle Reuse–Gap–Build Matrix v0.1

Status: `REPOSITORY MAPPING / IMPLEMENTATION PRIORITIES PROPOSED`

| Stage | Existing foundation to reuse | Verified gap | Minimal build candidate | Priority for first slice |
|---|---|---|---|---|
| Observe | QGIS Cooma foundations; terrain pack; spatial observation template; environmental evidence object | no common typed site-observation envelope | PC-01 schema and fixture | P0 |
| Retrieve | source registries; official-source intake; WaterNSW admission controls | request is not consistently bound to a planning claim and intended use | PC-02 schema | P0 |
| Validate | Evidence Passport; lineage contract; Admission Control; conclusion maturity | professional gates vary by domain and are not one interface | PC-03 interface adapter; do not replace domain cards | P0 |
| Build State | spatial layers; admitted evidence; conclusion language protocol | no unified, time-bounded environmental state object | PC-04 schema | P0 |
| Relationships | environmental coupling; ontology/claim graph patterns; model comparison | supported association and proposed influence can blur in narrative | PC-05 schema | P1 |
| Hypotheses | Mechanism Hypothesis Protocol v0.1 | not connected to Planner Cycle IDs and state objects | thin PC-06 adapter, not a second hypothesis system | P1 |
| Test/Simulate | forecast/model interfaces; static experiment and no-run gates | no decision-materiality or simpler-test test before simulation design | PC-07 gate | P1 |
| Risk/Opportunity | S0–S7 evidence maturity; L0–L4 conclusion levels; exposure concepts | opportunity, distribution and expiry lack a common paired record | PC-08 schema | P2 |
| Interventions | planning hypotheses; scenario demonstrator; stewardship principles | options lack consistent mechanism, harm, reversibility and no-action fields | PC-09 schema | P2 |
| Engineering Test | physical-reality and distributed-intervention principles | necessity hierarchy is not executable or reviewable | PC-10 checklist/state machine | P2 |
| Responsibility | governance layers; Founder Gates; review roles | affected parties, competence, accountability and legal authority are conflated | PC-11 schema | P2 |
| Rank Alternatives | scenario comparison and model divergence patterns | no non-compensable gates, sensitivity or uncertainty-bounded ranking | PC-12 schema | P3 |
| Action Passport | Evidence Passport and run receipt patterns | no decision-facing package joining evidence, reasoning, authority and monitoring | PC-13 schema/renderer | P0, A0-only |
| Monitoring | audit, persistence, early-warning expiry/demotion | no owner-trigger-response object tied back to an Action Passport | PC-14 schema | P1 |
| Learn | Founder Review; retrospective validation concept; versioned records | no governed outcome-to-Skill revision ledger | PC-15 schema | P1 |

## Reuse decisions

- Extend the Environmental Evidence Object; do not create a competing evidence
  identity system.
- Adapt the Professional Validation Interface and domain review cards; do not
  create a generic interface that pretends all professional competence is
  interchangeable.
- Reference the Mechanism Hypothesis Protocol; do not fork it into a second
  causal vocabulary.
- Retain S0–S7, L0–L4 and A0–A4 as independent governance axes.
- Reuse audit, receipt and append-only revision patterns for Action Passport,
  Monitoring and Skill Revision records.

## Build order

### P0 — first vertical slice

Implement only enough of PC-01, PC-02, PC-03, PC-04 and PC-13 to demonstrate
`EP-SKILL-001 Cooma Site Reading v0.1`. The Action Passport is restricted to
A0: evidence requests, scope narrowing, review requests and a next controlled
analysis recommendation.

### P1 — reasoning discipline and feedback

Add relationship typing, hypothesis linkage, simulation necessity, monitoring
and Skill revision after the first slice proves traceability and stopping.

### P2 — planning option formation

Add paired risk/opportunity, intervention structure, engineering necessity and
actor/authority only after appropriate professional evaluation criteria exist.

### P3 — bounded ranking

Alternative comparison comes last. A scoring interface built earlier would
create false precision and could hide non-compensable evidence or authority
failures.

## Explicit deferrals

- schema implementation and runtime orchestration;
- real Cooma Site Reading output;
- automated data retrieval;
- model or simulation execution;
- hydrology comparison pending H1–H8;
- Urban Flood Planning Skill;
- Shanghai extreme-rainfall reference-event stress test;
- RealBench/OOD implementation and task renumbering.
