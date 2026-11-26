# L2 failure conditions, uncertainty and limitations

## Failure conditions exercised in deterministic tests

- Negative, above-capacity or simultaneous tank charge/discharge: rejected as `InvalidModel`.
- Missing/nonfinite values, NaN flow, negative ground temperature, and pipe temperature outside 0–90 °C: rejected.
- Heat pump source lift with `COP≤1` or outside the Carnot bound: rejected/off; no invented heat-pump output.
- Absolute pressure below 120 kPa or saturation margin below 50 kPa: rejected. Annual L/T base minima were 257,993 Pa and 228,211 Pa respectively using the frozen simplified high-point pressure reference.
- Flow reversal uses the reversed upwind boundary; excessive CFL is rejected.
- Darcy loss and analytic transit time increase with long synthetic route length; no full long-pipe annual stress case was run.
- Backup requirement above 650 kW is rejected. Each annual substep checks this bound; both paired central runs completed without an exception.
- Terminal tank inventory, per-cell periodicity, high-loop energy and tank energy are annual acceptance gates. Both central runs passed their frozen tolerances.

The 12 executed unit tests exercise component and guard behavior. No standalone annual zero-flow outage, low-source stress, service-failure, negative-stock annual injection, full route-length stress, or terminal-mismatch case was executed. The failure behavior for those is defined by component guards, but system response under time-varying faults remains unverified.

## Key model uncertainties

1. **Constant water properties:** ρ, cp and μ are fixed across 12–68 °C. Temperature-dependent property effects on friction, COP and storage are not modeled.
2. **Hydraulics:** quasi-steady momentum, single circular diameter, generic roughness and `ΣK=4`; no acoustic transients, valve curves, branch balancing or measured pump map. Elevation is linear between A/C/B only; high points between nodes are unknown by construction.
3. **Thermal route:** P1's equivalent U′ is used independently for each pipe. No insulation layer, soil diffusion, seasonal ground temperature, moisture, burial depth, thermal interference or weather coupling.
4. **Heat pump:** frozen Carnot-fraction approximation; no manufacturer map, cycling, defrost or component dynamic lag. Source return state is only a first-order interface.
5. **Storage/building:** one well-mixed 320 kWh tank state with fixed ΔT; no stratification, dead band, heat-exchanger pinch, DHW draw timing or building thermal mass. B aggregates all buildings.
6. **Spatial envelope:** L/T are fictional lengths and node elevations, not routes, coordinates or a geographic survey. No site-level finding follows.
7. **Resolution:** only dt=60 s/dx=25 m was run. Delay, peak and annual results may move at finer/coarser levels; temporal/spatial convergence is missing and ranking is not accepted.
8. **Cost/carbon:** P1 synthetic factors and capital/price formulas are reused; no current price, tariff or emissions claim. Results are comparative algebra under frozen assumptions.

Founder should treat both annual tables as bounded synthetic demonstrations and decide whether to authorize a faster runtime or a revised, pre-registered smaller verification matrix. Neither choice advances this work into P2 or real-world data collection.
