# Task3500 — Copernicus CDS Future Science Data Infrastructure Roadmap and CRP

Date: 2026-07-13
Status: FUTURE_SCIENCE_INFRASTRUCTURE / NOT_EXECUTABLE
Project: ClimateOS / Eco-Agent-System
Founder return gate: **Task3500**
Primary reference: Copernicus Climate Data Store (CDS)

## 1. Founder intention

The Founder has decided that Copernicus Climate Data Store should be preserved as a future ClimateOS scientific-infrastructure resource, but should not interrupt the current ClimateOS delivery line.

Task3500 is therefore reserved as the formal return point for exploring a governed ClimateOS Future Science Data Infrastructure Library, with Copernicus CDS, ERA5 and ERA5-Land as the first registered resource family.

This is a preservation and research-planning record only. It is not authorization to download large datasets, build a production adapter, create credentials, incur cloud costs, or alter current ClimateOS tasks.

## 2. Why Task3500

Task3000 is reserved for Weather Jiu-Jitsu and Earth-System Sensitivity research: where the system may be dynamically sensitive and how small perturbations might alter trajectories in simulation.

Task3500 addresses a different need: the scientific evidence and data infrastructure required to support future sensitivity, constraint, counterfactual and coupled Earth-system research.

The long-range relationship is:

```text
Task3000
Earth-System Sensitivity Exploration
        ↓
Task3200 candidate
Dynamic Constraint Intelligence
        ↓
Task3400 candidate
Counterfactual Earth-System Research
        ↓
Task3500
Future Science Data Infrastructure Library
```

Task3500 is not a theory task. It is a future data-governance and research-infrastructure task.

## 3. Initial registered resource: Copernicus Climate Data Store

Copernicus CDS should be treated as an authoritative climate-data access platform and research source registry candidate.

Initial resource families to investigate at Task3500 include:

- ERA5 atmospheric reanalysis;
- ERA5-Land land-surface reanalysis;
- seasonal forecast products;
- CMIP climate projections and scenarios where available;
- climate indicators and derived products;
- metadata, provenance, licence and update records;
- API access and controlled-download workflows.

The future system must clearly distinguish:

- observations;
- reanalysis;
- model forecast;
- climate projection;
- derived indicator;
- downscaled product;
- ClimateOS transformation or inference.

## 4. Proposed Task3500–3699 roadmap

### Task3500–3539 — Source and governance verification

- verify the current official CDS platform and responsible institutions;
- review licences, terms, attribution and redistribution conditions;
- identify authentication and API requirements;
- inventory ERA5, ERA5-Land, seasonal and projection datasets relevant to ClimateOS;
- record temporal coverage, spatial resolution, variables, latency and update frequency;
- define what may and may not be stored or republished.

**Deliverable:** Copernicus CDS Source and Governance Dossier.

### Task3540–3579 — Scientific Resource Registry

Create a future ClimateOS scientific resource record supporting:

```yaml
resource_id:
provider:
product_family:
product_name:
resource_type:
  - observation
  - reanalysis
  - forecast
  - projection
  - derived_indicator
spatial_resolution:
temporal_resolution:
coverage_start:
coverage_end:
update_frequency:
variables:
licence:
attribution:
api_method:
access_constraints:
known_limitations:
provenance_status:
review_status:
```

**Deliverable:** ClimateOS Scientific Resource Registry v0.1.

### Task3580–3619 — Controlled retrieval and storage contract

- define region-first, variable-first and period-first request boundaries;
- prohibit uncontrolled global multi-decadal bulk download by default;
- define file naming, checksums, manifests and reproducible requests;
- separate raw, curated, transformed and model-ready data;
- establish storage budgets, retention rules and deletion approvals;
- record every transformation in an Evidence Passport.

**Deliverable:** Controlled Climate Data Retrieval Contract v0.1.

### Task3620–3659 — Minimal Australian data pilot

Candidate region:

- Snowy Valleys;
- Riverina;
- south-eastern NSW;
- another bounded Founder-approved study region.

Candidate variables:

- temperature;
- precipitation;
- wind;
- radiation;
- soil moisture;
- evaporation or related land-surface quantities.

The pilot must remain small, reproducible and scientifically reviewed.

**Deliverable:** bounded ERA5 / ERA5-Land Australian evidence package.

### Task3660–3699 — Future Science Data Infrastructure gate review

Assess whether ClimateOS should proceed toward:

- a read-only CDS adapter;
- a reusable request-template library;
- scientific data lineage services;
- integration with Environmental Coupling, Dynamic Constraint and Counterfactual research;
- long-term local or cloud storage.

The gate outcome must be one of:

- GO;
- HOLD;
- STOP.

## 5. Relationship to other future-science tasks

### Task3000

Sensitivity and Weather Jiu-Jitsu research may require historical atmospheric states, but Task3000 must not automatically trigger CDS ingestion.

### Task3200 candidate

Dynamic emergent constraints may use observational or reanalysis histories to reduce prediction uncertainty. Task3500 can later provide governed data lineage, but must not fabricate constraint validity.

### Task3400 candidate

Counterfactual Earth-system experiments may require reproducible initial and boundary states. Task3500 can provide source records and bounded datasets.

### Task1500–1700

Environmental Coupling work may eventually consume ERA5-derived evidence, but Task3500 remains a later infrastructure layer and does not reopen earlier tasks.

## 6. Scientific cautions

- ERA5 and ERA5-Land are reanalysis products, not direct observations.
- Grid resolution is not equivalent to local truth or effective process resolution.
- Dataset consistency does not remove model and assimilation bias.
- Downscaling cannot create evidence that was never observed.
- Historical relationships may not remain stationary under future climate change.
- Data accessibility does not equal permission for unrestricted redistribution.

## 7. Execution boundary

Task3500 is currently **NOT_EXECUTABLE**.

Before execution, a future agent must:

1. confirm the project is approaching Task3500;
2. re-read this roadmap and the Task3000 future-science files;
3. verify current CDS products, APIs, licences and institutional arrangements;
4. inspect current ClimateOS architecture, storage and budget;
5. propose a bounded preflight;
6. obtain explicit Founder authorization.

No present action is authorized for:

- account creation;
- API-key creation;
- bulk download;
- cloud deployment;
- storage purchase;
- dataset redistribution;
- production integration;
- operational forecasts;
- scientific claims based on unreviewed data.

## 8. Permanent reminder

> **Task3500 is the formal ClimateOS return point for the Future Science Data Infrastructure Library, with Copernicus CDS / ERA5 / ERA5-Land as the first registered resource family.**

Future retrieval keywords:

`Task3500`, `Copernicus CDS`, `ERA5`, `ERA5-Land`, `Future Science Data Infrastructure`, `Scientific Resource Registry`, `ClimateOS Data Provenance`.

## 9. CRP Harvest Block

### Core knowledge points

- Copernicus CDS is a major authoritative access platform for climate reanalysis, forecast and projection products.
- ERA5 and ERA5-Land can support future ClimateOS climate, land, water, ecological and scientific research.
- Reanalysis is model–observation synthesis and must not be represented as pure observation.
- Future science requires governed data lineage, not merely large downloads.

### Idea points

- Create a Future Science Data Infrastructure Library after Task3000.
- Use Task3500 as the formal return gate.
- Register scientific resources before building adapters.
- Make Copernicus CDS the first resource family, not the only resource.
- Build controlled, reproducible, region-bounded retrieval rather than indiscriminate bulk collection.

### Desire points

- Give ClimateOS a durable scientific evidence foundation for sensitivity, constraints, counterfactuals and Earth-system research.
- Preserve access to authoritative climate histories and projections without disrupting current work.
- Enable future researchers and agents to find, understand and reproduce every source and transformation.

### Reasoning points

- Data infrastructure should follow clear scientific questions, not precede them blindly.
- Task3500 is later than Task3000 because sensitivity exploration defines what evidence is needed.
- CDS should be governed as a source ecosystem rather than treated as a single downloadable dataset.
- Data volume, licensing and provenance are part of scientific validity.

### Key decisions

- Place the CDS infrastructure direction at Task3500.
- Keep the task future-facing and non-executable.
- Preserve Task3000 for Weather Jiu-Jitsu and sensitivity exploration.
- Treat ERA5, ERA5-Land, seasonal and projection products as separately classified resources.

### Unresolved questions

- Which CDS products will remain most suitable by the time Task3500 is reached?
- What storage and compute architecture will ClimateOS then have?
- Which Australian region and variables should form the first pilot?
- How should reanalysis bias and uncertainty be represented in Evidence Passports?
- Which products may be redistributed, cached or only referenced?

### Next actions

- Preserve this roadmap in GitHub.
- Do not alter the current ClimateOS execution line.
- Revisit only when the project approaches Task3500 or the Founder explicitly requests an earlier research review.

### Project keywords

ClimateOS; Task3500; Copernicus; CDS; ERA5; ERA5-Land; ECMWF; C3S; reanalysis; climate projections; scientific resource registry; evidence provenance; controlled data retrieval; future science infrastructure; Snowy Valleys; Riverina.
