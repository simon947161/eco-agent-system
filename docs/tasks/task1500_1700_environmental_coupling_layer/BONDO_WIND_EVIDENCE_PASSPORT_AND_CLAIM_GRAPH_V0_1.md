# Bondo Wind Evidence Passport and Claim Graph v0.1

Date: 2026-07-15  
Status: NON_OPERATIONAL_PASSPORT / PUBLIC_METADATA_ONLY / CONCLUSIONS_BLOCKED  
Task: ClimateOS Task1631–1640

## 1. Passport header

| Field | Value |
|---|---|
| Passport ID | `CLIMATEOS-AU-NSW-BONDO-WIND-EP-0001` |
| Subject | proposed Bondo Wind Farm public wind-evidence state |
| Project identities | NSW `SSD-86276211`; EPBC `2026/10465` |
| Evidence cut-off | 2026-07-15 |
| Owner/steward | ClimateOS Founder-controlled documentation process |
| Raw data included | no |
| Machine-readable project GIS included | no |
| Model or weights included | no |
| External account/paid source | no |
| Human scientific approval | none |
| Permitted use | provenance, contradiction and readiness review |
| Prohibited use | wind resource, yield, design, planning, safety or investment decisions |

## 2. Evidence-object registry

| ID | Object | Class | Version/access state | Admission |
|---|---|---|---|---|
| `E-NSW-001` | NSW Planning project page | official portal fact | live snapshot 2026-07-15 | current NSW stage/description |
| `E-EPBC-001` | EPBC referral summary/PDF | official referral record | March 2026 referral version | referral facts |
| `E-EPBC-LAYOUT-001` | `Att 1 Site Layout_Indicative_2026.pdf` | referral attachment identity | indexed; content retrieval blocked | identity only |
| `E-DEV-WEB-001` | Bondo developer webpage | proponent statement | live snapshot 2026-07-15 | attributed context |
| `E-DEV-MAP-001` | preliminary turbine-layout PDF | proponent preliminary map | 2025-11-21 filename identity | visual context only |
| `E-DEV-BOOK-001` | Community Information booklet | proponent dated statement | November 2025 | campaign statement |
| `E-BOM-WAGGA-001` | Wagga public station sample summary from earlier task | derived regional context | Task1601–1610 | non-site context only |
| `E-BOM-CABRA-001` | Cabramurra public station sample summary from earlier task | derived regional context | Task1601–1610 | non-site context only |

The passport references existing ClimateOS summaries; it does not re-ingest raw station observations or source PDFs.

## 3. Claim-node register

| Claim ID | Claim | Supporting object | Classification | State |
|---|---|---|---|---|
| `C-001` | Bondo Wind Farm is a real proposed project | `E-NSW-001`, `E-EPBC-001` | official identity fact | admitted |
| `C-002` | NSW public description states up to 149 turbines | `E-NSW-001` | versioned official portal fact | admitted for NSW snapshot |
| `C-003` | EPBC/developer description states up to/current 164 turbines | `E-EPBC-001`, `E-DEV-WEB-001` | versioned referral/proponent statement | admitted with attribution |
| `C-004` | turbine-count versions differ | `C-002`, `C-003` | derived metadata | admitted; unresolved |
| `C-005` | a preliminary developer map is public | `E-DEV-MAP-001` | public attachment fact | admitted |
| `C-006` | that map is the March 2026 EPBC Att 1 | none | equivalence claim | not established |
| `C-007` | five met masts had been installed by the booklet date | `E-DEV-BOOK-001` | dated proponent statement | admitted with attribution |
| `C-008` | a Bondo wind-monitoring campaign exists | `E-DEV-BOOK-001`, `E-DEV-WEB-001` | proponent campaign statement | admitted for existence only |
| `C-009` | mast measurements are scientifically review-ready | none | scientific readiness claim | rejected/missing evidence |
| `C-010` | Bondo has an independently validated strong wind resource | none | site-wind conclusion | prohibited/not established |
| `C-011` | regional BoM stations validate Bondo | `E-BOM-WAGGA-001`, `E-BOM-CABRA-001` | representativeness claim | rejected |
| `C-012` | Bondo capacity factor or energy yield can be estimated | none | performance claim | prohibited |

## 4. Contradiction and version ledger

| Ledger ID | Nodes | Type | Resolution rule | Current result |
|---|---|---|---|---|
| `V-001` | `C-002` vs `C-003` | 149/164 turbine version difference | retain source/date/stage; await controlling later application | unresolved, non-fatal for identity |
| `V-002` | `E-DEV-MAP-001` vs `E-EPBC-LAYOUT-001` | map identity/version | never substitute; compare only after both contents and metadata are available | blocked |
| `V-003` | narrative 41,923 ha vs generated 41,942.99 ha | area field difference inherited from Task1611–1620 | retain both fields and semantics; no normalization | unresolved |

A version difference is not automatically an error. It becomes a decision blocker when the downstream claim requires one current controlling version.

## 5. Missing-evidence ledger

| Gap ID | Required evidence | Blocks |
|---|---|---|
| `G-001` | authoritative current machine-readable boundary/layout | exact spatial comparison and station distance |
| `G-002` | mast/LiDAR coordinates and terrain context | representativeness review |
| `G-003` | measurement and sensor heights | hub-height/vertical comparison |
| `G-004` | calibration, maintenance and sensor specification | measurement integrity |
| `G-005` | measurement period, interval, recovery and QC | dataset fitness |
| `G-006` | long-term reference/MCP, shear, turbulence and density methods | wind-resource method review |
| `G-007` | uncertainty budget and sensitivity tests | quantitative conclusion |
| `G-008` | explicit licence/reuse terms | local retention and derivative publication |
| `G-009` | consenting qualified reviewer | accountable scientific admission |

## 6. Claim-state rules

Allowed states:

- `ADMITTED_IDENTITY`;
- `ADMITTED_ATTRIBUTED_STATEMENT`;
- `CONTEXT_ONLY`;
- `VERSION_CONFLICT`;
- `MISSING_EVIDENCE`;
- `REJECTED_INFERENCE`;
- `PROHIBITED_CONCLUSION`;
- `HUMAN_REVIEW_REQUIRED`.

No automatic transition may move a proponent statement to independent scientific fact. No evidence count, score or model output may override a missing authority or licence gate.

## 7. Passport result

`PROJECT_REALITY_PASS / CAMPAIGN_EXISTENCE_PASS_WITH_ATTRIBUTION / SITE_WIND_AND_PERFORMANCE_FAIL`

