# Radar Trigger Framework

## Purpose

Radar triggers describe why a change signal may need attention. They are
conceptual prompts, not automated alerts.

## Trigger Concepts

| Trigger | Purpose |
| --- | --- |
| Threshold Trigger | A value or condition appears to cross a reviewed boundary |
| Trend Trigger | Repeated observations suggest directional change |
| Relationship Trigger | A relationship appears to strengthen, weaken, or shift |
| Disturbance Trigger | A disturbance event may alter system behaviour |
| Governance Trigger | A change may require human review, accountability, or decision context |

## Review Needs

Each trigger should record source, baseline, comparison, relationship context,
uncertainty, and reviewer notes.

## Limits

No trigger is implemented as a live rule, alert, monitor, threshold engine,
forecast, or automated decision.
