# Task116 Expert Review Trigger Matrix Expansion

## Purpose

Task116 restores and explicitly maps the broader Task101 expert review trigger language that was narrower in Task102-110 CarbonOS Fast Track Sprint 01.

Task102-110 passed with a **minor note** that expert review triggers were narrower than full Task101 language. Task111-120 must restore or explicitly map the broader Task101 trigger language while preserving CarbonOS-specific triggers.

This is a documentation-only trigger matrix. It does not implement automated trigger detection, workflow engines, scoring systems, or decision systems.

## Background: Task102-110 Minor Note

Task102-110 expert review triggers (from Task103 and Task106) were:

> Expert review is required for high-stakes disclosure, compliance claims,
> assurance-like language, contested evidence, missing critical data, method
> choice disputes, or claims that may influence financial, operational, public,
> or regulatory decisions.

This language covers some but not all Task101 triggers. The minor note requires Task111-120 to restore the broader Task101 language.

## Task101 Expert Review Triggers (Full Language)

Task101 Human Use Graduation Test Suite defines **13 mandatory expert review triggers**. Expert review is a governance requirement — not an optional enhancement — when any trigger is present.

| # | Trigger | Task101 Definition |
|---|---------|---------------------|
| 1 | **High uncertainty** | Confidence cannot be reliably bounded with available data |
| 2 | **Conflicting evidence** | Multiple credible sources yield contradictory observations |
| 3 | **Low confidence** | Any judgment rated below the minimum confidence threshold for the scenario |
| 4 | **Missing critical data** | Required evidence types are absent or known to be incomplete |
| 5 | **Regulatory consequence** | The scenario output bears on a regulatory obligation or compliance determination |
| 6 | **Engineering consequence** | The scenario output bears on structural, hydrological, geotechnical, or similar technical design |
| 7 | **Safety consequence** | The scenario output bears on occupational, public, or environmental safety |
| 8 | **Insurance consequence** | The scenario output may affect insurance coverage, liability, or indemnity positions |
| 9 | **Legal consequence** | The scenario output may affect legal rights, obligations, or proceedings |
| 10 | **Financial consequence** | The scenario output bears on material investment, expenditure, or financial disclosure |
| 11 | **Public-impact consequence** | The scenario output may affect public health, safety, or community interest |
| 12 | **Irreversible or high-cost project action** | The scenario involves construction, land use change, infrastructure deployment, or similar action that is costly or impractical to reverse |
| 13 | **Domain-specific technical judgment** | The scenario requires specialist knowledge beyond what general ClimateOS review can reasonably assess |

## CarbonOS-Specific Trigger Language (Task102-110)

Task102-110 preserved these CarbonOS-specific trigger phrasing:

| Task102-110 Trigger Phrasing | Maps to Task101 Trigger # |
|-------------------------------|--------------------------|
| High-stakes disclosure | #5 Regulatory, #10 Financial, #11 Public-impact |
| Compliance claims | #5 Regulatory, #9 Legal |
| Assurance-like language | #13 Domain-specific technical judgment |
| Contested evidence | #2 Conflicting evidence |
| Missing critical data | #4 Missing critical data |
| Method choice disputes | #13 Domain-specific technical judgment |
| May influence financial decisions | #10 Financial consequence |
| May influence operational decisions | #12 Irreversible or high-cost action |
| May influence public decisions | #11 Public-impact consequence |
| May influence regulatory decisions | #5 Regulatory consequence |

## Expanded Expert Review Trigger Matrix for CarbonOS Evidence Passport

Task116 restores **all 13 Task101 triggers** and provides CarbonOS-specific examples and escalation guidance.

### Trigger Matrix: All 13 Triggers with CarbonOS Examples

| # | Trigger | CarbonOS Example | Expert Type Required | Escalation Requirement |
|---|---------|-------------------|---------------------|----------------------|
| 1 | **High uncertainty** | Incomplete activity data for material emission source; uncertainty in emission factor selection >30% | Carbon accounting expert; measurement uncertainty specialist | Expert review mandatory; do NOT use passport for disclosure |
| 2 | **Conflicting evidence** | Two suppliers provide contradictory fuel records; meter data conflicts with invoice data | Data verification specialist; auditor | Expert review mandatory; conflicts must be resolved or disclosed |
| 3 | **Low confidence** | Estimation methods used for >20% of emissions; uncertainty not bounded | Carbon accounting expert | Expert review mandatory; confidence assessment required |
| 4 | **Missing critical data** | No meter data for a material facility; missing emission factors for key sources | Carbon accounting expert; data specialist | Expert review mandatory; missing data impact must be assessed |
| 5 | **Regulatory consequence** | Claim will be used in mandatory ESG disclosure; claim supports compliance determination | Regulatory specialist; legal expert | Expert review mandatory; regulatory interpretation required |
| 6 | **Engineering consequence** | Claim involves engineered carbon removal project; claim supports nature-based solution with technical design | Engineering expert; carbon removal specialist | Expert review mandatory; technical design must be reviewed |
| 7 | **Safety consequence** | Claim involves industrial process safety data; claim supports carbon capture with safety implications | Safety engineer; process safety specialist | Expert review mandatory; safety implications must be assessed |
| 8 | **Insurance consequence** | Claim may affect environmental liability insurance; claim supports project that may change insurance coverage | Insurance specialist; risk management expert | Expert review mandatory; insurance implications must be assessed |
| 9 | **Legal consequence** | Claim may affect climate-related litigation; claim supports carbon credit transaction with legal risk | Legal expert; climate law specialist | Expert review mandatory; legal interpretation required |
| 10 | **Financial consequence** | Claim will be used in investor-facing disclosure; claim supports financial decision >$1M | Financial auditor; investor disclosure specialist | Expert review mandatory; financial disclosure standards apply |
| 11 | **Public-impact consequence** | Claim will be used in public sustainability report; claim may affect public perception | Public communications specialist; ESG reporting expert | Expert review mandatory; public disclosure standards apply |
| 12 | **Irreversible or high-cost project action** | Claim supports carbon removal project investment >$100K; claim supports land use change | Project finance specialist; carbon project developer | Expert review mandatory; investment decision requires expert review |
| 13 | **Domain-specific technical judgment** | Claim requires carbon accounting methodology review; claim involves carbon removal quantification | Carbon accounting expert; domain specialist | Expert review mandatory; domain expertise required |

## Trigger Detection and Flagging Procedure

The Evidence Passport review workflow (Task115) must check all 13 triggers at **Step 4: Expert Review Trigger Check**.

### Procedure

1. **Review the claim and evidence bundle** — identify any conditions that match the 13 triggers
2. **For each trigger**: document whether present (yes/no/potential)
3. **If any trigger is "yes" or "potential"**: flag it explicitly in the passport
4. **If any trigger is "yes"**: expert review is **mandatory** (not optional)
5. **Identify required expert type** from the matrix
6. **State that expert review is required** before the passport can be used for governance decision
7. **Do NOT present the passport as sufficient** for governance decision until expert review is complete

### Trigger Flagging Format (in Evidence Passport)

```markdown
## Expert Review Trigger Flags

### Triggers Assessed
| # | Trigger | Present? | Expert Type Required | Notes |
|---|---------|----------|---------------------|-------|
| 1 | High uncertainty | Yes | Carbon accounting expert | Estimation >20% of emissions |
| 2 | Conflicting evidence | No | — | — |
| 3 | Low confidence | Yes | Carbon accounting expert | Uncertainty not bounded |
| 4 | Missing critical data | No | — | — |
| 5 | Regulatory consequence | Yes | Regulatory specialist | Will be used in mandatory ESG disclosure |
| ... | ... | ... | ... | ... |

### Expert Review Required
✓ YES — one or more triggers present. Expert review is mandatory before this
passport can be used for governance decision.

Required expert type(s): [list]

Expert review completed: [Yes / No / Pending]

If pending: passport is NOT sufficient for governance decision.
```

## Trigger Expansion Mapping

This section explicitly maps the relationship between Task101 triggers, Task102-110 triggers, and the expanded CarbonOS triggers.

### Mapping Table

| Task101 Trigger | Task102-110 Phrasing | Expanded CarbonOS Trigger | Status in Task116 |
|-----------------|------------------------|--------------------------|-------------------|
| High uncertainty | Not explicitly named | High uncertainty (estimation >20%; unbounded uncertainty) | **RESTORED** |
| Conflicting evidence | Contested evidence | Conflicting evidence (contradictory sources) | Preserved + expanded |
| Low confidence | Not explicitly named | Low confidence (below minimum threshold) | **RESTORED** |
| Missing critical data | Missing critical data | Missing critical data (absent/incomplete) | Preserved |
| Regulatory consequence | Compliance claims; may influence regulatory decisions | Regulatory consequence (ESG disclosure; compliance) | Preserved + expanded |
| Engineering consequence | Not explicitly named | Engineering consequence (engineered removal; technical design) | **RESTORED** |
| Safety consequence | Not explicitly named | Safety consequence (process safety; industrial) | **RESTORED** |
| Insurance consequence | Not explicitly named | Insurance consequence (liability; coverage) | **RESTORED** |
| Legal consequence | May influence legal decisions | Legal consequence (litigation; obligations) | Preserved + expanded |
| Financial consequence | May influence financial decisions | Financial consequence (investor disclosure; materiality) | Preserved + expanded |
| Public-impact consequence | May influence public decisions | Public-impact consequence (sustainability reporting; public perception) | **RESTORED** |
| Irreversible or high-cost project action | May influence operational decisions | Irreversible or high-cost project action (investment; land use) | Preserved + expanded |
| Domain-specific technical judgment | Assurance-like language; method choice disputes | Domain-specific technical judgment (accounting methodology; removal quantification) | Preserved + expanded |

### Status Summary

| Status | Count | Triggers |
|--------|-------|-----------|
| **RESTORED** (was missing from Task102-110) | 6 | High uncertainty, Low confidence, Engineering consequence, Safety consequence, Insurance consequence, Public-impact consequence |
| Preserved (was in Task102-110) | 3 | Conflicting evidence, Missing critical data, Domain-specific technical judgment |
| Preserved + expanded (was in Task102-110, now broader) | 4 | Regulatory consequence, Legal consequence, Financial consequence, Irreversible or high-cost project action |
| **Total** | **13** | All Task101 triggers restored and mapped |

## Expert Review Output Requirements

When any trigger is present, the Evidence Passport must include:

1. **Explicit trigger flag(s)** — which triggers are present
2. **Expert type identification** — what kind of expert is required
3. **Expert review statement** — that expert review is required before the passport can be used
4. **Non-sufficiency statement** — that the passport is NOT sufficient for governance decision until expert review is complete
5. **Expert review record** — once expert review is complete, the expert opinion must be added to the passport

## Task102-110 Relationship

Task116 expands:

| Task102-110 Deliverable | Expansion in Task116 |
|------------------------|-----------------------|
| Task103 Evidence Discipline — Expert Review Triggers section | Expanded from 1 paragraph to full 13-trigger matrix |
| Task106 Responsibility Boundary — Expert Review Triggers section | Expanded from 5 bullet points to full 13-trigger matrix |
| Task102-110 minor note | Addressed — all 13 Task101 triggers restored and mapped |

## Task116 Status

```text
Task116: COMPLETE — Expert Review Trigger Matrix expanded and mapped.
```

All 13 Task101 triggers are restored. CarbonOS-specific examples and escalation guidance are provided. The trigger matrix is ready for use in Evidence Passport reviews.

Task117 may proceed (define governance boundary and decision log model).

---

**Status**: Draft
**Authority**: Task111-120 - QCloud Builder
**Date**: 2026-07-05
