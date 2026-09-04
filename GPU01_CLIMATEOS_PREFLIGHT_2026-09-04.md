# GPU01 ClimateOS Preflight — 2026-09-04

## Repository state

- Repository: `simon947161/eco-agent-system`
- Origin: `https://github.com/simon947161/eco-agent-system.git`
- Branch/HEAD at preflight: `main` / `7c33de4204af9038e23bdda69f393e0e9cf30a1a`
- Status at preflight: clean and aligned with `origin/main`
- Test framework: Python standard-library `unittest` style, discoverable with `python -m unittest discover -s tests`; tests live under `tests/test_*.py`.
- Runtime convention: small Python entry points at repository root call modules under `cczps_lite`; JSON contracts, admitted inputs, deterministic outputs, and Markdown closure/gate records are kept together.

## Required capability audit

| Capability | Present on main | Principal evidence |
|---|---|---|
| Evidence Admission | Yes | `cczps_lite/integration/cooma_evidence_admission.py`, Cooma admission schema/input/output and tests |
| Evidence Passport | Yes | Mittagang historical-characterisation output and broader evidence-passport contracts/docs |
| Run Receipt | Yes | `cczps_lite/output/mittagang_410033_historical_characterisation/run_receipt.json`; audit/run-receipt contract docs |
| Environmental Evidence Object | Contract vocabulary present | ClimateOS v2 architecture and evidence maturity/conclusion schema; must remain evidence-linked in EP-SKILL-001 |
| L0-L4 | Yes | `schemas/climateos_v2/evidence_maturity_and_conclusion.schema.json` and v2 architecture review docs |
| S0-S7 | Yes | same schema/architecture family; current Mittagang baseline is explicitly `S0` |
| Time-Bounded Environmental Answer | Yes | JSON schema plus generated Mittagang answer |
| Cooma evidence | Yes | official-source metadata, public-claim admission, real-data pilot, Cooma/QGIS task packs and tests |
| QGIS/spatial references | Yes | local spatial foundation, terrain/boundary, hydrology and integrated-experience scripts/modules/tests |
| Hydrology near-current state | Bounded blocker only | `ADMISSION_BLOCKED_MISSING_RAW_RESPONSE`; comparability/trend must remain `NOT_COMPARABLE_YET` / `TREND_DEFERRED` |

## CP1 reuse map for EP-SKILL-001

| Site-reading step | Reuse from main | Gap to implement |
|---|---|---|
| Locate | Cooma study scope, source metadata, spatial/QGIS packs | One stable site-reading location object and bounded location narrative |
| Observe | admitted Cooma claims, official-real-data pilot, Mittagang historical characterisation | Normalised observation records with explicit reasoning type |
| Contextualise | regional admission/translation boundary, tree-to-leaf architecture | Deterministic context assembly without inflating evidence scale |
| Compare where permitted | near-current comparability and historical-characterisation modules | A gate that emits comparison only when permitted |
| Identify evidence gaps | existing admission/governance statuses | Consolidated gap list, including hydrology raw-response absence |
| Produce bounded Site Reading | Time-Bounded Environmental Answer contract | Founder-readable site-reading output with reasoning labels |
| Recommend next evidence | existing gate/closure patterns | Ranked, non-authorising next-evidence recommendations |
| Human review | review-loop conventions and hydrology review card PR | Explicit pending-human-review state; never simulate H1-H8 sign-off |
| Passport + receipt | existing evidence passport and run receipt patterns | EP-SKILL-specific deterministic passport and receipt |

## Reasoning and conclusion boundary

EP-SKILL-001 must use only: `OBSERVED`, `KNOWN_FROM_ADMITTED_EVIDENCE`, `DERIVED`, `INFERRED`, `UNKNOWN`, `MISSING_EVIDENCE`, and `PROHIBITED_CONCLUSION`. An inference must identify its basis. `UNKNOWN` and `MISSING_EVIDENCE` are deliverable results. The current hydrology blocker limits water-related conclusions but does not stop the broader Site Reading.

## CP1 decision

`PASS_WITH_BOUNDED_GAPS`. Current `main` contains sufficient admitted Cooma, spatial, governance, passport, and receipt foundations to start the minimal vertical slice from a new branch. No Dell-only asset is assumed. PR #116 is treated as reference material only and is not merged.

## Checkpoint delivery

```text
=== CLIMATEOS CHECKPOINT DELIVERY ===

CHECKPOINT: CP1 preflight + reuse map
STATE: COMPLETE
VERIFIED_WORK: main/origin/HEAD/status, test and runtime conventions, evidence contracts, Cooma/QGIS assets, hydrology boundary, PR #116 reuse boundary
FILES_CHANGED: GPU01_CLIMATEOS_PREFLIGHT_2026-09-04.md; CLIMATEOS_OPEN_PR_DISPOSITION_2026-09-04.md
COMMIT: PENDING with implementation branch
TESTS: Repository inspection only; execution begins at CP3
LIMITATIONS: Dell local-only assets unavailable; near-current hydrology raw response unavailable
NEXT_ACTION: Create agent/ep-skill-001-cooma-site-reading from current main and implement minimal vertical slice
RESUME_POINTER: CP2 minimal engine

=== END DELIVERY ===
```

