# L2 analytic benchmarks and test receipt

**All test inputs are SYNTHETIC.** Command: `python -B -m unittest -v test_l2_model.py` (Python 3.14.4, standard library only). Result: **12 tests passed, 0 failed**, runtime 0.001 s. No package was installed. Independent annual replay commands:

```text
python -B independent_replay.py L 60 25
python -B independent_replay.py T 60 25
```

| Check | Frozen test | Observed | Result |
|---|---:|---:|---|
| Hydrostatic pressure | relative error ≤1e−6 | exact `ρgΔz`, 0 relative error | PASS |
| Laminar Darcy | relative error ≤1e−6 | Hagen–Poiseuille identity, 1e−16 scale floating error | PASS |
| Closed-loop static head | residual ≤1 Pa | 0 Pa around 0/+6/+3/0 m path | PASS |
| No-loss transit | ≤15 s fine-step error | residence-time identity `V/Q`; L AC analytic 350.1 s | PASS |
| Finite thermal mass | relative error ≤1% | capacity-weighted equilibrium within 1% | PASS |
| Zero flow | no advection; wall-ground exchange remains | finite unchanged water state | PASS |
| Flow reversal | reverse upwind boundary and route order | bounded finite temperatures | PASS |
| Upwind stability | CFL ≤0.7 | frozen worst case 0.6853562; oversized flow rejected | PASS |
| Pump curve and COP | pump-limited flow; `1<COP≤Carnot` | bounded flow; out-of-lift COP rejected | PASS |
| Absolute pressure | ≥120 kPa and saturation margin ≥50 kPa | 180 kPa/68 °C accepted; 129,999 Pa and >90 °C rejected | PASS |
| Tank state | 0–320 kWh, ≤90 kW, no simultaneous charge/discharge | valid 20 kW step conserves stock; negative, >capacity and simultaneous rates rejected | PASS |
| Bad units / NaN / nonfinite / temperature | reject invalid values | NaN flow, negative ground temperature and >90 °C rejected | PASS |
| Low source / long-distance / service failure | falsify rather than silently cap | impossible COP rejected; Darcy and travel time rise with 1,800 m route; inadequate 650 kW backup rejected | PASS |

The test suite is an analytic/component suite, not a substitute for full system convergence. The L2 annual runs also check the 650 kW backup guard at every internal step; a breach aborts the run.

## Independent replay receipts

The replay implementation imports no model functions. It reads hourly rows, checks the fixture row count and SYNTHETIC tag/layout, sums service independently, then rebalances the tank and high-loop energy ledger.

| Layout | Rows | Service replay (kWh) | Tank residual (kWh) | Pipe residual (kWh) | Hourly CSV SHA-256 |
|---|---:|---:|---:|---:|---|
| L | 8,760 | 909,419.8600000001 | 4.44e−9 | −1.46e−9 | `bacbab25ee5871e21137ac1d5e0ad7f2cbaff9a9aaf1610eca31d88829e698db` |
| T | 8,760 | 909,419.8600000000 | 4.02e−9 | −4.27e−9 | `68eca616ca21bf815426362e7bd195e1cc5046ca065c92de9781c2ffa9ca0171` |

P1 original test receipt remains 34/34 at its accepted SHA and is cited, not rerun or modified here.
