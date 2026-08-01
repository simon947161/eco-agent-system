# MCP/OpenAPI Cross-System Transport Contract RFC v0.2

**Status:** `FOUNDER REVIEW / RFC ONLY`  
**Date:** 2026-08-01  
**North Star:** `EVIDENCE_TRUST_GOVERNANCE_RUNTIME`  
**Implementation authority:** `NOT GRANTED`  
**Mainline write:** `FORBIDDEN`  
**External action:** `FORBIDDEN`

## 1. Purpose

Define one protocol-neutral evidence handoff contract that can be exposed as an
MCP tool or an OpenAPI endpoint without changing the meaning, authority,
provenance, limitations or governance state of the transferred object.

Transport success means only that a conforming envelope was received and a
receipt was issued. It does not mean the claim is true, approved, actionable,
assured, registered in production or accepted by a qualified professional.

## 2. Inherited controls

This RFC inherits and must not weaken:

1. lifecycle transition control;
2. protected-write admission;
3. parent-to-child capability containment;
4. resume safety;
5. bounded executable validation.

The v0.1 system boundaries remain authoritative:

| System | Permitted authority in this RFC |
|---|---|
| Mission Control | route, checkpoint, validate transport and record lifecycle |
| ClimateOS | admit environmental evidence, uncertainty and governance state |
| CarbonOS | translate admitted evidence for disclosure mappings without assurance |
| BuildingOS | form building-domain candidate claims within professional limits |
| ECOChain | register versions, proofs and receipts without upgrading truth status |
| GEGG | company strategy and internal gates; no domain-science substitution |

## 3. Canonical operation

Logical operation: `handoff_evidence(envelope) -> receipt`.

- MCP binding: tool `ggg.handoff_evidence.v0_2`.
- OpenAPI binding: `POST /v0.2/handoffs`.
- Media type: `application/vnd.ggg.handoff+json;version=0.2`.
- Contract Schema: `schemas/cross_os_transport_envelope.schema.json`.
- Receipt Schema: `schemas/cross_os_transport_receipt.schema.json`.

Both bindings carry the same JSON envelope. A binding may add network metadata,
but it must not remove, rename or reinterpret canonical fields.

## 4. Required semantic preservation

Every handoff preserves:

- immutable `handoff_id`, `correlation_id` and `object_id`;
- source and target system identity;
- sender authority and receiving authority;
- evidence state: `OBSERVED`, `PUBLISHED_PLAN`, `MODELLED`, `INFERRED` or
  `SYNTHETIC`;
- source identifier, publisher/provider, retrieval time, source version and
  checksum;
- event/measurement time separately from publication/retrieval time;
- spatial and process boundary;
- value, units, quality code and missing-data treatment where applicable;
- transformations and upstream object references;
- permitted-use/licence boundary;
- uncertainty, limitations, exclusions, freshness due date and supersession
  link;
- declared capabilities, protected-write status and external-action status;
- privacy boundary.

The receiver may append a derived object. It may not overwrite the upstream
object or silently remove its limitations.

## 5. Evidence-state monotonicity

Transport cannot upgrade evidence state. In particular:

- `SYNTHETIC` remains `SYNTHETIC` through the full pilot;
- `PUBLISHED_PLAN` cannot become `OBSERVED` merely because the publisher is an
  official body;
- a BuildingOS candidate claim derived from ClimateOS evidence remains a
  domain candidate, not an engineering conclusion;
- an ECOChain receipt proves registration of an object/version in the bounded
  fixture, not truth or assurance.

## 6. Admission and rejection

A receiver returns `ACCEPTED` only when Schema and governance validation pass.
It returns `REJECTED` with machine-readable reasons when any of these occur:

- missing identity, authority, time boundary, checksum or upstream reference;
- undeclared or incompatible units/boundaries;
- evidence-state upgrade or removal of uncertainty/limitations;
- child capability exceeds the parent capability set;
- protected write requested without approval;
- external action, customer/supplier/technology selection, funding request or
  production release is requested;
- real data appears while this RFC remains synthetic-only;
- private-person, biometric, Katie/Personal OS asset or connection is present;
- an ECOChain adapter claims authority to determine truth;
- a receiver claims authority belonging to another domain OS.

## 7. Idempotency and replay

`handoff_id` is the idempotency key. Replaying an identical envelope produces
the same logical receipt. Reusing the identifier with a different payload must
return `REJECTED / HANDOFF_ID_CONTENT_MISMATCH`. The receipt includes the
envelope SHA-256 and validator version.

## 8. Failure and resume safety

No receiver resumes directly into an executing or validating state after an
interruption. The handoff is checkpointed as `PAUSED_RECOVERY`; the next safe
action is revalidation of the immutable envelope. Partial downstream objects
must not be represented as complete.

## 9. Security posture

This prototype uses stable logical identifiers and SHA-256 content integrity.
Cryptographic actor signatures, DID/VC resolution, authentication, registry
deployment, event-store durability, rate limiting and production key
management are intentionally unresolved and are not simulated as complete.

## 10. Conformance

A conforming implementation must:

1. validate the canonical envelope and receipt fields;
2. enforce the inherited five controls;
3. enforce system authority and evidence-state monotonicity;
4. demonstrate one end-to-end synthetic handoff with receipts;
5. block the negative mutations in the validation suite;
6. make no external action and no mainline write.

## 11. Explicit non-authorizations

This RFC does not authorize real data, production MCP/OpenAPI deployment,
external recipients, real registry writes, engineering conclusions, disclosure
assurance, commercial commitments, token issuance or public-safety decisions.
