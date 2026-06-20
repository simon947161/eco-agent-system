# Observation Layer Architecture

## Purpose

The Observation Layer defines how raw environmental observations may be
collected, organised, and preserved before they are reviewed as evidence.

## Observation Sources

| Source | Purpose | Notes |
| --- | --- | --- |
| Satellite | Future remote-sensing context for land, vegetation, water, and heat signals | No satellite integration is implemented |
| Weather | Temperature, rainfall, wind, humidity, and related meteorological context | No weather API is implemented |
| Hydrology | Rivers, soil moisture context, water stress, and flood observations | Documentation only |
| Ecology | Vegetation, species, habitat, stress, recovery, flowering, and seasonal change | Human observation remains central |
| Community Observation | Local notes, photos, lived experience, and place-based signals | Requires transparency and review |

## Observation Flow

```text
Observation
  |
  v
Record
  |
  v
Evidence Candidate
  |
  v
Evidence
```

## Interpretation

An observation is a recorded signal. A record preserves the signal with time,
place, source, and context. An evidence candidate is a record that may support
future analysis. Evidence is a reviewed record with provenance, limitations,
and human interpretation.

## Boundaries

This architecture does not perform validation, forecasting, governance,
calculation, or automated decision-making.
