
# HEAT–001 L2 repair P0: exact-zero periodic-state audit

**Static review only. New model runs: 0.** Frozen source is PR #184 HEAD 8d70dbe349c9d8667eb09b1f041136f7775a7eaf.

## Trace

1. run_l2.py:35–45 selects geometry, constructs four Pipe instances once, sets tank stock to 0.0 once, and starts the annual cycle. No pipe or tank reinitialization appears inside the loop.
2. run_l2.py:46–48 begins each pass with a new snapshot Pipe; fluid_c and wall_c arrays are copied with list(...). The active arrays are not assigned from those snapshots.
3. l2_model.py:166–189 calculates mesh and coefficients. Default 40 C state arrays are made only when vectors are None; pipe construction is outside the annual loop and later snapshots pass explicit arrays.
4. l2_model.py:195–226 retains old array references locally, allocates new fluid/wall arrays, calculates from old state, and replaces the active arrays. The audited path has no explicit rounding or quantization.
5. run_l2.py:31–32 computes max absolute difference over zipped fluid and wall values. Tank is not part of this scalar.
6. run_l2.py:129–146 compares after each year, retains current-year outputs, breaks at delta <=0.01 K, then serializes the scalar. run_l2.py:140–141 separately requires terminal tank stock within 1e-7 kWh. The tank starts at zero and the model has terminal stock handling; this endpoint check does not force pipe delta to zero.

## Findings

### Verified in code/artifact

- Receipt contains periodic_delta_k=0.0 for both base layouts and warmup_cycles=2.
- Period comparison uses active arrays versus copied cycle-start arrays. No obvious self-alias.
- No explicit annual reset, forced zero assignment, vector rounding, or state reinitialization inside the reviewed loop.
- The comparison computes raw float abs differences before serialization; the numeric zero is not an output-format rounding artifact in the visible path.
- Receipt stores only a scalar; it does not contain per-cell vectors, fluid/wall split, per-pipe maxima, state hashes, or cycle trace. Both annual JSON files at frozen HEAD were read: they report periodic_error_K=0.0, warmup_cycles=2, pipe_energy_storage_delta_kwh=0.0, and their recorded annual residuals. The compressed hourly gzip files are binary and were not decompressed in this projectless environment; only their receipt hashes and byte sizes were checked, so hourly-row content remains NOT_VERIFIED.

### Plausible, not proven

- Annual dynamics may contract to a fixed point. Identical binary64 values at start and end can legitimately produce exact zero without any explicit rounding.
- Strong damping can make the state stop changing at machine precision by a later repeated annual pass.
- The exact-zero scalar could be genuine, but saved evidence is insufficient to confirm every cell and each cycle's trajectory.

### Unknown

- Whether every expected cell was compared or whether any mismatch in vector lengths could be silently truncated by zip. Mesh constructors establish expected dimensions, but no comparison-time length assertions are recorded.
- Per-cycle continuity and actual tank start/end sequence.
- Whether receipt scalar can be independently recomputed: state vectors were not persisted.
- High-resolution and T-specific runtime state behavior; only base output scalar exists.

## Future proof protocol (proposal only)

After separate authorization, freeze diagnostic capture of each cycle boundary: cell counts; independent raw start/end fluid and wall vectors; separate max absolute/RMS deltas by pipe/component; finite min/max; tank start/end; canonical IEEE-754 binary64 vector hashes; and object identity assertions. Preserve raw unrounded values. Add one or more nontrivial deterministic synthetic initial states or forcing variations in separately approved diagnostics to guard against trivial zero tests. Ensure vector lengths equal frozen mesh sizes and start snapshots are distinct objects.

Compare computed deltas from those captured vectors and preserve hashes in receipt. Require unchanged <=0.01 K pipe/wall and <=1e-7 kWh tank thresholds. Update future receipt schema to record total_cycles and discarded_warmup_cycles separately. Do not infer layout ranking from periodicity.

## Conclusion

No visible reset, state alias, forced zero, or rounding defect explains the 0 K in the inspected code. Genuine floating-point fixed-point convergence is plausible. Without raw state and per-cycle data, zero is **unverified**, not proof of a bug and not independently proven convergence. No code changed and no new model/partial/convergence scenario ran.
