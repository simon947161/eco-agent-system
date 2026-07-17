# ClimateOS Static Experiment Design Contract v0.1

Date: 2026-07-18

Status: FORM_CONTRACT_ONLY / NO_CASE_DESIGNED / NO_RUN / HUMAN_REVIEW_REQUIRED

## 1. Meaning of “static design”

In this contract, a static design is an empty governance structure describing
future required fields. It is not a synthetic experiment, model configuration,
scientific method selection or approval to fill the fields with real or
fabricated numerical content.

## 2. Identity and revision

Every future proposal requires:

| Field | Rule |
|---|---|
| `experiment_id` | stable `MECH-EXP-NNN`; never reused |
| `design_revision` | immutable revision identifier |
| `parent_revision` | required after the first revision |
| `hypothesis_revision_id` | exact reviewed hypothesis revision |
| `created_at` | proposal-record time, not run time |
| `owner_role` | role only until a person separately consents |
| `status` | one controlled state |

Allowed states are `EMPTY_TEMPLATE`, `BLOCKED_INCOMPLETE`,
`READY_FOR_INDEPENDENT_DESIGN_REVIEW`, `NOT_TESTABLE`, `DO_NOT_PROCEED`, and
`SUPERSEDED`. None authorizes a run.

## 3. Design-role separation

| Role | Required declaration | Boundary |
|---|---|---|
| baseline | reference configuration identity and rationale | not “truth” or observation |
| perturbation | one bounded proposed change and mechanism link | no implementation in this batch |
| control | what remains unchanged and why | cannot erase known confounding |
| sensitivity | one-factor or declared joint-change logic | no parameter values selected here |
| replication | identity and independence rule | no replicate count authorized |

Baseline and control are not interchangeable. A sensitivity case cannot be
introduced after seeing output without an append-only design revision and a
new review decision.

## 4. Reproducibility identity requirements

A future design must bind, before any run:

1. model and component versions;
2. source and dependency identities;
3. build and runtime environment identities;
4. configuration checksum;
5. input and boundary-object identities and checksums;
6. preprocessing and transformation versions;
7. random-seed policy where relevant;
8. diagnostic implementation versions;
9. output naming, retention and integrity rules;
10. responsible review decisions.

Current value for every runtime identity is `NOT_ADMITTED`. No placeholder in
this document may be treated as a version lock or executable configuration.

## 5. Diagnostic pre-registration

Before a future run request, each diagnostic must declare:

- the hypothesis link it tests;
- variable meaning, unit and sign convention;
- spatial and temporal support;
- aggregation or transformation method;
- expected direction and a null/no-material-response possibility;
- uncertainty and missingness treatment;
- evidence threshold and falsification contribution;
- primary, secondary or exploratory status.

After output inspection, a primary metric, period, region, level, aggregation
or threshold may not be silently changed. Any change creates a new revision,
records the reason and labels earlier output as belonging to the earlier design.

## 6. Resource and authority gates

| Gate | Current state |
|---|---|
| hypothesis expert review | not assigned / not consented |
| model and dependency admission | blocked |
| licence review | incomplete |
| data/input admission | blocked |
| compute authorization | zero / blocked |
| incremental storage authorization | zero / blocked |
| monetary commitment | AUD 0 only |
| carbon/energy execution allowance | zero / blocked |
| model or synthetic run | not authorized |

Zero is a refusal state for this batch, not an estimate of future requirements.

## 7. Minimum stop conditions

A future request stops before execution when any of the following is true:

- the linked hypothesis is incomplete, superseded or not independently reviewed;
- a version, licence, input, boundary, diagnostic or scale identity is unresolved;
- the proposed control cannot distinguish a named alternative explanation;
- a stop/abort condition is absent;
- expert ownership or consent is absent;
- resource, cost, storage, carbon or security authority is absent;
- the requested downstream use is prohibited.

## 8. Current decision

`STATIC_FORM_CONTRACT_READY / CASE_DESIGN_NOT_CREATED / TINY_SYNTHETIC_BLOCKED / MODEL_AND_DATA_BLOCKED / RUN_NOT_AUTHORIZED`
