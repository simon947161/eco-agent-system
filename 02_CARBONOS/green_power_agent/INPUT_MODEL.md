# Green Power Classification Input Model

## Purpose

This conceptual model identifies information that a future classification
workflow may receive. It is not a database schema, API, or implemented runtime
contract.

## Organisation

**Purpose:** identifies the entity reporting or claiming electricity
attributes.

**Example fields:** organisation ID, name, reporting role, jurisdiction,
reporting period, evidence owner.

**Relationships:** owns or operates Facilities; enters Electricity Contracts;
holds Green Certificates; creates internal allocations.

## Facility

**Purpose:** defines the physical or operational boundary where electricity is
generated, delivered, or consumed.

**Example fields:** facility ID, organisation ID, name, location reference,
meter references, operational boundary, reporting period.

**Relationships:** belongs to an Organisation; has Consumption Records and
Energy Sources.

## Consumption Record

**Purpose:** records electricity consumed within a declared boundary and
period.

**Example fields:** record ID, facility ID, start and end dates, quantity,
unit, meter or invoice reference, source, data quality, evidence status.

**Relationships:** belongs to a Facility; may be linked to an Energy Source,
Electricity Contract, Green Certificate, Transaction Record, or allocation.

## Energy Source

**Purpose:** describes the generation, supply, grid, or portfolio source
associated with electricity.

**Example fields:** source ID, source type, technology, asset or supplier,
location, generation period, ownership, evidence references.

**Relationships:** may supply a Facility or support physical, trading, or
allocation evidence for a Consumption Record.

## Electricity Contract

**Purpose:** records contractual terms relevant to electricity delivery and
attribute ownership.

**Example fields:** contract ID, parties, product, start and end dates,
quantity, delivery terms, attribute terms, geography, status, source document.

**Relationships:** connects an Organisation or Facility with an Energy Source,
supplier, Transaction Record, or Green Certificate.

## Green Certificate

**Purpose:** records an instrument that may support electricity-attribute
recognition.

**Example fields:** certificate ID, scheme, technology, generation dates,
quantity, unit, geography, owner, transfer history, retirement status,
registry reference.

**Relationships:** may support one or more Consumption Records through a
documented Transaction Record or contract.

## Transaction Record

**Purpose:** records a purchase, transfer, allocation, retirement, or other
event relevant to attribute ownership.

**Example fields:** transaction ID, parties, transaction type, date, quantity,
unit, price reference if permitted, certificate IDs, contract ID, status.

**Relationships:** links Organisations, Electricity Contracts, Green
Certificates, and proposed classifications.

## Supporting Documentation

**Purpose:** preserves evidence that does not fit the structured concepts
above.

**Example fields:** document ID, title, document type, issuer, issue date,
validity period, owner, source location, version, confidentiality, review
status.

**Relationships:** may support or challenge any input or proposed
classification.

## Shared Input Requirements

Every future input should preserve an identifier, source, owner, reporting
period, unit where applicable, version, evidence status, uncertainty, and
review state. Missing values must remain explicit.
