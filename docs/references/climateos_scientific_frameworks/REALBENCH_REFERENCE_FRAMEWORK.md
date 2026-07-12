# RealBench Reference Framework for ClimateOS

Date: 2026-07-12
Status: Independent scientific reference / deferred implementation
Primary roadmap placement: Task2100–2299

## Purpose

This file registers RealBench as an independent reference framework for evaluating data-driven numerical weather prediction systems under realistic operational conditions, strict out-of-distribution testing and extreme-weather event challenges.

RealBench must not be merged conceptually with PhysMetrics.Weather, AICON, UniCM or TianJi-Environ:

- PhysMetrics.Weather focuses on physical consistency;
- AICON provides an operational hybrid weather-system reference;
- UniCM informs coupled climate-mode intelligence;
- TianJi-Environ informs mechanism experiment and evidence-chain workflows;
- RealBench informs OOD, extreme-event and business-condition stress testing.

## Scientific reference

Paper:

*RealBench: Benchmarking Data-Driven Numerical Weather Prediction under Real-World Operational Conditions and Extreme Weather Challenges*

Preprint supplied by the Founder:
https://arxiv.org/pdf/2605.24945

At the future Task2100 gate, the authoritative publication record, authorship, repository, licence, benchmark data, test periods, model submissions and updated successors must be re-verified.

## Key ideas to preserve

- use evaluation periods after the training cut-off of major models;
- minimise or detect temporal data leakage;
- test distribution shift rather than only historical interpolation;
- include extreme-weather event subsets;
- evaluate business-like initialization and operational conditions;
- avoid relying only on global-average RMSE and ACC;
- report where, when and under which regime a model fails.

## ClimateOS interpretation

RealBench should later help ClimateOS evaluate:

1. temporal generalisation;
2. climate-regime shift;
3. extreme-event performance;
4. operational latency and robustness;
5. failure behaviour and fallback;
6. downstream impact on environmental decisions.

RealBench itself should not be treated as proof that a model is safe or suitable for public warning. ClimateOS should combine it with physical-consistency assessment, uncertainty calibration, provenance, domain-specific impact testing and human review.

## Deferred status

The Founder has explicitly decided not to add this work to the active or earlier Task1200–1700 execution line. Its formal return point is Task2100.

Before Task2100:

- preserve references only;
- do not implement the benchmark;
- do not download large datasets;
- do not reorganize current tasks around RealBench;
- do not claim ClimateOS compliance with RealBench.

## Future relationship to ClimateOS Decision Benchmark

RealBench primarily evaluates forecast behaviour under realistic and extreme conditions. ClimateOS may later extend this toward a decision-pipeline benchmark:

```text
forecast quality
→ environmental interpretation
→ impact estimate
→ human-reviewed decision
→ observed outcome
```

That extension is a ClimateOS research direction, not a claim made by the RealBench authors.

## Permanent retrieval terms

RealBench; Task2100; Task2100–2299; OOD weather benchmark; temporal leakage; 2025 test data; extreme weather evaluation; operational weather AI; ClimateOS Decision Benchmark.