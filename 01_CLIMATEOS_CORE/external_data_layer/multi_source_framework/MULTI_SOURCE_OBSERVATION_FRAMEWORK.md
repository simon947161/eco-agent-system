# Multi-Source Observation Framework

## Purpose

This document defines the provider-neutral observation architecture for
ClimateOS.

## Concept

ClimateOS should treat external providers as complementary observation sources,
not as replacements for evidence, validation, or governance.

## Provider-Neutral Flow

```text
Provider Observation
-> ClimateOS Observation Record
-> Relationship Context
-> Radar Signal
-> Evidence Candidate
-> Validation Review
```

## Supported Provider Families

- NASA
- Copernicus
- ECMWF
- BOM
- Open-Meteo
- Local sensors
- Community observation
- Future providers

## Boundary

No provider integration, API, ingestion pipeline, data download, or algorithm is
implemented.
