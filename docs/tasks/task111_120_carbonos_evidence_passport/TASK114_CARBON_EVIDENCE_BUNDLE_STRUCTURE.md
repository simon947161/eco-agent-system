# Task114 Carbon Evidence Bundle Structure

## Purpose

Task114 defines how carbon and ESG claim evidence is grouped and structured for human review.

The evidence bundle is a **documentation concept only**. It is not a database schema, runtime object, API response, file format, ZIP package, or software structure. It defines how humans should group evidence when preparing a claim for governance review.

## Evidence Bundle Concept

An **evidence bundle** is a grouped set of observations and sources that support a specific carbon or ESG claim.

The bundle is structured so that a human reviewer can:
1. See what evidence exists
2. Assess whether it is sufficient for the claim
3. Identify gaps or conflicts
4. Determine whether expert review is required
5. Trace each piece of evidence to its source

The bundle does **not**:
- Constitute verified evidence on its own
- Replace expert review when triggered
- Authorize any action
- Represent a compliance or assurance opinion

## Evidence Bundle Structure (Documentation Template)

```markdown
# Evidence Bundle for Claim: [Claim ID]

## Bundle Metadata
- Assembled By: [Human reviewer name/role]
- Assembly Date: [YYYY-MM-DD]
- Claim ID: [references Claim Intake Record]
- Evidence Period: [start date — end date]
- Boundary: [organizational, operational, geographic boundary of the claim]

## Bundle Structure by Evidence Type

### 1. Activity Data
[ Organized by emission source category, not by file format. ]

#### Stationary Combustion
- Source: [meter ID / invoice # / supplier]
- Period: [start — end]
- Raw data reference: [file, sheet, row]
- Observation: [human-readable statement of what was recorded]
- Provenance: [who provided, when, under what controls]
- Gaps: [missing periods, unverified sources, estimation methods used]
- Preliminary sufficiency note: [reviewer preliminary assessment]

#### Mobile Combustion
[Same structure as above]

#### Purchased Electricity
[Same structure as above]

#### Other Relevant Sources
[Same structure as above]

### 2. Emission Factors and Calculation Methods
[ Organized by method source and applicability. ]

#### Method Used
- Methodology: [GHG Protocol / EPA / ISO / other]
- Version: [year/version]
- Scope: [which emissions the method covers]
- Limitations: [known method limitations for this claim]

#### Emission Factors
- Source: [government agency / database / literature]
- Factor Value: [value and units]
- Applicability: [why this factor is appropriate]
- Uncertainty: [known factor uncertainty]

### 3. Boundary and Scope Documentation
[ Documents what is and is not included in the claim. ]

- Organizational boundary: [equity share / control approach]
- Operational boundary: [which emission sources are included]
- Exclusions: [what is explicitly excluded and why]
- Changes from prior period: [boundary changes and justification]

### 4. Supporting Third-Party Documents
[ Organized by document type and relevance. ]

- Certificates: [registry, serial, issuance date, retirement date]
- Assurance reports: [scope, standard, conclusion]
- Audit records: [scope, finding summary]
- Supplier statements: [scope, limitations]
- Other: [describe]

### 5. Conflict and Gap Log
[ Explicitly documents contradictions and missing data. ]

- Conflicting sources: [description, how resolved or escalated]
- Missing critical data: [description, impact on claim]
- Estimation methods used: [description, uncertainty, expert review triggered]
- Data quality issues: [description, impact on evidence sufficiency]

## Evidence Sufficiency Assessment (Preliminary)

[ This section is expanded in Task115 human review workflow.
  This preliminary assessment is not a final sufficiency determination. ]

- Evidence completeness: [preliminary assessment]
- Evidence quality: [preliminary assessment]
- Confidence level: [preliminary assessment]
- Expert review triggered: [yes/no/pending final assessment]
- Preliminary recommendation: [proceed / request data / escalate to expert / do not use for disclosure]
```

## Evidence Bundle Discipline Requirements

The evidence bundle must maintain evidence discipline:

| Term | Placement in Bundle | Requirement |
|------|---------------------|-------------|
| Raw data | Raw data references in each evidence type section | Listed as source only; not presented as evidence without processing |
| Observation | "Observation" field in each evidence type section | Clearly distinguished from inference |
| Inference | "Uncertainty" and "Limitations" fields | Labelled as provisional; not a claim or conclusion |
| Evidence | Combined observations sufficient for the specific claim | Must be sufficient in quality, provenance, and relevance |
| Claim | References Claim Intake Record | Not restated in full; referenced |
| Recommendation | "Preliminary recommendation" field | Not presented as authorization or approval |

## What the Bundle Is and Is Not

| The bundle **is** | The bundle **is not** |
|-------------------|-----------------------|
| A documentation structure for grouping evidence | A database schema |
| A human-readable organization method | A runtime object |
| A way to present evidence for review | An API response |
| A sufficiency assessment framework | A compliance engine |
| A conflict and gap identification method | An assurance opinion |
| A traceability structure | An automated decision |

## Bundle Assembly Principles

1. **Group by evidence type, not by file format** — the bundle structure helps the reviewer, not the file system
2. **Separate observations from inferences** — uncertain interpretations must be labelled
3. **Document gaps explicitly** — missing data is not "immaterial" by default
4. **Log conflicts** — contradictory sources must be disclosed and escalated
5. **State provenance** — every piece of evidence needs a source and controls statement
6. **Flag expert review triggers** — do not assess sufficiency without checking triggers

## Task102-110 Relationship

The evidence bundle structure expands:

| Task102-110 Deliverable | Expansion in Task114 |
|------------------------|-----------------------|
| Task103 Evidence Discipline Model | Enforced through bundle structure |
| Task104 Claim Review Template | Expanded into evidence type sections |
| Task105 Evidence Sufficiency Checklist | Referenced in preliminary assessment |
| Task106 Responsibility Boundary | Assembler identified in metadata |

## Evidence Bundle and Evidence Passport Relationship

The evidence bundle is **part of** the Evidence Passport.

| Concept | Contains |
|---------|-----------|
| Evidence Bundle | The evidence, grouped by type, with provenance and gaps |
| Evidence Passport | The bundle + claim statement + sufficiency assessment + responsibility + triggers + governance boundary + decision log |

The bundle is the evidence foundation. The passport is the complete governance review package.

## Task114 Status

```text
Task114: COMPLETE — Carbon Evidence Bundle Structure defined.
```

Task115 may proceed (define human review workflow).

---

**Status**: Draft
**Authority**: Task111-120 - QCloud Builder
**Date**: 2026-07-05
