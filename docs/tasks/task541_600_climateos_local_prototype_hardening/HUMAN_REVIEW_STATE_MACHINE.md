# Human Review State Machine

## Purpose

Task541-600 adds explicit local status-transition rules so candidate status changes cannot silently bypass Human Review boundaries.

## Candidate Statuses

- Draft Candidate
- Needs Source Verification
- Needs Translation Review
- Needs Human Review
- Blocked
- Founder Gate Required
- Human-Reviewed Candidate
- Archived
- Superseded

## Required Rules

- Status transitions must change the current status.
- Archived and Superseded records are terminal in the prototype.
- Blocked transitions require at least one linked risk flag.
- Founder Gate Required transitions require at least one linked risk flag and a Founder Gate trigger.
- Revoking Human-Reviewed Candidate status back to Needs Human Review requires linked risk context.
- Invalid transitions return a local conflict response and create a blocked-transition audit event.

## Boundary

The state machine is a local review-control mechanism. It does not approve evidence, verify claims, determine compliance, score records, certify records, assure records, or create an operational Evidence Passport.
