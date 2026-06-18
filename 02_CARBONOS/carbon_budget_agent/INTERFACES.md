# Carbon Budget Agent Interfaces

## Purpose

These conceptual flows define no API, schema, runtime, or external connection.

## Green Power Classification Agent

```text
Classification result
  -> Carbon Accounting energy record
  -> reviewed inventory
  -> Carbon Budget context
```

Classification status and uncertainty remain visible through the accounting
inventory. The budget agent does not reclassify electricity.

## Carbon Accounting Agent

```text
Reviewed Carbon Inventory
  -> boundary + period + version + exclusions + uncertainty
  -> Budget Definition and Performance Tracking
```

Only explicitly referenced accounting records may support actual-emissions
entries. Incomplete or scenario inventories retain their original status.

## Future Carbon Verification Agent

```text
Budget records + evidence + validation findings + change history
  -> Verification preparation
  -> Human verification workflow
```

Preparation does not constitute independent assurance.

## Future ESG Disclosure Agent

```text
Reviewed targets + performance records + uncertainty + limitations
  -> Disclosure preparation
  -> Human approval outside the agent
```

The interface does not authorize public claims or regulatory filing.

## Future ClimateOS Scenario Layer

```text
Scenario assumptions + bounded accounting inputs
  -> Scenario Budget
  -> comparison and review pack
```

Scenario records must remain distinct from observed records, approved targets,
forecasts, and operational commitments.

## Interface Rules

- preserve stable identifiers, versions, provenance, and source status;
- distinguish actual, target, allocation, assumption, and scenario records;
- never upgrade incomplete or unreviewed accounting inputs;
- retain uncertainty, exclusions, findings, and reviewer notes;
- keep decisions and approvals outside automated handoffs; and
- require a separate task before implementing machine-readable interfaces.
