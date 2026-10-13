# Mission Runtime Static Validation Report v0.1

Date: 2026-07-27
Status: PASS_WITH_FOUNDER_GATE
Parent: Issue #103
PR: #104
Branch: `agent/mission-runtime-phase-a-schema`

## 1. Scope

This validation covers only static JSON Schema and machine-readable fixtures for:

- Mission State Machine
- Mission Plan Contract
- Mission Checkpoint Bundle
- Mission Context Packet

It does not validate an executable scheduler, dispatcher, tool engine, network integration, merge action or mainline runtime change.

## 2. Method

Validation used JSON Schema Draft 2020-12 with format checking enabled.

Steps:

1. Parse each schema as JSON.
2. Meta-validate each schema.
3. Validate four positive fixtures.
4. Apply four intentional negative mutations.
5. Confirm every negative mutation is rejected for the intended reason.

## 3. Positive results

| Fixture | Expected | Actual | Result |
|---|---:|---:|---|
| Mission state at `FOUNDER_GATE` | PASS | PASS | PASS |
| Shared Mission Plan with bounded capability envelope | PASS | PASS | PASS |
| Checkpoint with permission revalidation and no always-approve restore | PASS | PASS | PASS |
| Context Packet with repository, branch and commit baseline | PASS | PASS | PASS |

## 4. Negative mutation results

| Mutation | Expected | Actual | Result |
|---|---:|---:|---|
| Unknown state `EXECUTING` | FAIL | FAIL | PASS |
| Child capability widening set to `true` | FAIL | FAIL | PASS |
| Resume restores always-approve authority | FAIL | FAIL | PASS |
| Context Packet missing authoritative commit | FAIL | FAIL | PASS |

Observed rejection messages included:

- state value not in the approved lifecycle enum;
- `False was expected` for capability widening;
- `False was expected` for always-approve restoration;
- `commit is a required property` for incomplete authority baseline.

## 5. Verification conclusion

The static schemas successfully enforce four critical properties:

1. Lifecycle vocabulary is bounded.
2. Child missions cannot declare permission widening.
3. Interrupted missions cannot restore unconditional approval.
4. A resumable context packet must identify an authoritative repository baseline.

## 6. Known limitations

Schema validation alone does not yet prove:

- that a proposed state transition is semantically allowed;
- that a child tool list is a true subset of the parent tool list;
- that a protected write request is correctly classified;
- that evidence references exist and are current;
- that checkpoint integrity hashes are valid;
- that repository state has not changed since checkpoint creation.

Those require a bounded executable Validator prototype and additional semantic tests.

## 7. Gate status

`STATIC_VALIDATION_PASS`

`EXECUTABLE_VALIDATOR_NOT_AUTHORISED`

`MAINLINE_RUNTIME_NO_CHANGE`

`FOUNDER_DECISION_REQUIRED`

## 8. Recommended next action

Founder reviews and decides the five governance questions in the final evidence package. Only an explicit approval may authorise the bounded executable Validator prototype.