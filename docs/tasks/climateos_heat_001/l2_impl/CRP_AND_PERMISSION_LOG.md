# CRP / permission and data-handling log — HEAT–001 L2

**Task:** Issue #183. **Host:** HOME-GPU-01. **Date:** 2026-11-27 Australia/Sydney. **Branch:** `codex/heat-001-l2-synthetic-implementation-20261127`.

## Authorization and computation

- Founder authorization is limited to minimal offline SYNTHETIC 1D transient heat–hydraulic implementation after a committed pre-run freeze.
- Gate contract v1.0.1 SHA-256 `60861f0fc5c34e14f7c66feff10b70b7680e61809cbf27e3df9225c4232a9c7b`, gate amendment commit `a351247e92a673dc39a2136822ed8fe3e5a65231`.
- Only standard-library Python 3.14.4 was used. No package manager, installation, network data retrieval, external service, GPU call or software licensing change.
- P1 data inputs were fetched from exact accepted PR #179 SHA and copied byte-for-byte into the isolated implementation fixture folder. Their original source SHAs are recorded in the frozen receipt. P1 was not rewritten, recalculated or altered.
- All modeled demand, route geometry, levels, properties, controls, prices and factors are SYNTHETIC. No Council/private/site/GIS/CRS data, credentials or field observations were read.
- L/T central yearly calculation completed; convergence matrix did not. Work stopped when actual solver runtime projection exceeded the frozen 180 s budget.

## Repository and local workspace safeguards

- No local Git checkout existed at task start; no user repository working tree or uncommitted file was overwritten.
- GitHub work was made only on the isolated implementation branch; no predecessor branch was changed.
- Draft PR is proposed for review only. No merge, production deployment or external outreach was performed.
- Not performed: P2, CFD, real geographic/site modeling, online data collection, installation, main-branch update or automatic next-stage execution.

## Constraints for the next stage

Any faster host or changed convergence design needs Founder authorization. A new resource/solver design must be documented and frozen before additional full-year cases. The current coarse L/T results are not accepted for layout ranking.
