# ClimateOS Planner Contract Registry v0.1

Status: `DESIGN REGISTRY / SCHEMAS NOT IMPLEMENTED`

## Common envelope

Every contract carries:

`object_id`, `object_type`, `schema_version`, `revision_id`, `parent_revision`,
`planner_cycle_id`, `created_at`, `author_role`, `place_scope`,
`spatial_boundary_id`, `time_scope`, `evidence_cutoff`, `intended_use`,
`prohibited_uses`, `source_object_ids`, `uncertainties`, `review_state`,
`maximum_conclusion_level`, `maximum_intervention_class`, `valid_until`,
`stop_reasons`, and `supersedes`.

Unknown values are explicit. Immutable revisions are appended, not overwritten.

## Contract definitions

| ID | Contract | Minimum stage-specific fields | Controlled decisions / states |
|---|---|---|---|
| PC-01 | Site Observation Contract | observation class; observation method; direct/derived/reported status; geometry; observed time; unit; limitation; unknowns | `RECORDED`, `CONTEXT_ONLY`, `EVIDENCE_REQUIRED`, `REJECTED_AS_OBSERVATION` |
| PC-02 | Evidence Request Contract | question/claim served; requested variable/object; spatial/temporal fitness; acceptable source class; authority; licence; cost/network limits; fulfilment test | `OPEN`, `FULFILLED_PENDING_VALIDATION`, `BLOCKED`, `CANCELLED`, `SUPERSEDED` |
| PC-03 | Professional Review Gate Interface | domain; why required; reviewer competence; evidence version; review questions; independence/conflict; findings; limitations; signature/consent; re-review trigger | `UNASSIGNED`, `PENDING`, `INSUFFICIENT_EVIDENCE`, `OUTSIDE_EXPERTISE`, `CONDITIONAL`, `SUPPORTED_FOR_FURTHER_ASSESSMENT`, `REJECTED` |
| PC-04 | Environmental State v0.1 | state variable; assertion class; value/category; unit; boundary/time; evidence support/contradiction; missingness; derivation; confidence basis | `OBSERVED`, `DERIVED`, `INTERPRETED`, `CONFLICTED`, `UNKNOWN`, `EXPIRED` |
| PC-05 | Relationship Claim Contract | source/target state IDs; relationship type; spatial/temporal alignment; support; counterevidence; alternatives; causal status; review | `OBSERVED_ASSOCIATION`, `DEFINED_DEPENDENCY`, `PROPOSED_INFLUENCE`, `POTENTIAL_CONFOUNDING`, `UNRESOLVED` |
| PC-06 | Hypothesis Record | bounded question; mechanism chain; alternatives; falsifiers; diagnostics; threshold; scale/lag; uncertainty; expert owner; stop condition | reuse mechanism protocol states; never `PROVEN` |
| PC-07 | Simulation Necessity Gate | decision uncertainty; materiality; expected information gain; simpler evidence/test alternatives; model fitness; data/compute/licence/cost; harm; owner | `NOT_NEEDED`, `NOT_JUSTIFIED`, `BLOCKED`, `DESIGN_REVIEW_REQUIRED`, `ELIGIBLE_FOR_SEPARATE_AUTHORIZATION` |
| PC-08 | Risk–Opportunity Register | driver; receptor/beneficiary; exposure; consequence/benefit; likelihood basis; time horizon; distribution/equity; uncertainty; reversibility; trigger | `CONTEXT_ONLY`, `CANDIDATE`, `REVIEW_REQUIRED`, `BOUNDED_ASSESSMENT`, `DEMOTED`, `EXPIRED` |
| PC-09 | Intervention Option Contract | objective; option class; mechanism; scale; dependencies; expected effect; co-benefits; harms; reversibility; lifecycle; evidence; owner; no-action comparator | `IDEA`, `ELIGIBLE_FOR_COMPARISON`, `REVIEW_REQUIRED`, `INADMISSIBLE`, `SUPERSEDED` |
| PC-10 | Engineering Necessity Test v0.1 | prevent/avoid; source reduction; distributed retention; infiltration; storage/reuse; natural-path restoration; land-use/operational change; residual risk; engineering case | `NON_ENGINEERING_SUFFICIENT`, `HYBRID_REVIEW`, `ENGINEERING_CASE_UNESTABLISHED`, `ENGINEERING_ASSESSMENT_JUSTIFIED`, `AUTHORITY_REQUIRED` |
| PC-11 | Actor–Authority Matrix | actor role; affected/beneficiary status; jurisdiction; competence; accountability; decision right; consent; duty; escalation; conflict | `INFORM`, `CONSULT`, `REVIEW`, `APPROVE`, `IMPLEMENT`, `MONITOR`; capability never implies authority |
| PC-12 | Bounded Alternative Comparison | criteria; non-compensable gates; option evidence; weights/ranges; uncertainty; sensitivity; distributional impacts; dissent; decision owner | `NOT_COMPARABLE`, `PARTIALLY_COMPARABLE`, `REVIEW_CANDIDATE`; no automatic winner |
| PC-13 | Action Passport | question; evidence/state snapshot; permissible claim; options; recommended consideration; uncertainty; dissent; authority; action class; expiry; verification | `DRAFT`, `BLOCKED`, `READY_FOR_HUMAN_REVIEW`, `ACCEPTED_AS_DECISION_SUPPORT`, `REJECTED`, `SUPERSEDED`, `CLOSED` |
| PC-14 | Monitoring and Re-review Trigger | indicator; baseline; method; owner; cadence; threshold; response; expiry; missing-data response; evidence destination | `ACTIVE`, `TRIGGERED`, `PAUSED`, `FAILED_OBSERVABILITY`, `CLOSED`, `SUPERSEDED` |
| PC-15 | Skill Revision Record | skill/version; triggering evidence/outcome; expected vs observed; error class; affected rules; proposed change; validation; approver; rollback | `DRAFT`, `VALIDATION_REQUIRED`, `FOUNDER_REVIEW`, `APPROVED_FOR_NEW_VERSION`, `REJECTED`, `ROLLED_BACK` |

## Cross-contract invariants

1. Evidence must be admitted for the exact named use before supporting a state.
2. Facts, derived values, interpretations, hypotheses and options remain typed.
3. Place, scale, time, datum, units and aggregation cannot change silently.
4. Relationship objects cannot use `CAUSES` without an applicable reviewed
   scientific basis; v0.1 defaults to proposed or associated relationships.
5. A failed professional, authority, licence, safety, privacy or evidence gate
   is non-compensable and cannot be outvoted by a score.
6. Simulation eligibility is not run authorization.
7. Option ranking is not approval, procurement, instruction or execution.
8. Every time-bounded object has expiry, demotion or re-review semantics.
9. Human dissent is preserved next to the decision, not removed from history.
10. Learning creates a new Skill version; it never retroactively alters the
    evidence, reasoning or decision record that produced an outcome.

## Minimal Action Passport shape

```yaml
action_passport_id: AP-DRAFT-001
planner_cycle_id: PCYCLE-DRAFT-001
status: DRAFT
question: null
place_scope: null
time_scope: null
evidence_cutoff: null
environmental_state_ids: []
relationship_claim_ids: []
risk_opportunity_ids: []
option_ids: []
comparison_id: null
permissible_claims: []
prohibited_uses: []
uncertainties: []
professional_review_gates: []
authority:
  accountable_human_role: null
  maximum_intervention_class: A0
recommended_consideration: null
monitoring_plan_id: null
valid_until: null
stop_reasons: []
```

This example is deliberately empty. It validates structure only and is not a
Cooma Action Passport.
