# Council Bridge validation and delivery status

Task CLIMATEOS-BRIDGE-COUNCIL-001. Date 2026-10-21, Australia/Sydney.

## Verified locally

- 14 new risk-oriented tests passed: node isolation, permissions, exact approvals, units/time/budget/classification, request idempotency, result mismatch rollback, timeout/failure/retry/cancel, provider replacement, synthetic review ceiling, expiry, export approval, privacy projection, source withdrawal, duplicate import, restart and audit inconsistency detection.
- Full repository suite: **496 tests run, OK, 1 skipped**. Existing tests regenerate four tracked legacy output files; those generated changes were inspected and restored. They are not part of this delivery.
- JavaScript syntax check passed.
- Desktop Chrome end-to-end check passed: prepare → approve → mock result → answer → human demo review → synthetic outcome → sharing preview → exact approval → second-Council metadata import. No browser page errors.
- Desktop 1440×1000 and mobile 390×844 screenshots captured and visually inspected. Wide evidence table scrolls within its container on mobile.
- HTTP tests verify bearer capability, exact Host, same-origin mutations, body type and unknown Council rejection. No live provider, Council internal source or private database was used.

Initial Windows sandbox test attempts could not access newly created Python temporary subdirectories. Normal-permission tests revealed an actual SQLite connection-lifetime problem, which was fixed with operation-scoped close. The reported passing results are from subsequent complete runs, not the failed attempts.

## Screenshots

- [Council overview](screenshots/overview.png)
- [Reviewed workflow](screenshots/reviewed-workflow.png)
- [Mobile view](screenshots/mobile.png)

Screenshots contain authored synthetic data and public candidate context only. They contain no session capability, personal records or real Council observations.

## Stage accounting

| Stage | Delivered | Honest limit |
| --- | --- | --- |
| 0 baseline | Rechecked main and specified remote records; reuse map and authority reconciliation | Not a full historical audit of every branch |
| 1 contracts/workspace | Council configuration, spatial relationships, provider Protocol, closed request, local UI | No admitted geographic boundary; schematic only |
| 2 local loop | Multiple place/resource objects, farm case lineage, mock run, existing-shaped answer/passport, review and outcome | All numerical records and execution synthetic; real evidence remains reference-only |
| 3 exchange | Two isolated local databases, exact-approved metadata exchange, duplicates, expiry/withdrawal sync | Same-host trusted broker; not signed distributed federation |
| 4 handoff | README, guide, baseline, unsent partner pack, tests and screenshots | Draft PR requires human review; no production activation |

## Not completed / gates for real use

1. Verify Council sponsorship and a real decision question.
2. Admit exact official geometry snapshot, feature identifier, source terms, attribution and transformation digest.
3. Admit representative observations and independent model evidence without broadening the old Cooma contracts.
4. Reconcile PR120/Task3000 through their own review; do not silently merge.
5. Verify Matrix One/MatchX/Ahmed/YLE identities and terms before any connection or contact.
6. Add real provider schema/quality/skill validation and explicit transfer/budget approval.
7. Implement multi-user identity, least privilege, signed remote transport, protected backups and revocation delivery before network deployment.

Design and synthetic validation are delivered. Real external integration and production deployment are **not** delivered or authorised.
