# ClimateOS Task1340-1379 Common Weather Data Contract

Date: 2026-07-12

Status: IMPLEMENTED_FOR_FOUNDER_REVIEW

Baseline: a782906a3737ece27399f707d9ad9f3c9f77ead2

## Purpose

Define provider-neutral forecast-time, spatial, vertical, field, quality and provenance semantics using synthetic fixtures only.

## Core Rules

- distinguish run time, valid time and lead time;
- require valid time to equal run time plus lead;
- separate deterministic and ensemble members;
- declare coordinates, grid type and grid spacing;
- never equate grid spacing with effective physical resolution;
- declare vertical coordinates, levels and surface definition;
- require variable identifiers, standard names, units and data types;
- preserve missing, stale, invalid, transformed and out-of-domain flags;
- preserve evidence snapshot, fixture or retrieval identity, transformations, checksum and responsible human.

## Boundary

The validator performs structural checks only. It cannot ingest live data, call an API, run a model, compare forecast skill, orchestrate sources or produce a public forecast. Task1380 remains separately gated.
