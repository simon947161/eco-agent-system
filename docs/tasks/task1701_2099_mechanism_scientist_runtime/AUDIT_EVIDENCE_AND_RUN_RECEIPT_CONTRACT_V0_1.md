# ClimateOS Audit Evidence and Run Receipt Contract v0.1

Date: 2026-07-18

Status: STATIC_CONTRACT / EMPTY_REGISTER / NO_LOGGER / NO_RUN

## 1. Contract boundary

A run receipt is evidence about a separately authorized run; it is not authority
to run. A receipt cannot repair missing prior approval, expand permissions,
validate scientific content or prove that a process was safe merely because it
terminated.

Task1771–1780 defines fields and refusal states only. It does not instantiate an
event, receipt, logger, hash chain, signature, clock, process or storage target.

## 2. Immutable identity model

| Record | Future identity rule |
|---|---|
| audit event | stable `MECH-AUDIT-EVENT-NNN`; never reused |
| run request | stable `MECH-RUN-REQUEST-NNN`; refers to approved revision |
| run receipt | stable `MECH-RUN-RECEIPT-NNN`; one attempt only |
| output set | stable `MECH-OUTPUT-SET-NNN`; starts quarantined |
| receipt revision | append-only correction; original remains visible |

Every future receipt must bind exact identifiers for the experiment-design
revision, mechanism hypothesis, reproducibility manifest, configuration
identity, admitted dependency/artifact set, sandbox decision, permission
request, secret/egress decision and output set. A missing reference is a failed
receipt, not an optional field.

## 3. Audit-event fields

Each future event requires:

1. event ID and monotonically ordered event sequence;
2. receipt ID and exact run-attempt ID;
3. event type from a controlled vocabulary;
4. accountable actor role and emitting process identity;
5. declared timestamp source, precision and timezone;
6. observed state before and after the event;
7. permission dimension used or denied;
8. resource counter class and bounded value, when applicable;
9. termination, containment or escalation relationship;
10. integrity-evidence method and predecessor reference;
11. redaction statement and secret-non-presence status;
12. capture status, uncertainty and exception code.

Controlled event types may include `REQUEST_SEEN`, `AUTHORITY_CHECKED`,
`PROCESS_START_OBSERVED`, `PERMISSION_DENIED`, `RESOURCE_LIMIT_OBSERVED`,
`PROCESS_TERMINATION_OBSERVED`, `OUTPUT_DECLARED`, `QUARANTINE_ENTERED`, and
`EVIDENCE_EXCEPTION`. These are vocabulary only; no event exists in this batch.

## 4. Run-receipt fields

| Section | Required future evidence |
|---|---|
| authority | exact approved request/revision, approver role, validity interval |
| identity | actor role, parent/child process identities, executable identity |
| inputs | admitted artifact IDs and declared non-presence of undeclared inputs |
| environment | configuration ID, sandbox decision and permission revision |
| time | requested start, observed start/end and clock-source qualification |
| resources | ceilings and observed CPU, memory, wall-time, disk/process counts |
| network/secrets | declared denied/approved state and observed denied attempts |
| lifecycle | start, transitions, exit/termination reason and containment state |
| output | output-set ID, declared members and quarantine entry evidence |
| integrity | event count, sequence completeness and integrity-evidence status |
| exceptions | missing fields, collection failures, inconsistencies and uncertainty |
| decision | receipt state; never a scientific or release conclusion |

No real measurements or resource values are entered here.

## 5. Receipt states

| State | Meaning |
|---|---|
| `NO_RUN_NO_RECEIPT` | current state; no execution and no receipt instance |
| `RECEIPT_TEMPLATE_ONLY` | schema vocabulary exists without evidence |
| `RUN_AUTHORITY_MISSING` | run cannot be promoted or interpreted |
| `EVIDENCE_INCOMPLETE` | one or more mandatory fields/events are absent |
| `SEQUENCE_INCONSISTENT` | ordering or transition claims conflict |
| `INTEGRITY_UNVERIFIED` | integrity method or predecessor evidence is absent |
| `TAMPER_SUSPECTED` | evidence conflicts or appears altered |
| `TERMINATION_UNCONFIRMED` | end state is not evidenced |
| `RECEIPT_REJECTED` | receipt is unusable for promotion |
| `RECEIPT_STRUCTURALLY_ACCEPTED` | form complete; no scientific validation implied |

Only `NO_RUN_NO_RECEIPT / RECEIPT_TEMPLATE_ONLY` applies in this batch.

## 6. Integrity and correction rules

- event order must be append-only and gaps must be explicit;
- a future integrity digest or signature requires a separately admitted method;
- a digest placeholder is not a digest and must never be presented as one;
- clocks, signing keys and timestamp authorities require independent gates;
- corrections append a new revision with reason, author role and superseded ID;
- original evidence is not silently edited, backfilled or deleted;
- suspected tampering immediately blocks receipt acceptance and output release;
- collection failure is recorded as failure, never inferred as a successful event.

No digest, signature, key, timestamp or evidence chain is generated here.

## 7. Refusal paths

| Condition | Required future response |
|---|---|
| approval or identity absent | do not start; receipt state `RUN_AUTHORITY_MISSING` |
| start event absent | reject attempt evidence; quarantine any claimed output |
| event gap or duplicate sequence | `SEQUENCE_INCONSISTENT`; investigate separately |
| termination not observed | `TERMINATION_UNCONFIRMED`; contain and quarantine |
| integrity evidence absent | `INTEGRITY_UNVERIFIED`; no promotion |
| alteration suspected | `TAMPER_SUSPECTED`; preserve, isolate and escalate |
| output not bound to receipt | reject provenance; quarantine by default |
| secret may appear in evidence | restrict access; independent incident gate |

## 8. Desk check A — empty receipt

Fictional request: accept an otherwise blank receipt because no error was
reported.

Decision: `RECEIPT_REJECTED / EVIDENCE_INCOMPLETE / TERMINATION_UNCONFIRMED`.
Silence is not evidence. No run or receipt instance is created.

## 9. Desk check B — edited event sequence

Fictional request: promote an output after an unexplained sequence gap and a
manually overwritten termination field.

Decision: `RECEIPT_REJECTED / SEQUENCE_INCONSISTENT / TAMPER_SUSPECTED`.
The claimed output remains quarantined. No file or output is handled.

## 10. Current decision

`STATIC_AUDIT_AND_RECEIPT_CONTRACT_READY / NO_RUN / NO_RECEIPT / NO_LOGGER / NO_INTEGRITY_ARTIFACT`

