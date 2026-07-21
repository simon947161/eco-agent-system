# Task2024 — Public Spatial Data Source Registry

Status: `METADATA_ONLY_NO_DATA_RETRIEVED`

The machine-readable register is
`cczps_lite/qgis_local_spatial_foundation/source_registry.json`. Every candidate
records publisher, product, URL, licence, spatial resolution, currency, CRS,
coverage, update frequency, retrieval date, limitations, retention and
redistribution status. A null retrieval date is intentional.

## Proposed first sources

| ID | Candidate | Proposed use | Licence position | Gate status |
|---|---|---|---|---|
| QGIS-SRC-001 | NSW Spatial Services FSDF Administrative Boundaries | bounded context boundary | CC BY 4.0 site/service position; item-level confirmation required | not retrieved |
| QGIS-SRC-002 | NSW Spatial Services Place Names and Transport | settlement and roads | CC BY 4.0 site/service position; item-level confirmation required | not retrieved |
| QGIS-SRC-003 | Geoscience Australia SRTM-derived 1 Second DEM v1.0 | bounded terrain input | CC BY 4.0 International | not retrieved |
| QGIS-SRC-004 | NSW Spatial Services FSDF Water | rivers and streams | CC BY 4.0 site/service position; item-level confirmation required | not retrieved |
| QGIS-SRC-005 | Bureau of Meteorology Geofabric | catchment context | product-version licence must be confirmed | not retrieved |
| QGIS-SRC-006 | Bureau Weather Station Directory | station locations/metadata | no open-data assumption; terms confirmation required | not retrieved |
| QGIS-SRC-007 | DEA Land Cover v2.0.0 | later vegetation/land-cover context | CC BY 4.0 International | later only; not retrieved |

Official metadata reviewed:

- NSW Spatial Services products, spatial data, web services and copyright pages;
- Geoscience Australia/DEA SRTM 1-second DEM metadata;
- Bureau Geofabric landing page and documentation;
- Bureau Weather Station Directory metadata guidance;
- DEA Land Cover Version 2.0.0 metadata.

## Source admission rules

Before any retrieval, the Founder must approve a named product, exact bounded
extent and expected size. The operator must then recheck the item-level licence,
version, CRS, vertical datum where applicable, attribution, retention and
redistribution terms. A general website licence must not be substituted for a
dataset licence.

Hillshade and slope are derived products, not independent sources. They remain
`NOT_CREATED` until an approved DEM has a recorded source digest, resolution,
vertical datum, CRS and bounded extent.

## Exclusions

No account, paid service, cloud GIS, ArcGIS Online project, bulk Australia-wide
download, Council non-public layer, private point, fire-history layer or public
infrastructure layer is admitted by this register.
