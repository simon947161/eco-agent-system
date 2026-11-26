# L2 paired spatial comparison — synthetic, coarse level

**Decision status: INCONCLUSIVE.** L and T share the same final solver, frozen input fixture, service year, dt=60 s, dx=25 m, controller and contracts. P1 values are copied from the accepted P1 ledger/contract and are not recomputed.

| Metric | R0 P1 | R1 P1 | L P1 | L L2 | T P1 | T L2 |
|---|---:|---:|---:|---:|---:|---:|
| Service (kWh/y) | 909,419.86 | 909,419.86 | 909,419.86 | 909,419.86 | 909,419.86 | 909,419.86 |
| Primary energy (kWh/y) | 1,111,513.16 | 654,155.32 | 429,983.30 | 428,789.16 | 447,310.65 | 467,198.87 |
| Operational carbon (kgCO₂e/y) | 202,093.30 | 130,050.36 | 85,203.92 | 82,863.42 | 88,542.90 | 89,828.66 |
| LCOH (AUD/MWh) | 95.8324 | 75.1388 | 74.2536 | 73.2241 | 90.3035 | 90.8691 |

The L2 base-level T−L deltas are +38,409.71 kWh/y primary energy, +6,965.24 kg/y operational CO₂e and +17.6449 AUD/MWh. The corresponding immutable P1 T−L deltas are +17,327.35 kWh/y, +3,338.98 kg/y and +16.0500 AUD/MWh. Thus this single resolution retains the P1 direction but increases the apparent T penalty. It does **not** establish that pipe dynamics robustly change the ranking because the preregistered timestep and spatial convergence checks were not run.

Same-arm P1-to-L2 deltas: L primary energy −1,194.14 kWh/y, operational carbon −2,340.50 kg/y, LCOH −1.0294 AUD/MWh; T primary energy +19,888.22 kWh/y, operational carbon +1,285.76 kg/y, LCOH +0.5655 AUD/MWh. The L changes are near or just beyond the frozen minimum meaningful deltas; the T LCOH difference is below the LCOH decision floor. These comparisons are highly sensitive to the simplified treatment of pipe properties, heat pump return state, pumping and the coarse 60 s/25 m resolution.

No confidence intervals or probability claims are available. The two base cases do not satisfy the full model-quality gate. No environmental receptor claim is made (`H2=UNKNOWN`); global cooling remains `H3=NOT_TESTABLE`.
