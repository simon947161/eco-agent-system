# Task707-710 Replay Recovery Validation And Checkpoint

## Task707 Replay And Rollback

Each accepted Evidence Contract revision creates an immutable snapshot.
Rollback restores selected content as a new higher revision and creates a new
audit event; it does not erase intervening history.

## Task708 Restart Recovery

Creating a new application instance against the same SQLite file reloads
Evidence Contracts, deliberations and audit events. Diagnostics explicitly
report persistence and restart behavior.

## Task709 Validation

Tests cover restart recovery, schema idempotency, correction, rollback,
abstention, synthetic cross-domain cases and bounded concurrent writes.

## Task710 Checkpoint

The persistent core is suitable only for local controlled review. It has no
public identity layer, external connector, background execution or production
availability promise.
