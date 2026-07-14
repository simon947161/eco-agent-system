# Bondo–Tumut Wind Evidence Acquisition and Validation Protocol v0.1

Date: 2026-07-14  
Status: PROTOCOL_READY / ZERO_COST_PHASE_AUTHORIZED / STATISTICAL_EXECUTION_NOT_YET RUN  
Task: ClimateOS Task1591–1600

## 1. Study object

Primary region:

`BONDO_TUMUT_COMPLEX_TERRAIN_PLANTATION_STUDY_AREA`

The definitive study polygon must later come from the current NSW planning record or an admitted public project GIS object. Until then, no hand-drawn boundary is authoritative.

Context layers may extend toward Batlow, Gundagai, Wagga Wagga and nearby elevated stations only to evaluate station representativeness and regional gradients. Cooma is excluded from the primary study and may become a later independent comparator.

## 2. Claim and decision threshold

Claim:

`BONDO_TUMUT_PUBLIC_EVIDENCE_WIND_REGIME_SCREENING`

A future result may state only one of:

- `SCREENING_EVIDENCE_SUFFICIENT_FOR_SITE_MEASUREMENT_DESIGN`;
- `SCREENING_EVIDENCE_INSUFFICIENT`;
- `INCOMPARABLE`;
- `BLOCKED_BY_LICENCE_ACCESS_OR_REVIEW`.

It may not state that the wind farm is viable, approved, profitable, safe, environmentally acceptable or likely to meet an energy target.

## 3. Acquisition phases

### Phase A — zero-cost, no-registration

Admit only:

- NSW and Commonwealth project metadata;
- BoM station metadata and public summary tables;
- BoM BARRA2-derived 1991–2020 monthly average wind products where licence is explicit;
- small public planning attachments where redistribution is permitted;
- public terrain/land-cover metadata, with dataset-specific licence verification.

### Phase B — free but registration required

Candidate only:

- NCI-hosted BARRA/BARRA2 subsets;
- Copernicus/ERA5 subsets;
- other registered scientific archives.

Founder must separately approve registration, account ownership, terms and storage before access.

### Phase C — paid or restricted

Candidate only:

- BoM custom extraction or subscription;
- proponent met-mast/LiDAR records;
- commercial wind atlases;
- specialist engineering data or software.

No Phase C purchase is authorized.

## 4. Data minimisation manifest

Before each file acquisition record:

```yaml
acquisition:
  evidence_id:
  source_url:
  publisher:
  dataset_and_version:
  exact_file_or_query:
  geography:
  time_window:
  variables:
  height_or_level:
  temporal_resolution:
  spatial_resolution:
  licence:
  registration_required:
  commercial_use_allowed:
  redistribution_allowed:
  expected_bytes:
  expected_cost_aud:
  local_path:
  github_path_or_exclusion_reason:
  sha256:
  accessed_at_utc:
  reviewer:
```

A missing licence, height, statistic, unit, time support or spatial support blocks admission.

## 5. Target evidence hierarchy

| Priority | Evidence | Purpose | Limitation |
|---|---|---|---|
| 1 | Site met mast or validated LiDAR | hub-height distribution and shear | unavailable publicly; required for resource conclusion |
| 2 | Eligible nearby station observations | independent temporal behaviour and events | point exposure, elevation and distance mismatch |
| 3 | BARRA2 or approved regional reanalysis subset | spatial/regime context | model-observation synthesis; terrain unresolved at site |
| 4 | BoM BARRA2-derived climatology maps | zero-cost height-aware screening | long-term monthly means, not 2021–2026 variability |
| 5 | ACCESS/ADFD exact products | forecast/model comparison | not observation truth; access separately gated |
| 6 | Developer statements | project hypothesis and disclosed studies | interested-party evidence, not validation |

No lower tier replaces a missing higher tier.

## 6. Candidate station eligibility

A station may enter the validation set only after recording:

- official station number and coordinates;
- elevation;
- distance and bearing to study polygon;
- wind instrument height;
- record start/end and completeness;
- changes in site, instrument or exposure;
- availability of speed, direction and gust;
- rural, airport, ridge, valley, plantation or portable status;
- licence and acquisition route.

Portable emergency-service stations are excluded from long-term climatology unless location history and instrument height are stable and documented.

Tumut public climate-summary coverage is not presumed sufficient. Wagga Wagga, Cabramurra-area, Gundagai/Young/Canberra-region candidates must be evaluated rather than automatically admitted.

## 7. Statistics contract

When admissible data exist, calculate separately by evidence object, height and period:

1. sample count and completeness;
2. mean and median wind speed;
3. 10th, 25th, 75th, 90th, 95th and 99th percentiles;
4. monthly and seasonal distributions;
5. hour-of-day distributions where temporal resolution supports them;
6. direction-sector frequency and circular mean/dispersion;
7. calm frequency using a pre-registered threshold;
8. strong-wind and gust exceedance frequency using source-compatible thresholds;
9. annual and seasonal interannual variability;
10. cross-source bias, MAE and RMSE only after matching height, statistic and time support.

No energy yield, Weibull extrapolation, power curve or capacity factor is authorized in Task1591–1600.

## 8. Height and terrain rules

- Treat 10 m, 50 m, 100 m, 150 m, 200 m and proposed hub height as different evidence objects.
- No logarithmic/power-law vertical extrapolation without roughness, stability, displacement-height and specialist controls.
- A 12.5 km BARRA2 cell cannot resolve ridge, valley, plantation canopy, clearing or turbine micro-siting.
- Station-to-grid comparisons must record elevation difference, land cover, exposure and representativeness.
- Forest canopy and plantation operations are material context, not cosmetic map layers.

## 9. Time rules

- 1991–2020 is the official aggregate climatological baseline for the admitted BoM map product.
- 2021–2025 is the preferred complete recent retrospective window.
- 2026 is provisional and must carry a cut-off timestamp.
- 2027–2031 is a monitoring schedule, not observed evidence.
- Forecasts and climate projections must be stored in different evidence classes from observations and reanalysis.

## 10. Storage and security

Local:

- store raw admitted files outside source-control working directories;
- use a structured path such as `ClimateOS/data/bondo_tumut/<evidence_id>/`;
- preserve original bytes read-only;
- keep derived outputs separate;
- generate SHA-256 checksums and a manifest.

GitHub:

- commit protocols, source URLs, manifests, small scripts, checksums and licence-permitted small summaries;
- do not commit credentials, tokens, personal data, restricted files or large grids;
- do not use Git LFS or cloud object storage without a separate decision.

## 11. Cost gate

Current approved cost: `AUD 0`.

Before proposing expenditure, provide:

- exact unmet evidence need;
- free alternative and its limitation;
- supplier and product;
- licence and commercial-use terms;
- one-off fee, monthly fee, GST and cancellation;
- storage/compute/network cost;
- scientific value gained;
- named payer and approval record.

No subscription renews automatically under this protocol.

## 12. Human review gates

- Dr Zhang Lu may be approached as a possible scientific reviewer only after current identity, affiliation, relevant atmospheric/wind expertise and willingness are confirmed.
- Professor Chen Shiping may be approached for data provenance, evidence integrity or distributed-record governance only after current identity, affiliation, expertise and willingness are confirmed.
- Neither is currently appointed.
- Meteorological review and data-governance review are complementary, not interchangeable.
- A later hub-height resource claim requires an independent wind-resource engineer or similarly accountable specialist.

## 13. Readiness decision

`ZERO_COST_PUBLIC_EVIDENCE_PHASE_READY / RAW_STATION_SELECTION_AND_STATISTICAL_RUN_REQUIRE_NEXT_BOUNDED_EXECUTION_RECORD`

Task1591–1600 establishes a defensible path for data acquisition and validation. It does not yet produce a regional wind statistic or project conclusion.
