"""Generate a deterministic, local-only cross-scenario evidence comparison."""
from __future__ import annotations

import json
from pathlib import Path

PROJECT_DIR = Path(__file__).resolve().parent.parent
OUTPUT_DIR = PROJECT_DIR / "output"
OUTPUT_PATH = OUTPUT_DIR / "scenario_comparison.json"
REPORT_PATH = OUTPUT_DIR / "scenario_comparison.md"
SCENARIOS = {
    "batlow": {"name": "Batlow", "meteorology_ids": ["batlow"]},
    "kunlun": {"name": "Kunlun", "meteorology_ids": ["kunlun"]},
    "iraq": {"name": "Iraq", "meteorology_ids": ["iraq"]},
    "baiyangdian_xiongan": {"name": "Baiyangdian-Xiong'an", "meteorology_ids": ["xiongan_wutai_headwaters", "xiongan_baiyangdian_wetland", "xiongan_downstream"]},
}
SOURCE_PATHS = {
    "trends": OUTPUT_DIR / "meteorology_trends.json",
    "transects": OUTPUT_DIR / "spatial_transects.json",
    "hypotheses": OUTPUT_DIR / "planning_hypotheses.json",
    "traceability": OUTPUT_DIR / "evidence_traceability.json",
    "validation": OUTPUT_DIR / "professional_validation_interface.json",
    "expert_reviews": OUTPUT_DIR / "expert_review_records.json",
    "approval_support": OUTPUT_DIR / "planning_approval_support_report.json",
    "governance": OUTPUT_DIR / "governance_decision_records.json",
}
COMPARISON_STATUSES = ("comparison_ready_with_limitations", "insufficient_evidence_for_comparison", "requires_professional_review", "requires_spatial_validation", "requires_governance_review")
SAFETY_BOUNDARY = ("Comparison support only. Records expose local evidence coverage, risk, uncertainty, and review status without ranking scenarios, selecting a best option, making a final recommendation, or claiming approval readiness.")


def _load(path: Path) -> dict | None:
    if not path.exists() or not path.read_text(encoding="utf-8").strip():
        return None
    return json.loads(path.read_text(encoding="utf-8"))


def _named(items: list[dict], field: str, value: str) -> dict | None:
    return next((item for item in items if item.get(field) == value), None)


def _trace_strength(traces: list[dict]) -> tuple[str, int, int]:
    if not traces:
        return "insufficient", 0, 0
    insufficient = sum(trace.get("evidence_strength") == "insufficient_evidence" for trace in traces)
    covered = len(traces) - insufficient
    if covered >= 5:
        return "medium", covered, insufficient
    if covered:
        return "low", covered, insufficient
    return "insufficient", covered, insufficient


def _trend_context(config: dict, trends: dict | None) -> dict:
    records = [(trends or {}).get("scenarios", {}).get(scenario_id) for scenario_id in config["meteorology_ids"]]
    records = [record for record in records if record]
    if not records:
        return {"trend_status": "unavailable", "rainfall_signal": "unknown", "humidity_signal": "unknown", "temperature_signal": "unknown", "solar_signal": "unknown"}

    def joined(variable: str) -> str:
        values = sorted({record.get("variables", {}).get(variable, {}).get("trend_classification", "unknown") for record in records})
        return "_and_".join(values)

    return {
        "trend_status": "available" if all(record.get("trend_status") == "sufficient_observations" for record in records) else "limited",
        "rainfall_signal": joined("rainfall_mm"),
        "humidity_signal": joined("humidity_percent"),
        "temperature_signal": joined("temperature_c"),
        "solar_signal": joined("solar_radiation_mj_m2"),
    }


def _comparison_status(traces, transect, validation, governance) -> str:
    if not traces:
        return "insufficient_evidence_for_comparison"
    if not transect or transect.get("validation", {}).get("status") != "valid_configured":
        return "requires_spatial_validation"
    if not validation or validation.get("review_status") == "awaiting_professional_review":
        return "requires_professional_review"
    if not governance or governance.get("internal_decision_status") in {"requires_further_review", "deferred", "not_decided"}:
        return "requires_governance_review"
    return "comparison_ready_with_limitations"


def _record(scenario_id: str, config: dict, sources: dict) -> dict:
    name = config["name"]
    traces = [item for item in (sources.get("traceability") or {}).get("records", []) if item.get("scenario_id") == scenario_id]
    hypothesis = (sources.get("hypotheses") or {}).get("hypotheses", {}).get(scenario_id)
    transect = _named((sources.get("transects") or {}).get("spatial_transects", []), "scenario_id", scenario_id)
    validation = (sources.get("validation") or {}).get("reviews", {}).get(scenario_id)
    expert = _named((sources.get("expert_reviews") or {}).get("records", []), "reviewed_scenario_or_module", name)
    approval = _named((sources.get("approval_support") or {}).get("scenarios", []), "scenario", name)
    governance = _named((sources.get("governance") or {}).get("records", []), "scenario_id", scenario_id)
    trend = _trend_context(config, sources.get("trends"))
    evidence_strength, covered_count, insufficient_count = _trace_strength(traces)
    unresolved_risks = list((approval or {}).get("unresolved_risks", []))
    spatial_status = (transect or {}).get("validation", {}).get("status", "unavailable")
    gis_status = (approval or {}).get("gis_dem_readiness", "unknown")
    hypothesis_text = " ".join(str((hypothesis or {}).get(field, "")) for field in ("problem_statement", "planning_assumption", "intervention_logic")).lower()
    hypothesis_ids = " ".join((hypothesis or {}).get("scenario_ids", [])).lower()
    energy_signal = "context_relevant_requires_review" if "energy" in hypothesis_text or "energy" in hypothesis_ids else "not_explicitly_documented"
    risk_level = "high" if len(unresolved_risks) >= 4 else "medium" if unresolved_risks else "unknown"
    uncertainty_level = "high" if (insufficient_count or not validation or validation.get("review_status") == "awaiting_professional_review" or not expert or expert.get("decision_status") == "not_reviewed" or gis_status != "validated") else "medium"
    approval_status = (approval or {}).get("approval_support_status", "not_ready_for_approval")
    if approval_status != "not_ready_for_approval":
        approval_status = "not_ready_for_approval"
    return {
        "scenario_id": scenario_id,
        "scenario_name": name,
        "comparison_status": _comparison_status(traces, transect, validation, governance),
        "environmental_signal": "context_documented_requires_validation",
        "water_signal": f"rainfall_{trend['rainfall_signal']};humidity_{trend['humidity_signal']};hydrology_requires_review",
        "land_signal": "requires_gis_dem_validation" if gis_status != "validated" else "spatial_validation_recorded",
        "energy_signal": energy_signal,
        "risk_level": risk_level,
        "evidence_strength": evidence_strength,
        "uncertainty_level": uncertainty_level,
        "planning_hypothesis_status": (hypothesis or {}).get("hypothesis_status", "unknown"),
        "traceability_status": "available" if traces else "unavailable",
        "trace_record_count": len(traces),
        "covered_trace_category_count": covered_count,
        "insufficient_trace_category_count": insufficient_count,
        "traceability_references": sorted(item.get("trace_id") for item in traces if item.get("trace_id")),
        "meteorology_trend_status": trend["trend_status"],
        "temperature_signal": trend["temperature_signal"],
        "rainfall_signal": trend["rainfall_signal"],
        "humidity_signal": trend["humidity_signal"],
        "solar_signal": trend["solar_signal"],
        "spatial_transect_status": spatial_status,
        "gis_dem_requirement_status": gis_status,
        "internal_governance_status": (governance or {}).get("internal_decision_status", "not_decided"),
        "professional_validation_status": (validation or {}).get("review_status", "awaiting_professional_review"),
        "expert_review_status": (expert or {}).get("decision_status", "not_reviewed"),
        "approval_support_status": approval_status,
        "unresolved_risks": unresolved_risks,
        "human_review_required": True,
        "professional_review_required": True,
        "comparison_notes": ["Comparison is based on local generated evidence only.", "Signals are descriptive evidence readings, not forecasts or causal findings.", "No scenario rank, winner, statutory approval, or implementation recommendation is produced."],
    }


def _summary(records: list[dict]) -> dict:
    def names(field: str, value: str) -> list[str]:
        return [record["scenario_name"] for record in records if record.get(field) == value]
    return {
        "evidence_coverage_groups": {"medium": names("evidence_strength", "medium"), "low": names("evidence_strength", "low"), "insufficient": names("evidence_strength", "insufficient")},
        "high_uncertainty_scenarios": names("uncertainty_level", "high"),
        "requires_spatial_validation": [record["scenario_name"] for record in records if record["gis_dem_requirement_status"] != "validated" or record["spatial_transect_status"] != "valid_configured"],
        "requires_expert_review": [record["scenario_name"] for record in records if record["expert_review_status"] == "not_reviewed"],
        "complete_traceability": [record["scenario_name"] for record in records if record["traceability_status"] == "available" and record["trace_record_count"] == 8],
        "summary_boundary": "Groups describe current evidence coverage and review needs only. They do not order scenarios or identify a preferred option.",
    }


def build_scenario_comparison(sources: dict | None = None) -> dict:
    loaded = sources or {key: _load(path) for key, path in SOURCE_PATHS.items()}
    records = [_record(scenario_id, config, loaded) for scenario_id, config in SCENARIOS.items()]
    return {
        "schema_version": "1.0", "runtime": "Scenario Comparison Runtime", "safety_boundary": SAFETY_BOUNDARY,
        "comparison_status_values": list(COMPARISON_STATUSES),
        "evidence_strength_values": ["low", "medium", "high", "insufficient", "unknown"],
        "risk_level_values": ["low", "medium", "high", "unknown"],
        "uncertainty_level_values": ["low", "medium", "high", "unknown"],
        "record_count": len(records), "cross_scenario_summary": _summary(records), "records": records,
    }


def render_markdown_report(output: dict) -> str:
    summary = output["cross_scenario_summary"]
    lines = ["# Scenario Comparison Runtime", "", output["safety_boundary"], "", "## Cross-Scenario Summary", "", summary["summary_boundary"], "",
        f"- Medium evidence coverage: {', '.join(summary['evidence_coverage_groups']['medium']) or 'None'}",
        f"- Low evidence coverage: {', '.join(summary['evidence_coverage_groups']['low']) or 'None'}",
        f"- High uncertainty: {', '.join(summary['high_uncertainty_scenarios']) or 'None'}",
        f"- GIS/DEM or spatial validation required: {', '.join(summary['requires_spatial_validation']) or 'None'}",
        f"- Expert review required: {', '.join(summary['requires_expert_review']) or 'None'}",
        f"- Complete eight-category traceability: {', '.join(summary['complete_traceability']) or 'None'}", "", "## Comparison Table", "",
        "| Scenario | Comparison status | Evidence | Uncertainty | Risk | Hypothesis | Traceability | Governance | Expert review | Approval support |",
        "| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |"]
    for record in output["records"]:
        lines.append("| {scenario_name} | {comparison_status} | {evidence_strength} | {uncertainty_level} | {risk_level} | {planning_hypothesis_status} | {traceability_status} | {internal_governance_status} | {expert_review_status} | {approval_support_status} |".format(**record))
    for record in output["records"]:
        lines += ["", f"## {record['scenario_name']}", "", f"- Environmental signal: `{record['environmental_signal']}`", f"- Water signal: `{record['water_signal']}`", f"- Land signal: `{record['land_signal']}`", f"- Energy signal: `{record['energy_signal']}`", f"- Spatial transect: `{record['spatial_transect_status']}`", f"- GIS/DEM requirement: `{record['gis_dem_requirement_status']}`", f"- Human review required: `{record['human_review_required']}`", f"- Professional review required: `{record['professional_review_required']}`", "", "Comparison notes:", "", *[f"- {note}" for note in record["comparison_notes"]]]
    return "\n".join(lines).rstrip() + "\n"


def write_scenario_comparison_outputs(output: dict, output_path: Path = OUTPUT_PATH, report_path: Path = REPORT_PATH) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(output, indent=2, ensure_ascii=True) + "\n", encoding="utf-8")
    report_path.write_text(render_markdown_report(output), encoding="utf-8")


def main() -> None:
    output = build_scenario_comparison()
    write_scenario_comparison_outputs(output)
    print(f"Wrote scenario comparison outputs to {OUTPUT_DIR}")


if __name__ == "__main__":
    main()
