# Task1547 — Static Dependency, Licence and Supply-Chain Review

Date: 2026-07-14

Status: STATIC REVIEW COMPLETE / ENVIRONMENT NOT LOCKED / NO INSTALLATION

## Upstream environment identity

File: environment.yml

Git blob:

01d1005b42a7da5c0ad052b182f63f038502b266

Environment name:

UniCM-env

Channels, in declared order:

1. pytorch
2. nvidia
3. pyg
4. conda-forge
5. defaults

## Declared dependencies

| Package | Upstream constraint | Lock quality | Preliminary licence family | Decision |
|---|---|---|---|---|
| python | 3.11 | minor only | PSF | NOT LOCKED |
| numpy | 1.26.* | patch wildcard | BSD-3-Clause | NOT LOCKED |
| pytorch | 2.0.1 | exact version, no build/hash | BSD-style | PARTIAL |
| pytorch-cuda | 11.8 | exact feature version, no build/hash | NVIDIA terms apply | LEGAL/PLATFORM REVIEW |
| torchaudio | 2.0.2 | exact version, no build/hash | BSD-style | PARTIAL |
| torchvision | 0.15.2 | exact version, no build/hash | BSD-style | PARTIAL |
| pip | unpinned | none | MIT | NOT LOCKED |
| torch-geometric | 2.5.3 | exact version, no artifact/hash | MIT | PARTIAL |
| timm | unpinned | none | Apache-2.0 family | NOT LOCKED |
| xarray | unpinned | none | Apache-2.0 | NOT LOCKED |
| netcdf4 | unpinned | none | MIT family | NOT LOCKED |
| scikit-learn | unpinned | none | BSD-3-Clause | NOT LOCKED |
| numba | unpinned | none | BSD-2-Clause family | NOT LOCKED |
| nvidia-ml-py | unpinned | none | package-specific verification required | NOT LOCKED |

Licence-family entries are preliminary metadata, not legal advice or a redistribution decision. Every resolved artifact and transitive dependency requires re-verification before installation.

## Compatibility reading

The official PyTorch previous-version record lists PyTorch 2.0.1, torchvision 0.15.2, torchaudio 2.0.2 and pytorch-cuda 11.8 as a supported historical Conda combination.

The PyTorch Geometric 2.5.3 documentation supports Python 3.8–3.12 and basic use with PyTorch alone. Optional compiled extensions require a matching PyTorch/CUDA wheel set and introduce additional build and supply-chain decisions.

Therefore the declared top-level tuple is plausible, but this does not prove the full environment will solve or run.

## Reproducibility gaps

The environment file lacks:

- operating-system and architecture target;
- exact Python patch;
- exact NumPy patch;
- pip and Conda versions;
- versions for seven pip packages;
- transitive dependency versions;
- channel-qualified package origins;
- channel-priority rule;
- Conda build strings;
- artifact URLs;
- package hashes;
- CUDA driver requirement;
- optional PyG extension decision;
- exported explicit environment;
- multi-platform lock;
- SBOM;
- vulnerability review.

No solver was run, so no hidden transitive package set is claimed.

## Channel and terms risk

The inclusion of defaults can access Anaconda-maintained offerings.

Anaconda terms dated 2025-07-15 distinguish free-use eligibility and cases requiring a Business Plan, and also identify additional restrictions for enterprise-scale deployment. ClimateOS has not determined an organizational eligibility category and has made no acceptance or payment commitment.

A future environment plan must decide, before access:

- whether defaults is required;
- whether nodefaults and explicitly qualified community/upstream channels can satisfy the environment;
- which Anaconda or Miniconda terms would apply;
- whether legal or procurement review is required.

No channel access or package download was performed in this batch.

## Proposed lock strategy

Documentation proposal only:

1. declare target platform and GPU/CPU profile;
2. remove or justify every channel;
3. qualify package origins;
4. pin every direct dependency;
5. decide whether optional PyG compiled extensions are needed;
6. solve only in an isolated temporary environment after authorization;
7. export a platform-specific explicit artifact list;
8. generate a multi-platform lock only for approved targets;
9. record URLs, hashes, licences and transitive dependencies;
10. create an SBOM and vulnerability snapshot;
11. preserve rollback and deletion procedures.

## Decision

The source environment is historically plausible but not reproducible, legally cleared or execution-ready.

Environment creation remains blocked.
