# ClimateOS Task1621–1630 — Bondo Public EIS Monitoring and Wind-Evidence Intake Formal Brief

Date: 2026-07-15  
Status: FOUNDER_AUTHORIZED / PUBLIC_DOCUMENT_MONITORING / NO_SITE_WIND_CONCLUSION  
Repository: `simon947161/eco-agent-system`  
Branch: `agent/task1621-1630-bondo-eis-intake-review-pack`  
Base merge commit: `d51f70f7cd01671eb9b38f3359eba19a6658e06c`

## 1. Authorization and inherited controls

The Founder authorized merge of PR #65 and one controlled Task1621–1630 advancement round. PR #65 was merged at `d51f70f7cd01671eb9b38f3359eba19a6658e06c`.

This round permits zero-cost, no-registration public-source monitoring, evidence-intake design and preparation of unsent inquiry/reviewer decision material. It does not authorize:

- sending any inquiry or contacting Neoen, NSW Planning, Dr Zhang Lu, Professor Chen Shiping or another person;
- account creation, subscription, quotation request, payment or paid/registered data access;
- committing raw project PDFs, maps, GIS, meteorological observations, models or weights;
- hub-height extrapolation, capacity factor, energy yield, site suitability, planning, safety, investment or viability conclusions.

GraphCast remains `LATER`. Constellation Journey material remains excluded.

## 2. Current official stage snapshot

Accessed 2026-07-15:

| Source | Public state |
|---|---|
| NSW Planning Portal, `SSD-86276211` | `Amend SEARs` / Prepare EIS; up to 149 turbines; EIS not displayed |
| EPBC Public Portal, `2026/10465` | `Assessment Approach Determined`; project documents remain inaccessible in the rendered decision page |
| Bondo developer site | development application aimed for November 2026; surveys and design work continuing; current web description uses 164 turbines |

No public EIS was found in this snapshot. The 149/164 difference remains a versioned source difference.

## 3. Newly resolved public evidence

The developer documents page publicly links:

1. a one-page preliminary turbine-layout PDF dated in its URL/file identity as 2025-11-21;
2. a 24-page Community Information booklet dated November 2025.

The preliminary map labels a project boundary, turbine locations, council boundaries and existing transmission lines. It is a proponent preliminary communication map, not a machine-readable authoritative approval geometry and not the March 2026 EPBC attachment `Att 1 Site Layout_Indicative_2026.pdf`.

The booklet states that:

- a wind-monitoring campaign is underway;
- five meteorological masts had been installed to date;
- the masts are intended to collect wind data for project design;
- some masts may also monitor bat activity and bushfire risk;
- the met masts were managed through the Snowy Valleys Council development-approval process.

The current developer webpage separately states that a Forestry Corporation camera has been installed on one project met mast. This confirms physical monitoring infrastructure, but does not publish the measurement dataset or method.

## 4. Evidence-state distinction

| Claim | Evidence state |
|---|---|
| A real Bondo wind-monitoring campaign exists | `PUBLIC_PROPONENT_DOCUMENT_SUPPORT` |
| Five met masts were installed by the November 2025 booklet date | `PUBLIC_PROPONENT_DOCUMENT_SUPPORT` |
| A preliminary project/turbine map is publicly viewable | `PUBLIC_PROPONENT_ATTACHMENT_READY` |
| The preliminary map is the March 2026 EPBC Att 1 | `NOT_ESTABLISHED` |
| Exact met-mast coordinates and heights are public | `NOT_FOUND` |
| Sensor, calibration, recovery and QC metadata are public | `NOT_FOUND` |
| Raw wind observations are public and reusable | `NOT_FOUND` |
| Bondo has an independently validated strong wind resource | `NOT_ESTABLISHED` |

## 5. Task map

| Task | Deliverable/result |
|---|---|
| 1621 | Merge lineage and authorization lock |
| 1622 | NSW, EPBC and developer-stage snapshot |
| 1623 | Public document-page and preliminary-map discovery |
| 1624 | Five-met-mast campaign evidence classification |
| 1625 | Versioned EIS/document intake manifest design |
| 1626 | Unsent Neoen evidence inquiry draft |
| 1627 | Unsent NSW Planning public-record inquiry draft |
| 1628 | Separate scientific and data-governance reviewer decision gate |
| 1629 | Licence, storage, cost and non-contact controls |
| 1630 | Closure and next-gate decision |

## 6. EIS/document intake protocol

When an EIS or new official attachment becomes public, record before substantive reading:

1. project IDs, source authority and portal stage;
2. document title, exact filename, date, revision and attachment group;
3. source URL, access timestamp and whether login was required;
4. file size and SHA-256 only if local download is separately permitted;
5. copyright/licence/terms and redistribution state;
6. relationship to earlier 149/164 turbine and boundary/layout versions;
7. whether the item is proponent-authored, regulator-issued, consultant-authored or independently reviewed;
8. wind-resource fields available and missing;
9. any confidentiality/redaction constraints;
10. admission decision: identity-only, context-only, method-review-ready, data-review-ready or blocked.

No file should be treated as current merely because its URL remains live.

## 7. Sources

Accessed 2026-07-15:

- [NSW Planning Portal — Bondo Wind Farm](https://www.planningportal.nsw.gov.au/major-projects/projects/bondo-wind-farm)
- [EPBC referral summary — Bondo Wind Farm](https://epbcpublicportal.environment.gov.au/all-referrals/project-referral-summary/?id=91a0bb3b-f91c-f111-8341-002248989885)
- [EPBC project decision page](https://epbcpublicportal.environment.gov.au/all-referrals/project-referral-summary/project-decision/?id=c29660f0-8538-f111-88b4-7c1e522abee3)
- [Bondo Wind Farm developer page](https://bondowindfarm.com.au/)
- [Bondo Wind Farm documents page](https://bondowindfarm.com.au/documents/)
- [Developer preliminary turbine-layout PDF](https://bondowindfarm.com.au/wp-content/uploads/2025/12/20251121_BON01_CommunityBookletMap.pdf)
- [Developer Community Information booklet, November 2025](https://bondowindfarm.com.au/wp-content/uploads/2025/12/20251121_BON01_CommunityInformationBooklet.pdf)

## 8. Decision

`PUBLIC_MONITORING_CAMPAIGN_CONFIRMED / FIVE_MET_MASTS_REPORTED / PRELIMINARY_PROPONENT_MAP_READY / EIS_AND_REVIEWABLE_WIND_DATA_NOT_PUBLIC`

## 9. Hard stop

Task1621–1630 closes without sending inquiries, contacting reviewers, requesting quotes, acquiring raw wind data or forming a regional/site wind conclusion. Do not merge the resulting Draft PR or start Task1631+ without the next authorized batch.

