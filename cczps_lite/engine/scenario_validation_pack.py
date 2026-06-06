"""Generate the CCZPS-Lite multi-scale scenario validation package.

This helper reuses the existing runtime layers against local validation fixtures.
Watershed continuity is a diagnostic reading only, not a routing or forecast model.
"""

from __future__ import annotations

import csv
import json
from pathlib import Path

from adaptive_response import derive_adaptive_response
from differential_field import derive_differential_field
from evidence_layer import (
    derive_evidence_strength,
    derive_human_review_required,
    derive_source_basis,
    derive_uncertainty_notes,
)
from forcing_layer import derive_forcing_candidates
from response_prioritisation import derive_response_prioritisation
from review_loop import derive_review_action
from runtime_fields import derive_runtime_fields
from runtime_reasoning import derive_runtime_reasoning
from scoring_rules import (
    calculate_governance_score,
    calculate_resilience_score,
    calculate_risk_adjusted_score,
    classify_recommendation,
)
from validation_layer import derive_validation_reading

PROJECT_DIR = Path(__file__).resolve().parent.parent
INPUT_PATH = PROJECT_DIR / "input" / "multi_scale_validation_pack.json"
OUTPUT_DIR = PROJECT_DIR / "output"
METADATA_FIELDS = [
    "validation_context",
    "geography",
    "geographic_scale",
    "watershed_stage",
    "watershed_continuity",
]


def _load_pack() -> dict:
    with INPUT_PATH.open("r", encoding="utf-8") as file_obj:
        return json.load(file_obj)


def _derive_fixture_row(scenario: dict) -> dict:
    scores = scenario.get("scores", {})
    runtime = derive_runtime_fields(scores)
    differential = derive_differential_field(scores, scenario.get("context_records", []))
    forcing = derive_forcing_candidates(differential, scores)
    evidence = scenario.get("evidence", {})
    evidence_result = {
        "evidence_strength": derive_evidence_strength(evidence),
        "source_basis": derive_source_basis(evidence),
        "uncertainty_notes": derive_uncertainty_notes(evidence),
        "human_review_required": derive_human_review_required(evidence),
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
        "validation_context": scenario.get("validation_context", ""),
        "geography": scenario.get("geography", ""),
        "geographic_scale": scenario.get("geographic_scale", ""),
        "watershed_stage": scenario.get("watershed_stage", "not_applicable"),
        "watershed_continuity": "Not applicable",
    }
    row["forcing_candidates"] = "; ".join(forcing["forcing_candidates"])
    row["validation_gaps"] = "; ".join(validation["validation_gaps"])
    row["review_triggers"] = "; ".join(review["review_triggers"])
    row["response_options"] = "; ".join(response["response_options"])
    return row


def derive_watershed_continuity(rows: list[dict], point_ids: list[str]) -> str:
    """Return a cautious source-to-consumption continuity diagnostic."""
    points = [row for row in rows if row.get("scenario_id") in point_ids]
    if len(points) != len(point_ids):
        return "Fragmented Continuity"
    water_values = [float(row["water_security"]) for row in points]
    ecology_values = [float(row["ecological_resilience"]) for row in points]
    evidence_values = [row["evidence_strength"] for row in points]
    if min(water_values) >= 7 and min(ecology_values) >= 7 and "Low" not in evidence_values:
        return "High Continuity"
    if min(water_values) >= 5 and min(ecology_values) >= 6:
        return "Moderate Continuity"
    return "Fragmented Continuity"


def _enrich_base_rows(rows: list[dict], pack: dict) -> None:
    metadata = pack.get("existing_scenario_metadata", {})
    for row in rows:
        details = metadata.get(row["scenario_id"], {})
        row["validation_context"] = details.get(
            "validation_context", "Baseline Batlow methodology pathway"
        )
        row["geography"] = details.get("geography", "Batlow, New South Wales, Australia")
        row["geographic_scale"] = details.get("geographic_scale", "local pathway")
        row["watershed_stage"] = "not_applicable"
        row["watershed_continuity"] = "Not applicable"


def _write_extended_matrix(base_rows: list[dict], fieldnames: list[str], pack: dict) -> list[dict]:
    rows = list(base_rows) + [_derive_fixture_row(item) for item in pack.get("scenarios", [])]
    continuity = derive_watershed_continuity(
        rows, pack.get("watershed_system", {}).get("validation_point_ids", [])
    )
    point_ids = set(pack.get("watershed_system", {}).get("validation_point_ids", []))
    for row in rows:
        if row["scenario_id"] in point_ids:
            row["watershed_continuity"] = continuity

    matrix_path = OUTPUT_DIR / "comparison_matrix.csv"
    insert_at = fieldnames.index("water_security") if "water_security" in fieldnames else 3
    extended_fields = fieldnames[:insert_at] + METADATA_FIELDS + fieldnames[insert_at:]
    with matrix_path.open("w", encoding="utf-8", newline="") as file_obj:
        writer = csv.DictWriter(file_obj, fieldnames=extended_fields, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)
    return rows


def _scenario_by_id(pack: dict) -> dict[str, dict]:
    return {scenario["scenario_id"]: scenario for scenario in pack.get("scenarios", [])}


def _format_values(values) -> str:
    return "; ".join(str(value) for value in values) if values else "None stated"


def _append_scenario_report(rows: list[dict], pack: dict, continuity: str) -> None:
    path = OUTPUT_DIR / "scenario_report.md"
    text = path.read_text(encoding="utf-8")
    marker = "\n## Multi-Scale Scenario Validation\n"
    text = text.split(marker, 1)[0].rstrip()
    scenarios = _scenario_by_id(pack)
    sections = [
        "",
        "## Multi-Scale Scenario Validation",
        "",
        "These fixtures test runtime consistency across contrasting contexts. They use indicative local inputs and do not establish real-world scientific validity.",
    ]
    validation_ids = ["BATLOW_ENERGY_RESILIENCE"] + list(scenarios)
    for scenario_id in validation_ids:
        row = next(row for row in rows if row["scenario_id"] == scenario_id)
        scenario = scenarios.get(scenario_id, {})
        sections.extend([
            "",
            f"### {row['validation_context']}",
            "",
            f"- Geography: {row['geography']}",
            f"- Scale: {row['geographic_scale']}",
            f"- Focus: {_format_values(scenario.get('focus', [])) if scenario else 'bushfire risk; distributed energy; microgrid resilience; agricultural continuity'}",
            f"- Evidence strength: {row['evidence_strength']}",
            f"- Validation status: {row['validation_status']}",
            f"- Human review required: {row['human_review_required']}",
            f"- Prioritised response: {row['prioritised_response']}",
            f"- Expected benefit: {row['expected_benefit']}",
            f"- Limitation: {scenario.get('limitations', pack.get('existing_scenario_metadata', {}).get(scenario_id, {}).get('limitations', 'Requires local review.'))}",
        ])
    sections.extend([
        "",
        "### Watershed Continuity Reading",
        "",
        f"- System: {pack['watershed_system']['name']}",
        f"- Diagnostic reading: {continuity}",
        "- Sequence examined: Mountain Source -> River Transport -> Wetland Storage -> Urban Consumption",
        "- Interpretation: The three validation points retain a usable concept-level connection, but downstream water pressure and uneven evidence prevent a High Continuity reading.",
        "- Boundary: River Transport is represented as a diagnostic connection only. No flow routing, travel-time, allocation, flood, or predictive model is used.",
    ])
    path.write_text(text + "\n" + "\n".join(sections) + "\n", encoding="utf-8")


def _append_governance_summary(rows: list[dict], pack: dict, continuity: str) -> None:
    path = OUTPUT_DIR / "governance_summary.md"
    text = path.read_text(encoding="utf-8")
    marker = "\n## Multi-Scale Validation Reading\n"
    text = text.split(marker, 1)[0].rstrip()
    validation_ids = {"BATLOW_ENERGY_RESILIENCE"} | {
        scenario["scenario_id"] for scenario in pack.get("scenarios", [])
    }
    validation_rows = [row for row in rows if row["scenario_id"] in validation_ids]
    high_rows = [row["scenario_name"] for row in validation_rows if row["implementation_priority"] == "High"]
    human_rows = [row["scenario_name"] for row in validation_rows if str(row["human_review_required"]) == "True"]
    sections = [
        "",
        "## Multi-Scale Validation Reading",
        "",
        f"- Validation contexts assessed: {len(validation_rows)} across local, regional, dryland, agricultural, headwater, wetland, and downstream scales.",
        f"- High implementation-priority pathways: {', '.join(high_rows) or 'None identified'}.",
        f"- Pathways requiring explicit human review: {', '.join(human_rows) or 'None identified'}.",
        f"- Watershed continuity reading: {continuity}.",
        "- Governance interpretation: The runtime chain executes consistently across the fixtures, while evidence quality and local validation needs continue to control review and response priority.",
        "- Decision boundary: Results remain diagnostic and concept-level; local experts, communities, asset owners, and relevant authorities must review assumptions before action.",
    ]
    path.write_text(text + "\n" + "\n".join(sections) + "\n", encoding="utf-8")


def _write_validation_pack(rows: list[dict], pack: dict, continuity: str) -> None:
    scenarios = _scenario_by_id(pack)
    validation_ids = ["BATLOW_ENERGY_RESILIENCE"] + list(scenarios)
    lines = [
        "# CCZPS-Lite Multi-Scale Scenario Validation Pack",
        "",
        pack.get("methodology_boundary", ""),
        "",
        "## Runtime Chain Under Validation",
        "",
        "Evidence -> Runtime Fields -> Differential Field -> Forcing -> Validation -> Review Loop -> Adaptive Response -> Response Prioritisation",
        "",
        "## Validation Summary",
        "",
        "| Context | Scale | Evidence | Validation | Human review | Prioritised response |",
        "| --- | --- | --- | --- | --- | --- |",
    ]
    for scenario_id in validation_ids:
        row = next(row for row in rows if row["scenario_id"] == scenario_id)
        lines.append(
            f"| {row['validation_context']} | {row['geographic_scale']} | {row['evidence_strength']} | {row['validation_status']} | {row['human_review_required']} | {row['prioritised_response']} |"
        )

    lines.extend(["", "## Scenario Validation Records"])
    for scenario_id in validation_ids:
        row = next(row for row in rows if row["scenario_id"] == scenario_id)
        scenario = scenarios.get(scenario_id, {})
        evidence = scenario.get("evidence", {})
        evidence_text = "; ".join(
            f"{name}: {record.get('strength', 'unknown')} / {record.get('source', 'unspecified')}"
            for name, record in evidence.items()
        ) or f"Existing Batlow evidence profile: {row['evidence_strength']} / {row['source_basis']}"
        scores = scenario.get("scores", {})
        score_text = "; ".join(f"{name}={value}" for name, value in scores.items()) or "Existing Batlow Energy scores"
        lines.extend([
            "",
            f"### {row['validation_context']}",
            "",
            f"- Scenario inputs: {score_text}",
            f"- Evidence assumptions: {evidence_text}",
            f"- Runtime outputs: risk index {row['risk_index']}; primary forcing {row['primary_forcing']}; forcing priority {row['forcing_priority']}",
            f"- Validation results: {row['validation_status']} (score {row['validation_score']}); gaps: {row['validation_gaps']}",
            f"- Review requirement: {row['review_action']}; owner: {row['review_owner']}; human review required: {row['human_review_required']}",
            f"- Prioritised response: {row['prioritised_response']} ({row['implementation_priority']}; {row['urgency_level']})",
            f"- Expected benefit: {row['expected_benefit']}",
            f"- Limitations: {scenario.get('limitations', pack.get('existing_scenario_metadata', {}).get(scenario_id, {}).get('limitations', 'Requires local review.'))}",
        ])

    lines.extend([
        "",
        "## Watershed Continuity Reading",
        "",
        f"- System: {pack['watershed_system']['name']}",
        f"- Result: {continuity}",
        "- Mountain Source: Wutai Mountain Headwaters",
        "- River Transport: represented as the diagnostic connection between validation points",
        "- Wetland Storage: Baiyangdian Wetland Core",
        "- Urban Consumption: Xiong'an and Downstream Region",
        "- Diagnostic basis: relative water-security, ecological-resilience, and evidence-strength bands across the three points",
        "- Limitation: no hydrological routing, water allocation, flood forecasting, demand forecasting, or predictive certainty",
        "",
        "## Cross-Scenario Limitations",
        "",
        "- All scores and representative context records are illustrative fixtures.",
        "- Geographic names do not imply that local authorities, communities, or domain experts have validated the assumptions.",
        "- The runtime demonstrates consistent rule execution, not scientific transferability or outcome accuracy.",
        "- Responses require local evidence, technical review, governance assessment, and community consultation before use.",
        "- No result is final planning, engineering, construction, investment, environmental, or regulatory advice.",
    ])
    (OUTPUT_DIR / "scenario_validation_pack.md").write_text(
        "\n".join(lines) + "\n", encoding="utf-8"
    )


def extend_validation_outputs() -> None:
    """Extend the standard generated outputs with multi-scale validation fixtures."""
    pack = _load_pack()
    matrix_path = OUTPUT_DIR / "comparison_matrix.csv"
    with matrix_path.open("r", encoding="utf-8", newline="") as file_obj:
        reader = csv.DictReader(file_obj)
        fieldnames = list(reader.fieldnames or [])
        base_rows = list(reader)
    _enrich_base_rows(base_rows, pack)
    rows = _write_extended_matrix(base_rows, fieldnames, pack)
    continuity = derive_watershed_continuity(
        rows, pack.get("watershed_system", {}).get("validation_point_ids", [])
    )
    _append_scenario_report(rows, pack, continuity)
    _append_governance_summary(rows, pack, continuity)
    _write_validation_pack(rows, pack, continuity)
