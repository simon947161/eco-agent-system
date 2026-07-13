# Task1543–1544 — UniCM Observation Frame

Date: 2026-07-14

Status: FRAME_READY / RESEARCH_ONLY / TRANSLATION_REQUIRED

## Identity

| Field | Record |
|---|---|
| Model | UniCM — Global Climate Modes |
| Publication | Learning the coupled dynamics of global climate modes |
| Official repository | tsinghua-fib-lab/UniCM-Global-Climate-Modes |
| Release | v1.0 |
| Commit | 67fe4c183df351d5039c5b3b80ae86a68b627398 |
| Commit tree | 501b96a31096b8d5f66bff93c32c6135c5d44537 |
| Code licence | MIT |
| Official weights | not identified |
| ClimateOS execution | none |

## Observation position

UniCM observes the climate system primarily from a global and ocean-basin climate-mode position.

It represents large-scale coupled ocean–atmosphere variability using gridded physical fields and derived climate-mode indices.

It does not observe a city, catchment, building, farm, ecological site or infrastructure asset directly.

## Spatial frame

| Dimension | Finding |
|---|---|
| Primary scale | planetary plus basin/mode |
| Physical support | coarsened gridded ocean physical fields |
| Mode support | fixed geographic boxes and derived indices |
| Locality support | absent |
| Site support | absent |
| Australian regional admission | absent |

The code-level default physical grid was previously assessed as 12 by 72 after preprocessing, with 2 by 2 patches. Exact raw-to-grid transformation remains incomplete.

## Temporal frame

| Dimension | Finding |
|---|---|
| Resolution | monthly |
| History window | 12 months by default |
| Prediction window | 24 months by default |
| Training period | code-expected CMIP6 files encode 1850–2014 |
| Evaluation periods | dataset-dependent; several loaders slice around 1980 onward |
| Future-climate stationarity | unproven |

Script defaults and paper-result settings are not assumed equivalent.

## Variable world

Primary physical variables identified:

- sea-surface temperature;
- zonal surface wind stress;
- meridional surface wind stress;
- upper-ocean heat-content or thermal representation to 300 m;
- 20-degree-Celsius isotherm depth/height representation.

Mode and region structures include ENSO/Niño regions, North and South Pacific Meridional Modes, Indian Ocean Basin mode, Indian Ocean Dipole, Southern Indian Ocean Dipole, Tropical North Atlantic and warm-water-volume support.

SAM and MJO were not identified as explicit modes.

## Mechanism class

UniCM is a learned dual-branch spatio-temporal model.

Its computational world includes:

- a gridded physical-field branch;
- a climate-mode branch;
- spatial and temporal attention;
- exchange between field and mode representations;
- joint mode interaction;
- autoregressive or sequential prediction;
- learned lead-lag structure.

Attention and learned association are not causal proof.

## Boundaries and omissions

UniCM does not directly represent:

- local rainfall;
- near-surface local air temperature;
- local topography;
- catchment hydrology;
- soil moisture;
- vegetation or ecological state;
- fire weather;
- building and infrastructure exposure;
- human behaviour and governance;
- a complete Australian driver set.

## Uncertainty

The supplied scripts train multiple random seeds and support ensemble evaluation, but no official checkpoint ensemble was found.

The existence of ensemble code does not establish calibrated probabilistic uncertainty.

## Validation and use boundary

Published performance remains a published claim, not a ClimateOS-reproduced fact.

Current ClimateOS admission:

FRAME_READY / RESEARCH_ONLY / TRANSLATION_REQUIRED / OPERATIONALLY_BLOCKED

A UniCM output cannot move directly from global climate-mode state to Sydney, Alice Springs, Snowy Valleys, Riverina or any other local claim.
