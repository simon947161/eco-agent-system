# HEAT–001 L2 SYNTHETIC IMPLEMENTATION — RESULTS

**Status: `INCONCLUSIVE — RESOURCE-GATED BEFORE REFINEMENT`**  
Authorization: [Issue #183](https://github.com/simon947161/eco-agent-system/issues/183) · Accepted design: [PR #182](https://github.com/simon947161/eco-agent-system/pull/182), fixed SHA `8b08152670406ec57de443facd5d589060a675b0` · Frozen P1: [PR #179](https://github.com/simon947161/eco-agent-system/pull/179), fixed SHA `5a2039a2753142b2eb17665da2dba6c4a8648b14`.

## Scope and freeze

This report covers synthetic, offline, one-dimensional transient heat and hydraulic calculations only. The byte-pinned P1 hourly profile is the sole demand input. No GIS, Council/site data, external service, CFD, P2, or production data was read. The P1 source artifacts and accepted calculations remain byte-identical and were not recalculated.

The pre-run contract was committed before scenario calculation. Gate amendment HEAD is `a351247e92a673dc39a2136822ed8fe3e5a65231`; frozen contract v1.0.1 SHA-256 is `60861f0fc5c34e14f7c66feff10b70b7680e61809cbf27e3df9225c4232a9c7b`. Receipt: [`L2_FREEZE_SHA_RECEIPT.json`](../L2_FREEZE_SHA_RECEIPT.json). v1.0.1 corrected an explicit-upwind Courant bound from 0.6 to 0.7 after the frozen geometry and maximum design flow gave 0.68536. This was caught before a formal case and revalidated; thresholds were not outcome-tuned.

## Model implemented

- A–C low-temperature and C–B high-temperature closed loops; supply and return are separate finite-volume pipes. A is the synthetic 40 °C source, C the heat-pump and single-state tank interface, B one aggregated building demand.
- Reuses exact L/T lengths and relative elevations from P0-A: L 80/40 m with 0/+2/+3 m nodes; T 120/180 m with 0/+6/+3 m nodes. There is no A–B third route.
- Water uses frozen constant SYNTHETIC properties (ρ 1000 kg/m³, cp 4180 J/kg-K, μ 0.001 Pa-s); Darcy–Weisbach and local K losses; quasi-steady pump curve; hydrostatic absolute-pressure check; explicit upwind water enthalpy with a separate wall heat-capacity state and frozen U′ ground conductance.
- The heat pump uses the frozen P1 Carnot fraction and dynamic A–C source outlet; sink and source energy are bounded by frozen capacities. The 320 kWh/90 kW C-side tank follows the P1 charge/discharge priority, losses and final-hour terminal dump rule. Backup is capped at 650 kW; service is never silently shed.
- Internal demand is zero-order held from the frozen 8760-row UTC P1 profile. This implementation reports the central paired profile only. Its actual annual simulation resolution was dt=60 s, dx=25 m.

Editable implementation and tests are in `l2_impl/`; the diagram is [`l2_synthetic_system.svg`](../figures/l2_synthetic_system.svg). The accepted design figures were reused by pinned links and were not overwritten: [P0-A flow](https://github.com/simon947161/eco-agent-system/blob/369ee6b9703fedb54ca4da684920e6c23825d6ca/docs/tasks/climateos_heat_001/figures/mvtee-flow.svg), [P0-A linear layout](https://github.com/simon947161/eco-agent-system/blob/369ee6b9703fedb54ca4da684920e6c23825d6ca/docs/tasks/climateos_heat_001/figures/mvtee-linear.svg), [P0-A offset layout](https://github.com/simon947161/eco-agent-system/blob/369ee6b9703fedb54ca4da684920e6c23825d6ca/docs/tasks/climateos_heat_001/figures/mvtee-offset.svg), and [L2 accepted thermohydraulic system](https://github.com/simon947161/eco-agent-system/blob/8b08152670406ec57de443facd5d589060a675b0/docs/tasks/climateos_heat_001/figures/l2_thermo_hydraulic_system.svg).

## Central synthetic annual results (coarse level only)

Both runs use the same final source and frozen inputs. P1 references below are copied unchanged from the accepted contract and are not L2 recalculations.

| Arm | P1 primary energy (kWh/y) | L2 primary energy (kWh/y) | P1 operational CO₂e (kg/y) | L2 operational CO₂e (kg/y) | P1 LCOH (AUD/MWh) | L2 LCOH (AUD/MWh) |
|---|---:|---:|---:|---:|---:|---:|
| R0 | 1,111,513.16 | reference only | 202,093.30 | reference only | 95.83 | reference only |
| R1 | 654,155.32 | reference only | 130,050.36 | reference only | 75.14 | reference only |
| L | 429,983.30 | 428,789.16 | 85,203.92 | 82,863.42 | 74.25 | 73.22 |
| T | 447,310.65 | 467,198.87 | 88,542.90 | 89,828.66 | 90.30 | 90.87 |

L2 delivered service is 909,419.860005 kWh/y for both arms, compared with the immutable P1 service 909,419.85999996 kWh/y; relative difference is below `1e-9`. L2 T−L is +38,409.71 kWh/y primary energy, +6,965.24 kg/y operational CO₂e, and +17.6449 AUD/MWh LCOH. The accepted P1 T−L differences are +17,327.35 kWh/y, +3,338.98 kg/y and +16.0500 AUD/MWh respectively. These are coarse-resolution synthetic observations only. **No layout recommendation is made:** the preregistered temporal and spatial convergence matrix was not run, so the sign and size are not accepted as a scientifically resolved L/T ranking.

## Audits and resource stop

At dt=60 s, dx=25 m:

| Check | L | T | Acceptance |
|---|---:|---:|---|
| Warm-up cycles to periodic state | 2 | 2 | ≤8 |
| Maximum cell temperature start/end delta | 0 K | 0 K | ≤0.01 K |
| Tank terminal stock | 0 kWh | 0 kWh | ≤1e-7 kWh |
| Annual high-loop energy residual | 5.14e-7 kWh | −4.06e-7 kWh | ≤1e-5 kWh |
| Annual tank energy residual | −1.71e-7 kWh | −1.56e-7 kWh | ≤1e-5 kWh |
| Backup maximum | 650 kW limit not exceeded | 650 kW limit not exceeded | pass |
| Runtime (solver timer) | 15.285 s | 19.910 s | record |
| Independent 8760-row service replay | 909,419.860000 kWh | 909,419.860000 kWh | matches within 1e-6 kWh |

The independent replay reads stored hourly CSV and the pinned gzip fixture, does not import the solver, and reproduces demand, served service, annual tank balance and annual pipe balance. The separate analytic/unit suite passes 12/12 tests. See [`L2_ANALYTIC_BENCHMARK_RECEIPTS.md`](L2_ANALYTIC_BENCHMARK_RECEIPTS.md) and [`L2_CONSERVATION_CONVERGENCE.md`](L2_CONSERVATION_CONVERGENCE.md).

An OS working-set sampler measured 47,501,312 bytes peak for one no-write L case; this is below the frozen 512 MiB ceiling. The two final hourly CSVs are 2,387,329 B (L) and 2,366,593 B (T), below the 100 MiB output ceiling. Actual measured solver throughput across the two base cases is approximately 1.15 million finite-volume cell updates/s (39,945,600 updates / 34.725 s). Even the frozen 276,465,600-update workload projects to about 240 s at observed throughput, exceeding the 180 s total solver budget; the full three-level time/space matrix is larger. **Stop condition applied:** no further full-year L2 runs were started. The two base results remain inspectable but do not pass the complete L2 verification gate.

## Limits and disposition

This is a deliberately minimal, quasi-steady hydraulic and fixed-ground 1D model, with constant synthetic water properties, generic pipe steel, a single tank state, no soil diffusion, no unobserved elevation peaks, and no field geometry. P1 LCOH margin is narrow; the coarse L2 shifts one same-arm LCOH by about 1.03 AUD/MWh, near the frozen 1 AUD/MWh decision floor. No environmental receptor or global cooling conclusions are possible (`H2=UNKNOWN`, `H3=NOT_TESTABLE`).

**Founder decision requested:** `REQUEST REPAIR / EVIDENCE` or `HOLD` for a resource-bounded verification plan (e.g. authorize a faster execution environment or a narrower pre-registered convergence design). `ACCEPT L2 SYNTHETIC` is not recommended from the current incomplete convergence evidence. No downstream stage is authorized by this report.
