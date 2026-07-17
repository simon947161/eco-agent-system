# ClimateOS Mechanism Hypothesis Protocol v0.1

Date: 2026-07-17

Status: STATIC_CONTRACT / NO_RUN / HUMAN_REVIEW_REQUIRED / CONCLUSIONS_BLOCKED

## 1. Record identity and revision

Every record requires:

| Field | Rule |
|---|---|
| `hypothesis_id` | stable `MECH-HYP-NNN` identity; never reused |
| `revision_id` | immutable revision; corrections append a new revision |
| `parent_revision` | required after the first revision |
| `created_at` | record time, not an observation time |
| `author_role` | role only; no unconsented person may be named |
| `status` | one controlled state from the state table |

Allowed states are `DRAFT_STATIC`, `BLOCKED_INCOMPLETE`,
`READY_FOR_EXPERT_REVIEW`, `NOT_TESTABLE`, `REJECTED_PROTOCOL`, and
`SUPERSEDED`. None means scientifically supported or run-authorized.

## 2. Minimum hypothesis content

1. bounded research question;
2. proposed mechanism statement explicitly labelled as a hypothesis;
3. typed chain nodes and directed edges;
4. expected direction for each edge;
5. spatial and temporal support assumed for each node;
6. proposed lag or simultaneity semantics without invented precision;
7. required diagnostics and the role of each diagnostic;
8. at least two plausible alternative explanations;
9. observations that would weaken or falsify each link;
10. evidence threshold stated before any future run;
11. uncertainty, non-stationarity and transformation risks;
12. stop conditions and prohibited downstream uses;
13. accountable expert-owner role and consent state.

## 3. Chain contract

Nodes must declare a type: `FORCING`, `STATE`, `PROCESS`, `RESPONSE`,
`CONFOUNDING_CONTEXT`, or `DIAGNOSTIC_ONLY`. Edges must declare
`PROPOSED_INFLUENCE`, `PROPOSED_MEDIATION`, `ALTERNATIVE_PATH`, or
`POTENTIAL_CONFOUNDING`.

An edge is never encoded as `CAUSES`. A diagram, correlation, temporal order,
model output or literature citation cannot silently promote an edge to a causal
finding. Missing intermediate diagnostics must remain visible.

## 4. Scale and time contract

- grid, station, catchment, regional and project/site scales are not interchangeable;
- an aggregation or downscaling step requires a named transformation and uncertainty note;
- observation time, model valid time, accumulation window, lag window and review time remain separate;
- a proposed lag must be a range or unresolved state until evidence supports precision;
- stationarity is never assumed across seasons, regimes, terrain or source versions;
- Cooma, Bondo and Riverina evidence may not be inferred from a generic hypothesis record.

## 5. Evidence-role separation

| Role | Permitted use | Prohibited promotion |
|---|---|---|
| observation | future measured evidence after separate admission | direct causal proof |
| model output | future experiment diagnostic after run authorization | observation or truth |
| proxy | indirect context with declared limitations | target-variable substitute |
| literature | attributed prior statement | ClimateOS finding |
| synthetic fixture | contract and failure-path test | real-world evidence |
| expert review | accountable interpretation after consent | replacement for missing evidence |

## 6. Falsification and alternatives

Every proposed edge requires:

- a diagnostic that could contradict the expected direction;
- an explicit null or no-material-response possibility;
- at least one measurement/representation failure alternative;
- at least one competing-process or confounding alternative;
- a stop condition when required evidence, licence, compute or expertise is absent.

`NOT_TESTABLE` and `DO_NOT_PROCEED` are valid results. Negative or ambiguous
results must not be hidden by selecting a more favourable metric, period,
region, model configuration or narrative after inspection.

## 7. Evidence threshold and promotion gate

A future record may reach `READY_FOR_EXPERT_REVIEW` only when it is structurally
complete. That state does not authorize an experiment. Promotion beyond static
review requires separate gates for reference/version, licence, data, compute,
reproducibility, safety, cost and a consenting qualified expert owner.

No count, score or agent vote may override a failed authority, licence,
falsification, scale, uncertainty or human-review gate.

## 8. Expert and consent contract

- record a role first, not an assumed person;
- naming or contacting an individual requires separate Founder authority;
- consent must be explicit, dated, scoped and revocable;
- conflicts of interest and institutional limits must be declared;
- the expert may return `INSUFFICIENT_EVIDENCE`, `NOT_TESTABLE` or
  `OUTSIDE_EXPERTISE` without pressure to approve;
- no uncontacted CSIRO or other scientist is represented as an appointed reviewer.

## 9. Current decision

`STATIC_PROTOCOL_READY / EXPERIMENT_DESIGN_NOT_AUTHORIZED / MODEL_RUN_BLOCKED / EXPERT_UNASSIGNED / SCIENTIFIC_AND_LOCAL_CONCLUSIONS_PROHIBITED`
