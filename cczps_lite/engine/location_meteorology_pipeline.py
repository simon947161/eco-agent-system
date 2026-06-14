"""Generate governed meteorology evidence for valid location intake profiles."""
from __future__ import annotations

import argparse
import json
from pathlib import Path

try:
    from .budget_guard import derive_budget_guard, load_budget_profile
    from .meteorology_batch_runtime import parse_observation_dates
    from .meteorology_runtime import (
        CACHE_PATH,
        cache_key,
        load_cache,
        nasa_power_fetch,
        parse_nasa_power_daily,
    )
    from .usage_cost_governance import derive_usage_cost_governance
except ImportError:
    from budget_guard import derive_budget_guard, load_budget_profile
    from meteorology_batch_runtime import parse_observation_dates
    from meteorology_runtime import (
        CACHE_PATH,
        cache_key,
        load_cache,
        nasa_power_fetch,
        parse_nasa_power_daily,
    )
    from usage_cost_governance import derive_usage_cost_governance

PROJECT_DIR = Path(__file__).resolve().parent.parent
INTAKE_PATH = PROJECT_DIR / "output" / "location_intake_profiles.json"
OUTPUT_PATH = PROJECT_DIR / "output" / "location_meteorology_evidence.json"
REPORT_PATH = PROJECT_DIR / "output" / "location_meteorology_evidence.md"
MAX_LOCATIONS_PER_RUN = 5
MAX_DATES_PER_RUN = 10
SCHEMA_VERSION = "1.0"
LIMITATIONS = [
    "Meteorology evidence only",
    "No GIS / DEM validation performed",
    "No planning conclusion generated",
    "Not ready for approval",
]
DECISION_BOUNDARY = (
    "Governed meteorology evidence only. No geocoding, GIS / DEM analysis, "
    "planning conclusion, approval decision, or recommendation is generated."
)


def load_intake_profiles(path: Path = INTAKE_PATH) -> list[dict]:
    """Read only valid preliminary profiles from the Task 42 output."""
    stored = json.loads(path.read_text(encoding="utf-8"))
    profiles = stored.get("scenario_profiles", [])
    if not isinstance(profiles, list):
        raise ValueError("location intake scenario_profiles must be a list")
    required = {"scenario_id", "location_name", "latitude", "longitude"}
    return [
        profile
        for profile in profiles
        if isinstance(profile, dict)
        and required.issubset(profile)
        and profile.get("scenario_status") == "intake_only"
    ]


def select_intake_profiles(
    profiles: list[dict],
    selected_ids: list[str] | None = None,
    max_locations: int = MAX_LOCATIONS_PER_RUN,
) -> list[dict]:
    """Select stable intake IDs and enforce a conservative location limit."""
    by_id = {profile["scenario_id"]: profile for profile in profiles}
    if selected_ids:
        normalized = list(dict.fromkeys(item.strip() for item in selected_ids if item.strip()))
        missing = [scenario_id for scenario_id in normalized if scenario_id not in by_id]
        if missing:
            raise ValueError(f"unknown intake scenario id(s): {', '.join(missing)}")
        selected = [by_id[scenario_id] for scenario_id in normalized]
    else:
        selected = list(profiles)
    if len(selected) > max_locations:
        raise ValueError(
            f"requested {len(selected)} intake locations; maximum per run is {max_locations}"
        )
    return selected


def _govern_pair(
    estimated_calls: int,
    manual_approval_granted: bool,
    uses_live_resource: bool,
    governance_deriver=derive_usage_cost_governance,
    guard_deriver=derive_budget_guard,
) -> tuple[dict, dict]:
    resource_types = ["NASA POWER"] if uses_live_resource else []
    governance = governance_deriver(
        "project_mode",
        "user",
        external_resource_count=len(resource_types),
        external_resource_types=resource_types,
        repeated_external_calls=estimated_calls > 1,
        platform_service_model="open_source",
    )
    request = {
        "resource_classes": resource_types,
        "estimated_calls": estimated_calls,
        "estimated_monthly_cost": "low",
        "agent_run_count": 0,
        "repeated_external_calls": estimated_calls > 1,
        "continuous_execution": False,
        "manual_approval_granted": manual_approval_granted,
    }
    guard = guard_deriver(governance, request, load_budget_profile()["default"])
    return governance, guard


def _base_record(profile: dict, date: str) -> dict:
    return {
        "scenario_id": profile["scenario_id"],
        "location_name": profile["location_name"],
        "latitude": float(profile["latitude"]),
        "longitude": float(profile["longitude"]),
        "observation_date": date,
        "source": "NASA POWER",
        "approval_support_status": "not_ready_for_approval",
        "human_review_required": True,
        "professional_review_required": True,
        "trend_status": "not_generated",
        "limitations": list(LIMITATIONS),
    }


def _blocked_record(
    profile: dict,
    date: str,
    governance: dict,
    guard: dict,
    retrieval_status: str,
    reason: str,
) -> dict:
    return {
        **_base_record(profile, date),
        "meteorology_status": "not_retrieved",
        "retrieval_status": retrieval_status,
        "from_cache": False,
        "budget_guard_status": guard["budget_status"],
        "budget_guard_summary": guard["budget_guard_summary"],
        "usage_governance_status": (
            "manual_approval_missing"
            if guard.get("requires_manual_confirmation")
            else "governed_not_retrieved"
        ),
        "usage_cost_governance": governance,
        "reason": reason,
        "meteorology_reading": None,
    }


def _success_record(
    profile: dict,
    date: str,
    reading: dict,
    governance: dict,
    guard: dict,
    from_cache: bool,
) -> dict:
    return {
        **_base_record(profile, date),
        "meteorology_status": "success",
        "retrieval_status": "success",
        "from_cache": from_cache,
        "budget_guard_status": guard["budget_status"],
        "budget_guard_summary": guard["budget_guard_summary"],
        "usage_governance_status": (
            "cache_only" if from_cache else "manual_approved"
        ),
        "usage_cost_governance": governance,
        "meteorology_reading": reading,
    }


def _failed_record(
    profile: dict,
    date: str,
    governance: dict,
    guard: dict,
) -> dict:
    return {
        **_base_record(profile, date),
        "meteorology_status": "not_retrieved",
        "retrieval_status": "retrieval_failed",
        "from_cache": False,
        "budget_guard_status": guard["budget_status"],
        "budget_guard_summary": guard["budget_guard_summary"],
        "usage_governance_status": "manual_approved",
        "usage_cost_governance": governance,
        "reason": "The governed NASA POWER retrieval failed.",
        "meteorology_reading": None,
    }


def _reading_from_cached(cached: dict) -> dict | None:
    reading = cached.get("meteorology_reading")
    if cached.get("retrieval_status") == "success" and isinstance(reading, dict):
        return reading
    return None


def build_location_meteorology_output(
    observation_dates: list[str],
    selected_ids: list[str] | None = None,
    manual_approval_granted: bool = False,
    force_refresh: bool = False,
    intake_path: Path = INTAKE_PATH,
    cache_path: Path = CACHE_PATH,
    fetcher=nasa_power_fetch,
    max_locations: int = MAX_LOCATIONS_PER_RUN,
    max_dates: int = MAX_DATES_PER_RUN,
    governance_deriver=derive_usage_cost_governance,
    guard_deriver=derive_budget_guard,
) -> dict:
    """Run cache-first governed retrieval without promoting intake scenarios."""
    dates = parse_observation_dates(
        ",".join(observation_dates),
        max_dates=max_dates,
    )
    profiles = select_intake_profiles(
        load_intake_profiles(intake_path),
        selected_ids,
        max_locations,
    )
    cache = load_cache(cache_path)
    cache.setdefault("readings", {})
    pairs = [(profile, date) for profile in profiles for date in dates]
    uncached_count = sum(
        1
        for profile, date in pairs
        if force_refresh or cache_key(profile, date) not in cache["readings"]
    )
    records = []
    stopped_live_retrieval = False

    for profile, date in pairs:
        key = cache_key(profile, date)
        cached = None if force_refresh else cache["readings"].get(key)
        cached_reading = _reading_from_cached(cached) if isinstance(cached, dict) else None
        if cached_reading is not None:
            governance, guard = _govern_pair(
                0,
                manual_approval_granted,
                False,
                governance_deriver,
                guard_deriver,
            )
            records.append(
                _success_record(profile, date, cached_reading, governance, guard, True)
            )
            continue

        governance, guard = _govern_pair(
            uncached_count,
            manual_approval_granted,
            True,
            governance_deriver,
            guard_deriver,
        )
        if stopped_live_retrieval:
            records.append(
                _blocked_record(
                    profile,
                    date,
                    governance,
                    guard,
                    "not_retrieved",
                    "A previous location/date pair returned stop_required.",
                )
            )
            continue
        if guard["budget_status"] == "stop_required":
            stopped_live_retrieval = True
            records.append(
                _blocked_record(
                    profile,
                    date,
                    governance,
                    guard,
                    "blocked_by_budget_guard",
                    "Budget Guard requires the run to stop before live retrieval.",
                )
            )
            continue
        if not manual_approval_granted or guard.get("requires_manual_confirmation"):
            records.append(
                _blocked_record(
                    profile,
                    date,
                    governance,
                    guard,
                    "manual_approval_required",
                    "Explicit --manual-approval is required for live retrieval.",
                )
            )
            continue
        try:
            payload = fetcher(
                {
                    "latitude": profile["latitude"],
                    "longitude": profile["longitude"],
                    "date": date,
                }
            )
            reading = parse_nasa_power_daily(payload, profile["location_name"], date)
        except (OSError, TimeoutError, ValueError, KeyError, json.JSONDecodeError):
            records.append(_failed_record(profile, date, governance, guard))
            continue
        if reading.get("retrieval_status") != "success":
            records.append(_failed_record(profile, date, governance, guard))
            continue
        record = _success_record(profile, date, reading, governance, guard, False)
        records.append(record)
        cache["readings"][key] = {
            "scenario_id": profile["scenario_id"],
            "location_name": profile["location_name"],
            "observation_date": reading.get("observation_date"),
            "source": reading.get("source", "NASA POWER"),
            "retrieval_status": "success",
            "confidence": reading.get("confidence"),
            "budget_guard_status": guard["budget_status"],
            "budget_guard_summary": guard["budget_guard_summary"],
            "from_cache": False,
            "meteorology_reading": reading,
        }

    cache_path.parent.mkdir(parents=True, exist_ok=True)
    cache_path.write_text(
        json.dumps(cache, indent=2, ensure_ascii=True) + "\n",
        encoding="utf-8",
    )
    return {
        "schema_version": SCHEMA_VERSION,
        "runtime": "Governed Location-to-Meteorology Pipeline",
        "decision_boundary": DECISION_BOUNDARY,
        "requested_dates": dates,
        "selected_intake_ids": [profile["scenario_id"] for profile in profiles],
        "max_locations_per_run": max_locations,
        "max_dates_per_run": max_dates,
        "uncached_request_count": uncached_count,
        "stopped_early": stopped_live_retrieval,
        "record_count": len(records),
        "records": records,
    }


def render_markdown_report(output: dict) -> str:
    lines = [
        "# Governed Location-to-Meteorology Pipeline",
        "",
        output["decision_boundary"],
        "",
        f"- Selected intake locations: {len(output['selected_intake_ids'])}",
        f"- Requested dates: {len(output['requested_dates'])}",
        f"- Uncached request count: {output['uncached_request_count']}",
        f"- Stopped early: {output['stopped_early']}",
        "",
    ]
    for record in output["records"]:
        lines.extend(
            [
                f"## {record['location_name']} - {record['observation_date']}",
                "",
                f"- Scenario ID: `{record['scenario_id']}`",
                f"- Meteorology status: `{record['meteorology_status']}`",
                f"- Retrieval status: `{record['retrieval_status']}`",
                f"- Source: {record['source']}",
                f"- From cache: {record['from_cache']}",
                f"- Budget Guard: `{record['budget_guard_status']}`",
                f"- Usage governance: `{record['usage_governance_status']}`",
                f"- Trend status: `{record['trend_status']}`",
                f"- Approval support: `{record['approval_support_status']}`",
                f"- Human review required: {record['human_review_required']}",
                f"- Professional review required: {record['professional_review_required']}",
            ]
        )
        if record.get("reason"):
            lines.append(f"- Reason: {record['reason']}")
        lines.extend(
            [
                "",
                "### Limitations",
                "",
                *[f"- {item}" for item in record["limitations"]],
                "",
            ]
        )
    return "\n".join(lines).rstrip() + "\n"


def write_location_meteorology_outputs(
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


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser()
    date_group = parser.add_mutually_exclusive_group(required=True)
    date_group.add_argument("--date")
    date_group.add_argument("--dates")
    parser.add_argument("--selected-intake-ids")
    parser.add_argument("--manual-approval", action="store_true")
    parser.add_argument("--force-refresh", action="store_true")
    args = parser.parse_args(argv)
    raw_dates = args.dates or args.date
    try:
        dates = parse_observation_dates(raw_dates, max_dates=MAX_DATES_PER_RUN)
        selected_ids = (
            [item.strip() for item in args.selected_intake_ids.split(",")]
            if args.selected_intake_ids
            else None
        )
        output = build_location_meteorology_output(
            dates,
            selected_ids,
            args.manual_approval,
            args.force_refresh,
        )
    except ValueError as exc:
        parser.error(str(exc))
    write_location_meteorology_outputs(output)
    print(
        f"Generated {output['record_count']} governed location meteorology record(s)"
    )


if __name__ == "__main__":
    main()
