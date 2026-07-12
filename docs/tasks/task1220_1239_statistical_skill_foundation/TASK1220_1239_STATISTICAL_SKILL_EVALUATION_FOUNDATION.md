# Task1220–1239 Limited Statistical Skill Evaluation Foundation

Status: Founder-authorized bounded implementation on an isolated execution branch

## Purpose

Establish reproducible statistical calculation contracts before ClimateOS evaluates any real model or dataset.

## Implemented scope

- Statistical Evaluation Contract v0.1;
- latitude-weighted MSE, RMSE, MAE, bias and ACC;
- RMSE calculated as the square root of aggregated MSE;
- explicit climatology dependency for ACC;
- synthetic candidate, persistence and climatology cases;
- declared variable, units, region, forecast lead, periods and human responsibility;
- non-overlapping training/evaluation period requirement;
- unit, dimension, empty-input, finite-value, latitude, leakage and ACC-variance blockers;
- canonical input SHA-256 and formula version for reproducibility;
- deterministic fixtures and automated tests.

## Interpretation boundary

Each result is evidence that a declared calculation ran on one synthetic slice. Results are kept separate. The implementation does not combine metrics into an overall score, compare cases, rank models, claim one model is better, assess regional fitness or create a Model Admission decision.

## External resource boundary

No WeatherBench 2, ERA5, IFS, GraphCast, Pangu or other external dataset/model is read, downloaded, streamed, cloned, imported or executed. Official WeatherBench 2 documentation informed metric conventions during preflight only.

## Limitations

- tiny one-dimensional synthetic samples only;
- no gridded xarray/Zarr or Beam pipeline;
- no probabilistic CRPS or ensemble evaluation;
- no extreme-event evaluation;
- no physical-consistency evaluation;
- no operational or Australian regional suitability conclusion;
- no Task1240+ work and no PR merge.
