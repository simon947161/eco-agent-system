# Bondo EIS Re-Review Trigger Register v0.1

Date: 2026-07-16

Status: TRIGGER_DEFINITION_ONLY / NO_MONITORING / NO_EXTERNAL_REVIEWER_CONTACT

Task: ClimateOS Task1641–1650

## 1. Trigger rule

A trigger opens a bounded re-review question. It does not establish that a
claim is true, authorize acquisition, contact a reviewer or produce a project
decision.

## 2. Trigger register

| Trigger | Event | Affected nodes/gaps | Required internal route | Automatic conclusion |
|---|---|---|---|---|
| `TR-EIS-001` | public EIS or amendment appears | all evidence classes; `G-001`–`G-008` | provenance first, then domain routing | none |
| `TR-LAYOUT-001` | current official layout/boundary becomes accessible | `V-001`, `V-002`, `G-001` | GIS/planning record review | none |
| `TR-COUNT-001` | turbine count changes or 149/164 conflict is resolved | `C-002`–`C-004`, `V-001` | provenance plus stage/authority review | none |
| `TR-AREA-001` | project/investigation area changes | `V-003`, `G-001` | GIS/planning record review | none |
| `TR-MAST-001` | mast/LiDAR coordinates or terrain context appear | `C-007`–`C-011`, `G-002` | provenance, then wind/GIS review | no site validation |
| `TR-HEIGHT-001` | sensor or measurement heights appear | `G-003` | wind-science review | no hub-height conclusion |
| `TR-QC-001` | calibration, maintenance, recovery or QC appears | `G-004`, `G-005` | wind and data-governance review | no fitness conclusion |
| `TR-METHOD-001` | MCP, shear, turbulence, density or extrapolation method appears | `G-006` | wind-science review | no resource conclusion |
| `TR-UNCERTAINTY-001` | uncertainty budget or sensitivity analysis appears | `G-007` | accountable scientific review | no quantitative admission |
| `TR-LICENCE-001` | access/reuse terms appear or change | `G-008` | data-governance/licence review | no reuse permission inferred |
| `TR-REVIEW-001` | consenting qualified reviewer is appointed | `G-009` | identity, expertise, consent and conflict check | no approval inferred |
| `TR-WITHDRAW-001` | source is removed or withdrawn | dependent evidence and claims | preserve receipt; provenance review | no project-status inference |

## 3. Routing order

1. Confirm object identity and source authority.
2. Record the new version without editing the earlier node.
3. Classify the change and affected claims.
4. Check access, licence and retention authority.
5. Route only the bounded question to the responsible role.
6. Record decision, uncertainty, dissent and unresolved gaps.
7. Return to the Founder before acquisition, contact, publication or execution.

## 4. Re-review role separation

| Role | May review | Must not be treated as |
|---|---|---|
| Evidence/provenance reviewer | identity, version, source class and claim support | wind-resource approver |
| GIS/planning record specialist | boundary, layout, stage and spatial-version relationship | legal determination by default |
| Wind/atmospheric scientist | measurement, representativeness, method and uncertainty | licence authority or project approver |
| Data-governance/licence reviewer | access, retention, transformation and redistribution | scientific fitness approver |
| Founder | scope, cost, contact and execution gates | substitute for accountable scientific review |

## 5. Trigger closure states

- `TRIGGER_RECORDED_NO_REVIEW_REQUIRED`;
- `REVIEW_OPEN_PROVENANCE`;
- `REVIEW_OPEN_GIS_PLANNING`;
- `REVIEW_OPEN_WIND_SCIENCE`;
- `REVIEW_OPEN_DATA_GOVERNANCE`;
- `WAIT_FOR_FOUNDER_AUTHORIZATION`;
- `WAIT_FOR_EVIDENCE`;
- `CONTRADICTION_RETAINED`;
- `REVIEW_CLOSED_NO_CLAIM_CHANGE`;
- `REVIEW_CLOSED_CLAIM_STATE_CHANGED`.

No closure state grants scientific approval, planning approval or project
performance assurance.
