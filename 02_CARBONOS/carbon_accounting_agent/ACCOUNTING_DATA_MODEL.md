# Carbon Accounting Conceptual Data Model

## Purpose

This model defines future information concepts. It is not a database schema,
API contract, emission model, or implemented runtime.

## Organisation

**Purpose:** identifies the reporting entity and organisational boundary.

**Example fields:** organisation ID, name, boundary method, jurisdiction,
owner, reporting period, version.

**Relationships:** contains Facilities, Projects, Products, Accounting Periods,
and Carbon Inventories.

## Facility

**Purpose:** identifies a bounded operational site.

**Example fields:** facility ID, organisation ID, name, location reference,
boundary version, owner, status.

**Relationships:** belongs to an Organisation and contains Activity and Energy
Records.

## Activity Record

**Purpose:** records an evidence-bearing operational activity.

**Example fields:** activity ID, activity type, boundary ID, period, quantity,
unit, source, evidence status, uncertainty.

**Relationships:** belongs to an Organisation, Facility, Project, Product, or
Scenario and may support an Emission Record.

## Energy Record

**Purpose:** records electricity, fuel, heat, steam, or other energy activity.

**Example fields:** energy record ID, energy type, quantity, unit, source,
period, facility, meter or invoice reference, quality status.

**Relationships:** is a type of activity evidence; electricity may link to a
Green Power Classification; may support an Emission Record.

## Emission Record

**Purpose:** represents a future derived emission amount and its full method
context.

**Example fields:** record ID, scope, category, activity references, factor
reference, method version, amount, unit, uncertainty, preparer, review status.

**Relationships:** derives from Activity or Energy Records and belongs to an
inventory. No derivation is implemented in Task52.

## Green Power Classification

**Purpose:** preserves a reviewed Task51 classification input.

**Example fields:** classification ID, status, consumption references,
quantity, period, evidence references, confidence description, validation
status, reviewer notes.

**Relationships:** links electricity Energy Records to a physical, trading,
allocation, unknown, or needs-review pathway.

## Carbon Inventory

**Purpose:** groups accounting records for a declared boundary, period, method,
and review state.

**Example fields:** inventory ID, boundary ID, accounting period ID, method,
included scopes, record references, exclusions, uncertainty, status, version.

**Relationships:** belongs to an Organisation or other boundary and contains
Emission Records and review findings.

## Accounting Period

**Purpose:** defines the time interval used for records and inventories.

**Example fields:** period ID, start date, end date, timezone, status,
comparison period, closure date.

**Relationships:** applies to Activity, Energy, Classification, Emission, and
Inventory records.

## Product

**Purpose:** identifies a product and declared product boundary.

**Example fields:** product ID, version, owner, functional unit, lifecycle
boundary, period, status.

**Relationships:** has Activity, Energy, and future Emission Records and may
feed product carbon information.

## Scenario

**Purpose:** identifies a bounded hypothetical accounting context.

**Example fields:** scenario ID, name, baseline, geography, time horizon,
assumptions, evidence status, owner, version.

**Relationships:** contains scenario-labelled Activity, Energy, Classification,
and future Emission Records.

## Relationship Summary

```text
Organisation -> Facility / Project / Product / Scenario
Boundary + Accounting Period -> Activity and Energy Records
Electricity Energy Record -> Green Power Classification
Activity or Energy Record -> future Emission Record
Emission Records -> Carbon Inventory
```

Every future entity should retain identity, provenance, owner, period, boundary,
version, uncertainty, and review status.
