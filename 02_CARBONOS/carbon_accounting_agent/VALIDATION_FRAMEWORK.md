# Carbon Accounting Validation Framework

## Purpose

These conceptual checks support preparation and review. They do not approve
inventories, claims, filings, or compliance.

## Completeness

Check whether expected facilities, activities, energy sources, periods,
categories, and required evidence are represented. Record exclusions and gaps.

## Consistency

Check identifiers, boundaries, dates, units, methods, classifications, and
versions across related records. Preserve unresolved conflicts.

## Traceability

Confirm that material values and interpretations link to identified evidence,
methods, factor references, owners, and transformations.

## Evidence Coverage

Compare evidence quantities, periods, locations, and boundaries with the
records they support. Partial coverage must remain explicit.

## Boundary and Period Alignment

Confirm that records belong to the declared organisational, facility, project,
product, or scenario boundary and accounting period.

## Green Power Interface

Confirm that Task51 classification identifiers, statuses, evidence,
uncertainty, and reviewer notes are preserved. `Unknown` and `Needs Review`
must not be treated as favorable classifications.

## Duplicate and Omission Review

Identify possible duplicate activity, energy, classification, or future
emission records, as well as missing expected records. Resolution remains a
human responsibility.

## Human Review

Every future inventory requires an identifiable human reviewer. Boundary
choices, factor selection, methodological interpretation, material gaps, and
public claims require qualified judgement.

## Uncertainty Recording

Record estimates, proxies, missing data, classification issues, factor
uncertainty, allocation assumptions, and method limitations without implying
unsupported precision.

## Invalid Inputs

Future logic should reject malformed records safely, preserve originals,
explain findings, and avoid silent coercion or default assumptions.

## Validation Boundary

Completed software checks would show only that declared rules ran. They would
not constitute professional assurance, audit, certification, regulatory
acceptance, or proof of environmental performance.
