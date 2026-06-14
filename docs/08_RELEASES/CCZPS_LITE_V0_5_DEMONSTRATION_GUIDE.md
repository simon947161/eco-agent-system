# CCZPS-Lite v0.5 Demonstration Guide

## Demonstration Boundary

This demonstration uses committed local outputs. It requires no API
credentials, external service, live NASA POWER request, GIS/DEM download,
simulation, or LLM call.

The expected GitHub Pages location, when Pages is enabled for the repository, is:

`https://simon947161.github.io/eco-agent-system/`

The repository-local dashboard is `cczps_lite/dashboard/index.html`. GitHub
Pages stages a self-contained copy through
`.github/workflows/deploy-dashboard-pages.yml`.

## Recommended Demonstration Sequence

1. Open the dashboard and state that it is a static view of generated outputs.
2. Introduce Batlow, Kunlun, Iraq, and Baiyangdian-Xiong'an as demonstration
   contexts, not approved projects.
3. Show meteorology evidence and trend readings.
4. Show planning hypotheses and their failure conditions.
5. Show evidence traceability and supporting local artifact IDs.
6. Show internal governance support and unresolved gaps.
7. Show scenario comparison as evidence coverage and uncertainty groups.
8. Finish with the mandatory human-review and approval boundary.

## Reading Scenario Outputs

Use `cczps_lite/output/scenario_report.md` and
`cczps_lite/output/comparison_matrix.csv` to explain the legacy deterministic
scenario chain. Values are indicative and must not be presented as scientific
calibration, a preferred scenario, or implementation authority.

## Reading Planning Hypotheses

Open:

- `cczps_lite/output/planning_hypotheses.json`
- `cczps_lite/output/planning_hypotheses.md`

Explain the problem statement, planning assumption, validation indicators, and
failure conditions. A hypothesis is a testable concept, not a recommendation.

## Reading Evidence Traceability

Open:

- `cczps_lite/output/evidence_traceability.json`
- `cczps_lite/output/evidence_traceability.md`

Use `trace_id`, `artifact_id`, `supporting_evidence_ids`, `evidence_source`,
`review_status`, and `limitations` to show how outputs link back to local
artifacts. Traceability does not make evidence stronger by itself.

## Reading Governance Decision Records

Open:

- `cczps_lite/output/governance_decision_records.json`
- `cczps_lite/output/governance_decision_records.md`

Explain that `requires_further_review` is an internal support status. It is not
an approval, professional conclusion, or implementation decision. Show the
unresolved gaps, risks, and required human actions.

## Reading Scenario Comparison

Open:

- `cczps_lite/output/scenario_comparison.json`
- `cczps_lite/output/scenario_comparison.md`

Compare evidence strength, uncertainty, risk, traceability, spatial validation,
hypothesis, expert review, governance, and approval-support status. Do not
describe evidence groups as rankings, winners, or preferred options.

## Explaining `not_ready_for_approval`

`not_ready_for_approval` means the local evidence and review package is
insufficient for an approval process. It does not mean a scenario is approved,
rejected, technically feasible, legally compliant, or professionally endorsed.

## Explaining Human Review

`human_review_required: true` and `professional_review_required: true` are
release boundaries, not optional UI labels. Qualified reviewers must assess
local evidence, methods, uncertainty, law, engineering, environmental effects,
community context, and other relevant requirements outside this demonstrator.

## Offline Verification

From the repository root:

```bash
python -m unittest discover
python cczps_lite/engine/evidence_traceability.py
python cczps_lite/engine/governance_decision_support.py
python cczps_lite/engine/scenario_comparison.py
```

The committed outputs can also be inspected without regenerating them.

## Human-Readable Dashboard

From the repository root, start a simple local static server:

```bash
python -m http.server 8000
```

Then open:

`http://localhost:8000/cczps_lite/dashboard/`

Begin with the plain-language sections near the top of the page:

1. scenario cards;
2. evidence summaries;
3. planning hypothesis summaries;
4. internal review status;
5. transparent scenario comparison;
6. capability boundaries; and
7. next human review actions.

For a non-technical audience, explain that each paragraph translates an
existing local JSON field. The dashboard does not create new environmental
analysis. Use the technical sections below the divider only when someone wants
to inspect the underlying runtime detail.

Keep the visible safety statement in view when presenting. Every scenario
remains demonstration-only, requires human and professional review, and is not
ready for approval.
