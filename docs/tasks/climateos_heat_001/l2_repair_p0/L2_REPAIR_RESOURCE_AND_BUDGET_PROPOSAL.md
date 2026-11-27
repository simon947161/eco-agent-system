
# HEAT–001 L2 repair P0: resource and budget proposal

**Recommendation:** Option A only after Founder explicitly approves a new aggregate runtime cap or a compatible faster CPU host. Until then HOLD; no matrix execution.

## Evidence classes

Source: frozen #184 HEAD 8d70dbe349c9d8667eb09b1f041136f7775a7eaf; gate a351247e92a673dc39a2136822ed8fe3e5a65231; contract SHA-256 60861f0fc5c34e14f7c66feff10b70b7680e61809cbf27e3df9225c4232a9c7b.

| Metric | Evidence | Value |
|---|---|---:|
| L base runtime (dt60/dx25) | measured receipt | 15.2846 s |
| T base runtime (dt60/dx25) | measured receipt | 19.9099 s |
| Pair solver time / updates | measured receipt | 35.1945 s / 39,945,600 |
| Pooled throughput | derived from recorded measurements | 1,134,994.97 updates/s |
| Full distinct matrix at two cycles | arithmetic + linear projection | 473,040,000 updates / 416.78 s pooled |
| Rate envelope (fast/slow observed layout) | linear projection | 344.59–573.17 s |
| Missing eight cases at two cycles | arithmetic + projection | 433,094,400 updates / 381.58 s |
| Eight-cycle matrix cap | arithmetic + projection | 1,892,160,000 updates / 1,667.11 s pooled |
| Working set | measured L base only | 47,501,312 B (45.30 MiB); T/high-grid unmeasured |
| Base outputs | measured artifacts | hourly gzip L/T 78,443/214,779 B; JSON 1,143/1,133 B |
| Host snapshot | prior dated resource report | 31.17 GiB total /16.33 GiB available RAM, C: 319.20 GiB free |
| Frozen hard limits | contract | 180 s; 536,870,912 B RSS; 104,857,600 B output |

Linear estimates omit initialization, I/O, validation, startup and safety margin. The observed-rate envelope is not a confidence interval. No high-resolution run or current hardware/permission verification exists. Host values are historical, not current measurements.

## A — unchanged full matrix

Retain all ten distinct paired cases and every original time and space level. Proposed for Founder approval: **720 s aggregate wall time**, **120 s per case**, **512 MiB RSS**, **100 MiB total output**. The 720 s covers the slower measured-layout rate extrapolation (573.17 s) plus about 26% headroom. It does not cover eight full cycles. If a case needs more than two total annual cycles, stop and obtain a fresh budget decision. No automatic carry-forward.

Before any future start: verify current host and permissions; amend/version/hash a new contract; define timer scope and case order; install no software; enable per-case and aggregate monitors. Strength: preserves full original convergence criteria and paired L/T. Risk: estimated wall time, not guaranteed; unknown high-grid memory; requires approved compute authorization. No provider/cost can be quoted without a runner selection; no purchase is authorized.

## B — narrower temporal-only verification screen

Illustrative new study: dt=60/30/15 s at dx=25 m for L and T: six distinct configurations. Retain existing base outputs; four scenarios remain. It tests paired temporal sensitivity at the frozen reference grid. It omits spatial refinements dx=50 and 12.5 m, so mesh convergence and mesh-dependent L/T ranking remain untested. It is not a full convergence pass and cannot support an L/T recommendation.

Two-cycle budget: 279,619,200 updates for all six cases; 239,673,600 new updates after the existing base pair. Pooled projections: 246.80 s whole screen, 211.17 s for new work. Both exceed the frozen 180 s aggregate limit. Thus B also requires a separately approved faster host or budget. Strength: answers a focused time-step sensitivity question. Risk: leaves all spatial criteria unresolved; not a shortcut to ranking. It must be registered as a distinct scientific task, not a post-hoc change to #184.

## C — HOLD

Freeze existing code and artifacts and do no further computation. Strength: no added compute risk and no science/contract changes; this is the only option executable under current authorization. Cost: convergence and ranking remain unresolved.

## Future gate proposal

PASS only if before any solver invocation: (1) new versioned contract defines scope, fixture/solver hashes, case order, cycle semantics, per-case and aggregate caps; (2) current host resources and permission verified; (3) frozen equations, geometry, data, event order, science thresholds and scenario levels unchanged or explicitly re-approved as a distinct study; (4) analytic/component anchors pass; (5) paired matrix enumerated with intersection counted once; (6) raw fluid/wall/tank state continuity can be checked; (7) frozen and independent replay hashes available; (8) original mass/energy/service/CFL/pressure/periodicity tests pass; (9) separate RSS/disk/wall monitors enforce hard stops; (10) no post-hoc tuning. Any failure is GATE_BLOCKED and no solver invocation.

## Founder decision

Choose A with an explicit amended budget and verified runner, B as a separately approved temporal-only non-ranking study plus resource remedy, or C HOLD. No option is approved by this proposal.
