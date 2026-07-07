# Task143 Cross-Standard Method Mapping Research Protocol

## Purpose

Task143 defines a research protocol for future cross-standard method mapping in CarbonOS.

The protocol covers how future work may research IPCC, ISSB, IFRS S2, ASRS, TNFD, China, EU, US, and other framework contexts before any factual standards content is recorded. This document does not explain those standards, interpret their requirements, or create a comparison table.

## Research Purpose

Future research may support CarbonOS by identifying source-backed information about:

- method categories
- formula references
- factor references
- boundary language
- evidence expectations
- disclosure or claim context
- review and citation status

The purpose is to prepare traceable research inputs for later architecture review. It is not to produce compliance guidance, assurance conclusions, certification opinions, legal interpretation, or public disclosure conclusions.

## Source Hierarchy

Future research should prefer sources in this order:

| Tier | Source Type | Use Boundary |
| --- | --- | --- |
| Tier 1 | Official primary source from the framework owner, regulator, standard setter, or responsible public body | Required before factual standard-specific statements become eligible for inclusion. |
| Tier 2 | Official implementation guidance, basis documents, consultation materials, or regulator notices | May support context, versioning, and interpretation questions, subject to review. |
| Tier 3 | Recognized professional, academic, or technical analysis | May identify issues or uncertainty, but cannot substitute for Tier 1 source support. |
| Tier 4 | Internal notes, prior repository documents, model recall, uncited memory, or informal summaries | May only generate research questions. They cannot support factual claims. |

## Citation Requirements

Every future factual standard-specific statement must include:

- source title
- source owner / publisher
- publication or effective date where available
- access date
- URL or stable locator where available
- version identifier where available
- section, paragraph, page, table, or clause locator where available
- reviewer and review state

Claims without sufficient citation metadata must remain marked as `Research Question`, `Unverified`, or `Not Eligible For Inclusion`.

## Freshness Requirements

Future research must record source freshness because standards and disclosure rules can change.

Minimum freshness controls:

- record access date for every source
- record publication date or effective date when available
- flag any source where currency is unknown
- re-check sources before reuse in later tasks
- avoid using stale repository notes as current authority
- require Founder / GPT review before treating any sourced statement as reusable

## Version Control Rules

Future research artifacts should record:

- source version
- retrieval date
- framework context
- jurisdiction or issuing body context
- change history when known
- replacement / supersession status when known
- reviewer notes
- unresolved version conflicts

If version status is unclear, the research item must remain blocked from factual inclusion.

## Review States

Allowed review states:

| Review State | Meaning |
| --- | --- |
| Research Question | A question or target for future source review. |
| Source Located | A possible source has been identified but not reviewed. |
| Citation Captured | Citation metadata has been recorded. |
| Primary Source Reviewed | A current primary source has been reviewed. |
| Cross-Checked | The finding has been checked against another reliable source or version note. |
| Founder / GPT Review Required | The finding cannot move forward until reviewed. |
| Eligible For Future Inclusion | The finding has enough citation and review support for later controlled use. |
| Rejected / Superseded | The finding is not safe to use or has been replaced. |

## Prohibited Uses Of Uncited Memory

Uncited memory, model recall, old repository notes, and prior informal summaries may not be used to:

- explain a standard
- compare requirements
- determine compliance
- identify required methods
- approve formulas or factors
- decide disclosure sufficiency
- support public or internal conclusions

They may only be used to generate research questions that must be checked against current sources.

## Eligibility For Future Factual Inclusion

A factual standards statement becomes eligible for future inclusion only when:

- it is supported by current source citation metadata
- the source hierarchy is recorded
- the version and access date are recorded
- the statement is narrow and traceable
- uncertainty and limitation notes are recorded
- it has passed the required review state
- it does not create compliance, assurance, certification, legal, or public disclosure authority

Eligibility does not mean approval for operational use.

## Standard-Specific Review Before Use

Before any standard-specific content is used in later tasks, it must pass:

- current source check
- citation completeness check
- version / freshness check
- scope and boundary check
- non-authoritative wording check
- Founder / GPT review

If any check fails, the content must stay out of CarbonOS comparative architecture artifacts except as an open research question.

## Task144 Handoff Boundary

Task144 may use this protocol to define source status and review state fields for a non-authoritative method and formula registry concept.

Task144 must not implement a registry, create formulas as authoritative content, perform calculations, or convert research protocol fields into operational capability.

## Status

```text
Task143 Cross-Standard Method Mapping Research Protocol: COMPLETED AS DOCUMENTATION-ONLY ARCHITECTURE WORK
Task144 Handoff: AUTHORIZED AS DOCUMENTATION-ONLY CONCEPT WORK
Standards Interpretation: NOT CREATED
Runtime / API / Database / MCP / Scoring / Automation Work: NOT CREATED
QCloud Builder Work: SUSPENDED
```
