# ClimateOS Task2071–2080 — Cooma Official Real-Data Pilot

Status: IMPLEMENTED / REAL OFFICIAL DATA RETRIEVED / ZERO COST / L1 MAXIMUM

## 1. Authority and inheritance

The Founder directed ClimateOS to complete the current PR #105 gate and then
start a limited official real-data pilot instead of another synthetic-only
preparation round.

The pilot is stacked from PR #105 Head:

`969b94a2225572199dd14d5d3bc29d9ad28b44f7`

PR #105 remains independently reviewable and is not merged by this batch.

## 2. Tasks

| Task | Completed output |
|---|---|
| 2071 | verified PR #105 scope, mergeability, review and check state |
| 2072 | fixed the real-data pilot identity and two-source allowlist |
| 2073 | implemented manual-approved, HTTPS-only, size-bounded retrieval |
| 2074 | recorded the raw-data public redistribution boundary |
| 2075 | downloaded two real BoM products into gitignored local storage |
| 2076 | parsed Cooma observation identity, stations, coverage and missingness |
| 2077 | parsed the dated official ENSO state and kept local impact separate |
| 2078 | generated a public provenance receipt without raw observation rows |
| 2079 | validated approval, redirects, integrity, parsing and claim limits |
| 2080 | returned the next evidence-acquisition and QGIS decision gate |

## 3. Exact official sources

1. Australian Bureau of Meteorology, Daily Weather Observations for Cooma,
   July 2026, product `IDCJDW2033.202607`.
2. Australian Bureau of Meteorology, Southern Hemisphere monitoring history,
   dated 14 July 2026.

The Cooma product states that temperature, humidity, cloud and rainfall
observations use Cooma Visitors Centre station `070278`; wind and pressure use
Cooma Airport AWS station `070217`.

## 4. Real run

The manually approved run occurred on `2026-07-27T02:06:37Z`.

- both sources returned HTTP 200;
- network was used;
- cost was AUD 0;
- both raw responses were stored under gitignored `runtime_data`;
- SHA-256 digests were recorded;
- the public receipt contains no copied observation rows or HTML body;
- no QGIS project was modified.

The Cooma CSV contained 27 dated rows from 1 to 27 July 2026, 22 columns and
27 non-missing rainfall fields at retrieval time. These are coverage and
missingness facts, not a rainfall sufficiency conclusion.

The dated BoM archive records El Niño as underway. It reports a relative
Niño3.4 value of +1.47 °C for the week ending 12 July 2026, above the Bureau's
+0.80 °C threshold, and a 30-day SOI of -25.8 to 12 July. This is an admitted
official climate-state/outlook fact; it is not a direct Cooma impact result.

## 5. Conclusion boundary

Maximum maturity is L1:

> The named official source records the stated observation identity or climate
> state for its declared period.

The pilot does not establish:

- catchment rainfall volume;
- storage change or water protected;
- streamflow, groundwater or soil-water balance;
- evapotranspiration or evaporation loss;
- extraction, leakage, demand or managed discharge;
- water quality;
- wastewater capacity, overflow, effluent quality or receiving-environment
  condition;
- a local El Niño outcome;
- any engineering, planning or operational decision.
