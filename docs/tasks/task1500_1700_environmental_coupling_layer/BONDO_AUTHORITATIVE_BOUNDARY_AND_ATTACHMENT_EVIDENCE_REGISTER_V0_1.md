# Bondo Authoritative Boundary and Attachment Evidence Register v0.1

Date: 2026-07-14  
Status: CADASTRAL_SOURCE_CONFIRMED / MACHINE_READABLE_POLYGON_NOT_FOUND / LAYOUT_CONTENT_BLOCKED  
Task: ClimateOS Task1611–1620

## 1. Evidence register

| Evidence object | Authority | Public state | Admission decision |
|---|---|---|---|
| NSW project page | NSW Planning Portal | Public; current status and project description visible | `ADMITTED_FOR_CURRENT_NSW_STAGE_AND_DESCRIPTION` |
| NSW map control | NSW Planning Portal | Map link present; no exportable authoritative project polygon verified | `CONTEXT_ONLY` |
| EPBC referral PDF | Australian Government EPBC Public Portal | Public, 47 pages | `ADMITTED_FOR_REFERRAL_VERSION_AND_CADASTRAL_DESCRIPTION` |
| EPBC Lot/DP list | Section 2.2.5 of referral PDF | Public multi-page cadastral list | `ADMITTED_AS_CONTROLLING_TEXTUAL_LIST`; source PDF controls over transcription |
| EPBC footprint fields | Referral PDF | Narrative and generated values both visible | `ADMITTED_WITH_VERSIONED_VALUES` |
| `Att 1 Site Layout_Indicative_2026.pdf` | EPBC attachment register | Name, date, type, sensitivity, confidence and 2,184 KB index visible | `IDENTITY_CONFIRMED / CONTENT_NOT_RETRIEVED` |
| Machine-readable GIS polygon | No verified official source found | Not available through reviewed no-registration path | `NOT_ADMITTED` |
| Developer description/layout | Neoen project page | Public and explicitly preliminary/indicative | `PROPONENT_CONTEXT_ONLY` |

## 2. Controlling cadastral record

The EPBC referral states that the project area is defined by Lot/DP. The list occupies pages 17–19 of the referral PDF and includes State-forest, private and Crown land parcels.

The official PDF remains the controlling list. This register intentionally does not create a substitute GIS boundary or a hand-transcribed legal schedule because:

- transcription could split or join Lot/DP entries incorrectly;
- cadastral inclusion does not prove the final development footprint;
- the development corridor and disturbance footprint remain subject to adjustment;
- an official spatial reference system and geometry were not supplied through the reviewed path.

## 3. Area values and semantics

| Field | Public value | Interpretation |
|---|---:|---|
| Project area, narrative | approximately 41,923 ha | boundary by Lot/DP |
| Project Area, generated footprint field | 41,942.99 ha | portal-generated value; retained separately |
| Development corridor | approximately 4,916 ha | micro-siting flexibility wholly within project area |
| Disturbance footprint | approximately 1,591 ha / generated 1,590.98 ha | indicative ground-disturbance extent |
| Avoidance footprint | approximately 165 ha / generated 165.60 ha | areas sought to be avoided for environmental constraints |

These are different spatial concepts. They must not be treated as interchangeable station-distance polygons.

## 4. Layout attachment state

The referral attachment table records:

- name: `Att 1 Site Layout_Indicative_2026.pdf`;
- type: Site layout;
- date: 2026-03-09;
- sensitivity: No;
- confidence: High.

The project-decision page search index reports 2,184 KB and a 2026-04-14 portal timestamp. The rendered page simultaneously reports no permission and unavailable SharePoint integration. Therefore:

`ATTACHMENT_PUBLICLY_INDEXED_BUT_CONTENT_RETRIEVAL_NOT_VERIFIED`

No attempt was made to bypass the portal, authenticate, scrape a private SharePoint endpoint or obtain the file from a third party.

## 5. Licence and storage decision

- Official pages and the referral PDF were read in place.
- No raw PDF, map image, cadastral geometry or attachment was committed to GitHub.
- No right to redistribute an attachment or derived boundary was assumed.
- GitHub stores only provenance, public metadata, evidence state and method limits.
- Any future local download must retain source URL, access date, checksum and licence/terms note, and must not be republished without a clear permission basis.

## 6. Boundary decision

`OFFICIAL_TEXTUAL_CADASTRAL_BOUNDARY_AVAILABLE / INDICATIVE_LAYOUT_IDENTITY_AVAILABLE / AUTHORITATIVE_MACHINE_READABLE_PROJECT_GEOMETRY_NOT_READY`

Exact station-to-boundary distance remains blocked.

