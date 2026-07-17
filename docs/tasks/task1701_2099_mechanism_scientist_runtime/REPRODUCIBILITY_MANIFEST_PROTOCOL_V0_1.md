# ClimateOS Reproducibility Manifest Protocol v0.1

Date: 2026-07-18

Status: STATIC_PROTOCOL / EMPTY_MANIFEST_ONLY / NO_ARTIFACT_INSPECTION / NO_RUN

## 1. Manifest identity

Every future manifest requires:

| Field | Rule |
|---|---|
| `manifest_id` | stable `MECH-RM-NNN`; never reused |
| `manifest_revision` | immutable revision identifier |
| `parent_revision` | required after the first revision |
| `hypothesis_revision_id` | exact governed hypothesis revision |
| `design_revision_id` | exact governed experiment-design revision |
| `created_at` | manifest record time, not build/run time |
| `steward_role` | role only until a person separately consents |
| `state` | one controlled manifest state |

Allowed states are `EMPTY_STATIC`, `IDENTITY_INCOMPLETE`, `LICENCE_BLOCKED`,
`ARTIFACTS_NOT_ADMITTED`, `READY_FOR_INDEPENDENT_MANIFEST_REVIEW`,
`QUARANTINED`, and `SUPERSEDED`. None authorizes access, installation or run.

## 2. Identity classes

| Class | Future minimum identity | Current state |
|---|---|---|
| source repository | canonical locator, owner, repository, commit/tag, tree receipt | not inspected / not admitted |
| dependency | name, source, exact version, licence, integrity receipt | not inspected / not admitted |
| build toolchain | OS, architecture, compiler/interpreter and build tool identities | not created / not admitted |
| runtime environment | OS/container/runtime/library identities and environment receipt | not created / not admitted |
| configuration | immutable config ID, format, checksum and semantic role | not created |
| input | object ID, source/version, licence, checksum and admission receipt | not accessed / not admitted |
| boundary asset | object ID, support, time/version, licence and checksum | not accessed / not admitted |
| diagnostic | implementation ID, version, unit/semantics and checksum | not created / not admitted |
| output | run ID, design/manifest link, format, checksum and retention state | no run / no output |

Public visibility is not licence approval. A locator is not proof that content
was inspected, and a filename or version label is not an integrity receipt.

## 3. Future checksum receipt

A future receipt must contain:

1. stable receipt ID;
2. artifact class and artifact ID;
3. exact lawful local object identity;
4. algorithm identifier, normally `SHA-256`;
5. lowercase hexadecimal digest only after an artifact is separately admitted;
6. byte size and canonicalization rule;
7. calculation tool/version and calculation time;
8. responsible role;
9. licence and retention state;
10. parent/superseded receipt relation.

Task1731–1740 computes no digest. Current digest state is
`ABSENT_ARTIFACT_NOT_ADMITTED`, not an empty string, zero hash or fabricated
example.

## 4. Relationship contract

The governed chain is:

`hypothesis revision → design revision → manifest revision → future run identity → future output identity`

Rules:

- every link uses an exact immutable ID;
- a newer manifest never silently changes an older design or run;
- one design may have multiple reviewed manifests, but each future run binds one manifest revision;
- a changed dependency, toolchain, configuration, input, boundary or diagnostic creates a new manifest revision;
- an output cannot be admitted without its exact run, manifest and design lineage;
- missing links return `IDENTITY_INCOMPLETE`, never “approximately reproducible.”

## 5. Completeness dimensions

Manifest review remains multidimensional:

| Dimension | Pass requirement |
|---|---|
| identity | every required component has an exact immutable identity |
| integrity | admitted artifacts have valid receipts |
| licence | access, retention, use and output rights are explicit |
| environment | build/runtime identity is complete and reviewable |
| semantics | configuration and diagnostic meanings are preserved |
| lineage | hypothesis, design, manifest, run and output links are exact |
| authority | data, compute, cost and human roles are separately authorized |
| reproducibility | independently attempted under a later gate; not inferred from completeness |

No numeric score may hide a failed dimension.

## 6. Version and quarantine rules

1. Append a new revision; never rewrite the old identity.
2. `SUPERSEDES` requires an explicit controlling relation.
3. `DIFFERS_FROM` preserves both versions without declaring either correct.
4. `WITHDRAWN` retains prior identity and withdrawal evidence.
5. `INACCESSIBLE` retains identity without claiming content inspection.
6. `QUARANTINED` blocks build, run, interpretation and redistribution.
7. A repaired artifact or manifest does not delete its earlier failure record.
8. Licence changes never retroactively grant earlier rights.

## 7. Current decision

`EMPTY_MANIFEST_PROTOCOL_READY / ALL_ARTIFACT_IDENTITIES_UNADMITTED / CONFIGURATION_NOT_CREATED / CHECKSUM_NOT_COMPUTED / REPRODUCIBILITY_NOT_TESTED`
