# Knowledge Provider Interface

## Purpose

The Knowledge Provider Interface defines how external or internal knowledge
sources may conceptually connect to the ClimateOS Knowledge Runtime.

## Core Principle

ClimateOS depends on interfaces, not platforms.

Providers may change without requiring ClimateOS architecture to be rewritten.

## Interface Responsibilities

- identify provider type and scope
- describe provider capabilities
- preserve knowledge metadata
- support Knowledge Object mapping
- preserve source and citation context
- define import and export boundaries
- support governance review

## Non-Responsibilities

The interface does not implement:

- provider connectors
- APIs
- synchronization engines
- vector search
- embeddings
- LLM retrieval
- automated reasoning

