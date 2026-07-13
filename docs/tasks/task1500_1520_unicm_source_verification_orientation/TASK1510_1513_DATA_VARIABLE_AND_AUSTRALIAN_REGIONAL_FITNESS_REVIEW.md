# Task1510–1513 — Data, Variable and Australian Regional-Fitness Review

Date: 2026-07-14

Status: ORIENTATION_COMPLETE / REGIONAL_TRANSLATION_REQUIRED

## 1. Dataset registry

The Nature paper identifies all study datasets as publicly available and names the following authoritative sources.

| Dataset | Role visible in paper/code | Authoritative source | Current admission |
|---|---|---|---|
| CMIP6 | model training data | https://cds.climate.copernicus.eu/datasets/projections-cmip6 | METADATA VERIFIED / TERMS AND SUBSET REQUIRED |
| ORAS5 | ocean reanalysis, validation and auxiliary fields | https://cds.climate.copernicus.eu/datasets/reanalysis-oras5 | METADATA VERIFIED / TERMS AND SUBSET REQUIRED |
| ERA5 | reanalysis evaluation | https://cds.climate.copernicus.eu/datasets/reanalysis-era5-single-levels-monthly-means | METADATA VERIFIED / EXACT PRODUCT MAPPING REQUIRED |
| GODAS | ocean data/reanalysis evaluation | https://psl.noaa.gov/data/gridded/data.godas.html | METADATA VERIFIED / FILE AND TERMS REVIEW REQUIRED |
| SODA | ocean reanalysis evaluation | https://soda.umd.edu/ | METADATA VERIFIED / VERSION AND TERMS REQUIRED |

No data were downloaded.

## 2. Code-expected data structure

The README expects local directories:

`CMIP6/`, `ERA5/`, `ORAS5/`, `SODA224/`, and `GODAS/`.

The loader expects preprocessed NetCDF files with specific names and variables. Public availability does not guarantee that upstream files already match those names, grids, masks, temporal slices or preprocessing assumptions.

Task1521 must produce a file-level manifest before acquisition:

- provider and product;
- exact dataset version;
- variable and unit;
- temporal and spatial subset;
- native and transformed grid;
- expected file size;
- licence/terms;
- checksum;
- preprocessing script and output checksum;
- retention and deletion rule.

## 3. Variable suitability

UniCM's five principal ocean fields are scientifically relevant to coupled ocean–atmosphere modes, but they are not direct local-impact variables.

They do not by themselves supply:

- Australian rainfall;
- near-surface air temperature;
- soil moisture;
- streamflow or reservoir state;
- vegetation condition;
- fire weather;
- biodiversity response;
- building or infrastructure exposure.

A regional evidence chain therefore needs separately governed observations, reanalysis/downscaling and domain models.

## 4. Australian regional relevance

The Australian Bureau of Meteorology treats El Niño/La Niña, the Indian Ocean Dipole, the Madden–Julian Oscillation and the Southern Annular Mode as distinct influences on Australian climate:

https://www.bom.gov.au/climate/about/

UniCM has direct conceptual relevance through ENSO and IOD-related coupled modes. However, the inspected code does not establish a complete Australian driver set, because SAM and MJO were not identified.

### South-eastern Australia / Snowy Valleys position

Current classification:

`PROMISING_GLOBAL_DRIVER_REFERENCE / NOT_REGIONALLY_ADMITTED`

Reasons:

- global climate modes can influence Australian seasonal climate;
- UniCM's spatial and monthly outputs are not a local forecast product;
- local topography, frontal systems, cut-off lows, east-coast lows, land-surface state and catchment processes are not represented by the climate-mode indices alone;
- Snowy Valleys and Riverina impacts require regional observations and an explicit translation model;
- non-stationarity under climate change can alter historical teleconnections;
- UniCM skill on its reported benchmarks does not establish skill for NSW rainfall, heat, fire or ecological consequences.

## 5. Proposed future regional validation chain

No implementation is authorized, but a future evidence design should separate:

1. UniCM global climate-mode state;
2. BoM or other authoritative Australian climate-driver state;
3. regional rainfall and temperature observations/reanalysis;
4. soil-moisture, water, vegetation or fire-domain evidence;
5. statistical or physical translation method;
6. uncertainty propagation;
7. Australian climate-scientist review;
8. bounded planning interpretation.

## 6. Regional stop rules

Do not proceed to regional claims if:

- SAM/MJO and other relevant drivers are silently omitted;
- local validation data are unavailable;
- the global-to-regional translation is not independently evaluated;
- correlation is described as causation;
- model attention is treated as mechanism proof;
- the output is used as an operational warning;
- expert review is absent for consequential interpretation.

## 7. Task1513 decision

UniCM is suitable for continued **scientific orientation** and potential future research acquisition.

It is not admitted as a Task1500-ready regional input and is not authorized for Snowy Valleys, Riverina or NSW decision support.
