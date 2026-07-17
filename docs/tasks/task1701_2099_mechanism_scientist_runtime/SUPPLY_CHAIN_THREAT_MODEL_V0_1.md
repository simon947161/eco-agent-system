# ClimateOS Static Supply-Chain Threat Model v0.1

Date: 2026-07-18

Status: GENERIC_MODEL / NO_REAL_TARGET / NO_INSPECTION / NO_SECURITY_FINDING

## 1. Protected asset classes

| Asset class | Future protection objective | Current state |
|---|---|---|
| source identity | authentic owner/repository/version lineage | no source selected |
| package/archive | exact artifact and integrity receipt | no artifact selected |
| dependency graph | complete direct/transitive identity | not resolved |
| build toolchain | immutable compiler/interpreter/generator identity | not created |
| runtime | bounded process, privilege and environment | not created |
| plugin/extension | explicit discovery and load authority | none admitted |
| service/API | endpoint, terms, account and data-flow boundary | none accessed |
| data/model asset | identity, integrity, licence and admission | none accessed |
| secrets/credentials | non-exposure and least privilege | none created |
| output/log | integrity, containment and lawful retention | none generated |
| provenance | append-only decisions, receipts and incidents | documentation only |

## 2. Trust boundaries

The future conceptual sequence is:

`UNTRUSTED_IDENTITY → QUARANTINE → IDENTITY/LICENCE/SECURITY REVIEW → SANDBOX_CANDIDATE → SEPARATE EXECUTION GATE → OUTPUT_QUARANTINE → HUMAN REVIEW`

Task1751–1760 activates none of these operational stages. Every external
artifact remains before `UNTRUSTED_IDENTITY` because no real item was selected.

## 3. Generic threat classes

| ID | Threat class | Potential future failure | Required gate response |
|---|---|---|---|
| `SC-T01` | identity spoofing | wrong owner/repository/version represented as authoritative | block identity admission |
| `SC-T02` | source compromise | upstream account or repository content compromised | quarantine; independent evidence required |
| `SC-T03` | name collision/dependency confusion | unintended component resolved | require exact source/version/receipt |
| `SC-T04` | substitution/typosquatting | similar name or locator replaces intended artifact | reject unmatched identity |
| `SC-T05` | archive/package tampering | bytes differ from reviewed artifact | checksum failure; quarantine |
| `SC-T06` | malicious install/build action | setup or build performs undeclared action | no install; sandbox/security review |
| `SC-T07` | transitive drift | unlocked dependency changes | immutable lock and graph review |
| `SC-T08` | dynamic plugin loading | unreviewed code loads at runtime | disable/deny until separately admitted |
| `SC-T09` | secret or credential exposure | process reads or transmits credentials | no secrets; stop and contain |
| `SC-T10` | unexpected network egress | code contacts an undeclared endpoint | default-deny network; abort future run |
| `SC-T11` | filesystem escape/write | code reads/writes outside allowed paths | read-only boundary; stop and contain |
| `SC-T12` | privilege escalation | process gains broader authority | non-privileged execution required; abort |
| `SC-T13` | data/model poisoning | input or weight integrity/meaning compromised | quarantine; no scientific use |
| `SC-T14` | output/log exfiltration | sensitive or restricted content leaves boundary | block egress and output release |
| `SC-T15` | hosted-service drift | remote behaviour/terms/version change | re-review identity and data flow |
| `SC-T16` | provenance loss/rollback | decisions, receipts or failures deleted/replaced | append-only history; block promotion |

These are generic possibilities, not findings about a real project or artifact.

## 4. Threat dimensions

Every future assessment must keep separate:

- likelihood evidence, which may remain unknown;
- impact domain: integrity, confidentiality, availability, licence, cost,
  reproducibility, scientific validity or governance;
- exposure stage: discovery, access, install, build, runtime or output;
- affected identity and version;
- preventive, detective, containment and recovery controls;
- residual uncertainty and human-review requirement.

No unsupported numeric risk score may replace missing evidence.

## 5. Security decision states

| State | Meaning |
|---|---|
| `NOT_ASSESSED` | no authorized inspection occurred |
| `IDENTITY_BLOCKED` | exact target identity unresolved |
| `THREAT_REVIEW_INCOMPLETE` | generic controls not mapped to a real item |
| `QUARANTINE_REQUIRED` | artifact cannot enter build/runtime scope |
| `SANDBOX_CANDIDATE_ONLY` | prerequisites documented; no sandbox/run authority |
| `SECURITY_EXPERT_REQUIRED` | decision exceeds current role |
| `DO_NOT_PROCEED` | requested action crosses an unresolved or prohibited boundary |

## 6. Current decision

`GENERIC_THREAT_MODEL_READY / REAL_TARGET_NOT_SELECTED / SECURITY_NOT_ASSESSED / NO_SANDBOX_OR_EXECUTION AUTHORIZED`
