# Google Earth Visual Reference Protocol v0.1

## Decision

Google Earth may be used as a **human visual-reference and communication
layer**, subordinate to QGIS, official datasets and admitted evidence objects.
It is not an authoritative scientific dataset or automated inference source.

## Authorised uses

- human inspection of terrain, settlement and landscape context;
- viewing historical imagery where available;
- noting apparent visual features or change candidates for later verification;
- stakeholder orientation and attributed communication;
- creating local KML annotations;
- comparison with the accepted QGIS project and official layers.

## Prohibited or separately gated uses

- bulk or automated imagery download;
- extraction of Google content into a substitute mapping dataset;
- silent redistribution or removal of attribution;
- measurements treated as engineering or survey evidence;
- imagery date assumed from the viewing date;
- automated feature classification used as a ClimateOS conclusion;
- treating visual absence as proof that a feature or event does not exist;
- using Google Earth instead of a licensed official GIS layer where authority
  matters.

## `VISUAL_REFERENCE_OBSERVATION`

Required fields:

```yaml
observation_id:
viewer:
viewed_at:
product: Google Earth
location:
view_extent:
imagery_date_displayed:
imagery_date_precision:
view_mode: 2D | 3D | historical | street_view
visual_observation:
interpretation_candidate:
verification_required: true
comparison_qgis_layer_ids: []
source_attribution_visible:
screenshot_or_export_reference:
licence_note:
permitted_use:
prohibited_use:
human_review_status:
```

## Evidence treatment

- default conclusion level: `L0 visual-reference presence/candidate`;
- default evidence maturity: no higher than `S1 SIGNAL_DETECTED`;
- promotion requires an independent admitted source or field/official
  verification;
- imagery age, resolution, cloud, season, 3D reconstruction and viewpoint are
  recorded limitations;
- a visual observation can open an investigation but cannot close a scientific
  claim.

## QGIS relationship

| Google Earth | QGIS |
|---|---|
| rapid human context and communication | governed analysis and evidence alignment |
| imagery and 3D visual reference | declared CRS, provenance and licensed layers |
| candidate observation | reproducible spatial evidence object |
| local KML annotation | versioned project and layer metadata |

Google Earth-derived annotations may be imported only as clearly labelled
reference objects. They must not be fused silently with authoritative layers.

## Current official terms basis

The current Google Earth end-user terms permit viewing and annotating maps,
creating KML files/layers and public display with proper attribution. They
prohibit redistribution, mass download and creating a substitute mapping
dataset, and warn that actual conditions may differ from displayed content.

Official references:

- https://www.google.com/help/terms_maps-earth/
- https://www.google.com/help/terms_maps/
- https://earth.google.com/studio/docs/attribution/

Terms and product availability can change. Recheck them before a new export,
public communication workflow or automated integration.

