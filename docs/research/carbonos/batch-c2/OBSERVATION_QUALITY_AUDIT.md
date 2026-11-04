# BOM raw-observation quality audit — PARTIAL / raw export not obtained

Two exemplars only: Cooma Airport AWS 070217, 16 January 2019; Rockhampton Aero 039083, 25 November 2018. Their values remain Batch C published summaries, not independently reconstructed daily records. The [event register](EVENT_QUALITY_REGISTER.json) keeps raw series, flags, coverage and UTC endpoints null. [Attempt log](ACCESS_ATTEMPTS.json) distinguishes tool unavailability, browser timeout and unvalidated constructed URL probes; none proves legal restriction or absence of BOM data. Stop this bounded acquisition attempt rather than manufacture a series or repeatedly alter requests.

Q1 describes the actual temperature product: plain black table values have completed QC; red italic values have not; blank means no available observation. A following multi-day maximum may also be red because the precise occurrence date is uncertain. Download files are generated with the table and expire. We did not obtain that table for either event. Do not assign a CSV Y/N code from memory, from the unrelated CliDE manual or HRS quality codes. Preserve native code dictionary with any future export. QC-completed does not mean zero sensor uncertainty.

Q2 describes nominal 24-hour maximum to 9am, attributed to the previous day. Hence an event-date maximum nominally covers 9am on the label date to 9am next day. Actual station/day standard-time versus daylight-saving convention and accumulated intervals remain unverified. Australia/Sydney civil DST is not sufficient evidence to convert Cooma records. UTC remains null; no instant at midnight is invented.

## Station history and completeness

| Station | Evidence inspected | What remains unresolved |
|---|---|---|
| Rockhampton 039083 | Q3 compiled 27 July 2026; opened1939. Printed p2 reports approximate Tmax holdings completeness99.8% for Aug1939–Jun2026. Equipment history pp18–20 contains 2018 rain/evaporation equipment changes and a 2017 humidity-probe entry. | Whole-record completeness is NOT event-window completeness. Rain/evaporation changes do not prove a Tmax discontinuity. Moves, dry-bulb calibration and event-specific errors not resolved; no assertion of unchanged site. |
| Cooma 070217 | Q4 indexed excerpt compiled27 July2024; Q5 identifies station commencing1967. Direct metadata file not inspected. | Historical moves, event-era instrument and observation-clock details UNKNOWN; current summary coordinate cannot prove 2019 exposure. |

BOM warns historical metadata is incompletely backfilled and not fully quality-controlled. No sensor serials, site maps or current coordinates are copied as facility geometry. Cooma Airport is not Cooma Visitors Centre. Station, facility, treatment unit and monitoring point remain distinct.

For a later authorised replay, count expected versus actual dates, duplicates, blank values, native QC categories and accumulated spans separately; inspect both target month and proposed before/after window. Missing is never zero. Whole-station completeness cannot substitute. Event-day and proposed analysis-window completeness are currently UNKNOWN. No raw source-file digest exists; package hashes authenticate authored records only.
