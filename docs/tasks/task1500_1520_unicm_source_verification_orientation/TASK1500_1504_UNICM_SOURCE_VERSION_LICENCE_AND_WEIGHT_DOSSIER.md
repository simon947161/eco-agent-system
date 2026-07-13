# Task1500–1504 — UniCM Source, Version, Licence and Weight Dossier

Date: 2026-07-14

Status: VERIFIED_WITH_OPEN_BLOCKERS / NOT_EXECUTABLE

## 1. Publication identity

- Title: *Learning the coupled dynamics of global climate modes*
- Authors: Yuan Yuan, Jingtao Ding, Zhongpu Qiu, Jingfang Fan, Yong Li et al.
- Journal: Nature Machine Intelligence, volume 8, pages 930–941 (2026)
- Published: 2026-06-01
- DOI: https://doi.org/10.1038/s42256-026-01245-5
- Article page: https://www.nature.com/articles/s42256-026-01245-5
- Article status: peer-reviewed version of record.
- Article access: subscription-controlled article text; ordinary scholarly citation and limited factual extraction only. The article licence is not the same as the software licence.

The publication's Code availability section directly identifies both the GitHub and Zenodo records below. This establishes authoritative paper-to-code provenance.

## 2. Official code identity

- Official GitHub repository: https://github.com/tsinghua-fib-lab/UniCM-Global-Climate-Modes
- Owner: `tsinghua-fib-lab`, the Future Intelligence Lab at Tsinghua University
- Repository visibility: public
- Default branch: `main`
- Verified main HEAD on 2026-07-14:
  `67fe4c183df351d5039c5b3b80ae86a68b627398`
- Latest visible release: `v1.0 - Learning the coupled dynamics of global climate modes`, dated 2026-03-23
- Zenodo DOI named by the paper:
  https://doi.org/10.5281/zenodo.19173780

The GitHub repository README describes itself as the official implementation and links the Future Intelligence Lab and Tsinghua University. This claim is independently anchored by the Nature paper.

## 3. Software licence

The repository contains an MIT License:

- copyright: 2025 FIB LAB, Tsinghua University;
- use, copying, modification, merging, publication, distribution, sublicensing and sale are allowed;
- copyright and permission notices must be preserved;
- the software is supplied without warranty.

Licence URL:
https://github.com/tsinghua-fib-lab/UniCM-Global-Climate-Modes/blob/main/LICENSE

### Licence boundary

The MIT licence covers the repository software. It does not automatically license:

- the Nature article or supplementary material;
- CMIP6, ERA5, ORAS5, GODAS or SODA data;
- separately hosted checkpoints or derived datasets;
- third-party Python/CUDA dependencies;
- ClimateOS redistribution of upstream data or outputs.

Each non-code asset requires its own source and terms record before acquisition.

## 4. Release and commit control

Future acquisition must pin both:

1. an immutable Git commit; and
2. the selected release or Zenodo record.

The currently verified reference commit is `67fe4c183df351d5039c5b3b80ae86a68b627398`. Task1521 must not silently track moving `main`.

Before acquisition, compare the GitHub release tag, Zenodo archive and current main tree. Record any divergence.

## 5. Weight and checkpoint status

The inspected repository includes:

- training, individual-test and ensemble-test scripts;
- model and training code;
- a `--pretrained_path` argument;
- expected output paths such as `experiments/runs/SaveModel_Seed<SEED>`;
- ensemble loading logic.

The inspected README and repository metadata did **not identify a direct public download location for a complete published pretrained ensemble**. The repository scripts expect local checkpoints or locally trained models.

Classification:

`REQUIRES_FURTHER_EVIDENCE`

Required before reproduction:

- confirm whether v1.0 or Zenodo contains weights not visible in the GitHub tree;
- record file names, sizes, checksums and licence;
- confirm whether published metrics require 20 seeds or a specific ensemble subset;
- confirm paper-to-checkpoint correspondence;
- reject unverified third-party mirrors.

## 6. Source admission decision

| Asset | Current decision |
|---|---|
| Nature paper identity | VERIFIED |
| Official GitHub identity | VERIFIED |
| GitHub main commit | VERIFIED |
| Software licence | MIT / VERIFIED |
| Zenodo identity | PAPER-VERIFIED / CONTENT NOT YET INSPECTED |
| Pretrained weights | REQUIRES_FURTHER_EVIDENCE |
| Dataset rights | SOURCE-SPECIFIC REVIEW REQUIRED |
| ClimateOS integration | NOT AUTHORIZED |
| Model execution | NOT AUTHORIZED |

## 7. Task1521 blocking questions

- Does Zenodo provide immutable code only, or code plus checkpoints?
- Are trained weights available under MIT or separate terms?
- Which exact commit/tag generated the paper results?
- Are preprocessing scripts sufficient to reconstruct every expected NetCDF input?
- Are any undocumented author-provided assets required?

Until answered, no claim of reproducibility or operational readiness is permitted.
