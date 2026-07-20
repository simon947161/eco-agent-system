# ClimateOS Task2004–2010 — Monthly Research Operations Console

Date: 2026-07-20

Status: IMPLEMENTED / LOCAL_ONLY / NO_SOURCE_ACCESS

Base main: `043e90f74c26b8e8ba543395a9801c2304168b7f`

## Outcome

Task2004–2010 turns the Task2003 monthly form into a resumable local operations
console. A human can close the page or stop the localhost process, return later,
open a stored cycle from the timeline and inspect the exact persisted record.

Opening a cycle is read-only by default. It does not create another cycle,
repeat a source refresh, compile again, change a review or rewrite SQLite.

## Task map

| Task | Capability |
|---|---|
| 2004 | define the resumable-cycle product need and no-rerun boundary |
| 2005 | add timeline controls for opening a stored cycle |
| 2006 | restore observations and source-outcome metadata into the workspace |
| 2007 | restore Difference, Receipt and Evidence Passport views |
| 2008 | show a state-derived next action and lock non-admitted controls |
| 2009 | verify accepted-cycle reopening through the localhost HTTP interface |
| 2010 | close the capability milestone and return the next decision gate |

## State behaviour

- `COLLECTING_EVIDENCE`: observation entry and admitted refresh/compile controls
  remain available subject to the existing refresh state gate.
- `COMPILED_AWAITING_HUMAN_REVIEW`: collection controls are locked and the four
  human review decisions remain available.
- reviewed states: the cycle is historical and read-only; the stored human
  decision, Receipt and Passport are displayed.
- interrupted refresh: Compile remains locked and the existing retry rule is
  preserved.

## Evidence and privacy boundary

- no real source was refreshed;
- no raw page, meteorological dataset, model, GIS or external code was accessed;
- no account, secret, cloud service, external contact or cost was introduced;
- no Cooma, Bondo or Riverina environmental conclusion was formed;
- the Founder's accepted July 2026 record is not stored in GitHub and is not
  migrated or rewritten by this change;
- GraphCast remains `LATER`;
- Constellation Journey and WorkOS material remain excluded.

## Verification

The local test suite verifies that an accepted cycle can be fetched again with
its accepted state, observation and no-refresh Passport intact. Static Web
checks verify the timeline open control, workspace restoration function and
explicit no-rerun explanation.

