# Task171 Framework Intake Control Boundary Gate

## Purpose

Task171 defines the rules for metadata-only framework intake under the Runtime Lens.

The gate converts official source discovery into structured framework metadata without interpreting standards or creating implementation dependencies.

## Framework Intake Rules

| Rule | Requirement |
| --- | --- |
| Official-source-first | Intake records must identify official owner and official source locator before framework metadata is reused. |
| Metadata-only | Records may describe identity, owner, hierarchy, version, lifecycle, and update signals. |
| No interpretation | Records must not explain what a standard requires, prohibits, calculates, assures, certifies, or scores. |
| No comparison | Cross-framework notes must stay at relationship and dependency metadata level. |
| No compliance conclusion | Intake records cannot determine applicability, compliance, assurance, certification, or disclosure quality. |
| Review before use | Any future factual framework claim requires source freshness review and human review before reuse. |

## Framework Metadata Rules

| Metadata field | Intake rule |
| --- | --- |
| Framework identity | Use the official name or official family name where available. |
| Owner | Record the official publisher, standard-setter, regulator, taskforce, or responsible ministry. |
| Official website | Prefer official primary pages, official portals, or official legal/publication repositories. |
| Primary documents | Record document family names only. Do not summarize requirements. |
| Version | Record version, issue date, effective date, cycle, or page update signal where visible. |
| Update frequency | Record observed cycle or state "not specified on intake source". |
| Revision mechanism | Record observed consultation, amendment, project, portal, or errata mechanism where visible. |
| Document hierarchy | Distinguish framework, standard, recommendation, guidance, project page, questionnaire, legal act, and portal. |
| Evidence freshness | Record whether future use needs freshness, amendment, reporting-period, or cycle checks. |
| Runtime lens | Record future runtime relevance as metadata only. |

## Framework Identity

Framework identity is the stable label ClimateOS / CarbonOS may use to refer to a source family during later research.

Identity is not a claim that the framework applies to any entity, project, country, asset, disclosure, carbon inventory, or ESG conclusion.

## Framework Hierarchy

Intake records must distinguish:

- owner / publisher
- framework or standard family
- primary standard, report, recommendation, legal act, or questionnaire
- supporting guidance, basis, tools, taxonomies, portals, or project pages
- amendments, errata, updates, exposure drafts, consultations, and future-period versions

## Framework Lifecycle

Lifecycle metadata may include:

- assessment cycle
- annual disclosure cycle
- reporting-period version routing
- standard-setting project status
- amendment project status
- consultation status
- publication date
- update date
- effective date
- supersession or archive status

## Framework Version Relationship

Version relationship metadata must record whether a framework uses:

- named versions
- reporting periods
- assessment cycles
- annual questionnaires
- amendments
- project updates
- future-period versions
- official legal consolidation

## Framework Ownership

Ownership metadata must identify the official source authority. Where a framework ecosystem has multiple authorities, record the owners without merging their authority.

Example: China climate, carbon, and ESG materials may route through ministry, regulator, market, exchange, or standards bodies. Intake must preserve those boundaries.

## Dependency Principles

| Dependency type | Metadata treatment |
| --- | --- |
| Source dependency | Record upstream or related official source family only. |
| Evidence dependency | Record whether future use may require observations, inventory data, document evidence, questionnaire response data, or external datasets. |
| Runtime dependency | Record possible future runtime relevance only. No runtime is authorized. |
| Human review dependency | Flag where future use requires source freshness review, translation review, legal review, or domain expert review. |

## AEP Compliance

Task171-180 is an Enhancement Layer under the active Architecture Enhancement Protocol. It preserves Architecture Baseline v1.1 and does not freeze a new architecture baseline.

## Boundary Status

```text
Task171 Boundary Gate: COMPLETED
Framework intake authorized: YES, METADATA ONLY
Standards interpretation: NOT AUTHORIZED
Runtime / API / database / MCP / scoring / automation: NOT AUTHORIZED
QCloud: SUSPENDED
```
