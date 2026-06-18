# Carbon Accounting Workflow

## Purpose

This is a narrative workflow for future implementation. It performs no
calculations and creates no executable process.

```text
Activity Data
  |
  v
Energy Records
  |
  v
Green Power Classification
  |
  v
Carbon Accounting Records
  |
  v
Inventory Review
  |
  v
Verification Preparation
  |
  v
Disclosure Preparation
```

## 1. Activity Data

Collect bounded operational records with source, period, quantity, unit,
owner, evidence status, and uncertainty. Missing records remain explicit.

## 2. Energy Records

Organise electricity, fuel, heat, steam, and other energy evidence. Reconcile
facility, meter, invoice, contract, and reporting-period references without
inventing missing values.

## 3. Green Power Classification

Attach reviewed Task51 classification results to relevant electricity records.
Preserve `Physical`, `Trading`, `Allocation`, `Unknown`, or `Needs Review`
status together with evidence, validation, uncertainty, and review notes.

## 4. Carbon Accounting Records

Future approved logic may combine activity data with declared methods and
emission factors to create emission records. Task52 defines only the record
structure and requires factor provenance, method version, assumptions, and
uncertainty.

## 5. Inventory Review

Group records under a declared boundary and accounting period. Review
completeness, consistency, exclusions, duplicate records, unresolved
classifications, method versions, and uncertainty.

## 6. Verification Preparation

Prepare evidence indexes, record lineage, validation findings, assumptions,
exceptions, changes, and reviewer notes for a future verification workflow.
Preparation is not assurance.

## 7. Disclosure Preparation

Prepare human-readable summaries with boundaries, periods, methods, evidence,
status, uncertainty, exclusions, and limitations. Disclosure preparation does
not authorize filing or public claims.

## Review Loops

Any stage may return records for correction when evidence, boundaries, periods,
units, classifications, methods, or assumptions conflict. Revisions should be
versioned and must not erase source or review history.
