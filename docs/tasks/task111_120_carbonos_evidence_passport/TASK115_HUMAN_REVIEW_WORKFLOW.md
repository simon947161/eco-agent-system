# Task115 Human Review Workflow for Carbon / ESG Claims

## Purpose

Task115 defines a manual, documentation-only review workflow for carbon and ESG claims.

The workflow is a **human review process**. It is not software, not an automated workflow, not a workflow engine, not an API, and not a runtime process. It defines the steps a human reviewer should follow when reviewing a carbon or ESG claim using the Evidence Passport structure.

## Workflow Overview

The workflow takes a carbon/ESG claim from intake through evidence review, sufficiency assessment, expert review triggering, and governance decision.

```text
Intake → Evidence Bundle Assembly → Sufficiency Assessment →
Expert Review Trigger Check → Expert Review (if triggered) →
Governance Boundary Check → Decision / Recommendation → Decision Log
```

## Workflow Steps (Documentation-Only)

### Step 1: Claim Intake

**Input**: Claim owner submits claim for review  
**Output**: Completed Claim Intake Record (Task113 template)

**Actions**:
1. Record claim statement (specific, reviewable assertion)
2. Record intended use (ESG disclosure / investor report / internal / other)
3. Identify available evidence sources
4. Flag known data gaps
5. Flag early expert review triggers
6. Assign initial responsibility
7. State governance boundary

**Evidence discipline**:
- Raw data: listed as sources only
- Observation: may be preliminary; marked as such
- Inference: marked as preliminary; not verified
- Evidence: not assessed at intake
- Claim: must be specific and reviewable
- Recommendation: next steps are recommendations; not authorizations

**Completion criteria**: Intake record complete; claim owner confirms claim statement

---

### Step 2: Evidence Bundle Assembly

**Input**: Completed intake record; evidence sources  
**Output**: Completed Evidence Bundle (Task114 structure)

**Actions**:
1. Group evidence by type (activity data, emission factors, boundary docs, third-party docs)
2. For each evidence item: record raw data reference, observation, provenance, gaps
3. Document calculation methods and emission factors used
4. Document organizational and operational boundary
5. Log conflicts and gaps explicitly
6. Assign bundle assembler

**Evidence discipline**:
- Raw data: referenced; not presented as evidence without processing
- Observation: clearly separated from inference
- Inference: labelled as provisional; not a claim or conclusion
- Evidence: grouped observations sufficient for the specific claim
- Claim: referenced from intake record
- Recommendation: not yet made

**Completion criteria**: All evidence types addressed; conflicts and gaps logged

---

### Step 3: Evidence Sufficiency Assessment

**Input**: Completed evidence bundle  
**Output**: Sufficiency assessment against defined criteria

**Assessment dimensions** (from Task105, expanded):

| Dimension | Review Question | Pass Criterion |
|-----------|-----------------|---------------|
| Provenance | Who produced the source, when, under what controls? | Known and documented for all critical evidence |
| Relevance | Does the evidence directly support the claim? | All claim elements have supporting evidence |
| Completeness | Are required periods, assets, scopes covered? | No material gaps in required scope |
| Method clarity | Are methods stated clearly enough for review? | Method documented; limitations stated |
| Conflict handling | Are contradictory sources disclosed? | All conflicts logged; resolution attempted or escalated |
| Human readability | Can a non-specialist understand the evidence? | Terms defined; structure navigable |

**Evidence discipline**:
- Evidence: assessed for sufficiency for the specific claim
- Claim: sufficiency is always "for this claim" — not general
- Recommendation: sufficiency assessment may lead to recommendation

**Completion criteria**: All dimensions assessed; preliminary recommendation formed

---

### Step 4: Expert Review Trigger Check

**Input**: Completed evidence bundle; sufficiency assessment; trigger matrix (Task116)  
**Output**: Trigger assessment; expert review required or not

**Trigger check procedure**:
1. Review the 13-trigger matrix (Task116)
2. For each trigger: assess whether present in this claim review
3. Document which triggers are present (if any)
4. If any trigger present: flag required expert type
5. If any trigger present: state that expert review is required
6. If any trigger present: do NOT present the passport as sufficient for governance decision

**Triggers** (expanded from Task101 and Task102-110):

| # | Trigger | CarbonOS Example |
|---|---------|-------------------|
| 1 | High uncertainty | Incomplete activity data for material emission source |
| 2 | Conflicting evidence | Two suppliers provide contradictory fuel records |
| 3 | Low confidence | Estimation methods used for >20% of emissions |
| 4 | Missing critical data | No meter data for a material facility |
| 5 | Regulatory consequence | Claim will be used in mandatory ESG disclosure |
| 6 | Engineering consequence | Claim involves engineered carbon removal project |
| 7 | Safety consequence | Claim involves industrial process safety data |
| 8 | Insurance consequence | Claim may affect environmental liability insurance |
| 9 | Legal consequence | Claim may affect climate-related litigation |
| 10 | Financial consequence | Claim will be used in investor-facing disclosure |
| 11 | Public-impact consequence | Claim will be used in public sustainability report |
| 12 | Irreversible or high-cost project action | Claim supports carbon removal project investment |
| 13 | Domain-specific technical judgment | Claim requires carbon accounting methodology review |

**Completion criteria**: All 13 triggers assessed; triggers present are flagged; expert type identified if required

---

### Step 5: Expert Review (If Triggered)

**Input**: Evidence bundle; sufficiency assessment; trigger flags  
**Output**: Expert review opinion; updated sufficiency assessment

**Expert review procedure**:
1. Identify required expert type from trigger assessment
2. Provide expert with evidence bundle and passport structure
3. Expert reviews within assigned scope (technical, accounting, legal, regulatory)
4. Expert provides written opinion on reviewed elements
5. Opinion is added to the Evidence Passport
6. Expert opinion is NOT a governance decision — only an input

**Expert review boundaries**:
- Expert owns expert judgment within assigned scope
- Expert does NOT own governance decision unless formally authorized
- Expert review does NOT eliminate the need for governance authority approval

**Completion criteria**: Expert review complete; opinion documented; passport updated

---

### Step 6: Governance Boundary Check

**Input**: Evidence bundle; sufficiency assessment; expert review (if any)  
**Output**: Governance boundary confirmation; decision recommendation

**Boundary check procedure**:
1. Verify that all responsibility assignments are clear
2. Verify that the action-authority boundary is stated
3. Verify that the passport does not authorize action
4. Verify that recommendations are clearly separated from decisions
5. Verify that the decision log records who decided what

**Governance boundary statement** (must be present in passport):

> This Evidence Passport is a documentation package for governance review.
> It does not authorize: implementation, approval, construction, investment,
> compliance declaration, public claim, or operational action.
>
> A CarbonOS / ClimateOS recommendation is not an action authority.
> It may identify a possible next step, review requirement, or decision option,
> but it cannot authorize [listed actions] without the required human, expert,
> or governance approval.

**Completion criteria**: Governance boundary confirmed; statement present in passport

---

### Step 7: Decision / Recommendation

**Input**: All prior steps completed  
**Output**: Decision or recommendation; decision log entry

**Decision types**:

| Decision | Meaning | Authority Required |
|----------|----------|-------------------|
| Proceed to disclosure | Evidence sufficient; governance boundaries clear; no untriggered expert review | Governance authority |
| Request additional data | Evidence insufficient; gaps must be filled before use | Reviewer recommendation |
| Request expert review | One or more triggers present; expert review required | Reviewer recommendation (mandatory if triggered) |
| Do not use for disclosure | Evidence insufficient; gaps material; confidence low | Reviewer recommendation |
| Escalate to governance authority | Responsibility boundary unclear; or high-stakes decision | Reviewer recommendation |

**Decision documentation**:
- Decision: [proceed / request data / expert review / do not use / escalate]
- Rationale: [evidence sufficiency, trigger flags, confidence]
- Required approvals: [list human, expert, governance approvals still needed]
- Action-authority boundary: [what this decision does and does not authorize]

**Completion criteria**: Decision made; logged; authority requirements stated

---

### Step 8: Decision Log

**Input**: Completed review; decision made  
**Output**: Decision log entry in Evidence Passport

**Decision log contents**:
- Review ID: [unique identifier]
- Review Date: [YYYY-MM-DD]
- Reviewer: [name/role]
- Steps Completed: [1-7]
- Decision: [proceed / request data / expert review / do not use / escalate]
- Rationale: [summary]
- Approvals Still Required: [list]
- Action-Authority Boundary: [restated]

**Decision log purpose**:
- Records who decided what and why
- Maintains traceability for governance review
- Preserves evidence discipline (recommendation vs. authorization)
- Supports future review or audit

**Completion criteria**: Decision log entry complete; passport complete

---

## Workflow Quality Checks

| Check | Method | Responsibility |
|-------|--------|----------------|
| Evidence discipline maintained | Cross-check terms in passport | Human reviewer |
| Expert triggers assessed | 13-trigger matrix applied | Human reviewer |
| Governance boundary stated | Boundary statement present | Human reviewer |
| Responsibility assigned | Responsibility matrix complete | Human reviewer |
| Decision logged | Decision log entry present | Human reviewer |

## Task102-110 Relationship

The workflow expands:

| Task102-110 Deliverable | Expansion in Task115 |
|------------------------|-----------------------|
| Task102 First Human Use Test | Workflow steps derived from test |
| Task103 Evidence Discipline | Enforced at each workflow step |
| Task104 Claim Review Template | Expanded into workflow steps |
| Task105 Evidence Sufficiency | Step 3 formalizes the assessment |
| Task106 Responsibility Boundary | Step 6 formalizes the boundary check |
| Task107 Pilot Review Record | Adapted as decision log (Step 8) |
| Task108 Human Readability | Checked at each workflow step |

## Task115 Status

```text
Task115: COMPLETE — Human Review Workflow defined.
```

Task116 may proceed (expand expert review trigger matrix).

---

**Status**: Draft  
**Authority**: Task111-120 - QCloud Builder  
**Date**: 2026-07-05
