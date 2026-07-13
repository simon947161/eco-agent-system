# Task1529 — UniCM Zero-Cost Acquisition Plan

Date: 2026-07-14

Status: PLAN ONLY / NO ACQUISITION AUTHORIZED

## Principle

Zero cost means no direct external charge. It does not mean zero governance, zero labour, unlimited downloads or permanent rejection of paid resources.

Current approved direct cost remains **AUD 0**.

## Phase A — completed metadata work

Completed without acquiring file content:

- verified Nature paper identity and source links;
- verified GitHub repository, v1.0 tag and commit;
- verified v1.0/main equivalence;
- verified Zenodo record, file name, byte size and checksum metadata;
- verified MIT software licence;
- established that no pretrained weights are published in the inspected release/archive inventory;
- mapped code-expected dataset files and variables;
- created static compute/storage bounds and security controls.

## Phase B — possible future source-only acquisition

Requires new Founder authorization.

Maximum proposed asset:

- Zenodo v1.0 source ZIP only;
- 1,103,721 bytes;
- expected MD5 `ab8a324953bb91a5f00e0e38a8a08348`;
- direct cost: AUD 0.

Procedure:

1. download into quarantine;
2. verify published MD5 and calculate SHA-256;
3. scan archive without execution;
4. extract into an isolated read-only source zone;
5. compare tree to pinned Git commit;
6. preserve licence and provenance;
7. produce a source-integrity report;
8. delete and re-acquire if any mismatch occurs.

This phase would not install dependencies or run code.

## Phase C — checkpoint inquiry

Because weights are absent, use no-cost evidence channels first:

- inspect maintainer release notes and repository issues;
- inspect future official releases/Zenodo versions;
- prepare a concise maintainer inquiry asking whether paper checkpoints and preprocessing assets will be released;
- do not send external messages without separate user direction;
- reject unofficial weights until authenticated.

## Phase D — provider-side data planning

Before any download:

- use official catalogue metadata;
- select only exact variables, periods and grids required;
- calculate expected byte counts provider-side;
- confirm terms and citation;
- decide whether a tiny metadata/sample request can answer the question;
- avoid bulk “download everything” behaviour.

No dataset request is authorized by this plan.

## Phase E — resource decision

After source, checkpoint and data manifests are complete:

- compare local hardware with static VRAM/storage ranges;
- prefer a tiny synthetic structural test before real data;
- prepare separate options for local GPU, free research compute and paid cloud;
- prepare a Paid Decision Brief only if free/local options are inadequate.

## Stop conditions

Stop before acquisition if:

- the asset source is not authoritative;
- checksum metadata is absent;
- licence scope is unclear;
- archive contents differ from the pinned tree;
- a download expands beyond the approved byte ceiling;
- credentials or payment details are requested;
- an asset contains unexpected executables or weights;
- the plan drifts into model execution.

## Task1529 decision

A source-only, approximately 1.05 MiB, zero-direct-cost acquisition could be considered safely under a separate authorization.

Model weights and climate datasets are not part of that proposed acquisition.
