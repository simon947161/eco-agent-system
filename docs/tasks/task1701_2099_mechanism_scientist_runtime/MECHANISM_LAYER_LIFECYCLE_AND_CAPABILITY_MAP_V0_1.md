# ClimateOS Mechanism Layer Lifecycle and Capability Map v0.1

Date: 2026-07-18

Status: PHASE_INTEGRATION / HONEST_CAPABILITY_CLASSIFICATION / NO_RUN

## 1. The system in one sentence

ClimateOS now has a detailed set of rules for turning a scientific question into
a reviewable, reproducible and safely governed experiment, but it does not yet
have a working mechanism experiment or Environmental AI Scientist Runtime.

## 2. Integrated lifecycle

```text
research question
  -> hypothesis and alternative explanations
  -> pre-registered experiment design and stop rules
  -> reproducibility manifest and configuration identity
  -> licence/dependency/artifact admission
  -> supply-chain and sandbox decision
  -> least-privilege, secret and network decision
  -> separately authorized execution
  -> audit events and run receipt
  -> output quarantine and inspection
  -> structural/security/licence/scientific review
  -> scoped sign-off, dissent preservation and release decision
```

The central achievement is that no arrow is allowed to silently imply the next.
A complete hypothesis is not permission to run; a successful process exit is
not scientific evidence; and a scientific review is not publication authority.

## 3. What each layer protects

| Layer | Repository result | Prevents |
|---|---|---|
| reference return gate | candidate identities and no-run validator | a paper/repository becoming a runtime dependency by implication |
| hypothesis protocol | immutable hypothesis, alternatives, falsification and uncertainty fields | correlation or a plausible story being labelled causation |
| experiment design | baseline/perturbation/control/sensitivity and stop/failure contracts | changing the question after seeing results |
| reproducibility | manifest/configuration identity and provenance requirements | “same experiment” claims without the same ingredients |
| admission | licence, use-right, dependency and artifact states | public visibility being mistaken for permission to use |
| supply chain | threat and sandbox prerequisites | running unknown code because it is convenient or popular |
| permissions | process/filesystem/secret/network/resource dimensions | broad or persistent authority leaking across purposes |
| audit/receipt | future event, resource, termination and integrity evidence | treating silence or an exit code as a trustworthy run record |
| quarantine | provenance, inspection and release states | viewing or distributing untrusted output automatically |
| human review | separate competence, conflict, dissent and sign-off tracks | one generic “approved” label hiding missing review |

## 4. Actual capability classes

### A. Implemented and executable repository machinery

Task1701–1710 added:

- `mechanism_return_gate.schema.json`;
- a no-run JSON registration;
- an offline validator and deterministic preview;
- targeted tests integrated with the repository test suite.

This machinery validates a bounded no-run readiness record. It does not build or
run WRF, WRF-Chem, TianJi-Environ or another scientific model.

The preceding Task1500–1700 line also delivered machine-readable evidence,
claim and ledger prototypes. Those are useful foundations, but they do not form
an operational regional environmental model or a causal finding.

### B. Implemented as static, reviewable specifications

Task1711–1790 added contracts and empty registers for:

- hypothesis structure;
- experiment design and failure modes;
- reproducibility/configuration identity;
- licence/dependency/artifact admission;
- supply-chain/sandbox admission;
- permission/secret/network egress;
- audit/run receipts/output quarantine;
- human review/sign-off/dissent/release governance.

These files are durable design work. They are not code paths, configured
services, populated scientific records or evidence of a successful experiment.

### C. Not implemented

- a filled real or tiny-synthetic hypothesis/experiment package;
- an admitted model, version, dependency graph or executable environment;
- input or boundary data and their quality/licence review;
- a sandbox, permission policy or network allowlist;
- an execution controller, logger, receipt generator or quarantine store;
- diagnostics and a Mechanism Evidence Passport produced from a run;
- a consenting scientific reviewer and completed review;
- a bounded atmospheric pilot;
- Environmental AI Scientist workflow agents or closed-loop runtime.

## 5. Why the recent process felt mechanical

From Task1711 onward, most ten-task blocks divided one governance idea into four
Markdown files, then required a separate merge and next-block authorization.
This preserved lineage and boundaries, but the approval frequency was not
proportional to the actual risk because every block remained documentation-only,
zero-cost and non-executing.

The process optimized auditability at the expense of Founder comprehension. It
also made task-number progress look more like capability progress than it was.
Reaching Task1800 does not mean the Task1800–1849 Evidence Passport milestone is
complete.

## 6. Simpler future cadence

Use three decision levels instead of automatic ten-task approvals:

| Level | Example | Founder interaction |
|---|---|---|
| green: same bounded documentation | consolidate or correct existing contracts | batch authorization; one milestone PR |
| amber: reversible local demonstration | create tiny synthetic fixture/config and run locally | one explicit experiment-package approval with ceilings |
| red: external or consequential action | real data/model access, account, cost, network, expert contact, publication | separate explicit decision per material action |

Task numbers remain indexes, not reasons to request approval. A new PR should
represent a meaningful capability or decision, not merely the next ten numbers.

## 7. Integrated phase decision

`GOVERNANCE_ARCHITECTURE_SUBSTANTIALLY_SPECIFIED / NO_MECHANISM_EXPERIMENT / NO_RUNTIME / NEXT_VALUE_REQUIRES_A_DEMONSTRATION_DECISION`

