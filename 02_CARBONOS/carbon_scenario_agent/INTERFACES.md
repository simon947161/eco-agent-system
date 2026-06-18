# Carbon Scenario Agent Interfaces

## Carbon Accounting Agent

```text
Reviewed accounting records
  -> scenario source inputs
```

Accounting records provide baseline or comparison context. Their source
status, boundaries, periods, and uncertainty remain intact.

## Carbon Budget Agent

```text
Budget targets and allocations
  -> target or budget-alignment scenarios
```

Budget records provide planning context but are not automatically treated as
approved pathways.

## Carbon Verification Agent

```text
Verification findings and unresolved issues
  -> scenario validation review
```

Verification records support evidence and traceability review but do not
approve scenario conclusions.

## ClimateOS Scenario Layer

```text
Carbon-oriented scenario records
  -> future ClimateOS scenario coordination
```

ClimateOS integration is conceptual until future scenario systems are
implemented.

## EcoEngine

```text
Scenario assumptions and comparisons
  -> future evidence and validation processes
```

EcoEngine alignment adds no runtime connection in Task56.

## Interface Rules

- preserve source identifiers, versions, boundaries, and review status;
- distinguish observed data, assumptions, comparisons, and outcomes;
- avoid rankings, recommendations, forecasts, and automated decisions;
- retain uncertainty and unknowns; and
- require a separate task for schemas, APIs, runtime links, or calculations.
