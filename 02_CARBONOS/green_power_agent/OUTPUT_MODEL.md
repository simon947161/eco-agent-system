# Green Power Classification Output Model

## Purpose

This document defines conceptual outputs for future implementation. Task51
does not generate these outputs.

## Classification Result

Records the proposed attribution pathway for a bounded consumption record.

**Example fields:** result ID, consumption record IDs, classification status,
classified quantity and unit, reporting period, method version, evidence
references, reviewer, review date.

**Allowed conceptual statuses:**

- `Physical`
- `Trading`
- `Allocation`
- `Unknown`
- `Needs Review`

`Needs Review` indicates that a proposed classification cannot be finalized
without human examination. `Unknown` indicates that current evidence does not
support a pathway.

## Confidence Level

Provides a transparent qualitative description of evidence support. It must
not be interpreted as statistical certainty or regulatory acceptance.

**Example values:** `High Evidence Support`, `Moderate Evidence Support`,
`Low Evidence Support`, `Not Assessed`.

The criteria for any confidence vocabulary require a later approved task.

## Evidence Summary

Lists supporting and conflicting evidence, source provenance, coverage period,
quantity coverage, missing information, and evidence status.

The summary should distinguish source facts from interpretations and should
not replace the underlying evidence.

## Review Notes

Records reviewer observations, assumptions, unresolved questions, conflicting
pathways, requested corrections, and decision boundaries.

Review notes should identify the reviewer role and date without overwriting
the original proposed result.

## Validation Status

Records whether conceptual checks have been considered.

**Suggested values:** `Not Checked`, `Checks Complete`, `Issues Found`,
`Incomplete Evidence`, `Human Review Required`.

A validation status is not an approval, certificate, assurance opinion, or
compliance decision.

## Human-Readable Output

A future classification summary should include:

- organisation, facility, consumption boundary, period, quantity, and unit;
- proposed classification and confidence description;
- evidence used and evidence missing;
- validation findings and uncertainty;
- human review status and reviewer notes; and
- limitations and prohibited interpretations.

## Runtime Status

`Not implemented`. Field types, schemas, serialization, compatibility, and
machine-readable interfaces require a separate implementation task.
