# Bondo Public Document and Wind-Measurement Manifest v0.2

Date: 2026-07-15  
Status: PUBLIC_DOCUMENTS_VERSIONED / MEASUREMENT_CAMPAIGN_CONFIRMED / DATA_NOT_PUBLIC  
Task: ClimateOS Task1621–1630

## 1. Public document manifest

| Object | Date/version evidence | Authority/type | Public access | Admission |
|---|---|---|---|---|
| NSW project page, `SSD-86276211` | live snapshot 2026-07-15 | NSW regulator portal | public webpage | current NSW stage/description |
| EPBC referral summary, `2026/10465` | live snapshot 2026-07-15 | Commonwealth portal | public webpage | referral identity/description |
| EPBC referral PDF, application 03367 | commenced 2026-03-09 | proponent referral lodged to Commonwealth | public PDF | referral-version facts |
| EPBC `Att 1 Site Layout_Indicative_2026.pdf` | attachment table date 2026-03-09 | EPBC referral attachment | indexed; rendered decision-page retrieval blocked | identity only |
| Developer preliminary turbine layout | filename identity `20251121_BON01_CommunityBookletMap.pdf` | proponent public map | public one-page PDF | preliminary context only |
| Community Information booklet | November 2025 | proponent public booklet | public 24-page PDF | campaign/stage assertions |
| Developer project page | live snapshot 2026-07-15 | proponent webpage | public | current proponent statements |
| Public EIS | none displayed in reviewed sources | not available | not found | blocked/wait |

## 2. Layout-version separation

The public developer map and EPBC attachment are different evidence objects:

| Field | Developer preliminary map | EPBC Att 1 |
|---|---|---|
| Evidenced date | 2025-11-21 filename identity | 2026-03-09 attachment table |
| Authoritative context | community/project communication | EPBC referral attachment |
| Content viewed | yes, through public developer URL | no, portal retrieval blocked |
| Machine-readable geometry | no | not verified |
| Final approved layout | no | no; explicitly indicative |

They must not be substituted for one another or used to infer a final legal boundary.

## 3. Wind-measurement evidence manifest

| Field | Public evidence | State |
|---|---|---|
| Campaign existence | November 2025 booklet says campaign underway | confirmed as proponent statement |
| Number of installed met masts | five installed “to date” in booklet | confirmed as dated proponent statement |
| Council approval path | Snowy Valleys Council development-approval process stated | stated; approval files not independently acquired |
| Fire camera | current project page says FCNSW camera installed on one project mast | stated by proponent |
| Bat monitoring | some masts may monitor bat activity at height | purpose/context only |
| Coordinates | not disclosed in reviewed material | missing |
| Ground elevations/terrain for each mast | not disclosed | missing |
| Mast and sensor heights | not disclosed | missing |
| Sensor makes/models | not disclosed | missing |
| Calibration/maintenance | not disclosed | missing |
| Sampling interval/time basis | not disclosed | missing |
| Campaign start/end dates | not disclosed precisely | missing |
| Recovery/completeness | not disclosed | missing |
| Quality-control rules | not disclosed | missing |
| Long-term reference/MCP | not disclosed | missing |
| Raw or aggregate wind statistics | not disclosed | missing |
| Uncertainty budget | not disclosed | missing |

## 4. Claim controls

“Five masts installed” proves neither five independent high-quality records nor adequate spatial representativeness. A mast may serve wind, ecology or fire-monitoring functions; purpose must be resolved per instrument and period.

The following remain prohibited:

- counting turbine symbols as an approved turbine total without version context;
- digitising the public map into a pseudo-authoritative boundary;
- estimating mast coordinates from map pixels;
- treating proponent “windy/strong resource” wording as an independent finding;
- inferring measurement duration from the booklet’s project timeline;
- comparing public BoM station statistics directly with undisclosed mast data.

## 5. Monitoring trigger fields

A new document warrants intake when at least one changes:

- NSW stage, EIS/exhibition state or SEARs package;
- EPBC assessment decision or document access;
- turbine count, hub/tip height, project area or disturbance footprint;
- official layout/boundary version;
- met-mast/LiDAR count, coordinates, height, period, QC or result;
- wind-resource methodology or uncertainty disclosure;
- licence, access or redaction state.

## 6. Storage and licence state

- Source documents were inspected in place through public URLs.
- No raw PDF, image, geometry or wind dataset is committed to GitHub.
- GitHub records provenance, document identity, factual extracts and admission state.
- Public accessibility does not automatically grant redistribution or commercial reuse.
- Future locally retained files require explicit permission, checksum and licence notes.

## 7. Manifest result

`DOCUMENT_IDENTITY_AND_MEASUREMENT_CAMPAIGN_READY / SCIENTIFIC_DATA_REVIEW_NOT_READY`

