# ClimateOS Task2001 — Build Week Founder Human Composite Review Gate

Date: 2026-07-18

Status: AUTHORIZED / STARTED / BLOCKER FIXES IMPLEMENTED / FOUNDER RETEST PENDING

Founder authorization:

- `AUTHORIZE_PR86_FREEZE_MERGE`
- `AUTHORIZE_TASK2001_CONTROLLED_HUMAN_REVIEW`

Frozen baseline:

- repository: `simon947161/eco-agent-system`
- merged pull request: `#86`
- main merge commit: `b0294ff23224fd4b7903254c9ec5104c3ca6428c`
- retained capability commit: `c015438608a851357e55f59ebf88608a1be20cbd`
- Task2000 decision: `ACCEPT_RUNTIME_DEMO`
- Task2000 session: `MECH-SESSION-5473B2E44F2540FA`

## 1. Original meaning

Task2001 is the first Founder-operated human review of the frozen Minimum
Human–AI Scientist Interaction Runtime. It tests whether Simon can understand,
control, inspect and review one real local tiny-synthetic session without relying
on the Task2000 implementation narrative.

Task2001 does not redesign ClimateOS, introduce a new long-term architecture, or
authorize Task2002+. It is a human composite review gate for Build Week.

## 2. Required interaction

The review must examine this complete intended journey:

```text
human question
-> structured experiment plan
-> explicit human approve / reject / revise
-> local controlled tiny-synthetic execution
-> result
-> Evidence Passport
-> Run Receipt
-> human accept / question / revise / re-run
```

The review must distinguish a genuinely executable transition from a label,
static screen or architecture description.

## 3. Fixed boundaries

- zero external cost;
- localhost only for this review;
- repository-authored fictional tiny-synthetic data only;
- no arbitrary code execution;
- no network service, API, model account, secret or external data;
- no scientific, environmental, regional, engineering or investment conclusion;
- GraphCast remains `LATER`;
- no Bondo/Riverina wind-resource or project-feasibility conclusion;
- Constellation Journey and WorkOS private materials remain isolated;
- no weakening of approval, evidence, receipt, quarantine or audit gates.

Any public deployment is a separate Build Week delivery decision and is not
authorized by this local human review contract.

## 4. Founder review procedure

### 4.1 Start

From the repository root at the frozen baseline or its Task2001 review branch:

```bash
python run_scientist_runtime.py --db runtime_data/task2001_founder_review.sqlite3
```

Open:

```text
http://127.0.0.1:8765
```

Use this boundary-safe question, or another question that stays entirely inside
the fictional sealed scalar box:

```text
In the fictional sealed scalar box, does the fixed perturbation increase the
response index compared with the fixed baseline?
```

### 4.2 Baseline pass

Simon personally attempts to:

1. create the question;
2. inspect the structured hypothesis and experiment plan;
3. understand limitations, falsification criteria and resource ceiling;
4. approve, reject or revise the plan;
5. approve one exact plan and run it;
6. inspect the result, Run Receipt and Evidence Passport;
7. verify that the Passport remains non-environmental;
8. accept, question, revise or re-run;
9. record any missing action, unclear label, error or dead end.

A missing UI action is recorded as a failure or friction point. It must not be
marked successful merely because a lower-level Python method exists.

### 4.3 Validation pass after blocker fixes

If the baseline pass finds a Build Week blocker, only the smallest fix necessary
to complete the intended journey may be implemented. Simon then repeats the
affected path and records whether the blocker is resolved.

Task2001 remains open until Simon submits the final decision in section 6.

## 5. Human review record

This section must be completed from Simon's direct experience. Do not infer or
pre-fill observations on his behalf.

- reviewer: Simon / Founder
- review started at: 2026-07-18 13:25 AEST (first startup attempt)
- review completed at:
- operating system: Windows (version not yet recorded)
- browser: Microsoft Edge
- Python version: Python 3.14 family inferred from the reported `Python314` executable path; exact patch version pending
- baseline commit:
- reviewed commit:
- Runtime session ID: `MECH-SESSION-096A9CA000F7443D`
- hypothesis ID: `MECH-HYP-282828C614DD655A`
- Run Receipt ID: `MECH-RUN-RECEIPT-F94B32C73448C6BB`
- Evidence Passport ID: `MECH-EVIDENCE-PASSPORT-5AA4237F899D4398` (recovered read-only from local SQLite because the Web card omitted it)
- audit chain valid: YES (Founder screenshot)
- time to first successful session:
- external cost observed:
- network dependency observed: NO — Receipt displayed `Network: not used`

### Direct evidence note

At 2026-07-18 13:53 AEST, Simon supplied a screenshot showing the final Human review panel with `REVIEWED_DEMO_ACCEPTED`, a human-readable statement that the supervised workflow completed, and `Environmental release: blocked`. This verifies the Founder personally completed the main acceptance path. Artifact identifiers were outside the first captured viewport. Follow-up screenshots at 13:56 AEST verify Receipt `MECH-RUN-RECEIPT-F94B32C73448C6BB`, `RECEIPT_STRUCTURALLY_ACCEPTED`, `FIXED_EXECUTOR_COMPLETED`, wall time `0.048516 s`, output `503` bytes, no network, valid audit chain, Passport state `SUPPORTED_SYNTHETIC_ONLY`, quarantine state `REVIEWED_BUT_REMAINS_NON_ENVIRONMENTAL_DEMO`, diagnostic `3.5`, and both non-environmental limitations. The Web UI does not render the Passport ID; Simon recovered `MECH-EVIDENCE-PASSPORT-5AA4237F899D4398` with a read-only SQLite query. The same output verified Session `MECH-SESSION-096A9CA000F7443D`, Hypothesis `MECH-HYP-282828C614DD655A`, Receipt `MECH-RUN-RECEIPT-F94B32C73448C6BB`, and final state `REVIEWED_DEMO_ACCEPTED`.

### Step record

| Step | Directly completed? | Friction or failure | Severity | Suggested change |
|---|---|---|---|---|
| Open Runtime | YES AFTER RETRY | First attempt failed because PowerShell was outside the repository; after receiving clone/location and `cd` instructions, Simon reported that the Runtime website opened successfully. | DOCUMENTATION BLOCKER | Add permanent first-time Windows clone, directory and launch instructions to the Build Week README. |
| Enter/select question |  |  |  |  |
| Understand structured plan |  |  |  |  |
| Approve plan |  |  |  |  |
| Reject plan |  |  |  |  |
| Modify plan |  |  |  |  |
| Run controlled experiment | YES | Simon supplied a 2026-07-18 13:53 AEST screenshot of the completed Human review panel. | NONE ON SUCCESS PATH | Preserve the working controlled-run path. |
| Understand result | YES | Founder screenshot shows the completed fixed executor and diagnostic `3.5`; the meaning of the synthetic numbers required separate explanation. | T2001-002 REMAINS | Add plain-language labels and interpretation. |
| Inspect Evidence Passport | YES WITH IDENTIFIER GAP | Screenshot shows `SUPPORTED_SYNTHETIC_ONLY`, `REVIEWED_BUT_REMAINS_NON_ENVIRONMENTAL_DEMO`, diagnostic `3.5`, and both limitations. The Passport ID is not rendered by the Web UI. | HIGH | Render the Passport ID and explain the Passport/Receipt distinction. |
| Inspect Run Receipt | YES | Receipt `MECH-RUN-RECEIPT-F94B32C73448C6BB` is `RECEIPT_STRUCTURALLY_ACCEPTED`; termination `FIXED_EXECUTOR_COMPLETED`; wall time `0.048516 s`; output `503` bytes; network not used; audit chain valid. | NONE ON CORE RECORD | Preserve these fields and improve copyability. |
| Accept/question result | PARTIAL | Simon personally selected `Accept runtime demo`; the page displayed `REVIEWED_DEMO_ACCEPTED` and `Environmental release: blocked`. The alternative question/revise path remains unavailable. | BLOCKER FOR ALTERNATIVE PATHS | Retain acceptance and add honest question/revise controls. |
| Modify and re-run |  |  |  |  |

### Evidence and comprehension questions

- Was it clear that the structuring assistant is deterministic and not an
  external LLM?
- Was the human approval gate explicit and unavoidable?
- Could a run occur before approval?
- Were result, receipt and Passport visibly distinguishable?
- Was the fictional/non-environmental boundary unmistakable?
- Could Simon recover from a rejection or requested revision?
- Could Simon repeat the experiment without manually editing SQLite?
- Which single point caused the most uncertainty?

### Issues

| ID | Description | Reproduction | Severity | Build Week blocker? | Resolution |
|---|---|---|---|---|---|
| T2001-001 | First-time startup instructions assumed the shell was already inside a local repository checkout. | From the Windows Desktop directory, run `git switch main`, `git pull --ff-only`, then `python run_scientist_runtime.py ...`; Git reports `not a git repository`, Python reports file not found, and localhost refuses the connection. | BLOCKER | YES | IMPLEMENTED / RETEST PENDING — README now includes first-time Windows clone, directory, launch and keep-open instructions. |
| T2001-002 | The default question and page use unexplained terms such as `fictional sealed scalar box`, `fixed perturbation`, `response index` and `baseline`, so the Founder cannot tell what the question means or why it matters. | Open the Runtime and read the default question before creating a session. Simon directly reported that he did not understand it and asked whether he could enter a meaningful question of his own. | BLOCKER | YES | IMPLEMENTED / RETEST PENDING — the page now uses a plain-language fixed-number question and explains the workflow-only purpose. |
| T2001-003 | The question field suggests free-form AI interpretation, but the current deterministic assistant does not semantically interpret arbitrary questions; permitted wording is attached to the same fixed synthetic plan. | Enter a different boundary-safe question and propose a plan; inspect that the fixed fixture and fixed experiment structure remain unchanged. | HIGH | YES | IMPLEMENTED / RETEST PENDING — the question and hypothesis panels explicitly state the deterministic template limitation. |
| T2001-004 | The Web Passport card omits `passport_id`, preventing the Founder from capturing the required artifact identifier from the demonstrated UI. | Complete a run and inspect section 05. Receipt ID is visible, but the Passport card renders only state, quarantine state, diagnostic and limitations. | HIGH | YES | IMPLEMENTED / RETEST PENDING — section 05 now renders Session and Passport identifiers alongside Receipt evidence. |
| T2001-005 | The Web flow did not expose explicit plan rejection, bounded hypothesis revision, result rejection, or a recovery/re-run path. | Complete or reject a session and inspect the available controls. | BLOCKER | YES | IMPLEMENTED / RETEST PENDING — UI and HTTP adapter now expose reject, audited wording revision, result rejection, and a new-session recovery path requiring fresh approval. |

### Blocker-fix implementation checkpoint

- implementation branch: `agent/task2001-founder-human-review`;
- fixed fixture, executor, resource ceiling and evidence quarantine are unchanged;
- human wording revision is audited and cannot replace the stable hypothesis identity or cross prohibited real-region boundaries;
- a revised session must be structured and explicitly approved again before execution;
- full automated suite: 316 tests passed;
- JavaScript syntax, Python compile and `git diff --check`: passed;
- status: IMPLEMENTED / FOUNDER RETEST REQUIRED.

## 6. Founder decision

Choose exactly one after direct operation:

- `TASK2001_HUMAN_REVIEW_ACCEPTED`
- `TASK2001_HUMAN_REVIEW_REVISE`
- `TASK2001_HUMAN_REVIEW_REJECTED`

Decision:

Reason:

Known limitations accepted for the submission:

Blocking fixes still required:

## 7. Completion and stop rule

Task2001 closes only when:

- Simon has personally operated the Runtime;
- the record above contains real session and artifact identifiers;
- success, friction and failure points are recorded;
- every Build Week blocker is either fixed and re-tested or explicitly blocks
  submission;
- the Founder decision is recorded.

Until then:

`TASK2001_STARTED / FOUNDER_RETEST_PENDING / BUILD_WEEK_SUBMISSION_NOT_READY`

Task2002+ remains not started.
