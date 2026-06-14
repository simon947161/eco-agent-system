"""Create preliminary scenario profiles from local location intake records."""
from __future__ import annotations

import argparse
import json
import re
import unicodedata
from pathlib import Path

PROJECT_DIR = Path(__file__).resolve().parent.parent
INPUT_PATH = PROJECT_DIR / "input" / "location_intake_examples.json"
OUTPUT_PATH = PROJECT_DIR / "output" / "location_intake_profiles.json"
REPORT_PATH = PROJECT_DIR / "output" / "location_intake_profiles.md"
SCHEMA_VERSION = "1.0"
SAFETY_BOUNDARY = (
    "Location intake only. This runtime does not perform geocoding, environmental "
    "analysis, meteorology retrieval, GIS / DEM processing, planning assessment, "
    "professional review, approval assessment, or recommendation generation."
)
LIMITATIONS = [
    "Location intake only",
    "No planning conclusion generated",
    "No GIS / DEM validation performed",
    "No meteorology retrieval performed unless separately triggered",
    "Not ready for approval",
]
RECOMMENDED_NEXT_STEPS = [
    "run governed meteorology refresh",
    "prepare GIS / DEM validation requirements",
    "generate planning hypothesis after evidence exists",
    "request professional review before any planning decision",
]


def load_location_intakes(path: Path = INPUT_PATH) -> list[object]:
    """Load a local JSON array without contacting external services."""
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, list):
        raise ValueError("location intake input must be a JSON array")
    return data


def _is_number(value: object) -> bool:
    return isinstance(value, (int, float)) and not isinstance(value, bool)


def validate_location_record(record: object) -> list[str]:
    """Return deterministic validation errors without repairing the record."""
    if not isinstance(record, dict):
        return ["record_must_be_an_object"]
    errors: list[str] = []
    if not isinstance(record.get("location_name"), str) or not record["location_name"].strip():
        errors.append("location_name_is_required")
    latitude = record.get("latitude")
    if not _is_number(latitude):
        errors.append("latitude_must_be_numeric")
    elif not -90 <= float(latitude) <= 90:
        errors.append("latitude_must_be_between_-90_and_90")
    longitude = record.get("longitude")
    if not _is_number(longitude):
        errors.append("longitude_must_be_numeric")
    elif not -180 <= float(longitude) <= 180:
        errors.append("longitude_must_be_between_-180_and_180")
    if not isinstance(record.get("intake_context"), str) or not record["intake_context"].strip():
        errors.append("intake_context_is_required")
    return errors


def scenario_id_for(location_name: str) -> str:
    """Generate a stable ASCII scenario identifier from the supplied name."""
    normalized = unicodedata.normalize("NFKD", location_name)
    ascii_name = normalized.encode("ascii", "ignore").decode("ascii").lower()
    slug = re.sub(r"[^a-z0-9]+", "_", ascii_name).strip("_")
    return f"{slug or 'location'}_intake"


def build_scenario_profile(record: dict) -> dict:
    """Convert one valid intake record into an explicitly preliminary profile."""
    return {
        "scenario_id": scenario_id_for(record["location_name"]),
        "location_name": record["location_name"].strip(),
        "country": record.get("country"),
        "region": record.get("region"),
        "latitude": float(record["latitude"]),
        "longitude": float(record["longitude"]),
        "intake_context": record["intake_context"].strip(),
        "user_intent": record.get("user_intent"),
        "notes": record.get("notes"),
        "scenario_status": "intake_only",
        "workflow_status": "awaiting_evidence_generation",
        "evidence_status": "not_generated",
        "meteorology_status": "not_requested",
        "gis_dem_status": "not_requested",
        "planning_hypothesis_status": "not_generated",
        "approval_support_status": "not_ready_for_approval",
        "human_review_required": True,
        "professional_review_required": True,
        "limitations": list(LIMITATIONS),
        "recommended_next_steps": list(RECOMMENDED_NEXT_STEPS),
    }


def build_location_intake_output(records: list[object]) -> dict:
    """Separate valid profiles from invalid input records."""
    profiles = []
    invalid_records = []
    for index, record in enumerate(records):
        errors = validate_location_record(record)
        if errors:
            invalid_records.append(
                {
                    "input_index": index,
                    "location_name": record.get("location_name") if isinstance(record, dict) else None,
                    "validation_errors": errors,
                    "record": record,
                }
            )
        else:
            profiles.append(build_scenario_profile(record))
    return {
        "schema_version": SCHEMA_VERSION,
        "runtime": "Location-to-Scenario Intake Runtime",
        "dashboard_compatible": True,
        "safety_boundary": SAFETY_BOUNDARY,
        "profile_count": len(profiles),
        "invalid_record_count": len(invalid_records),
        "scenario_profiles": profiles,
        "invalid_records": invalid_records,
    }


def render_markdown_report(output: dict) -> str:
    lines = [
        "# Location-to-Scenario Intake Runtime",
        "",
        output["safety_boundary"],
        "",
        f"- Valid preliminary profiles: {output['profile_count']}",
        f"- Invalid input records: {output['invalid_record_count']}",
        "",
    ]
    for profile in output["scenario_profiles"]:
        lines.extend(
            [
                f"## {profile['location_name']}",
                "",
                f"- Scenario ID: `{profile['scenario_id']}`",
                f"- Country / region: {profile.get('country') or 'not supplied'} / {profile.get('region') or 'not supplied'}",
                f"- Coordinates: {profile['latitude']}, {profile['longitude']}",
                f"- Intake context: `{profile['intake_context']}`",
                f"- Scenario status: `{profile['scenario_status']}`",
                f"- Workflow status: `{profile['workflow_status']}`",
                f"- Evidence status: `{profile['evidence_status']}`",
                f"- Meteorology status: `{profile['meteorology_status']}`",
                f"- GIS / DEM status: `{profile['gis_dem_status']}`",
                f"- Approval support status: `{profile['approval_support_status']}`",
                f"- Human review required: {profile['human_review_required']}",
                f"- Professional review required: {profile['professional_review_required']}",
                "",
                "### Recommended Next Steps",
                "",
                *[f"- {step}" for step in profile["recommended_next_steps"]],
                "",
                "### Limitations",
                "",
                *[f"- {limitation}" for limitation in profile["limitations"]],
                "",
            ]
        )
    if output["invalid_records"]:
        lines.extend(["## Invalid Records", ""])
        for invalid in output["invalid_records"]:
            name = invalid.get("location_name") or f"Input record {invalid['input_index']}"
            lines.extend(
                [
                    f"### {name}",
                    "",
                    f"- Input index: {invalid['input_index']}",
                    f"- Validation errors: {', '.join(invalid['validation_errors'])}",
                    "- Promotion status: not promoted to a scenario profile",
                    "",
                ]
            )
    return "\n".join(lines).rstrip() + "\n"


def write_location_intake_outputs(
    output: dict,
    output_path: Path = OUTPUT_PATH,
    report_path: Path = REPORT_PATH,
) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(
        json.dumps(output, indent=2, ensure_ascii=True) + "\n",
        encoding="utf-8",
    )
    report_path.write_text(render_markdown_report(output), encoding="utf-8")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Create local-only preliminary CCZPS-Lite location intake profiles."
    )
    parser.add_argument("--input", type=Path, default=INPUT_PATH)
    parser.add_argument("--output", type=Path, default=OUTPUT_PATH)
    parser.add_argument("--report", type=Path, default=REPORT_PATH)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    output = build_location_intake_output(load_location_intakes(args.input))
    write_location_intake_outputs(output, args.output, args.report)
    print(
        f"Wrote {output['profile_count']} location intake profile(s) and "
        f"{output['invalid_record_count']} invalid record(s) to {args.output}"
    )


if __name__ == "__main__":
    main()
