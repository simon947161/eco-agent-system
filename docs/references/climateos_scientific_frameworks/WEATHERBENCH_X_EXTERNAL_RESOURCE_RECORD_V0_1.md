# WeatherBench-X External Evaluation Resource Record v0.1

Date: 2026-07-16

Status: VERIFIED_REFERENCE / NO_SOURCE_ACQUISITION / NO_DATA_ACCESS / NO_UPSTREAM_EXECUTION

ClimateOS role: external evaluation-framework reference, not a model and not an admitted runtime dependency

## 1. Identity and version record

| Field | WeatherBench-X | Legacy WeatherBench 2 |
|---|---|---|
| Official repository | `https://github.com/google-research/weatherbenchX` | `https://github.com/google-research/weatherbench2` |
| Provider/maintainer namespace | `google-research` | `google-research` |
| Recorded release | `v2025.02.1` | `v0.2.0` |
| Remote Git object ID verified 2026-07-16 | `82ba4a46338e6c5a4e0a250bfa6308245ed62048` | `81f1993ee6a1a156611c32dd85deeb3f3059b486` |
| Code licence | Apache-2.0 | Apache-2.0 |
| ClimateOS acquisition | none | none |
| Archive checksum | not applicable; no archive downloaded | not applicable; no archive downloaded |

The official WeatherBench 2 repository identifies WeatherBench-X as the newer
evaluation codebase and retains its data guide as current. The WeatherBench-X
repository describes a modular framework using interoperable loaders,
interpolation, metrics and aggregation around xarray, with optional scalable
execution. These descriptions are reference facts only.

## 2. Admitted reference concepts

- separate forecast and ground-truth inputs;
- explicit variable, unit, grid, initialization time, valid time and lead time;
- metric and aggregation semantics that remain visible;
- modular separation between loading, transformation, metric and aggregation;
- reproducible configuration and provenance;
- statistical skill as one evaluation dimension, not automatic model admission.

No WeatherBench or WeatherBench-X source code has been copied, vendored,
installed, imported or executed. The ClimateOS prototype is an independently
written standard-library boundary test.

## 3. Dataset, licence and cost gate

| Gate | Current state |
|---|---|
| WeatherBench-related dataset selected | NO |
| Dataset licence/terms accepted | NO / NOT ASSESSED |
| ERA5, IFS or model forecasts accessed | NO |
| Object size or transfer estimate needed | NO, because no object is authorized |
| Storage provisioned | NO |
| Cloud/Dataflow/API/account used | NO |
| Compute or transfer cost | AUD 0 |
| Model submitted to public benchmark | NO |

Every real dataset remains blocked until its exact object identity, licence,
geography, variables, levels, grid, time convention, redistribution terms,
size, storage, transfer and compute implications receive a separate gate.

## 4. ClimateOS v0.1 compatibility matrix

| Evaluation concept | Tiny adapter treatment | Compatibility state |
|---|---|---|
| Data class | exact `SYNTHETIC_ONLY` literal | controlled prototype only |
| Source | repository-inline JSON fixture | no external loader |
| Variable/unit | `2m_temperature` / `K` only | fixed narrow mapping |
| Grid | regular latitude/longitude lists and row-major values | synthetic convention only |
| Time | UTC initialization, valid time and integer lead hours | explicit and validated |
| Aggregation | positive cosine-latitude weights over six points | WeatherBench-inspired, not reproduced |
| Metrics | weighted RMSE, MAE and bias | statistical boundary test only |
| Missing values | rejected | no missing-data contract yet |
| Interpolation/regridding | absent | blocked |
| Probabilistic metrics | absent | blocked |
| Climatology/ACC | absent | blocked |
| Spectral/physical consistency | absent | remains separate PhysMetrics-style layer |
| Model admission/ranking | always `NOT_EVALUATED` | prohibited |

## 5. Risk register

- Similar metric names do not establish official WeatherBench equivalence.
- A synthetic arithmetic pass does not establish forecast skill.
- Reanalysis is not pure observational truth.
- Regridding, climatology, accumulation and masking choices can materially alter scores.
- Operational forecasts and retrospective reanalysis may have asymmetric information.
- Statistical skill does not establish physical consistency, regional fitness or decision value.
- Licence compatibility for code does not settle dataset rights or cost.

## 6. Standing boundary

The following description is mandatory for prototype outputs:

`CLIMATEOS_SYNTHETIC_RESULT_NOT_WEATHERBENCH_SCORE`

No later work may remove or weaken that boundary without a new Founder gate.
