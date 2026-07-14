# Bondo–Tumut Public Station Eligibility Register v0.1

Date: 2026-07-14  
Status: TWO_CONTEXT_STATIONS_ADMITTED / NO_BONDO_VALIDATION_STATION  
Task: ClimateOS Task1601–1610

## 1. Eligibility decision

No public station reviewed can presently be admitted as a validation station for the proposed Bondo Wind Farm.

Two stations are admitted only as contrasting regional context objects:

| Field | Wagga Wagga AMO | Cabramurra SMHEA AWS |
|---|---|---|
| BoM station | 072150 | 072161 |
| Latitude | 35.16°S | 35.94°S |
| Longitude | 147.46°E | 148.38°E |
| Elevation | 212 m | 1,482 m |
| Commenced | 1941 | 1996 |
| Status | Open | Open |
| Public DWO product | IDCJDW2139 | IDCJDW2023 |
| Wind source statement | Wagga Wagga AMO | Cabramurra AWS; cloud from Tumbarumba PO |
| Instrument height | UNVERIFIED | UNVERIFIED |
| Exposure history | UNVERIFIED | UNVERIFIED |
| Exact distance to project polygon | BLOCKED — polygon not acquired | BLOCKED — polygon not acquired |
| Primary use | western/plain/airport context | elevated/highland context |
| Bondo site validation | NOT ADMITTED | NOT ADMITTED |

## 2. Project-boundary check

The public EPBC description records:

- project area: approximately 41,923 ha;
- development corridor: approximately 4,916 ha;
- disturbance footprint: approximately 1,591 ha;
- avoidance footprint: approximately 165 ha;
- an indicative 2026 layout attachment;
- ongoing survey and micro-siting work.

No authoritative machine-readable polygon was acquired through the zero-registration public path. A town-centre or hand-drawn project point would introduce false precision, so exact station distance and bearing were not calculated.

## 3. Candidate review

### Tumut

Public long-term summary pages exist, but current wind coverage does not provide a stable, sufficiently documented series for this task. Tumut is not admitted merely because it is geographically close.

### Tumbarumba

The current Daily Weather Observation product uses multiple source stations for different elements. It is retained as metadata context but not admitted as a clean independent wind comparator without an exact element/source audit.

### Wagga Wagga AMO

Strengths:

- open official BoM station;
- clear coordinates and elevation;
- public Daily Weather Observation pages;
- daily gust plus 9am and 3pm wind fields;
- long station history.

Limits:

- airport/plain exposure differs from Bondo plantation and ridges;
- lower elevation;
- exact wind instrument height and exposure-history changes not verified;
- no authoritative project-polygon distance.

Decision: `CONTEXT_ONLY`.

### Cabramurra SMHEA AWS

Strengths:

- open official BoM AWS;
- high-elevation regional context;
- clear coordinates and elevation;
- public daily gust plus 9am and 3pm wind fields.

Limits:

- very high elevation and exposure differ from the project area;
- mixed cloud-source note requires care, although wind is stated as Cabramurra AWS;
- exact wind instrument height and exposure history not verified;
- no authoritative project-polygon distance.

Decision: `CONTEXT_ONLY`.

### Portable RFS stations

Excluded from climatological eligibility. Public BoM notes state portable stations can move and wind instruments may be at 3 m or 10 m AGL. Location history and height must be verified before any bounded event use.

## 4. Wind semantics

BoM Daily Weather Observation notes define:

- maximum wind gust: strongest gust in the 24 hours to midnight, km/h;
- 9am wind: direction and speed averaged over the 10 minutes before 9am;
- 3pm wind: direction and speed averaged over the 10 minutes before 3pm;
- current public data are real-time-system observations with some quality checking but may later be corrected.

These quantities are not interchangeable.

## 5. Licence and storage decision

- Public pages were read without registration or charge.
- The public webpages remain the controlling source objects.
- Raw page tables are not copied into GitHub.
- GitHub records source URLs, access dates, method and aggregate derived statistics only.
- Commercial reuse and redistribution rights for the daily observation tables were not assumed.
- No local credential, account or paid extraction was created.

## 6. Eligibility result

`NO_PUBLIC_BONDO_VALIDATION_STATION / TWO_REGIONAL_CONTEXT_STATIONS_READY_FOR_METHOD_DEMONSTRATION`

The gap is scientifically useful: a future Bondo claim requires project-area met-mast or LiDAR evidence plus an exact regional comparison design.
