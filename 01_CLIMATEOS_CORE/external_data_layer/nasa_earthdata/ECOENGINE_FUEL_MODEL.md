# EcoEngine Fuel Model

## Purpose

This document defines how selected NASA-derived inputs may be routed to
EcoEngine in future systems.

## Concept

ClimateOS supplies structured observation inputs.
EcoEngine performs computation.
ClimateOS receives computation outputs.

## Future Flow

```text
NASA Observation Resource
-> ClimateOS Observation Input
-> EcoEngine Computation Input
-> EcoEngine Computation Output
-> ClimateOS Evidence or Validation Context
```

## Requirements For Future Routing

Future routing should preserve:

- Source provenance
- Time and location context
- Units
- Dataset limitations
- ClimateOS layer mapping
- Calculation transparency

## Boundary

No formulas, computation, routing code, or EcoEngine modification is included.
