# Task1521–1530 — UniCM Safe Acquisition and Reproducibility Manifest

Date: 2026-07-14

Status: FOUNDER_AUTHORIZED / METADATA_AND_STATIC_ANALYSIS_ONLY

Authoritative baseline: `2c3aac8f102b3b6b6db8608ec8fd338a991a27b6`

Working branch: `agent/task1521-1530-unicm-safe-acquisition-manifest`

## Scope

This batch verifies:

- GitHub v1.0 and Zenodo asset metadata;
- model-weight metadata and availability;
- code-expected dataset file names and preprocessing assumptions;
- static parameter, memory and storage planning bounds;
- isolated-workspace security requirements;
- a zero-cost acquisition plan.

## Prohibited actions preserved

No upstream repository or archive was cloned or downloaded. No dependency was installed. No Conda/CUDA environment was created. No model or checkpoint was loaded. No dataset, model weight or large file was downloaded. No live API or operational source was connected. No paid commitment was created.

## Task map

| Task | Deliverable |
|---|---|
| Task1521–1523 | v1.0, Zenodo and weight asset manifest |
| Task1524–1526 | data-file and preprocessing manifest |
| Task1527 | static compute and storage budget |
| Task1528 | isolated-workspace security plan |
| Task1529 | zero-cost acquisition plan |
| Task1530 | closure and Task1531 Founder Gate |

## Executive result

The GitHub `v1.0` tag, GitHub `main` and commit
`67fe4c183df351d5039c5b3b80ae86a68b627398` are identical.

Zenodo record `19173780` contains one 1,103,721-byte source-code ZIP with an MD5 checksum. The verified release/archive inventory does not supply pretrained model weights.

UniCM therefore remains source-available but not checkpoint-ready. Model execution and large-data acquisition remain blocked.
