# ESG Disclosure Conceptual Data Model

## Disclosure Record

**Purpose:** groups a disclosure-preparation subject, boundary, evidence, and
review status.

**Example fields:** disclosure ID, subject, boundary, period, source records,
statement type, owner, status, version, limitations.

**Relationships:** references verified CarbonOS records and governance notes.

## Disclosure Statement

**Purpose:** records a draft human-readable statement for review.

**Example fields:** statement ID, disclosure ID, text, source references,
assumptions, uncertainty, reviewer notes, approval status.

**Relationships:** belongs to a Disclosure Record and must trace to evidence.

## Evidence Summary

**Purpose:** summarises evidence used, missing, conflicting, or excluded.

**Example fields:** summary ID, evidence IDs, coverage, gaps, limitations,
access notes, review status.

**Relationships:** links CarbonOS evidence and verification records to a
Disclosure Record.

## Verification Summary

**Purpose:** carries forward verification findings and unresolved issues.

**Example fields:** verification summary ID, verification record IDs,
findings, exceptions, uncertainty, unresolved issues, reviewer, status.

**Relationships:** supports Disclosure Statements without replacing source
verification records.

## Governance Review Record

**Purpose:** records human ownership, review, and decision boundaries.

**Example fields:** governance ID, decision owner, reviewer, role, date,
decision boundary, approval status, restrictions.

**Relationships:** defines whether a Disclosure Record can proceed to later
human-controlled use.

## Stakeholder Context

**Purpose:** describes the intended audience and interpretation limits.

**Example fields:** audience, purpose, jurisdiction context, communication
channel, confidentiality, limitations, review requirements.

**Relationships:** informs Governance Review Records and Disclosure Statements.

## Scenario Disclosure Note

**Purpose:** labels hypothetical information and assumptions.

**Example fields:** scenario ID, baseline, horizon, assumptions, uncertainty,
evidence status, non-forecast statement, reviewer notes.

**Relationships:** references ClimateOS scenario concepts and CarbonOS scenario
records.

No entity is implemented in Task55. Future schemas must preserve identifiers,
versions, provenance, evidence status, uncertainty, and human authorship.
