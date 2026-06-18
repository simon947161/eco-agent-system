# ESG Disclosure Agent Interfaces

## Green Power Classification Agent

```text
Classification result + evidence + status
  -> accounting and verification context
  -> disclosure preparation
```

Classification status remains visible and is not converted into a claim.

## Carbon Accounting Agent

```text
Inventory records + methods + evidence + uncertainty
  -> disclosure record source material
```

Accounting records provide source context only when their version and review
status are preserved.

## Carbon Budget Agent

```text
Targets + allocations + performance records + scenarios
  -> budget disclosure preparation
```

Budget information must distinguish targets, actuals, assumptions, scenarios,
and unresolved variances.

## Carbon Verification Agent

```text
Verification summary + findings + unresolved issues
  -> disclosure readiness review
```

Verification preparation is not assurance, and unresolved findings remain
visible.

## ClimateOS Governance Processes

```text
Disclosure preparation record
  -> governance review
  -> human decision outside the agent
```

ClimateOS governance concepts may later coordinate review ownership and
decision boundaries.

## EcoEngine

```text
Evidence + validation + governance context
  -> future runtime support after separate approval
```

EcoEngine alignment is conceptual. Task55 adds no runtime connection.

## Interface Rules

- preserve source identifiers, versions, status, boundaries, and periods;
- distinguish source facts, derived records, findings, draft statements, and decisions;
- never upgrade incomplete, scenario, or unresolved status;
- keep publication and compliance decisions outside automated handoffs; and
- require a separate task before adding schemas, APIs, or integrations.
