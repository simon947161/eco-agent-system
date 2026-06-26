# Knowledge Adapter Model

## Purpose

The Knowledge Adapter Model explains how providers may connect without changing
ClimateOS core architecture.

## Adapter Principle

```text
Provider
-> Adapter
-> Knowledge Provider Interface
-> Knowledge Runtime
```

ClimateOS should depend on the interface, not the provider platform.

## Adapter Responsibilities

- map provider records into Knowledge Object concepts
- preserve metadata
- preserve citation context
- identify provider capability
- identify import and export boundaries
- report limitations

## Boundary

No adapters are implemented. This document defines the conceptual adapter role
only.

