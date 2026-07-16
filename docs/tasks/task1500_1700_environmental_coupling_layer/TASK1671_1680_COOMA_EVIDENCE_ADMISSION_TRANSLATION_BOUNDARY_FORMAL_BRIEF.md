# ClimateOS Task1671–1680 — Cooma Evidence Admission and Translation Boundary Formal Brief

Status: implementation complete; independent Founder review required
Authorized base main: `131e63bd4954ef9a8772967f4849427661235f9e`
Cost: AUD 0
External access: none

## Purpose

Task1671–1680 makes Cooma the primary long-term regional observation anchor for
ClimateOS. It defines when a future static environmental relation could become
an evidence relation. It does not acquire evidence and does not say anything
about Cooma's present environmental, planning, water, wastewater or compliance
conditions.

The intended future division is:

- ClimateOS: regional, catchment, climate, planning and environmental evidence
  context, provenance, uncertainty and translation governance;
- a separate Cooma WorkOS: operational backflow prevention, liquid waste and
  trade waste work;
- the interface: context identifiers and review states only, with customer,
  person, address, inspection, enforcement, legal and operational records
  blocked from ClimateOS.

## Task map

| Task | Closed deliverable |
|---|---|
| 1671 | Verify post-PR #71 main lineage and isolate the authorized branch |
| 1672 | Register Cooma as a named real-place anchor without source verification |
| 1673 | Define the nine eligible evidence classes |
| 1674 | Separate source visibility from licence and reuse permission |
| 1675 | Define global, regional, Cooma, town-catchment, station and worksite scales |
| 1676 | Define observation, publication, retrieval and revision time gates |
| 1677 | Require uncertainty, alternative-explanation and non-stationarity review |
| 1678 | Define unassigned expert-review roles without granting authority |
| 1679 | Specify the ClimateOS–WorkOS privacy and operational boundary |
| 1680 | Validate fictional fixtures, close the batch and return a Founder Gate |

## Five admission conditions

1. Evidence type: a candidate must belong to the controlled evidence-class
   registry and retain a stable evidence identifier.
2. Visibility and licence: the ability to see a source never proves permission
   to copy, retain, transform or redistribute it.
3. Spatial scale: global, south-eastern Australian, Cooma regional,
   town-catchment, observation-station and property/worksite objects remain
   distinct. No automatic downscaling or local inference is permitted.
4. Time: observed, published, retrieved and revised times are separate. A future
   relation must declare temporal overlap and mismatch before use.
5. Uncertainty and review: data quality, spatial representativeness, temporal
   alignment, non-stationarity and alternative explanations require explicit
   treatment and human review before promotion.

## Implemented artifacts

- `cczps_lite/contracts/cooma_regional_evidence_admission.schema.json`
- `cczps_lite/input/cooma_evidence_admission_fictional_examples.json`
- `cczps_lite/integration/cooma_evidence_admission.py`
- `cczps_lite/output/cooma_evidence_admission_preview.json`
- `tests/test_cooma_evidence_admission.py`

The fixture contains no source URL, downloaded content, real observation,
official instrument identity, private worksite, customer or compliance record.
The expressions “RP” and “DCP” remain user-supplied planning concepts whose
exact official identities and current versions require a later source check.

## Non-authorizations

This batch does not authorize source browsing, downloads, real datasets, model
execution, monitoring, cloud services, paid services, legal interpretation,
planning advice, local environmental conclusions, scientific conclusions,
operational job instructions, inspections or compliance decisions.
