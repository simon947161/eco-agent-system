# ClimateOS Task901-1000 Founder Gate Brief

Version: v0.1

Date: 2026-07-11

Status: Founder-authorized start; execution in progress

## Purpose In Plain Language

Task901-1000 asks whether the local ClimateOS Alpha is understandable and safe
enough to prepare for a limited local Beta. It does not turn the prototype into
a public product.

The phase combines two different kinds of evidence:

1. checks Codex can complete now, including automated accessibility structure,
   security boundaries, deliberation rules, persistence and regression tests;
2. human evidence that only Shu Min and a later independent observer can
   provide by actually using the interface without hidden assistance.

The second kind cannot be fabricated or marked passed in advance.

## Starting Point

- repository: `simon947161/eco-agent-system`;
- branch: `task46-repository-control-codex-batch-queue`;
- authorized starting SHA: `f533f32ea20bffc8689d37f2aaed33272ce3e4c6`;
- worktree and origin aligned at `0/0`;
- Task741-900 closed with 48 passing tests;
- schema remains v3;
- Task901 was not started before this gate.

## Task Map

### Task901-920 - Founder Human Test Preparation And Execution

Prepare the test task card, observation sheet, safe local start instructions
and acceptance rules. Shu Min completes the real test. Until then this batch is
`WAITING_FOR_FOUNDER_HUMAN_TEST`.

### Task921-940 - Independent Observer Test

Prepare a no-prompt observer protocol. A second person operates the Alpha while
Shu Min observes without helping. This may occur after the Founder self-test
and is not silently replaced by automated testing.

### Task941-960 - Accessibility Review

Run automated semantic and responsive checks now. Later add keyboard-only,
200% zoom and Windows Narrator observations from a real browser session.

### Task961-980 - Validation Security Deliberation And ESG++ Review

Recheck localhost controls, request limits, evidence history, correction,
escalation, abstention, audit, backup, restore and governance-translation
boundaries. ESG++ remains a translation boundary; it cannot issue disclosure,
compliance, assurance, scoring or certification conclusions.

### Task981-1000 - Beta-Readiness Decision And Closure

Reconcile automated and human evidence. Choose `READY`, `CONDITIONALLY_READY`
or `NOT_READY` for a limited local Beta preparation phase. Close at Task1000
only after the required human evidence exists. Task1001 is a hard stop.

## Technical Envelope

Allowed work remains limited to the existing localhost Python/FastAPI, SQLite
v3, local HTML/CSS/JavaScript, synthetic/public-safe fixtures, tests and
documentation. Changes must be small, evidenced and manually initiated.

## Prohibited Scope

No private EcoEngine or `D:\eco_engine_v200`, live data, external model, MCP,
n8n, QCloud, authentication, multi-user system, automated approval, autonomous
agent, background worker, scheduler, scoring, certification, compliance,
assurance, public disclosure conclusion, cloud persistence, telemetry,
deployment, release, merge, tag or Task1001 is authorized.

## Completion Rule

Automated green tests are necessary but insufficient. Task1000 must not be
closed until the Founder self-test is recorded. Independent observer and
assistive-technology findings must either be recorded or explicitly carried as
Beta blockers; they cannot be called passed without a person performing them.
