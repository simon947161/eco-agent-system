# ClimateOS Agent Standard

This is the official documentation standard for future ClimateOS repository
agents. It defines a reviewable blueprint; it does not implement executable
agents or scientific validation.

## Agent Name

Use a clear, unique name that identifies the domain and responsibility. Avoid
names that imply approval, certification, autonomy, or authority the agent
does not have.

## Purpose

Explain the narrow problem the agent supports, who uses it, and who reviews its
outputs. State why a separate agent is justified.

## Scope

Define included responsibilities and explicit boundaries. Keep the scope small
enough for independent testing, maintenance, and review.

## Inputs

List required and optional inputs, formats, units, identifiers, provenance,
allowed values, missing-data behavior, and ownership.

## Outputs

List human-readable and machine-readable outputs. Explain what each output
means and what it must not be interpreted as.

## Evidence Requirements

State required evidence sources, traceability, confidence, uncertainty,
currency, quality, licensing, and professional-review needs.

## Runtime Fields

Define stable field names, types, allowed statuses, defaults, version fields,
and compatibility expectations. Documentation-only agents may state that no
runtime fields exist yet.

## Assumptions

Record every material assumption, its source, owner, status, uncertainty, and
conditions that would invalidate it.

## Validation Rules

Describe deterministic checks, invalid-input handling, expected tests,
professional validation, and conditions that require further review.

## Governance Notes

State human decision boundaries, approval limits, resource ownership, cost
controls, privacy, security, audit, retention, and stakeholder responsibilities.

## Limitations

List missing capabilities and evidence. Explicitly state whether the agent does
not provide scientific confirmation, professional certification, engineering
or regulatory conclusions, ranking, recommendation, approval, or autonomous
decisions.

## Example Scenario

Provide one small demonstration with labelled inputs and expected outputs. The
example must preserve uncertainty and must not be presented as validated
professional advice.

## Future Development

List possible incremental tasks and their dependencies. Do not describe future
work as existing capability.

## Standard Principles

- Prefer one narrow responsibility per agent.
- Reuse ClimateOS Core evidence, validation, governance, and report concepts.
- Keep local and deterministic behavior unless a later task explicitly
  approves external integrations.
- Preserve source statuses; do not silently upgrade evidence or readiness.
- Require human-readable outputs and clear limitations.
- Add executable functionality only through a separate approved task.
