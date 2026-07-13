# Task1540 — Closure and Task1541 Founder Gate Brief

Date: 2026-07-14

Status: TASK1531–1540 COMPLETE / FOUNDER REVIEW PENDING

Execution status: NOT EXECUTABLE

## Closure

PR #58 was merged first. The authoritative branch advanced to:

b9c871393add8497f75bb1c899479c5dd5e7df3f

Task1531–1540 then completed the explicitly authorized source-only integrity scope.

Verified:

- the single Zenodo v1.0 source ZIP was acquired under a 2 MiB hard ceiling;
- the observed 1,103,721-byte length matched record metadata;
- the published MD5 matched exactly;
- SHA-256 was calculated and recorded;
- 21 archive entries represented 17 files and four directories;
- uncompressed file content totalled 1,256,256 bytes;
- no absolute path, parent traversal or symbolic link was present;
- extraction occurred only in temporary quarantine;
- all 17 files and modes matched the fixed GitHub commit;
- extracted and fixed commit tree hashes were both
  501b96a31096b8d5f66bff93c32c6135c5d44537;
- the source ZIP and extraction were not added to ClimateOS.

## Readiness decisions

| Capability | Decision |
|---|---|
| Release source acquisition | COMPLETE |
| Archive identity and checksum | PASS |
| Archive extraction safety | PASS FOR INSPECTED ARCHIVE |
| Fixed-commit tree equality | EXACT MATCH |
| Source provenance record | READY |
| SBOM input record | READY BUT INCOMPLETE |
| Dependency installation | NOT AUTHORIZED |
| Environment creation | NOT AUTHORIZED |
| Upstream code execution | NOT AUTHORIZED |
| Model or checkpoint run | BLOCKED / NOT AUTHORIZED |
| Climate-data acquisition | BLOCKED / NOT AUTHORIZED |
| Operational or Australian regional use | BLOCKED |
| Paid resource | NOT AUTHORIZED |

## CRP decision record

Founder authorization received:

“合并 PR #58；授权执行 ClimateOS Task1531–1540 Source-Only Integrity Acquisition，按上述边界执行。”

Interpreted boundary:

- merge only PR #58 before the batch;
- acquire only the official source ZIP;
- enforce the 2 MiB ceiling;
- perform checksum, archive and fixed-tree integrity checks;
- do not install or run upstream content;
- do not acquire weights or climate data;
- do not create API integrations or paid commitments.

Execution conformed to this boundary.

## Task1541 gate question

Should ClimateOS begin a separately bounded, non-executing dependency and environment lock review?

No answer is inferred from this closure.

## Possible bounded next scope

If separately authorized, a Task1541–1550 planning batch could be limited to:

- statically parse environment.yml;
- resolve package names against authoritative package metadata without installing;
- identify version, licence and supply-chain gaps;
- draft a lockfile strategy without creating an environment;
- define static-code-review and sandbox controls;
- define a minimal no-data smoke-test protocol without running it;
- prepare a later Founder Gate.

This is a recommendation only. The authoritative roadmap must be re-read before any next batch, and the Founder must separately approve the exact scope.

## Hard stop

Task1541 and all later tasks remain unauthorized.

No dependency may be installed. No environment may be created. No upstream code may be executed. No model, weight, checkpoint or climate dataset may be acquired or loaded. No live/API source may be integrated. No paid commitment may be made.
