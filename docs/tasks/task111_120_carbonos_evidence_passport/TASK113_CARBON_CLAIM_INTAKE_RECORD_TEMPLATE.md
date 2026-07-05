# Task113 Carbon Claim Intake Record Template

## Purpose

Task113 provides a structured intake record template for carbon and ESG claim review.

The intake record is a documentation template only. It is not a form, database, API, web form, or software interface. It is filled out by a human reviewer as part of governance review.

## Intake Record Purpose

The intake record captures claim details at the start of review — before evidence is assessed, before expert review is triggered, and before governance decisions are made.

It serves to:
1. Record the claim statement and intended use
2. Identify available evidence sources
3. Flag potential expert review triggers early
4. Assign initial responsibility
5. State governance boundaries before review begins

## Carbon Claim Intake Record Template

```markdown
# Carbon Claim Intake Record: [Claim ID]

## Intake Metadata
- Intake Date: [YYYY-MM-DD]
- Intake Prepared By: [Human reviewer name/role]
- Claim Owner: [Person/entity making the claim]
- Intended Use: [ESG disclosure / investor report / internal review / other]

## Claim Statement
[Specific, reviewable assertion. Must be separable from observations and inferences.]

Example: "Scope 1 emissions for Site A decreased by 12% in FY2025 compared to FY2024 baseline."

## Intended Use and Consequence Assessment
[What will this claim be used for? Does it trigger any expert review conditions?]

- [ ] Regulatory consequence (mandatory ESG disclosure)
- [ ] Financial consequence (investor-facing document)
- [ ] Public-impact consequence (public sustainability report)
- [ ] Legal consequence (may affect legal obligations)
- [ ] Insurance consequence (may affect environmental liability)
- [ ] Engineering consequence (supports engineered carbon project)
- [ ] Irreversible or high-cost project action (supports investment decision)
- [ ] Domain-specific technical judgment required (carbon accounting methodology)

## Evidence Sources Available
[List known evidence sources at intake. This is not a sufficiency assessment — only a source inventory.]

### Raw Data References
- [ ] Meter data: [locations, periods]
- [ ] Invoices: [fuel suppliers, periods]
- [ ] Certificate records: [registry, serials, periods]
- [ ] Project documents: [locations, methodologies]
- [ ] Internal estimates: [methods, limitations]
- [ ] Third-party reports: [source, scope, limitations]
- [ ] Other: [describe]

### Known Data Gaps
[ List missing evidence types that may be required for this claim. ]

- [ ] Missing critical data: [describe]
- [ ] Incomplete periods: [describe]
- [ ] Unverified sources: [describe]
- [ ] Conflicting sources known: [describe]

## Early Expert Review Trigger Flags
[Flag any triggers that are already apparent at intake. Final trigger assessment happens after evidence review.]

- [ ] High uncertainty expected (incomplete methods or data)
- [ ] Conflicting evidence expected or known
- [ ] Low confidence expected (estimation methods >20% of claim)
- [ ] Domain-specific technical judgment likely required
- [ ] [Other triggers from Task116 matrix]

## Responsibility Assignment (Initial)
[Assign responsibility at intake. This may be updated after review.]

| Role | Assigned To | Date |
|------|-------------|------|
| Claim Owner | [Name/role] | [YYYY-MM-DD] |
| Intake Preparer | [Name/role] | [YYYY-MM-DD] |
| Initial Reviewer | [Name/role] | [YYYY-MM-DD] |
| Expert Reviewer (if triggered) | [Not yet assigned / Name] | [N/A or YYYY-MM-DD] |
| Governance Authority | [Name/role] | [YYYY-MM-DD] |

## Governance Boundary Statement
[Explicit statement of what this intake record does and does not authorize.]

> This intake record is a documentation package for governance review.
> It does not authorize:
> - implementation
> - approval
> - construction
> - investment
> - compliance declaration
> - public claim
> - operational action
>
> A CarbonOS / ClimateOS recommendation is not an action authority.
> It may identify a possible next step, review requirement, or decision option,
> but it cannot authorize implementation, approval, construction, investment,
> compliance declaration, public claim, or operational action without the
> required human, expert, or governance approval.

## Intake Notes
[Free-text notes from the intake preparer.]

## Next Steps
[Identified next steps after intake. These are recommendations, not authorizations.]

- [ ] Proceed to evidence bundle assembly (Task114)
- [ ] Request missing data from claim owner
- [ ] Flag expert review triggers and identify required expert type
- [ ] Proceed to human review workflow (Task115)
- [ ] Other: [describe]

---
Intake Status: [PENDING / COMPLETE / ON HOLD / ESCALATE]
```

## Intake Record Discipline Requirements

The intake record must maintain evidence discipline:

| Term | Requirement in Intake Record |
|------|--------------------------------|
| Raw data | Listed as source references only; not presented as evidence |
| Observation | May be partially stated; clearly marked as "preliminary observation" |
| Inference | Must be marked as "preliminary inference — not verified" |
| Evidence | Not assessed at intake; only sources listed |
| Claim | Must be a specific, reviewable assertion; separated from observations |
| Recommendation | Next steps are recommendations only; not authorizations |

## Intake Record vs. Evidence Passport

The intake record is **not** the Evidence Passport.

| Concept | Timing | Purpose |
|---------|--------|---------|
| Intake Record | Before evidence review | Capture claim, sources, early triggers, initial responsibility |
| Evidence Passport | After evidence review | Present structured evidence, sufficiency assessment, final trigger flags, decision log |

The intake record feeds into the Evidence Passport. The passport is the complete review documentation.

## Intake Record Boundaries

The intake record:

- **Is**: a documentation template for governance review planning
- **Is not**: a compliance form, assurance engagement letter, certification application, or approval document
- **Does not**: authorize disclosure, investment, construction, or operational action
- **Does not**: constitute verified evidence or validated conclusions
- **Does not**: replace expert review when triggered

## Task102-110 Relationship

The intake record template expands:

| Task102-110 Deliverable | Expansion in Task113 |
|------------------------|-----------------------|
| Task104 Claim Review Template | Expanded into full intake record structure |
| Task103 Evidence Discipline | Enforced through term separation requirements |
| Task105 Evidence Sufficiency | Referenced but not assessed at intake |
| Task106 Responsibility Boundary | Included as initial responsibility assignment |

## Intake Record Template Success Criteria

The template is successful if:

1. A human reviewer can complete it without software
2. Evidence discipline is maintained (terms not conflated)
3. Expert review triggers can be flagged early
4. Governance boundaries are explicit
5. Responsibility is assigned before review begins
6. The record is clearly documentation-only

## Task113 Status

```text
Task113: COMPLETE — Carbon Claim Intake Record Template defined.
```

Task114 may proceed (define carbon evidence bundle structure).

---

**Status**: Draft  
**Authority**: Task111-120 - QCloud Builder  
**Date**: 2026-07-05
