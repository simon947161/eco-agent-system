# ClimateOS Task1701–1710 — Mechanism Experiment Return-Gate Revalidation and No-Run Readiness Pack

Status: local implementation complete; independent Founder review required

Base main HEAD: `5bfc2312b8d93783de7e94af57d8a86351f71563`

## Purpose

Re-open the Mechanism Experiment Layer at a controlled return gate without
installing or running a scientific model. This batch distinguishes useful
reference architecture from an admitted, reproducible experiment runtime.

## Task map

| Task | Closed result |
|---|---|
| 1701 | Verified the post-PR #74 main HEAD and Task1500–1700 closure |
| 1702 | Defined a closed return-gate state and refusal contract |
| 1703 | Revalidated TianJi and TianJi-Environ identities and artifact limits |
| 1704 | Candidate-locked WRF `release-v4.8.0` at `0708348f…` pending Release recheck |
| 1705 | Separated WRF core, WRF-Chem, WPS, schemes, inputs and compute |
| 1706 | Added falsification, alternatives, scale/time and expert-owner requirements |
| 1707 | Defined a no-run experiment-registration contract |
| 1708 | Recorded version, licence, data, compute, expert and reproducibility gaps |
| 1709 | Tested static registration and mandatory execution refusal paths |
| 1710 | Returned `REFERENCE_REVIEW_INCOMPLETE` and a separate Founder gate |

## Result

TianJi-Environ is useful as an independent workflow reference. Its public
repository currently describes curated manuscript artifacts, selected scripts
and sanitized summaries, not a complete WRF-Chem runtime. Full reproduction
requires external model, data and compute assets.

The official WRF repository contains a `release-v4.8.0` branch whose observed
head declares version 4.8.0. Because public Release views were not fully
consistent during review, ClimateOS records a candidate version lock rather
than claiming a final runnable release.

No source code repository was cloned, model or dependency installed, dataset or
observation downloaded, scientific run performed, or causal/local conclusion
formed.
