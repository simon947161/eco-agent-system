# Founder Gate History Model

## Purpose

Task541-600 hardens Founder Gate records by adding manual decision history fields.

## Added Fields

- `supersedes_gate_id`
- `decision_version`

## Behavior

Founder Gate records remain manually entered. A new gate may reference an earlier gate as superseded. Decision version is calculated per gate trigger to make history easier to review.

## Non-Authority Rule

Founder Gate records do not open a gate automatically, pass a gate automatically, approve architecture, authorize runtime, authorize implementation, authorize deployment, authorize Task601, or replace Founder review.

## Boundary

Founder Gate history is a local recordkeeping aid only. It does not create automated authorization or operational governance.
