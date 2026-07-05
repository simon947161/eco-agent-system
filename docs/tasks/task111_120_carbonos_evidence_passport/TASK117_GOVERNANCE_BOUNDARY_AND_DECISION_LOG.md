# Task117 Governance Boundary and Decision Log Model

## Purpose

Task117 defines a documentation-only decision log model that records responsibility, boundary, and non-authority status for CarbonOS Evidence Passport reviews.

The decision log is a **documentation concept only**. It is not a database, not an API, not a runtime object, not a compliance engine, and not an assurance engine. It is a structured record that a human reviewer creates and maintains as part of the Evidence Passport.

## Governance Boundary Model

The governance boundary model prevents the Evidence Passport from being mistaken for authority, certification, assurance, compliance approval, investment advice, or operational instruction.

### Responsibility Roles (Expanded from Task106)

| Role | Responsibility | Owns | Does NOT Own |
|------|----------------|------|--------------|
| **Data provider** | Supplies source data and provenance | Source data accuracy (within source scope) | Proving claims beyond source scope |
| **Claim owner** | States the claim and intended use | Claim text and intended use | Independent validation unless separately assigned |
| **Intake preparer** | Completes the intake record | Intake record accuracy | Evidence sufficiency assessment |
| **Evidence bundle assembler** | Groups evidence by type; documents provenance and gaps | Bundle structure and completeness | Evidence sufficiency determination |
| **Human reviewer** | Separates evidence, inference, claim, recommendation; assesses sufficiency | Review record and recommendation | Final approval or expert certification |
| **Expert reviewer** | Reviews technical, accounting, legal, or regulatory issues within assigned scope | Expert judgment within assigned scope | Governance decision unless formally authorized |
| **Governance authority** | Makes approved decisions within formal mandate | Decision within mandate | Replacing evidence requirements |
| **CarbonOS / ClimateOS document** | Structures review and identifies gaps | Passport structure and traceability | Authorizing action, disclosure, compliance, investment, or implementation |

### Boundary Rules (Expanded from Task106)

1. A claim owner owns the claim text and intended use — not the evidence sufficiency
2. A reviewer owns the review record and recommendation — not the truth of the underlying world
3. An expert owns expert judgment within the assigned scope — not the governance decision
4. A governance authority owns decisions only within its formal mandate — not outside it
5. CarbonOS / ClimateOS documents support traceable review — not final authority
6. A recommendation is never an authorization — it identifies a possible path, not an approved action

## Decision Log Model (Documentation-Only)

The decision log is a section of the Evidence Passport that records review steps and outcomes.

### Decision Log Structure

```markdown
# Decision Log — Evidence Passport: [Claim ID]

## Log Metadata
- Passport ID: [references passport]
- Claim ID: [references claim intake record]
- Log Started By: [human reviewer name/role]
- Log Start Date: [YYYY-MM-DD]

## Review Steps Recorded

### Step 1: Intake
- Date: [YYYY-MM-DD]
- Completed By: [name/role]
- Claim confirmed: [yes/no]
- Early triggers flagged: [list]
- Responsibility assigned: [yes/no]

### Step 2: Evidence Bundle Assembly
- Date: [YYYY-MM-DD]
- Completed By: [name/role]
- Evidence types addressed: [list]
- Conflicts logged: [yes/no — describe]
- Gaps logged: [yes/no — describe]

### Step 3: Evidence Sufficiency Assessment
- Date: [YYYY-MM-DD]
- Completed By: [name/role]
- Dimensions assessed: [list]
- Preliminary recommendation: [proceed / request data / escalate / do not use]

### Step 4: Expert Review Trigger Check
- Date: [YYYY-MM-DD]
- Completed By: [name/role]
- Triggers assessed: [13 triggers checked]
- Triggers present: [list]
- Expert review required: [yes/no]
- Expert type identified: [list if yes]

### Step 5: Expert Review (If Triggered)
- Date: [YYYY-MM-DD]
- Expert Name/Role: [name/role]
- Scope of expert review: [describe]
- Expert opinion: [summary]
- Opinion attached: [yes/no — reference attachment]

### Step 6: Governance Boundary Check
- Date: [YYYY-MM-DD]
- Completed By: [name/role]
- Responsibility assigned: [yes/no — reference assignment]
- Action-authority boundary stated: [yes/no — reference statement]
- Recommendations separated from decisions: [yes/no]

### Step 7: Decision / Recommendation
- Date: [YYYY-MM-DD]
- Decision By: [name/role]
- Decision: [proceed / request data / expert review / do not use / escalate]
- Rationale: [evidence sufficiency, trigger flags, confidence]
- Approvals still required: [list human, expert, governance approvals]
- Action-authority boundary restated: [what this decision does and does not authorize]

## Decision Log Status
- Log Complete: [yes/no]
- Passport Ready for Governance Decision: [yes/no — conditional on expert review if triggered]
- Governance Authority Approval Still Required: [yes/no — list authority type]

## Signatures / Attestations
[Human-readable attestation statements. Not electronic signatures or legal signatures.]

- Intake preparer attestation: [name, role, date]
- Reviewer attestation: [name, role, date]
- Expert attestation (if applicable): [name, role, date, scope]
- Governance authority attestation (if applicable): [name, role, date, decision]
```

## Decision Log Discipline Requirements

The decision log must maintain evidence discipline and governance boundaries:

| Term | Requirement in Decision Log |
|------|----------------------------|
| Raw data | Referenced in Step 2; not presented as evidence |
| Observation | Referenced in Step 2; clearly separated from inference |
| Inference | Labelled in Step 2; not a claim or conclusion |
| Evidence | Assessed in Step 3; sufficiency is "for this claim" |
| Claim | Referenced from intake; not restated without discipline |
| Recommendation | Recorded in Step 7; explicitly not an authorization |

## Decision Log and Governance Boundary

The decision log records **recommendations and decisions** but always maintains the governance boundary:

### Recommendation (from reviewer)
- Identifies a possible next step, review requirement, or decision option
- Does NOT authorize implementation, approval, construction, investment, compliance declaration, public claim, or operational action
- Must be followed by required human, expert, or governance approval before any action

### Decision (from governance authority)
- Is a decision within formal mandate only
- Does NOT replace evidence requirements
- Does NOT eliminate the need for further approvals if required
- Must reference the action-authority boundary

### Governance Authority Decision Recorded in Log
```markdown
## Governance Authority Decision (if applicable)

- Authority Name/Role: [name/role]
- Decision Date: [YYYY-MM-DD]
- Decision: [proceed / request data / do not use / escalate]
- Authority Scope: [formal mandate within which this decision is made]
- Conditions: [any conditions attached to the decision]
- Further Approvals Required: [list any approvals still needed]
- Action-Authority Boundary: This decision is within [Authority] mandate for [scope].
  It does not authorize [actions outside mandate]. Further approvals required for:
  [list].
```

## What the Decision Log Is and Is Not

| The decision log **is** | The decision log **is not** |
|------------------------|---------------------------|
| A documentation record of review steps | A compliance determination |
| A record of responsibility assignment | An assurance opinion |
| A record of governance boundaries | A certification |
| A record of recommendations and decisions | An authorization (unless made by governance authority within mandate) |
| A traceability tool for governance review | A public disclosure document (unless reviewed) |
| A structured way to maintain evidence discipline | An automated decision |

## Task102-110 Relationship

Task117 expands:

| Task102-110 Deliverable | Expansion in Task117 |
|------------------------|-----------------------|
| Task106 Responsibility Boundary Model | Expanded into full governance boundary model with 8 roles |
| Task107 Pilot Review Record | Adapted as decision log structure |
| Task102-110 action-authority boundary | Preserved and expanded in decision log |

## Decision Log Model Success Criteria

The model is successful if:

1. A human reviewer can complete the log without software
2. Governance boundaries are explicit at each step
3. Responsibility is assigned and recorded
4. Recommendations are clearly separated from decisions
5. The action-authority boundary is maintained throughout
6. The log is clearly documentation-only

## Task117 Status

```text
Task117: COMPLETE — Governance Boundary and Decision Log Model defined.
```

Task118 may proceed (define pilot case selection protocol).

---

**Status**: Draft  
**Authority**: Task111-120 - QCloud Builder  
**Date**: 2026-07-05
