# Integration System Map

## Purpose

This map shows how the Integration Layer connects ClimateOS and EcoEngine.

## Visual Architecture

```text
Observation
-> Relationship
-> Radar
-> Evidence
-> Validation
-> ClimateOS Runtime
-> Engine Call
-> EcoEngine
```

## Return Path

```text
EcoEngine
-> Computation Result
-> Evidence Candidate
-> Evidence
-> Validation
-> Governance
```

## Major Components

```text
Integration Layer
├─ System Responsibilities
├─ Input Output Model
├─ Computation Request Types
├─ Computation Response Types
├─ Evidence Integration
├─ Validation Integration
├─ CCZPS Alignment
├─ ESG++ Alignment
└─ Future Engine Support
```

## Boundary

This is an architecture document only. No runtime calls, APIs, simulations, or
engine integrations are implemented.
