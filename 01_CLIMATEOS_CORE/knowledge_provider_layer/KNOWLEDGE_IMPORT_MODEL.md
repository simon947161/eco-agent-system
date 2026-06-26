# Knowledge Import Model

## Purpose

The Knowledge Import Model defines how provider knowledge may conceptually enter
the ClimateOS Knowledge Runtime.

## Import Modes

- Manual Import
- Scheduled Import
- Runtime Import
- Future Event-driven Synchronization

## Import Review

Imported knowledge should preserve:

- source
- provider ID
- citation
- metadata
- version
- context
- maturity status
- governance notes

## Boundary

No import implementation, scheduler, API call, file watcher, or synchronization
engine is created.

