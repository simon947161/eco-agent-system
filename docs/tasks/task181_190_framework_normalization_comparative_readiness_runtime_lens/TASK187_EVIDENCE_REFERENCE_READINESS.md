# Task187 Evidence Reference Readiness

## Purpose

Task187 defines evidence reference fields needed before framework metadata can support future Evidence Passport, ClaimOS, CarbonOS, or ClimateOS review work.

This is metadata-only readiness work. No evidence record, runtime link, or claim conclusion is created.

## Evidence Reference Fields

| Field | Requirement |
| --- | --- |
| Evidence reference ID | Stable ID for a future evidence reference. |
| Citation unit ID | Required before any evidence link is created. |
| Framework family | Source family associated with the citation unit. |
| Evidence type | Observation, document, inventory, questionnaire response, disclosure, methodology, factor database, review note, or external dataset. |
| Version linkage | Framework version, reporting period, cycle, amendment, or notice date. |
| Citation linkage | Official URL plus location unit. |
| Source freshness | Freshness check date and status. |
| Observation linkage | Whether future evidence can link to observation records. |
| Claim timing | Reporting period, publication date, event date, assessment cycle, or notice effective date where relevant. |
| Runtime relevance | Potential future runtime relevance tag only. |
| Human review trigger | Required where source, translation, legal, domain, or version risk exists. |

## Readiness Rules

| Rule | Requirement |
| --- | --- |
| No citation unit, no evidence link | Evidence reference work cannot proceed without a citation unit. |
| No version, no current claim | Evidence reference work cannot support future currentness claims without version metadata. |
| No translation review, no translated claim | Translated source material cannot support future claims without review. |
| No hierarchy check, no mapping | Framework source type must be classified before mapping. |
| No runtime by implication | Runtime relevance metadata does not authorize runtime implementation. |

## Framework Evidence Readiness Notes

| Framework | Evidence linkage metadata | Readiness state |
| --- | --- | --- |
| IPCC | Report/chapter/figure/table/methodology citation units may support future climate context references | Partial; exact citation units needed |
| ISSB / IFRS | Standard/amendment/effective-period citation units may support future disclosure source references | Partial; amendment and effective-period review needed |
| ASRS | Portal-period citation units may support future Australia-specific disclosure references | Partial; reporting-period routing needed |
| TNFD | Recommendation/guidance citation units may support future nature-risk evidence references | Partial; guidance hierarchy needed |
| GHG Protocol | Standard/guidance/tool/correction citation units may support future inventory source references | Partial; correction and tool boundary needed |
| GRI | Final topic-standard citation units may support future sustainability reporting source references | Partial; final-standard versus project status needed |
| CDP | Annual questionnaire/guidance/scoring-method citation units may support future disclosure-data references | Partial; cycle-specific material needed |
| China source ecosystem | Official Chinese source, notice, database, methodology, or regulator citation units may support future China source references | Needs translation, authority segmentation, and final/draft review |

## Boundary

Evidence reference readiness is not evidence validation and does not create Evidence Passport records.
