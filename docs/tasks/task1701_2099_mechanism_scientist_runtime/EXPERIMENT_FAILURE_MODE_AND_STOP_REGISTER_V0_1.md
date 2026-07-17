# ClimateOS Experiment Failure-Mode and Stop Register v0.1

Date: 2026-07-18

Status: STATIC_REGISTER / NO_EXECUTION / NO_FAILURE_EVENT CLAIMED

## 1. Failure classes

| ID | Class | Example trigger | Mandatory response |
|---|---|---|---|
| `FM-001` | hypothesis gate failure | hypothesis incomplete, superseded or not reviewed | stop before design promotion |
| `FM-002` | expert/consent failure | accountable role unassigned or person not consented | stop; do not infer approval |
| `FM-003` | version identity failure | model, dependency or configuration not immutable | stop; append unresolved identity |
| `FM-004` | licence failure | code, data, input or output rights unclear | quarantine identity; no use |
| `FM-005` | data admission failure | input, boundary or observation not admitted | stop before access or execution |
| `FM-006` | scale/time mismatch | supports or windows cannot be compared defensibly | return to hypothesis/design review |
| `FM-007` | diagnostic registration failure | primary diagnostic or threshold added after inspection | invalidate promotion; append revision |
| `FM-008` | control/confounding failure | control cannot distinguish a named alternative | mark `NOT_TESTABLE` or redesign |
| `FM-009` | resource authority failure | compute, storage, carbon or cost permission absent | stop; no reservation or commitment |
| `FM-010` | build/configuration failure | future environment cannot reproduce locked identity | record failure; no result promotion |
| `FM-011` | numerical instability/non-convergence | future run violates stability or convergence criteria | abort under pre-registered rule |
| `FM-012` | output integrity failure | incomplete, corrupt or checksum-mismatched output | quarantine output; no interpretation |
| `FM-013` | reproducibility failure | independent repeat cannot reproduce governed result | retain contradiction; review |
| `FM-014` | inconclusive outcome | diagnostics do not discriminate hypothesis/alternative | report `INCONCLUSIVE` |
| `FM-015` | prohibited-use request | result requested for unsupported decision or conclusion | refuse use and notify Founder internally |

FM-010 through FM-014 are future failure categories only. No build, run, output,
repeat or result exists in Task1721–1730.

## 2. Stop severity

| Severity | Meaning | Allowed action |
|---|---|---|
| `STOP_PRE_DESIGN` | minimum proposal requirement absent | retain record; no promotion |
| `STOP_PRE_ACCESS` | licence/data/source authority absent | no access or download |
| `STOP_PRE_RUN` | execution/resource/expert authority absent | no install, compute or run |
| `ABORT_FUTURE_RUN` | pre-registered future run condition breached | terminate and preserve failure log |
| `QUARANTINE_OUTPUT` | integrity, licence or reproducibility unresolved | no analysis or claim support |
| `REJECT_DOWNSTREAM_USE` | requested use crosses scientific/governance boundary | no decision or conclusion |

## 3. Immutable failure log

Every future failure log must retain:

1. event ID, record time and triggering design revision;
2. detecting role and detection method;
3. affected component, input, diagnostic or output identities;
4. failure class and stop severity;
5. whether access, build or execution had begun;
6. preservation/quarantine action;
7. evidence supporting the classification;
8. uncertainty and alternative explanations;
9. recovery proposal, or `DO_NOT_PROCEED`;
10. review and consent state.

Failure records are append-only. A recovered condition does not delete the
original failure, and a rerun never overwrites failed output.

## 4. Recovery boundary

Recovery may return a record only to an earlier review gate. It cannot grant
licence, data, compute, cost, expert or run authority. Changed versions,
configuration, inputs, diagnostics or thresholds require a new immutable design
revision and a new decision.

## 5. Non-numerical desk checks

### Desk check A — empty form

An `EMPTY_TEMPLATE` with all runtime identities `NOT_ADMITTED` is correctly
classified `STOP_PRE_DESIGN`. No synthetic case, variable, value or run is
created.

### Desk check B — attempted promotion with absent authority

A hypothetical request to execute while model, data, compute and expert gates
are absent triggers `FM-002`, `FM-003`, `FM-005` and `FM-009`, with severity
`STOP_PRE_RUN`. The correct outcome is `DO_NOT_PROCEED`.

These are governance-form checks, not experiment designs or scientific tests.

## 6. Boundary status

| Boundary | Result |
|---|---|
| tiny-synthetic design or run | none |
| model/config/input created | none |
| source, data, GIS or weight accessed | none |
| compute/storage/carbon allocation | none |
| cost | AUD 0 |
| expert contact/appointment | none |
| external notification | none |
| scientific or regional conclusion | none |

## 7. Register decision

`FAILURE_TAXONOMY_READY / NO_FAILURE_EVENT ASSERTED / ALL_EXECUTION_GATES_CLOSED`
