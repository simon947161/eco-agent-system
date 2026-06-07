"""Generate local meteorology evidence, with an explicit NASA POWER live path."""
from __future__ import annotations
import argparse
import json
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urlencode
from urllib.request import urlopen
try:
    from .budget_guard import derive_budget_guard, load_budget_profile
    from .evidence_layer import meteorology_evidence_record
    from .meteorology_connector import configured_scenario_reading, empty_reading, load_scenario_configuration, parse_observation
    from .usage_cost_governance import derive_usage_cost_governance
except ImportError:
    from budget_guard import derive_budget_guard, load_budget_profile
    from evidence_layer import meteorology_evidence_record
    from meteorology_connector import configured_scenario_reading, empty_reading, load_scenario_configuration, parse_observation
    from usage_cost_governance import derive_usage_cost_governance

PROJECT_DIR = Path(__file__).resolve().parent.parent
OUTPUT_PATH = PROJECT_DIR / "output" / "meteorology_evidence.json"
CACHE_PATH = PROJECT_DIR / "output" / "meteorology_cache.json"
TIMESERIES_PATH = PROJECT_DIR / "output" / "meteorology_timeseries.json"
LOCATION_PATH = PROJECT_DIR / "input" / "meteorology_locations.json"
NASA_POWER_ENDPOINT = "https://power.larc.nasa.gov/api/temporal/daily/point"
NASA_PARAMETERS = "T2M,PRECTOTCORR,RH2M,WS2M,WD2M,ALLSKY_SFC_SW_DWN"
TIMESERIES_SCHEMA_VERSION = "1.0"


def nasa_power_fetch(request: dict) -> dict:
    query = urlencode({"parameters": NASA_PARAMETERS, "community": "AG", "longitude": request["longitude"], "latitude": request["latitude"], "start": request["date"], "end": request["date"], "format": "JSON"})
    with urlopen(f"{NASA_POWER_ENDPOINT}?{query}", timeout=30) as response:
        return json.loads(response.read().decode("utf-8"))


def parse_nasa_power_daily(payload: dict, location: str, date: str) -> dict:
    parameters = payload.get("properties", {}).get("parameter", {})
    def value(name: str):
        values = parameters.get(name, {})
        return values.get(date) if isinstance(values, dict) else None
    wind_speed = value("WS2M")
    normalized = {
        "observation_timestamp": datetime.strptime(date, "%Y%m%d").replace(tzinfo=timezone.utc).isoformat().replace("+00:00", "Z"),
        "T2M": value("T2M"), "PRECTOTCORR": value("PRECTOTCORR"),
        "RH2M": value("RH2M"),
        "WS2M_KMH": None if wind_speed in (None, -999) else float(wind_speed) * 3.6,
        "WD2M": value("WD2M"), "ALLSKY_SFC_SW_DWN": value("ALLSKY_SFC_SW_DWN"),
    }
    return parse_observation("nasa_power", location, normalized)


def load_locations(path: Path = LOCATION_PATH) -> list[dict]:
    return json.loads(path.read_text(encoding="utf-8"))["locations"]


def load_cache(path: Path = CACHE_PATH) -> dict:
    return json.loads(path.read_text(encoding="utf-8")) if path.exists() else {"readings": {}}


def empty_timeseries() -> dict:
    return {
        "schema_version": TIMESERIES_SCHEMA_VERSION,
        "runtime": "Meteorology Time-Series Store",
        "decision_boundary": (
            "Historical observational evidence only. No forecast, prediction, "
            "recommendation, or automated scoring change."
        ),
        "observations": [],
    }


def load_timeseries(path: Path = TIMESERIES_PATH) -> dict:
    if not path.exists() or not path.read_text(encoding="utf-8").strip():
        return empty_timeseries()
    stored = json.loads(path.read_text(encoding="utf-8"))
    if isinstance(stored, list):
        migrated = empty_timeseries()
        migrated["observations"] = stored
        return migrated
    if not isinstance(stored, dict):
        raise ValueError("meteorology time-series store must be an object or legacy list")
    observations = stored.get("observations", [])
    if not isinstance(observations, list):
        raise ValueError("meteorology time-series observations must be a list")
    if stored.get("schema_version") not in (None, TIMESERIES_SCHEMA_VERSION):
        raise ValueError("unsupported meteorology time-series schema version")
    migrated = empty_timeseries()
    migrated["observations"] = observations
    return migrated


def _timeseries_observation(record: dict) -> dict:
    reading = record["meteorology_reading"]
    return {
        "scenario_id": record["scenario_id"],
        "location_name": record["location_name"],
        "observation_date": record["observation_date"],
        "observation_timestamp": reading.get("observation_timestamp"),
        "source": record["source"],
        "retrieval_status": record["retrieval_status"],
        "confidence": record["confidence"],
        "budget_guard_status": record.get("budget_guard_status"),
        "budget_guard_summary": record.get("budget_guard_summary"),
        "meteorology_reading": reading,
    }


def update_timeseries(output: dict, path: Path = TIMESERIES_PATH) -> dict:
    store = load_timeseries(path)
    observations = store["observations"]
    existing_keys = {
        (
            item.get("scenario_id"),
            item.get("location_name"),
            item.get("observation_date"),
        )
        for item in observations
    }
    for record in output.get("scenarios", {}).values():
        if record.get("retrieval_status") != "success":
            continue
        key = (
            record.get("scenario_id"),
            record.get("location_name"),
            record.get("observation_date"),
        )
        if None in key or key in existing_keys:
            continue
        observations.append(_timeseries_observation(record))
        existing_keys.add(key)
    observations.sort(
        key=lambda item: (
            item.get("observation_date") or "",
            item.get("scenario_id") or "",
            item.get("location_name") or "",
        )
    )
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(store, indent=2, ensure_ascii=True) + "\n", encoding="utf-8")
    return store


def cache_key(location: dict, date: str) -> str:
    return f"{location['scenario_id']}|{date}"


def _blocked_reading(location: dict, date: str, guard: dict) -> dict:
    reading = empty_reading(location["location_name"], "NASA POWER", "blocked_by_budget_guard")
    reading["observation_date"] = datetime.strptime(date, "%Y%m%d").date().isoformat()
    reading["budget_guard_summary"] = guard["budget_guard_summary"]
    return reading


def build_live_meteorology_output(observation_date: str, force_refresh: bool = False, manual_approval_granted: bool = False, fetcher=nasa_power_fetch, cache_path: Path = CACHE_PATH) -> dict:
    datetime.strptime(observation_date, "%Y%m%d")
    cache = load_cache(cache_path)
    records = {}
    budget_profile = load_budget_profile()["default"]
    for location in load_locations():
        key = cache_key(location, observation_date)
        if not force_refresh and key in cache["readings"]:
            cached = dict(cache["readings"][key])
            cached["from_cache"] = True
            records[location["scenario_id"]] = cached
            continue
        governance = derive_usage_cost_governance("project_mode", "user", external_resource_count=1, external_resource_types=["NASA POWER"], platform_service_model="open_source")
        request = {"resource_classes": ["NASA POWER"], "estimated_calls": 1, "estimated_monthly_cost": "low", "agent_run_count": 0, "repeated_external_calls": False, "continuous_execution": False, "manual_approval_granted": manual_approval_granted}
        guard = derive_budget_guard(governance, request, budget_profile)
        allowed = guard["budget_status"] != "stop_required" and (not guard["requires_manual_confirmation"] or manual_approval_granted)
        if not allowed:
            reading = _blocked_reading(location, observation_date, guard)
        else:
            try:
                payload = fetcher({"latitude": location["latitude"], "longitude": location["longitude"], "date": observation_date})
                reading = parse_nasa_power_daily(payload, location["location_name"], observation_date)
            except (OSError, TimeoutError, ValueError, KeyError, json.JSONDecodeError):
                reading = empty_reading(location["location_name"], "NASA POWER", "retrieval_failed")
                reading["observation_date"] = datetime.strptime(observation_date, "%Y%m%d").date().isoformat()
        record = {"scenario_id": location["scenario_id"], "location_name": location["location_name"], "observation_date": reading["observation_date"], "meteorology_reading": reading, "source": reading["source"], "retrieval_status": reading["retrieval_status"], "confidence": reading["confidence"], "budget_guard_status": guard["budget_status"], "budget_guard_summary": guard["budget_guard_summary"], "from_cache": False, "evidence": meteorology_evidence_record(reading)}
        records[location["scenario_id"]] = record
        if reading["retrieval_status"] == "success":
            cache["readings"][key] = record
    cache_path.parent.mkdir(parents=True, exist_ok=True)
    cache_path.write_text(json.dumps(cache, indent=2, ensure_ascii=True) + "\n", encoding="utf-8")
    return {"runtime": "Meteorology Connector Runtime", "live_source": "NASA POWER", "decision_boundary": "Supporting observational evidence only. No forecast, conclusion, recommendation, or automated scoring change.", "scenarios": records}


def build_meteorology_output(fetcher=None, retrieved_at: str | None = None) -> dict:
    records = {}
    for scenario_key in load_scenario_configuration()["scenarios"]:
        reading = configured_scenario_reading(scenario_key, fetcher=fetcher, retrieved_at=retrieved_at)
        records[scenario_key] = {"meteorology_reading": reading, "evidence": meteorology_evidence_record(reading)}
    return {"runtime": "Meteorology Connector Runtime", "decision_boundary": "Supporting observational evidence only. No forecast, conclusion, recommendation, or automated scoring change.", "scenarios": records}


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--live", action="store_true")
    parser.add_argument("--date", help="Observation date in YYYYMMDD format")
    parser.add_argument("--force-refresh", action="store_true")
    parser.add_argument("--manual-approval", action="store_true")
    args = parser.parse_args(argv)
    if args.live and not args.date:
        parser.error("--date is required with --live")
    output = build_live_meteorology_output(args.date, args.force_refresh, args.manual_approval) if args.live else build_meteorology_output()
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_PATH.write_text(json.dumps(output, indent=2, ensure_ascii=True) + "\n", encoding="utf-8")
    if args.live:
        update_timeseries(output)
    print(f"Generated {OUTPUT_PATH.relative_to(PROJECT_DIR.parent)}")


if __name__ == "__main__":
    main()
