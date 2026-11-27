
# HEAT–001 L2 repair P0: frozen workload audit

**Scope:** static arithmetic from frozen contract and receipts; no solver/model call. **Status:** INCONCLUSIVE / MODEL_NOT_READY_FOR_RANKING. **New model runs: 0.**

## Frozen sources

Audited PR #184 HEAD 8d70dbe349c9d8667eb09b1f041136f7775a7eaf; gate commit a351247e92a673dc39a2136822ed8fe3e5a65231; contract SHA-256 60861f0fc5c34e14f7c66feff10b70b7680e61809cbf27e3df9225c4232a9c7b. Issue #185 is the sole authorization. Main was 9eb7577e145e76161f9f1cd8509348b19c2904cc at branch creation. PR #184 remains open, Draft and unmerged; unchanged.

Code/document evidence at that exact HEAD:
- l2_impl/run_l2.py:27–28 constructs pipes; 31–32 compares state; 35–48 initializes layout and cycle; 51 onward performs yearly stepping; 129–146 compares state, retains output and breaks.
- l2_impl/L2_FROZEN_SYNTHETIC_CONTRACT.json:453–456 periodic initialization/acceptance; 668–692 resource scope and budgets; 734 onward pre-run gate.
- l2_impl/profile_resources.py:10M dummy nonphysical operation probe and planned counts at lines 37–40.
- l2_impl/L2_RUN_RECEIPT.json: base timing, throughput, memory observation, cap and NOT_RUN convergence.
- l2_impl/docs/L2_CONSERVATION_CONVERGENCE.md:31–36 base case/resource stop.

Frozen geometries have two supply/return pairs. L lengths AC=80 m, CB=40 m; T AC=120 m, CB=180 m (contract geometry; run_l2.py:38–40). Cell count = 2*ceil(AC/dx)+2*ceil(CB/dx). Annual steps = 8760*3600/dt. Cell updates = cells per step × annual steps × total cycles. This budget uses two total annual cycles per case, as the base receipt records: one prior transient cycle plus one accepted/analyzed cycle.

## Full frozen distinct matrix

Time convergence: dt=60/30/15 s at dx=25 m. Space convergence: dx=50/25/12.5 m at dt=30 s. The shared (30 s,25 m) intersection is counted once per layout.

| Layout | dt (s) | dx (m) | Cells/step | Steps/year | Cycles | Cell updates |
|---|---:|---:|---:|---:|---:|---:|
| L | 60 | 25 | 12 | 525,600 | 2 | 12,614,400 |
| L | 30 | 25 | 12 | 1,051,200 | 2 | 25,228,800 |
| L | 15 | 25 | 12 | 2,102,400 | 2 | 50,457,600 |
| L | 30 | 50 | 6 | 1,051,200 | 2 | 12,614,400 |
| L | 30 | 12.5 | 22 | 1,051,200 | 2 | 46,252,800 |
| T | 60 | 25 | 26 | 525,600 | 2 | 27,331,200 |
| T | 30 | 25 | 26 | 1,051,200 | 2 | 54,662,400 |
| T | 15 | 25 | 26 | 2,102,400 | 2 | 109,324,800 |
| T | 30 | 50 | 14 | 1,051,200 | 2 | 29,433,600 |
| T | 30 | 12.5 | 50 | 1,051,200 | 2 | 105,120,000 |
| **Total** | | | | | **20 model-years** | **473,040,000** |

Ten unique configurations (five per layout). Already run: L and T at dt=60/dx=25 only, two configurations / four model-years / 39,945,600 updates in the receipt. Eight remain, estimated at 433,094,400 more updates. They were not run here.

## Cycle semantics and ceiling

Receipt field warmup_cycles=2 is the total loop count. In run_l2.py lines 134–145, cycle_count is assigned the current loop index, last_outputs retains that cycle, the loop breaks on the state threshold at 136–137, and the count is serialized. Thus 2 means two total annual passes: one preceding state adaptation and one accepted/analyzed pass, not two discarded warm-up years plus an analyzed third year. This matches contract wording at 453 that warm-up outputs are excluded and a following cycle is analyzed. The receipt field label is imprecise. If the intended limit means eight discarded warm-up cycles plus one analysis cycle, contract and implementation semantics conflict and require clarification before a run. The contract cap of eight total cycles yields a conservative 1,892,160,000-update matrix (4× two-cycle count).

## Measured versus projected runtime

**Measured at the one base resolution only:** L 15.2846 s; T 19.9099 s; combined 35.1945 s over 39,945,600 updates; pooled rate 1,134,994.97 updates/s. Derived per-layout rates: L 825,299.38; T 1,372,745.47 updates/s. No convergence case has a measured runtime.

**Extrapolations, not measurements:** pooled rate gives 416.78 s for the full two-cycle distinct matrix; missing eight cases 381.58 s. Applying the fastest observed layout rate to all work gives 344.59 s; the slowest gives 573.17 s. Layout-stratified estimate is L 178.32 + T 237.39 = 415.71 s. Largest individual 2-cycle case estimates are L 61.14 s and T 79.64 s. These linear projections omit startup, I/O, validation and safety margin. Eight-cycle matrix at pooled rate estimates 1,667.11 s (27.8 min).

The old 276,465,600 planned updates equal 139,809,600 time-refinement plus 136,656,000 space-refinement updates, one cycle each. Their shared dt30/dx25 intersection is counted in both subtotals, so this is not the unique paired L/T matrix. At the measured rate it projects to the receipt's 243.58 s. It is not a full two-cycle suite result. The 10M dummy probe with a 2× margin estimated 71.04 s but is not a solver benchmark.

## The frozen 180-second scope

The contract sets projected_runtime_budget_seconds=180 but does not define per scenario, process, matrix, or aggregate job. The resource preflight sums time and space workload and applies the stop before any formal annual case (contract 682–692, 734 onward); the implementation receipt also compares its workload projection directly against 180. This supports the original interpretation as a workload cap, while leaving scope ambiguous. This report does not raise or reinterpret it.

Conservative rule: treat 180 s as the aggregate limit for the whole authorized matrix, including L/T, initialization and final validation, until Founder freezes another scope. Full matrix estimate already exceeds that cap. If Founder explicitly changes it to per-case, the two-cycle per-case projections are below 180 s, but the aggregate remains about 417 s; eight-cycle work is higher. A later contract should specify both per-case timeout and aggregate cap.

## Memory, disk and host evidence

**Observed:** L base-case no-write OS working set 47,501,312 bytes (45.30 MiB); probe wall time 15.4507 s. Frozen host report records 31.17 GiB RAM total /16.33 GiB available and C: 319.20 GiB free at the time of measurement; this is historical, not current hardware verification. T and high-grid peak memory were not sampled. A tracemalloc probe stopped at 120 s and has no memory result.

**Frozen hard limits:** 536,870,912 bytes (512 MiB) memory; 104,857,600 bytes (100 MiB) output disk. These remain ceilings, not measured future use. Highest mesh has 50 cells per pipe (T dx=12.5 m); no peak memory evidence exists for it.

**Disk estimate only:** existing compressed hourly artifacts are 78,443 B (L) and 214,779 B (T); annual JSON 1,143 B and 1,133 B. Resource-only 8,760-row/26-metric CSV was 1,094,129 B. Ten tables at about 1.1 MB each suggests ~11 MB raw plus receipts; this is an extrapolation, not a convergence artifact measurement. Compression and output-width effects are unknown; enforce the 100 MiB cap if later authorized.

## Disposition

Full frozen distinct work is 10 cases / 20 model-years at two cycles, not the old 276.47M overlapped one-cycle preflight. Measured-rate estimate is ~417 s; no new computation occurred. Memory is not the proven bottleneck, and high-grid memory is unmeasured. Keep ranking inconclusive.
