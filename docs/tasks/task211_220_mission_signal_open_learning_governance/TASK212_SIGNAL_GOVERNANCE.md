# Task212 Signal Governance

## Purpose

Create a documentation-only taxonomy for ClimateOS signals.

Signals are possible inputs to learning, knowledge, evidence, governance, or future runtime routing. A signal is not automatically true, mature, authoritative, or actionable.

## Signal Taxonomy

| Signal Type | Purpose | Possible Source | Lifecycle | Governance |
| --- | --- | --- | --- | --- |
| Reality Signal | Indicates a condition in the world | Observation, event, measurement, field report | Capture, review, evidence routing, archive | Requires provenance and uncertainty review |
| Observation Signal | Records a specific observed condition | Human observation, sensor output, imagery, local report | Capture, freshness check, validation routing | Requires context and review status |
| Knowledge Signal | Suggests reusable knowledge | Paper, official publication, project note, CRP, conversation | Harvest, review, maturity classification | Requires source and relevance review |
| Founder Signal | Expresses Founder intent, direction, concern, or decision | Founder instruction, review, correction | Capture, routing, governance review, archive | High governance relevance; not a substitute for evidence |
| Governance Signal | Indicates a rule, gate, boundary, or responsibility issue | AEP, task record, approval gate, risk review | Route, review, decision, archive | Requires traceable authority |
| Runtime Signal | Indicates future runtime relevance or readiness | Runtime Lens metadata, readiness map, failure mode, freshness trigger | Record, review, defer or route | Planning-only unless implementation is separately authorized |
| Routing Signal | Indicates where a signal should go next | Task index, roadmap, context packet, review note | Classify, route, monitor, close | Requires no silent escalation into execution |

## Signal Purpose

Signals help ClimateOS notice, route, and review information.

They do not by themselves create:

- implementation authority
- evidence authority
- compliance authority
- public claim authority
- automated action authority

## Boundary

This document creates a taxonomy only. It does not implement signal processing, databases, scoring, routing automation, or runtime behavior.
