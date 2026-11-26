# HEAT–001 | HOME-GPU-01 portable research handoff
**Dated:** 2026-11-26 Australia/Sydney
**Scope:** ClimateOS thermal ecology — two coordinated strategic lines
**Source of truth:** GitHub Issues and pinned PR SHAs; this handoff is an index, NOT a merged scientific or software result.
**Important:** This file lives on a separate HANDOFF branch, not default `main`. It neither merges nor modifies any existing Draft PR.

## 1. Two strategic lines (do not confuse their permissions)
### Track A — authorized bounded computation: P1 SYNTHETIC ENERGY LEDGER
- Founder authorization: https://github.com/simon947161/eco-agent-system/issues/176
- P0 science basis: https://github.com/simon947161/eco-agent-system/issues/173
- P0 scientific audit: Draft PR #174 https://github.com/simon947161/eco-agent-system/pull/174 at `de0b951e5644696e956c20cc03ab848e5742be70` (as checked 2026-11-26; open/draft/unmerged).
- P0-A spatial design scope: https://github.com/simon947161/eco-agent-system/issues/175
- P0-A deliverables: stacked Draft PR #177 https://github.com/simon947161/eco-agent-system/pull/177 at `369ee6b9703fedb54ca4da684920e6c23825d6ca` (as checked 2026-11-26; open/draft/unmerged). **Its PR base is the P0 branch, NOT main.**
- Fixed design links: `docs/tasks/climateos_heat_001/MVTEE_EXPERIMENT_DESIGN.md`, `MVTEE_SPATIAL_LAYOUT_CONCEPT.md`, `MVTEE_BOUNDARY_AND_LEDGERS.md`, `MVTEE_FAILURE_MODES.md`, `MVTEE_ACCEPTANCE_REVIEW_CN.md`, and five SVGs in `figures/` at PR #177 HEAD.
- Model objects: A fictional stable low-/medium-temperature waste-heat source, B one aggregated seasonal-building heat demand, C heat pump and optional thermal tank.
- Synthetic paths: L = A–C 80 m / C–B 40 m; T = A–C 120 m / C–B 180 m (each figure is conceptual single-route trench length, not measured GIS).
- Comparators: R0 existing boiler and R1 local air-source heat pump; require identical hourly useful thermal services and terminal stores, backup and curtailment explicitly counted.
- P1 outputs: deterministic offline synthetic energy / exergy / loss / economy / carbon ledgers; spatial route sensitivity; unit & conservation tests; low COP, long pipe, seasonal mismatch, duplicate edge, negative storage, no-effect layout and sign-flip cases; Chinese Slides-style acceptance. All input values `SYNTHETIC`.
- NO P2, NO real-data, site/regional modeling, CFD, installation, deployment, mergers, or real environmental claims.

### Track B — new bounded architecture inquiry: ARCH–P0
- Scope and tasks: https://github.com/simon947161/eco-agent-system/issues/178
- Research only: 3D Physical Scene Graph, 1D dynamic hydraulic/thermal evolution, candidate OpenModelica/EnergyPlus/QGIS/Blender/OpenFOAM/FMI connections, time/space/interface contracts, fidelity gate, environmental receptor boundaries and validation requirements.
- **No software installation or simulations authorized in Track B**. Future L2/L3 work requires separate Founder approval.

## 2. Repo dependency graph — why main does not show drafts
```
origin/main (verified at design review): 9eb7577e145e76161f9f1cd8509348b19c2904cc
    └─ P0 draft branch (#174): de0b951e5644696e956c20cc03ab848e5742be70
          └─ P0-A design draft branch (#177): 369ee6b9703fedb54ca4da684920e6c23825d6ca

separate handoff branch: handoff/heat-001-home-gpu01-20261126
    └─ this README (index only)
```
Do not infer that main contains P0/P0-A files. Do not merge or rebase #174/#177 merely to make them appear locally. Refresh remote refs because the above is a timestamped snapshot; choose a safe separate P1 working branch only after verifying both current remote heads and draft statuses.

## 3. HOME-GPU-01 startup: read-only verification FIRST
Open PowerShell / Git Bash on HOME-GPU-01 where Git and Codex are available. If repo already exists, **use that clone**; do not overwrite it. In repository root:
```powershell
git status --short --branch
git remote -v
git fetch origin --prune
git branch -r --list "*heat-001*" "*heat*"
git show --no-patch --format=fuller de0b951e5644696e956c20cc03ab848e5742be70
git show --no-patch --format=fuller 369ee6b9703fedb54ca4da684920e6c23825d6ca
git show origin/handoff/heat-001-home-gpu01-20261126:docs/tasks/climateos_heat_001/HOME_GPU01_HANDOFF_20261126.md
```
The first `git status` must be inspected before checkout; **never** `git reset --hard`, `git clean -fd` or discard uncommitted local work. `git fetch` does not merge, but requires valid Git access. If pinned commits are not fetched by branch names, inspect online PRs, then fetch exact branch refs/commits using a user-approved command. A repo absent from GPU01 should be cloned into a **new** path after confirming it is safe. If `git` or Codex is absent, use GitHub browser pages and report the blocker rather than inventing execution.

Quick browser source-of-truth:
- https://github.com/simon947161/eco-agent-system/issues/176
- https://github.com/simon947161/eco-agent-system/issues/178
- https://github.com/simon947161/eco-agent-system/pull/174
- https://github.com/simon947161/eco-agent-system/pull/177
- https://github.com/simon947161/eco-agent-system/blob/handoff/heat-001-home-gpu01-20261126/docs/tasks/climateos_heat_001/HOME_GPU01_HANDOFF_20261126.md

## 4. One starter instruction to paste into Codex on GPU01
> Continue ClimateOS HEAT–001 from GitHub, not from any assumed local chat state. FIRST read this handoff and Issues #176 (approved synthetic P1) and #178 (architecture P0 research only); inspect Draft PRs #174 and #177 and verify their current SHAs, stacked base relationship and files. Run only safe read-only checks initially; identify any uncommitted local work and existing branches. For Track A create a NEW isolated P1 work branch based on the verified P0-A source only if this can be done without disturbing local work. Build deterministic SYNTHETIC A–C–B accounting with R0/R1/L/T as specified by #176 and #177; preserve #175 as design-only. For Track B undertake DOCUMENTATION-ONLY 3D/multiphysics interface investigation per #178; no installations or numerical L2/L3/CFD. Prefer separate branches and Draft PRs; source receipts and tests with exact SHAs, English identifiers, a Chinese Founder Slides-style review and CRP. STOP at review. P2 and real-world data/modeling remain NO-GO.

## 5. Safe continuation gates
- Verify local clone cleanliness before writing, then verify latest remote refs and existing PR state.
- Keep P1 and ARCH-P0 in **separate branches/PRs** with independent output paths; link the same overarching HEAT index.
- No automatic merge/deploy. No secret uploads, private Council files or local machine identifiers. No BOT success claim without positive receiver acknowledgement. GitHub posting is not proof that HOME-GPU-01 pulled work.
- Record command, output SHA, source/permission and test evidence; never claim site benefits from synthetic energy accounting.
- If P1 existing work is already in another PR, stop duplicate implementation, review it and extend the same work only after verifying ownership/state.
- Preserve environmental scientific restrictions: Fraley 18.4 TW unit conversion is arithmetically correct, 46 TW atmospheric storage premise conflicts with observation, 39% is NOT valid global-warming attribution; local heat reuse is a separate falsifiable claim.

## 6. CRP + long-term radar
Knowledge: graph topology is not 3D geometry or fluid mechanics; thermal balances, exergy, spatial losses and environmental recipients must have distinct ledgers.
Idea: one canonical 3D scene & cross-solver interface; model fidelity chosen by decision need, not visual appeal.
Wish: spatially organized human thermal ecology supporting comfort, efficiency and ecosystems.
Reasoning: first L1 synthetic accounting and validation; only then decide whether L2 transient pipe model changes L/T layout ranking; no premature L3 CFD.
Decision: P1 is approved; ARCH-P0 is inquiry-only; P2 NO-GO; PRs #174/#177 remain drafts.
Unresolved: true available source heat and site evidence/licence, appropriate heat-network/CFD tool compatibility, platform resources, actual environmental receptors.
Next: GPU01 inspect remote/local state, produce independently reviewable P1 and architecture packages; return their links/SHA and explicit Founder decisions.
Keywords: HEAT–001, HOME-GPU-01, MVTEE, thermal ecology, CarbonOS, BuildingOS, EcoEngine, 3D scene graph, multiscale coupling, exergy, model fidelity.
