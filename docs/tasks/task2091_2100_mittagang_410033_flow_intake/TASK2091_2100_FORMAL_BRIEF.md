# ClimateOS Task2091–2100 — Mittagang 410033 Official Flow Intake

Date: 2026-07-28

Status: FOUNDER_AUTHORIZED / REAL OFFICIAL DATA / L1 MAXIMUM

Stacked base: PR #107 Head `106ab36354dc76a86da41d4c3e09e184d17c1c4b`

## Authorized boundary

This slice retrieves one fixed public Bureau of Meteorology Hydrologic
Reference Stations product for gauge `410033`. It validates station identity,
coverage, units, day boundary, source quality codes, missing dates, blank
values, duplicates, SHA-256 and licence context.

It does not access Council non-public data, edit QGIS v0.4, calculate town
water availability, or publish a water-quality, engineering, environmental,
planning or public-safety conclusion.

## Task map

| Task | Deliverable |
|---|---|
| 2091 | Verify PR #107 and select stacked branch strategy |
| 2092 | Lock exact BoM HRS HTTPS endpoint |
| 2093 | Implement bounded manual-approval acquisition |
| 2094 | Validate station and product identity |
| 2095 | Validate coverage and `ML/day` units |
| 2096 | Validate day boundary and record unresolved IANA time zone |
| 2097 | Validate quality codes, gaps, blanks and duplicates |
| 2098 | Generate SHA-256 and gitignored full receipt |
| 2099 | Publish redacted L1 Run Receipt and tests |
| 2100 | Return independent Founder Gate |

## Source semantics retained

The source describes each value as a daily discharge total reported at 9am
local time for the previous 24 hours. The product does not declare an IANA time
zone identifier. ClimateOS therefore retains the source wording and does not
silently convert the boundary to UTC or assert AEST/AEDT.

Quality meanings remain source-controlled:

- `A`: best available;
- `B`: good;
- `C`: poor;
- `E`: unreliable;
- `G`: gap-filled.

The file also states that data gaps were filled with a daily rainfall-runoff
model. A complete calendar sequence therefore does not prove every value was
directly observed.
