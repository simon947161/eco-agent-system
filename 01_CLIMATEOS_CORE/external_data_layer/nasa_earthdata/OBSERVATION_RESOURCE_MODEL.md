# Observation Resource Model

## Purpose

The Observation Resource Model defines common fields for describing external
observation resources.

## Common Fields

| Field | Purpose |
| --- | --- |
| Source Name | Human-readable name of the observation resource |
| Provider | Organization or system providing the resource |
| Dataset Category | Category such as rainfall, vegetation, or elevation |
| Spatial Resolution | Spatial detail or grid size, when known |
| Temporal Resolution | Update interval or observation frequency, when known |
| Time Coverage | Historical or current coverage period |
| Data Format | Format such as raster, table, image, or API response |
| Access Method | How the data may be accessed in future work |
| Use Case | ClimateOS use case or interpretation purpose |
| Limitations | Known constraints, uncertainty, or unsuitable uses |
| ClimateOS Layer Mapping | Where the resource may enter ClimateOS |

## Boundary

This is a documentation model only. No schema, parser, or data loader is
implemented.
