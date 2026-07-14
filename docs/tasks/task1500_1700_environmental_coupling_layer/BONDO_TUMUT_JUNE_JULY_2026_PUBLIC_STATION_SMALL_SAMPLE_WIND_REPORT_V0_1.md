# Bondo–Tumut June–July 2026 Public Station Small-Sample Wind Report v0.1

Date: 2026-07-14  
Status: METHOD_DEMONSTRATION_COMPLETE / REPRESENTATIVENESS_FAILURE_CONFIRMED / NO_BONDO_WIND_RESULT  
Task: ClimateOS Task1601–1610

## 1. Purpose

This report runs the bounded descriptive-statistic method on two contrasting public BoM station products.

It tests whether those public stations can support a Bondo site-wind statement. It does not test wind-farm performance.

## 2. Source window and completeness

| Station | Public source days represented | Expected page days | Gust values | 9am values | 3pm values |
|---|---:|---:|---:|---:|---:|
| Wagga Wagga AMO 072150 | 2026-06-01 to 2026-07-14 | 44 | 43 (97.7%) | 44 (100%) | 44 (100%) |
| Cabramurra SMHEA AWS 072161 | 2026-06-01 to 2026-07-10, with June page containing 29 days | 39 | 37 (94.9%) | 39 (100%) | 39 (100%) |

Completeness is relative to the days present in the public pages reviewed, not to 2021–2026.

The July pages are provisional. BoM states that real-time observations may later be corrected.

## 3. Calculation method

For each station and field:

- missing cells are omitted, not treated as zero;
- reported `Calm` is represented as 0 km/h only for the 9am or 3pm wind-speed field;
- arithmetic mean uses available numeric values;
- median, P90 and P95 use linear interpolation over sorted available values;
- maximum is the largest available value;
- gust exceedance percentages use the available daily gust count;
- no direction statistic is reported because a defensible circular calculation requires a preserved extraction table and calm-direction rule.

## 4. Results

All speeds are km/h.

### Daily maximum gust

| Station | n | Mean | Median | P90 | P95 | Maximum | ≥50 km/h | ≥80 km/h |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| Wagga Wagga | 43 | 30.8 | 28 | 50 | 53.8 | 72 | 14.0% | 0% |
| Cabramurra | 37 | 55.6 | 48 | 93 | 100 | 104 | 48.6% | 21.6% |

### 9am 10-minute mean wind

| Station | n | Mean | Median | P90 | P95 | Maximum | Calm |
|---|---:|---:|---:|---:|---:|---:|---:|
| Wagga Wagga | 44 | 12.2 | 11 | 19 | 24 | 31 | 4.5% |
| Cabramurra | 39 | 22.2 | 22 | 40 | 46.4 | 52 | 5.1% |

### 3pm 10-minute mean wind

| Station | n | Mean | Median | P90 | P95 | Maximum | Calm |
|---|---:|---:|---:|---:|---:|---:|---:|
| Wagga Wagga | 44 | 13.7 | 13 | 23.4 | 25.7 | 31 | 2.3% |
| Cabramurra | 39 | 18.8 | 17 | 32.2 | 39.7 | 52 | 0% |

## 5. Long-term public summary context

The BoM public climate-summary pages report:

| Station | Elevation | Long-term mean 9am wind | Long-term mean 3pm wind | Wind-statistic years shown |
|---|---:|---:|---:|---:|
| Wagga Wagga AMO | 212 m | 10.1 km/h | 14.2 km/h | 68 |
| Cabramurra SMHEA AWS | 1,482 m | 16.2 km/h | 18.2 km/h | 13 |

The public Cabramurra page states that a standard 30-year period is not available. Long-term summary periods and recent sample periods remain separate.

## 6. Interpretation

The sample shows a large contrast between a lower-elevation plain/airport station and an exposed highland station.

That contrast supports only this inference:

> Station elevation, exposure, terrain and source identity materially affect observed wind statistics, so distant public stations cannot be promoted to Bondo site truth.

It does not establish:

- wind at any Bondo turbine location;
- wind at 200 m hub height;
- vertical wind shear;
- plantation-canopy effects;
- turbine-class suitability;
- annual energy production or capacity factor;
- project feasibility.

## 7. Representativeness decision

| Requirement | Wagga | Cabramurra |
|---|---|---|
| Official station identity | PASS | PASS |
| Public wind observations | PASS | PASS |
| Stable exact instrument height verified | FAIL | FAIL |
| Exposure history verified | FAIL | FAIL |
| Exact distance to project polygon | BLOCKED | BLOCKED |
| Similar project elevation/roughness | UNVERIFIED/LIKELY POOR | UNVERIFIED/LIKELY POOR |
| Hub-height support | FAIL | FAIL |
| Bondo validation eligibility | FAIL | FAIL |

## 8. Scientific result

`PUBLIC_STATION_SAMPLE_SUFFICIENT_TO_DEMONSTRATE_NON_EQUIVALENCE / INSUFFICIENT_FOR_BONDO_WIND_RESOURCE`

The correct next evidence is not more confident interpolation. It is an authoritative project polygon, exact station/instrument metadata, a longer licence-compatible series and project-area met-mast or LiDAR data reviewed by a wind specialist.
