# Task1537–1538 — Pinned GitHub Tree Comparison

Date: 2026-07-14

Status: COMPLETE / EXACT MATCH

## Fixed reference

Repository:

tsinghua-fib-lab/UniCM-Global-Climate-Modes

Commit:

67fe4c183df351d5039c5b3b80ae86a68b627398

## Method

The extracted files were staged into a newly initialized Git object database inside the temporary quarantine. This calculated Git blob and tree identities without running upstream content.

The fixed commit was then fetched at depth one with blob filtering. No checkout occurred.

Checks performed:

1. verify FETCH_HEAD resolved to the exact authorized commit;
2. calculate the extracted staged-tree hash;
3. read the fixed commit tree hash;
4. compare staged paths, content and modes against FETCH_HEAD;
5. independently compare all 17 local blob hashes with the corresponding fixed-commit file identities.

## Results

| Evidence | Value |
|---|---|
| Requested commit | 67fe4c183df351d5039c5b3b80ae86a68b627398 |
| Resolved FETCH_HEAD | 67fe4c183df351d5039c5b3b80ae86a68b627398 |
| Extracted staged-tree hash | 501b96a31096b8d5f66bff93c32c6135c5d44537 |
| Fixed commit tree hash | 501b96a31096b8d5f66bff93c32c6135c5d44537 |
| Name-status diff | EMPTY |
| File/blob comparisons | 17 of 17 exact |
| Mode differences | NONE |

## Blob identities

| Path | Git blob SHA-1 |
|---|---|
| .gitignore | 184b86137cfb0e5af125cddaa69872d8db68afd1 |
| LICENSE | 78a588b58a31fc498cbe52c0829319246732820b |
| README.md | 057d489adf1b2382de816b1fc2c56f5f22482d3a |
| assets/framework.png | ff2d10601e726e588d5ba76e68f79b363fd3e8e9 |
| environment.yml | 01d1005b42a7da5c0ad052b182f63f038502b266 |
| src/Embed.py | df39417ade879d477cd378d240624d29fa2c7fad |
| src/LoadData.py | 38886f02c24d1d3550ce3ebd1d36317c282b91e8 |
| src/Trainer.py | 59010e5725a7dbbe1a4d45658cd31ea34f8ae59f |
| src/app_ensemble.py | ec3156174405f266f43f4dabe944614a9f4eb830 |
| src/app_test.py | b4c12d6d40b703dffcab8b25902aeb6b4b1a8cd2 |
| src/app_train.py | ad1eb0c1b1a2e1327cfd5f10d77a01698e928c37 |
| src/config.py | 863de9e3e991b26f584d3d0a5c2f268e8fff47bb |
| src/models.py | 22aab3c173ababe4ba78e6aa665b85907d2b05e1 |
| src/my_tools.py | a45603e828cf4a740865006dd8ea99d9f720cfd7 |
| src/script/test.sh | 6d26e2cf82fded6dacf398d2e5e1c99086adec80 |
| src/script/train.sh | e643f2e28e12a594b2b536d5f5034a3d0a18495c |
| src/settings.py | 633da339cb459c1ca2ab58a3129fc5415f43fa16 |

## Decision

The Zenodo v1.0 ZIP is a content- and mode-exact snapshot of the pinned GitHub commit tree.

This conclusion establishes source integrity only. It does not establish dependency safety, runtime reproducibility, scientific validity, checkpoint availability or operational readiness.
