# Task101 Pass/Fail Decision Model

## Purpose

This document defines the decision criteria and thresholds for determining whether the frozen ClimateOS Foundation passes the Human Use Graduation Test Suite.

## Action Authority Boundary

**A Task101 recommendation is not an action authority.**

It may identify a possible next step, review requirement, or decision option, but it cannot authorize:
- implementation
- approval
- construction
- investment
- compliance declaration
- public claim
- operational action

or any other action without the required human, expert, or governance approval.

This boundary is absolute and applies to every recommendation in every test suite output, regardless of outcome category.

## Evidence Discipline Definitions

These terms are used precisely throughout the decision model. They must not be conflated:

| Term | Definition |
|------|------------|
| **Raw data** | Unprocessed sensor outputs, survey results, field measurements, or third-party data records. Raw data has not been interpreted, filtered, or validated for governance use. |
| **Observation** | A human-readable record or reading derived from raw data, selected and formatted for governance context. An observation is a selected statement of what was measured or recorded. |
| **Inference** | A reasoned interpretation of one or more observations. An inference connects observations to a provisional meaning or implication. It is not a verified conclusion. |
| **Evidence** | An observation or set of observations sufficient in quality, provenance, and relevance to support a specific governance claim. Evidence is evidence *for* a claim; it is not the claim itself. |
| **Claim** | A specific, reviewable assertion put forward for governance evaluation. A claim requires evidence. A claim is not an observation or an inference dressed as fact. |
| **Recommendation** | A suggested next step, review action, or decision option. A recommendation identifies a possible path; it does not authorize, approve, or commit any party to action. |

## Expert Review Triggers

The test suite must escalate to qualified human experts — not rely on general ClimateOS review — when the scenario involves any of the following. Expert review is a governance requirement, not an optional enhancement:

- **High uncertainty**: confidence cannot be reliably bounded with available data
- **Conflicting evidence**: multiple credible sources yield contradictory observations
- **Low confidence**: any judgment rated below the minimum confidence threshold for the scenario
- **Missing critical data**: required evidence types are absent or known to be incomplete
- **Regulatory consequence**: the scenario output bears on a regulatory obligation or compliance determination
- **Engineering consequence**: the scenario output bears on structural, hydrological, geotechnical, or similar technical design
- **Safety consequence**: the scenario output bears on occupational, public, or environmental safety
- **Insurance consequence**: the scenario output may affect insurance coverage, liability, or indemnity positions
- **Legal consequence**: the scenario output may affect legal rights, obligations, or proceedings
- **Financial consequence**: the scenario output bears on material investment, expenditure, or financial disclosure
- **Public-impact consequence**: the scenario output may affect public health, safety, or community interest
- **Irreversible or high-cost project action**: the scenario involves construction, land use change, infrastructure deployment, or similar action that is costly or impractical to reverse
- **Domain-specific technical judgment**: the scenario requires specialist knowledge beyond what general ClimateOS review can reasonably assess (e.g., carbon accounting methodology, stormwater modelling, building code compliance, satellite data calibration)

When any trigger is present, the test output must:
1. Explicitly flag the trigger(s) activated
2. State that expert review is required before the governance output can be used
3. Identify the type of expert required (domain, qualification level)
4. Not present the governance output as sufficient for decision

## Decision Framework

The pass/fail decision follows a multi-level assessment:

1. **Individual Test Assessment**: Each of the five Task100 graduation checks
2. **Criteria Assessment**: Each of the seven test criteria
3. **Scenario Assessment**: Each of the five scenarios
4. **Overall Assessment**: Combined test suite result

---

## Level 1: Individual Test Assessment

### Reality Test Decision

**Criterion**: Can claims be traced to observable reality?

**Pass Threshold**: 100% of claims in the scenario have traceable paths to real-world references.

**Decision Matrix**:

| Condition | Result |
|-----------|--------|
| 100% claims traceable | PASS |
| 90–99% claims traceable | CONDITIONAL (document gaps) |
| <90% claims traceable | FAIL |

**Required Evidence**:
- Traceability path documented for each claim
- Human verification completed
- Gaps identified and documented (if any)

### Evidence Test Decision

**Criterion**: Are evidence sufficiency guidelines defined and human-executable?

**Pass Threshold**: Evidence sufficiency guidelines exist for all claim types and are executable by human reviewers without automated tools.

**Decision Matrix**:

| Condition | Result |
|-----------|--------|
| Guidelines exist for all claim types | PASS |
| Guidelines exist for >80% of claim types | CONDITIONAL |
| Guidelines exist for ≤80% of claim types | FAIL |

**Required Evidence**:
- Sufficiency guidelines documented
- Human-executable without specialized tools
- Gap analysis completed

### Validation Test Decision

**Criterion**: Can human reviewers conduct structured reviews?

**Pass Threshold**: Review workflows are documented, human-executable, and produce clear outputs.

**Decision Matrix**:

| Condition | Result |
|-----------|--------|
| All workflows human-executable | PASS |
| >80% workflows human-executable | CONDITIONAL |
| ≤80% workflows human-executable | FAIL |

**Required Evidence**:
- Review workflow documentation
- Human-executor verification
- Output format defined

### Governance Test Decision

**Criterion**: Are responsibility boundaries clearly defined?

**Pass Threshold**: 100% of decision points have assigned responsible parties with documented accountability.

**Decision Matrix**:

| Condition | Result |
|-----------|--------|
| 100% decision points assigned | PASS |
| 90–99% decision points assigned | CONDITIONAL (document gaps) |
| <90% decision points assigned | FAIL |

**Required Evidence**:
- Responsibility assignment matrix
- Accountability mechanisms documented
- Escalation paths defined

### Inheritance Test Decision

**Criterion**: Can future runtimes inherit Foundation capabilities?

**Pass Threshold**: All scenario elements map to Foundation capabilities with documented inheritance paths.

**Decision Matrix**:

| Condition | Result |
|-----------|--------|
| 100% elements mapped | PASS |
| 90–99% elements mapped | CONDITIONAL (document gaps) |
| <90% elements mapped | FAIL |

**Required Evidence**:
- Capability mapping documentation
- Inheritance path verification
- Gap analysis completed

---

## Level 2: Criteria Assessment

### Criterion 1: Human Readability

**Threshold**: Human reviewers can understand 90% of governance terms without external references.

**Assessment Method**: Terminology review by human non-specialist

**Decision**:
- ≥90% understood → PASS
- 80–89% understood → CONDITIONAL
- <80% understood → FAIL

### Criterion 2: Evidence Sufficiency

**Threshold**: Evidence sufficiency guidelines exist for all scenario types.

**Assessment Method**: Guidelines completeness check

**Decision**:
- All scenario types covered → PASS
- >80% scenario types covered → CONDITIONAL
- ≤80% scenario types covered → FAIL

### Criterion 3: Responsibility Boundary

**Threshold**: Every decision point has an assigned human responsible party.

**Assessment Method**: Responsibility matrix review

**Decision**:
- 100% decision points assigned → PASS
- 90–99% assigned → CONDITIONAL
- <90% assigned → FAIL

### Criterion 4: Review Boundary

**Threshold**: Each review has explicit scope, criteria, and limitations.

**Assessment Method**: Review scope documentation check

**Decision**:
- All reviews have explicit boundaries → PASS
- >80% reviews have explicit boundaries → CONDITIONAL
- ≤80% reviews have explicit boundaries → FAIL

### Criterion 5: Confidence Boundary

**Threshold**: Every judgment includes an explicit confidence assessment.

**Assessment Method**: Confidence assessment presence check

**Decision**:
- All judgments have confidence assessment → PASS
- >80% judgments have confidence assessment → CONDITIONAL
- ≤80% judgments have confidence assessment → FAIL

### Criterion 6: Pass/Fail Decision

**Threshold**: Pass/fail criteria are defined for each scenario.

**Assessment Method**: Criteria definition completeness check

**Decision**:
- All scenarios have pass/fail criteria → PASS
- >80% scenarios have criteria → CONDITIONAL
- ≤80% scenarios have criteria → FAIL

### Criterion 7: Runtime Inheritance Mapping

**Threshold**: Each scenario maps to Foundation capabilities.

**Assessment Method**: Inheritance mapping completeness check

**Decision**:
- All scenarios have mapping → PASS
- >80% scenarios have mapping → CONDITIONAL
- ≤80% scenarios have mapping → FAIL

---

## Level 3: Scenario Assessment

### Scenario Pass Requirements

A scenario is **governance-ready** if:

1. All five Task100 graduation checks pass (or conditional with documented gaps)
2. All seven criteria meet pass thresholds (or conditional with documented gaps)
3. Human judgment is documented for all required decision points
4. Expert review triggers are flagged where applicable

### Scenario Fail Triggers

A scenario is **failed / unsafe** if ANY of the following:

1. Reality Test fails (<90% claims traceable)
2. Evidence Test fails (≤80% claim types covered)
3. Validation Test fails (≤80% workflows human-executable)
4. Governance Test fails (<90% decision points assigned)
5. Inheritance Test fails (<90% elements mapped)
6. Any criterion fails (<80% threshold)
7. Human readability falls below 80%

### Scenario Conditional Triggers

A scenario is **partially usable** if:

1. Any test is conditional (not failing)
2. Any criterion is conditional
3. Human judgment is incomplete
4. Expert review triggers are present but not flagged

---

## Level 4: Overall Assessment

### Outcome Category Definitions

The test suite uses four practical outcome categories:

| Category | Definition |
|----------|------------|
| **readable** | All governance terms are defined in plain language and the document structure is navigable by a non-specialist human reviewer without external references. Human readability is satisfied. |
| **partially usable** | The governance output is structurally sound and has some actionable content, but has gaps — such as missing evidence sufficiency guidelines, undefined responsibility assignments, or incomplete confidence assessments — that require remediation before it can support a governance decision. |
| **governance-ready** | The governance output passes all applicable checks: evidence sufficiency is defined, responsibility boundaries are assigned, confidence is assessed, review scope is explicit, expert review triggers are documented where applicable, and no required element is missing. The output is ready for human expert review and governance decision. |
| **failed / unsafe** | The governance output has fundamental gaps — missing evidence requirements, undefined responsibility boundaries, absent confidence assessments, or any condition that means the output could be used to support a governance decision that is not adequately supported. It must not be used for governance purposes until remediated. |

### Mapping from Earlier Framing

| Previous Category | New Category |
|-------------------|-------------|
| PASS (all checks + all criteria) | governance-ready |
| CONDITIONAL (partial completion) | partially usable |
| FAIL (significant gaps) | failed / unsafe |
| — | readable: prerequisite state; a governance-ready output is also readable |

### Overall Pass Requirements

The test suite achieves **governance-ready** if:

1. All five scenarios are governance-ready, AND
2. Expert review triggers are documented for all applicable scenarios, AND
3. No scenario is failed / unsafe

The test suite is **partially usable** if:

1. All five scenarios are governance-ready or partially usable, AND
2. No scenario is failed / unsafe, AND
3. Gaps are documented with remediation paths

The test suite is **failed / unsafe** if ANY of the following:

1. Three or more scenarios have fundamental gaps
2. Any scenario is failed / unsafe AND one other scenario is partially usable
3. Reality Test fails in two or more scenarios
4. Evidence Test fails in two or more scenarios
5. Human judgment cannot be documented for three or more scenarios

---

## Decision Tree

```
START: Test Suite Execution
│
├── Execute Individual Tests
│   ├── Reality Test
│   ├── Evidence Test
│   ├── Validation Test
│   ├── Governance Test
│   └── Inheritance Test
│
├── Assess Criteria
│   ├── Human Readability
│   ├── Evidence Sufficiency
│   ├── Responsibility Boundary
│   ├── Review Boundary
│   ├── Confidence Boundary
│   ├── Pass/Fail Decision
│   └── Runtime Inheritance
│
├── Evaluate Scenario Results
│   ├── CarbonOS: governance-ready / partially usable / failed / unsafe
│   ├── WaterOS: governance-ready / partially usable / failed / unsafe
│   ├── EnergyOS: governance-ready / partially usable / failed / unsafe
│   ├── BuildingOS: governance-ready / partially usable / failed / unsafe
│   └── Climate Data: governance-ready / partially usable / failed / unsafe
│
└── Determine Overall Result
    │
    ├── ALL 5 SCENARIOS governance-ready → GRADUATION: PASS
    │
    ├── 4 governance-ready + 1 partially usable → GRADUATION: CONDITIONAL
    │
    ├── Any partially usable (no failed/unsafe) → GRADUATION: partially usable
    │
    ├── ≥1 failed / unsafe → GRADUATION: failed / unsafe
    │
    └── 3+ failed / unsafe → GRADUATION: failed / unsafe (significant gaps)
```

---

## Remediation Paths

### For Partially Usable Results

| Gap Type | Remediation Action | Timeline |
|----------|-------------------|----------|
| Traceability gaps | Document additional evidence paths | 5 business days |
| Sufficiency guidelines missing | Develop guidelines per claim type | 10 business days |
| Responsibility gaps | Assign responsible parties | 3 business days |
| Review boundary gaps | Define review scope | 5 business days |
| Confidence gaps | Add confidence assessments | 3 business days |
| Inheritance gaps | Complete Foundation mapping | 10 business days |
| Expert trigger not flagged | Document applicable triggers and required expert type | 3 business days |

### For Failed / Unsafe Results

| Fail Type | Remediation Action | Prerequisite |
|-----------|-------------------|--------------|
| Reality Test failure | Re-evaluate Foundation observation capability | Review Task100 Observation Layer |
| Evidence Test failure | Enhance evidence sufficiency guidelines | Review Task100 Evidence Layer |
| Validation Test failure | Redesign review workflows | Review Task100 Review Layer |
| Governance Test failure | Clarify responsibility assignments | Review Task100 Governance Layer |
| Inheritance Test failure | Strengthen inheritance documentation | Review Task100 Foundation Review |

---

## Outcome Summary Matrix

| Decision Level | readable | partially usable | governance-ready | failed / unsafe |
|----------------|----------|-----------------|-----------------|-----------------|
| Reality Test | N/A | 90–99% traceable | 100% traceable | <90% traceable |
| Evidence Test | N/A | >80% guidelines | 100% guidelines + sufficiency explicit | ≤80% guidelines |
| Validation Test | N/A | >80% human-executable | 100% human-executable + complete | ≤80% human-executable |
| Governance Test | N/A | 90–99% assigned | 100% assigned + explicit boundaries | <90% assigned |
| Inheritance Test | N/A | 90–99% mapped | 100% mapped + documented | <90% mapped |
| Criteria | N/A | >80% pass | All criteria defined + met | ≤80% pass |
| Scenario | Structure sound | Some gaps; no unsafe gaps | All checks pass | Any fundamental gap |
| Overall | Prerequisite | Gaps present; no unsafe | All 5 scenarios governance-ready | ≥1 fundamental gap |

---

## Final Graduation Decision

### Decision Categories

**GRADUATION: PASS — governance-ready**
- All five scenarios are governance-ready (all checks and criteria met)
- Human judgment documented for all required points
- Expert review triggers are flagged where applicable
- No failed / unsafe scenario
- No remediation required

**GRADUATION: CONDITIONAL — partially usable**
- All five scenarios are governance-ready or partially usable
- Human judgment documented with gaps
- No failed / unsafe scenario
- Remediation path defined for all partially usable items

**GRADUATION: FAIL — failed / unsafe**
- One or more scenarios is failed / unsafe
- Fundamental gaps in Foundation capability
- Remediation required before re-testing

### Decision Attestation

```markdown
## Graduation Decision Attestation

### Test Execution Summary
- Tests Executed: [Number]
- Tests Passed: [Number]
- Tests Conditional: [Number]
- Tests Failed: [Number]

### Scenario Results
- CarbonOS: [governance-ready / partially usable / failed / unsafe]
- WaterOS: [governance-ready / partially usable / failed / unsafe]
- EnergyOS: [governance-ready / partially usable / failed / unsafe]
- BuildingOS: [governance-ready / partially usable / failed / unsafe]
- Climate Data: [governance-ready / partially usable / failed / unsafe]

### Expert Review Triggers Flagged
- [List scenarios and which triggers were activated]

### Human Judgment Summary
- Judgment Points: [Number]
- Judgment Documented: [Number]
- Gaps: [Description if any]

### GRADUATION DECISION: [governance-ready / partially usable / failed / unsafe]

### Action Authority Statement
A Task101 recommendation is not an action authority.
It may identify a possible next step, review requirement, or decision option,
but it cannot authorize implementation, approval, construction, investment,
compliance declaration, public claim, or operational action without the
required human, expert, or governance approval.

### Rationale:
[Document the reasoning for the decision]

### Attested By:
- Human Reviewer: [Name/Role]
- Date: [YYYY-MM-DD]
- Signature: [Signature or attestation statement]
```

---

## References

- [Human Use Graduation Test Suite](TASK101_HUMAN_USE_GRADUATION_TEST_SUITE.md)
- [Test Scenario Catalog](TEST_SCENARIO_CATALOG.md)
- [Test Input/Output Template](TEST_INPUT_OUTPUT_TEMPLATE.md)
- [Task101 Completion Review](TASK101_COMPLETION_REVIEW.md)

---

**Status**: Draft  
**Authority**: Task101 - QCLAW Builder  
**Date**: 2026-07-04
