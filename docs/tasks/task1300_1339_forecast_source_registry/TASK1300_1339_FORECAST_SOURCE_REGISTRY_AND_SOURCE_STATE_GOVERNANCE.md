# ClimateOS Task1300-1339 Forecast Source Registry And Source-State Governance

Date: 2026-07-12

Status: IMPLEMENTED_FOR_FOUNDER_REVIEW

Baseline: 3492028c11db06076de7a6fc86eb59930cd2a7db

## Purpose

Establish a provider-neutral registry for physical models, AI models, observations, ensembles and downscaling products before ClimateOS connects to any forecast source.

## Source States

- VERIFIED_CANDIDATE
- CONNECTED_FOR_RESEARCH
- CONNECTED_WITH_LIMITATIONS
- DEFERRED_UNVERIFIED
- DEFERRED_ACCESS_OR_LICENCE
- CUSTOMER_REQUESTED_EXPERIMENT
- NOT_SUITABLE_FOR_DECLARED_USE
- RETIRED_OR_UNAVAILABLE

A state is scoped to its source version, use, evidence date, licence and access path. It is not a universal endorsement or rejection.

## Governance

The registry reports missing fields and blockers. It cannot connect, call, download, run, approve or rank a source. Customer-requested experiments require separate approval, explicit opt-in, limitations, bounded trial, audit, stop conditions and exit path. Customer acceptance does not remove ClimateOS legal, safety, licence or platform responsibility.

Paid APIs, commercial models and software remain legitimate future options through a Paid Decision Brief and Founder approval. No chargeable commitment is created here.

## Controlled Candidate Records

- AICON: DEFERRED_UNVERIFIED.
- ECMWF IFS Open Data: VERIFIED_CANDIDATE.
- ECMWF AIFS Open Data: VERIFIED_CANDIDATE.
- BoM ACCESS: DEFERRED_ACCESS_OR_LICENCE.
- WeatherNext / GraphCast / GenCast: DEFERRED_ACCESS_OR_LICENCE for commercial use.

These are registry decisions only, not live connections or scientific admission decisions.

## Boundary

No external model, data, API, download, paid service, public forecast, public-safety conclusion, private EcoEngine asset, Task1340 work or PR merge.
