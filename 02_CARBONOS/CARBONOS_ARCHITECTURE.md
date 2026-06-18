# CarbonOS Architecture

## Purpose

This document defines the conceptual layers of CarbonOS. The layers organise
responsibilities and evidence flows; they are not executable components.

## Green Power Layer

Organises electricity-consumption records and evidence about renewable or
other qualifying green electricity. It may record source, ownership,
certificate, reporting period, matching method, and review status.

Its future outputs provide governed inputs to the Carbon Accounting Layer.
Classification remains evidence-based and subject to human review.

## Carbon Accounting Layer

Organises activity data, reporting boundaries, emission factors, assumptions,
and emission records across Scope 1, Scope 2, and Scope 3 categories.

It may consume reviewed green-power classifications when preparing
electricity-related records. No calculation method is implemented by this
foundation.

## Carbon Budget Layer

Organises carbon budgets by organisation, facility, reporting period, scope,
or other approved boundary. It compares reviewed accounting records with
documented targets or limits while preserving assumptions and uncertainty.

Budget records support review; they do not approve actions or make automated
management decisions.

## Carbon Verification Layer

Organises evidence checks, exceptions, reviewer notes, uncertainties, and
verification status for records produced by the other layers.

Verification is a governed review workflow. CarbonOS does not claim
independent assurance, certification, or regulatory approval.

## Carbon Passport Layer

Organises product-level carbon information, lifecycle boundaries, source
records, versions, and verification references in a human-readable form.

It may reuse reviewed accounting and verification records. A passport is an
information package, not an automatic certification or market authorization.

## Layer Interaction

```text
Energy and activity evidence
  -> Green Power Layer
  -> Carbon Accounting Layer
  -> Carbon Budget Layer
  -> Carbon Verification Layer
  -> Carbon Passport or Disclosure Outputs
```

Information may return to an earlier layer when evidence is missing,
assumptions change, or a reviewer requests correction. Every handoff should
retain source references, reporting boundaries, versions, uncertainty, and
review status.

## Shared Boundaries

- ClimateOS Core is the future source of shared evidence and governance
  conventions.
- ScenarioOS may provide bounded scenario context.
- ValidationOS may provide reusable validation workflows.
- GovernanceOS may record human review and decision authority.
- CarbonOS owns domain-specific carbon definitions and records.

No layer in this architecture adds runtime, API, external data, scientific
calculation, approval, recommendation, or automated decision capability.
