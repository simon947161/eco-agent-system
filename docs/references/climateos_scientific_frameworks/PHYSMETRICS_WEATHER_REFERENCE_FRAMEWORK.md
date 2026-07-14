# PhysMetrics.Weather — Independent Reference Framework

Date: 2026-07-12
Status: Research reference / not an implementation authorization
ClimateOS role: Model Assurance Foundation
Primary roadmap range: Task1200–1299

## Purpose

PhysMetrics.Weather is registered as an independent reference for evaluating the physical consistency of machine-learning weather prediction models beyond point-wise statistical metrics such as RMSE and ACC.

## ClimateOS lessons

- statistical accuracy is necessary but not sufficient;
- nominal grid resolution is not necessarily effective resolution;
- physical drift can accumulate during autoregressive rollout;
- mass, water, energy, spectra, balance and vertical-structure diagnostics should inform model admission;
- physical consistency does not replace forecast skill, extreme-event evaluation or human review.

## Intended use

ClimateOS may adapt its concepts into a Model Evidence Passport and Model Admission Gate. Any code reuse requires separate verification of the official repository, licence, version and dependencies.

## Non-goals

- not a forecast model;
- not proof that a model is physically correct in all respects;
- not a substitute for WeatherBench-style evaluation;
- not automatically combined with AICON or TianJi-Environ.

## Return reminder

At Task1200, re-check the latest PhysMetrics.Weather paper, official code, licence, supported variables, reference datasets and validation limits before preparing an executable implementation brief.

## Keywords

PhysMetrics.Weather; ClimateOS; Task1200; Model Assurance; physical consistency; mass drift; water drift; energy drift; effective resolution; spectra; hydrostatic balance; geostrophic balance; lapse rate; Model Evidence Passport.