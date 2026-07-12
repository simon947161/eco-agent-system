# Task1199 Founder Retest Gap Patch Record

Status: implemented and automated verification passed; Founder human retest pending

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
founder_human_retest: pending
pr_43_merge: not_authorized
task1200: not_started
```

## Boundaries

No live external data, authentication, multi-user runtime, public deployment, automatic scientific/compliance/legal/investment conclusion, external model, private EcoEngine access, PR merge or Task1200 work was added.
