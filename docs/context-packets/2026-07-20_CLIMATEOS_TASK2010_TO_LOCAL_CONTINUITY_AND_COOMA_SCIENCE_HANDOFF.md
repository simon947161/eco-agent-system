# ClimateOS Task2010 to Local Continuity and Cooma Science — Handoff

Date: 2026-07-20

Status: AUTHORITATIVE_THREAD_TRANSFER / PR91_DRAFT / FOUNDER_COMPUTER_REVIEW_MOBILE_DEFERRED

Repository: `simon947161/eco-agent-system`

Authoritative main HEAD:

`043e90f74c26b8e8ba543395a9801c2304168b7f`

Current Draft PR: `#91`

Branch:

`agent/task2004-2010-monthly-research-operations`

Head before this handoff commit:

`eeaaba0898233678bbd503310aff2bafc5af0fde`

## 1. Closed and merged state

PR #89 is merged at `043e90f74c26b8e8ba543395a9801c2304168b7f`.
Task2003 is closed as an implemented and Founder-operated Persistent Research
Program milestone.

The first stable program is:

`COOMA-WATER-FIRE-WASTEWATER-WATCH`

The Founder completed two July 2026 cycles locally:

- one `MATERIAL_EVENT` cycle honestly reviewed as
  `CYCLE_REVIEWED_REVISION_REQUIRED` after a Refresh/Compile race exposed an
  inconsistent Receipt;
- one separate `MONTHLY` cycle with one unverified public-area observation, no
  source refresh, `network_used=false`, `AUD 0`, no environmental conclusion and
  final state `CYCLE_REVIEWED_ACCEPTED_AS_RESEARCH_RECORD`.

The race, lifecycle display and no-refresh Passport labels were repaired before
PR #89 merged. No Founder SQLite content was committed or migrated.

## 2. Current Draft PR #91

Task2004–2010 adds a resumable monthly research operations console:

- latest cycles first in the timeline;
- `Open stored cycle` control;
- restoration of observations, source outcomes, Difference, Receipt, Passport
  and human review;
- lifecycle-derived next action;
- controls locked outside their admitted state;
- opening a stored cycle does not rerun or rewrite it.

Fresh preflight at handoff preparation:

- open: YES;
- Draft: YES;
- merged: NO;
- mergeable: YES;
- base: authoritative main;
- `behind 0`;
- local full suite: 335 tests passed;
- GitHub Actions run #316: SUCCESS.

Do not merge PR #91 until the deferred Founder computer review or a later
explicit Founder waiver/decision.

## 3. Deferred Founder computer review

The Founder is currently mobile-only. The only current computer validation is:

`PENDING_FOUNDER_COMPUTER_REVIEW / MOBILE_DEFERRED / REMIND_AT_NEXT_COMPUTER_SESSION`

When the Founder next says that a computer is available, read:

`docs/tasks/task1701_2099_mechanism_scientist_runtime/TASK2010_FOUNDER_COMPUTER_REVIEW_REMINDER.md`

The review opens the accepted July MONTHLY cycle and the revised MATERIAL_EVENT
cycle from History, checks restored records and confirms that reviewed controls
are locked. Do not click Refresh during this UI review.

The older Task2001 `RETEST PENDING` items do not require returning to the port
8765 scalar demonstration. The Founder explicitly accepted that control
foundation, and Task2002/Task2003 supplied the superseding meaningful and
persistent Runtime tests.

## 4. What ClimateOS can say about Cooma now

ClimateOS can currently say only that:

- a durable supervised research program exists;
- the Founder reported an unverified visual observation;
- official-page retrieval metadata can be captured under explicit approval;
- changes and failures can be recorded as research signals;
- no admitted analysis establishes a Cooma environmental trend, causal link,
  forecast, bushfire warning, water-security estimate, wastewater capacity or
  adaptation conclusion.

This is workflow evidence, not an environmental conclusion.

## 5. Cooma conclusion ladder and indicative time

The Founder asked when ClimateOS could provide a Cooma environmental conclusion.
The answer depends on the claim class. These are planning estimates, not a
scientific promise or an activated task.

| Level | Potential output | Minimum missing work | Indicative elapsed time after activation |
|---|---|---|---|
| 0 | source and observation register | already available; remains non-conclusive | now |
| 1 | bounded descriptive evidence statement about a named period and variable | exact claim, official datasets/documents, provenance, quality checks, spatial/temporal coverage, uncertainty and human scientific review | about 4–8 weeks |
| 2 | multi-year trend assessment for snow/water/fire-related indicators | Level 1 plus defensible baselines, station/area representativeness, missing-data handling, trend methods, sensitivity checks and domain review | about 2–4 months |
| 3 | integrated future climate–fire–water–wastewater scenario conclusion | admitted projections/models, scenario definitions, infrastructure evidence, causal limits, cross-domain review and reproducibility dossier | about 4–9 months |
| 4 | operational, engineering, emergency, compliance or investment recommendation | responsible authorities, current operational/non-public evidence where lawful, accountable specialists, regulatory duties and formal sign-off | normally 6–12+ months and may remain outside ClimateOS authority |

The fastest honest target is one narrow Level-1 descriptive claim. Do not start
with “What will happen to Cooma?” Start with one measurable question, for
example a named historical period, indicator, source set and geographic scope.

## 6. Required work before the first bounded conclusion

1. choose one exact claim class and decision use;
2. set geographic and temporal scope;
3. approve named official evidence products and their licences;
4. acquire only the minimum required data/documents under a separate data gate;
5. validate completeness, units, dates, revisions and provenance;
6. assess whether stations/proxies represent the selected Cooma scope;
7. pre-register method, alternatives, uncertainty and stop conditions;
8. run reproducible descriptive analysis with no automatic causal upgrade;
9. create Receipt and Evidence Passport tied to exact inputs and code;
10. obtain a consenting, appropriately qualified scientific reviewer;
11. preserve dissent and limit the conclusion to the reviewed claim;
12. obtain Founder release approval for the exact wording and use.

Neither Zhang Lu nor Professor Chen Shiping is assumed, contacted, appointed or
represented as a reviewer. Any identity check, approach, consent, fee or review
remains a separate Founder gate.

## 7. Mainline next target

The immediate mainline target is not a Cooma conclusion. It is reliable local
continuity so the research program can grow without losing or leaking records.

Task2011–2020 candidate:

- local backup preview;
- canonical JSON manifest, schema version and digest;
- new-file export with overwrite refusal;
- small size ceiling and path/symlink controls;
- restore-difference preview without database mutation;
- human-confirmed observation-draft interchange;
- tests preventing local/private records entering Git history or logs.

The readiness plan exists at:

`docs/tasks/task1701_2099_mechanism_scientist_runtime/TASK2011_2020_LOCAL_PRIVATE_CONTINUITY_READINESS_PLAN.md`

Implementation has not started. The recommended first slice is backup preview
and new-file local export only, after PR #91 review.

## 8. Red and separately gated work

- real scientific data acquisition or broad official-source refresh;
- Cooma trend, forecast, causal, infrastructure or operational conclusion;
- external model/code/package download or installation;
- GraphCast, WRF, WRF-Chem or other model execution;
- automatic scheduling, alerts or publication;
- ChatGPT/MCP-to-localhost bridge;
- cloud/object storage, account, secret or payment;
- expert, Council, agency or developer contact;
- Bondo/Riverina wind-resource or project-feasibility conclusion.

GraphCast remains `LATER`.

## 9. Project isolation

Constellation Journey, David family testing, multi-screen game work, audio,
ecological game missions, time acceleration and interstellar strategy are
excluded. WorkOS private/customer/site material is excluded unless separately
admitted.

PR #90 is an independent Build Week/integrity Draft. Do not import it into the
ClimateOS Runtime branch or assume it is inherited by PR #91.

## 10. Required first response in the next thread

> Handoff received. PR #89 and Task2003 are treated as merged and closed at main `043e90f74c26b8e8ba543395a9801c2304168b7f`. PR #91 remains an open Draft awaiting a mobile-deferred Founder computer review; I will not merge it automatically. I will treat old Task2001 retest markers as superseded by their explicit acceptance and the completed Task2002/Task2003 Founder tests. The immediate mainline is local research continuity, while any Cooma environmental conclusion remains a separately activated scientific evidence gate. I will not access real data, contact reviewers, connect external services or form a Cooma conclusion without explicit authorization.

