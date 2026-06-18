# Carbon Verification Conceptual Data Model

## Evidence Record

**Purpose:** identifies a source reviewed or requested.

**Example fields:** evidence ID, type, source, owner, period, version, status,
location, limitations, confidentiality.

**Relationships:** supports or conflicts with Accounting, Budget, or
Verification Records.

## Verification Record

**Purpose:** groups a defined review scope, method, evidence, findings, and
status.

**Example fields:** verification ID, subject, boundary, period, reviewer,
review criteria, evidence IDs, findings, limitations, status, version.

**Relationships:** contains Review Notes, Uncertainty Records, Traceability
Records, and Reviewer Observations.

## Accounting Record

**Purpose:** references an upstream Carbon Accounting record under review.

**Example fields:** accounting ID, inventory ID, boundary, period, method,
source version, uncertainty, review status.

**Relationships:** may be supported by Evidence Records and linked through
Traceability Records.

## Budget Record

**Purpose:** references an upstream target, allocation, actual, or variance
record.

**Example fields:** budget ID, record type, boundary, period, source inventory,
version, assumptions, uncertainty, status.

**Relationships:** links to Accounting Records, evidence, and findings.

## Review Note

**Purpose:** records a question, exception, response, or requested action.

**Example fields:** note ID, subject, author, date, category, text, owner,
due date, resolution status.

**Relationships:** belongs to a Verification Record and may reference evidence.

## Uncertainty Record

**Purpose:** records a source and interpretation of uncertainty.

**Example fields:** uncertainty ID, subject, source, description, significance,
evidence, owner, treatment, status.

**Relationships:** applies to evidence, accounting, budget, or scenario records.

## Traceability Record

**Purpose:** records a link between a statement or derived record and its
sources, methods, and versions.

**Example fields:** trace ID, subject ID, source IDs, transformation reference,
method version, completeness, issues, reviewer.

**Relationships:** connects CarbonOS records to Evidence Records.

## Reviewer Observation

**Purpose:** preserves a reviewer's bounded observation without changing the
source record.

**Example fields:** observation ID, reviewer, role, date, subject, observation,
basis, significance, recommendation, status.

**Relationships:** belongs to a Verification Record and may create Review Notes.

No entity is implemented in Task54. Future schemas must preserve identifiers,
provenance, versions, status, uncertainty, and human authorship.
