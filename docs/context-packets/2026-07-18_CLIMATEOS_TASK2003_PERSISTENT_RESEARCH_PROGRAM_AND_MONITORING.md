# ClimateOS Task2003 — Persistent Research Program + Monthly Review Cycle

Date: 2026-07-18

Base main: `c9c16a917c9469b38c204a1726f9497daa3a73b5`

Founder authorization: merge PR #88; build the green Persistent Research Program + Monthly Review Cycle; save the completed Cooma question as the first long-term project; start controlled real-network monitoring and Task2003+.

Implementation status: LOCAL CAPABILITY SLICE IMPLEMENTED / VALIDATED / DRAFT PR PENDING

## Capability milestone

Task2003 converts a one-time question session into a durable, versioned research program:

`Program → Monthly/Event Cycle → Evidence Snapshot → Difference → Hypothesis Version → Human Review → Receipt + Passport`

The first stable program identity is:

`COOMA-WATER-FIRE-WASTEWATER-WATCH`

It preserves the Founder question concerning observed water and snow conditions,
future bushfire and drinking-water risk, wastewater work and constraints, and
the role wastewater management might play in climate adaptation.

## Green scope

- durable SQLite research-program identity;
- monthly and material-event cadence policy;
- append-only monthly cycles;
- manually entered, dated human field observations;
- evidence snapshots and previous-cycle comparison;
- versioned hypothesis-state records;
- cycle Run Receipt, Evidence Passport and human review;
- no overwriting prior cycles or prior reviewed states.

## Time contract

- each monthly cycle records `period_start`, `period_end` and `review_due_on`;
- `review_due_on` is the last calendar day, not a hard-coded day 30;
- each field report records the human's `observed_on` date separately from the
  system `reported_at` timestamp;
- the original human wording is preserved as `verbatim_human_report` beside the
  confirmed date, place and category structure;
- a year-end report requires a human-reviewed December cycle and explicitly
  lists missing months rather than presenting incomplete coverage as complete.

## Conversation-to-Observation Inbox Bridge

Intended workflow:

`Human natural report → AI observation draft → human correction/confirmation → local private intake → monthly cycle`

The human is responsible for an honest account of what was observed. The AI is
responsible for preserving the original account, identifying missing date/place
fields, separating observation from interpretation, and never upgrading an
honest but incomplete report into an instrument measurement or verified fact.

Current state: `CONTRACT_DEFINED_NOT_CONNECTED_TO_LOCALHOST`. ChatGPT cannot
silently write into a SQLite database running on the Founder's computer. A
future authenticated MCP/API bridge may connect them after privacy, identity,
consent, failure and local-network controls are independently reviewed. Until
then, the local Web form is the admitted intake path.

## Controlled real-network monitoring scope

- public official HTTPS sources only;
- repository allowlist only;
- explicit human approval for every refresh;
- zero paid services, no credentials, no API keys;
- retain URL, retrieval time, response metadata, byte count and digest only;
- raw page bodies are not retained;
- content changes produce `CHANGE_CANDIDATE`, never an automatic scientific,
  operational, emergency, compliance or project conclusion;
- failed or redirected-outside-allowlist sources remain visible and do not
  silently become evidence.

## Prohibited data and conclusions

- no Council internal systems, customer records, personal information,
  non-public worksite evidence or employment records;
- no automatic bushfire warning, drinking-water shortage estimate, wastewater
  capacity conclusion or engineering recommendation;
- no claim that a changed webpage proves a changed environmental condition;
- GraphCast remains LATER;
- no Bondo/Riverina wind-resource or project-feasibility conclusion;
- Constellation Journey and WorkOS private materials remain isolated.

## Automation boundary

Task2003 records a monthly cadence and enables a human-approved live refresh.
It does not install an unattended local background service or automatically
publish alerts. Autonomous scheduling and notifications require a later,
separately tested operational gate because they create persistent external
behaviour and failure/alert obligations.

## Validation record

- `python -m unittest discover`: 329 tests passed on 2026-07-18.
- Targeted persistent-program and HTTP tests: 10 passed.
- Local smoke test served `/program.html` and returned the stable
  `COOMA-WATER-FIRE-WASTEWATER-WATCH` program identity.
- Official public entry verification found the allowlisted BOM climate-driver
  monitoring and long-range-outlook pages, NSW RFS fire-danger page (including
  the Monaro Alpine/Snowy Monaro area), and Snowy Monaro Council water and
  wastewater pages publicly reachable at verification time.
- The discontinued legacy BOM ENSO Outlook URL is not used; the allowlist uses
  the current Southern Hemisphere monitoring page.
