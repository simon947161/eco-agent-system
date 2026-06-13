"""Generate deterministic internal governance decision-support records."""
from __future__ import annotations

import json
from pathlib import Path

PROJECT_DIR = Path(__file__).resolve().parent.parent
OUTPUT_DIR = PROJECT_DIR / "output"
OUTPUT_PATH = OUTPUT_DIR / "governance_decision_records.json"
REPORT_PATH = OUTPUT_DIR / "governance_decision_records.md"
SCHEMA_VERSION = "1.0"
ALLOWED_STATUSES = (
    "not_decided", "requires_further_review",
    "conditionally_supported_for_internal_planning",
    "not_supported_by_current_evidence", "deferred",
)
SCENARIOS = {
    "batlow": "Batlow", "kunlun": "Kunlun", "iraq": "Iraq",
    "baiyangdian_xiongan": "Baiyangdian-Xiong'an",
}
SOURCE_PATHS = {
    "traceability": OUTPUT_DIR / "evidence_traceability.json",
    "hypotheses": OUTPUT_DIR / "planning_hypotheses.json",
    "validation": OUTPUT_DIR / "professional_validation_interface.json",
    "expert_reviews": OUTPUT_DIR / "expert_review_records.json",
    "approval_support": OUTPUT_DIR / "planning_approval_support_report.json",
}
SAFETY_BOUNDARY = (
    "Internal planning support only. This layer does not make governance decisions, "
    "grant approval, provide professional validation, establish engineering or "
    "regulatory readiness, or replace qualified human review."
)


def _load(path: Path) -> dict | None:
    if not path.exists() or not path.read_text(encoding="utf-8").strip():
        return None
    return json.loads(path.read_text(encoding="utf-8"))


def _scenario_item(items: list[dict], scenario_name: str) -> dict | None:
    return next((item for item in items if item.get("scenario") == scenario_name), None)


def _expert_item(source: dict | None, scenario_name: str) -> dict | None:
    return next((item for item in (source or {}).get("records", [])
                 if item.get("reviewed_scenario_or_module") == scenario_name), None)


def _status_for(traces, hypothesis, validation, expert, approval) -> str:
    if not traces or not hypothesis or not validation or not expert or not approval:
        return "deferred"
    trace_values = {str(value).lower() for trace in traces
                    for value in (trace.get("evidence_strength"), trace.get("review_status"))
                    if value is not None}
    if (hypothesis.get("hypothesis_status") == "not_supported"
            or "not_supported" in trace_values
            or "not_supported_by_current_evidence" in trace_values):
        return "not_supported_by_current_evidence"
    if (validation.get("review_status") == "awaiting_professional_review"
            or expert.get("decision_status") == "not_reviewed"
            or approval.get("approval_support_status") != "not_ready_for_approval"):
        return "requires_further_review"
    if expert.get("decision_status") in {"approved_for_further_assessment", "conditional"}:
        return "conditionally_supported_for_internal_planning"
    return "not_decided"


def _build_record(scenario_id: str, scenario_name: str, sources: dict) -> dict:
    traces = [item for item in (sources.get("traceability") or {}).get("records", [])
              if item.get("scenario_id") == scenario_id]
    hypothesis = (sources.get("hypotheses") or {}).get("hypotheses", {}).get(scenario_id)
    validation = (sources.get("validation") or {}).get("reviews", {}).get(scenario_id)
    expert = _expert_item(sources.get("expert_reviews"), scenario_name)
    approval = _scenario_item((sources.get("approval_support") or {}).get("scenarios", []), scenario_name)
    missing = [label for label, value in (
        ("evidence traceability", traces), ("planning hypothesis", hypothesis),
        ("professional validation record", validation), ("expert review record", expert),
        ("planning approval support record", approval),
    ) if not value]
    trace_ids = sorted(item["trace_id"] for item in traces)
    insufficient_types = sorted({item.get("artifact_type", "unknown") for item in traces
                                 if item.get("evidence_strength") == "insufficient_evidence"})
    gaps = [f"Missing {item}." for item in missing]
    gaps.extend(f"{item.replace('_', ' ')} remains insufficient evidence."
                for item in insufficient_types)
    if validation and validation.get("review_status") == "awaiting_professional_review":
        gaps.append("Professional validation remains incomplete.")
    if expert and expert.get("decision_status") == "not_reviewed":
        gaps.append("Expert review remains incomplete.")
    actions = list((approval or {}).get("recommended_next_steps", [])) or [
        "Restore the missing local source artifacts.",
        "Complete qualified professional and expert review.",
        "Re-run the deterministic support layer after source records are updated.",
    ]
    validation_refs = []
    if validation:
        validation_refs.append(f"professional_validation:{validation.get('review_status', 'unknown')}")
    if expert:
        validation_refs.append(f"expert_review:{expert.get('decision_status', 'unknown')}")
    return {
        "decision_record_id": f"{scenario_id}:internal_governance_support",
        "scenario_id": scenario_id, "scenario_name": scenario_name,
        "internal_decision_status": _status_for(traces, hypothesis, validation, expert, approval),
        "external_approval_status": "not_ready_for_approval",
        "evidence_trace_ids": trace_ids,
        "planning_hypothesis_reference": (hypothesis or {}).get("hypothesis_id"),
        "validation_references": validation_refs,
        "evidence_summary": f"{len(trace_ids)} local trace records were considered. The record organizes existing evidence for internal human review only.",
        "unresolved_evidence_gaps": gaps,
        "unresolved_risks": list((approval or {}).get("unresolved_risks", [])),
        "required_human_actions": actions,
        "human_review_required": True, "professional_review_required": True,
        "limitations": [SAFETY_BOUNDARY,
            "The status is not a planning, regulatory, engineering, environmental, or construction approval.",
            "No scenario comparison, prioritization, forecast, simulation, GIS/DEM operation, API call, or LLM call is performed."],
    }


def build_governance_decision_records(sources=None) -> dict:
    loaded = sources or {key: _load(path) for key, path in SOURCE_PATHS.items()}
    records = [_build_record(scenario_id, scenario_name, loaded)
               for scenario_id, scenario_name in SCENARIOS.items()]
    return {"schema_version": SCHEMA_VERSION,
            "runtime": "Internal Governance Decision Support Layer",
            "safety_boundary": SAFETY_BOUNDARY,
            "allowed_internal_decision_statuses": list(ALLOWED_STATUSES),
            "external_approval_status": "not_ready_for_approval",
            "record_count": len(records), "records": records}


def render_markdown_report(output: dict) -> str:
    lines = ["# Internal Governance Decision Support", "", output["safety_boundary"], "",
             "All external approval statuses remain `not_ready_for_approval`.", ""]
    for record in output["records"]:
        lines += [f"## {record['scenario_name']}", "",
            f"- Internal status: `{record['internal_decision_status']}`",
            f"- External approval status: `{record['external_approval_status']}`",
            f"- Evidence traces: {len(record['evidence_trace_ids'])}",
            f"- Planning hypothesis: `{record['planning_hypothesis_reference'] or 'missing'}`",
            f"- Human review required: `{record['human_review_required']}`",
            f"- Professional review required: `{record['professional_review_required']}`", "",
            "Unresolved evidence gaps:", "",
            *([f"- {item}" for item in record["unresolved_evidence_gaps"]] or ["- None recorded."]), "",
            "Required human actions:", "", *[f"- {item}" for item in record["required_human_actions"]], "",
            "Trace references:", "",
            *([f"- `{item}`" for item in record["evidence_trace_ids"]] or ["- No trace records available."]), ""]
    return "\n".join(lines).rstrip() + "\n"


def write_governance_decision_outputs(output, output_path=OUTPUT_PATH, report_path=REPORT_PATH) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(output, indent=2, ensure_ascii=True) + "\n", encoding="utf-8")
    report_path.write_text(render_markdown_report(output), encoding="utf-8")


def main() -> None:
    output = build_governance_decision_records()
    write_governance_decision_outputs(output)
    print(f"Wrote governance decision support outputs to {OUTPUT_DIR}")


if __name__ == "__main__":
    main()
