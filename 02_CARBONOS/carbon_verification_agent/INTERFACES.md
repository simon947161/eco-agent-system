# Carbon Verification Agent Interfaces

## Green Power Classification Agent

```text
Classification result + evidence + uncertainty + review status
  -> verification evidence and traceability review
```

The verification agent preserves classification status and does not
authenticate certificates or reclassify electricity.

## Carbon Accounting Agent

```text
Accounting records + inventory + method + evidence index
  -> boundary, lineage, completeness, and uncertainty review
```

The agent does not recalculate emissions or select factors.

## Carbon Budget Agent

```text
Targets + allocations + actual references + scenarios + evidence
  -> basis, boundary, version, and documentation review
```

The agent does not approve targets, calculate variance, or forecast outcomes.

## Future ESG Disclosure Agent

```text
Verification summary + findings + unresolved issues + limitations
  -> disclosure preparation
  -> human approval outside the agent
```

The handoff does not authorize publication or establish compliance.

## ClimateOS Validation Layer

```text
CarbonOS verification concepts
  -> future shared evidence, validation, scenario, and governance conventions
```

ValidationOS remains scaffold-only. Alignment is conceptual until a separate
task implements shared contracts.

## Interface Rules

- preserve identifiers, versions, provenance, boundaries, and source status;
- separate source facts, derived records, findings, and reviewer observations;
- retain uncertainty, unavailable evidence, conflicts, and limitations;
- keep professional conclusions and approvals outside automated handoffs; and
- require a separate task before implementing schemas or APIs.
