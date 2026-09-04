# ClimateOS Open PR Disposition — 2026-09-04

Read-only review against `main` at `7c33de4204af9038e23bdda69f393e0e9cf30a1a`. GitHub reported ten open PRs. No PR state was changed, and no merge/close action was taken.

| PR | Title | Divergence observed | Recommendation | Rationale / next gate |
|---:|---|---|---|---|
| 116 | Planner Cycle Architecture Mapping | 5 commits ahead, 3 behind; five new architecture documents | `EXTRACT_UNIQUE_CONTENT` | Founder-approved Option A direction is useful, but implement EP-SKILL-001 from latest main. Reuse the contract/reuse matrices selectively after reconciling them with current v2 architecture. Do not silently merge. |
| 115 | Hydrology Professional Review Card | 1 ahead, 3 behind; one 518-line review card | `HOLD_FOR_HUMAN_REVIEW` | Preserve the professional gate. Do not simulate H1-H8 signatures and do not block non-hydrology Site Reading work. |
| 114 | GGG/GEGG commercial and interoperability set | 59 ahead, 3 behind; 75 files | `ROUTE_TO_OTHER_REPOSITORY` | Route to `simon947161/gegg-company-foundation`; it is outside the ClimateOS scientific mainline. |
| 109 | ClimateOS v2 architecture review ACTP | 2 ahead, 8 behind; two context/harvest documents | `EXTRACT_UNIQUE_CONTENT` | Extract any CRP/ACTP decisions not represented in current `docs/architecture/climateos_v2_review`; then archive the stale PR through a separate human-approved action. |
| 104 | Mission Runtime Phase A | 16 ahead, 23 behind; schemas, fixtures and governance docs | `ROUTE_TO_OTHER_REPOSITORY` | Route to `project-runtime-initiative`; do not use a cleanup merge into ClimateOS. |
| 102 | Task2051-2060 post-merge ACTP | 1 ahead, 23 behind; one context packet | `SUPERSEDE_WITH_CURRENT_MAIN_WORK` | Main already contains the active Cooma/QGIS continuation lineage. Preserve only any missing historical note before closing later. |
| 100 | Earth System ontology and driver registry | 3 ahead, 53 behind; two architecture docs and one schema | `EXTRACT_UNIQUE_CONTENT` | Potentially valuable, but operationalise only the subset needed by a real tree-to-leaf reasoning chain; avoid merging a detached ontology wholesale. |
| 90 | Integrity covenant / Build Week | 36 ahead, 68 behind; 16 files | `EXTRACT_UNIQUE_CONTENT` | Extract the enduring integrity covenant if absent; Build Week submission/video artifacts should not be merged as current scientific mainline state. |
| 61 | External-model observation foundation | 332 ahead, 234 behind; 1,531 files | `EXTRACT_UNIQUE_CONTENT` | Extremely divergent historical tree. Identify narrowly unique external-model observation contracts; never merge the full branch into current main. |
| 50 | Hybrid weather runtime preflight | 174+ historical commits ahead and deeply behind; large legacy tree | `SUPERSEDE_WITH_CURRENT_MAIN_WORK` | Current main has later model-assurance, Cooma, and runtime work. Extract only a demonstrably missing preflight constraint before archival. |

## Safe action sequence

1. Keep #115 open for genuine professional review.
2. Build EP-SKILL-001 from current `main`, using #116 only as reference.
3. Open focused extraction PRs for #109/#100/#90/#61 only when a line-by-line uniqueness check proves value.
4. Route #104 and #114 to their named repositories.
5. Reassess #102/#50 for archival only after confirming no unique record remains.

This matrix is a recommendation record, not authorization to merge, close, sign, or transfer any PR.

