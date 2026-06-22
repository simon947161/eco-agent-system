# Forecast Confidence Model

## Purpose

Forecast confidence should describe the trustworthiness of a Forecast Candidate
after review, not before.

## Confidence Inputs

- data quality
- provider reliability
- model suitability
- time horizon suitability
- uncertainty range
- comparison with other providers
- comparison with observed reality
- bias review
- domain expert review
- governance relevance

## Suggested Statuses

| Status | Meaning |
| --- | --- |
| Unreviewed | Forecast Candidate has not been validated. |
| Low Confidence | Major uncertainty, poor fit, or weak evidence. |
| Moderate Confidence | Some validation support exists, but uncertainty remains. |
| High Confidence | Strong validation support exists for the stated scope. |
| Invalidated | Later evidence contradicts the forecast or assumptions. |

## Boundary

Confidence status does not create automated decisions.

