# Task1524–1526 — UniCM Data-File and Preprocessing Manifest

Date: 2026-07-14

Status: STATIC CODE MANIFEST / NO DATA ACQUISITION

## Directory contract

The code expects a caller-provided `data_root` with:

```text
data_root/
├── CMIP6/
├── ERA5/
├── ORAS5/
├── SODA224/
└── GODAS/
```

The repository does not contain these datasets.

## Code-expected files

### CMIP6 training

| Expected path/name | Variable | Time encoded in filename | Source/model assumption |
|---|---|---|---|
| `CMIP6/tos_Omon_{MODEL}_historical_r1i1p1f1_{GRID}_185001_201412.nc` | `tos` | 1850-01 to 2014-12 | default `CESM2-FV2*gr` |
| `CMIP6/tauu_Amon_CESM2-FV2_historical_r1i1p1f1_gn_185001_201412.nc` | `tauu` | same | CESM2-FV2 |
| `CMIP6/tauv_Amon_CESM2-FV2_historical_r1i1p1f1_gn_185001_201412.nc` | `tauv` | same | CESM2-FV2 |
| `CMIP6/t20d_Emon_EC-Earth3-Veg-LR_historical_r1i1p1f1_gn_185001_201412.nc` | `t20d` | same | EC-Earth3-Veg-LR |
| `CMIP6/thetaot300_Emon_EC-Earth3-CC_historical_r1i1p1f1_gn_185001_201412.nc` | `thetaot300` | same | EC-Earth3-CC |

The training tensor therefore combines variables from different CMIP6 models. This is a material scientific and preprocessing assumption that must be matched exactly before reproduction.

### ERA5 evaluation/support

| Expected path/name | Variables | Code period |
|---|---|---|
| `ERA5/ERA5.nc` | `sst`, `u10`, `v10` | testing selects 1980-01 to 2014-12 |
| root-level `ERA5.nc` in an alternate training loader | same | selects 1958-01 to 1979-12 |

The Nature data link points to ERA5 single-level monthly means, but the code-specific combined `ERA5.nc` is a derived local artefact, not a provider-native filename.

### ORAS5

| Expected path/name | Variables | Encoded period |
|---|---|---|
| `ORAS5/ORAS5_1958_2014.nc` | `sosstsst`, `sozotaux`, `sometauy`, `sohtc300`, optionally `so20chgt` | 1958–2014 |

The code divides this file into pre-1980 training/validation support and 1980+ test support.

### SODA 2.2.4

| Expected path/name | Variables/levels | Code period |
|---|---|---|
| `SODA224/soda_224_1876_2011.nc` | `temp`; surface uses first level, heat-content proxy averages levels | 1876–2011 file; testing slices from 1980 |

### GODAS

| Expected path/name | Variables/levels | Code period |
|---|---|---|
| `GODAS/pottemp_1980_2021.nc` | `pottmp`; surface first level, heat-content proxy first 26 levels | 1980–2021 |

## Preprocessing operations found

- xarray/NetCDF4 loading;
- spatial cropping;
- grid coarsening;
- interpolation for GODAS;
- fill/invalid-value replacement;
- monthly climatology removal;
- standard-deviation normalization;
- concatenation of multiple physical fields;
- rolling 12-month history plus 24-month target sequences;
- fixed geographic boxes for climate-mode indices.

## Missing reproducibility assets

The repository does not provide a complete raw-to-derived pipeline that proves how to build:

- `ERA5.nc`;
- `ORAS5_1958_2014.nc`;
- `soda_224_1876_2011.nc`;
- `pottemp_1980_2021.nc`;
- the mixed-model CMIP6 training set.

Provider-native variable names, units, coordinate orientation, calendars, masks, regridding methods, compression, chunking and checksums remain to be recorded.

## Required future acquisition manifest

Before any data request, every file must have:

- authoritative provider URL and product version;
- source variable and unit;
- exact spatial/temporal subset;
- native-grid size estimate;
- transformation recipe;
- derived filename and expected dimensions;
- source and derived checksums;
- terms, citation and retention rules;
- raw, temporary and final storage budget;
- deletion/rollback plan.

## Decision

The code-level file contract is now documented.

The data package is not reproducible from provider links alone. Large-data acquisition and preprocessing remain unauthorized and blocked.
