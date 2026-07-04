# Task101 Test Input/Output Template

## Purpose

This document provides a standardized template for executing human use graduation tests across all five scenarios.

## Template Structure

Each scenario test follows the same structure:

1. **Test Input**: Required inputs for the scenario test
2. **Test Execution**: Step-by-step test execution protocol
3. **Test Output**: Standardized output format
4. **Test Assessment**: Pass/fail determination

---

## Test Input Specification

### Required Inputs for All Scenarios

| Input | Description | Source | Required |
|-------|-------------|--------|----------|
| Scenario Brief | Description of the environmental judgment context | Test Scenario Catalog | Yes |
| Foundation Reference | Relevant Foundation capability documentation | ClimateOS Core | Yes |
| Governance Framework | Responsibility and review boundary definitions | Task100 Freeze Record | Yes |
| Evidence Standard | Evidence sufficiency guidelines | Task100 Graduation Review | Yes |
| Confidence Protocol | Confidence boundary definitions | Task100 Graduation Review | Yes |

### Scenario-Specific Inputs

#### CarbonOS Scenario Inputs

| Input | Description | Source |
|-------|-------------|--------|
| Carbon Claim Description | Physical assets and scope boundary | Scenario Brief |
| Evidence Package | Carbon accounting records | Scenario Evidence |
| ESG Disclosure Context | Reporting framework and requirements | Scenario Brief |
| Stakeholder List | Decision-maker and reviewer assignments | Scenario Governance |

#### WaterOS Scenario Inputs

| Input | Description | Source |
|-------|-------------|--------|
| Development Description | Site and project scope | Scenario Brief |
| Stormwater Assessment | Drainage and risk evidence | Scenario Evidence |
| Municipal Requirements | Regulatory and policy context | Scenario Brief |
| Responsibility Assignment | Decision-maker and reviewer assignments | Scenario Governance |

#### EnergyOS Scenario Inputs

| Input | Description | Source |
|-------|-------------|--------|
| Project Proposal | Community energy project scope | Scenario Brief |
| Benefit Evidence | Community benefit documentation | Scenario Evidence |
| Environmental Impact | Impact assessment records | Scenario Evidence |
| Responsibility Assignment | Decision-maker and reviewer assignments | Scenario Governance |

#### BuildingOS Scenario Inputs

| Input | Description | Source |
|-------|-------------|--------|
| Module Proposal | Building module specifications | Scenario Brief |
| Safety Evidence | Safety assessment documentation | Scenario Evidence |
| Interface Documentation | Interoperability evidence | Scenario Evidence |
| Responsibility Assignment | Decision-maker and reviewer assignments | Scenario Governance |

#### Climate Data Scenario Inputs

| Input | Description | Source |
|-------|-------------|--------|
| Observation Sources | NASA/BOM data source descriptions | Scenario Brief |
| Data Provenance | Data lineage and attribution records | Scenario Evidence |
| Interpretation Claims | Proposed environmental conclusions | Scenario Brief |
| Responsibility Assignment | Decision-maker and reviewer assignments | Scenario Governance |

---

## Test Execution Protocol

### Phase 1: Input Validation

**Step 1.1**: Verify all required inputs are present
```
CHECKLIST:
[ ] Scenario Brief received
[ ] Foundation Reference available
[ ] Governance Framework accessible
[ ] Evidence Standard documented
[ ] Confidence Protocol defined
```

**Step 1.2**: Verify input completeness
```
CHECKLIST:
[ ] CarbonOS: All required inputs present
[ ] WaterOS: All required inputs present
[ ] EnergyOS: All required inputs present
[ ] BuildingOS: All required inputs present
[ ] Climate Data: All required inputs present
```

### Phase 2: Reality Test Execution

**Step 2.1**: Trace claims to observable reality
```
TEMPLATE:
Claim: [Extract claim from scenario]
Observable Reference: [Identify physical/measurable evidence]
Traceability Path: [Document the connection]
Human Verification: [Describe human verification method]
RESULT: TRACEABLE / NOT TRACEABLE / PARTIAL
```

**Step 2.2**: Verify evidence-to-reality connection
```
TEMPLATE:
Evidence: [Extract evidence from scenario]
Reality Anchor: [Identify real-world reference]
Connection Quality: [Document connection strength]
Human Assessment: [Describe human assessment method]
RESULT: CONNECTED / NOT CONNECTED / WEAK
```

### Phase 3: Evidence Test Execution

**Step 3.1**: Assess evidence sufficiency
```
TEMPLATE:
Claim: [State the claim requiring evidence]
Evidence Type: [Identify evidence category]
Sufficiency Standard: [Reference Foundation sufficiency guideline]
Evidence Quality: [Assess evidence against standard]
Human Sufficiency Assessment: [Document human judgment]
RESULT: SUFFICIENT / INSUFFICIENT / PARTIAL
```

**Step 3.2**: Verify evidence requirements
```
TEMPLATE:
Evidence Requirement: [State requirement from scenario]
Evidence Provided: [List evidence available]
Gap Analysis: [Identify any gaps]
Human Gap Assessment: [Document human judgment]
RESULT: MET / NOT MET / PARTIALLY MET
```

### Phase 4: Validation Test Execution

**Step 4.1**: Verify review workflow
```
TEMPLATE:
Review Type: [Identify review type]
Review Scope: [Define review boundaries]
Review Criteria: [List explicit criteria]
Human Reviewer: [Assign human reviewer]
RESULT: REVIEW DEFINED / NOT DEFINED / PARTIAL
```

**Step 4.2**: Validate review process
```
TEMPLATE:
Process Documented: [Yes/No]
Process Human-Executable: [Yes/No]
Process Repeatable: [Yes/No]
Output Defined: [Yes/No]
RESULT: VALID / INVALID / CONDITIONAL
```

### Phase 5: Governance Test Execution

**Step 5.1**: Verify responsibility assignment
```
TEMPLATE:
Decision Point: [Identify decision point]
Responsible Party: [Assign human/team]
Accountability Mechanism: [Define accountability method]
Escalation Path: [Document escalation process]
RESULT: ASSIGNED / NOT ASSIGNED / AMBIGUOUS
```

**Step 5.2**: Verify governance boundaries
```
TEMPLATE:
Boundary Type: [Identify boundary category]
Boundary Definition: [State explicit boundary]
Human Role: [Describe human involvement]
Limit Documentation: [Document limitations]
RESULT: DEFINED / NOT DEFINED / UNCLEAR
```

### Phase 6: Inheritance Test Execution

**Step 6.1**: Map to Foundation capabilities
```
TEMPLATE:
Scenario Element: [Identify scenario component]
Foundation Capability: [Reference Foundation layer]
Mapping Quality: [Assess mapping completeness]
Human Validation: [Document human judgment]
RESULT: MAPPED / NOT MAPPED / PARTIAL
```

**Step 6.2**: Verify inheritance paths
```
TEMPLATE:
Runtime Domain: [Identify domain (CarbonOS/WaterOS/etc)]
Foundation Inheritance: [List inherited capabilities]
Extension Points: [Document domain-specific additions]
Human Assessment: [Document human judgment]
RESULT: INHERITABLE / NOT INHERITABLE / PARTIAL
```

### Phase 7: Confidence Test Execution

**Step 7.1**: Verify confidence assessment
```
TEMPLATE:
Judgment: [State the environmental judgment]
Confidence Scale: [Reference explicit scale]
Confidence Factors: [List uncertainty factors]
Confidence Limitations: [Document explicit limits]
Human Confidence Assessment: [Document human judgment]
RESULT: ASSESSED / NOT ASSESSED / PARTIAL
```

**Step 7.2**: Verify revisability
```
TEMPLATE:
Revisability Mechanism: [Document process]
New Evidence Path: [Define evidence update method]
Human Role in Revision: [Describe human involvement]
RESULT: REVISABLE / NOT REVISABLE / UNCLEAR
```

---

## Test Output Specification

### Standard Output Format

```markdown
# Test Output: [Scenario Name]

## Test Metadata
- Test Date: [YYYY-MM-DD]
- Test Executor: [Human reviewer name/role]
- Scenario: [Scenario identifier]
- Foundation Reference: [Relevant Foundation docs]

## Reality Test Results
- Claim Traceability: [PASS/FAIL/PARTIAL]
- Evidence-to-Reality Connection: [PASS/FAIL/PARTIAL]
- Human Verification Method: [Description]

## Evidence Test Results
- Evidence Sufficiency: [PASS/FAIL/PARTIAL]
- Evidence Requirements Met: [PASS/FAIL/PARTIAL]
- Human Gap Assessment: [Description]

## Validation Test Results
- Review Workflow Defined: [PASS/FAIL/PARTIAL]
- Process Human-Executable: [PASS/FAIL/PARTIAL]
- Review Process Quality: [Description]

## Governance Test Results
- Responsibility Assigned: [PASS/FAIL/PARTIAL]
- Governance Boundaries Defined: [PASS/FAIL/PARTIAL]
- Human Role Clarity: [Description]

## Inheritance Test Results
- Foundation Capability Mapped: [PASS/FAIL/PARTIAL]
- Runtime Inheritance Valid: [PASS/FAIL/PARTIAL]
- Human Inheritance Assessment: [Description]

## Confidence Test Results
- Confidence Assessment Complete: [PASS/FAIL/PARTIAL]
- Revisability Mechanism Defined: [PASS/FAIL/PARTIAL]
- Human Confidence Judgment: [Description]

## Overall Scenario Result
- Reality Test: [PASS/FAIL]
- Evidence Test: [PASS/FAIL]
- Validation Test: [PASS/FAIL]
- Governance Test: [PASS/FAIL]
- Inheritance Test: [PASS/FAIL]
- SCENARIO GRADUATION: [PASS/FAIL/CONDITIONAL]
```

---

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

This boundary is absolute. It applies to every test output regardless of outcome category.

## Evidence Discipline Definitions

These terms are used precisely throughout the test suite:

| Term | Definition |
|------|------------|
| **Raw data** | Unprocessed sensor outputs, survey results, field measurements, or third-party data records. Not yet interpreted or validated for governance use. |
| **Observation** | A human-readable record or reading derived from raw data, selected and formatted for governance context. |
| **Inference** | A reasoned interpretation of one or more observations. Not a verified conclusion. |
| **Evidence** | An observation or set of observations sufficient in quality, provenance, and relevance to support a specific governance claim. |
| **Claim** | A specific, reviewable assertion put forward for governance evaluation. Requires evidence. |
| **Recommendation** | A suggested next step, review action, or decision option. Identifies a possible path; does not authorize action. |

## Expert Review Triggers

The template must flag expert review requirements when any of the following are present:

- High uncertainty: confidence cannot be reliably bounded
- Conflicting evidence: multiple credible sources yield contradictory observations
- Low confidence: judgment rated below minimum confidence threshold
- Missing critical data: required evidence types are absent or known incomplete
- Regulatory, engineering, safety, insurance, legal, financial, or public-impact consequence
- Irreversible or high-cost project action
- Domain-specific technical judgment beyond general ClimateOS review capacity

When any trigger is present, the test output must:
1. Flag the trigger(s) explicitly
2. State that expert review is required
3. Identify the type of expert required
4. Not present the output as sufficient for governance decision

## Test Assessment Matrix

### Outcome Category Matrix

| Category | Definition | Action Required |
|----------|------------|----------------|
| **readable** | All governance terms defined in plain language; navigable by non-specialist without external references | None (prerequisite satisfied) |
| **partially usable** | Structurally sound with some actionable content, but has gaps | Remediate gaps before governance use |
| **governance-ready** | Passes all checks: evidence sufficiency defined, responsibility assigned, confidence assessed, review scope explicit, expert triggers documented | Ready for human expert review |
| **failed / unsafe** | Fundamental gaps — missing evidence requirements, undefined boundaries, absent confidence assessments | Must not be used for governance; remediate first |

### Scenario Graduation Matrix

| Scenario | Reality | Evidence | Validation | Governance | Inheritance | Confidence | Expert Trigger Flag | Outcome Category |
|----------|---------|----------|------------|------------|-------------|------------|---------------------|-----------------|
| CarbonOS | Pass | Pass | Pass | Pass | Pass | Pass | [Flag if applicable] | [Category] |
| WaterOS | Pass | Pass | Pass | Pass | Pass | Pass | [Flag if applicable] | [Category] |
| EnergyOS | Pass | Pass | Pass | Pass | Pass | Pass | [Flag if applicable] | [Category] |
| BuildingOS | Pass | Pass | Pass | Pass | Pass | Pass | [Flag if applicable] | [Category] |
| Climate Data | Pass | Pass | Pass | Pass | Pass | Pass | [Flag if applicable] | [Category] |

### Outcome Determination

| Condition | Outcome Category |
|----------|------------------|
| All checks pass + expert triggers flagged or cleared | governance-ready |
| Some checks pass + gaps present | partially usable |
| Fundamental gaps present | failed / unsafe |
| Readability prerequisite not met | failed / unsafe |

---

## Human Judgment Documentation

### Required Human Judgment Points

For each test execution, document human judgment at these points:

1. **Claim Verification**: Human confirms claim traceability
2. **Evidence Quality**: Human assesses evidence sufficiency
3. **Review Execution**: Human conducts review workflow
4. **Responsibility Approval**: Human approves responsibility assignment
5. **Inheritance Validation**: Human validates Foundation mapping
6. **Confidence Assessment**: Human assigns confidence level

### Human Judgment Record Template

```markdown
## Human Judgment Record

### JJ-1: Claim Verification
- Human Reviewer: [Name/Role]
- Date: [YYYY-MM-DD]
- Judgment: [TRACEABLE/NOT TRACEABLE/PARTIAL]
- Rationale: [Document reasoning]

### JJ-2: Evidence Quality
- Human Reviewer: [Name/Role]
- Date: [YYYY-MM-DD]
- Judgment: [SUFFICIENT/INSUFFICIENT/PARTIAL]
- Rationale: [Document reasoning]

### JJ-3: Review Execution
- Human Reviewer: [Name/Role]
- Date: [YYYY-MM-DD]
- Judgment: [COMPLETED/NOT COMPLETED/PARTIAL]
- Rationale: [Document reasoning]

### JJ-4: Responsibility Approval
- Human Reviewer: [Name/Role]
- Date: [YYYY-MM-DD]
- Judgment: [APPROVED/NOT APPROVED/AMBIGUOUS]
- Rationale: [Document reasoning]

### JJ-5: Inheritance Validation
- Human Reviewer: [Name/Role]
- Date: [YYYY-MM-DD]
- Judgment: [VALID/INVALID/PARTIAL]
- Rationale: [Document reasoning]

### JJ-6: Confidence Assessment
- Human Reviewer: [Name/Role]
- Date: [YYYY-MM-DD]
- Confidence Level: [Scale 1-5]
- Rationale: [Document reasoning]
```

---

## References

- [Human Use Graduation Test Suite](TASK101_HUMAN_USE_GRADUATION_TEST_SUITE.md)
- [Test Scenario Catalog](TEST_SCENARIO_CATALOG.md)
- [Pass/Fail Decision Model](PASS_FAIL_DECISION_MODEL.md)

---

**Status**: Draft  
**Authority**: Task101 - QCLAW Builder  
**Date**: 2026-07-04
