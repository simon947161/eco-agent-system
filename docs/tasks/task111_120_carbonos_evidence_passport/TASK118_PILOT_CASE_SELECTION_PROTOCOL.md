# Task118 Pilot Case Selection Protocol

## Purpose

Task118 defines how future fictional or clearly non-operational pilot cases should be selected for testing the CarbonOS Evidence Passport and review workflow.

Pilot cases are needed to test the documentation package. But pilot cases must NOT be real carbon conclusions, real ESG disclosure claims, or operational decisions. They must be clearly fictional or clearly non-operational.

This is a documentation-only protocol. It does not implement software, databases, APIs, or automated case selection.

## Pilot Case Purpose

Pilot cases are used to:

1. Test the Evidence Passport structure (Task112)
2. Test the carbon claim intake record template (Task113)
3. Test the evidence bundle structure (Task114)
4. Test the human review workflow (Task115)
5. Test the expert review trigger matrix (Task116)
6. Test the governance boundary and decision log model (Task117)

Pilot cases are **NOT** used to:
- Generate real carbon conclusions
- Create public disclosure claims
- Support investment or operational decisions
- Create compliance or assurance opinions
- Replace real expert review for real claims

## Pilot Case Selection Criteria

### Acceptable Pilot Case Characteristics

A pilot case is acceptable if it is:

| Criterion | Requirement | Example |
|-----------|-------------|---------|
| **Clearly fictional** | Case is explicitly marked as fictional; all data is illustrative | "Fictional Company A — illustrative emissions review" |
| **Clearly non-operational** | Case is not connected to a real disclosure, investment, or operational decision | "Training exercise — not for operational use" |
| **Bounded scope** | Case covers a limited scope that does not require real expert review | "Illustrative Scope 1 only — no regulatory consequence" |
| **Evidence discipline demonstrated** | Case shows raw data → observation → inference → evidence → claim → recommendation separation | Full evidence chain shown with discipline labels |
| **Governance boundary demonstrated** | Case shows recommendation vs. authorization boundary | "This is a recommendation only — not an authorization" |
| **Trigger matrix demonstrated** | Case shows trigger checking (some triggered, some not) | Case designed to trigger 2-3 expert review triggers |
| **Human review workflow demonstrated** | Case shows all 8 workflow steps (Task115) | Full workflow from intake to decision log |

### Unacceptable Pilot Case Characteristics

A pilot case is NOT acceptable if it:

| Criterion | Why Unacceptable |
|-----------|------------------|
| Uses real company data without explicit fictional labelling | May be mistaken for real conclusion |
| Uses real disclosure timelines or regulatory deadlines | May imply operational consequence |
| Claims to support real investment or operational decision | Violates action-authority boundary |
| Claims to be compliance-ready or assurance-ready | Violates governance boundary |
| Does not flag expert review triggers when present | Fails the trigger matrix test |
| Conflates recommendation with authorization | Fails the governance boundary test |
| Does not maintain evidence discipline | Fails the evidence discipline test |

## Pilot Case Documentation Requirements

Every pilot case must include:

### 1. Fictional / Non-Operational Disclaimer

```markdown
## Pilot Case Disclaimer

This is a **fictional or non-operational pilot case** for documentation testing only.

- It is NOT a real carbon conclusion.
- It is NOT a real ESG disclosure claim.
- It is NOT sufficient for compliance, assurance, investment, or operational decision.
- All data is illustrative.
- All conclusions are illustrative.
- This pilot case must not be used for any operational, public, or regulatory purpose.
```

### 2. Evidence Discipline Labels

Every element in the pilot case must be labelled:

```markdown
## Evidence Discipline Labels (Pilot Case)

- Raw data: [explicitly labelled as "illustrative raw data"]
- Observation: [explicitly labelled as "illustrative observation"]
- Inference: [explicitly labelled as "illustrative inference — not verified"]
- Evidence: [explicitly labelled as "illustrative evidence — for pilot only"]
- Claim: [explicitly labelled as "illustrative claim — not a real assertion"]
- Recommendation: [explicitly labelled as "illustrative recommendation — not an authorization"]
```

### 3. Governance Boundary Restatement

The pilot case must restate the governance boundary:

```markdown
## Governance Boundary (Pilot Case)

This pilot case is a documentation exercise only.

It does not authorize:
- implementation
- approval
- construction
- investment
- compliance declaration
- public claim
- operational action

The recommendations in this pilot case are illustrative only.
They do not authorize any action.
```

### 4. Trigger Matrix Demonstration

The pilot case should demonstrate trigger checking:

```markdown
## Expert Review Trigger Check (Pilot Case — Illustrative)

For this pilot case, the following triggers are illustrated as present:

- [ ] High uncertainty: [illustrative example]
- [x] Conflicting evidence: [illustrative example]
- [ ] Low confidence: [illustrative example]
- ... [all 13 triggers assessed illustratively]
```

## Pilot Case Selection Protocol

### Protocol Steps

1. **Define pilot case purpose** — which Task111-120 element is being tested
2. **Select fictional scenario** — create a clearly fictional company/claim context
3. **Assign pilot case ID** — use format `PC-001`, `PC-002`, etc.
4. **Document fictional disclaimer** — explicit statement at the start
5. **Create illustrative data** — raw data, observations, inferences (all labelled)
6. **Run through workflow** — complete all 8 steps (Task115)
7. **Check evidence discipline** — verify terms are separated
8. **Check trigger matrix** — verify all 13 triggers assessed
9. **Check governance boundary** — verify action-authority boundary maintained
10. **Document as pilot case** — full passport with all disclaimers

### Selection Criteria Checklist

```markdown
## Pilot Case Selection Checklist

- [ ] Case is clearly fictional OR clearly non-operational
- [ ] Case does NOT use real company data without fictional labelling
- [ ] Case does NOT imply operational, regulatory, or public consequence
- [ ] Case demonstrates evidence discipline (all 6 terms separated)
- [ ] Case demonstrates trigger matrix (all 13 triggers assessed)
- [ ] Case demonstrates governance boundary (recommendation vs. authorization)
- [ ] Case includes fictional / non-operational disclaimer
- [ ] Case includes evidence discipline labels
- [ ] Case includes governance boundary restatement
- [ ] Case is documented as a pilot case (not a real conclusion)
```

## Pilot Case Library (Future)

Task118 recommends creating a **Pilot Case Library** for future testing.

The library would contain:
- 3-5 fictional pilot cases covering different CarbonOS scenarios
- Each pilot case tests different elements of the Evidence Passport
- Each pilot case includes full disclaimers and labels

**Pilot Case Library is NOT part of Task111-120.** Task118 only defines the protocol. The library can be created in a future task (Task121+).

## Task102-110 Relationship

Task118 expands:

| Task102-110 Deliverable | Expansion in Task118 |
|------------------------|-----------------------|
| Task107 Pilot Review Record | Expanded into pilot case selection protocol |
| Task102-110 pilot case | Protocol defined for future pilot cases |

## Pilot Case Protocol Success Criteria

The protocol is successful if:

1. A human reviewer can select a pilot case using the protocol
2. The protocol prevents real claims from being used as pilots
3. The protocol ensures evidence discipline is demonstrated
4. The protocol ensures governance boundaries are maintained
5. The protocol is clearly documentation-only

## Task118 Status

```text
Task118: COMPLETE — Pilot Case Selection Protocol defined.
```

Task119 may proceed (record QCloud builder dispatch).

---

**Status**: Draft  
**Authority**: Task111-120 - QCloud Builder  
**Date**: 2026-07-05
