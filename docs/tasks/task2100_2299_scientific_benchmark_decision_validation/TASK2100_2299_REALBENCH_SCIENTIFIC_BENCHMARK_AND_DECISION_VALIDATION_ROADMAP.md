# Task2100–2299 — RealBench-Inspired Scientific Benchmark and Decision Validation Roadmap

Date: 2026-07-12
Status: Long-range founder roadmap / deferred research target
Project: ClimateOS / Eco-Agent-System
Primary return gate: **Task2100**
Planning horizon: Task2100–2299

## 1. Founder decision

The Founder has decided that RealBench-inspired operational benchmarking, out-of-distribution evaluation, extreme-weather stress testing, and downstream decision validation are important, but must not interrupt the current ClimateOS execution line or be pulled forward into the earlier Task1200–1700 roadmap.

This work is therefore intentionally deferred until after the Environmental AI Scientist roadmap reaches Task2099.

> Task2100 is the formal ClimateOS return point for RealBench-inspired business-condition testing and scientific benchmark architecture.

Before Task2100, ClimateOS may preserve research notes and references only. No benchmark implementation, model re-ranking, large-scale evaluation run, or new scientific workstream is authorized by this roadmap.

## 2. Why this work is placed after Task2099

RealBench is not simply another model metric. Its strongest value appears only after ClimateOS has already established:

- model and dataset provenance;
- hybrid physical-and-AI forecast interfaces;
- environmental coupling structures;
- mechanism experiment records;
- scientific evidence passports;
- controlled AI-scientist workflows;
- human-governed decision pathways.

Only then can ClimateOS evaluate not merely whether a weather model scores well, but whether the full scientific and decision pipeline remains reliable under new climate states, unseen years, extreme events, operational latency, missing data, and model disagreement.

The sequencing principle is:

```text
Build the scientific system
→ make its evidence traceable
→ make its tools governable
→ then stress-test the whole system under realistic conditions
```

## 3. Strategic position

Task2100–2299 creates a later-stage **Scientific Benchmark and Decision Validation Layer**.

It is downstream of:

```text
Task1200–1499: model assurance and hybrid weather runtime
Task1500–1700: environmental coupling layer
Task1701–1899: mechanism experiment layer
Task1900–2099: environmental AI scientist runtime
```

It does not replace those layers. It evaluates whether they remain reliable when used together.

## 4. Reference framework

RealBench is registered as an independent reference framework for:

- strict out-of-distribution testing;
- recent-year, zero-leakage evaluation;
- extreme-weather event challenge sets;
- operational forecast conditions;
- robustness under climate-regime shift;
- evaluation beyond average RMSE and ACC.

RealBench is not treated as a code dependency, model dependency, or automatic implementation target. At Task2100, the latest paper, official repository, licence, dataset terms, benchmark protocol, and successors must be re-verified.

## 5. Proposed roadmap

### Task2100–2139 — Benchmark Governance and Source Verification

- verify the latest RealBench publication, maintainers, repository, licence and dataset access;
- identify whether later benchmarks have superseded or extended it;
- register benchmark versions and data leakage controls;
- define benchmark governance and reproducibility rules;
- separate published benchmark claims from ClimateOS interpretation.

**Deliverable:** RealBench and Operational Benchmark Source Dossier.

### Task2140–2179 — Out-of-Distribution and Temporal Generalisation Protocol

- define training-cutoff and evaluation-period separation;
- establish zero-leakage checks;
- test climate-regime and recent-year generalisation;
- record dataset revisions and retrospective contamination risks;
- define acceptable and unacceptable forms of model adaptation.

**Deliverable:** ClimateOS OOD Evaluation Protocol v0.1.

### Task2180–2219 — Extreme Event Stress-Test Library

Candidate event families:

- tropical cyclones;
- extreme rainfall and flooding;
- heatwaves;
- cold outbreaks;
- atmospheric rivers;
- high-wind and fire-weather episodes;
- compound heat–drought–fire events;
- smoke and air-quality episodes.

The library must preserve event definitions, references, thresholds, lead times, spatial scales and uncertainty.

**Deliverable:** ClimateOS Extreme Event Stress-Test Library v0.1.

### Task2220–2259 — Operational Robustness Benchmark

Evaluate system behaviour under:

- delayed or missing observations;
- partial model failure;
- stale initialization;
- model disagreement;
- latency constraints;
- infrastructure interruption;
- fallback activation;
- version drift;
- incomplete downstream data.

**Deliverable:** ClimateOS Operational Resilience Benchmark v0.1.

### Task2260–2299 — Decision Validation and Impact Benchmark

Extend evaluation from model skill to decision value.

Candidate questions:

- Did the system provide useful lead time?
- Did uncertainty remain visible?
- Did downstream agents amplify or reduce model error?
- Did the decision recommendation change for a valid reason?
- Would a human reviewer have been able to detect failure?
- Did the intervention reduce environmental or social harm?

Candidate domains:

- flood preparedness;
- fire-weather planning;
- water allocation;
- energy demand and reliability;
- biodiversity and restoration planning;
- building and infrastructure risk.

**Deliverable:** ClimateOS Decision Benchmark v0.1 and Task2299 maturity review.

## 6. Benchmark dimensions

The later benchmark architecture should distinguish at least five dimensions:

```text
1. Statistical skill
   RMSE, ACC, CRPS and calibration

2. Physical consistency
   mass, water, energy, spectrum and dynamical balance

3. Operational generalisation
   OOD years, new circulation regimes, latency and failure conditions

4. Extreme-event usefulness
   intensity, location, timing, lead time and tail behaviour

5. Decision value
   whether the full pipeline supports safer and more defensible action
```

PhysMetrics.Weather remains a separate physical-consistency reference. RealBench remains a separate operational and extreme-event reference. They must not be collapsed into one framework or one score.

## 7. Decision-pipeline evaluation

The long-term ClimateOS benchmark target is not only:

```text
Model → Forecast Score
```

It is:

```text
Source model
→ transformation and downscaling
→ environmental coupling
→ impact model
→ evidence interpretation
→ human-reviewed decision
→ observed outcome
```

Every stage should preserve provenance, uncertainty and transformation history so that failure can be located rather than hidden inside an end-to-end score.

## 8. Boundaries

This roadmap does not authorize:

- immediate RealBench implementation;
- downloading benchmark datasets now;
- moving Task2100 work into current ClimateOS sprints;
- claiming that RealBench alone proves model safety;
- collapsing statistical, physical, operational and decision metrics into one opaque score;
- automated public-warning approval;
- retrospective claims of lives or losses saved without evidence.

## 9. Permanent reminder

> When ClimateOS approaches Task2100, retrieve this roadmap and the RealBench reference file, verify the then-current scientific and repository state, and request fresh Founder authorization before any benchmark implementation.

Until then, continue the active ClimateOS roadmap without interruption.

## Project keywords

ClimateOS; Task2100; Task2100–2299; RealBench; operational benchmark; out-of-distribution; OOD; zero leakage; extreme weather; stress testing; model robustness; decision benchmark; impact validation; scientific assurance; human governance; Earth System Decision Intelligence.