# CarbonOS Agent Catalog

## Purpose

This catalog records the official planned CarbonOS agent families. Entries are
placeholders and do not represent executable or operational agents.

| ID | Agent Name | Purpose | Status | Future Task |
| --- | --- | --- | --- | --- |
| CarbonOS-01 | Green Power Classification Agent | Organise electricity consumption, physical, trading, and allocation pathways, evidence, uncertainty, and human review status. | Foundation Established | Task51 completed; future implementation task to be assigned |
| CarbonOS-02 | Carbon Accounting Agent | Organise activity and energy data, boundaries, classification inputs, future emission records, inventories, evidence, uncertainty, and human review. | Foundation Established | Task52 completed; future implementation task to be assigned |
| CarbonOS-03 | Carbon Budget Agent | Organise budget boundaries, periods, targets, allocations, accounting inputs, future variance records, scenarios, uncertainty, and human review. | Foundation Established | Task53 completed; future implementation task to be assigned |
| CarbonOS-04 | Carbon Verification Agent | Organise evidence, boundary, traceability, documentation, uncertainty, findings, reviewer observations, and verification preparation without claiming professional assurance. | Foundation Established | Task54 completed; future implementation task to be assigned |
| CarbonOS-05 | ESG Disclosure Agent | Organise reviewed CarbonOS records, evidence summaries, verification findings, governance notes, stakeholder context, and disclosure-preparation records without generating or approving reports. | Foundation Established | Task55 completed; future implementation task to be assigned |
| CarbonOS-06 | Carbon Scenario Agent | Organise carbon-oriented scenario records, assumptions, constraints, unknowns, comparisons, validation review, and governance review without forecasting or recommendations. | Foundation Established | Task56 completed; future implementation task to be assigned |

## Catalog Rules

- An entry at `Planned` status adds no executable capability.
- `Foundation Established` means the agent is documented but not implemented.
- Every agent must follow the repository Agent Standard and Agent Lifecycle.
- A future task must define inputs, outputs, evidence, runtime fields,
  assumptions, validation, governance, limitations, tests, and review.
- Agent outputs must preserve human decision authority and uncertainty.
- No catalog entry authorizes calculations, APIs, regulatory decisions,
  certification, recommendations, or external data access.

The existing `carbon_market_agent/` scaffold is not promoted into this
official five-agent foundation catalog. Any future market-related agent
requires a separate scope and governance review because financial trading and
transactions are outside Task50.

The existing `product_carbon_passport_agent/` scaffold remains a future
extension point. It is not part of the CarbonOS v0.5 five-agent foundation
sequence unless a later task explicitly promotes it.
