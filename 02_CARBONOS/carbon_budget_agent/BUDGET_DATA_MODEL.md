# Carbon Budget Conceptual Data Model

## Purpose

This model defines future information concepts. It is not a database schema,
calculation model, forecast, or runtime contract.

## Organisation

**Purpose:** identifies the owner of an organisational budget.

**Example fields:** organisation ID, name, boundary method, budget owner,
inventory references, version.

**Relationships:** contains Facilities, Budget Targets, Allocations, and
Scenarios.

## Facility

**Purpose:** identifies a site receiving or reporting against a budget.

**Example fields:** facility ID, organisation ID, name, boundary version,
owner, status.

**Relationships:** belongs to an Organisation and may receive Budget
Allocations and Actual Emissions records.

## Carbon Inventory

**Purpose:** preserves a reviewed accounting input for budget preparation.

**Example fields:** inventory ID, boundary ID, period, method, version,
emission-record references, exclusions, uncertainty, review status.

**Relationships:** supports target basis, performance tracking, and variance
review. No inventory calculation is performed here.

## Budget Period

**Purpose:** defines the time interval for a budget and its reviews.

**Example fields:** period ID, start date, end date, timezone, baseline period,
review dates, status.

**Relationships:** applies to targets, allocations, actuals, and variances.

## Budget Target

**Purpose:** records a human-defined planning target.

**Example fields:** target ID, boundary ID, period ID, target amount, unit,
basis, baseline reference, assumptions, owner, approval status, version.

**Relationships:** may be allocated to Facilities, Projects, Products, or
Scenarios and compared with reviewed Actual Emissions.

## Budget Allocation

**Purpose:** records how a parent target is assigned to child boundaries.

**Example fields:** allocation ID, parent target ID, recipient boundary,
amount, unit, method, assumptions, owner, status.

**Relationships:** belongs to a Budget Target and recipient boundary.

## Actual Emissions

**Purpose:** references reviewed accounting emissions associated with a budget.

**Example fields:** actual record ID, inventory ID, boundary ID, period,
amount, unit, uncertainty, review status, source version.

**Relationships:** derives only from referenced Carbon Accounting records and
may support a Variance Record.

## Variance Record

**Purpose:** records a future comparison between a target or allocation and
reviewed actual emissions.

**Example fields:** variance ID, target ID, actual references, period, value,
unit, explanation, uncertainty, reviewer, status.

**Relationships:** connects Budget Targets or Allocations with Actual
Emissions. No variance calculation is implemented in Task53.

## Scenario

**Purpose:** identifies a bounded hypothetical budget context.

**Example fields:** scenario ID, name, baseline, horizon, assumptions, target
references, evidence status, owner, version.

**Relationships:** may contain scenario-labelled targets, allocations, and
comparison records.

## Relationship Summary

```text
Organisation -> Facility
Carbon Inventory -> basis for Budget Target
Budget Target -> Budget Allocation
Reviewed accounting records -> Actual Emissions reference
Budget Target + Actual Emissions -> future Variance Record
Scenario -> scenario-labelled targets and allocations
```

Every future entity should retain identity, source, owner, boundary, period,
unit, version, uncertainty, evidence status, and review status.
