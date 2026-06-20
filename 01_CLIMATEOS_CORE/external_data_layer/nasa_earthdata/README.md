# NASA Earthdata Integration Framework V1

## Purpose

This directory defines how ClimateOS may integrate NASA Earth observation
resources as external observation inputs.

NASA is an external observation provider.
ClimateOS uses NASA data as observation inputs.
EcoEngine may consume selected NASA-derived inputs through ClimateOS.

NASA provides observational fuel.
ClimateOS provides runtime structure.
EcoEngine provides scientific computation.

## Strategic Flow

```text
NASA Earthdata
-> ClimateOS Observation Layer
-> ClimateOS Relationship Layer
-> ClimateOS Radar Layer
-> ClimateOS Evidence Layer
-> EcoEngine Computation
-> Validation
-> Governance Runtime
```

## Documents

- [NASA Earthdata Integration Framework](NASA_EARTHDATA_INTEGRATION_FRAMEWORK.md)
- [NASA Data Source Catalog V1](NASA_DATA_SOURCE_CATALOG_V1.md)
- [Observation Resource Model](OBSERVATION_RESOURCE_MODEL.md)
- [ClimateOS NASA Input Model](CLIMATEOS_NASA_INPUT_MODEL.md)
- [EcoEngine Fuel Model](ECOENGINE_FUEL_MODEL.md)
- [NASA to Relationship Layer](NASA_TO_RELATIONSHIP_LAYER.md)
- [NASA to Radar Layer](NASA_TO_RADAR_LAYER.md)
- [NASA to Evidence Layer](NASA_TO_EVIDENCE_LAYER.md)
- [NASA Data Governance](NASA_DATA_GOVERNANCE.md)
- [Multi Source Observation Alignment](MULTI_SOURCE_OBSERVATION_ALIGNMENT.md)
- [Future Adapter Roadmap](FUTURE_ADAPTER_ROADMAP.md)
- [NASA Integration System Map](NASA_INTEGRATION_SYSTEM_MAP.md)
- [External Data Provider Interface](EXTERNAL_DATA_PROVIDER_INTERFACE.md)
- [NASA Integration Glossary](NASA_INTEGRATION_GLOSSARY.md)

## Current Status

`Foundation Established`

This is documentation only. No API implementation, authentication
implementation, data download, database, runtime connector, automated ingestion,
forecasting, or model execution is implemented.
