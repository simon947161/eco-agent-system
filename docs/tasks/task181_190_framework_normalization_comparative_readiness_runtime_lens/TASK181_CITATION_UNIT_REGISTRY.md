# Task181 Citation Unit Registry

## Purpose

Task181 defines the citation unit structure that future ClimateOS / CarbonOS framework work must use before any mapping or reasoning is attempted.

This registry defines citation metadata only. It does not interpret any cited source.

## Citation Unit Structure

| Field | Requirement |
| --- | --- |
| Citation unit ID | Stable ClimateOS / CarbonOS identifier for a future citation unit. |
| Framework family | IPCC, ISSB / IFRS, ASRS, TNFD, GHG Protocol, GRI, CDP, or China source ecosystem. |
| Owner / authority | Official publisher, board, regulator, ministry, taskforce, or portal authority. |
| Document class | Report, standard, guidance, technical note, FAQ, questionnaire, portal record, legal act, notice, database, methodology, amendment, or supporting material. |
| Document title | Official title as shown by the official source. |
| Official URL | Official locator only. |
| Version / cycle | Version, assessment cycle, reporting period, annual cycle, amendment, database edition, or notice date where visible. |
| Publication date | Official publication date where visible. |
| Access date | Date ClimateOS / CarbonOS accessed the source. |
| Location unit | Section, chapter, paragraph, table, figure, annex, question, methodology code, notice title, or portal period selection. |
| Citation status | Candidate, located, metadata complete, freshness check needed, human review needed, or approved for future mapping. |
| Interpretation status | Must remain "not interpreted" until a later approved research task. |

## Identifier Format

Recommended format:

```text
CFW-[FRAMEWORK]-[DOCUMENT_CLASS]-[YYYY_OR_CYCLE]-[SEQUENCE]
```

Examples:

```text
CFW-IPCC-REPORT-AR6-001
CFW-IFRS-STANDARD-2026-001
CFW-ASRS-PORTAL-2025-001
CFW-CDP-QUESTIONNAIRE-2026-001
CFW-CN-MEE-NOTICE-2026-001
```

## Framework-Specific Citation Unit Rules

| Framework family | Required citation unit |
| --- | --- |
| IPCC | Report cycle plus report or methodology family; future use should add chapter, section, table, figure, or annex before mapping. |
| ISSB / IFRS | Standard page plus standard identifier, issued/amended status, effective period, and related amendment/project where relevant. |
| ASRS | AASB portal period selection plus standard or amendment identifier; reporting period is mandatory metadata. |
| TNFD | Recommendation version or guidance document type; version and page update date are mandatory metadata where visible. |
| GHG Protocol | Standard or guidance family plus correction, tool, or supporting-document status where relevant. |
| GRI | Final standard versus project/supporting-material status; topic standard identifier is mandatory where visible. |
| CDP | Disclosure cycle plus questionnaire/guidance/scoring-method family; annual cycle is mandatory metadata. |
| China source ecosystem | Official source authority, official Chinese title, publication date, final/draft status, translation status, and source-family segment are mandatory metadata. |

## Boundary

Citation units are not evidence conclusions. They are source-addressing units for later review.
