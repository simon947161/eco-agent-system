# Task1539 — SBOM Input and Integrity Risk Register

Date: 2026-07-14

Status: COMPLETE / NON-EXECUTABLE INPUT ONLY

## Source component record

| Field | Value |
|---|---|
| Component | UniCM Global Climate Modes |
| Component type | source archive |
| Upstream version | v1.0 |
| Upstream repository | tsinghua-fib-lab/UniCM-Global-Climate-Modes |
| Commit | 67fe4c183df351d5039c5b3b80ae86a68b627398 |
| Commit tree | 501b96a31096b8d5f66bff93c32c6135c5d44537 |
| Zenodo record | 19173780 |
| DOI | 10.5281/zenodo.19173780 |
| Archive bytes | 1,103,721 |
| MD5 | ab8a324953bb91a5f00e0e38a8a08348 |
| SHA-256 | 3c4b9b9abf4a75e780c085b65c5aea8495e8fbb4c334725a91eb65996d08cf08 |
| Declared licence | MIT |
| Files | 17 |
| Installed | no |
| Executed | no |
| Vendored into ClimateOS | no |

This is input for a future SBOM. It is not a complete SBOM because dependencies were not resolved, downloaded or installed.

## Integrity and reproducibility risks

| ID | Risk | Current evidence | Status |
|---|---|---|---|
| I-01 | Publisher supplies MD5 but not SHA-256 metadata | ClimateOS SHA-256 calculated locally | MITIGATED FOR THIS ACQUISITION |
| I-02 | Later archive replacement | length, MD5, SHA-256 and commit tree pinned | CONTROL DEFINED |
| I-03 | Archive extraction abuse | no traversal, absolute path or symlink | PASS FOR THIS ARCHIVE |
| I-04 | Source differs from GitHub release commit | exact Git tree equality | CLOSED |
| I-05 | Dependency drift | environment.yml not resolved or locked | OPEN |
| I-06 | Dependency supply-chain exposure | no dependency artifacts inspected | OPEN |
| I-07 | No official pretrained weights | prior search found none | BLOCKING |
| I-08 | Raw-to-derived data preparation incomplete | prior manifest remains incomplete | BLOCKING |
| I-09 | Upstream scripts can execute training/testing | scripts present but not run | CONTAINED |
| I-10 | MIT licence does not cover external data | no external data acquired | OPEN FOR FUTURE |
| I-11 | Scientific and regional fitness unproven | source integrity is not scientific validation | BLOCKING |
| I-12 | Temporary quarantine persistence | binary artifacts excluded from repository | CONTROLLED |

## Security disposition

The verified source may be referenced by immutable identity in future planning. It must not be promoted to an executable dependency until a separately authorized review covers:

- dependency lock and licence inventory;
- package-origin and checksum controls;
- static code security review;
- environment isolation;
- bounded runtime acceptance tests;
- checkpoint and data provenance;
- named human scientific responsibility.

## Cost disposition

This batch used only public, zero-direct-cost assets and local temporary storage. It created no cloud booking, subscription, paid API use or procurement commitment.
