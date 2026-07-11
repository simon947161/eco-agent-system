# Task696 Audit Replay Rollback And Diagnostics

Alpha actions create append-only in-memory audit events with contiguous sequence
numbers. Diagnostics check sequence continuity and report evidence,
deliberation, and event counts.

Evidence records retain revision snapshots. A human can request rollback to an
available revision with a reviewer label and reason. Rollback creates a new
revision and audit event rather than deleting history.

Restart clears all Alpha state. This is a deliberate local skeleton boundary,
not durable audit storage.
