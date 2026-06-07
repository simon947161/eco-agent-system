"""Transparent meteorology observation connector for CCZPS-Lite.

The connector standardises provider payloads supplied by a caller. Network
transport is deliberately injected so tests and generated outputs remain
deterministic and no provider credentials or hidden retrieval logic are used.
"""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Callable

PROJECT_DIR = Path(__file__).resolve().parent.parent
DEFAULT_SOURCE_PATH = PROJECT_DIR / "input" / "meteorology_sources.json"
DEFAULT_SCENARIO_PATH = PROJECT_DIR / "input" / "meteorology_scenarios.json"

STANDARD_FIELDS = (
    "temperature_c",
    "rainfall_mm",
    "humidity_percent",
    "wind_speed_kmh",
    "wind_direction_degrees",
    "solar_radiation_mj_m2",
    "evaporation_mm",
)


def load_source_configuration(path: Path = DEFAULT_SOURCE_PATH) -> dict:
    """Load and minimally validate public meteorology source definitions."""
    with path.open("r", encoding="utf-8") as file_obj:
        config = json.load(file_obj)
    sources = config.get("sources")
    if not isinstance(sources, dict) or not sources:
        raise ValueError("meteorology source configuration requires sources")
    for source_id, source in sources.items():
        if not source.get("name") or not source.get("documentation_url"):
            raise ValueError(f"source {source_id} requires name and documentation_url")
        if not isinstance(source.get("field_map"), dict):
            raise ValueError(f"source {source_id} requires a field_map")
    return config


def load_scenario_configuration(path: Path = DEFAULT_SCENARIO_PATH) -> dict:
    """Load scenario locations and preferred public observation sources."""
    with path.open("r", encoding="utf-8") as file_obj:
        config = json.load(file_obj)
    scenarios = config.get("scenarios")
    if not isinstance(scenarios, dict) or not scenarios:
        raise ValueError("meteorology scenario configuration requires scenarios")
    return config


def _number(value):
    if value in (None, "", "null", "NA", "N/A", -999, -999.0):
        return None
    try:
        return float(value)
    except (TypeError, ValueError):
        return None


def _iso_timestamp(value) -> str | None:
    if value in (None, ""):
        return None
    text = str(value).strip()
    if text.endswith("Z"):
        text = text[:-1] + "+00:00"
    try:
        parsed = datetime.fromisoformat(text)
    except ValueError:
        return None
    if parsed.tzinfo is None:
        parsed = parsed.replace(tzinfo=timezone.utc)
    return parsed.astimezone(timezone.utc).isoformat().replace("+00:00", "Z")


def empty_reading(
    location: str,
    source_name: str,
    retrieval_status: str,
    retrieved_at: str | None = None,
) -> dict:
    """Return a complete missing-data record rather than omitting fields."""
    reading = {
        "location": location,
        "observation_date": None,
        **{field: None for field in STANDARD_FIELDS},
        "source": source_name,
        "observation_timestamp": None,
        "retrieved_at": retrieved_at,
        "retrieval_status": retrieval_status,
        "confidence": "low",
    }
    return reading


def parse_observation(
    source_id: str,
    location: str,
    payload: dict,
    config: dict | None = None,
    retrieved_at: str | None = None,
) -> dict:
    """Standardise one provider payload using its explicit field mapping."""
    config = config or load_source_configuration()
    source = config["sources"].get(source_id)
    if source is None:
        raise KeyError(f"unknown meteorology source: {source_id}")
    if not isinstance(payload, dict):
        return empty_reading(location, source["name"], "invalid_payload", retrieved_at)

    field_map = source["field_map"]
    timestamp = _iso_timestamp(payload.get(field_map.get("observation_timestamp", "")))
    reading = {
        "location": location,
        "observation_date": timestamp[:10] if timestamp else None,
        **{
            field: _number(payload.get(field_map.get(field, "")))
            for field in STANDARD_FIELDS
        },
        "source": source["name"],
        "observation_timestamp": timestamp,
        "retrieved_at": retrieved_at,
        "retrieval_status": "success",
        "confidence": str(payload.get("confidence", source.get("default_confidence", "medium"))).lower(),
    }
    if all(reading[field] is None for field in STANDARD_FIELDS):
        reading["retrieval_status"] = "missing_data"
        reading["confidence"] = "low"
    return reading


def retrieve_observation(
    source_id: str,
    location: str,
    request: dict,
    fetcher: Callable[[dict, dict], dict] | None = None,
    config: dict | None = None,
    retrieved_at: str | None = None,
) -> dict:
    """Retrieve through an injected transport and standardise the response."""
    config = config or load_source_configuration()
    source = config["sources"].get(source_id)
    if source is None:
        raise KeyError(f"unknown meteorology source: {source_id}")
    if fetcher is None:
        return empty_reading(location, source["name"], "not_retrieved", retrieved_at)
    try:
        payload = fetcher(source, request)
    except (OSError, TimeoutError, ValueError):
        return empty_reading(location, source["name"], "retrieval_failed", retrieved_at)
    return parse_observation(source_id, location, payload, config, retrieved_at)


def configured_scenario_reading(
    scenario_key: str,
    fetcher: Callable[[dict, dict], dict] | None = None,
    retrieved_at: str | None = None,
) -> dict:
    """Retrieve a reading for a configured scenario location."""
    scenario = load_scenario_configuration()["scenarios"].get(scenario_key)
    if scenario is None:
        raise KeyError(f"unknown meteorology scenario: {scenario_key}")
    return retrieve_observation(
        scenario["preferred_source"],
        scenario["location"],
        scenario,
        fetcher=fetcher,
        retrieved_at=retrieved_at,
    )
