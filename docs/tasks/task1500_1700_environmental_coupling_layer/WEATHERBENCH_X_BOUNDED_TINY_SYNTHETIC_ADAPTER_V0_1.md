# WeatherBench-X Bounded Tiny Synthetic Adapter v0.1

Date: 2026-07-16

Status: FOUNDER_AUTHORIZED_BOUNDED_PROTOTYPE / SYNTHETIC_ONLY / ZERO_COST

Base main HEAD: `b2f8ada01e0306937805571d496e2ba2962414f0`

Branch: `agent/weatherbench-tiny-synthetic-adapter-v0-1`

## 1. Authorization boundary

The Founder authorized lane B: a bounded WeatherBench / WeatherBench-X tiny
synthetic adapter using only repository-authored micro data and a fixed
interface, with no real-data download, no complete WeatherBench execution, no
cloud service and no cost.

This authorization is independent of the full Task1641–1650 candidate batch.
It does not mark Task1641–1650 started or complete.

## 2. Implemented interface

The prototype accepts one strict JSON object containing:

- exact contract, synthetic classification and repository-inline origin;
- one supported variable/unit pair: `2m_temperature` / `K`;
- UTC initialization and valid times plus integer lead hours;
- latitude and longitude arrays;
- row-major forecast and synthetic-reference values;
- an exact request for latitude-weighted RMSE, MAE and bias.

Unknown fields are rejected. A URL field, remote origin, real-data label,
unsupported unit, inconsistent time, non-finite value or grid mismatch fails
closed.

The loader additionally confines accepted fixtures to `cczps_lite/input`.

## 3. Synthetic fixture

The committed six-point case uses:

- latitudes `[-60, 0, 60]`;
- longitudes `[140, 141]`;
- a six-hour synthetic temperature forecast;
- six hand-authored forecast/reference values;
- cosine-latitude weighting.

Expected bounded results:

| Metric | Result |
|---|---:|
| Latitude-weighted RMSE | `sqrt(2)` / approximately `1.4142135624 K` |
| Latitude-weighted MAE | `1.25 K` |
| Latitude-weighted bias | `0.5 K` |

These numbers test arithmetic and contract enforcement only. They are not
evidence of model skill or an official WeatherBench score.

## 4. Prototype files and pre-commit SHA-256

| File | SHA-256 |
|---|---|
| `cczps_lite/integration/weatherbench_synthetic_adapter.py` | `0947f30e4e7b4cc869386a4e3069014ad6b8ea4db9a20658eed7d3e374c6cdc3` |
| `cczps_lite/input/weatherbench_tiny_synthetic_case.json` | `7bfcf0cb4198b6747e5cba9ef70f777ee5e700f4a01ab3f47cd99c5b98e405fb` |
| `tests/test_weatherbench_synthetic_adapter.py` | `a99365cd6b388562abadc589b28c8cc8d98afff13abfff8d1dc85215454c9fc8` |

## 5. Verification

- nine targeted adapter tests: PASS;
- full repository suite: 219 tests PASS;
- Python standard library only;
- no WeatherBench dependency or upstream source copied;
- no network call, API, cloud client or data loader in the adapter;
- no real forecast, observation, reanalysis, model or weight;
- no model ranking, admission or Bondo wind conclusion;
- cost: AUD 0.

## 6. Output controls

Every result records:

- `upstream_code_executed: false`;
- `external_data_accessed: false`;
- `network_or_cloud_used: false`;
- `model_admission_state: NOT_EVALUATED`;
- `human_review_required: true`;
- `CLIMATEOS_SYNTHETIC_RESULT_NOT_WEATHERBENCH_SCORE`.

## 7. Exclusions

Not implemented or authorized:

- WeatherBench 2 or WeatherBench-X clone/install/import/execution;
- xarray, Beam, Dataflow or cloud storage;
- real data, large files, remote URLs or local external files;
- interpolation, regridding, climatology, ACC, CRPS or probabilistic evaluation;
- official benchmark reproduction or submission;
- model comparison, ranking, admission or operational forecast use;
- environmental, legal, compliance, safety or investment conclusion.
