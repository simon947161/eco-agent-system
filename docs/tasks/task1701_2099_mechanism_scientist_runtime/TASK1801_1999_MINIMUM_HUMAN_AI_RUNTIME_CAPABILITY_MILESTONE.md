# ClimateOS Task1801–1999 — Minimum Human–AI Runtime Capability Milestone

Date: 2026-07-18

Status: IMPLEMENTED / BOUNDED_YELLOW_RUN_COMPLETE / TASK2000_FOUNDER_ACCEPTED

Base main HEAD: `19fc212feb4f823aaafc208273fbc7262042d030`

## 1. Outcome

ClimateOS now has one thin supervised Runtime spine:

```text
human question
-> deterministic AI-style hypothesis structuring
-> explicit human approve/reject/stop
-> linked object-graph validation
-> fixed local tiny-synthetic execution
-> append-only audit and Run Receipt
-> quarantined Mechanism Evidence Passport candidate
-> explicit human post-run review
```

The Runtime is a workflow demonstration. It is not an autonomous scientist, a
general-purpose execution agent, an environmental model or scientific evidence.

## 2. Capability-based task map

Task numbers remain traceability indexes; the capability milestones are the
authoritative work units.

| Original range | Implemented capability |
|---|---|
| Task1801–1849 | machine-readable hypothesis/design/manifest/configuration/run-request/receipt/output/passport identities and closed validators |
| Task1850–1899 | repository-authored fictional scalar fixture, diagnostic, refusal paths and quarantined rehearsal; real atmospheric pilot remains `NOT_READY` |
| Task1900–1949 | local supervised question, hypothesis, approval, run and review workflow plus human-facing Web interface |
| Task1950–1999 | SQLite persistence, append-only digest-linked audit, localhost binding, no external dependency, fixed executor, resource checks and denial tests |
| Task2000 | bounded run reached a quarantined passport; Founder selected `ACCEPT_RUNTIME_DEMO`; Task2000 closed without releasing environmental evidence |

## 3. Why the legacy FastAPI prototype was not merged wholesale

Read-only preflight found that the earlier FastAPI/SQLite prototype remains on
`task46-repository-control-codex-batch-queue`, not in current `main`. Its SQLite
transaction, review-state, audit and localhost patterns were useful references.

The current environment does not contain FastAPI, httpx or uvicorn, and the ACTP
prohibits dependency installation. The minimum Runtime therefore uses only the
Python standard library (`sqlite3`, `http.server`, `hashlib`, `tracemalloc`) and
does not merge the diverged historical branch.

## 4. Implemented files

- `cczps_lite/scientist_runtime/contracts.py` — closed vocabulary, identities,
  resource ceilings and validation;
- `store.py` — SQLite sessions and append-only digest-linked audit events;
- `runtime.py` — supervised state machine, fixed executor, receipt, passport and
  export;
- `server.py` and `static/` — localhost-only six-stage human interface;
- `fixtures/tiny_synthetic_scalar_case.json` — fictional fixed input only;
- `run_scientist_runtime.py` — local launcher;
- `tests/test_scientist_runtime*.py` — success, refusal, tamper, boundary and Web
  tests.

## 5. Enforced boundary

The fixed executor:

- accepts only `TINY-SYNTH-SCALAR-001` from the repository;
- performs one scalar subtraction;
- does not accept user code or a subprocess;
- imports no network, API, model or LLM client;
- records zero network, zero secrets, zero subprocess and `AUD 0`;
- checks one worker, five-second wall ceiling, 64 MiB incremental-memory target
  and 100,000-byte output ceiling;
- rejects real-region and external-model terms including Bondo, Riverina,
  Tumut, Cooma, GraphCast and WRF;
- keeps all passport output non-environmental and quarantined after review.

## 6. Honest AI boundary

The v0.1 local assistant is a deterministic structuring template, not an LLM.
ChatGPT/Codex supplied the development-time reasoning surface permitted by the
ACTP. The local Runtime exposes the structured proposal and requires a human
decision; it makes no claim of autonomous scientific reasoning.

## 7. Deferred red work

No real meteorological/wind/GIS/project data, external model, clone, download,
package installation, API, network egress, account, credential, cloud, cost,
expert contact, scientific claim or regional conclusion was used.

GraphCast remains `LATER`. The real atmospheric pilot remains `NOT_READY`.
Constellation Journey and WorkOS private material remain absent from the diff.

## 8. Decision

`MINIMUM_RUNTIME_SPINE_IMPLEMENTED / BOUNDED_SYNTHETIC_RUN_REVIEWED / REAL_PILOT_NOT_READY / TASK2000_CLOSED / STOP_BEFORE_TASK2001`
