"""Run the CCZPS-Lite Batlow scenario comparison engine."""

from __future__ import annotations

import csv
import json
import sys
from pathlib import Path

ENGINE_DIR = Path(__file__).resolve().parent
PROJECT_DIR = ENGINE_DIR.parent
REPO_ROOT = PROJECT_DIR.parent
if str(ENGINE_DIR) not in sys.path:
    sys.path.insert(0, str(ENGINE_DIR))

from differential_field import derive_differential_field  # noqa: E402
from evidence_layer import (  # noqa: E402
    derive_evidence_strength,
    derive_human_review_required,
    derive_source_basis,
    derive_uncertainty_notes,
)
from runtime_fields import derive_runtime_fields  # noqa: E402
from runtime_reasoning import derive_runtime_reasoning  # noqa: E402
from scoring_rules import (  # noqa: E402
    calculate_governance_score,
    calculate_resilience_score,
    calculate_risk_adjusted_score,
    classify_recommendation,
)

INPUT_DIR = PROJECT_DIR / "input"
OUTPUT_DIR = PROJECT_DIR / "output"
SCENARIO_EVIDENCE_PATHWAYS = {
    "water_priority": ("water",),
    "energy_resilience": ("energy",),
    "ecology_fire_buffer_priority": ("ecology", "fire"),
}
CSV_FIELDS = [
    "scenario_id",
    "scenario_name",
    "scenario_type",
    "water_security",
    "energy_resilience",
    "ecological_resilience",
    "fire_resilience",
    "community_acceptance",
    "investment_feasibility",
    "implementation_complexity",
    "validation_need",
    "risk_index",
    "water_balance_signal",
    "ecological_signal",
    "evaporation_pressure",
    "confidence_level",
    "validation_required",
    "runtime_reasoning",
    "water_gradient",
    "water_gradient_class",
    "heat_gradient",
    "heat_gradient_class",
    "vegetation_gradient",
    "vegetation_gradient_class",
    "fire_gradient",
    "fire_gradient_class",
    "differential_status",
    "differential_summary",
    "reference_record_count",
    "evidence_strength",
    "source_basis",
    "uncertainty_notes",
    "human_review_required",
    "resilience_score",
    "governance_score",
    "risk_adjusted_score",
    "recommendation_class",
]


def load_json(path: Path) -> dict:
    """Read a JSON file using UTF-8 encoding."""
    with path.open("r", encoding="utf-8") as file_obj:
        return json.load(file_obj)


def evidence_for_scenario(scenario: dict, evidence_profile: dict) -> dict:
    """Return relevant evidence records for a scenario type."""
    evidence = evidence_profile.get("evidence", {})
    pathway_keys = SCENARIO_EVIDENCE_PATHWAYS.get(scenario.get("scenario_type"), ())
    return {key: evidence[key] for key in pathway_keys if key in evidence}


def build_comparison_rows(
    scenarios: list[dict],
    evidence_profile: dict,
    context_records: list[dict],
) -> list[dict]:
    """Calculate runtime, differential, evidence, and scoring fields."""
    rows = []
    for scenario in scenarios:
        scores = scenario.get("scores", {})
        runtime = derive_runtime_fields(scores)
        differential = derive_differential_field(scores, context_records)
        scenario_evidence = evidence_for_scenario(scenario, evidence_profile)
        risk_adjusted_score = calculate_risk_adjusted_score(scores)
        row = {
            "scenario_id": scenario.get("scenario_id", ""),
            "scenario_name": scenario.get("scenario_name", ""),
            "scenario_type": scenario.get("scenario_type", ""),
            **scores,
            **runtime,
            "runtime_reasoning": derive_runtime_reasoning(scenario, runtime),
            **differential,
            "evidence_strength": derive_evidence_strength(scenario_evidence),
            "source_basis": derive_source_basis(scenario_evidence),
            "uncertainty_notes": derive_uncertainty_notes(scenario_evidence),
            "human_review_required": derive_human_review_required(scenario_evidence),
            "resilience_score": calculate_resilience_score(scores),
            "governance_score": calculate_governance_score(scores),
            "risk_adjusted_score": risk_adjusted_score,
            "recommendation_class": classify_recommendation(risk_adjusted_score),
        }
        rows.append(row)
    return rows


def write_comparison_csv(rows: list[dict]) -> None:
    """Write the comparison matrix CSV."""
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    with (OUTPUT_DIR / "comparison_matrix.csv").open("w", encoding="utf-8", newline="") as file_obj:
        writer = csv.DictWriter(file_obj, fieldnames=CSV_FIELDS)
        writer.writeheader()
        writer.writerows(rows)


def _format_list(values: list[str]) -> str:
    return "\n".join(f"- {value}" for value in values)


def write_scenario_report(location: dict, scenarios: list[dict], rows: list[dict]) -> None:
    """Write the detailed scenario Markdown report."""
    row_by_id = {row["scenario_id"]: row for row in rows}
    sections = [
        "# CCZPS-Lite v0.4 — Batlow Scenario Report",
        "",
        "This is a methodology demonstrator using indicative values only.",
        "It is not a final planning, engineering, financial, or regulatory assessment.",
        "",
        "## Location Profile",
        "",
        f"- Location: {location.get('location_name')}",
        f"- Location ID: {location.get('location_id')}",
        f"- Region type: {location.get('region_type')}",
        f"- Climate regime: {location.get('climate_regime')}",
        "- Key climate risks:",
        _format_list(location.get("key_climate_risks", [])),
        "",
        "## Scenario Comparison Summary",
        "",
        "| Scenario | Risk-adjusted score | Differential status | Evidence strength | Source basis | Human review required | Recommendation |",
        "| --- | ---: | --- | --- | --- | --- | --- |",
    ]

    for row in rows:
        sections.append(
            "| {scenario_name} | {risk_adjusted_score} | {differential_status} | "
            "{evidence_strength} | {source_basis} | {human_review_required} | "
            "{recommendation_class} |".format(**row)
        )

    scenario_headings = [
        "## Scenario A: Water Priority",
        "## Scenario B: Energy Resilience",
        "## Scenario C: Ecology / Fire Buffer Priority",
    ]
    for heading, scenario in zip(scenario_headings, scenarios):
        row = row_by_id[scenario["scenario_id"]]
        sections.extend(
            [
                "",
                heading,
                "",
                scenario.get("description", ""),
                "",
                "### Interventions",
                _format_list(scenario.get("interventions", [])),
                "",
                "### Runtime and Evidence Fields",
                "",
                f"- Runtime reasoning: {row['runtime_reasoning']}",
                f"- Risk index: {row['risk_index']}",
                f"- Confidence level: {row['confidence_level']}",
                f"- Validation required: {row['validation_required']}",
                f"- Evidence strength: {row['evidence_strength']}",
                f"- Source basis: {row['source_basis']}",
                f"- Uncertainty notes: {row['uncertainty_notes']}",
                f"- Human review required: {row['human_review_required']}",
                "",
                "### Differential Field Runtime",
                "",
                f"- Differential status: {row['differential_status']}",
                f"- Water gradient: {row['water_gradient']} ({row['water_gradient_class']})",
                f"- Heat gradient: {row['heat_gradient']} ({row['heat_gradient_class']})",
                f"- Vegetation gradient: {row['vegetation_gradient']} ({row['vegetation_gradient_class']})",
                f"- Fire gradient: {row['fire_gradient']} ({row['fire_gradient_class']})",
                f"- Differential summary: {row['differential_summary']}",
                f"- Reference record count: {row['reference_record_count']}",
            ]
        )

    sections.extend(
        [
            "",
            "## Notes on Confidence and Validation",
            "",
            "Low evidence indicates higher uncertainty and requires human review before decisions are advanced.",
            "High evidence indicates comparatively higher confidence, but it does not remove the need for local consultation, professional judgement, or site-specific validation.",
            "Differential field gradients are indicative comparisons against representative context records, not validated field measurements.",
            "",
            "## Methodology Boundary",
            "",
            "CCZPS-Lite v0.4 uses local JSON inputs, transparent rules, and generated text outputs only.",
            "It does not connect to weather APIs, GIS services, databases, machine learning models, or world models.",
        ]
    )
    (OUTPUT_DIR / "scenario_report.md").write_text("\n".join(sections) + "\n", encoding="utf-8")


def _rank_value(strength: str) -> int:
    return {"Low": 1, "Medium": 2, "High": 3}.get(strength, 0)


def _scenario_metric_text(row: dict, metric: str, class_metric: str | None = None) -> str:
    class_text = f" ({row[class_metric]})" if class_metric else ""
    return f"{row['scenario_name']} ({row[metric]}{class_text})"


def write_governance_summary(rows: list[dict]) -> None:
    """Write the governance-oriented Markdown summary."""
    highest_ranked = max(rows, key=lambda row: row["risk_adjusted_score"])
    strongest = max(rows, key=lambda row: _rank_value(row["evidence_strength"]))
    weakest = min(rows, key=lambda row: _rank_value(row["evidence_strength"]))
    highest_uncertainty = max(rows, key=lambda row: (row["human_review_required"], row["validation_need"]))
    human_review_rows = [row for row in rows if row["human_review_required"]]
    human_review_text = ", ".join(row["scenario_name"] for row in human_review_rows) or "None flagged by the current low-evidence rule"
    strongest_water = max(rows, key=lambda row: row["water_gradient"])
    highest_heat = max(rows, key=lambda row: row["heat_gradient"])
    strongest_vegetation = max(rows, key=lambda row: row["vegetation_gradient"])
    highest_fire = max(rows, key=lambda row: row["fire_gradient"])

    lines = [
        "# Governance Summary",
        "",
        "## Recommended Reading of Results",
        "",
        "The result indicates a preliminary priority for further review.",
        "Final selection requires local consultation, data validation, and governance assessment.",
        "",
        "## Highest-Ranked Pathway",
        "",
        f"- {highest_ranked['scenario_name']} has the highest indicative risk-adjusted score ({highest_ranked['risk_adjusted_score']}).",
        f"- Recommendation class: {highest_ranked['recommendation_class']}.",
        "",
        "## Key Trade-Offs",
        "",
        "- Water-focused action improves drought and orchard resilience but still requires hydrological validation.",
        "- Energy-focused action supports emergency continuity but currently relies on concept-level evidence.",
        "- Ecology and fire-buffer action has strong fire relevance but requires site-specific ecological and implementation review.",
        "",
        "## Validation Needs",
        "",
        "- Treat all scores as indicative demonstrator values.",
        "- Validate assumptions with local data, professional review, and community consultation before implementation.",
        "",
        "## Evidence Assessment",
        "",
        f"- Strongest evidence pathway: {strongest['scenario_name']} ({strongest['evidence_strength']}; {strongest['source_basis']}).",
        f"- Weakest evidence pathway: {weakest['scenario_name']} ({weakest['evidence_strength']}; {weakest['source_basis']}).",
        f"- Highest uncertainty pathway: {highest_uncertainty['scenario_name']} ({highest_uncertainty['uncertainty_notes']}).",
        f"- Scenarios requiring human review: {human_review_text}.",
        "",
        "## Differential Field Reading",
        "",
        "These gradients compare scenario scores with indicative representative Batlow context records only.",
        f"- Strongest water advantage: {_scenario_metric_text(strongest_water, 'water_gradient', 'water_gradient_class')}.",
        f"- Highest heat pressure: {_scenario_metric_text(highest_heat, 'heat_gradient', 'heat_gradient_class')}.",
        f"- Strongest vegetation buffer: {_scenario_metric_text(strongest_vegetation, 'vegetation_gradient', 'vegetation_gradient_class')}.",
        f"- Highest fire exposure: {_scenario_metric_text(highest_fire, 'fire_gradient', 'fire_gradient_class')}.",
        "",
        "## Suggested Next Step",
        "",
        "Use the comparison as an agenda for human review: confirm evidence quality, test local assumptions, and decide which pathway should be refined first.",
    ]
    (OUTPUT_DIR / "governance_summary.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    """Load inputs, calculate scenario fields, and write outputs."""
    location = load_json(INPUT_DIR / "location_profile.json")
    scenario_options = load_json(INPUT_DIR / "scenario_options.json")
    evidence_profile = load_json(INPUT_DIR / "evidence_profile.json")
    differential_context = load_json(INPUT_DIR / "differential_context.json")
    scenarios = scenario_options.get("scenarios", [])
    context_records = differential_context.get("records", [])
    rows = build_comparison_rows(scenarios, evidence_profile, context_records)
    write_comparison_csv(rows)
    write_scenario_report(location, scenarios, rows)
    write_governance_summary(rows)
    print("Generated CCZPS-Lite comparison outputs in cczps_lite/output")


if __name__ == "__main__":
    main()
