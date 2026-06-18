# CarbonOS System Map

## Purpose

This map describes the planned CarbonOS information flow. It is documentation
only and does not represent implemented orchestration or runtime capability.

```text
CarbonOS Foundation
  |
  v
Green Power Classification Agent
  |
  v
Carbon Accounting Agent
  |
  v
Carbon Budget Agent
  |
  v
Carbon Verification Agent
  |
  v
ESG Disclosure Agent
```

## Component Map

| Component | Purpose | Inputs | Outputs | Status |
| --- | --- | --- | --- | --- |
| CarbonOS Foundation | Defines subsystem scope, architecture, data concepts, workflow, governance, catalog, and roadmap | Repository standards and approved CarbonOS task definitions | Shared CarbonOS documentation and boundaries | Foundation Established |
| Green Power Classification Agent | Organises physical, trading, allocation, unknown, and needs-review electricity attribution pathways | Consumption records, sources, contracts, certificates, transactions, and evidence | Proposed classification, evidence summary, validation status, uncertainty, and review notes | Foundation Established |
| Carbon Accounting Agent | Organises bounded activity, energy, classification, emission, and inventory records | Activity and energy evidence plus reviewed classification results | Future accounting records, inventory structures, evidence indexes, and review preparation | Foundation Established |
| Carbon Budget Agent | Organises targets, allocations, performance records, variance review, and scenarios | Reviewed accounting inventories, plans, targets, assumptions, and evidence | Budget records, validation findings, review notes, and future verification preparation | Foundation Established |
| Carbon Verification Agent | Plans evidence checks, exceptions, findings, and human verification workflows | CarbonOS records, evidence, lineage, validation findings, and limitations | Verification records and unresolved-issue summaries | Planned |
| ESG Disclosure Agent | Plans controlled disclosure preparation using reviewed records | Reviewed inventories, budgets, verification findings, methods, evidence, and limitations | Human-readable disclosure inputs for human approval | Planned outside current CarbonOS foundations |

## Information Rules

```text
Source evidence
  -> preserves provenance and status
  -> classification
  -> accounting
  -> budget
  -> verification preparation
  -> disclosure preparation
  -> human decision
```

- Every handoff preserves identifiers, versions, boundaries, periods,
  uncertainty, evidence, validation findings, and review status.
- `Unknown`, `Needs Review`, incomplete, and scenario statuses must not be
  silently upgraded.
- Verification preparation is not professional assurance.
- Disclosure preparation is not approval to publish or a compliance finding.
- No component currently performs calculations, forecasting, optimisation,
  external integration, or automated decisions.
