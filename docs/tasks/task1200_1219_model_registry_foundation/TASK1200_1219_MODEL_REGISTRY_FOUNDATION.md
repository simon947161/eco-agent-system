# Task1200–1219 Limited Model Registry Foundation

Status: Founder-authorized bounded implementation on an isolated execution branch

## Purpose

Create the first Model Assurance Foundation contracts so ClimateOS can record what a model or diagnostic framework claims to be before evaluating or depending on it.

## Architecture position

```text
Task1199 scientific-input readiness
→ Task1200–1219 model metadata registration
→ future Task1220+ statistical and physical evaluation gates
```

Registration is deliberately separated from evaluation and admission.

## Implemented scope

- Model Registry Contract v0.1;
- Model Evidence Passport Contract v0.1;
- identity, maintainer, version, canonical source and source revision fields;
- licence name and review state;
- research, experimental, claimed operational-service and unknown status distinctions;
- input/output interface declarations;
- spatial and temporal resolution declarations;
- training/evaluation data declarations;
- known limitations, uncertainty, evidence references and human metadata review;
- licence/provenance blocking conditions;
- dispute, counter-evidence, revision and audit foundations;
- one complete and one intentionally blocked synthetic fixture;
- deterministic structural and boundary tests.

## Model Evidence Passport boundary

The passport is an evidence container. It does not establish forecast skill, physical consistency, operational suitability, scientific validity or model admission. Statistical evaluation, physical-consistency evaluation, extreme-event fitness, regional suitability and admission decisions remain reserved and unimplemented.

## Scientific preflight context

PhysMetrics.Weather and WeatherBench 2 were reviewed only as current official reference points. Their code, data and dependencies were not downloaded, cloned, imported or executed. PhysMetrics.Weather remains a recent preprint and repository-level reference; no model or framework is registered as approved by this batch.

## Limitations

- no runtime registry API or database table;
- no external model, code, weights or dataset;
- no evaluation calculation;
- no score, rank, recommendation or admission decision;
- no Task1220+ work;
- no PR merge.

## Verification target

The complete existing local prototype test suite plus the new Task1200–1219 contract tests must pass. JavaScript syntax and diff checks remain required even though this batch does not modify browser runtime code.
