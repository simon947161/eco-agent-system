# Knowledge Object Model

## Definition

A Knowledge Object is a structured knowledge unit that can be identified,
referenced, versioned, matured, and connected to ClimateOS layers.

## Knowledge Object Types

- CRP
- task documents
- strategy documents
- architecture documents
- research papers
- external standards
- observation reports
- validation reports
- future skill documents

## Suggested Fields

| Field | Purpose |
| --- | --- |
| identifier | Stable reference for the object. |
| title | Human-readable name. |
| source | Origin or provider. |
| creation time | When the object was created. |
| version | Current version or revision. |
| maturity | Concept, Foundation, Prototype, Validated, Operational, or Deprecated. |
| related layers | ClimateOS layers connected to the object. |
| related tasks | Task IDs connected to the object. |
| related evidence | Evidence records or evidence concepts connected to the object. |
| confidence | Conceptual confidence status only. |

## Boundary

This model does not create a database schema, retrieval engine, or automated
knowledge classifier.

