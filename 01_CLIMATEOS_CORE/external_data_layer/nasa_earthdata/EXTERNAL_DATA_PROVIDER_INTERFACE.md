# External Data Provider Interface

## Purpose

This document defines a reusable concept for describing future external data
providers.

It can be reused for NASA, Copernicus, BOM, ECMWF, Destination Earth,
Open-Meteo, local sensors, and other providers.

## Interface Fields

| Field | Purpose |
| --- | --- |
| Provider | Organization or system providing the data |
| Dataset | Dataset or resource name |
| Access Method | How the dataset may be accessed |
| Spatial Coverage | Geographic coverage |
| Temporal Coverage | Time period covered |
| Update Frequency | How often the resource changes |
| Data Format | File, API, raster, table, or other format |
| Use Case | Intended ClimateOS use |
| Limitations | Known limits or unsuitable uses |
| Validation Requirements | Review or validation needs before use |

## Boundary

This is a conceptual interface only. No software interface, adapter, or schema
is implemented.
