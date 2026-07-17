# ClimateOS Sandbox Admission and Incident Escalation Protocol v0.1

Date: 2026-07-18

Status: STATIC_PROTOCOL / NO_SANDBOX CREATED / NO_INCIDENT ASSERTED

## 1. Sandbox candidate prerequisites

A future artifact cannot reach `SANDBOX_CANDIDATE_ONLY` unless all of the
following are independently reviewed:

1. exact source, artifact, dependency and version identities;
2. lawful access, retention and execution rights;
3. integrity receipts and transitive dependency graph;
4. declared install, build, runtime, plugin and network behaviour;
5. sandbox engine/runtime identity and configuration receipt;
6. non-privileged user and privilege-escalation prohibition;
7. read-only repository/input mounts and bounded temporary write path;
8. default-deny network with separately approved endpoints, if any;
9. no host credentials, tokens, SSH agents, cloud keys or personal secrets;
10. CPU, memory, time, disk, process and output ceilings;
11. system-call/process/filesystem/network audit coverage;
12. kill switch, timeout and incident containment path;
13. output quarantine and human release review;
14. Founder scope plus consenting security and domain roles where required.

Documenting prerequisites does not create a sandbox or authorize execution.

## 2. Static admission matrix

| Dimension | Required future evidence | Current state |
|---|---|---|
| artifact identity/integrity | exact version and lawful receipt | absent |
| licence/execution rights | bounded review for exact use | absent |
| dependencies | complete locked graph | absent |
| sandbox runtime | pinned engine/environment/config | not created |
| privilege | non-root/least privilege evidence | not configured |
| filesystem | explicit read/write mounts and quotas | not configured |
| network | deny-by-default and endpoint policy | not configured |
| secrets | proof of absence/injection boundary | not configured |
| resources | approved ceilings | zero / not authorized |
| logging | tamper-evident audit destination | not created |
| termination | kill/timeout/containment test | not performed |
| output | quarantine/release policy | static definition only |
| human roles | consent and escalation ownership | unassigned |

Current outcome: `DO_NOT_PROCEED`.

## 3. Incident classes and escalation

| Incident class | Future trigger | Immediate response |
|---|---|---|
| identity/integrity mismatch | target or checksum differs | stop; quarantine; preserve receipt |
| undeclared process/build action | unexpected executable or child process | abort; preserve logs |
| network-policy breach | unexpected connection attempt | block/abort; record endpoint evidence |
| filesystem-policy breach | read/write outside allowed path | abort; contain affected files |
| secret-access attempt | process requests protected credential/path | abort; treat secret as potentially exposed |
| privilege-policy breach | elevated capability requested/obtained | abort; isolate environment |
| resource-ceiling breach | CPU/memory/time/disk/process limit exceeded | terminate under pre-registered rule |
| output-policy breach | restricted/unknown content in output | quarantine; no release or interpretation |
| provenance/log failure | audit evidence missing or altered | invalidate run; no result promotion |
| scientific-boundary breach | output promoted beyond authorized use | reject conclusion; Founder/domain review |

No such incident occurred in Task1751–1760 because no sandbox or execution
exists.

## 4. Escalation states

1. `RECORD_ONLY` — non-operational governance note;
2. `BLOCK_ADMISSION` — target cannot proceed to sandbox review;
3. `QUARANTINE_IDENTITY` — isolate artifact identity/receipt;
4. `STOP_PRE_RUN` — execution authority absent;
5. `ABORT_FUTURE_RUN` — pre-registered stop condition activated;
6. `CONTAIN_AND_PRESERVE` — isolate environment and retain evidence;
7. `FOUNDER_REVIEW_REQUIRED` — scope/resource/governance decision needed;
8. `SECURITY_EXPERT_REQUIRED` — specialist assessment needed with consent.

## 5. Incident record contract

Every future incident record must be append-only and include incident ID,
artifact/sandbox/run identities, detection time/method, affected boundaries,
observed evidence, containment action, possible exposure, uncertainty,
notification authority, recovery decision and reviewer consent state.

Recovery returns the artifact only to an earlier gate. It cannot restore trust,
grant licence or authorize a rerun automatically.

## 6. Desk checks

### Desk check A — public package execution request

An unspecified publicly visible package is requested for immediate execution.
Because identity, terms, dependencies, integrity and sandbox controls are
absent, the result is `BLOCK_ADMISSION / DO_NOT_PROCEED`.

### Desk check B — sandbox with unspecified network and secrets

A fictional sandbox request omits network-deny and secret-isolation evidence.
The result is `STOP_PRE_RUN`; no sandbox configuration is created and no test
is executed.

## 7. Boundary verification

| Boundary | Result |
|---|---|
| real code/security inspection or scan | none |
| clone/download/install/build/import | none |
| sandbox/container/VM/config created | none |
| process/network/filesystem test | none |
| secret/key/account created or accessed | none |
| synthetic/model/data execution | none |
| compute/storage/cloud/payment | none / AUD 0 |
| security expert contact | none |
| real vulnerability/incident finding | none |

## 8. Protocol decision

`SANDBOX_PREREQUISITES_DEFINED / CURRENT_ADMISSION_REJECTED / NO_SANDBOX / NO_INCIDENT / NO_EXECUTION`
