# Reference Knowledge Object

## Purpose

A Reference Knowledge Object illustrates how a knowledge item may enter
validation review.

## Conceptual Object

```text
Object Type: Knowledge Object
Topic: Conceptual emissions activity record.
Source Layer: Knowledge Runtime.
Evidence Relationship: Links to source notes, assumptions, and evidence package.
Validation Relationship: Requires knowledge validation before runtime use.
Status: Reviewable concept.
Revision Status: Open.
```

## Required Context

A Knowledge Object should describe:

- topic
- source
- evidence basis
- assumptions
- uncertainty
- relationship to other objects
- review status

## Validation Relationship

Knowledge Objects may flow through:

```text
Knowledge Runtime
-> Knowledge Validation
-> Evidence Package Review
-> Validation IO Model
-> Validation Pack
```

## Boundaries

This is not an Obsidian note schema, vector object, database record, or LLM
retrieval object.

## Related Files

- [Reference Evidence Package](REFERENCE_EVIDENCE_PACKAGE.md)
- [Reference Validation Pack](REFERENCE_VALIDATION_PACK.md)

