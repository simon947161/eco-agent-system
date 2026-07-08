# Task192 Citation Unit Verification Registry

## Purpose

Task192 defines how citation units must be verified before future mapping or evidence reasoning can begin.

This registry is metadata-only. It does not interpret cited sources.

## Citation Unit Definition

A citation unit is the smallest source reference that ClimateOS / CarbonOS may use in a future mapping or evidence reasoning task.

A citation unit must be specific enough to identify:

- framework family
- official source owner
- official document
- document hierarchy level
- version or cycle
- location inside the source
- official URL or official portal path
- access date
- review status

## Official Citation Hierarchy

| Hierarchy level | Verification requirement |
| --- | --- |
| Framework family | Official family name or source ecosystem label recorded. |
| Owner / authority | Official owner, publisher, regulator, ministry, board, or taskforce recorded. |
| Document class | Report, standard, guidance, technical note, FAQ, questionnaire, legal act, notice, database, methodology, amendment, or supporting material classified. |
| Document title | Official title recorded exactly enough for later retrieval. |
| Version reference | Assessment cycle, named version, issue date, amendment, reporting period, annual cycle, database edition, or notice date recorded. |
| Section reference | Chapter, section, annex, table, figure, question, methodology code, notice heading, or portal period recorded where applicable. |
| Paragraph reference | Paragraph, clause, numbered item, row, or equivalent unit recorded where available. |
| Official URL reference | Official URL, official portal locator, or official document download locator recorded. |
| Access date | Required. |
| Citation completeness check | Complete, partial, stale check needed, translation review needed, or governance review needed. |

## Completeness Status Values

| Status | Meaning |
| --- | --- |
| Complete | Required citation metadata is present for the selected future use. |
| Partial | Some metadata is present, but not enough for mapping or reasoning. |
| Needs version review | Version, amendment, reporting period, cycle, or notice status must be rechecked. |
| Needs translation review | Official-language or translation status must be reviewed. |
| Needs source verification | Official owner, URL, or source hierarchy must be confirmed. |
| Not eligible | Citation unit cannot be used for future mapping or reasoning. |

## Framework-Specific Verification Notes

| Framework family | Required verification focus |
| --- | --- |
| IPCC | Report cycle, report family, chapter/section/table/figure, methodology status, and error-handling status. |
| ISSB / IFRS | Standard identifier, amendment status, effective period, related standard relationship, and official page or standard text access condition. |
| ASRS | Portal reporting period, standard identifier, amendment, compiled/uncompiled status, and support-material boundary. |
| TNFD | Recommendation version, guidance type, page update date, and recommendation/guidance separation. |
| GHG Protocol | Standard family, guidance/tool/correction boundary, document date, and under-development status. |
| GRI | Final standard versus project/supporting-material status, topic standard identifier, and standards-development context. |
| CDP | Disclosure cycle, questionnaire/guidance/scoring-method boundary, portal status, and annual-cycle version. |
| China source ecosystem | Official Chinese title, official authority, publication date, final/draft status, translation status, and source-family segment. |

## Boundary

Verified citation units still do not create interpretation, comparison, or compliance claims.
