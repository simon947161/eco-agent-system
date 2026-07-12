# Task1199 Founder Retest Gap Patch Record

Status: implemented, automated verification passed and Founder human retest accepted; not merged

## Purpose

Close only the two gaps reported during the Founder limited local Beta retest: existing Alpha Evidence correction and ordinary list ordering.

## Root cause and repair

The runtime already preserved revision snapshots, review history, rollback history and append-only audit events. The browser exposed no load-existing-record action and its correction payload could replace only the summary. The patch wires an existing record into explicit title, summary and uncertainty correction fields. Submitting the correction creates the next revision; it does not overwrite or delete the prior revision.

Evidence Cards, Audit Trail and loaded Alpha lists now have labelled Sort by and Direction controls. Defaults are Date/time plus Newest first, with record ID as a deterministic tie-break. Sorting is browser presentation only and does not mutate stored data or imply priority, quality, score, truth or scientific importance.

## Verification

```yaml
automated_tests: 61_passed
existing_warning: one_TestClient_deprecation_warning
javascript_syntax: passed
diff_check: passed
founder_human_retest: passed_2026_07_12
tested_record: ALPHA-EVIDENCE-b1298ad52e61
tested_domain: water
tested_case: Cooma_synthetic_water_backflow_liquid_trade_waste
update_and_revision: passed_revision_3
revision_history: revisions_1_2_preserved
review_history: dispute_and_correct_preserved
sorting: date_title_ascending_descending_passed
restart_recovery: passed
browser_reload_existing_record: passed
pr_43_merge: not_authorized
task1200: not_started_pending_fresh_preflight_and_authorization
```

## Founder observation

After restart, the direct record endpoint and the Alpha Review load-existing-record action both recovered revision 3 and its prior history. The left-hand Create synthetic evidence form intentionally remained a separate new-record form; it was not the recovered record editor. This distinction was explained and accepted, while clearer future wording remains a minor usability opportunity rather than a Task1199 blocker.

## Acceptance decision

The Founder accepted the bounded Task1199 retest on 2026-07-12. This closes the reported update/revision and sorting gaps. It does not merge Draft PR #43 and does not itself authorize Task1200 implementation. Task1200 remains subject to its fresh scientific, repository, licence, data and compute preflight plus an explicit bounded Founder authorization.

## Boundaries

No live external data, authentication, multi-user runtime, public deployment, automatic scientific/compliance/legal/investment conclusion, external model, private EcoEngine access, PR merge or Task1200 work was added.
