# Task623 Water Land Biodiversity Example

## Purpose

Provide a fictional cross-domain example involving WaterOS, LandOS, and
BiodiversityOS.

## Fictional Scenario

A community observation notes that a small wetland edge appears drier than in
previous seasons, nearby vegetation looks stressed, and bird activity appears
lower during morning walks.

## Observations

- Wetland edge dryness is reported by a human observer.
- Vegetation stress is visually observed, not measured.
- Bird activity is an informal community signal.

## Assumptions

- The observer is familiar with the site.
- No instrumented water-level, soil-moisture, or biodiversity survey data is
  available in this example.
- The record is useful as a signal, not as proof.

## Domain Routing

| Domain | Role |
| --- | --- |
| WaterOS | Check whether hydrology or water-level questions are relevant. |
| LandOS | Check soil, land-use, and disturbance context. |
| BiodiversityOS | Check habitat and species-signal relevance. |
| GovernanceOS | Track review state and action limitations. |

## Interpretation

The record is an early cross-domain signal. It should trigger evidence
questions, not conclusions. The main value is identifying which domains need
review and what evidence is missing.

## Uncertainty

- No baseline data is attached.
- Observation may be seasonal or weather-related.
- Species activity may vary by time of day.
- Land-use or maintenance context is unknown.

## Human Review Requirement

Human review should determine whether this signal should become:

- a watch-list item;
- a request for field observation;
- a rejected weak signal;
- a Founder Gate issue if it affects sensitive land or biodiversity claims.

## Current Capability

No monitoring, sensors, model calls, hydrology analysis, biodiversity scoring,
or automated escalation is created.
