# Task163 Runtime Relevance Metadata Model

## Purpose

Task163 defines metadata fields that allow official source discovery to support future runtime integrity without creating runtime implementation.

## Required Metadata Fields

| Field | Purpose |
| --- | --- |
| Source ID | Stable local identifier for discovery records. |
| Source label | Human-readable short name. |
| Owner / publisher | Official body responsible for the source. |
| Official locator | URL or permanent locator. |
| Source category | Standard, guidance, legal source, questionnaire, project page, recommendation, or portal. |
| Access date | Date the source was accessed. |
| Publication date | Publication date if visible and verified. |
| Effective date | Effective date if applicable and verified. |
| Version / amendment signal | Visible version, amendment, project, or update marker. |
| Reporting-period dependency | Whether source use depends on a reporting period. |
| Jurisdiction / framework scope | Routing label only. |
| Runtime relevance tags | Future runtime metadata categories. |
| Freshness risk | Current, stale risk, unknown, superseded risk, or review needed. |
| Citation completeness | Missing, partial, complete, or review needed. |
| Review blocker | Missing information that prevents future factual use. |

## Runtime Relevance Tags

Allowed tags:

- evidence freshness
- evidence versioning
- amendment tracking
- official correction tracking
- reporting-period sensitivity
- observation anchoring
- extreme-event update pathway
- physical-risk context
- claim boundary sensitivity
- claim confidence evolution
- cross-framework dependency
- source hierarchy risk
- human review trigger

## Boundary

The metadata model does not define a schema, database, API, ontology, scoring model, or automated registry.

It is a documentation pattern for future human-reviewed source records.
