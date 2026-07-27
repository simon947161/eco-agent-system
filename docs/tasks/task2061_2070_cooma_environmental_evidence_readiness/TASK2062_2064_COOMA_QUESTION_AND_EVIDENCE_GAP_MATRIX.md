# Task2062–2064 Cooma Question and Evidence Gap Matrix

## 1. Question families

| ID | Theme | Persistent question |
|---|---|---|
| `CQ-SNOW-01` | snow and climate | How are precipitation form, snow persistence, temperature and seasonal climate background changing across the selected Cooma study system? |
| `CQ-FIRE-01` | bushfire context | What admitted weather, fuel, terrain, ignition and exposure evidence is needed to describe bushfire context without making an operational warning? |
| `CQ-WATER-01` | water quantity and protection | For a declared spatial and time boundary, what water enters, is stored, leaves, is consumed, or remains unmeasured, and how large is the uncertainty? |
| `CQ-WASTEWATER-01` | wastewater resilience | What admitted inflow, capacity, overflow, maintenance, receiving-environment and climate-stress evidence is needed to assess wastewater resilience? |

Drinking-water quality remains a distinct claim track inside the water theme.
It must not be inferred from water quantity, mapped catchments or wastewater
records.

## 2. Evidence gap matrix

| Question | Existing capability | Minimum missing evidence | Candidate derivation | Allowed now |
|---|---|---|---|---|
| precipitation and snow background | monthly program; climate/model registries; QGIS terrain | dated station/gridded observations, precipitation form, temperature, snow observations, baseline period, spatial representativeness | seasonal totals, anomalies, snow-day or persistence indicators with uncertainty | question and acquisition plan only |
| water entering the system | QGIS catchment context; source admission | declared accounting boundary; precipitation observations; surface and imported inflows | boundary-aligned inflow ledger | no quantity claim |
| water stored or protected | named water features as orientation | storage identities, capacity/level/volume series, soil moisture or groundwater evidence where relevant, date and operating context | change in known storage plus explicitly unmeasured stores | no sufficiency claim |
| water leaving through atmosphere | wind protocols; model registry | temperature, humidity, radiation, wind, land cover, method fitness and validation evidence | reference ET or water-surface evaporation with method/uncertainty | no evaporation estimate |
| water leaving through use or flow | hydrology map | streamflow, extraction, transfer, consumption, leakage and discharge evidence | auditable outflow/use ledger | no balance claim |
| drinking-water safety | source/claim admission | sampling locations, dates, analytes, methods, limits, QA/QC and responsible authority | compliance-oriented comparison by qualified authority | source inventory only |
| wastewater loading and resilience | persistent wastewater question | inflow/load series, design/approved capacity, bypass/overflow, wet-weather infiltration, maintenance, receiving waters | capacity and stress indicators with operational context | question and gap register only |
| bushfire context | terrain; source registry; monthly program | dated fuel/vegetation, fire history, weather, drought/moisture, ignition and exposure evidence | descriptive background or approved risk method | terrain/source context only |

## 3. Water-balance question contract

The Founder’s long-term question is represented as an accounting identity, not
as a conclusion:

\[
\Delta S = P + Q_{in} + I_{in} - ET - Q_{out} - W - L - D + \epsilon
\]

Where:

- \(\Delta S\): change in declared storage;
- \(P\): precipitation over the declared boundary;
- \(Q_{in}\), \(Q_{out}\): measured surface/subsurface inflow and outflow;
- \(I_{in}\): imported water;
- \(ET\): evapotranspiration or evaporation, with method declared;
- \(W\): withdrawals and consumptive use;
- \(L\): leakage or other measured losses;
- \(D\): managed discharge;
- \(\epsilon\): residual combining measurement error and unmeasured terms.

Every term must carry a spatial boundary, time interval, units, method, source,
uncertainty and missing-data state. A large residual is a diagnostic signal, not
evidence that one preferred explanation is true.

## 4. Scenario discipline

“Before El Niño” is useful as a preparedness scenario but must not be stored as
a forecast fact without a dated, admitted climate-state source. The program
should distinguish:

- `OBSERVED_STATE`;
- `OFFICIAL_OUTLOOK`;
- `FOUNDER_SCENARIO`;
- `MODEL_SCENARIO`;
- `UNKNOWN`.

The same rule applies to drought, high-wind, high-fire-danger and wet-weather
wastewater scenarios.

## 5. Gap-priority rule

Prioritise a gap only when it:

1. blocks a named question;
2. has a declared decision use;
3. can be sourced lawfully and reproducibly;
4. has an accountable reviewer;
5. does not duplicate an existing ClimateOS object;
6. can be kept within a bounded cost, network and privacy gate.
