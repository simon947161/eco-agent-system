# Green Power Classification Validation Rules

## Purpose

These conceptual rules describe checks for future implementation and human
review. They do not implement automated approval logic.

## Evidence Present

Confirm that a proposed classification references the evidence required by
its pathway. Missing evidence should result in `Unknown`, `Needs Review`, or
an explicit incomplete-evidence finding rather than a favorable assumption.

## Evidence Consistency

Compare organisation, facility, quantity, unit, reporting period, source,
contract, certificate, transaction, and allocation records for conflicts.
Record each unresolved inconsistency.

## Source Traceability

Confirm that each material fact can be traced to an identified source,
version, owner, and relevant period. Unsupported copied values or labels
should not be treated as verified evidence.

## Boundary Alignment

Confirm that consumption, generation, contract, certificate, transaction, and
allocation boundaries refer to the same declared reporting purpose or explain
their differences.

## Quantity and Unit Alignment

Check that quantities and units are declared and comparable. A future
implementation may identify over-allocation or incomplete coverage, but no
calculation is implemented in Task51.

## Temporal and Geographic Alignment

Check whether evidence periods and locations align with the declared
consumption and classification method. Misalignment should remain visible for
human review.

## Duplicate Recognition Risk

Identify evidence or quantities that appear to be transferred, allocated,
retired, or claimed more than once. The agent must not resolve ownership or
legal entitlement autonomously.

## Human Review Requirement

Every final classification remains subject to an identifiable human reviewer.
Conflicting pathways, incomplete evidence, unusual instruments, policy
interpretation, and material uncertainty require explicit review.

## Uncertainty Recording

Record estimates, missing intervals, proxy records, ambiguous rights,
methodological choices, and other uncertainty. Confidence descriptions must
not conceal unresolved issues.

## Invalid or Incomplete Inputs

Future logic should reject malformed records safely, preserve the original
evidence, explain validation findings, and avoid silently coercing a record
into a classification.

## Validation Boundary

Passing these checks would mean only that defined data and evidence checks
were completed. It would not establish legal compliance, regulatory
recognition, professional assurance, certificate validity, or environmental
benefit.
