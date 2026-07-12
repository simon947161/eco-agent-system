# Task1240–1269 Limited Physical Consistency Assurance Foundation

Status: Founder-authorized bounded contract implementation on an isolated execution branch

## Purpose

Define what evidence and metadata would be required before ClimateOS could calculate or interpret physical-consistency diagnostics for a weather model.

## Implemented scope

- model-neutral catalog for nine conservation, spectral, dynamical and thermodynamic metrics;
- per-metric variables, pressure-level requirements and reference dependencies;
- prediction/reference dataset declaration gate;
- canonical units for surface pressure, temperature, winds, humidity and geopotential;
- grid, regridding, time, lead, missing-data and surface-pressure-method declarations;
- tolerance governance with global `not_established` default;
- cited Effective Resolution research defaults of 0.5 retention and five consecutive wavenumbers, explicitly not an admission threshold;
- reference-sensitivity status and review requirements;
- Physical Consistency Evidence Passport contract;
- complete prediction/reference metadata fixtures and one intentionally blocked fixture;
- structural and boundary tests.

## Non-execution boundary

No physical metric is calculated. There is no spherical harmonic transform, vertical integration, balance residual, Wasserstein calculation, real atmospheric value or external dependency. A complete declaration means only `declaration_complete_no_execution`.

## Scientific limitations

- universal tolerances are not established;
- reference choice can shift absolute metric values;
- physical consistency does not replace statistical skill or expert meteorological review;
- global diagnostics do not establish Australian regional or extreme-event suitability;
- PhysMetrics.Weather remains a recent preprint/reference, not a ClimateOS dependency.

## Prohibited

No PhysMetrics clone/integration, external data access, model execution, real evaluation, invented tolerance, score, rank, pass/fail, admission, PR merge or Task1270+ work.
