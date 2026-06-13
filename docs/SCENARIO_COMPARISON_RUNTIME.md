# Scenario Comparison Runtime

The Scenario Comparison Runtime consolidates existing local CCZPS-Lite evidence
and review records into a transparent cross-scenario view.

It compares:

- environmental, water, land, energy, and risk context
- evidence coverage and traceability
- uncertainty and spatial validation needs
- planning hypothesis, professional validation, expert review, governance, and
  approval-support status

Comparison groups describe current evidence coverage and review needs. They do
not rank scenarios, select a best option, make a final recommendation, or claim
planning, engineering, regulatory, construction, or investment readiness.

Every record requires human and professional review and preserves
`approval_support_status` as `not_ready_for_approval`.

The runtime reads local generated JSON only. It performs no external API, LLM,
GIS/DEM download, simulation, forecast, or hidden network operation.
