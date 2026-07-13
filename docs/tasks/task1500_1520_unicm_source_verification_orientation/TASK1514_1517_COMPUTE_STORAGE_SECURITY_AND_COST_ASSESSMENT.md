# Task1514–1517 — Compute, Storage, Security and Cost Assessment

Date: 2026-07-14

Status: PRELIMINARY / NO RESOURCE COMMITMENT

## Evidence boundary

This assessment is based on read-only inspection of repository metadata, `environment.yml`, configuration, loaders and shell scripts.

No dependency was installed. No environment was created. No model, parameter-count script or benchmark was run. No dataset size was queried through bulk download. Numerical resource requirements therefore remain estimates or unknowns.

## 1. Software environment

Verified dependency baseline:

- Python 3.11;
- PyTorch 2.0.1;
- CUDA 11.8 toolkit package;
- torchvision 0.15.2;
- torchaudio 2.0.2;
- NumPy 1.26;
- torch-geometric 2.5.3;
- xarray, NetCDF4, scikit-learn, numba, timm and NVIDIA monitoring packages;
- Conda-based environment.

Risks:

- an older CUDA/PyTorch stack may conflict with current drivers;
- transitive pip packages are not fully pinned;
- `environment.yml` is not a cryptographic lock file;
- shell scripts assume a Unix-like environment;
- arbitrary upstream environment installation is a supply-chain action and belongs after Task1521 authorization.

## 2. Compute demand

Code facts:

- embedding dimension: 256;
- four encoder and four decoder layers per branch by default;
- five input channels;
- 12-month history and 24-month prediction windows;
- default batch size: 32;
- training script iterates 20 seeds;
- training and ensemble paths select CUDA device 0 when available;
- model size is printed only after initialization.

Unknowns:

- parameter count and in-memory activation size;
- peak VRAM by batch size;
- training time per seed and total ensemble time;
- exact paper-result epoch count and hyperparameters;
- inference time;
- CPU-only feasibility;
- multi-GPU or mixed-precision support;
- reproducibility across GPU architectures.

Current decision:

`COMPUTE_REQUIREMENTS_UNVERIFIED`

No GPU purchase or cloud reservation is justified at this stage.

## 3. Storage demand

Storage components include:

- selected CMIP6 training fields across multiple models/periods;
- ERA5, ORAS5, SODA and GODAS evaluation files;
- transformed NetCDF copies;
- temporary arrays and caches;
- 20 seed checkpoints;
- ensemble predictions and target outputs;
- logs, evidence hashes and retained provenance copies.

Exact volume is unknown because the code assumes preprocessed local files without publishing a complete manifest.

Task1521 must calculate three budgets before download:

- minimum metadata/sample-only budget;
- bounded single-checkpoint inference budget;
- published-result reproduction budget.

Each budget must include raw, transformed, checkpoint, temporary and evidence-retention storage, plus a deletion plan.

## 4. Security controls required for Task1521

- use an isolated research workspace outside ClimateOS core;
- pin immutable upstream commit and asset checksums;
- inspect environment and scripts before installation;
- do not execute downloaded notebooks or shell scripts automatically;
- prohibit secrets in configuration and logs;
- use read-only source mirrors where practical;
- record outbound endpoints;
- apply least-privilege filesystem permissions;
- scan dependencies and archives;
- separate untrusted model artefacts from operational data;
- prohibit deserializing unverified PyTorch checkpoints;
- retain software-bill-of-materials and licence records;
- define stop and cleanup procedures.

PyTorch checkpoint files can execute unsafe deserialization paths when untrusted. Only author-verified, checksum-pinned weights may be considered.

## 5. Cost position

Current approved direct external cost:

`AUD 0`

Free/open/public options are preferred for orientation but are not treated as permanently mandatory.

Potential future costs:

- article or supplementary access;
- storage;
- cloud GPU time;
- egress;
- backup;
- expert climate-science review;
- engineering time.

No amount is estimated responsibly until the weight, data and runtime manifests are complete.

Any paid resource requires a separate Paid Decision Brief covering provider, billing basis, ceiling, alternatives, ownership, retention, cancellation, lock-in and exit plan.

## 6. Task1517 resource gate

Current result:

`CONSTRAINED_GO_FOR_FURTHER_DOCUMENTED_PREFLIGHT_ONLY`

Not approved:

- GPU or cloud booking;
- hardware purchase;
- Conda/CUDA installation;
- model or dataset download;
- repository clone/fork/vendor;
- model initialization or execution;
- paid article purchase.

Task1521 must begin, if authorized, with acquisition planning and immutable metadata capture—not execution.
