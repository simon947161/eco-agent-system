# ClimateOS Review Engine Design Decision

## Purpose

This document records the architectural decision made during Batch18.

It describes long-term design intent only. It does not claim that a runtime
review engine, automated reasoning system, scoring system, or decision engine
currently exists.

## Decision

ClimateOS itself is the Review Engine.

Humans, AI agents, Earth Intelligence providers, observations, forecasts,
scientific knowledge, expert opinion, community observations, minority signals,
and whistleblower signals are contributors to review. They are not permanent
authorities by status alone.

## Key Conclusions

- ClimateOS itself is the Review Engine.
- Humans are contributors, not permanent authorities.
- AI Agents are contributors, not permanent authorities.
- Review is evidence-driven.
- Review is revision-oriented.
- ClimateOS continuously improves rather than declaring absolute truth.
- EcoEngine provides relationship analysis.
- ClimateOS provides integrated review capability.

## Architectural Meaning

ClimateOS is designed to continuously improve its understanding of
relationships in natural systems through observation, evidence, validation,
scientific knowledge, and collective learning.

Its review goal is to produce the most evidence-consistent judgment available at
a given point in time while remaining open to revision whenever new evidence
appears.

## EcoEngine Boundary

EcoEngine provides relationship analysis.

ClimateOS uses relationship analysis as one input into integrated system-level
review.

ClimateOS does not replace EcoEngine. EcoEngine does not replace ClimateOS.

## Review Boundary

Review is not final truth.

Review is not hierarchy.

Review is not voting.

Review is not automated decision-making.

Review is a structured, evidence-driven, revisable process for improving
ClimateOS understanding over time.

## Current Status

Status:

```text
Architecture decision recorded
```

Implemented capability:

```text
Documentation foundation only
```

No runtime implementation, APIs, automated reasoning, scoring engine, voting
system, decision engine, or governance automation is added.

