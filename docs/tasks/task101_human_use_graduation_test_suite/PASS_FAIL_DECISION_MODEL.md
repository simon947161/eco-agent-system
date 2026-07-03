# Pass/Fail Decision Model

## Purpose

This document defines a simple documentation-only pass/fail model for Task101 Human Use Graduation.

The model helps human reviewers decide whether a scenario demonstrates sufficient Foundation readiness for real environmental project judgment.

The model is **documentation-only**. It does not create automated scoring logic, runtime thresholds, or algorithmic decision-making.

## Decision Principle

**Pass/fail is a human judgment, not a score.**

The model provides a structured way to make that judgment explicit, consistent, and reviewable — but the decision itself is made by a qualified human reviewer.

## Three Outcome Types

Each scenario has one of three outcomes:

```
PASS        → Foundation logic holds. Judgment traceable.
BOUNDED FAIL→ Foundation logic holds partially. Gaps documented.
                Remediation path identified.
FAIL        → Foundation logic breaks down. Critical gap.
                Remediation required before proceeding.
```

**BOUNDED FAIL is not a rejection.** It is the correct outcome when the test is working correctly — when it reveals exactly what the Foundation cannot yet support. Bounded failures define the work for the next phase.

**FAIL is a serious outcome.** It means the Foundation cannot support this type of judgment at all. A FAIL requires immediate documentation and a decision about whether to remediate before continuing.

## The Five-Check Gate

For each scenario, the reviewer evaluates five checks:

```
Reality Test       → Reality PASS / Reality FAIL
Evidence Test      → Evidence PASS / Evidence FAIL
Validation Test    → Validation PASS / Validation FAIL
Governance Test    → Governance PASS / Governance FAIL
Inheritance Test   → Inheritance PASS / Inheritance FAIL
```

Each check is evaluated independently.

The scenario outcome is determined by how the five check results combine.

## Check Evaluation Criteria

### Reality Test: PASS

The reviewer can trace the judgment back to a specific, identifiable environmental object.

Environmental object is described with enough specificity to be located, identified, or verified.

**Reality Test: FAIL**

The environmental object is not identifiable from the judgment. The judgment is about a generalized category rather than a specific thing.

### Evidence Test: PASS

The reviewer can trace the judgment through every level of the evidence chain — from raw data, to observation, to inference, to evidence, to claim, to recommendation — without any level being skipped or assumed.

Each step is distinguishable from adjacent steps.

**Evidence Test: FAIL**

One or more steps in the evidence chain are missing, assumed without documentation, or leapfrogged by authority or assumption. The reviewer cannot trace the full chain.

### Validation Test: PASS

The reviewer can confirm that validation considerations have been addressed:
- Source reliability assessed
- Time validity evaluated
- Spatial fit evaluated
- Conflicting evidence identified and addressed
- Confidence level assigned and justified
- Human review requirement determined

**Validation Test: FAIL**

Validation considerations are not addressed, or are addressed only superficially. The reviewer cannot confirm that the evidence has been properly validated before the judgment is made.

### Governance Test: PASS

A responsible party is identified, the governance boundary is defined, and the review/approval process before action is documented.

The reviewer can confirm that no action can proceed without the defined review and approval.

**Governance Test: FAIL**

No responsible party is identified, or the governance boundary is absent, or the review/approval process is not documented. The judgment could lead to action without governance oversight.

### Inheritance Test: PASS

The judgment logic follows the Foundation's common governance pattern — Observation → Evidence → Validation → Confidence → Review → Recommendation → Responsibility — in a domain-agnostic way.

A reviewer can confirm that the same pattern could be applied in a different domain runtime (CarbonOS, WaterOS, EnergyOS, BuildingOS) without modifying the Foundation architecture.

**Inheritance Test: FAIL**

The judgment logic is domain-specific and cannot be separated from the particular domain context. The Foundation's common governance pattern is not being followed.

## Scenario Outcome Matrix

```
Reality     Evidence   Validation  Governance  Inheritance → Scenario Result
────────────────────────────────────────────────────────────────────────────
PASS        PASS       PASS        PASS        PASS        → PASS
PASS        PASS       PASS        PASS        BOUNDED FAIL → BOUNDED FAIL
PASS        PASS       PASS        PASS        FAIL         → FAIL
PASS        PASS       PASS        BOUNDED FAIL  any         → BOUNDED FAIL
PASS        PASS       PASS        FAIL         any         → FAIL
PASS        PASS       BOUNDED FAIL any         any         → BOUNDED FAIL
PASS        PASS       FAIL        any         any         → FAIL
PASS        BOUNDED FAIL any       any         any         → BOUNDED FAIL
PASS        FAIL       any         any         any         → FAIL
BOUNDED FAIL any       any         any         any         → BOUNDED FAIL
FAIL        any        any         any         any         → FAIL
```

**Rule:** Governance and Reality are critical gates. If either fails, the scenario fails regardless of other results.

**Rule:** Evidence is a critical gate. If Evidence fails, the scenario fails regardless of other results.

**Rule:** Bounded failures in Validation, Governance (where Reality and Evidence both pass), or Inheritance result in a BOUNDED FAIL, not a FAIL.

**Rule:** If Reality is a BOUNDED FAIL, the scenario is a BOUNDED FAIL — the Foundation can partially identify the environmental object but with gaps.

## Confidence Gate

Before making the final outcome decision, the reviewer applies the confidence gate:

```
Confidence Level Required: [Depends on judgment type]
Confidence Level Assigned: [From Validation Test]

If Assigned < Required:
→ Scenario outcome downgrades by one level:
   PASS → BOUNDED FAIL
   BOUNDED FAIL → BOUNDED FAIL (document the gap)
   FAIL → FAIL (document but do not downgrade further)
```

**Confidence level thresholds:**

| Judgment Type | Minimum Required Confidence |
|--------------|---------------------------|
| Routine disclosure / monitoring | Medium |
| Risk assessment / project planning | Medium-High |
| Certification / approval / legal claim | High |
| Emergency response / public safety | Very High |

**Note:** If no confidence level is assigned at all, this is treated as a FAIL in the Validation Test, which cascades to a FAIL in the overall scenario.

## Bounded Fail Documentation

For any BOUNDED FAIL, the reviewer documents:

```
Bounded Failure Record:

Check Affected:         [e.g., Governance Test]
Severity:               [Critical / Moderate / Minor]
Description:            [What the gap is]
Impact:                 [What the gap means for the judgment]
Remediation Path:       [What is needed to close the gap]
Remediation Owner:      [Who is responsible for remediation]
Remediation Timeline:   [When the gap should be closed]
Blocking:               [Yes / No — does this gap prevent moving to next phase?]
```

**Blocking vs. Non-Blocking Bounded Failures:**

- **Non-blocking bounded failure:** The gap does not prevent the Foundation from being submitted for the next phase. The gap is documented and remediation is planned.
- **Blocking bounded failure:** The gap is severe enough that proceeding to the next phase without remediation would undermine the Foundation's credibility or safety. The gap must be closed before the Foundation advances.

## Test Suite Outcome

After evaluating all five scenarios:

```
Overall Pass/Fail Determination:

Test Suite Result: [PASS / PARTIAL PASS / FAIL]

PARTIAL PASS means:
- All scenarios are either PASS or BOUNDED FAIL (non-blocking)
- No scenario is a FAIL
- All bounded failures are documented with remediation paths
- The Foundation demonstrates sufficient judgment capability to proceed
  to the next controlled phase with the identified gaps as work items

FAIL means:
- One or more scenarios is a FAIL
- The Foundation reveals critical gaps that prevent real environmental
  judgment support in the affected domain areas
- Remediation is required before the Foundation can advance
```

## Decision Review Process

Before finalizing the scenario outcome:

1. **Review all five checks** — ensure each check has been evaluated
2. **Apply the decision matrix** — determine the scenario outcome
3. **Apply the confidence gate** — adjust if confidence level is below threshold
4. **Document bounded failures** — for any BOUNDED FAIL, complete the Bounded Failure Record
5. **Apply the test suite outcome** — aggregate all scenario results to determine the test suite result

## Documentation Requirements

For each scenario, the reviewer must document:

- [ ] All five checks evaluated
- [ ] Each check result (PASS / BOUNDED FAIL / FAIL)
- [ ] Decision matrix applied
- [ ] Confidence gate applied
- [ ] Bounded Failure Records (if applicable)
- [ ] Scenario outcome
- [ ] Rationale for outcome decision
- [ ] Reviewer name and date

## What the Model Does Not Do

This model does not:
- Generate automated scores from check results
- Create algorithmic pass/fail thresholds
- Replace human judgment
- Declare environmental conclusions
- Validate technical accuracy of domain-specific claims

The model is a structured documentation framework for making a human judgment explicit and reviewable.

## Related Documents

- `TASK101_HUMAN_USE_GRADUATION_TEST_SUITE.md` — test suite overview
- `TEST_SCENARIO_CATALOG.md` — scenario descriptions
- `TEST_INPUT_OUTPUT_TEMPLATE.md` — how to evaluate each scenario

## Status

Draft in progress.
