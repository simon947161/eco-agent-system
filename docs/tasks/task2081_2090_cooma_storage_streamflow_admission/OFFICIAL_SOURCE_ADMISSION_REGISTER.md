# Official Source Admission Register — Cooma Storage and Streamflow

## Admitted sources

| ID | Official source | Evidence admitted | Access/licence | Maximum level |
|---|---|---|---|---|
| `COOMA-FLOW-STATION-410033` | Bureau of Meteorology Hydrologic Reference Stations station details | Murrumbidgee River at Mittagang Crossing; station `410033`; latitude `-36.17`; longitude `149.09`; NSW; catchment area about `1890 km²`; data owner WaterNSW; HRS identity `w00231` | Public HTTPS; HRS page states CC BY 4.0 unless otherwise noted | L1 |
| `COOMA-DROUGHT-FRAMEWORK-2026` | Australian Government DCCEEW, Upper Murrumbidgee drought response, updated 10 April 2026 | Gauge `410033` is the Mittagang Crossing trigger near Cooma; framework trigger is flow below `32 ML/day`; WaterNSW real-time data is the nominated flow source | Public official webpage; attribution required | L1 |
| `COOMA-SHL-WEEKLY-2026-07-23` | Snowy Hydro, Upper Murrumbidgee Drought Operating Framework Weekly Report, status 23 July 2026 | Daily Mittagang Crossing flows for 16–22 July 2026 are published in `ML/day`; report states the trigger was not active at the report date | Public official PDF; source attribution retained | L1 |
| `COOMA-WATER-SOURCE-SMRC` | Snowy Monaro Regional Council, Where Does My Water Come From? | Cooma source is the Murrumbidgee River; treatment occurs at Cooma WTP including fluoridation; treated water is pumped to reservoirs and gravity-fed to reticulation | Public Council webpage | L1 |
| `COOMA-STORAGE-CHAIN-SMRC-DSP` | Snowy Monaro Regional Council Development Servicing Plan | Treated water is transferred to Snowy ballast reservoirs, then gravitates to Pine Range, Royal Hill and Church Hill storages before distribution | Public Council PDF | L1 |

## Dated operational flow facts

The Snowy Hydro report for 16–22 July 2026 records Mittagang Crossing daily flows of `324, 290, 255, 248, 252, 224, 210 ML/day` respectively.

Quality qualifier: the report explicitly describes these as operational data and states that final volumes published by DCCEEW may differ after quality assurance. ClimateOS therefore admits these values only as dated, attributed operational source facts. It does not promote them to a final hydrological assessment.

## Storage time-series admission outcome

`FACILITY_IDENTITY_ADMITTED / PUBLIC_STORAGE_TIME_SERIES_NOT_LOCATED`

The public sources identify the source-water pathway and named treated-water storages. This bounded search did not locate an official public continuous series for reservoir level, usable volume, capacity utilisation, inflow, withdrawal or daily storage change for those Cooma facilities.

The absence of a located public series is a gap record, not proof that the data does not exist. It may be held operationally by Council and remains outside this authorization.

## Prohibited inference

None of the admitted evidence supports a claim that:

- Cooma has enough or insufficient water;
- the `32 ML/day` trigger is a town-supply adequacy threshold;
- distribution reservoirs provide a stated number of days of supply;
- a dated river-flow value establishes water quality;
- Council assets are adequate, inadequate, safe, unsafe or compliant.
