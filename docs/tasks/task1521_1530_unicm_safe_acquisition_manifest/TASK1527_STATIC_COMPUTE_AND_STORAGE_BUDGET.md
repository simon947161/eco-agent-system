# Task1527 — UniCM Static Compute and Storage Budget

Date: 2026-07-14

Status: STATIC ESTIMATE / NOT BENCHMARKED

## Method boundary

No Python environment, PyTorch model, dataset or checkpoint was loaded. All calculations below are analytical estimates derived from inspected default configuration and source structure.

They are planning bounds, not benchmark results.

## Default architecture inputs used

- embedding dimension `d=256`;
- four encoder and four decoder layers per branch;
- physical-field and climate-mode branches;
- five physical input channels;
- patch size `2×2`;
- physical patch count `12×72/(2×2)=216`;
- 12-month history;
- 24-month prediction;
- batch size 32 in the supplied training script;
- 20 training seeds.

## Static parameter estimate

Counting embeddings, output layers, attention projections, feed-forward layers and layer-normalization parameters gives an approximate total of:

- **12.73 million trainable parameters**;
- approximately **48.5 MiB** of float32 parameter storage.

This estimate is consistent with the code's relatively compact parameter design, but parameter size is not the primary memory risk.

A typical float32 Adam training state may require roughly:

- parameters;
- gradients;
- first moments;
- second moments.

That is approximately 194 MiB before framework overhead, saved activations or temporary tensors.

## Activation and attention pressure

For batch 32, 216 spatial patches, 24 time steps and dimension 256:

- one full feature tensor is about **162 MiB** in float32;
- one four-head spatial-attention score tensor at 24 steps is about **547 MiB**;
- the equivalent 12-step score tensor is about **273 MiB**.

Multiple encoder/decoder layers and gradient retention can multiply these figures. Autoregressive decoding and duplicated temporary tensors add further pressure.

### Planning judgement

- 8 GiB GPU: likely inadequate for default batch-32 training;
- 16 GiB GPU: uncertain and potentially inadequate without batch reduction or memory optimisation;
- 24 GiB GPU: plausible dry-run candidate, still unverified;
- CPU-only: code permits CPU fallback in places, but feasibility and runtime are unknown.

These are conservative planning judgements, not purchase recommendations. No GPU acquisition or cloud booking is authorized.

## Checkpoint storage

Approximate raw float32 state-dict size per model is near parameter storage, around 49 MiB before serialization overhead.

A 20-seed ensemble would therefore require at least about 1 GiB for one checkpoint per seed, and potentially several GiB when best/latest/optimizer states and logs are retained.

No actual checkpoint package is available for verification.

## Dataset storage bands

Exact provider file sizes are unknown. The code's expected monthly global/tropical grids and multi-decade periods imply:

| Budget level | Purpose | Planning band |
|---|---|---:|
| Metadata only | catalogues, terms, variable manifests | under 100 MiB |
| Source archive only | GitHub/Zenodo source snapshot | under 10 MiB |
| Tiny synthetic structural fixture | future parser/shape test only | under 1 GiB |
| Single bounded preprocessed evaluation subset | future, exact subset required | 5–25 GiB |
| Multi-dataset reproduction workspace | CMIP6 + ERA5 + ORAS5 + SODA + GODAS, raw and derived | 50–250+ GiB |
| Full retained experiment with checkpoints/temp/backup | reproduction plus evidence retention | 100–500+ GiB |

The last three bands are deliberately broad because native grid, depth levels, compression, chunking and duplicate transformed files are unresolved.

## Compute-time budget

No defensible wall-clock estimate is possible without:

- actual GPU;
- exact paper hyperparameters and epoch count;
- checkpoint or training path;
- final data dimensions;
- dataloader performance;
- batch-size feasibility.

The supplied script's two epochs and twenty seeds must not be assumed to reproduce the paper.

## Cost position

Approved external spend: **AUD 0**.

Metadata review can continue at zero direct cost. Any future paid GPU, storage, article, egress or expert service requires a separate Paid Decision Brief and explicit Founder approval.

## Task1527 conclusion

Static analysis identifies activation memory and data preparation—not parameter count—as the dominant resource risks.

Model execution remains blocked until a separately authorized, hardware-specific dry-run plan exists.
