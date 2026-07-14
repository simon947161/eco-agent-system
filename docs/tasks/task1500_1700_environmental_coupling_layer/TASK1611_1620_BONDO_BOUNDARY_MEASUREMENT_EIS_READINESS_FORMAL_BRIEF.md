# ClimateOS Task1611–1620 — Bondo Boundary, Measurement Evidence and EIS Readiness Formal Brief

Date: 2026-07-14  
Status: FOUNDER_AUTHORIZED / PUBLIC_EVIDENCE_READINESS_ONLY / NO_WIND_RESOURCE_CONCLUSION  
Repository: `simon947161/eco-agent-system`  
Branch: `agent/task1611-1620-bondo-boundary-eis-readiness`  
Base merge commit: `2daa63010f46ef781e1e69a98b0c93e9ac24e170`

## 1. Authorization and inherited controls

The Founder authorized merge of PR #64 and execution of Task1611–1620. PR #64 was merged at `2daa63010f46ef781e1e69a98b0c93e9ac24e170`.

This task is limited to public, no-registration, zero-cost evidence discovery and readiness classification. It does not authorize:

- contact with Neoen, NSW Planning, the Bureau of Meteorology, Dr Zhang Lu, Professor Chen Shiping or any other person;
- a quote request, account creation, FTP, NCI, cloud-object or paid access;
- acquisition or redistribution of raw GIS, layout, met-mast, LiDAR or meteorological data;
- hub-height extrapolation, wind-resource assessment, capacity factor, energy yield, planning, safety, investment or viability conclusions.

GraphCast remains `LATER`.

## 2. Controlling project identity and version state

Primary object: proposed Bondo Wind Farm.

| Public record | Identity and stage | Current design statement |
|---|---|---|
| NSW Planning Portal | `SSD-86276211`; current status `Amend SEARs`; EIS preparation stage | up to 149 turbines; approximately 1.2 GW; two 400 MW / 1,600 MWh BESS |
| EPBC Public Portal | `2026/10465`; controlled action; bilateral/accredited assessment path | up to 164 turbines; hub height up to 200 m; tip height up to 300 m; around 1.2 GW; two 400 MW / 1,600 MWh BESS |
| Developer project page | feasibility/planning and approvals stage | indicative 164-turbine design; subject to studies and approvals |

The 149/164 difference is retained as a public-record version difference. It must not be silently reconciled. The current NSW record controls the NSW planning-stage description; the March 2026 EPBC referral controls its own referral description.

## 3. Task claim

`PUBLIC_PROJECT_IDENTITY_AND_CADASTRAL_DESCRIPTION_CONFIRMED / LAYOUT_RETRIEVAL_AND_WIND_MEASUREMENT_EVIDENCE_NOT_READY`

Question:

> Are the public boundary, layout and project-area wind-measurement materials sufficient to begin an independently reviewable Bondo site-wind assessment?

Answer: no. The public sources identify the project and provide a cadastral description, but the reviewed public path does not provide a verified machine-readable authoritative polygon or the minimum met-mast/LiDAR evidence needed for a site-wind assessment.

## 4. Task map

| Task | Result |
|---|---|
| 1611 | Merge lineage and project isolation locked |
| 1612 | NSW and EPBC project identities/stages reverified |
| 1613 | Project-area, corridor, disturbance and avoidance definitions recorded |
| 1614 | Official Lot/DP boundary source identified |
| 1615 | Indicative layout attachment identity and access state checked |
| 1616 | Public machine-readable GIS availability checked |
| 1617 | Met-mast/LiDAR and wind-method disclosure checked |
| 1618 | Minimum scientific-review evidence gate defined |
| 1619 | Licence, storage, cost and non-contact controls recorded |
| 1620 | Readiness decision and next Founder gate closed |

## 5. Boundary and layout evidence

The EPBC referral states:

- narrative project area: approximately 41,923 ha;
- generated footprint field: 41,942.99 ha;
- development corridor: approximately 4,916 ha;
- disturbance footprint: approximately 1,591 ha, with generated field 1,590.98 ha;
- avoidance footprint: approximately 165 ha, with generated field 165.60 ha;
- project area defined by Lot/DP and including the State-forest investigation-permit area plus private land;
- indicative layout attachment `Att 1 Site Layout_Indicative_2026.pdf`, dated 2026-03-09, marked non-sensitive and high confidence.

The approximate narrative value and generated footprint value are retained separately. No arithmetic normalization is performed.

The public decision page indexes the layout attachment at 2,184 KB, but the rendered portal reports that the user lacks permission and that SharePoint integration is unavailable. Attachment identity is therefore confirmed, while direct content retrieval is `BLOCKED_BY_PUBLIC_PORTAL_ACCESS_STATE`.

An indicative layout is not a legal final project boundary. Micro-siting and survey work remain active. No authoritative machine-readable polygon was found through the reviewed zero-registration public path.

## 6. Measurement-evidence check

The EPBC referral lists permanent meteorological masts as proposed permanent ancillary infrastructure. This establishes only that such infrastructure is contemplated. It does not establish that historical project-area measurements are public or scientifically reviewable.

The reviewed official public material does not disclose:

- existing met-mast or LiDAR coordinates;
- sensor type, calibration or maintenance records;
- measurement heights or boom/orientation details;
- start/end dates, sampling interval or recovery rate;
- filtering, icing, wake, tower-shadow or other quality-control rules;
- long-term reference correlation or measure-correlate-predict method;
- shear, veer, turbulence-intensity or air-density method;
- uncertainty budget;
- turbine-specific hub-height wind distribution or independent validation.

The statement that the area has a “strong wind resource” is a proponent/site-selection assertion. It is not admitted as an independently validated ClimateOS result.

## 7. Minimum admission gate for future scientific review

A future Bondo site-wind evidence package should identify, at minimum:

1. exact project/layout version and spatial reference system;
2. instrument coordinates, terrain/forest context and measurement heights;
3. sensor/LiDAR model, configuration, calibration and maintenance provenance;
4. measurement period, time basis, sampling/aggregation intervals and recovery rate;
5. quality-control and exclusion rules with retained-data counts;
6. reference station/reanalysis choice and correlation/MCP method;
7. vertical extrapolation, shear, veer, turbulence and air-density treatment;
8. uncertainty components and sensitivity tests;
9. separation of observed, modelled, developer-asserted and independently reviewed claims;
10. reviewer identity, conflicts, scope and signed review outcome.

Until these fields are available, the admissible result remains an evidence-gap finding only.

## 8. Sources

Accessed 2026-07-14:

- [NSW Planning Portal — Bondo Wind Farm](https://www.planningportal.nsw.gov.au/major-projects/projects/bondo-wind-farm)
- [EPBC referral summary — Bondo Wind Farm](https://epbcpublicportal.environment.gov.au/all-referrals/project-referral-summary/?id=91a0bb3b-f91c-f111-8341-002248989885)
- [EPBC referral PDF — application 03367](https://epbcpublicportal.environment.gov.au/_entity/sharepointdocumentlocation/1dd7acd6-8638-f111-88b4-7c1e5262eacb/2ab10dab-d681-4911-b881-cc99413f07b6?file=00-2026-10465+Referral.pdf)
- [EPBC project decision page](https://epbcpublicportal.environment.gov.au/all-referrals/project-referral-summary/project-decision/?id=c29660f0-8538-f111-88b4-7c1e522abee3)
- [Bondo Wind Farm developer page](https://bondowindfarm.com.au/)

## 9. Decision

`WAIT_FOR_EIS_PUBLICATION / PUBLIC_ATTACHMENT_IDENTITY_CONFIRMED / DIRECT_LAYOUT_RETRIEVAL_BLOCKED / AUTHORITATIVE_MACHINE_READABLE_GIS_NOT_FOUND / PROJECT_MEASUREMENT_EVIDENCE_NOT_PUBLIC`

## 10. Hard stop

Task1611–1620 closes without downloading or committing raw attachments, contacting any person, requesting a quote, accessing paid/registered data, or forming a Bondo wind-resource conclusion. Do not start Task1621+ or merge the resulting Draft PR without the next explicit Founder decision.

