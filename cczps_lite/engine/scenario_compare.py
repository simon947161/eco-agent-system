"""Run the CCZPS-Lite Batlow scenario comparison engine."""

from __future__ import annotations

import csv
import json
import sys
from collections import Counter
from pathlib import Path

ENGINE_DIR = Path(__file__).resolve().parent
PROJECT_DIR = ENGINE_DIR.parent
REPO_ROOT = PROJECT_DIR.parent
if str(ENGINE_DIR) not in sys.path:
    sys.path.insert(0, str(ENGINE_DIR))

from adaptive_response import derive_adaptive_response  # noqa: E402
from differential_field import derive_differential_field  # noqa: E402
from evidence_layer import (  # noqa: E402
    derive_evidence_strength,
    derive_human_review_required,
    derive_source_basis,
    derive_uncertainty_notes,
)
from forcing_layer import derive_forcing_candidates  # noqa: E402
from response_prioritisation import derive_response_prioritisation  # noqa: E402
from review_loop import derive_review_action  # noqa: E402
from runtime_fields import derive_runtime_fields  # noqa: E402
from runtime_reasoning import derive_runtime_reasoning  # noqa: E402
from scoring_rules import (  # noqa: E402
    calculate_governance_score,
    calculate_resilience_score,
    calculate_risk_adjusted_score,
    classify_recommendation,
)
from validation_layer import derive_validation_reading  # noqa: E402

INPUT_DIR = PROJECT_DIR / "input"
OUTPUT_DIR = PROJECT_DIR / "output"
SCENARIO_EVIDENCE_PATHWAYS = {
    "water_priority": ("water",),
    "energy_resilience": ("energy",),
    "ecology_fire_buffer_priority": ("ecology", "fire"),
}
CSV_FIELDS = [
    "scenario_id", "scenario_name", "scenario_type", "water_security",
    "energy_resilience", "ecological_resilience", "fire_resilience",
    "community_acceptance", "investment_feasibility", "implementation_complexity",
    "validation_need", "risk_index", "water_balance_signal", "ecological_signal",
    "evaporation_pressure", "confidence_level", "validation_required", "runtime_reasoning",
    "water_gradient", "water_gradient_class", "heat_gradient", "heat_gradient_class",
    "vegetation_gradient", "vegetation_gradient_class", "fire_gradient", "fire_gradient_class",
    "differential_status", "differential_summary", "reference_record_count",
    "forcing_candidates", "primary_forcing", "forcing_priority", "forcing_summary",
    "evidence_strength", "source_basis", "uncertainty_notes", "human_review_required",
    "validation_score", "validation_status", "validation_gaps", "validation_summary",
    "review_action", "review_priority", "review_owner", "review_triggers", "review_summary",
    "response_priority", "response_options", "response_mode", "response_summary",
    "implementation_priority", "urgency_level", "expected_benefit",
    "prioritised_response", "prioritisation_summary",
    "resilience_score", "governance_score", "risk_adjusted_score", "recommendation_class",
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


def build_comparison_rows(scenarios: list[dict], evidence_profile: dict, context_records: list[dict]) -> list[dict]:
    """Calculate runtime, response, prioritisation, and scoring fields."""
    rows = []
    for scenario in scenarios:
        scores = scenario.get("scores", {})
        runtime = derive_runtime_fields(scores)
        differential = derive_differential_field(scores, context_records)
        forcing = derive_forcing_candidates(differential, scores)
        scenario_evidence = evidence_for_scenario(scenario, evidence_profile)
        evidence_result = {
            "evidence_strength": derive_evidence_strength(scenario_evidence),
            "source_basis": derive_source_basis(scenario_evidence),
            "uncertainty_notes": derive_uncertainty_notes(scenario_evidence),
            "human_review_required": derive_human_review_required(scenario_evidence),
        }
        validation = derive_validation_reading(runtime, differential, forcing, evidence_result)
        review = derive_review_action(validation, evidence_result, forcing)
        response = derive_adaptive_response(validation, review, forcing, evidence_result)
        prioritisation = derive_response_prioritisation(response, validation, forcing)
        risk_adjusted_score = calculate_risk_adjusted_score(scores)
        row = {
            "scenario_id": scenario.get("scenario_id", ""),
            "scenario_name": scenario.get("scenario_name", ""),
            "scenario_type": scenario.get("scenario_type", ""),
            **scores,
            **runtime,
            "runtime_reasoning": derive_runtime_reasoning(scenario, runtime),
            **differential,
            **forcing,
            **evidence_result,
            **validation,
            **review,
            **response,
            **prioritisation,
            "resilience_score": calculate_resilience_score(scores),
            "governance_score": calculate_governance_score(scores),
            "risk_adjusted_score": risk_adjusted_score,
            "recommendation_class": classify_recommendation(risk_adjusted_score),
        }
        row["forcing_candidates"] = "; ".join(forcing["forcing_candidates"])
        row["validation_gaps"] = "; ".join(validation["validation_gaps"])
        row["review_triggers"] = "; ".join(review["review_triggers"])
        row["response_options"] = "; ".join(response["response_options"])
        rows.append(row)
    return rows


def write_comparison_csv(rows: list[dict]) -> None:
    """Write the comparison matrix CSV."""
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    with (OUTPUT_DIR / "comparison_matrix.csv").open("w", encoding="utf-8", newline="") as file_obj:
        writer = csv.DictWriter(file_obj, fieldnames=CSV_FIELDS, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def _format_list(values: list[str]) -> str:
    return "\n".join(f"- {value}" for value in values)


def write_scenario_report(location: dict, scenarios: list[dict], rows: list[dict]) -> None:
    """Write the detailed scenario Markdown report."""
    row_by_id = {row["scenario_id"]: row for row in rows}
    sections = [
        "# CCZPS-Lite v0.4 — Batlow Scenario Report", "",
        "This is a methodology demonstrator using indicative values only.",
        "It is not a final planning, engineering, financial, or regulatory assessment.", "",
        "## Location Profile", "",
        f"- Location: {location.get('location_name')}",
        f"- Location ID: {location.get('location_id')}",
        f"- Region type: {location.get('region_type')}",
        f"- Climate regime: {location.get('climate_regime')}",
        "- Key climate risks:", _format_list(location.get("key_climate_risks", [])), "",
        "## Scenario Comparison Summary", "",
        "| Scenario | Validation | Response priority | Implementation priority | Urgency | Prioritised response | Recommendation |",
        "| --- | --- | --- | --- | --- | --- | --- |",
    ]
    for row in rows:
        sections.append(
            "| {scenario_name} | {validation_status} | {response_priority} | "
            "{implementation_priority} | {urgency_level} | {prioritised_response} | "
            "{recommendation_class} |".format(**row)
        )

    scenario_headings = [
        "## Scenario A: Water Priority",
        "## Scenario B: Energy Resilience",
        "## Scenario C: Ecology / Fire Buffer Priority",
    ]
    for heading, scenario in zip(scenario_headings, scenarios):
        row = row_by_id[scenario["scenario_id"]]
        sections.extend([
            "", heading, "", scenario.get("description", ""), "",
            "### Interventions", _format_list(scenario.get("interventions", [])), "",
            "### Runtime and Evidence Fields", "",
            f"- Runtime reasoning: {row['runtime_reasoning']}",
            f"- Risk index: {row['risk_index']}",
            f"- Confidence level: {row['confidence_level']}",
            f"- Validation required: {row['validation_required']}",
            f"- Evidence strength: {row['evidence_strength']}",
            f"- Source basis: {row['source_basis']}",
            f"- Uncertainty notes: {row['uncertainty_notes']}",
            f"- Human review required: {row['human_review_required']}", "",
            "### Validation Layer Runtime", "",
            f"- Validation score: {row['validation_score']}",
            f"- Validation status: {row['validation_status']}",
            f"- Validation gaps: {row['validation_gaps']}",
            f"- Validation summary: {row['validation_summary']}", "",
            "### Validation Feedback / Review Loop", "",
            f"- Review action: {row['review_action']}",
            f"- Review priority: {row['review_priority']}",
            f"- Review owner: {row['review_owner']}",
            f"- Review triggers: {row['review_triggers']}",
            f"- Review summary: {row['review_summary']}", "",
            "### Adaptive Response Runtime", "",
            f"- Response priority: {row['response_priority']}",
            f"- Response mode: {row['response_mode']}",
            f"- Response options: {row['response_options']}",
            f"- Response summary: {row['response_summary']}", "",
            "### Response Prioritisation Runtime", "",
            f"- Implementation priority: {row['implementation_priority']}",
            f"- Urgency level: {row['urgency_level']}",
            f"- Expected benefit: {row['expected_benefit']}",
            f"- Prioritised response: {row['prioritised_response']}",
            f"- Prioritisation summary: {row['prioritisation_summary']}", "",
            "### Differential Field Runtime", "",
            f"- Differential status: {row['differential_status']}",
            f"- Water gradient: {row['water_gradient']} ({row['water_gradient_class']})",
            f"- Heat gradient: {row['heat_gradient']} ({row['heat_gradient_class']})",
            f"- Vegetation gradient: {row['vegetation_gradient']} ({row['vegetation_gradient_class']})",
            f"- Fire gradient: {row['fire_gradient']} ({row['fire_gradient_class']})",
            f"- Differential summary: {row['differential_summary']}",
            f"- Reference record count: {row['reference_record_count']}", "",
            "### Forcing Layer Runtime", "",
            f"- Primary forcing: {row['primary_forcing']}",
            f"- Forcing candidates: {row['forcing_candidates']}",
            f"- Forcing priority: {row['forcing_priority']}",
            f"- Forcing summary: {row['forcing_summary']}",
        ])

    sections.extend([
        "", "## Notes on Confidence and Validation", "",
        "Low evidence indicates higher uncertainty and requires human review before decisions are advanced.",
        "High evidence does not remove the need for local consultation, professional judgement, or site-specific validation.",
        "Differential field gradients are indicative comparisons against representative context records, not validated field measurements.",
        "Response and prioritisation outputs are candidate concept-level readings only; they require review and are not final design advice.",
        "", "## Methodology Boundary", "",
        "CCZPS-Lite v0.4 uses local JSON inputs, transparent rules, and generated text outputs only.",
        "It does not connect to weather APIs, GIS services, databases, machine learning models, or world models.",
    ])
    (OUTPUT_DIR / "scenario_report.md").write_text("\n".join(sections) + "\n", encoding="utf-8")


def _rank_value(strength: str) -> int:
    return {"Low": 1, "Medium": 2, "High": 3}.get(strength, 0)


def _priority_rank(priority: str) -> int:
    return {"Low": 1, "Medium": 2, "High": 3}.get(priority, 0)


def _urgency_rank(urgency: str) -> int:
    return {"Routine": 1, "Moderate": 2, "Critical": 3}.get(urgency, 0)


def _split_field(row: dict, field: str) -> list[str]:
    return [value.strip() for value in row[field].split(";") if value.strip()]


def _most_common(rows: list[dict], field: str, empty_text: str) -> str:
    counts = Counter(value for row in rows for value in _split_field(row, field))
    if not counts:
        return empty_text
    value, count = max(counts.items(), key=lambda item: (item[1], item[0]))
    return f"{value} ({count} scenario(s))"


def _scenario_names_with_value(rows: list[dict], field: str, value: str) -> str:
    names = [row["scenario_name"] for row in rows if value in _split_field(row, field)]
    return ", ".join(names) or "None identified"


def _scenario_names_with_exact(rows: list[dict], field: str, value: str) -> str:
    names = [row["scenario_name"] for row in rows if row[field] == value]
    return ", ".join(names) or "None identified"


def write_governance_summary(rows: list[dict]) -> None:
    """Write the governance-oriented Markdown summary."""
    highest_ranked = max(rows, key=lambda row: row["risk_adjusted_score"])
    strongest = max(rows, key=lambda row: _rank_value(row["evidence_strength"]))
    weakest = min(rows, key=lambda row: _rank_value(row["evidence_strength"]))
    highest_uncertainty = max(rows, key=lambda row: (row["human_review_required"], row["validation_need"]))
    human_review_text = ", ".join(row["scenario_name"] for row in rows if row["human_review_required"]) or "None flagged by the current low-evidence rule"
    strongest_water = max(rows, key=lambda row: row["water_gradient"])
    highest_heat = max(rows, key=lambda row: row["heat_gradient"])
    strongest_vegetation = max(rows, key=lambda row: row["vegetation_gradient"])
    highest_fire = max(rows, key=lambda row: row["fire_gradient"])
    highest_forcing = max(rows, key=lambda row: _priority_rank(row["forcing_priority"]))
    weakest_validation = min(rows, key=lambda row: row["validation_score"])
    strongest_validation = max(rows, key=lambda row: row["validation_score"])
    validation_review_text = ", ".join(
        row["scenario_name"] for row in rows
        if row["validation_status"] != "Validated Enough for Concept Review"
    ) or "None flagged by the current validation layer"
    highest_review = max(rows, key=lambda row: (_priority_rank(row["review_priority"]), -row["validation_score"]))
    owner_counts = Counter(row["review_owner"] for row in rows)
    common_owner, common_owner_count = max(owner_counts.items(), key=lambda item: (item[1], item[0]))
    highest_response = max(rows, key=lambda row: (_priority_rank(row["response_priority"]), -row["validation_score"]))
    implementation_focus = _split_field(highest_response, "response_options")[0]
    highest_implementation = max(
        rows,
        key=lambda row: (
            _priority_rank(row["implementation_priority"]),
            _urgency_rank(row["urgency_level"]),
            -row["validation_score"],
        ),
    )

    lines = [
        "# Governance Summary", "", "## Recommended Reading of Results", "",
        "The result indicates a preliminary priority for further review.",
        "Final selection requires local consultation, data validation, and governance assessment.", "",
        "## Highest-Ranked Pathway", "",
        f"- {highest_ranked['scenario_name']} has the highest indicative risk-adjusted score ({highest_ranked['risk_adjusted_score']}).",
        f"- Recommendation class: {highest_ranked['recommendation_class']}.", "",
        "## Key Trade-Offs", "",
        "- Water-focused action improves drought and orchard resilience but still requires hydrological validation.",
        "- Energy-focused action supports emergency continuity but currently relies on concept-level evidence.",
        "- Ecology and fire-buffer action has strong fire relevance but requires site-specific ecological and implementation review.", "",
        "## Validation Needs", "",
        "- Treat all scores as indicative demonstrator values.",
        "- Validate assumptions with local data, professional review, and community consultation before implementation.", "",
        "## Evidence Assessment", "",
        f"- Strongest evidence pathway: {strongest['scenario_name']} ({strongest['evidence_strength']}; {strongest['source_basis']}).",
        f"- Weakest evidence pathway: {weakest['scenario_name']} ({weakest['evidence_strength']}; {weakest['source_basis']}).",
        f"- Highest uncertainty pathway: {highest_uncertainty['scenario_name']} ({highest_uncertainty['uncertainty_notes']}).",
        f"- Scenarios requiring human review: {human_review_text}.", "",
        "## Differential Field Reading", "",
        "These gradients compare scenario scores with indicative representative Batlow context records only.",
        f"- Strongest water advantage: {strongest_water['scenario_name']} ({strongest_water['water_gradient']} ({strongest_water['water_gradient_class']})).",
        f"- Highest heat pressure: {highest_heat['scenario_name']} ({highest_heat['heat_gradient']} ({highest_heat['heat_gradient_class']})).",
        f"- Strongest vegetation buffer: {strongest_vegetation['scenario_name']} ({strongest_vegetation['vegetation_gradient']} ({strongest_vegetation['vegetation_gradient_class']})).",
        f"- Highest fire exposure: {highest_fire['scenario_name']} ({highest_fire['fire_gradient']} ({highest_fire['fire_gradient_class']})).", "",
        "## Forcing Layer Reading", "",
        "These are candidate pressure readings from representative gradients only; they do not prove causality.",
        f"- Highest forcing priority: {highest_forcing['scenario_name']} ({highest_forcing['forcing_priority']}; {highest_forcing['primary_forcing']}).",
        f"- Most common candidate forcing: {_most_common(rows, 'forcing_candidates', 'None identified')}.",
        f"- Scenarios with Fire Exposure forcing: {_scenario_names_with_value(rows, 'forcing_candidates', 'Fire Exposure')}.",
        f"- Scenarios with Microclimate Buffer Support: {_scenario_names_with_value(rows, 'forcing_candidates', 'Microclimate Buffer Support')}.", "",
        "## Validation Layer Runtime", "",
        "The validation layer combines evidence strength, runtime confidence, review flags, and candidate forcing outputs into concept-level validation readings.",
        f"- Strongest validation reading: {strongest_validation['scenario_name']} ({strongest_validation['validation_score']}; {strongest_validation['validation_status']}).",
        f"- Weakest validation reading: {weakest_validation['scenario_name']} ({weakest_validation['validation_score']}; {weakest_validation['validation_status']}).",
        f"- Scenarios needing further validation attention: {validation_review_text}.", "",
        "## Review Loop Reading", "",
        f"- Highest review priority pathway: {highest_review['scenario_name']} ({highest_review['review_priority']}; {highest_review['review_action']}).",
        f"- Pathways held for evidence: {_scenario_names_with_exact(rows, 'review_action', 'Hold and collect evidence')}.",
        f"- Pathways requiring technical review: {_scenario_names_with_exact(rows, 'review_action', 'Escalate to technical review')}.",
        f"- Most common review owner: {common_owner} ({common_owner_count} scenario(s)).",
        f"- Suggested next governance action: Begin with {highest_review['scenario_name']}: {highest_review['review_action'].lower()}, with the {highest_review['review_owner']} coordinating the next concept-level review.", "",
        "## Adaptive Response Reading", "",
        f"- Highest response priority pathway: {highest_response['scenario_name']} ({highest_response['response_priority']}; {highest_response['response_mode']}).",
        f"- Most common response option: {_most_common(rows, 'response_options', 'None identified')}.",
        f"- Evidence-building response pathways: {_scenario_names_with_exact(rows, 'response_mode', 'Evidence-building response')}.",
        f"- Technical response pathways: {_scenario_names_with_exact(rows, 'response_mode', 'Technical validation response')}.",
        f"- Suggested next implementation focus: {implementation_focus} for {highest_response['scenario_name']}, subject to local and expert review; this is not final design advice.", "",
        "## Response Prioritisation Reading", "",
        f"- Highest priority pathway: {highest_implementation['scenario_name']} ({highest_implementation['implementation_priority']}; {highest_implementation['urgency_level']}).",
        f"- Most common prioritised response: {_most_common(rows, 'prioritised_response', 'None identified')}.",
        f"- Critical urgency pathways: {_scenario_names_with_exact(rows, 'urgency_level', 'Critical')}.",
        f"- Evidence-priority pathways: {_scenario_names_with_exact(rows, 'expected_benefit', 'Confidence improvement')}.",
        f"- Water-priority pathways: {_scenario_names_with_exact(rows, 'expected_benefit', 'Hydrological resilience improvement')}.",
        f"- Fire-priority pathways: {_scenario_names_with_exact(rows, 'expected_benefit', 'Risk reduction and asset protection')}.",
        f"- Suggested first implementation focus: {highest_implementation['prioritised_response']} for {highest_implementation['scenario_name']}, as a candidate response subject to concept-level review and local checking.", "",
        "## Suggested Next Step", "",
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
    rows = build_comparison_rows(scenarios, evidence_profile, differential_context.get("records", []))
    write_comparison_csv(rows)
    write_scenario_report(location, scenarios, rows)
    write_governance_summary(rows)
    print("Generated CCZPS-Lite comparison outputs in cczps_lite/output")


if __name__ == "__main__":
    main()
