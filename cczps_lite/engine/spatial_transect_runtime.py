"""Provider-agnostic spatial context and transect runtime for CCZPS-Lite."""
from __future__ import annotations
import json
from datetime import datetime, timezone
from pathlib import Path

PROJECT_DIR = Path(__file__).resolve().parent.parent
INPUT_PATH = PROJECT_DIR / "input" / "spatial_transects.json"
OUTPUT_PATH = PROJECT_DIR / "output" / "spatial_transects.json"
REPORT_PATH = PROJECT_DIR / "output" / "spatial_transects.md"
SCENARIO_PACK_PATH = PROJECT_DIR / "output" / "spatial_transect_scenario_pack.json"
SCENARIO_PACK_REPORT_PATH = PROJECT_DIR / "output" / "spatial_transect_scenario_pack.md"
SCHEMA_VERSION = "1.0"
CORE_ROLE = "core"
REFERENCE_ROLES = ("upstream", "downstream", "upwind", "downwind", "highland", "lowland", "lateral")
POINT_ROLES = (CORE_ROLE, *REFERENCE_ROLES)
FUTURE_COMPATIBLE_SOURCES = ("Google Earth", "DEM", "watershed analysis", "wind corridor data", "ENVI-met", "Fluent", "other spatial computation tools")
SAFETY_BOUNDARY = "Configured spatial relationship evidence only. No automatic point selection, GIS calls, DEM calls, mapping calls, weather calls, simulations, forecasts, hydrology inference, wind inference, design advice, or construction advice."


def load_transect_configuration(path: Path = INPUT_PATH) -> dict:
    with path.open("r", encoding="utf-8") as file_obj:
        config = json.load(file_obj)
    if not isinstance(config.get("transects"), list):
        raise ValueError("spatial transect configuration requires a transects list")
    return config


def _validate_coordinates(coordinates: object) -> tuple[dict | None, list[str]]:
    if coordinates is None:
        return None, ["missing_coordinates"]
    if not isinstance(coordinates, dict):
        return None, ["invalid_coordinates"]
    latitude = coordinates.get("latitude")
    longitude = coordinates.get("longitude")
    if not isinstance(latitude, (int, float)) or not isinstance(longitude, (int, float)):
        return None, ["invalid_coordinates"]
    return {"latitude": float(latitude), "longitude": float(longitude)}, []


def _copy_optional_fields(point: dict, output: dict) -> None:
    for field in ("direction_label", "direction_degrees", "distance_km", "elevation_m", "elevation_context", "source", "confidence", "status", "notes", "support_basis"):
        output[field] = point.get(field)


def normalize_point(point: dict, expected_roles: tuple[str, ...], seen_ids: set[str]) -> tuple[dict, list[str]]:
    issues: list[str] = []
    point_id = point.get("point_id")
    role = point.get("role")
    if not point_id:
        issues.append("missing_point_id")
        point_id = "missing_point_id"
    elif point_id in seen_ids:
        issues.append(f"duplicate_point_id:{point_id}")
    seen_ids.add(point_id)
    if role not in expected_roles:
        issues.append(f"invalid_role:{role}")
    coordinates, coordinate_issues = _validate_coordinates(point.get("coordinates"))
    issues.extend(issue for issue in coordinate_issues if issue != "missing_coordinates")
    normalized = {"point_id": point_id, "role": role, "name": point.get("name"), "coordinates": coordinates, "missing_data_status": ",".join(coordinate_issues) if coordinate_issues else "complete"}
    _copy_optional_fields(point, normalized)
    normalized["validation_issues"] = issues
    return normalized, issues


def validate_transect(transect: dict) -> dict:
    seen_ids: set[str] = set()
    validation_errors: list[str] = []
    core_location = transect.get("core_location")
    if not isinstance(core_location, dict):
        core_location = {"point_id": "missing_core_location", "role": CORE_ROLE, "coordinates": None}
        validation_errors.append("missing_core_location")
    normalized_core, core_issues = normalize_point(core_location, (CORE_ROLE,), seen_ids)
    validation_errors.extend(f"core:{issue}" for issue in core_issues)
    reference_points = transect.get("reference_points", [])
    if not isinstance(reference_points, list):
        validation_errors.append("reference_points_not_list")
        reference_points = []
    normalized_references = []
    role_counts = {role: 0 for role in REFERENCE_ROLES}
    for point in reference_points:
        if not isinstance(point, dict):
            validation_errors.append("invalid_reference_point")
            continue
        normalized_point, point_issues = normalize_point(point, REFERENCE_ROLES, seen_ids)
        if normalized_point.get("role") in role_counts:
            role_counts[normalized_point["role"]] += 1
        validation_errors.extend(f"reference:{normalized_point['point_id']}:{issue}" for issue in point_issues)
        normalized_references.append(normalized_point)
    missing_data = [point["point_id"] for point in (normalized_core, *normalized_references) if point["missing_data_status"] != "complete"]
    validation_status = "valid_configured"
    if validation_errors:
        validation_status = "configured_with_validation_issues"
    elif missing_data:
        validation_status = "configured_with_missing_data"
    return {"transect_id": transect.get("transect_id"), "scenario_id": transect.get("scenario_id"), "scenario_name": transect.get("scenario_name"), "core_location": normalized_core, "reference_points": normalized_references, "relationship_summary": {"reference_point_count": len(normalized_references), "configured_reference_roles": sorted(role for role, count in role_counts.items() if count > 0), "missing_data_points": missing_data, "relationship_inference": "not_performed"}, "validation": {"status": validation_status, "errors": validation_errors}}


def build_spatial_transect_output(config: dict | None = None) -> dict:
    config = config if config is not None else load_transect_configuration()
    return {"schema_version": SCHEMA_VERSION, "runtime": "Spatial Context & Transect Runtime", "generated_at": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"), "provider_agnostic": True, "safety_boundary": SAFETY_BOUNDARY, "supported_point_roles": list(POINT_ROLES), "future_compatible_sources": list(config.get("future_compatible_sources") or FUTURE_COMPATIBLE_SOURCES), "output_notes": ["Reference points are consumed only when supplied by configuration.", "Direction, distance, and elevation values are preserved when supplied and are not inferred.", "Missing coordinates remain explicit in missing_data_status and validation output."], "spatial_transects": [validate_transect(transect) for transect in config.get("transects", [])]}


def build_scenario_pack_output(spatial_output: dict) -> dict:
    scenarios = []
    for transect in spatial_output["spatial_transects"]:
        references = []
        all_points = [transect["core_location"], *transect["reference_points"]]
        for point in transect["reference_points"]:
            references.append({field: point.get(field) for field in ("point_id", "role", "name", "coordinates", "direction_label", "distance_km", "elevation_context", "source", "confidence", "status", "support_basis", "missing_data_status")})
        scenarios.append({"scenario_id": transect["scenario_id"], "scenario_name": transect["scenario_name"], "transect_id": transect["transect_id"], "dashboard_section": "spatial_transect_scenario_pack", "field_validation_claim": "not_claimed", "scenario_report": "Configured local transect context only. Reference points are illustrative or user-defined fixtures and are not field validated.", "core_location": transect["core_location"], "reference_points": references, "configured_reference_roles": transect["relationship_summary"]["configured_reference_roles"], "missing_data_points": transect["relationship_summary"]["missing_data_points"], "validation_status": transect["validation"]["status"], "relationship_inference": transect["relationship_summary"]["relationship_inference"], "source_profile": sorted({point.get("source") or "unspecified" for point in all_points}), "confidence_profile": sorted({point.get("confidence") or "unspecified" for point in all_points})})
    return {"schema_version": SCHEMA_VERSION, "runtime": "Transect Scenario Pack", "generated_at": spatial_output["generated_at"], "dashboard_compatible": True, "safety_boundary": spatial_output["safety_boundary"], "scenario_count": len(scenarios), "scenarios": scenarios}


def render_markdown_report(output: dict) -> str:
    lines = ["# Spatial Context & Transect Runtime", "", f"Schema version: {output['schema_version']}", "", output["safety_boundary"], "", "## Supported Roles", "", ", ".join(output["supported_point_roles"]), "", "## Future Compatibility", "", ", ".join(output["future_compatible_sources"]), "", "## Transect Readings", ""]
    for transect in output["spatial_transects"]:
        summary = transect["relationship_summary"]
        lines.extend([f"### {transect.get('scenario_name') or transect.get('scenario_id')}", "", f"- Transect ID: {transect.get('transect_id')}", f"- Scenario ID: {transect.get('scenario_id')}", f"- Core location: {transect['core_location'].get('name')}", f"- Validation status: {transect['validation']['status']}", f"- Configured roles: {', '.join(summary['configured_reference_roles']) or 'none'}", f"- Missing-data points: {', '.join(summary['missing_data_points']) or 'none'}", f"- Relationship inference: {summary['relationship_inference']}", ""])
    return "\n".join(lines).rstrip() + "\n"


def render_scenario_pack_report(pack_output: dict) -> str:
    lines = ["# Transect Scenario Pack", "", f"Schema version: {pack_output['schema_version']}", "", pack_output["safety_boundary"], "", "No field validation, GIS automation, mapping calls, DEM calls, simulation calls, hydrology inference, wind inference, planning conclusions, design advice, or construction advice are claimed.", ""]
    for scenario in pack_output["scenarios"]:
        lines.extend([f"## {scenario['scenario_name']}", "", f"- Scenario ID: {scenario['scenario_id']}", f"- Transect ID: {scenario['transect_id']}", f"- Validation status: {scenario['validation_status']}", f"- Configured roles: {', '.join(scenario['configured_reference_roles']) or 'none'}", f"- Missing-data points: {', '.join(scenario['missing_data_points']) or 'none'}", f"- Field validation claim: {scenario['field_validation_claim']}", f"- Scenario report: {scenario['scenario_report']}", "", "| Point | Role | Direction | Distance km | Confidence | Status | Missing data |", "| --- | --- | --- | --- | --- | --- | --- |"])
        for point in [scenario["core_location"], *scenario["reference_points"]]:
            lines.append(f"| {point.get('name')} | {point.get('role')} | {point.get('direction_label') or 'not supplied'} | {point.get('distance_km') if point.get('distance_km') is not None else 'not supplied'} | {point.get('confidence') or 'unspecified'} | {point.get('status') or 'unspecified'} | {point.get('missing_data_status')} |")
        lines.append("")
    return "\n".join(lines).rstrip() + "\n"


def write_spatial_transect_outputs(output: dict, output_path: Path = OUTPUT_PATH, report_path: Path = REPORT_PATH, scenario_pack_path: Path | None = None, scenario_pack_report_path: Path | None = None) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(output, indent=2) + "\n", encoding="utf-8")
    report_path.write_text(render_markdown_report(output), encoding="utf-8")
    pack_output = build_scenario_pack_output(output)
    scenario_pack_path = scenario_pack_path or output_path.parent / SCENARIO_PACK_PATH.name
    scenario_pack_report_path = scenario_pack_report_path or output_path.parent / SCENARIO_PACK_REPORT_PATH.name
    scenario_pack_path.write_text(json.dumps(pack_output, indent=2) + "\n", encoding="utf-8")
    scenario_pack_report_path.write_text(render_scenario_pack_report(pack_output), encoding="utf-8")


def main() -> None:
    output = build_spatial_transect_output()
    write_spatial_transect_outputs(output)
    print(f"Wrote spatial transect output to {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
