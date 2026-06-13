"""Run controlled, manually approved meteorology refresh batches."""
from __future__ import annotations

import argparse
import json
from datetime import datetime, timedelta
from pathlib import Path

try:
    from .budget_guard import derive_budget_guard, load_budget_profile
    from .meteorology_runtime import (
        CACHE_PATH,
        OUTPUT_PATH,
        TIMESERIES_PATH,
        build_live_meteorology_output,
        build_trend_output,
        cache_key,
        load_cache,
        load_locations,
        load_timeseries,
        update_timeseries,
        write_trend_outputs,
    )
    from .usage_cost_governance import derive_usage_cost_governance
except ImportError:
    from budget_guard import derive_budget_guard, load_budget_profile
    from meteorology_runtime import (
        CACHE_PATH,
        OUTPUT_PATH,
        TIMESERIES_PATH,
        build_live_meteorology_output,
        build_trend_output,
        cache_key,
        load_cache,
        load_locations,
        load_timeseries,
        update_timeseries,
        write_trend_outputs,
    )
    from usage_cost_governance import derive_usage_cost_governance

MAX_DATES_PER_RUN = 10


def _validated_date(value: str) -> str:
    candidate = value.strip()
    try:
        parsed = datetime.strptime(candidate, "%Y%m%d")
    except ValueError as exc:
        raise ValueError(
            f"invalid observation date {value!r}; expected YYYYMMDD"
        ) from exc
    if parsed.strftime("%Y%m%d") != candidate:
        raise ValueError(f"invalid observation date {value!r}; expected YYYYMMDD")
    return candidate


def parse_observation_dates(
    observation_dates: str | None = None,
    start_date: str | None = None,
    end_date: str | None = None,
    interval_days: int = 1,
    max_dates: int = MAX_DATES_PER_RUN,
) -> list[str]:
    explicit = bool(observation_dates and observation_dates.strip())
    ranged = bool((start_date and start_date.strip()) or (end_date and end_date.strip()))
    if explicit and ranged:
        raise ValueError("use either observation_dates or a date range, not both")
    if explicit:
        raw_dates = [item.strip() for item in observation_dates.split(",")]
        if not raw_dates or any(not item for item in raw_dates):
            raise ValueError("observation_dates must be a non-empty comma-separated list")
        dates = sorted({_validated_date(item) for item in raw_dates})
    elif ranged:
        if not start_date or not start_date.strip() or not end_date or not end_date.strip():
            raise ValueError("both start_date and end_date are required for range mode")
        if interval_days <= 0:
            raise ValueError("interval_days must be a positive integer")
        start = datetime.strptime(_validated_date(start_date), "%Y%m%d")
        end = datetime.strptime(_validated_date(end_date), "%Y%m%d")
        if start > end:
            raise ValueError("start_date must not be after end_date")
        dates = []
        current = start
        while current <= end:
            dates.append(current.strftime("%Y%m%d"))
            if len(dates) > max_dates:
                break
            current += timedelta(days=interval_days)
    else:
        raise ValueError("provide observation_dates or both start_date and end_date")
    if len(dates) > max_dates:
        raise ValueError(
            f"requested {len(dates)} observation dates; maximum per run is {max_dates}"
        )
    return dates


def _govern_date(
    estimated_calls: int,
    manual_approval_granted: bool,
    governance_deriver=derive_usage_cost_governance,
    guard_deriver=derive_budget_guard,
) -> tuple[dict, dict]:
    governance = governance_deriver(
        "project_mode",
        "user",
        external_resource_count=1,
        external_resource_types=["NASA POWER"],
        repeated_external_calls=estimated_calls > 1,
        platform_service_model="open_source",
    )
    request = {
        "resource_classes": ["NASA POWER"],
        "estimated_calls": estimated_calls,
        "estimated_monthly_cost": "low",
        "agent_run_count": 0,
        "repeated_external_calls": estimated_calls > 1,
        "continuous_execution": False,
        "manual_approval_granted": manual_approval_granted,
    }
    guard = guard_deriver(
        governance,
        request,
        load_budget_profile()["default"],
    )
    return governance, guard


def _uncached_count(date: str, force_refresh: bool, cache_path: Path) -> int:
    cache = load_cache(cache_path)
    return sum(
        1
        for location in load_locations()
        if force_refresh or cache_key(location, date) not in cache["readings"]
    )


def build_batch_meteorology_output(
    observation_dates: list[str],
    force_refresh: bool = False,
    manual_approval_granted: bool = False,
    fetcher=None,
    cache_path: Path = CACHE_PATH,
    timeseries_path: Path = TIMESERIES_PATH,
    governance_deriver=derive_usage_cost_governance,
    guard_deriver=derive_budget_guard,
) -> tuple[dict, dict]:
    dates = parse_observation_dates(",".join(observation_dates))
    date_results = []
    cumulative_calls = 0
    latest_output = None
    stopped = False
    for date in dates:
        if stopped:
            date_results.append({
                "observation_date": date,
                "status": "not_retrieved",
                "reason": "A previous date returned stop_required from Budget Guard.",
                "scenarios": {},
            })
            continue
        uncached_calls = _uncached_count(date, force_refresh, cache_path)
        governance, guard = _govern_date(
            cumulative_calls + uncached_calls,
            manual_approval_granted,
            governance_deriver,
            guard_deriver,
        )
        if guard["budget_status"] == "stop_required":
            stopped = True
            date_results.append({
                "observation_date": date,
                "status": "blocked_by_budget_guard",
                "uncached_calls": uncached_calls,
                "usage_cost_governance": governance,
                "budget_guard": guard,
                "scenarios": {},
            })
            continue
        runtime_args = (date, force_refresh, manual_approval_granted)
        if fetcher is None:
            output = build_live_meteorology_output(
                *runtime_args,
                cache_path=cache_path,
            )
        else:
            output = build_live_meteorology_output(
                *runtime_args,
                fetcher=fetcher,
                cache_path=cache_path,
            )
        latest_output = output
        timeseries = update_timeseries(output, timeseries_path)
        cumulative_calls += uncached_calls
        date_results.append({
            "observation_date": date,
            "status": "completed",
            "uncached_calls": uncached_calls,
            "usage_cost_governance": governance,
            "budget_guard": guard,
            "scenarios": output["scenarios"],
        })
    if latest_output is None:
        latest_output = {
            "runtime": "Meteorology Connector Runtime",
            "live_source": "NASA POWER",
            "decision_boundary": (
                "Supporting observational evidence only. No forecast, conclusion, "
                "recommendation, or automated scoring change."
            ),
            "scenarios": {},
        }
        timeseries = load_timeseries(timeseries_path)
    batch_output = {
        **latest_output,
        "runtime": "Batch Meteorology Connector Runtime",
        "requested_dates": dates,
        "max_dates_per_run": MAX_DATES_PER_RUN,
        "stopped_early": stopped,
        "date_results": date_results,
    }
    return batch_output, timeseries


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--dates")
    parser.add_argument("--start-date")
    parser.add_argument("--end-date")
    parser.add_argument("--interval-days", type=int, default=1)
    parser.add_argument("--force-refresh", action="store_true")
    parser.add_argument("--manual-approval", action="store_true")
    args = parser.parse_args(argv)
    try:
        dates = parse_observation_dates(
            args.dates,
            args.start_date,
            args.end_date,
            args.interval_days,
        )
    except ValueError as exc:
        parser.error(str(exc))
    output, timeseries = build_batch_meteorology_output(
        dates,
        args.force_refresh,
        args.manual_approval,
    )
    OUTPUT_PATH.write_text(
        json.dumps(output, indent=2, ensure_ascii=True) + "\n",
        encoding="utf-8",
    )
    write_trend_outputs(build_trend_output(timeseries))
    print(f"Generated batch meteorology evidence for {len(dates)} date(s)")


if __name__ == "__main__":
    main()
