# Data Integrity Diagnostics

## Purpose

The diagnostics layer gives reviewers a local way to identify data-quality risks in the prototype database.

## Diagnostic Checks

- Required table presence.
- SQLite foreign-key violations.
- Candidate status validity.
- Archived status and `archived_at` consistency.
- Duplicate relationship records.
- Orphan Human Review records.
- Founder Gate references to missing candidates.
- Invalid Founder Gate affected-record JSON.
- Superseded records without a supersession relationship.

## Status Values

Diagnostics return:

- `healthy`
- `warning`
- `failed`

## Boundary

Diagnostics are not scoring, verification, compliance review, assurance review, certification review, ESG assessment, carbon accounting, standards interpretation, or framework interpretation. Diagnostics only identify local prototype record conditions for human review.
