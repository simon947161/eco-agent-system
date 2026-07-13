# Task1531–1532 — Bounded Source Acquisition and Provenance

Date: 2026-07-14

Status: COMPLETE

## Authorized object

Exactly one release asset was acquired:

- provider: Zenodo;
- record: 19173780;
- DOI: 10.5281/zenodo.19173780;
- release: UniCM v1.0;
- file: tsinghua-fib-lab/UniCM-Global-Climate-Modes-v1.0.zip;
- declared size: 1,103,721 bytes;
- licence: MIT;
- related GitHub repository: tsinghua-fib-lab/UniCM-Global-Climate-Modes;
- pinned source commit: 67fe4c183df351d5039c5b3b80ae86a68b627398.

## Transfer control

The transfer command applied a 2,097,152-byte maximum-file-size control before writing the asset.

Result:

| Control | Outcome |
|---|---|
| One authorized ZIP only | PASS |
| 2 MiB hard ceiling | PASS |
| Observed size | 1,103,721 bytes |
| Excess-size transfer | NOT OBSERVED |
| Weight or checkpoint transfer | NONE |
| Climate-data transfer | NONE |

The source ZIP occupied approximately 52.63% of the permitted ceiling.

## Isolation

The asset was written under a newly generated temporary directory:

/tmp/climateos-task1531-1540.[random]

It was not written into the ClimateOS repository, working branch, dependency cache or operational runtime.

Network activity was limited to:

1. the authorized Zenodo source-asset transfer;
2. a depth-one, blob-filtered Git metadata fetch for the pinned commit tree;
3. governance and read-only file identity checks through the connected GitHub repository service.

No model, live-data or climate-data API was invoked.

## Provenance decision

The acquired object is admitted only as an integrity-verified source snapshot. It is not admitted as:

- an executable ClimateOS dependency;
- a pretrained model;
- a checkpoint;
- a data product;
- an operational climate source;
- evidence of Australian regional skill.

## Retention decision

The ZIP and extracted files remain temporary quarantine artifacts. Only hashes, inventory, provenance and comparison results are retained in the repository documentation.
