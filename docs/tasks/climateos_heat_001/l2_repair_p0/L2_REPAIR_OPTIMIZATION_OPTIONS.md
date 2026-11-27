
# HEAT–001 L2 repair P0: deterministic optimization design

**Proposal only. No code edit, benchmark or model run.** Frozen implementation: #184 HEAD 8d70dbe349c9d8667eb09b1f041136f7775a7eaf.

## Constraints

Keep physical equations, synthetic fixture/parameters, boundaries, event order, CFL 0.7, periodic tolerance 0.01 K, conservation/service thresholds and all original grid levels unchanged. Optimize implementation overhead only. Never skip warm-up unless an independently verified state criterion proves periodicity. Frozen outputs are the reference.

## Candidates and equivalence evidence

| Candidate | Benefit | Risk | Required proof |
|---|---|---|---|
| Precompute immutable geometry, coefficients and fixed per-cell factors | Less repeated attribute/formula work | Low if arithmetic/order retained; changed float order can alter last bits | Coefficient equality; identical frozen input and source hashes; bitwise state/output match if operation order unchanged |
| Replace temporary objects and generator-heavy reductions with fixed indexed loops and bound local values | Potentially lower interpreter overhead | Summation order may change float results | Compare every fluid/wall cell at identical event boundaries, hourly fields, annual totals and frozen residual/service gates |
| Preallocate arrays and swap double buffers | Less allocation/GC; current Pipe.step creates new lists (l2_model.py:203–206,225) | Stale buffer or alias errors | Explicit no-alias invariants, per-step reference comparison, full state/hourly/ledger equality |
| Keep hourly outputs only for candidate accepted cycle | Lower memory/output work; run_l2.py:49–50,127 rebuilds 8,760 rows each cycle | Misattributed or missing output year | Cycle index validation; exact 0–8759 row order/count, field equality, output hash and annual sum equality |
| Separate compute, serialization and end-to-end timers | Reveals true 180 s scope and I/O overhead | Misleading timer boundary | Freeze timer scope; report CPU, solver, per-case and aggregate wall duration; reconcile base 35.195 s |
| Change state storage to standard-library numeric arrays | Potential locality and memory improvement | Conversion/rounding semantics | Binary64 format, operation order, vector hashes and full output equivalence |

Flow-dependent friction caching is lower priority: quantized keys would change inputs; exact-key cache needs bounded memory and proof of unchanged computation.

## Equivalence protocol

1. Under new authorization, freeze source/input/output hashes and retain old implementation as reference.
2. Validate the frozen analytic/component tests and independent replay at approved scope. No tolerance changes.
3. Use the same deterministic synthetic fixtures and scenario order. Compare each per-step boundary and fluid/wall cell. Prefer bitwise IEEE-754 state and output equality.
4. If a candidate changes operation order, require Founder to approve a numerical-equivalence bound stricter than existing scientific tolerances before running. Report max absolute/relative difference and demonstrate no L/T metric ordering change.
5. Recheck unchanged mass/energy closure, service and backup, pressure/CFL, tank stock and periodicity. Independent replay must use a separately implemented calculation path and report hashes.
6. Only after equivalence may the optimization be used in an separately authorized unchanged matrix. Enforce frozen resource caps.

Any changed fixture, omitted cell, nonfinite state, unexpected hash mismatch, analytic/residual/service/periodic failure, or resource breach is a hard stop. Do not adjust input, equations, grids or thresholds to make a candidate pass.
