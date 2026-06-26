# Registry Identifier Model

## Purpose

Registry identifiers help Knowledge Objects remain stable across providers and
versions.

## Identifier Principles

- stable enough for references
- human-readable where possible
- provider-independent
- version-aware
- task-aware when appropriate
- not tied to one storage platform

## Example Pattern

```text
KO-<domain>-<layer>-<short-name>-<version>
```

Example:

```text
KO-climateos-knowledge-runtime-v1
```

## Boundary

No identifier generator is implemented.

