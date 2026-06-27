# Review Objects Architecture Decision

## Purpose

This document records the Batch19 architectural decision for ClimateOS Review
Objects.

It describes architecture and long-term design intent only. It does not claim
that runtime review, automated reasoning, proof execution, or governance
automation currently exists.

## Decision

ClimateOS Review Engine reviews objects, not opinions.

Opinions, human experience, expert interpretation, AI agent outputs, community
observations, and provider outputs may contribute to review, but the Review
Engine should operate on structured Review Objects.

## Primary Review Objects

```text
Reality Claims
-> Proof Records
-> Evidence Packages
-> Knowledge Objects
-> Forecast Candidates
-> RDA Objects
-> Evidence Assets
```

## Review Object Principle

Review Objects evolve over time through continuous evidence accumulation and
revision.

A Review Object may strengthen, weaken, remain unresolved, reopen, split into
competing hypotheses, merge with new evidence, or become superseded by better
review objects.

## Why This Matters

Object-based review helps ClimateOS preserve:

- traceability
- provenance
- context
- evidence relationships
- confidence changes
- revision history
- unresolved conflict
- governance relevance

## Boundary

This decision does not implement object storage, runtime review, APIs,
automated reasoning, scoring, blockchain, or automated governance decisions.

