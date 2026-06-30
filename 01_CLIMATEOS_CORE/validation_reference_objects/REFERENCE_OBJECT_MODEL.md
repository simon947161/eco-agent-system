# Reference Object Model

## Purpose

This document defines the shared conceptual structure of a Validation Reference
Object.

## Reference Object Fields

A reference object may describe:

- reference object name
- object type
- purpose
- source layer
- related evidence
- related validation process
- confidence context
- revision status
- governance relevance
- limitations

## Conceptual Structure

```text
Reference Object
-> Context
-> Evidence Relationship
-> Validation Relationship
-> Review Status
-> Revision Status
-> Future Runtime Relevance
```

## Object Types

Task96 includes reference forms for:

- Reality Claim
- Knowledge Object
- Evidence Package
- Proof Record
- Scenario Candidate
- Evidence Asset
- Validation Pack

## Use In Examples

Reference Objects can be used by Task95 examples to make validation sessions
more concrete without using real data or executable schemas.

## Boundaries

This model is not a database schema, data contract, JSON schema, API payload, or
runtime object model.

## Related Foundations

- [Knowledge Runtime](../knowledge_runtime/README.md)
- [Proof Record Review Layer](../proof_record_review_layer/README.md)
- [Evidence Package Review Layer](../evidence_package_review_layer/README.md)
- [Validation IO Model](../validation_io_model/README.md)

