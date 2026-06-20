# NASA Integration System Map

## Purpose

This map shows how NASA Earthdata may fit into ClimateOS.

## Visual Architecture

```text
NASA Earthdata
-> ClimateOS External Data Layer
-> Observation Layer
-> Relationship Layer
-> Radar Layer
-> Evidence Layer
-> EcoEngine
-> Validation Layer
-> Governance Runtime
```

## Major Components

```text
NASA Earthdata Integration
├─ Data Source Catalog
├─ Observation Resource Model
├─ ClimateOS NASA Input Model
├─ EcoEngine Fuel Model
├─ Relationship Layer Mapping
├─ Radar Layer Mapping
├─ Evidence Layer Mapping
├─ Data Governance
└─ Future Adapter Roadmap
```

## Boundary

This is an architecture map only. No connector, API, database, download process,
or ingestion runtime is implemented.
