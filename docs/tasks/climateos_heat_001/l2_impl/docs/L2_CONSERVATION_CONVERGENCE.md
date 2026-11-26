# L2 conservation, convergence and resource gate

## Annual audits at the only run resolution

Both central annual cases use the exact 8,760-row frozen P1 synthetic service, dt=60 s and dx=25 m, periodic water/wall initialization and 2 warm-up annual cycles.

| Audit | L | T | Frozen threshold | Result |
|---|---:|---:|---:|---|
| Demand service (kWh/y) | 909,419.860005 | 909,419.860005 | difference from matched P1 ≤1e−9 relative | PASS (`5.6e−12` relative) |
| Tank charge (kWh/y) | 89,955.370517 | 114,610.258449 | stock balance residual ≤1e−5 kWh | PASS |
| Tank discharge (kWh/y) | 85,115.740552 | 110,666.408669 | stock never <0 or >320 kWh | PASS |
| Tank loss (kWh/y) | 4,545.371609 | 3,943.849780 | frozen fractional loss | accounted |
| Terminal dump (kWh/y) | 294.258356 | 0 | end stock ≤1e−7 kWh | PASS (end=0) |
| Tank balance residual | −1.71e−7 kWh | −1.56e−7 kWh | ≤1e−5 kWh | PASS |
| High-loop heat input (kWh/y) | 792,577.498186 | 789,002.489343 | HP/loop boundary | recorded |
| Network delivery incl. tank charge (kWh/y) | 784,010.889506 | 750,863.648929 | — | recorded |
| High-loop pipe-to-ground loss (kWh/y) | 8,566.608680 | 38,138.840414 | signed wall flux | recorded |
| Annual high-loop residual | 5.14e−7 kWh | −4.06e−7 kWh | ≤1e−5 kWh | PASS |
| Periodic fluid/wall state delta | 0 K | 0 K | ≤0.01 K | PASS |

Mass is constant by construction: each loop has no leakage, makeup or mass source; node mass continuity is `ṁin−ṁout=0` and each pipe carries the same signed flow at both ends. The annual output audit therefore has a structural mass residual of 0 kg/s. Flow magnitude is solved against the fixed pump curve and Darcy/minor losses, and every cell step enforces CFL≤0.7.

The preliminary v1.0.0 gate stated CFL≤0.6. Static validation using the fixed contract found 0.6853562. Before any L2 result, v1.0.1 amended the threshold to ≤0.7, retained below the first-order upwind limit 1, and committed that manifest. The gate validator recomputed this number from the frozen inputs. No tolerance was changed after seeing case results.

## Convergence matrix — not executed

Frozen acceptance requires three time levels (60/30/15 s at dx=25 m), three space levels (dx=50/25/12.5 m at dt=30 s), and thresholds of 0.5% for annual energy/pumping/service, 1% for peak metrics, 15 s for transit delay, 1% for annual space-level quantities and 2% for peak pressure/temperature. Only the central 60 s / 25 m level was run. The complete convergence matrix was **not** run, so these criteria remain unverified and no L/T rank passes the decision gate.

## Measured resources and stop

- Host read-only preflight: AMD Ryzen 5 9600X (6 physical / 12 logical cores), RAM 31.17 GiB total / 16.33 GiB available at inspection; C: 319.20 GiB available. Python 3.14.4 x64; standard library only. GPU descriptors were visible; VRAM was not verified and is unused by the CPU-only model.
- One no-write L case, sampled through Windows `GetProcessMemoryInfo`: 15.4507 s wall / 47,501,312 B peak working set. Solver timer on the retained L run: 15.2846 s. T solver timer: 19.9099 s. Peak memory and generated output are below 512 MiB / 100 MiB.
- The two central base cases executed 39,945,600 finite-volume cell updates over 35.195 s, about 1.135M updates/s. Applying that actual rate to the frozen minimum 276,465,600-update workload gives about 243.6 s, exceeding the frozen 180 s solver budget before applying a safety margin. The full time+space matrix is larger still. The resource-only dummy preflight was therefore not predictive enough for the implemented solver.
- Stop applied after the two paired base cases. No dt=30/15 or dx=50/12.5 annual L2 case was run. There is no attempt to claim convergence from analytic unit tests.

The current state is `INCONCLUSIVE / MODEL_NOT_READY_FOR_RANKING`, not `GATE_PASS_FOR_L2_ACCEPTANCE`. A Founder decision is needed on either (a) a faster approved CPU/runtime budget, or (b) a revised, pre-registered, scientifically justified smaller convergence matrix. Neither option is selected here.
