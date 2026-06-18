# Repository Maturity

This document separates repository structure from implemented capability.
Creating a folder or template does not mean an agent, subsystem, or scientific
method exists.

## Maturity Levels

| Level | Meaning |
| --- | --- |
| Scaffold | Directory or placeholder documentation exists |
| Documented | Purpose, scope, fields, evidence, validation, and limits are specified |
| Implemented | Reviewable code or deterministic builder exists |
| Validated | Tests and declared-scope reviews are complete |
| Operational | Versioned use, ownership, maintenance, and monitoring are approved |

## Current Repository Reading

| Area | Current maturity | Evidence |
| --- | --- | --- |
| Project Control Layer | Documented baseline | Included in ClimateOS Repository OS v1.0 |
| Master Directory Layer | Scaffold baseline | Fifteen-part documentation scaffold included in v1.0 |
| Batch Queue Layer | Documented baseline | Dashboard, status, rules, dependencies, pipeline, and templates included in v1.0 |
| Agent Standard Layer | Documented baseline | Standard, lifecycle, checklist, catalog, and templates included in v1.0 |
| CCZPS-Lite core | Implemented with automated tests | Existing deterministic runtimes, outputs, and repository test suite |
| Consolidated summary packs | Implemented with automated tests | Existing Scenario Summary and Evidence Review builders |
| CarbonOS | Scaffold | Directories and README placeholders only |
| EnergyOS | Scaffold | Directories and README placeholders only |
| WaterOS | Scaffold | Directories and README placeholders only |
| LandOS | Scaffold | Directories and README placeholders only |
| BiodiversityOS | Scaffold | Directories and README placeholders only |
| ParkOS | Scaffold | Directories and README placeholders only |
| ESGOS | Scaffold | Directories and README placeholders only |
| GISOS | Scaffold / planning only | Documentation only; no GIS or DEM runtime |
| ScenarioOS | Scaffold | Scenario category directories only |
| ValidationOS | Scaffold | Workflow directories only; existing CCZPS-Lite validation remains separate |
| GovernanceOS | Scaffold | Governance layer directories only; existing CCZPS-Lite governance remains separate |
| Business Layer | Planning only | No payments, transactions, wallets, or marketplace runtime |
| Demonstrations | Scaffold | Placeholder cases only |

## Maturity Rules

- Do not infer `Implemented` from a README or directory.
- Do not infer `Validated` from passing unit tests alone when professional
  review is required.
- Do not infer `Operational` from a demonstration.
- Every maturity increase requires a task, evidence, tests, review, and a
  recorded decision.
- Subsystems must reuse ClimateOS Core evidence and governance standards.
