# Task674 Adapter Concept Versus Implementation Boundary

## Purpose

Clarify what ClimateOS may call an adapter concept and what would become
implementation work requiring a separate Founder Gate.

## Adapter Concept

An adapter concept may describe:

- the future role of a model;
- the type of inputs a model expects;
- the type of outputs a model may provide;
- the context that must accompany outputs;
- the review questions required before reuse;
- licensing and permission issues;
- uncertainty and failure concerns;
- human review responsibilities;
- stop conditions.

An adapter concept is a way to think clearly before building anything.

## Adapter Implementation

Adapter implementation begins when work creates or modifies any technical
mechanism that can move data, call a model, transform output, persist records,
automate review, or connect ClimateOS to a provider.

Implementation includes:

- connector code;
- API client code;
- authentication flow;
- database table or migration;
- runtime schema;
- CLI command;
- MCP tool;
- automation;
- scheduled job;
- model execution script;
- external data retrieval;
- sensor or live source integration;
- deployment configuration.

## Boundary Rule

Task671-680 may name future adapter concerns, but it must not create an adapter.

## Founder Gate Required

Before any future adapter implementation begins, the Founder must approve a
bounded technical work request that names the provider, model, data boundary,
permission status, security controls, private-asset boundary, validation plan,
human review process, and stop condition.

## Current Capability

No adapter implementation is created by this document.
