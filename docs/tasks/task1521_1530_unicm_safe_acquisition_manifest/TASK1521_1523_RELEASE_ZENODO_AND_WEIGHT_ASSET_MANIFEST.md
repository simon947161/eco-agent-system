# Task1521–1523 — UniCM Release, Zenodo and Weight Asset Manifest

Date: 2026-07-14

Status: METADATA VERIFIED / WEIGHTS ABSENT

## GitHub release identity

- Repository: https://github.com/tsinghua-fib-lab/UniCM-Global-Climate-Modes
- Release/tag: `v1.0`
- Release title: `v1.0 - Learning the coupled dynamics of global climate modes`
- Release date shown by GitHub: 2026-03-23
- Release commit: `67fe4c183df351d5039c5b3b80ae86a68b627398`
- Release author shown by GitHub: `YuanYuan98`
- GitHub release page: https://github.com/tsinghua-fib-lab/UniCM-Global-Climate-Modes/releases/tag/v1.0

A GitHub compare operation returned `identical` for `v1.0...main`, with zero commits ahead or behind. The release tag, current main and the Task1500 pinned commit therefore resolve to the same source tree as of this review.

The release page reports two assets but exposes no separately named weight package in the inspected metadata. These are consistent with GitHub-generated source archives, not evidence of checkpoints.

## Zenodo record identity

Read-only public API metadata was inspected. No file content was downloaded.

| Field | Verified value |
|---|---|
| Record ID | `19173780` |
| Concept record | `19173779` |
| DOI | `10.5281/zenodo.19173780` |
| Version | `v1.0` |
| Publication date | 2026-03-23 |
| Creator | Yuan Yuan, Tsinghua University |
| Resource type | Software |
| Access | Open |
| Licence | MIT |
| Related GitHub | `.../tree/v1.0` |
| Record status | Published |
| File count | 1 |

### Zenodo file inventory

| File | Size | Checksum | Classification |
|---|---:|---|---|
| `tsinghua-fib-lab/UniCM-Global-Climate-Modes-v1.0.zip` | 1,103,721 bytes | `md5:ab8a324953bb91a5f00e0e38a8a08348` | source-code archive |

Software Heritage directory identifier recorded by Zenodo:

`swh:1:dir:fd31447bccd6ac7912d53aa299e775ac4463f6ba`

This provides an additional immutable provenance anchor.

## Weight search result

The inspected source tree and documentation contain:

- checkpoint path parameters;
- expected local `model_best.pkl` paths;
- model-saving and loading code;
- ensemble paths such as `SaveModel_Seed<SEED>`.

They do not contain or identify:

- a downloadable `.pt`, `.pth`, `.ckpt` or trained `.pkl` package;
- a model-card or checkpoint checksum;
- checkpoint size or training provenance;
- a licence separate from source;
- a published 20-seed ensemble.

The Zenodo source archive is approximately 1.05 MiB and is explicitly described as source code. It is not a credible container for the trained ensemble described by the scripts.

## Admission decision

| Asset | Status |
|---|---|
| GitHub v1.0 source | VERIFIED |
| Current main equivalence | VERIFIED |
| Zenodo source archive | VERIFIED BY METADATA |
| Source checksum | VERIFIED AS PUBLISHED METADATA |
| Software Heritage anchor | VERIFIED AS PUBLISHED METADATA |
| Pretrained single checkpoint | NOT FOUND |
| Pretrained ensemble | NOT FOUND |
| Checkpoint licence/checksum | NOT AVAILABLE |
| Inference readiness | BLOCKED |
| Training authorization | NOT GRANTED |

## Consequence

There is no authorized or evidenced “download weights and run inference” path.

A future path must either:

1. obtain authoritative checkpoint evidence from the authors; or
2. propose a bounded training reproduction with a new Founder gate, data budget, compute budget and scientific acceptance criteria.

Third-party checkpoint mirrors are prohibited unless independently authenticated by the maintainers.
