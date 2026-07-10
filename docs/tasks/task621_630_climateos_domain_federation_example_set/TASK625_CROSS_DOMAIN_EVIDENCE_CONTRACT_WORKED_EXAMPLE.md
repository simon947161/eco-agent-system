# Task625 Cross-Domain Evidence Contract Worked Example

## Purpose

Show a conceptual, non-operational Evidence Contract record using the Task608-
609 field model.

## Status

This is an illustrative Markdown example. It is not JSON, schema, database
design, API payload, runtime contract, or operational Evidence Passport.

## Worked Example

| Field | Example Value |
| --- | --- |
| Evidence ID | `EXAMPLE-EVIDENCE-001` |
| Origin Domain | WaterOS |
| Receiving Domain | BiodiversityOS |
| Claim Type | Possible habitat condition signal |
| Source Type | Human observation |
| Source Status | Raw, human review needed |
| Method Context | Visual observation, no instrument reading |
| Spatial Context | Fictional wetland edge zone |
| Temporal Context | Single seasonal observation |
| Uncertainty | No baseline, no survey, no water-level record |
| Review State | Draft; domain review needed |
| Prohibited Reuse | No scoring, certification, public claim, or model training |
| Cross-Domain Notes | BiodiversityOS should review whether species/habitat observation is needed |

## Interpretation

The contract preserves context while preventing overclaiming. It allows a
receiving domain to understand the evidence without pretending it is validated.

## Validation Needs

Future examples should test:

- conflicting domain interpretations;
- stronger source evidence;
- rejected evidence;
- superseded evidence;
- human review comments.

## Current Capability

No operational Evidence Contract, Evidence Passport runtime, schema, API, or
database is created.
