# Test Input/Output Template

## Purpose

This document provides a reusable template for structuring Task101 test inputs and outputs.

Each scenario evaluation follows the same template structure. The template ensures that all five Task100 graduation checks are applied consistently across all scenarios.

## Template Structure

Each scenario evaluation contains:

```
1. Test Header
2. Environmental Object Definition
3. Test Input
4. Expected Human-Readable Output
5. Evidence Notes
6. Validation Notes
7. Governance Boundary Notes
8. Responsibility Boundary Notes
9. Confidence Notes
10. Runtime Inheritance Notes
11. Scenario Evaluation Record
```

---

## 1. Test Header

```
Scenario ID:        [e.g., CarbonOS-01]
Scenario Title:     [e.g., Carbon Claim / ESG Disclosure]
Domain:             [e.g., CarbonOS]
Judgment Type:      [e.g., Disclosure readiness assessment]
Complexity:         [Low / Medium / High]
Reviewer:           [Name or role]
Review Date:        [YYYY-MM-DD]
ClimateOS Version:   [Reference to frozen Foundation version]
```

---

## 2. Environmental Object Definition

```
Environmental Object:   [Describe the specific environmental object]
Object Type:            [e.g., Land parcel / Infrastructure / Ecosystem / Dataset]
Location:               [Geographic specificity]
Time Reference:          [Temporal specificity]
Data Source:             [Primary data source(s)]
```

**Purpose:** Establishes what real environmental thing the judgment is about.

---

## 3. Test Input

```
Judgment Question:
[Write the specific judgment question for this scenario]

Context:
[Describe the environmental situation that triggers the judgment question.
Include relevant background, constraints, and known data.]

Available Evidence:
- [Evidence item 1]: [Description, source, date, reliability level]
- [Evidence item 2]: [Description, source, date, reliability level]
- [Evidence item N]: [Description, source, date, reliability level]

Known Gaps:
- [Any evidence that is known to be missing, unverified, or disputed]
```

---

## 4. Expected Human-Readable Output

```
Judgment Recommendation:
[What the ClimateOS Foundation recommends, in plain language.
Not code, not structured data — a human-readable conclusion.]

Reasoning Trace:
[Step-by-step explanation of how the Foundation arrived at the recommendation.
Each step should be traceable back to the Evidence Notes section.]

Evidence Chain:
Observation → [Observation description]
    → Inference → [Inference description]
    → Evidence → [Evidence description]
    → Claim → [Claim description]
    → Recommendation → [Recommendation description]

Confidence Level:
[Assigned confidence level with justification]
[Confidence type: evidence-based / assumption-based / mixed]

Limitations and Conditions:
[Any conditions under which the recommendation would change]
[Any known limitations of the evidence base]
```

---

## 5. Evidence Notes

```
Evidence Assessment:

Raw Data vs. Observation:
[Can the reviewer distinguish raw data from the observation?
Yes / Partially / No / Not Applicable]
[Notes: ...]

Observation vs. Inference:
[Can the reviewer distinguish the observation from the inference drawn from it?
Yes / Partially / No / Not Applicable]
[Notes: ...]

Inference vs. Evidence:
[Can the reviewer distinguish inference from the evidence used to support the claim?
Yes / Partially / No / Not Applicable]
[Notes: ...]

Evidence vs. Claim:
[Can the reviewer trace the evidence to the specific claim being made?
Yes / Partially / No / Not Applicable]
[Notes: ...]

Claim vs. Recommendation:
[Can the reviewer trace the claim to the specific recommendation?
Yes / Partially / No / Not Applicable]
[Notes: ...]

Missing Evidence:
[List any evidence links that are missing, assumed, or unverified]

Evidence Sufficiency Rating:
[Green: All evidence links traceable]
[Amber: Some evidence links missing or assumed, but bounded]
[Red: Critical evidence links missing or unrecoverable]
```

---

## 6. Validation Notes

```
Validation Assessment:

Source Reliability:
[Does the evidence come from a reliable source?
Rate: High / Medium / Low / Unknown]
[Notes: ...]

Time Validity:
[Is the evidence current enough for the judgment being made?
Rate: Valid / Partially Valid / Outdated / Unknown]
[Notes: ...]

Spatial Fit:
[Does the evidence cover the specific environmental object?
Rate: Good Fit / Partial Fit / Poor Fit / Unknown]
[Notes: ...]

Conflicting Evidence:
[Are there conflicting signals in the evidence?
Yes / No]
[If yes: Describe the conflict and how it was addressed]

Confidence Assessment:
[What confidence level is assigned to the judgment?
Confidence Level: High / Medium / Low / Indeterminate]
[Confidence Basis: evidence-based / assumption-based / mixed]

Human Review Required:
[Is human review required before action?
Yes / No / Conditional]
[If yes or conditional: Describe what human review is required and by whom]
```

---

## 7. Governance Boundary Notes

```
Governance Assessment:

Review Boundary:
[Who can review this judgment?]
[What is the review process?]

Approval Boundary:
[Who can approve this judgment leading to action?]
[What approvals are required before action is taken?]

Action Boundary:
[What action is authorized by this judgment?]
[What action is explicitly outside the governance boundary?]

Accountability Chain:
[Name of responsible party 1] → [Action they are accountable for]
[Name of responsible party 2] → [Action they are accountable for]
[Name of responsible party N] → [Action they are accountable for]

Governance Completeness:
[Green: Governance boundary fully defined]
[Amber: Governance boundary partially defined, some gaps]
[Red: Governance boundary not defined]
```

---

## 8. Responsibility Boundary Notes

```
Responsibility Assessment:

Responsible Party:
[Who is the primary responsible party for this judgment?]
[What is their authority to make or recommend this judgment?]

Responsibility Scope:
[What is this party responsible for?]
[What is explicitly outside their responsibility?]

Responsibility Evidence:
[Is the responsibility assignment documented?]
[Is it traceable to a governance record?]

Responsibility Boundary Clarity:
[Green: Responsibility is clearly assigned and documented]
[Amber: Responsibility is assigned but documentation is incomplete]
[Red: No responsible party identified]
```

---

## 9. Confidence Notes

```
Confidence Assessment:

Confidence Level Assigned:
[High / Medium / Low / Indeterminate]

Confidence Basis:
[Evidence-based: confidence derived from validated evidence]
[Assumption-based: confidence derived from assumptions where evidence is lacking]
[Mixed: some evidence-based, some assumption-based]

Confidence Boundary:
[What confidence level is required for this type of judgment?]
[Does the assigned confidence meet the required threshold?]

Confidence Communication:
[Is the confidence level communicated clearly to the responsible party?]
[Is the confidence boundary (evidence-based vs. assumption-based) explicit?]

Confidence Update Process:
[How should confidence be updated if new evidence becomes available?]
[Who is responsible for updating confidence?]
```

---

## 10. Runtime Inheritance Notes

```
Inheritance Assessment:

Domain-Agnostic Pattern:
[Can this judgment logic be applied in a different domain runtime?
Yes / No / Partially]
[Notes: ...]

Foundation Layer Coverage:
[Observation Layer: covered / not covered / partial]
[Evidence Layer: covered / not covered / partial]
[Validation Layer: covered / not covered / partial]
[Governance Layer: covered / not covered / partial]

Inheritance Path:
[CarbonOS: Can inherit? Yes / No / Requires adaptation]
[WaterOS: Can inherit? Yes / No / Requires adaptation]
[EnergyOS: Can inherit? Yes / No / Requires adaptation]
[BuildingOS: Can inherit? Yes / No / Requires adaptation]

Adaptation Required:
[If adaptation is required for any domain, describe what changes are needed]
```

---

## 11. Scenario Evaluation Record

```
Summary Assessment:

Reality Test:       [PASS / BOUNDED FAIL / FAIL]
Evidence Test:      [PASS / BOUNDED FAIL / FAIL]
Validation Test:    [PASS / BOUNDED FAIL / FAIL]
Governance Test:    [PASS / BOUNDED FAIL / FAIL]
Inheritance Test:   [PASS / BOUNDED FAIL / FAIL]

Overall Scenario Result: [PASS / BOUNDED FAIL / FAIL]

Bounded Failures (if any):
[Bounded failure 1: description and remediation path]
[Bounded failure 2: description and remediation path]

Gaps Requiring Future Work:
[Gap 1: description]
[Gap 2: description]

Reviewer Notes:
[Free-text notes from the reviewer on the overall quality of the scenario evaluation]

Reviewed by:    [Name]
Date:           [YYYY-MM-DD]
Signature:      [Optional]
```

---

## Example: Completed Evaluation (CarbonOS-01 — Abbreviated)

```
Scenario ID:        CarbonOS-01
Scenario Title:     Carbon Claim / ESG Disclosure
Domain:             CarbonOS
Judgment Type:      Disclosure readiness assessment
Complexity:         Medium
Reviewer:           Task101 Reviewer
Review Date:        2026-07-04
ClimateOS Version:  Task100 Frozen Foundation

---

Environmental Object:
A 500-hectare rural land parcel in the Riverina region, NSW.
Registered as a carbon sequestration project under the Australian Carbon
Credit Unit (ACCU) scheme. Vegetation type: mixed native forest.

---

Judgment Question:
Is the carbon sequestration claim of 10,000 tCO2e/year sufficiently
evidenced, validated, and governed for a responsible party to issue
an ESG disclosure?

---

Evidence Notes:
Evidence Sufficiency Rating: Amber
[Some measurement methodology details are assumed; additional
monitoring data would strengthen the evidence chain]

Validation Notes:
Human Review Required: Yes
[The confidence level is medium; a responsible party with domain
expertise must review before the disclosure is issued]

Governance Boundary:
Approval Authority: [Named party redacted pending governance definition]
[Governance boundary partially defined; review committee structure
not yet documented]

Overall Scenario Result: BOUNDED FAIL
[Bounded failure: governance boundary documentation incomplete.
Remediation path: document review committee structure and approval
authority before proceeding with ESG disclosure]
```

---

## Completing the Template

1. **Copy this template** for each scenario evaluation
2. **Complete all sections** — partial completion is itself a bounded failure worth noting
3. **Apply the Pass/Fail Decision Model** at the end (see `PASS_FAIL_DECISION_MODEL.md`)
4. **Do not skip sections** — skipping a section does not mean it passes; it means the evidence is insufficient
5. **Be explicit** — if something is unknown, write "Unknown" and note the implication; do not assume

## Related Documents

- `TASK101_HUMAN_USE_GRADUATION_TEST_SUITE.md` — test suite overview
- `TEST_SCENARIO_CATALOG.md` — scenario descriptions
- `PASS_FAIL_DECISION_MODEL.md` — pass/fail decision model

## Status

Draft in progress.
