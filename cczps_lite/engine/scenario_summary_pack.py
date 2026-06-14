"""Build a deterministic, local-only Scenario Summary Pack."""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any

PROJECT_DIR = Path(__file__).resolve().parent.parent
OUTPUT_DIR = PROJECT_DIR / "output"
CONSOLIDATED_DIR = OUTPUT_DIR / "consolidated"
OUTPUT_PATH = CONSOLIDATED_DIR / "scenario_summary_pack.json"
REPORT_PATH = CONSOLIDATED_DIR / "scenario_summary_pack.md"
PACK_NAME = "CCZPS-Lite Scenario Summary Pack"
PACK_VERSION = "0.1"
SAFETY_BOUNDARY = (
    "Summary only. This pack reorganises existing local outputs and does not "
    "create evidence, conclusions, approvals, recommendations, rankings, "
    "engineering determinations, or regulatory determinations."
)
SOURCE_PATHS = {
    "intake": OUTPUT_DIR / "location_intake_profiles.json",
    "location_meteorology": OUTPUT_DIR / "location_meteorology_evidence.json",
    "meteorology": OUTPUT_DIR / "meteorology_evidence.json",
    "trends": OUTPUT_DIR / "meteorology_trends.json",
    "hypotheses": OUTPUT_DIR / "planning_hypotheses.json",
    "traceability": OUTPUT_DIR / "evidence_traceability.json",
    "governance": OUTPUT_DIR / "governance_decision_records.json",
    "comparison": OUTPUT_DIR / "scenario_comparison.json",
    "approval_support": OUTPUT_DIR / "planning_approval_support_report.json",
}
DEFAULT_LIMITATIONS = [
    "Summary only",
    "No planning conclusion",
    "No approval readiness",
    "No engineering or regulatory determination",
]
ESTABLISHED_SCENARIO_NAMES = {
    "batlow": "Batlow",
    "kunlun": "Kunlun",
    "iraq": "Iraq",
    "baiyangdian_xiongan": "Baiyangdian-Xiong'an",
}


def _load(path: Path) -> dict[str, Any] | None:
    if not path.exists() or not path.read_text(encoding="utf-8").strip():
        return None
    return json.loads(path.read_text(encoding="utf-8"))


def load_sources(output_dir: Path = OUTPUT_DIR) -> dict[str, dict[str, Any] | None]:
    return {
        key: _load(output_dir / path.name)
        for key, path in SOURCE_PATHS.items()
    }


def _items(source: dict[str, Any] | None, field: str) -> list[dict[str, Any]]:
    value = (source or {}).get(field, [])
    return value if isinstance(value, list) else []


def _find(items: list[dict[str, Any]], field: str, value: str) -> dict[str, Any] | None:
    return next((item for item in items if item.get(field) == value), None)


def _unique(values: list[str]) -> list[str]:
    return list(dict.fromkeys(value for value in values if value))


def _review_required(*records: dict[str, Any] | None, field: str) -> bool:
    explicit = [record[field] for record in records if record and field in record]
    return all(explicit) if explicit else True


def _approval_status(*records: dict[str, Any] | None) -> str:
    values = [
        record.get("approval_support_status") or record.get("external_approval_status")
        for record in records
        if record
    ]
    return "not_ready_for_approval" if "not_ready_for_approval" in values or not values else "not_ready_for_approval"


def _established_ids(sources: dict[str, dict[str, Any] | None]) -> list[str]:
    found = {
        record.get("scenario_id")
        for record in _items(sources.get("comparison"), "records")
        + _items(sources.get("governance"), "records")
        + _items(sources.get("traceability"), "records")
        if record.get("scenario_id") in ESTABLISHED_SCENARIO_NAMES
    }
    hypotheses = (sources.get("hypotheses") or {}).get("hypotheses", {})
    found.update(key for key in hypotheses if key in ESTABLISHED_SCENARIO_NAMES)
    return [scenario_id for scenario_id in ESTABLISHED_SCENARIO_NAMES if scenario_id in found]


def _established_record(
    scenario_id: str,
    sources: dict[str, dict[str, Any] | None],
) -> dict[str, Any]:
    name = ESTABLISHED_SCENARIO_NAMES[scenario_id]
    comparison = _find(_items(sources.get("comparison"), "records"), "scenario_id", scenario_id)
    governance = _find(_items(sources.get("governance"), "records"), "scenario_id", scenario_id)
    approval = _find(_items(sources.get("approval_support"), "scenarios"), "scenario", name)
    hypothesis = (sources.get("hypotheses") or {}).get("hypotheses", {}).get(scenario_id)
    traces = [
        record
        for record in _items(sources.get("traceability"), "records")
        if record.get("scenario_id") == scenario_id
    ]
    meteorology = (sources.get("meteorology") or {}).get("scenarios", {}).get(scenario_id)
    evidence_strength = (comparison or {}).get("evidence_strength", "insufficient_evidence")
    hypothesis_status = (hypothesis or {}).get("hypothesis_status", "not_generated")
    trace_status = (comparison or {}).get(
        "traceability_status", "available" if traces else "not_available"
    )
    governance_status = (governance or {}).get(
        "internal_decision_status", "requires_further_review"
    )
    expert_status = (comparison or {}).get("expert_review_status", "not_reviewed")
    professional_status = (comparison or {}).get(
        "professional_validation_status", "awaiting_professional_review"
    )
    meteorology_status = (meteorology or {}).get(
        "retrieval_status", (comparison or {}).get("meteorology_trend_status", "not_available")
    )
    actions = list((governance or {}).get("required_human_actions", []))
    if not actions:
        actions = list((approval or {}).get("recommended_next_steps", []))
    if not actions:
        actions = [
            "restore or generate missing local evidence",
            "complete professional review",
            "record expert review findings",
        ]
    limitations = _unique(
        list((governance or {}).get("limitations", [])) + DEFAULT_LIMITATIONS
    )
    current_knowledge = (
        f"The system has {len(traces)} traceable local evidence record(s). "
        f"Current evidence strength is {evidence_strength}, meteorology status is "
        f"{meteorology_status}, and the planning hypothesis status is {hypothesis_status}."
    )
    cannot_conclude = (
        "The available records do not establish causation, professional validity, "
        "engineering readiness, regulatory readiness, or approval readiness."
    )
    return {
        # Minimal core mapping: Scenario identity, Evidence summary, Hypothesis
        # summary, Review boundary, and a plain-language Report record.
        "scenario_id": scenario_id,
        "scenario_name": name,
        "location_name": (meteorology or {}).get("location_name", name),
        "country": "not_available",
        "region": "not_available",
        "latitude": None,
        "longitude": None,
        "scenario_type": "established_demonstration_scenario",
        "scenario_status": "existing_scenario",
        "workflow_status": governance_status,
        "summary_status": governance_status,
        "evidence_status": evidence_strength,
        "meteorology_status": meteorology_status,
        "planning_hypothesis_status": hypothesis_status,
        "evidence_traceability_status": trace_status,
        "internal_governance_status": governance_status,
        "expert_review_status": expert_status,
        "professional_review_status": professional_status,
        "approval_support_status": _approval_status(comparison, governance, approval),
        "human_review_required": _review_required(
            comparison, governance, field="human_review_required"
        ),
        "professional_review_required": _review_required(
            comparison, governance, field="professional_review_required"
        ),
        "plain_language_summary": (
            f"{name} is an existing CCZPS-Lite demonstration scenario with "
            f"{evidence_strength} evidence and a {hypothesis_status} planning "
            "hypothesis. Further human and professional review remains required."
        ),
        "current_evidence_summary": current_knowledge,
        "planning_hypothesis_summary": (
            (hypothesis or {}).get("planning_assumption")
            or (approval or {}).get("planning_hypothesis")
            or "No planning hypothesis is available in the current local sources."
        ),
        "what_the_system_currently_knows": current_knowledge,
        "what_the_system_cannot_conclude_yet": cannot_conclude,
        "review_summary": (
            f"Internal governance status is {governance_status}; expert review is "
            f"{expert_status}; professional review is {professional_status}; "
            "approval support remains not_ready_for_approval."
        ),
        "next_human_review_actions": actions,
        "limitations": limitations,
        "source_references": _unique(
            [record.get("trace_id", "") for record in traces]
            + [(hypothesis or {}).get("hypothesis_id", "")]
        ),
    }


def _intake_record(
    profile: dict[str, Any],
    sources: dict[str, dict[str, Any] | None],
) -> dict[str, Any]:
    scenario_id = profile["scenario_id"]
    meteorology_records = [
        record
        for record in _items(sources.get("location_meteorology"), "records")
        if record.get("scenario_id") == scenario_id
    ]
    meteorology = meteorology_records[-1] if meteorology_records else None
    meteorology_status = (meteorology or {}).get(
        "meteorology_status", profile.get("meteorology_status", "not_available")
    )
    has_meteorology = meteorology_status == "success"
    current_knowledge = (
        "The system has a structured location intake profile"
        + (" and governed meteorology evidence." if has_meteorology else ".")
        + " Broader environmental evidence and professional validation are not complete."
    )
    return {
        "scenario_id": scenario_id,
        "scenario_name": profile.get("location_name", scenario_id),
        "location_name": profile.get("location_name", "not_available"),
        "country": profile.get("country", "not_available"),
        "region": profile.get("region", "not_available"),
        "latitude": profile.get("latitude"),
        "longitude": profile.get("longitude"),
        "scenario_type": profile.get("intake_context", "intake_profile"),
        "scenario_status": profile.get("scenario_status", "intake_only"),
        "workflow_status": profile.get("workflow_status", "requires_further_review"),
        "summary_status": profile.get("scenario_status", "intake_only"),
        "evidence_status": profile.get("evidence_status", "not_generated"),
        "meteorology_status": meteorology_status,
        "planning_hypothesis_status": profile.get(
            "planning_hypothesis_status", "not_generated"
        ),
        "evidence_traceability_status": "not_available",
        "internal_governance_status": "requires_further_review",
        "expert_review_status": "not_reviewed",
        "professional_review_status": "awaiting_professional_review",
        "approval_support_status": _approval_status(profile, meteorology),
        "human_review_required": _review_required(
            profile, meteorology, field="human_review_required"
        ),
        "professional_review_required": _review_required(
            profile, meteorology, field="professional_review_required"
        ),
        "plain_language_summary": (
            f"{profile.get('location_name', scenario_id)} is currently a preliminary "
            "intake scenario. Evidence generation and professional review are still required."
        ),
        "current_evidence_summary": current_knowledge,
        "planning_hypothesis_summary": (
            "No validated planning hypothesis has been generated for this intake profile."
        ),
        "what_the_system_currently_knows": current_knowledge,
        "what_the_system_cannot_conclude_yet": (
            "The intake profile cannot support a planning conclusion, professional "
            "determination, recommendation, or approval decision."
        ),
        "review_summary": (
            "Human and professional review are required before this intake profile "
            "can support any planning decision."
        ),
        "next_human_review_actions": list(profile.get("recommended_next_steps", []))
        or ["generate governed evidence", "request professional review"],
        "limitations": _unique(
            list(profile.get("limitations", []))
            + list((meteorology or {}).get("limitations", []))
            + DEFAULT_LIMITATIONS
        ),
        "source_references": _unique(
            [
                "location_intake_profiles.json",
                "location_meteorology_evidence.json" if meteorology else "",
            ]
        ),
    }


def build_scenario_summary_pack(
    sources: dict[str, dict[str, Any] | None] | None = None,
) -> dict[str, Any]:
    loaded = sources if sources is not None else load_sources()
    records = [
        _established_record(scenario_id, loaded)
        for scenario_id in _established_ids(loaded)
    ]
    records.extend(
        _intake_record(profile, loaded)
        for profile in _items(loaded.get("intake"), "scenario_profiles")
    )
    return {
        "pack_name": PACK_NAME,
        "pack_version": PACK_VERSION,
        "minimal_core_mapping": {
            "Scenario": "scenario identity and context",
            "Evidence": "current evidence summary",
            "Hypothesis": "planning hypothesis summary",
            "Review": "human, professional, and governance status",
            "Report": "plain-language scenario summary",
        },
        "safety_boundary": SAFETY_BOUNDARY,
        "generated_from": [
            path.name for key, path in SOURCE_PATHS.items() if loaded.get(key) is not None
        ],
        "scenario_count": len(records),
        "scenarios": records,
    }


def _status(value: Any) -> str:
    return "not_available" if value is None else str(value)


def render_markdown_report(pack: dict[str, Any]) -> str:
    lines = [
        f"# {pack['pack_name']}",
        "",
        pack["safety_boundary"],
        "",
        (
            "This report presents the minimal core objects as Scenario, Evidence, "
            "Hypothesis, Review, and Report. It summarises local source files only."
        ),
    ]
    for scenario in pack["scenarios"]:
        lines += [
            "",
            f"## Scenario: {scenario['scenario_name']}",
            "",
            "### Plain-language summary",
            "",
            scenario["plain_language_summary"],
            "",
            "### What the system currently knows",
            "",
            scenario["what_the_system_currently_knows"],
            "",
            "### What the system cannot conclude yet",
            "",
            scenario["what_the_system_cannot_conclude_yet"],
            "",
            "### Current review status",
            "",
            scenario["review_summary"],
            "",
            f"- Scenario status: `{_status(scenario['scenario_status'])}`",
            f"- Evidence status: `{_status(scenario['evidence_status'])}`",
            f"- Meteorology status: `{_status(scenario['meteorology_status'])}`",
            (
                "- Planning hypothesis status: "
                f"`{_status(scenario['planning_hypothesis_status'])}`"
            ),
            (
                "- Approval support status: "
                f"`{_status(scenario['approval_support_status'])}`"
            ),
            f"- Human review required: `{scenario['human_review_required']}`",
            (
                "- Professional review required: "
                f"`{scenario['professional_review_required']}`"
            ),
            "",
            "### Next human review actions",
            "",
            *[f"- {item}" for item in scenario["next_human_review_actions"]],
            "",
            "### Limitations",
            "",
            *[f"- {item}" for item in scenario["limitations"]],
        ]
    return "\n".join(lines).rstrip() + "\n"


def write_scenario_summary_outputs(
    pack: dict[str, Any],
    output_path: Path = OUTPUT_PATH,
    report_path: Path = REPORT_PATH,
) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(
        json.dumps(pack, indent=2, ensure_ascii=True) + "\n", encoding="utf-8"
    )
    report_path.write_text(render_markdown_report(pack), encoding="utf-8")


def main() -> None:
    pack = build_scenario_summary_pack()
    write_scenario_summary_outputs(pack)
    print(f"Wrote Scenario Summary Pack outputs to {CONSOLIDATED_DIR}")


if __name__ == "__main__":
    main()
