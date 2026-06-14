"""Build a deterministic, local-only Evidence Review Pack."""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any

PROJECT_DIR = Path(__file__).resolve().parent.parent
OUTPUT_DIR = PROJECT_DIR / "output"
CONSOLIDATED_DIR = OUTPUT_DIR / "consolidated"
OUTPUT_PATH = CONSOLIDATED_DIR / "evidence_review_pack.json"
REPORT_PATH = CONSOLIDATED_DIR / "evidence_review_pack.md"
PACK_NAME = "CCZPS-Lite Evidence Review Pack"
PACK_VERSION = "0.1"
PACK_PURPOSE = "Consolidated technical evidence review for CCZPS-Lite scenarios."
SAFETY_BOUNDARY = (
    "Evidence review only. This pack organises existing local records and does "
    "not create evidence, scientific confirmation, professional conclusions, "
    "approvals, recommendations, rankings, or engineering or regulatory determinations."
)
SOURCE_PATHS = {
    "meteorology": OUTPUT_DIR / "meteorology_evidence.json",
    "location_meteorology": OUTPUT_DIR / "location_meteorology_evidence.json",
    "timeseries": OUTPUT_DIR / "meteorology_timeseries.json",
    "trends": OUTPUT_DIR / "meteorology_trends.json",
    "transects": OUTPUT_DIR / "spatial_transect_scenario_pack.json",
    "gis_dem": OUTPUT_DIR / "gis_dem_access_plan.json",
    "hypotheses": OUTPUT_DIR / "planning_hypotheses.json",
    "traceability": OUTPUT_DIR / "evidence_traceability.json",
    "validation": OUTPUT_DIR / "professional_validation_interface.json",
    "approval_support": OUTPUT_DIR / "planning_approval_support_report.json",
    "scenario_summary": CONSOLIDATED_DIR / "scenario_summary_pack.json",
}
METEOROLOGY_IDS = {
    "batlow": ["batlow"],
    "kunlun": ["kunlun"],
    "iraq": ["iraq"],
    "baiyangdian_xiongan": [
        "xiongan_wutai_headwaters",
        "xiongan_baiyangdian_wetland",
        "xiongan_downstream",
    ],
}
DEFAULT_LIMITATIONS = [
    "Evidence review only",
    "No professional conclusion",
    "No approval readiness",
    "No engineering or regulatory determination",
]


def _load(path: Path) -> dict[str, Any] | None:
    if not path.exists() or not path.read_text(encoding="utf-8").strip():
        return None
    return json.loads(path.read_text(encoding="utf-8"))


def load_sources(output_dir: Path = OUTPUT_DIR) -> dict[str, dict[str, Any] | None]:
    consolidated_dir = output_dir / "consolidated"
    return {
        key: _load(
            consolidated_dir / path.name
            if key == "scenario_summary"
            else output_dir / path.name
        )
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


def _coverage(record_count: int, expected_count: int = 1) -> str:
    if record_count <= 0:
        return "not_available"
    if record_count < expected_count:
        return "partially_available"
    return "available"


def _meteorology_records(
    scenario: dict[str, Any],
    sources: dict[str, dict[str, Any] | None],
) -> list[dict[str, Any]]:
    scenario_id = scenario["scenario_id"]
    if scenario_id.endswith("_intake"):
        return [
            record
            for record in _items(sources.get("location_meteorology"), "records")
            if record.get("scenario_id") == scenario_id
        ]
    source = (sources.get("meteorology") or {}).get("scenarios", {})
    return [
        source[item_id]
        for item_id in METEOROLOGY_IDS.get(scenario_id, [scenario_id])
        if item_id in source
    ]


def _timeseries_records(
    scenario_id: str,
    sources: dict[str, dict[str, Any] | None],
) -> list[dict[str, Any]]:
    ids = set(METEOROLOGY_IDS.get(scenario_id, [scenario_id]))
    return [
        record
        for record in _items(sources.get("timeseries"), "observations")
        if record.get("scenario_id") in ids
    ]


def _trend_records(
    scenario_id: str,
    sources: dict[str, dict[str, Any] | None],
) -> list[dict[str, Any]]:
    ids = METEOROLOGY_IDS.get(scenario_id, [scenario_id])
    trends = (sources.get("trends") or {}).get("scenarios", {})
    return [trends[item_id] for item_id in ids if item_id in trends]


def _missing_evidence(
    coverage: dict[str, str],
    spatial: dict[str, Any] | None,
    validation: dict[str, Any] | None,
    traces: list[dict[str, Any]],
) -> list[str]:
    missing = []
    labels = {
        "meteorology": "meteorology evidence",
        "time_series": "meteorology time-series evidence",
        "trends": "meteorology trend evidence",
        "spatial_transects": "configured spatial transect evidence",
    }
    for key, label in labels.items():
        if coverage[key] in {"not_available", "not_generated", "partially_available"}:
            missing.append(label)
    missing.append("professional GIS / DEM evidence and verification")
    if not spatial or spatial.get("field_validation_claim") != "claimed":
        missing.append("field verification of configured spatial relationships")
    if not validation or validation.get("review_status") == "awaiting_professional_review":
        missing.append("completed qualified professional review")
    if any(trace.get("evidence_strength") == "insufficient_evidence" for trace in traces):
        missing.append("resolution of trace records marked insufficient evidence")
    return _unique(missing)


def _record(
    scenario: dict[str, Any],
    sources: dict[str, dict[str, Any] | None],
) -> dict[str, Any]:
    scenario_id = scenario["scenario_id"]
    meteorology = _meteorology_records(scenario, sources)
    timeseries = _timeseries_records(scenario_id, sources)
    trends = _trend_records(scenario_id, sources)
    transect = _find(
        _items(sources.get("transects"), "scenarios"), "scenario_id", scenario_id
    )
    hypothesis = (sources.get("hypotheses") or {}).get("hypotheses", {}).get(scenario_id)
    traces = [
        item
        for item in _items(sources.get("traceability"), "records")
        if item.get("scenario_id") == scenario_id
    ]
    validation = (sources.get("validation") or {}).get("reviews", {}).get(scenario_id)
    approval = _find(
        _items(sources.get("approval_support"), "scenarios"),
        "scenario",
        scenario["scenario_name"],
    )
    expected_meteorology = len(METEOROLOGY_IDS.get(scenario_id, [scenario_id]))
    coverage = {
        "meteorology": _coverage(len(meteorology), expected_meteorology),
        "time_series": _coverage(
            len({item.get("scenario_id") for item in timeseries}), expected_meteorology
        ),
        "trends": _coverage(len(trends), expected_meteorology),
        "spatial_transects": (
            "available"
            if transect and not transect.get("missing_data_points")
            else "partially_available"
            if transect
            else "not_available"
        ),
        "gis_dem": (
            "planning_only"
            if (sources.get("gis_dem") or {}).get("implementation_status")
            == "planning_only"
            else "not_available"
        ),
        "professional_validation": (
            (validation or {}).get("review_status", "not_available")
        ),
    }
    trace_strengths = {
        item.get("evidence_strength")
        for item in traces
        if item.get("evidence_strength")
    }
    if scenario_id.endswith("_intake") or not traces:
        evidence_strength = "insufficient"
    elif "insufficient_evidence" in trace_strengths:
        evidence_strength = "low"
    else:
        evidence_strength = scenario.get("evidence_status", "unknown")
    if evidence_strength not in {"low", "medium", "high", "insufficient", "unknown"}:
        evidence_strength = "insufficient"
    review_incomplete = (
        not validation
        or validation.get("review_status") == "awaiting_professional_review"
        or coverage["gis_dem"] != "available"
        or any(value in {"not_available", "partially_available"} for value in coverage.values())
    )
    uncertainty = "high" if review_incomplete else "unknown"
    missing = _missing_evidence(coverage, transect, validation, traces)
    trace_ids = sorted(item["trace_id"] for item in traces if item.get("trace_id"))
    validation_refs = []
    if validation:
        validation_refs.append(
            f"professional_validation:{validation.get('review_status', 'not_available')}"
        )
        validation_refs.extend(
            f"required_discipline:{item}"
            for item in validation.get("required_disciplines", [])
        )
    hypothesis_refs = []
    if hypothesis:
        hypothesis_refs.append(hypothesis.get("hypothesis_id", ""))
        hypothesis_refs.extend(hypothesis.get("supporting_evidence", []))
    limitations = _unique(
        list(scenario.get("limitations", []))
        + list((approval or {}).get("unresolved_risks", []))
        + DEFAULT_LIMITATIONS
    )
    return {
        "scenario_id": scenario_id,
        "scenario_name": scenario["scenario_name"],
        "scenario_status": scenario.get("scenario_status", "not_available"),
        "evidence_review_status": "requires_further_review",
        "evidence_coverage": coverage,
        "meteorology_evidence_status": coverage["meteorology"],
        "meteorology_time_series_status": coverage["time_series"],
        "meteorology_trend_status": coverage["trends"],
        "spatial_transect_status": coverage["spatial_transects"],
        "gis_dem_evidence_status": coverage["gis_dem"],
        "professional_validation_status": coverage["professional_validation"],
        "evidence_strength": evidence_strength,
        "evidence_strength_summary": (
            f"Current evidence strength is {evidence_strength}. "
            "The pack records source availability only; it does not increase evidence strength."
        ),
        "uncertainty_level": uncertainty,
        "uncertainty_summary": (
            "Uncertainty remains high because professional review and GIS / DEM "
            "evidence are incomplete or absent."
        ),
        "missing_evidence": missing,
        "planning_hypothesis_evidence_references": _unique(hypothesis_refs),
        "traceability_references": trace_ids,
        "validation_references": _unique(validation_refs),
        "supported_outputs": _unique(
            [
                "planning_hypothesis" if hypothesis else "",
                "scenario_summary",
                "governance_decision_support" if traces else "",
            ]
        ),
        "professional_review_requirements": (
            list((validation or {}).get("required_disciplines", []))
            or [
                "qualified environmental or planning review",
                "GIS / terrain or hydrology review where relevant",
            ]
        ),
        "human_review_required": _review_required(
            scenario, field="human_review_required"
        ),
        "professional_review_required": _review_required(
            scenario, field="professional_review_required"
        ),
        "approval_support_status": "not_ready_for_approval",
        "limitations": limitations,
    }


def build_evidence_review_pack(
    sources: dict[str, dict[str, Any] | None] | None = None,
) -> dict[str, Any]:
    loaded = sources if sources is not None else load_sources()
    scenarios = _items(loaded.get("scenario_summary"), "scenarios")
    return {
        "pack_name": PACK_NAME,
        "pack_version": PACK_VERSION,
        "pack_purpose": PACK_PURPOSE,
        "minimal_core_mapping": {
            "Scenario": "scenario identity and context",
            "Evidence": "meteorology, trends, spatial context, GIS / DEM status, and traceability",
            "Hypothesis": "evidence references supporting planning hypotheses",
            "Review": "professional validation and missing review status",
            "Report": "technical evidence review package",
        },
        "safety_boundary": SAFETY_BOUNDARY,
        "coverage_status_values": [
            "available",
            "partially_available",
            "planning_only",
            "not_generated",
            "not_available",
            "insufficient_evidence",
            "requires_further_review",
        ],
        "generated_from": [
            path.name for key, path in SOURCE_PATHS.items() if loaded.get(key) is not None
        ],
        "record_count": len(scenarios),
        "review_records": [_record(scenario, loaded) for scenario in scenarios],
    }


def render_markdown_report(pack: dict[str, Any]) -> str:
    lines = [
        f"# {pack['pack_name']}",
        "",
        pack["pack_purpose"],
        "",
        pack["safety_boundary"],
    ]
    for record in pack["review_records"]:
        coverage = record["evidence_coverage"]
        lines += [
            "",
            f"## Scenario: {record['scenario_name']}",
            "",
            "### Evidence coverage",
            "",
            f"- Meteorology: `{coverage['meteorology']}`",
            f"- Time series: `{coverage['time_series']}`",
            f"- Trends: `{coverage['trends']}`",
            f"- Spatial transects: `{coverage['spatial_transects']}`",
            f"- GIS / DEM: `{coverage['gis_dem']}`",
            f"- Professional validation: `{coverage['professional_validation']}`",
            "",
            "### Evidence strength",
            "",
            record["evidence_strength_summary"],
            "",
            "### Meteorology evidence",
            "",
            (
                f"Meteorology is `{record['meteorology_evidence_status']}`, "
                f"time-series evidence is `{record['meteorology_time_series_status']}`, "
                f"and trend evidence is `{record['meteorology_trend_status']}`."
            ),
            "",
            "### Spatial evidence",
            "",
            (
                f"Configured spatial transect evidence is "
                f"`{record['spatial_transect_status']}`. Configured relationships "
                "are not field verification or GIS-derived conclusions."
            ),
            "",
            "### GIS / DEM status",
            "",
            (
                f"GIS / DEM status is `{record['gis_dem_evidence_status']}`. "
                "A planning-only access plan is not spatial evidence."
            ),
            "",
            "### Traceability references",
            "",
            *(
                [f"- `{item}`" for item in record["traceability_references"]]
                or ["- No traceability references are available."]
            ),
            "",
            "### Uncertainty and missing evidence",
            "",
            f"Uncertainty level: `{record['uncertainty_level']}`.",
            "",
            record["uncertainty_summary"],
            "",
            *[f"- {item}" for item in record["missing_evidence"]],
            "",
            "### Professional review requirements",
            "",
            *[f"- {item}" for item in record["professional_review_requirements"]],
            "",
            f"- Human review required: `{record['human_review_required']}`",
            f"- Professional review required: `{record['professional_review_required']}`",
            f"- Approval support status: `{record['approval_support_status']}`",
            "",
            "### Limitations",
            "",
            *[f"- {item}" for item in record["limitations"]],
        ]
    return "\n".join(lines).rstrip() + "\n"


def write_evidence_review_outputs(
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
    pack = build_evidence_review_pack()
    write_evidence_review_outputs(pack)
    print(f"Wrote Evidence Review Pack outputs to {CONSOLIDATED_DIR}")


if __name__ == "__main__":
    main()
