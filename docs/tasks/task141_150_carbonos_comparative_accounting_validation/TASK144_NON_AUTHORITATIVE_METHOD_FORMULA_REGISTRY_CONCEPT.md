# Task144 Non-Authoritative Method And Formula Registry Concept

## Purpose

Task144 defines a conceptual registry model for methods, formulas, factors, source status, versioning, and review state.

This is a non-authoritative documentation artifact. It does not implement a registry, database, calculator, formula library, scoring engine, API, MCP server, or compliance tool.

## Registry Purpose

The future registry concept may help CarbonOS track whether a method, formula, factor, or assumption has:

- an identified source
- a recorded citation
- a version marker
- a review state
- an uncertainty flag
- a limitation note
- a relationship to a claim boundary
- a relationship to ClimateOS / EcoEngine validation questions

The registry concept supports review discipline. It does not approve or calculate anything.

## Conceptual Fields

| Field | Purpose | Boundary |
| --- | --- | --- |
| Registry item ID | Stable conceptual reference for review. | Not a database key or runtime identifier. |
| Item type | Method, formula reference, factor reference, assumption, boundary note, or evidence rule candidate. | Category only; not authoritative content. |
| Framework / jurisdiction context | Future research context associated with the item. | Research target only unless Task143 protocol has been satisfied. |
| Source citation | Source metadata captured under Task143 protocol. | Required before factual use. |
| Version marker | Source version, date, or supersession note. | Must remain visible. |
| Formula reference status | Whether a formula reference is missing, partial, cited, disputed, superseded, or not applicable. | Does not validate or run the formula. |
| Factor reference status | Whether a factor reference is missing, partial, cited, disputed, superseded, or not applicable. | Does not approve a factor. |
| Review status | Current review state. | No assurance or certification meaning. |
| Uncertainty flag | Known uncertainty, conflict, missing source, or limitation. | Must not be hidden in later use. |
| Claim boundary linkage | Relationship to claim or accounting boundary categories. | Descriptive only. |

## Review Status

Allowed review statuses:

- Draft Concept
- Research Question
- Source Located
- Citation Captured
- Primary Source Reviewed
- Cross-Checked
- Founder / GPT Review Required
- Eligible For Future Inclusion
- Rejected
- Superseded

No status creates compliance, assurance, certification, verification, or legal authority.

## Source Status

Allowed source statuses:

- No Source
- Source Needed
- Candidate Source
- Primary Source
- Secondary Source
- Superseded Source
- Conflicting Sources
- Source Freshness Unknown
- Source Reviewed Under Task143 Protocol

## Uncertainty Flags

Uncertainty flags may include:

- source missing
- version unclear
- applicability unclear
- framework context unclear
- method boundary unclear
- formula reference incomplete
- factor reference incomplete
- evidence sufficiency unresolved
- review conflict
- future expert review needed

## Formula Reference Status

Formula reference status records whether a formula is referenced and reviewable. It does not record an executable formula and does not authorize calculation.

Allowed states:

- Not Applicable
- Missing
- Mentioned But Uncited
- Cited But Not Reviewed
- Reviewed As Source Reference
- Disputed
- Superseded
- Blocked From Use

## Prohibited Calculation Use

The Task144 registry concept may not be used to:

- calculate emissions
- calculate reductions
- calculate removals
- calculate offsets
- calculate risk
- score evidence
- certify claims
- determine compliance
- generate disclosure outputs
- operate as a database or runtime system

## Boundary Against Calculators / Compliance / Certification

This concept is a map of review metadata. It is not a calculator, compliance tool, assurance workflow, certification registry, public reporting engine, or financial / legal system.

Any future operational registry would require a separate architecture gate, security review, data governance review, source governance review, and explicit Founder approval.

## Relationship To Task143 Research Protocol

Task144 inherits Task143 source hierarchy, citation requirements, freshness requirements, review states, and prohibited memory rules.

No registry item may be treated as factually usable unless the Task143 protocol has been satisfied.

## Task145 Handoff Boundary

Task145 may use the registry concept to define how Evidence Passport v0.2 records method relationship, source status, uncertainty, and review state.

Task145 must not create real evidence records, operational passports, databases, calculators, APIs, or compliance outputs.

## Status

```text
Task144 Non-Authoritative Method And Formula Registry Concept: COMPLETED AS DOCUMENTATION-ONLY ARCHITECTURE WORK
Registry Implementation: NOT CREATED
Formulas As Authoritative Content: NOT CREATED
Calculators / Compliance / Certification: NOT CREATED
Runtime / API / Database / MCP / Scoring / Automation Work: NOT CREATED
QCloud Builder Work: SUSPENDED
```
