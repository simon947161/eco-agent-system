# ClimateOS Task2001 — Build Week Founder Human Composite Review Gate

Date: 2026-07-18

Status: AUTHORIZED / STARTED / HUMAN REVIEW PENDING

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
- review started at:
- review completed at:
- operating system:
- browser:
- Python version:
- baseline commit:
- reviewed commit:
- Runtime session ID:
- hypothesis ID:
- Run Receipt ID:
- Evidence Passport ID:
- audit chain valid: YES / NO / NOT CHECKED
- time to first successful session:
- external cost observed:
- network dependency observed:

### Step record

| Step | Directly completed? | Friction or failure | Severity | Suggested change |
|---|---|---|---|---|
| Open Runtime |  |  |  |  |
| Enter/select question |  |  |  |  |
| Understand structured plan |  |  |  |  |
| Approve plan |  |  |  |  |
| Reject plan |  |  |  |  |
| Modify plan |  |  |  |  |
| Run controlled experiment |  |  |  |  |
| Understand result |  |  |  |  |
| Inspect Evidence Passport |  |  |  |  |
| Inspect Run Receipt |  |  |  |  |
| Accept/question result |  |  |  |  |
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
| T2001- |  |  |  |  |  |

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

`TASK2001_STARTED / HUMAN_REVIEW_PENDING / BUILD_WEEK_SUBMISSION_NOT_READY`

Task2002+ remains not started.
