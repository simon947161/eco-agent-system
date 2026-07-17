# ClimateOS Dependency and Artifact Admission Register v0.1

Date: 2026-07-18

Status: EMPTY_STATIC_REGISTER / NO_DEPENDENCY_RESOLUTION / NO_ARTIFACT_ADMITTED

## 1. Dependency classes

| Class | Future role | Independent review requirement |
|---|---|---|
| direct | explicitly imported or linked component | exact version, licence and integrity |
| transitive | required by a direct dependency | full reachable chain and obligations |
| build | compiler, generator or build-only component | build reproducibility and output obligations |
| runtime | required during execution | environment, security, licence and support |
| optional | feature-gated component | prove disabled/absent or review separately |
| plugin | dynamically loaded extension | discovery, version and authority boundary |
| toolchain | OS/interpreter/compiler/container/library stack | immutable environment identity |
| data/model asset | non-code dependency required for function | separate data/model rights and admission |
| hosted service | API, account or remote execution dependency | terms, privacy, cost and operational boundary |

## 2. Dependency-risk states

| State | Trigger | Required response |
|---|---|---|
| `DEPENDENCY_IDENTITY_MISSING` | exact component/version absent | stop admission |
| `TRANSITIVE_CHAIN_UNKNOWN` | reachable dependency set unresolved | stop admission |
| `VERSION_RANGE_UNLOCKED` | future resolution may change | require immutable lock/receipt |
| `LICENCE_SCOPE_UNKNOWN` | component obligations unresolved | block corresponding use |
| `INCOMPATIBILITY_UNRESOLVED` | obligations or technical requirements conflict | quarantine decision |
| `OPTIONALITY_UNPROVEN` | claimed optional component may still load | treat as required until proven |
| `REMOTE_SERVICE_REQUIRED` | function requires account/network/service | independent Founder gate |
| `SECURITY_REVIEW_REQUIRED` | code execution or supply-chain risk exists | no install/run |
| `MAINTENANCE_STATE_UNKNOWN` | support/version status unresolved | record risk; no readiness claim |
| `DEPENDENCY_WITHDRAWN` | component unavailable or withdrawn | preserve identity; block new admission |

## 3. Empty decision record

| Field | Current value |
|---|---|
| decision ID | `MECH-ADM-EMPTY-001` |
| artifact identity | none selected |
| artifact class | not assigned |
| artifact version | missing |
| controlling terms | `TERMS_NOT_INSPECTED` |
| rights dimensions | all `UNKNOWN` |
| direct dependencies | not enumerated |
| transitive dependencies | `TRANSITIVE_CHAIN_UNKNOWN` |
| integrity receipt | absent; no artifact admitted |
| requested use | none authorized |
| decision | `DO_NOT_ADMIT` |
| reviewer | roles unassigned; no consent/contact |

This empty record is a form-boundary test, not a decision about real software,
data, model, service or documentation.

## 4. Desk check A — public visibility promotion

Request: admit an unspecified artifact for execution because it is publicly
visible.

Decision: `BLOCKED_LICENCE / BLOCKED_DEPENDENCY / DO_NOT_ADMIT`.

Reasons:

1. visibility does not grant execution or retention rights;
2. artifact/version and controlling terms are unidentified;
3. direct and transitive dependencies are unknown;
4. integrity, security, resource and expert gates are absent;
5. execution remains separately prohibited.

## 5. Desk check B — repository-level terms propagation

Request: apply unspecified repository-level terms automatically to every future
submodule, weight, dataset and hosted service.

Decision: `REJECTED / THIRD_PARTY_TERMS_REQUIRED`.

Each artifact family and dependency retains separate identity, scope and
rights dimensions. No parent licence is presumed to grant permissions for
third-party or remotely hosted materials.

## 6. Withdrawal and changed terms

- never overwrite the earlier decision;
- append a new terms/artifact revision and link it to the prior record;
- stop new access/use when controlling terms become inaccessible or change;
- retain lawful identity/receipt history without retaining prohibited content;
- quarantine dependent artifacts until scope and obligations are re-reviewed;
- a later permission never retroactively authorizes an earlier use.

## 7. Human review boundaries

- repository steward: records identity and lineage only;
- licence/governance reviewer: evaluates bounded rights dimensions, not science;
- security reviewer: evaluates execution/supply-chain risks, not licence rights;
- scientific reviewer: evaluates fitness only after consent, not legal permission;
- Founder: grants scope and resource authority but does not replace specialist review;
- no role or person is assigned or contacted in this batch.

## 8. Boundary verification

| Boundary | Result |
|---|---|
| external terms/source/repository inspected | no |
| artifact/dependency selected or admitted | no |
| clone/download/install/config/run | none |
| synthetic design/run | none |
| real data/GIS/model/weight | none |
| account/cloud/compute/storage | none |
| payment/cost commitment | none / AUD 0 |
| expert/legal contact | none |
| legal/scientific/regional conclusion | none |

## 9. Register decision

`EMPTY_ADMISSION_REGISTER_VALID / PUBLIC_VISIBILITY_PROMOTION_REJECTED / LICENCE_PROPAGATION_REJECTED / ALL_ARTIFACTS_UNADMITTED`
