# ClimateOS Task1631–1640 to Task1641+ WeatherBench Reference Continuation ACTP

**Date:** 2026-07-16  
**Status:** READY_FOR_NEXT_THREAD / PREFLIGHT_ONLY / NOT_EXECUTABLE  
**Repository:** `simon947161/eco-agent-system`  
**Authoritative branch:** `main`  
**Authoritative HEAD at handoff:** `e1bbd566483ba0a416758f639479ca3d4f27b09d`  
**Current execution branch:** `agent/task1631-1640-bondo-evidence-passport-claim-graph`  
**Current Draft PR:** #67  
**Current Draft PR HEAD before this ACTP:** `9169f0d02fee56f8ef1158ec5d4249f48d9cd2ea`

## 1. Purpose

This ACTP transfers the current ClimateOS state into a clean thread without reopening or repeating superseded Task1200–1299 work.

It also records the Founder direction that WeatherBench should be treated as a valuable external scientific evaluation resource: reuse what is genuinely open, lawful, inspectable and fit for purpose; preserve attribution and versioning; and extend rather than imitate it where ClimateOS has different regional, physical-consistency, governance and human-review requirements.

This document does not authorize Task1641+, merge PR #67, run WeatherBench/WeatherBench-X, acquire large datasets, incur cloud cost, submit a ClimateOS model, or make a forecast-quality or admission conclusion.

## 2. Verified repository state

### Superseded historical draft

PR #48, **Close Task1200-1289 season and propose Task1290-1299 gate**, is closed and unmerged. It was a documentation-only, `DRAFT_FOR_FOUNDER_REVIEW / NOT_EXECUTABLE` package based on an old branch and old baseline. It must not be reopened or merged into the current main line.

The work it anticipated was superseded by the later controlled implementation and merge chain. Task1200–1289 is therefore not an unfinished season requiring PR #48.

### Later merged main-line chain

The verified later history includes:

- PR #42 merged: scientific roadmap and model-neutral parallel-model architecture;
- PR #51 onward: later model/source/data/evaluation and environmental-coupling stages;
- PR #65 merged: Task1611–1620 Bondo boundary and EIS readiness;
- PR #66 merged: Task1621–1630 Bondo EIS intake and review decision pack;
- main HEAD `e1bbd566483ba0a416758f639479ca3d4f27b09d` activates Task1631–1640;
- PR #67 is the current open Draft for Task1631–1640.

No task-number rollback is permitted.

## 3. Current Task1631–1640 state

PR #67 is documentation-only and currently contains:

- Bondo Wind Evidence Passport and Claim Graph v0.1;
- scientific-review dry run and Founder decision view;
- Task1631–1640 formal brief;
- Task1640 closure and next-gate brief.

The passport distinguishes official evidence, proponent statements, regional-context evidence, missing evidence and rejected claims. It does not establish Bondo site wind, hub-height wind, capacity factor, energy yield, project viability or scientific approval.

PR #67 remains Draft and must not be merged without a fresh explicit Founder merge decision.

## 4. What WeatherBench is

WeatherBench is an external Google Research community benchmark, not a ClimateOS-built website.

Its official scope is like-for-like evaluation of data-driven and traditional numerical global weather forecasting models, with a focus on medium-range forecasts. It provides:

- public, cloud-optimized ground-truth and baseline datasets;
- open-source evaluation code;
- deterministic and probabilistic evaluation views;
- a public score website;
- documented model-submission and evaluation conventions.

The WeatherBench 2 repository is Apache-2.0 licensed. Its own repository now recommends moving evaluation-code users to the newer WeatherBench-X codebase while retaining the WeatherBench 2 data guide. Code licensing does not automatically settle every dataset's licence, access condition, transfer cost or compute cost.

## 5. What Codex/ClimateOS has used it for so far

Verified repository search did not find a direct WeatherBench implementation, clone, dependency, adapter or execution record in ClimateOS.

Therefore the defensible statement is:

- WeatherBench has been used as an external research and architecture reference for evaluation concepts;
- it has **not** yet been proven to be installed, run, integrated or used to score a ClimateOS model;
- no ClimateOS result may be described as a WeatherBench result until the exact code version, data objects, configuration, compute run and output provenance are recorded.

## 6. Founder integration direction

ClimateOS should absorb WeatherBench through a controlled adapter/reference strategy.

### Reuse candidates

1. Metric definitions and evaluation conventions where semantically compatible.
2. Variable, pressure-level, lead-time, initialization-time and valid-time conventions.
3. Baseline and ground-truth catalogue metadata.
4. Deterministic, probabilistic, precipitation and spectral evaluation structures.
5. Reproducible configuration and provenance patterns.
6. Public comparison UX patterns that clearly expose variable, lead time, level, reference and evaluation period.

### ClimateOS extensions that remain separate

1. Regional fitness for Karamay and NSW South East/Tablelands.
2. Extreme-event, sample-sufficiency, non-stationarity and OOD evidence.
3. Physical-consistency assurance and missing-variable blocking.
4. Scale translation from global/grid output to regional or site evidence.
5. Licence, cost, storage, provenance, revision, dispute and counter-evidence history.
6. Human scientific review, uncertainty and non-operational decision boundaries.
7. Domain coupling and environmental evidence passports.

WeatherBench scores must not be transformed automatically into a ClimateOS ranking, model-admission decision, public warning, compliance statement, legal conclusion or investment conclusion.

## 7. Required WeatherBench intake gates

Before any implementation or execution, the next authorized batch must record:

- exact upstream repository: WeatherBench-X or legacy WeatherBench 2;
- pinned commit or release and source checksum;
- code licence and attribution obligations;
- per-dataset licence, terms, geographic coverage and redistribution constraints;
- expected object size, transfer cost, storage cost and compute cost;
- required variables, vertical levels, grid, reference, accumulation and units;
- evaluation dates, lead times, initialization/valid-time convention and climatology;
- compatibility mapping to ClimateOS contracts;
- data leakage, reference asymmetry and operational-vs-reanalysis comparability risks;
- reproducibility and audit outputs;
- an explicit no-run/no-download/no-cost gate until Founder authorization when material resources are involved.

The standing collaboration rule applies: free/open/inspectable/controllable sources first; real data is encouraged when authorized and licensed; any paid commitment requires a clear cost/benefit explanation and explicit Founder approval.

## 8. Recommended next controlled batch

### Task1641–1650 candidate

**Bondo Evidence Passport Validation, Change Detection and WeatherBench Reference Intake**

Proposed bounded scope:

1. validate the Task1631–1640 passport and claim graph;
2. define version/change detection for referenced Bondo public documents;
3. create a WeatherBench/WeatherBench-X External Evaluation Resource Record;
4. create a metric-and-data compatibility matrix against existing ClimateOS statistical and physical contracts;
5. create a zero-run, zero-download cost and licence manifest;
6. prepare a tiny synthetic adapter test plan only;
7. return a Founder decision gate for any later code installation, data access or evaluation run.

This is a proposal only. It does not start Task1641.

## 9. Next-thread mandatory preflight

The next thread must first:

1. read this ACTP;
2. fetch and verify main HEAD;
3. verify PR #67 state, head and exact changed files;
4. verify PR #48 remains closed/unmerged and do nothing to it;
5. inspect the Task1640 closure brief;
6. present the Founder with separate decisions for:
   - PR #67 merge or continued review;
   - Task1641–1650 authorization;
   - WeatherBench reference-only intake versus later bounded execution.

## 10. Hard stops

Unless separately and explicitly authorized, do not:

- merge PR #67 or any other PR;
- reopen or merge PR #48;
- restart Task1200–1299;
- start Task1641+;
- clone, install or run WeatherBench 2 or WeatherBench-X;
- download large WeatherBench, ERA5, IFS or model forecast datasets;
- launch GCP/Dataflow or incur storage, transfer, subscription or compute cost;
- submit a model to the WeatherBench website;
- integrate or run an external model;
- form a real model ranking, admission conclusion, operational forecast, public-safety conclusion, scientific approval, legal conclusion or investment conclusion;
- send Bondo inquiries or contact reviewers.

## 11. Founder review prompts

The next thread should ask only after completing the mandatory preflight:

1. Approve or decline the controlled merge of PR #67.
2. Approve, revise or decline Task1641–1650.
3. Choose the WeatherBench lane:
   - reference and compatibility intake only;
   - bounded tiny synthetic adapter prototype;
   - later controlled real evaluation after a separate cost/data preflight.

Until those decisions are recorded, the correct state is `WAIT_FOR_FOUNDER_DECISION`.
