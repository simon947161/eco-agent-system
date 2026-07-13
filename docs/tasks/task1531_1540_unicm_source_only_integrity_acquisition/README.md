# Task1531–1540 — UniCM Source-Only Integrity Acquisition

Date: 2026-07-14

Status: FOUNDER_AUTHORIZED / SOURCE_INTEGRITY_ONLY

Authoritative baseline: b9c871393add8497f75bb1c899479c5dd5e7df3f

Working branch: agent/task1531-1540-unicm-source-integrity

## Scope

This batch performed the bounded acquisition and integrity verification authorized by the Founder:

- acquired only the official Zenodo v1.0 source ZIP;
- enforced a 2 MiB transfer ceiling;
- verified the published MD5 and calculated SHA-256;
- inspected archive names, modes and sizes before extraction;
- extracted only into a temporary quarantine;
- compared the complete extracted Git tree with GitHub commit
  67fe4c183df351d5039c5b3b80ae86a68b627398;
- prepared provenance, SBOM-input and reproducibility-risk records.

## Task map

| Task | Deliverable |
|---|---|
| Task1531–1532 | bounded source acquisition and provenance record |
| Task1533–1534 | checksum verification record |
| Task1535–1536 | archive safety and file inventory |
| Task1537–1538 | pinned GitHub tree comparison |
| Task1539 | SBOM-input and integrity risk register |
| Task1540 | closure and separate Task1541 Founder Gate |

## Executive result

The Zenodo file was 1,103,721 bytes, below the 2,097,152-byte hard ceiling.

Published MD5:

ab8a324953bb91a5f00e0e38a8a08348

Observed MD5:

ab8a324953bb91a5f00e0e38a8a08348

Observed SHA-256:

3c4b9b9abf4a75e780c085b65c5aea8495e8fbb4c334725a91eb65996d08cf08

The archive contained 17 files and four directory entries, totalling 1,256,256 uncompressed bytes. No absolute path, parent traversal or symbolic link was present.

The extracted tree hash was:

501b96a31096b8d5f66bff93c32c6135c5d44537

The fixed GitHub commit tree hash was the same. A staged-tree comparison returned no differences, including file modes.

## Preserved boundary

No upstream shell or Python file was run. No dependency was installed. No environment was created. No model was initialized. No weight, checkpoint or climate dataset was acquired. No live data or model API was connected. No paid resource or commitment was created.

The temporary archive and extraction were not added to ClimateOS or the task branch.
