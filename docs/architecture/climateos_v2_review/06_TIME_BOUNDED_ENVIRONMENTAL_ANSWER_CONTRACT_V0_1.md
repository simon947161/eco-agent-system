# Time-Bounded Environmental Answer Contract v0.1

## Required fields

```yaml
answer_id: stable identifier
question:
decision_use:
place:
spatial_boundary:
assessment_period:
evidence_cutoff:
issued_at:
valid_until:
conclusion_level: L0 | L1 | L2 | L3 | L4
evidence_maturity: S0 | S1 | S2 | S3 | S4 | S5 | S6 | S7
answer:
confidence:
supporting_evidence: []
conflicting_evidence: []
missing_critical_evidence: []
local_translation_path: []
alternative_explanations: []
consequence_if_true:
consequence_if_false:
intervention_window:
permitted_actions: []
prohibited_actions: []
update_triggers: []
demotion_triggers: []
stop_conditions: []
human_review:
official_confirmation:
retrospective_validation:
```

## Semantic rules

1. `answer` must be narrower than the evidence.
2. `confidence` is not a substitute for conclusion level or maturity.
3. `official_confirmation` records issuer, date, scope and relationship to the
   local question; absence does not force the answer to null.
4. `valid_until` is mandatory for S1–S6.
5. a missing critical variable must reduce scope, confidence or level;
6. conflicting evidence is preserved, not averaged away silently;
7. permitted actions must be proportionate to reversibility and consequence;
8. changed evidence creates a new version rather than mutating history;
9. expired answers are not current answers;
10. retrospective validation cannot rewrite what was known at issue time.

## Minimum human-readable answer

```text
As of [evidence cut-off], for [boundary] and [period], the evidence supports
[bounded answer] at [stage/level/confidence].

This is supported by [evidence] and weakened by [conflicts/gaps].
It remains valid until [date/event].

The proportionate action now is [action]. Do not use this answer for
[prohibited use]. Reassess if [trigger].
```

## Release controls

- L0/L1 facts may be displayed with attribution and scope;
- L2 indicators require reproducible method and receipt;
- L3 assessments require triangulation, alternatives, uncertainty and
  qualified review;
- L4 decisions remain with the accountable authority or professional;
- public emergency communication requires a separate release authority,
  regardless of stage.

