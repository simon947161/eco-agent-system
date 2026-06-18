# Carbon Accounting Agent Interfaces

## Purpose

This document describes conceptual information flows. It defines no API,
schema, runtime integration, or external connection.

## CarbonOS Foundation

```text
CarbonOS scope, data model, workflow, and governance
  -> Carbon Accounting Agent boundaries and records
```

CarbonOS provides shared organisation, facility, energy, emission, product,
evidence, verification, and governance concepts. The accounting agent should
reuse them rather than create a parallel architecture.

## Green Power Classification Agent

```text
Electricity Consumption
  -> Green Power Classification Result
  -> Carbon Accounting Energy Record
```

The handoff should preserve classification ID, consumption references,
`Physical`, `Trading`, `Allocation`, `Unknown`, or `Needs Review` status,
quantity, period, method version, evidence, confidence description,
validation status, uncertainty, and review notes.

The accounting agent must not upgrade classification status or infer missing
green-power evidence.

## Future Carbon Budget Agent

```text
Reviewed Carbon Inventory
  -> boundary + period + uncertainty + review status
  -> Carbon Budget Review
```

Future budget workflows may consume reviewed accounting records and exclusions.
They must preserve inventory versions and must not treat incomplete records as
final.

## Future Carbon Verification Agent

```text
Accounting records + evidence index + validation findings
  -> Verification preparation
  -> Human verification workflow
```

The accounting agent prepares traceability material. It does not provide
independent assurance or verification.

## Future ESG Disclosure Agent

```text
Reviewed inventory + methods + evidence + limitations
  -> Disclosure preparation
  -> Human approval outside the agent
```

Disclosure interfaces should preserve the exact boundary, period, method,
uncertainty, exclusions, and review state. They do not authorize publication
or establish regulatory compliance.

## Interface Rules

- use stable identifiers and versions;
- preserve provenance and source status;
- distinguish observed, derived, estimated, and scenario data;
- never silently replace `Unknown`, `Needs Review`, or incomplete evidence;
- keep human decisions and approvals outside automated handoffs; and
- require a separate task before implementing machine-readable interfaces.
