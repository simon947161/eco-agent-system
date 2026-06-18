# CarbonOS Conceptual Data Model

## Purpose

This model defines the main information concepts expected in future CarbonOS
work. It is not a database schema, API contract, or executable model.

## Organisation

**Purpose:** identifies the organisation responsible for, reporting, or
reviewing carbon information.

**Example fields:** organisation ID, legal or display name, reporting role,
jurisdiction, reporting period, owner, review status.

**Relationships:** owns or operates Facilities; defines Carbon Budgets; may
report Emission Records and Products.

## Facility

**Purpose:** identifies a bounded site, building, plant, or operational unit.

**Example fields:** facility ID, name, organisation ID, location reference,
operational boundary, reporting period, status.

**Relationships:** belongs to an Organisation; records Electricity Consumption
and other energy activity; may have Emission Records and Carbon Budgets.

## Energy Source

**Purpose:** describes the source or supply category associated with energy
consumption.

**Example fields:** source ID, source type, technology, supplier reference,
geographic region, validity period, evidence references.

**Relationships:** supplies or classifies Electricity Consumption; may support
a Green Electricity record.

## Electricity Consumption

**Purpose:** records electricity used within a declared boundary and period.

**Example fields:** consumption ID, facility ID, start date, end date,
quantity, unit, meter or invoice reference, source ID, data quality.

**Relationships:** belongs to a Facility; references an Energy Source; may be
linked to Green Electricity, Green Certificates, and Emission Records.

## Green Electricity

**Purpose:** records an evidence-based classification of electricity for a
declared reporting purpose.

**Example fields:** classification ID, consumption ID, claimed quantity,
classification basis, matching period, evidence references, uncertainty,
review status.

**Relationships:** classifies Electricity Consumption; may be supported by one
or more Green Certificates; may inform an Emission Record.

## Green Certificate

**Purpose:** records certificate evidence associated with qualifying
electricity.

**Example fields:** certificate ID, scheme, technology, generation period,
quantity, unit, owner, retirement or cancellation reference, status.

**Relationships:** may support one or more Green Electricity records; is
reviewed through a Verification Record.

## Carbon Budget

**Purpose:** records a carbon limit, target, or planning envelope for a
declared boundary and period.

**Example fields:** budget ID, owner, boundary, scopes, baseline, budget
amount, unit, start date, end date, assumptions, status.

**Relationships:** belongs to an Organisation or Facility; is reviewed against
relevant Emission Records; may have Verification Records.

## Emission Record

**Purpose:** records an emission amount together with its activity,
classification, method, factor, and evidence context.

**Example fields:** emission record ID, scope, category, activity reference,
factor reference, method version, amount, unit, uncertainty, reporting period,
review status.

**Relationships:** may belong to an Organisation, Facility, or Product; may
reference Electricity Consumption and Green Electricity; may be checked by a
Verification Record.

## Product

**Purpose:** identifies a product or product version for which carbon
information may be organised.

**Example fields:** product ID, name, version, organisation ID, lifecycle
boundary, functional unit, reporting period, status.

**Relationships:** belongs to an Organisation; may aggregate Emission Records;
may be represented by a future carbon passport and Verification Records.

## Verification Record

**Purpose:** records the review of evidence, assumptions, methods, exceptions,
and uncertainties.

**Example fields:** verification ID, subject type, subject ID, reviewer,
evidence reviewed, checks performed, findings, unresolved issues, status,
review date.

**Relationships:** may review any governed CarbonOS entity without replacing
the source record.

## Relationship Summary

```text
Organisation
  -> Facility
     -> Electricity Consumption
        -> Energy Source
        -> Green Electricity
           -> Green Certificate
        -> Emission Record
  -> Carbon Budget
  -> Product
     -> Emission Record

Verification Record -> may review any entity above
```

Future tasks must define identifiers, required fields, controlled terms,
units, versioning, and validation rules before implementation.
