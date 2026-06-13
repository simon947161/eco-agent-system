"""Derive cautious, testable planning hypotheses from local CCZPS-Lite outputs."""
from __future__ import annotations
import csv
import json
from pathlib import Path

PROJECT_DIR = Path(__file__).resolve().parent.parent
INPUT_DIR = PROJECT_DIR / "input"
OUTPUT_DIR = PROJECT_DIR / "output"
OUTPUT_PATH = OUTPUT_DIR / "planning_hypotheses.json"
REPORT_PATH = OUTPUT_DIR / "planning_hypotheses.md"
SCHEMA_VERSION = "1.0"
HYPOTHESIS_STATUSES = {"concept_level", "evidence_supported", "requires_validation", "not_supported", "insufficient_evidence"}
SAFETY_BOUNDARY = "Testable concept-level assumptions only. No final recommendation, engineering design, construction advice, regulatory approval, autonomous decision, forecast, simulation, GIS automation, live API call, or language-model call."
HYPOTHESIS_PROFILES = {
    "batlow": {
        "scenario": "Batlow", "scenario_ids": ["BATLOW_WATER_PRIORITY", "BATLOW_ENERGY_RESILIENCE", "BATLOW_ECOLOGY_FIRE_BUFFER"],
        "hypothesis_id": "batlow_microclimate_resilience_hypothesis",
        "problem_statement": "Dry-season water, heat, fire, and continuity pressures may reduce landscape and community resilience.",
        "planning_assumption": "Coordinated water retention, microclimate buffering, ecological recovery, and continuity planning may reduce combined climate stress.",
        "intervention_logic": "Test locally appropriate water-sensitive measures, vegetation and shade buffers, fire-aware landscape review, and continuity planning as linked concepts rather than final designs.",
        "expected_effect": "Improved resilience indicators may be observed if the assumed water, heat, fire, and continuity pathways are supported by local evidence.",
    },
    "kunlun": {
        "scenario": "Kunlun", "scenario_ids": ["KUNLUN_ECO_WATER"], "hypothesis_id": "kunlun_eco_water_buffer_hypothesis",
        "problem_statement": "Dryland water limitation and ecological stress may constrain restoration and climate adaptation.",
        "planning_assumption": "Improved water retention knowledge and ecological buffering may strengthen dryland resilience where field evidence supports the relationship.",
        "intervention_logic": "Test water-storage review, soil-moisture observation, ecological buffer restoration, and local adaptation consultation.",
        "expected_effect": "Water and ecological resilience indicators may improve if the proposed buffering relationship is confirmed locally.",
    },
    "iraq": {
        "scenario": "Iraq", "scenario_ids": ["IRAQ_AGRICULTURE_RECOVERY"], "hypothesis_id": "iraq_agricultural_recovery_hypothesis",
        "problem_statement": "Water scarcity, heat exposure, degraded soils, and weak ecological buffers may constrain agricultural recovery.",
        "planning_assumption": "Evidence-led irrigation review, soil-moisture monitoring, and shelterbelt assessment may identify feasible recovery pathways.",
        "intervention_logic": "Collect field evidence before testing irrigation efficiency, soil moisture, and ecological buffer concepts.",
        "expected_effect": "Agricultural and ecological indicators may improve only if local water, soil, infrastructure, and safety evidence supports the assumed pathway.",
    },
    "baiyangdian_xiongan": {
        "scenario": "Baiyangdian-Xiong'an", "scenario_ids": ["XIONGAN_WUTAI_HEADWATERS", "XIONGAN_BAIYANGDIAN_WETLAND", "XIONGAN_DOWNSTREAM_URBAN"],
        "hypothesis_id": "baiyangdian_xiongan_watershed_continuity_hypothesis",
        "problem_statement": "Headwater condition, wetland water balance, urban demand, and ecological connectivity may interact across the watershed.",
        "planning_assumption": "Coordinated review across mountain source, wetland storage, and downstream demand may reveal more resilient watershed intervention priorities.",
        "intervention_logic": "Test headwater protection, wetland water-balance observation, ecological connectivity, flood resilience, and demand review as a linked diagnostic set.",
        "expected_effect": "Watershed continuity indicators may improve if monitored relationships support coordinated action across the configured validation points.",
    },
}


def _load_json(path: Path, fallback: dict) -> dict:
    if not path.exists() or not path.read_text(encoding="utf-8").strip():
        return fallback
    return json.loads(path.read_text(encoding="utf-8"))


def _load_comparison_rows(path: Path = OUTPUT_DIR / "comparison_matrix.csv") -> list[dict]:
    if not path.exists():
        return []
    with path.open("r", encoding="utf-8", newline="") as file_obj:
        return list(csv.DictReader(file_obj))


def classify_hypothesis_status(evidence_strengths: list[str], validation_statuses: list[str], trend_status: str | None, spatial_status: str | None, contradictory_signals: int = 0) -> str:
    """Classify support without converting concept evidence into a recommendation."""
    strengths = {str(value).lower() for value in evidence_strengths if value}
    validations = {str(value).lower() for value in validation_statuses if value}
    if contradictory_signals >= 2:
        return "not_supported"
    if not strengths and not validations and not trend_status and not spatial_status:
        return "insufficient_evidence"
    if strengths <= {"low"} and (not trend_status or trend_status == "insufficient_data"):
        return "insufficient_evidence"
    if any("insufficient" in value for value in validations) and strengths <= {"low"}:
        return "insufficient_evidence"
    if any(term in value for value in validations for term in ("requires technical", "requires local", "insufficient")):
        return "requires_validation"
    if spatial_status and spatial_status != "valid_configured":
        return "requires_validation"
    if strengths.intersection({"medium", "high"}) and trend_status == "sufficient_observations" and any("validated enough" in value for value in validations) and spatial_status == "valid_configured":
        return "evidence_supported"
    return "concept_level"


def derive_validation_indicators(context: dict) -> list[str]:
    indicators = ["temperature trend", "rainfall trend", "humidity trend", "spatial transect context", "local field evidence", "expert planning review"]
    focus = " ".join(context.get("focus", [])).lower()
    if any(term in focus for term in ("water", "irrigation", "wetland", "runoff")):
        indicators.append("water balance or soil moisture evidence")
    if any(term in focus for term in ("ecolog", "forest", "vegetation")):
        indicators.append("vegetation or ecological condition evidence")
    if any(term in focus for term in ("fire", "flood")):
        indicators.append("hazard-specific technical review")
    return list(dict.fromkeys(indicators))


def derive_failure_conditions(context: dict) -> list[str]:
    conditions = ["insufficient local evidence", "contradictory trend signal", "unsupported spatial relationship", "intervention effect not observed", "professional review does not support the assumption"]
    if context.get("missing_spatial_data"):
        conditions.append("required spatial context remains incomplete")
    return conditions


def derive_intervention_logic(profile: dict, context: dict) -> str:
    interventions = context.get("interventions", [])
    if not interventions:
        return profile["intervention_logic"]
    return f"{profile['intervention_logic']} Existing candidate actions include {', '.join(interventions[:5])}; each remains subject to validation."


def summarize_planning_hypothesis(hypothesis: dict) -> str:
    status = hypothesis["hypothesis_status"].replace("_", " ")
    return f"This {status} planning hypothesis is a testable assumption, not a recommendation. Further local evidence and professional review are required."


def derive_planning_hypothesis(profile: dict, context: dict) -> dict:
    status = classify_hypothesis_status(context.get("evidence_strengths", []), context.get("validation_statuses", []), context.get("trend_status"), context.get("spatial_status"), context.get("contradictory_signals", 0))
    hypothesis = {
        "hypothesis_id": profile["hypothesis_id"], "scenario": profile["scenario"], "scenario_ids": profile["scenario_ids"], "hypothesis_status": status,
        "problem_statement": profile["problem_statement"], "planning_assumption": profile["planning_assumption"],
        "intervention_logic": derive_intervention_logic(profile, context), "expected_effect": profile["expected_effect"],
        "validation_indicators": derive_validation_indicators(context), "failure_conditions": derive_failure_conditions(context), "human_review_required": True,
        "evidence_context": {"evidence_strengths": context.get("evidence_strengths", []), "validation_statuses": context.get("validation_statuses", []), "meteorology_trend_status": context.get("trend_status"), "spatial_transect_status": context.get("spatial_status")},
    }
    hypothesis["hypothesis_summary"] = summarize_planning_hypothesis(hypothesis)
    return hypothesis


def _scenario_contexts() -> dict[str, dict]:
    comparison = _load_comparison_rows()
    validation_pack = _load_json(INPUT_DIR / "multi_scale_validation_pack.json", {"scenarios": []})
    trends = _load_json(OUTPUT_DIR / "meteorology_trends.json", {"scenarios": {}})
    spatial = _load_json(OUTPUT_DIR / "spatial_transect_scenario_pack.json", {"scenarios": []})
    extended = {item["scenario_id"]: item for item in validation_pack.get("scenarios", [])}
    spatial_by_id = {item.get("scenario_id"): item for item in spatial.get("scenarios", [])}
    contexts = {}
    for key, profile in HYPOTHESIS_PROFILES.items():
        rows = [row for row in comparison if row.get("scenario_id") in profile["scenario_ids"]]
        records = [extended[scenario_id] for scenario_id in profile["scenario_ids"] if scenario_id in extended]
        trend = trends.get("scenarios", {}).get(key, {})
        spatial_record = spatial_by_id.get(key, {})
        contexts[key] = {
            "evidence_strengths": [row.get("evidence_strength") for row in rows if row.get("evidence_strength")] + [evidence.get("strength") for record in records for evidence in record.get("evidence", {}).values() if evidence.get("strength")],
            "validation_statuses": [row.get("validation_status") for row in rows if row.get("validation_status")],
            "trend_status": trend.get("trend_status"), "spatial_status": spatial_record.get("validation_status"),
            "missing_spatial_data": bool(spatial_record.get("missing_data_points")),
            "focus": [value for record in records for value in record.get("focus", [])],
            "interventions": [value for record in records for value in record.get("interventions", [])],
        }
    return contexts


def build_planning_hypotheses() -> dict:
    contexts = _scenario_contexts()
    return {"schema_version": SCHEMA_VERSION, "runtime": "Planning Hypothesis Runtime", "dashboard_compatible": True, "safety_boundary": SAFETY_BOUNDARY, "status_values": sorted(HYPOTHESIS_STATUSES), "hypotheses": {key: derive_planning_hypothesis(profile, contexts.get(key, {})) for key, profile in HYPOTHESIS_PROFILES.items()}}


def render_markdown_report(output: dict) -> str:
    lines = ["# Planning Hypothesis Runtime", "", output["safety_boundary"], "", "A planning hypothesis connects observed conditions to a testable intervention assumption. It is not a final recommendation or approval.", ""]
    for hypothesis in output["hypotheses"].values():
        lines.extend([f"## {hypothesis['scenario']}", "", f"- Hypothesis ID: {hypothesis['hypothesis_id']}", f"- Status: {hypothesis['hypothesis_status']}", f"- Human review required: {hypothesis['human_review_required']}", f"- Problem statement: {hypothesis['problem_statement']}", f"- Planning assumption: {hypothesis['planning_assumption']}", f"- Intervention logic: {hypothesis['intervention_logic']}", f"- Expected effect: {hypothesis['expected_effect']}", "", "### Validation Indicators", "", *[f"- {value}" for value in hypothesis["validation_indicators"]], "", "### Failure Conditions", "", *[f"- {value}" for value in hypothesis["failure_conditions"]], "", f"**Summary:** {hypothesis['hypothesis_summary']}", ""])
    return "\n".join(lines).rstrip() + "\n"


def write_planning_hypothesis_outputs(output: dict, output_path: Path = OUTPUT_PATH, report_path: Path = REPORT_PATH) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(output, indent=2, ensure_ascii=True) + "\n", encoding="utf-8")
    report_path.write_text(render_markdown_report(output), encoding="utf-8")


def main() -> None:
    output = build_planning_hypotheses()
    write_planning_hypothesis_outputs(output)
    print(f"Wrote planning hypotheses to {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
