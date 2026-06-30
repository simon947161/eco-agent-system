# Example Scope And Limits

## Purpose

This document defines what the Task95 examples include and exclude.

## In Scope

Task95 includes conceptual examples for:

- validation sessions
- validation input sets
- validation output sets
- Validation Packs
- Review Packs
- Recommendation Packs
- benchmark application
- future domain runtime inheritance

## Out Of Scope

Task95 excludes:

- executable examples
- scripts
- APIs
- data schemas for implementation
- automated validation
- scoring engines
- workflow engines
- domain runtime creation
- production decisions

## Conceptual Boundaries

The examples are written as structured documentation. They are intended to help
future contributors see how the Foundation pieces fit together.

They do not define software behavior.

## Domain Runtime Preparation

The examples may mention CarbonOS, WaterOS, EnergyOS, and BuildingOS as future
inheritance targets.

Those mentions are contextual only. They do not start domain runtime
development.

## Relationship To Task100

Task95 supports Task100 by showing that the runtime interface, pack model, IO
model, and benchmark library can be understood as one coherent Foundation
pattern.

Task100 remains the Foundation Graduation milestone.

## Task101+ Parking

Possible future work after Task100:

- executable example templates
- domain-specific validation scenarios
- reusable example fixtures
- validation pack generators

