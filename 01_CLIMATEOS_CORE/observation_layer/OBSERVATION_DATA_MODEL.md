# Observation Data Model

## Purpose

This conceptual data model defines fields for future observation records. It is
not a database schema or runtime contract.

## Core Fields

| Field | Purpose |
| --- | --- |
| Date | Calendar date of the observation |
| Time | Local time of the observation |
| Location | Site name or place reference |
| Temperature | Observed or referenced temperature context |
| Rainfall | Observed or referenced rainfall context |
| Wind | Wind condition, direction, or qualitative note |
| Vegetation Notes | Plant condition, flowering, dryness, recovery, or stress |
| Community Notes | Human observations, local context, or lived experience |
| Photo Reference | Link or identifier for related photo evidence |
| Evidence Reference | Link or identifier for future reviewed evidence |

## Additional Review Fields

| Field | Purpose |
| --- | --- |
| Observer | Person or role recording the observation |
| Source Type | Satellite, weather, hydrology, ecology, or community observation |
| Confidence Note | Plain-language note about uncertainty |
| Review Status | Draft, reviewed, needs review, or archived |
| Version | Record version or change history reference |

## Limits

Fields define record structure only. They do not create a database, API,
validation process, or automated interpretation.
