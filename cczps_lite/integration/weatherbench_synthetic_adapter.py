"""Bounded, dependency-free WeatherBench-X reference adapter prototype.

This module evaluates only tiny, repository-authored synthetic fixtures.  It
does not import, install, execute, or claim compatibility with WeatherBench 2
or WeatherBench-X.  The small fixed contract exists to test ClimateOS boundary
behaviour before any real data or upstream evaluation code is considered.
"""

from __future__ import annotations

import json
import math
from datetime import datetime
from pathlib import Path
from typing import Any

ADAPTER_ID = "climateos.weatherbench_x.synthetic_adapter.v0.1"
CONTRACT_VERSION = "climateos.weatherbench_x.synthetic_case.v0.1"
DATA_CLASSIFICATION = "SYNTHETIC_ONLY"
ORIGIN = "REPOSITORY_INLINE_FIXTURE"
RESULT_CLASSIFICATION = "CLIMATEOS_SYNTHETIC_RESULT_NOT_WEATHERBENCH_SCORE"
SUPPORTED_VARIABLE_UNITS = {"2m_temperature": "K"}
SUPPORTED_METRICS = (
    "latitude_weighted_rmse",
    "latitude_weighted_mae",
    "latitude_weighted_bias",
)
FIXTURE_ROOT = Path(__file__).resolve().parents[1] / "input"
REQUIRED_FIELDS = {
    "case_id",
    "contract_version",
    "data_classification",
    "origin",
    "variable",
    "unit",
    "initial_time",
    "valid_time",
    "lead_time_hours",
    "latitude_degrees",
    "longitude_degrees",
    "forecast_values",
    "reference_values",
    "metric_request",
}


class SyntheticAdapterContractError(ValueError):
    """Raised when a record tries to cross the bounded synthetic contract."""


def load_synthetic_case(path: str | Path) -> dict[str, Any]:
    """Load a local JSON fixture without resolving URLs or external sources."""
    fixture_path = Path(path).resolve()
    try:
        fixture_path.relative_to(FIXTURE_ROOT.resolve())
    except ValueError as exc:
        raise SyntheticAdapterContractError(
            "Synthetic fixtures must be stored under cczps_lite/input"
        ) from exc
    with fixture_path.open("r", encoding="utf-8") as file_obj:
        record = json.load(file_obj)
    if not isinstance(record, dict):
        raise SyntheticAdapterContractError("Synthetic case must be a JSON object")
    return record


def _utc_time(value: Any, field_name: str) -> datetime:
    if not isinstance(value, str) or not value.endswith("Z"):
        raise SyntheticAdapterContractError(f"{field_name} must be an ISO-8601 UTC string")
    try:
        return datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError as exc:
        raise SyntheticAdapterContractError(f"{field_name} is not valid ISO-8601") from exc


def _finite_numbers(values: Any, field_name: str) -> list[float]:
    if not isinstance(values, list) or not values:
        raise SyntheticAdapterContractError(f"{field_name} must be a non-empty list")
    converted: list[float] = []
    for value in values:
        if isinstance(value, bool) or not isinstance(value, (int, float)):
            raise SyntheticAdapterContractError(f"{field_name} must contain only numbers")
        number = float(value)
        if not math.isfinite(number):
            raise SyntheticAdapterContractError(f"{field_name} must contain only finite numbers")
        converted.append(number)
    return converted


def validate_synthetic_case(record: dict[str, Any]) -> None:
    """Validate the exact no-network, synthetic-only adapter interface."""
    actual_fields = set(record)
    missing = REQUIRED_FIELDS - actual_fields
    unknown = actual_fields - REQUIRED_FIELDS
    if missing:
        raise SyntheticAdapterContractError(f"Missing fields: {sorted(missing)}")
    if unknown:
        raise SyntheticAdapterContractError(f"Unknown fields are blocked: {sorted(unknown)}")

    if record["contract_version"] != CONTRACT_VERSION:
        raise SyntheticAdapterContractError("Unsupported contract_version")
    if record["data_classification"] != DATA_CLASSIFICATION:
        raise SyntheticAdapterContractError("Only SYNTHETIC_ONLY data are permitted")
    if record["origin"] != ORIGIN:
        raise SyntheticAdapterContractError("Only repository-inline fixtures are permitted")

    variable = record["variable"]
    expected_unit = SUPPORTED_VARIABLE_UNITS.get(variable)
    if expected_unit is None:
        raise SyntheticAdapterContractError(f"Unsupported variable: {variable!r}")
    if record["unit"] != expected_unit:
        raise SyntheticAdapterContractError(
            f"Unit mismatch for {variable}: expected {expected_unit!r}"
        )

    initial_time = _utc_time(record["initial_time"], "initial_time")
    valid_time = _utc_time(record["valid_time"], "valid_time")
    lead_time = record["lead_time_hours"]
    if isinstance(lead_time, bool) or not isinstance(lead_time, int) or lead_time < 0:
        raise SyntheticAdapterContractError("lead_time_hours must be a non-negative integer")
    actual_lead_hours = (valid_time - initial_time).total_seconds() / 3600
    if actual_lead_hours != lead_time:
        raise SyntheticAdapterContractError("valid_time does not match initial_time + lead_time")

    latitudes = _finite_numbers(record["latitude_degrees"], "latitude_degrees")
    longitudes = _finite_numbers(record["longitude_degrees"], "longitude_degrees")
    if any(latitude < -90 or latitude > 90 for latitude in latitudes):
        raise SyntheticAdapterContractError("latitude_degrees must be within [-90, 90]")
    if any(longitude < -180 or longitude > 360 for longitude in longitudes):
        raise SyntheticAdapterContractError("longitude_degrees must be within [-180, 360]")

    forecast = _finite_numbers(record["forecast_values"], "forecast_values")
    reference = _finite_numbers(record["reference_values"], "reference_values")
    expected_points = len(latitudes) * len(longitudes)
    if len(forecast) != expected_points or len(reference) != expected_points:
        raise SyntheticAdapterContractError(
            "forecast_values and reference_values must match the row-major grid size"
        )

    metric_request = record["metric_request"]
    if metric_request != list(SUPPORTED_METRICS):
        raise SyntheticAdapterContractError("metric_request must equal the fixed metric set")


def evaluate_synthetic_case(record: dict[str, Any]) -> dict[str, Any]:
    """Evaluate the fixed tiny case and retain the non-WeatherBench boundary."""
    validate_synthetic_case(record)

    latitudes = [float(value) for value in record["latitude_degrees"]]
    longitudes = record["longitude_degrees"]
    forecast = [float(value) for value in record["forecast_values"]]
    reference = [float(value) for value in record["reference_values"]]

    errors: list[float] = []
    weights: list[float] = []
    longitude_count = len(longitudes)
    for latitude_index, latitude in enumerate(latitudes):
        latitude_weight = math.cos(math.radians(latitude))
        if latitude_weight <= 0:
            raise SyntheticAdapterContractError(
                "Latitude weights must be positive; pole-only points are excluded in v0.1"
            )
        start = latitude_index * longitude_count
        for offset in range(longitude_count):
            index = start + offset
            errors.append(forecast[index] - reference[index])
            weights.append(latitude_weight)

    weight_sum = sum(weights)
    weighted_bias = sum(error * weight for error, weight in zip(errors, weights)) / weight_sum
    weighted_mae = sum(abs(error) * weight for error, weight in zip(errors, weights)) / weight_sum
    weighted_mse = sum(error * error * weight for error, weight in zip(errors, weights)) / weight_sum

    return {
        "adapter_id": ADAPTER_ID,
        "contract_version": CONTRACT_VERSION,
        "case_id": record["case_id"],
        "result_classification": RESULT_CLASSIFICATION,
        "data_classification": DATA_CLASSIFICATION,
        "source_mode": ORIGIN,
        "upstream_code_executed": False,
        "external_data_accessed": False,
        "network_or_cloud_used": False,
        "variable": record["variable"],
        "unit": record["unit"],
        "initial_time": record["initial_time"],
        "valid_time": record["valid_time"],
        "lead_time_hours": record["lead_time_hours"],
        "grid_point_count": len(errors),
        "metrics": {
            "latitude_weighted_rmse": math.sqrt(weighted_mse),
            "latitude_weighted_mae": weighted_mae,
            "latitude_weighted_bias": weighted_bias,
        },
        "model_admission_state": "NOT_EVALUATED",
        "human_review_required": True,
        "boundary_note": (
            "Interface and metric semantics are WeatherBench-X-inspired references only; "
            "this output is not an official or reproduced WeatherBench score."
        ),
    }
