# CCZPS-Lite v0.5 Repository Structure Review

## Review Scope

This review documents future cleanup opportunities. Task 40 intentionally does
not move, rename, or delete runtime files.

## Current Strengths

- `cczps_lite/engine/` keeps deterministic runtime modules together
- `cczps_lite/input/` and `cczps_lite/output/` make data flow inspectable
- `cczps_lite/dashboard/` contains a self-contained static presentation layer
- `tests/` provides broad unit and structural regression coverage
- `.github/workflows/` separates tests, Pages deployment, and manual workflows
- numbered documentation directories provide a developing architecture map

## Observed Structure Issues

- root-level and numbered documentation overlap in subject and age
- legacy Batlow score comparison and newer four-context evidence comparison
  use similar names but serve different purposes
- generated outputs and maintained example fixtures share one output directory
- some older validation documents describe historical test counts and runtime
  boundaries that predate v0.5
- runtime documentation is split between `docs/`, `docs/03_RUNTIME_LAYER/`,
  `docs/06_ROADMAP/`, and release documents

## Recommended Future Cleanup

1. Define a documentation ownership and lifecycle policy: current, historical,
   roadmap, template, and release.
2. Add a versioned data-contract directory for input and output schemas.
3. Distinguish generated demonstration fixtures from ephemeral runtime output.
4. Document the legacy `scenario_compare.py` matrix separately from the v0.5
   `scenario_comparison.py` evidence posture runtime.
5. Add a generated-output drift check after contracts stabilize.
6. Review historical documents for explicit version banners rather than
   rewriting history.
7. Consider a dedicated package entry point only in a future runtime task.

## Recommendation

Keep the current repository layout stable for v0.5. Perform any structural
cleanup in a dedicated future task with migration notes, link checks, and a
clear compatibility plan.
