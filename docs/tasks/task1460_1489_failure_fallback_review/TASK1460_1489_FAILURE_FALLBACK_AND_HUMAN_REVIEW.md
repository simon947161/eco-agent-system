# ClimateOS Task1460-1489 Failure, Fallback And Human Review

Date: 2026-07-12

Status: IMPLEMENTED_FOR_FOUNDER_REVIEW

Baseline: 8aebe4589507d6bc0eaaf163ea218e0ec7cbc376

## Purpose

Govern synthetic missing, stale, invalid, conflicting and recovering sources without operating a live forecast service.

## Principles

- preserve the declared primary source identity;
- fallback never masquerades as the primary source;
- no automatic production failover;
- no eligible source means STOP_REQUIRED;
- research fallback requires explicit human acknowledgement;
- recovery requires new evidence;
- failure, decision and recovery history remain auditable;
- public warnings and safety decisions remain outside authority.

## Boundary

Fixture-only governance. No live source, automatic failover, public warning, model execution, paid service or Task1490 work.
