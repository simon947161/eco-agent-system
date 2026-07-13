# Task1518–1519 — UniCM Reproducibility Risk Register

Date: 2026-07-14

Status: ACTIVE GATE REGISTER / NO EXPERIMENT AUTHORIZED

| ID | Risk | Evidence/status | Severity | Required control | Gate |
|---|---|---|---|---|---|
| R01 | Paper-code version mismatch | Paper links repo/Zenodo, but exact paper-result commit/tag mapping is not yet recorded | High | compare v1.0, Zenodo and pinned Git commit | Before acquisition |
| R02 | Missing pretrained weights | No direct complete checkpoint download was identified in inspected README/tree | Critical | author/release/Zenodo verification, checksum and terms | Before inference |
| R03 | Incomplete preprocessing path | Code expects named preprocessed NetCDF files | Critical | raw-to-input manifest and deterministic scripts | Before data download |
| R04 | Unknown data volume | Five large climate/ocean data families are referenced | High | provider-side subset and storage calculation | Before download |
| R05 | Unknown VRAM/runtime | No validated benchmark or peak-memory record | High | static estimate, then separately authorized dry-run | Before paid compute |
| R06 | Environment ageing | PyTorch 2.0.1/CUDA 11.8 and partially unpinned pip stack | Medium | isolated lock, SBOM and compatibility review | Before install |
| R07 | Unsafe checkpoint loading | Unverified PyTorch artefacts may be unsafe | Critical | authoritative source, checksum, quarantine and safe loading review | Before weight access |
| R08 | Script/default inconsistency | CLI default epochs differ from supplied shell script | High | reconstruct exact paper configuration | Before reproduction |
| R09 | Metric mismatch | Published metrics may depend on ensemble size, preprocessing and evaluation period | High | metric crosswalk and acceptance tolerance | Before claiming reproduction |
| R10 | Dataset licence mismatch | MIT code licence does not cover third-party data | Critical | dataset-by-dataset terms dossier | Before acquisition |
| R11 | Australian driver omission | SAM and MJO were not identified in inspected UniCM mode set | Critical | separate Australian driver layer | Before regional use |
| R12 | Global-to-local overreach | Climate-mode skill does not prove NSW impact skill | Critical | independent regional translation and validation | Before pilot |
| R13 | Correlation/attention misread as causality | Paper reports interpretable attention and coupled relationships | Critical | evidence-class labels and expert review | Permanent |
| R14 | Non-stationary teleconnections | Climate change may alter historical relationships | High | rolling evaluation and stationarity warnings | Before planning use |
| R15 | Operational misuse | Research output could be mistaken for warning service | Critical | research-only labels and human gate | Permanent |
| R16 | Core dependency contamination | Direct installation could destabilize ClimateOS | High | isolated workspace and adapter-only boundary | Before environment setup |
| R17 | Cost escalation | data, GPU, storage or expert costs are unknown | High | bounded Paid Decision Brief and ceiling | Before commitment |
| R18 | Unverified scientific completeness | Subscription article access may limit method reconstruction | Medium | use supplementary/author materials lawfully; record gaps | Before reproduction |
| R19 | Reproducibility failure | Published output may not reproduce | High | define failure as valid documented result; stop conditions | During future experiment |
| R20 | Expert authority gap | AI/code review is not climate-science validation | Critical | named Australian domain reviewer for consequential interpretation | Before regional pilot |

## Risk decision

- Open critical risks: R02, R03, R07, R10, R11, R12, R13, R15, R20.
- Task1521 readiness: `NOT YET EXECUTABLE`.
- Task1551–1600 reproduction readiness: `BLOCKED`.
- Australian regional-use readiness: `BLOCKED`.

## Mandatory stop conditions

Stop and return to Founder review if:

- official assets or terms cannot be verified;
- weights require an unapproved source;
- the data/compute burden is disproportionate;
- environment installation would alter ClimateOS core;
- a reproduction claim cannot preserve exact lineage;
- the project begins implying causality or operational warnings;
- a newer, more open or more regionally suitable model becomes preferable.
