"""Compatibility bridge from EcoEngine v1.9.2b-style records to CCZPS-Lite.

The adapter is intentionally small and tolerant. It reads local JSON records that
resemble EcoEngine scenario validation output and maps the available fields into
CCZPS-Lite runtime field names. It does not import EcoEngine, call live weather
services, connect to GIS, or validate the record as authoritative evidence.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

DRY_WATER_PATHWAYS = {"evaporation_dominated", "wind_exposed_dry"}
SOIL_LIMITING_PATHWAY = "soil_degradation"
EVAPORATION_PATHWAY = "evaporation_dominated"


def load_ecoengine_record(path):
    """Load an EcoEngine-style JSON scenario validation record from disk."""
    with Path(path).open("r", encoding="utf-8") as file_obj:
        return json.load(file_obj)


def _runtime_fields(record: dict[str, Any]) -> dict[str, Any]:
    runtime_fields = record.get("runtime_fields", {})
    if isinstance(runtime_fields, dict):
        return runtime_fields
    return {}


def _first_available(record: dict[str, Any], field_name: str, default=None):
    runtime_fields = _runtime_fields(record)
    if field_name in runtime_fields:
        return runtime_fields[field_name]
    if field_name in record:
        return record[field_name]
    return default


def _pathways(record: dict[str, Any]) -> set[str]:
    pathways = record.get("instability_pathways", [])
    if not isinstance(pathways, list):
        return set()
    return {str(pathway) for pathway in pathways}


def _as_bool(value) -> bool:
    if isinstance(value, bool):
        return value
    if isinstance(value, str):
        return value.strip().lower() in {"true", "yes", "1", "required"}
    return bool(value)


def map_ecoengine_to_runtime_fields(record):
    """Map an EcoEngine-style record into CCZPS-Lite runtime fields.

    The mapping accepts values nested under ``runtime_fields`` or at the record
    root. When explicit values are absent, selected instability pathways provide
    cautious fallback signals.
    """
    pathways = _pathways(record)

    risk_index = _first_available(record, "risk_index")

    water_balance_signal = _first_available(record, "water_balance_signal")
    if water_balance_signal is None:
        water_balance_signal = "watch" if pathways & DRY_WATER_PATHWAYS else "unknown"

    ecological_signal = _first_available(record, "ecological_resilience")
    if ecological_signal is None:
        ecological_signal = "limited" if SOIL_LIMITING_PATHWAY in pathways else "unknown"

    evaporation_pressure = _first_available(record, "evaporation_pressure")
    if evaporation_pressure is None:
        evaporation_pressure = "high" if EVAPORATION_PATHWAY in pathways else "unknown"

    confidence_level = _first_available(record, "confidence_level", "low")

    validation_value = _first_available(record, "validation_required")
    if validation_value is None:
        validation_required = True
    else:
        validation_required = _as_bool(validation_value)
    if str(confidence_level).lower() == "low":
        validation_required = True

    return {
        "risk_index": risk_index,
        "water_balance_signal": water_balance_signal,
        "ecological_signal": ecological_signal,
        "evaporation_pressure": evaporation_pressure,
        "confidence_level": confidence_level,
        "validation_required": validation_required,
    }


def summarize_ecoengine_bridge(record):
    """Return a cautious human-readable summary of the bridge mapping."""
    climate_regime = record.get("climate_regime", "unknown climate regime")
    pathways = sorted(_pathways(record))
    mapped_fields = map_ecoengine_to_runtime_fields(record)

    if pathways:
        pathway_text = " and ".join(pathways[:3])
    else:
        pathway_text = "no listed instability pathways"

    return (
        "EcoEngine v1.9.2b bridge cautiously detected "
        f"{climate_regime} regime with {pathway_text}. "
        "Runtime mapping suggests water balance "
        f"{mapped_fields['water_balance_signal']}, "
        f"{mapped_fields['evaporation_pressure']} evaporation pressure, "
        f"and validation_required={mapped_fields['validation_required']}."
    )
