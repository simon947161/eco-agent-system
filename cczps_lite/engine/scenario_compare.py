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


def build_comparison_rows(scenarios: list[dict], evidence_profile: dict) -> list[dict]:
    """Calculate runtime, evidence, and scoring fields for each scenario."""
    rows = []
    for scenario in scenarios:
        scores = scenario.get("scores", {})
        runtime = derive_runtime_fields(scores)
        scenario_evidence = evidence_for_scenario(scenario, evidence_profile)
        risk_adjusted_score = calculate_risk_adjusted_score(scores)
        row = {
            "scenario_id": scenario.get("scenario_id", ""),
            "scenario_name": scenario.get("scenario_name", ""),
            "scenario_type": scenario.get("scenario_type", ""),
            **scores,
            **runtime,
            "runtime_reasoning": derive_runtime_reasoning(scenario, runtime),
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
        "| Scenario | Risk-adjusted score | Evidence strength | Source basis | Human review required | Recommendation |",
        "| --- | ---: | --- | --- | --- | --- |",
    ]

    for row in rows:
        sections.append(
            "| {scenario_name} | {risk_adjusted_score} | {evidence_strength} | {source_basis} | "
            "{human_review_required} | {recommendation_class} |".format(**row)
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
            ]
        )

    sections.extend(
        [
            "",
            "## Notes on Confidence and Validation",
            "",
            "Low evidence indicates higher uncertainty and requires human review before decisions are advanced.",
            "High evidence indicates comparatively higher confidence, but it does not remove the need for local consultation, professional judgement, or site-specific validation.",
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


def write_governance_summary(rows: list[dict]) -> None:
    """Write the governance-oriented Markdown summary."""
    highest_ranked = max(rows, key=lambda row: row["risk_adjusted_score"])
    strongest = max(rows, key=lambda row: _rank_value(row["evidence_strength"]))
    weakest = min(rows, key=lambda row: _rank_value(row["evidence_strength"]))
    highest_uncertainty = max(rows, key=lambda row: (row["human_review_required"], row["validation_need"]))
    human_review_rows = [row for row in rows if row["human_review_required"]]
    human_review_text = ", ".join(row["scenario_name"] for row in human_review_rows) or "None flagged by the current low-evidence rule"

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
    scenarios = scenario_options.get("scenarios", [])
    rows = build_comparison_rows(scenarios, evidence_profile)
    write_comparison_csv(rows)
    write_scenario_report(location, scenarios, rows)
    write_governance_summary(rows)
    print("Generated CCZPS-Lite comparison outputs in cczps_lite/output")


if __name__ == "__main__":
    main()
