# Task637 Stale And Superseded Evidence Contract Example

## Purpose

Show how time and replacement status can be represented.

## Stale Record Example

| Field | Example Value |
| --- | --- |
| Evidence ID | `EC-STALE-001` |
| Origin Domain | WaterOS |
| Receiving Domain | GovernanceOS |
| Claim Type | Historical water condition context |
| Source Type | Fictional old review note |
| Source Status | Stale |
| Method Context | Prior observation window, no current confirmation |
| Spatial Context | Fictional site boundary |
| Temporal Context | Prior season |
| Uncertainty | Current condition unknown |
| Review State | Stale; refresh needed |
| Prohibited Reuse | No current claim or decision use |
| Cross-Domain Notes | Use only as historical context |

## Superseded Record Example

| Field | Example Value |
| --- | --- |
| Evidence ID | `EC-SUPERSEDED-001` |
| Origin Domain | BiodiversityOS |
| Receiving Domain | GovernanceOS |
| Claim Type | Habitat condition signal |
| Source Type | Fictional earlier field note |
| Source Status | Superseded |
| Method Context | Replaced by later fictional reviewed note |
| Spatial Context | Fictional habitat zone |
| Temporal Context | Earlier observation window |
| Uncertainty | Earlier interpretation no longer current |
| Review State | Superseded; preserve for history |
| Prohibited Reuse | No active claim use |
| Cross-Domain Notes | Link to future replacement record if created |

## Interpretation

Stale means time has weakened the record. Superseded means another record has
replaced it. Both should remain traceable.

## Validation Requirement

Future examples should test how stale and superseded records appear in review
summaries without becoming current evidence.
