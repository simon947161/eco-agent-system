# CCZPS-Lite — Batlow Runtime Demonstrator

CCZPS-Lite is a small, file-based demonstrator for comparing possible environmental resilience pathways. It supports the EcoEngine Runtime Core idea that scenario assumptions should move through evidence, runtime interpretation, reasoning, and governance review before being treated as decision-support output.

Batlow, NSW is used as the first demonstrator because it provides a clear rural resilience context: orchard water security, energy continuity, ecological recovery, bushfire resilience, and community safety can be compared without building a large platform.

## Runtime Flow

```text
Scenario
    ↓
Evidence Profile
    ↓
Runtime Fields
    ↓
Runtime Reasoning
    ↓
Evidence-Aware Governance Output
```

## How to Run

From the repository root:

```bash
python cczps_lite/engine/scenario_compare.py
```

The script uses only the Python standard library. It does not call weather APIs, GIS services, databases, machine learning systems, or world models.

## Input Files

- `input/location_profile.json` describes the Batlow location profile.
- `input/scenario_options.json` describes three indicative future pathways.
- `input/evidence_profile.json` describes the first evidence layer for water, energy, ecology, and fire assumptions.

## Generated Output Files

- `output/comparison_matrix.csv` contains scenario scores, runtime fields, evidence fields, and recommendation classes.
- `output/scenario_report.md` provides a readable scenario comparison report.
- `output/governance_summary.md` provides a short governance-oriented summary, including evidence assessment.

## Methodology Boundary

This prototype is not a final environmental model, regulatory-grade planning tool, financial assessment, or scientific simulation. It is a methodology demonstrator using indicative values only.

Low evidence means higher uncertainty and triggers human review. High evidence means comparatively higher confidence, but it does not remove the need for local consultation, professional judgement, or site-specific validation.

## Connection to CCZPS 2.0 and EcoEngine

CCZPS compares possible futures. EcoEngine runtime logic helps describe how scenario assumptions translate into operational signals. This CCZPS-Lite version introduces the first evidence layer so that governance outputs can show where assumptions come from, where uncertainty is highest, and which pathways require human review.