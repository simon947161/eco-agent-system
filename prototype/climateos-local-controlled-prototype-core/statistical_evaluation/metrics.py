"""Bounded synthetic statistical calculations for Task1220-1239.

This module does not load data, call models, compare models, rank results or make
admission decisions. It uses only Python's standard library.
"""

from __future__ import annotations

import hashlib
import json
import math
from datetime import date
from typing import Any


FORMULA_VERSION = "climateos-statistical-metrics-0.1"


class StatisticalEvaluationBlocked(ValueError):
    """Raised when a bounded evaluation contract fails before calculation."""


def _period(value: dict[str, str], label: str) -> tuple[date, date]:
    try:
        start = date.fromisoformat(value["start"])
        end = date.fromisoformat(value["end"])
    except (KeyError, TypeError, ValueError) as exc:
        raise StatisticalEvaluationBlocked(f"{label} must contain valid ISO start and end dates.") from exc
    if start > end:
        raise StatisticalEvaluationBlocked(f"{label} start must not follow end.")
    return start, end


def _validate(payload: dict[str, Any]) -> tuple[list[float], list[float], list[float], list[float]]:
    if payload.get("fixture_only") is not True:
        raise StatisticalEvaluationBlocked("Only fixture_only synthetic inputs are authorized.")
    if payload.get("formula_version") != FORMULA_VERSION:
        raise StatisticalEvaluationBlocked("Unknown formula_version.")
    if not payload.get("units") or payload.get("forecast_units", payload.get("units")) != payload.get("units"):
        raise StatisticalEvaluationBlocked("Forecast and observation units must match.")
    if not payload.get("responsible_human"):
        raise StatisticalEvaluationBlocked("A responsible human label is required.")

    names = ["forecast_values", "observation_values", "latitudes", "climatology_values"]
    values = [payload.get(name) for name in names]
    if any(not isinstance(value, list) for value in values):
        raise StatisticalEvaluationBlocked("All value fields must be lists.")
    lengths = {len(value) for value in values}
    if lengths == {0} or len(lengths) != 1:
        raise StatisticalEvaluationBlocked("Value dimensions must match and must not be empty.")
    try:
        numeric = [[float(item) for item in value] for value in values]
    except (TypeError, ValueError) as exc:
        raise StatisticalEvaluationBlocked("All values must be numeric.") from exc
    if any(not math.isfinite(item) for value in numeric for item in value):
        raise StatisticalEvaluationBlocked("All values must be finite.")
    if any(latitude < -90 or latitude > 90 for latitude in numeric[2]):
        raise StatisticalEvaluationBlocked("Latitudes must be between -90 and 90 degrees.")

    training_start, training_end = _period(payload.get("training_period", {}), "training_period")
    evaluation_start, evaluation_end = _period(payload.get("evaluation_period", {}), "evaluation_period")
    if training_start <= evaluation_end and evaluation_start <= training_end:
        raise StatisticalEvaluationBlocked("Training and evaluation periods must not overlap.")
    if not payload.get("leakage_declaration"):
        raise StatisticalEvaluationBlocked("A leakage declaration is required.")
    return numeric[0], numeric[1], numeric[2], numeric[3]


def _weights(latitudes: list[float]) -> list[float]:
    raw = [max(0.0, math.cos(math.radians(latitude))) for latitude in latitudes]
    total = sum(raw)
    if total <= 0:
        raise StatisticalEvaluationBlocked("Latitude weights have zero total.")
    return [item / total for item in raw]


def evaluate_synthetic_slice(payload: dict[str, Any]) -> dict[str, Any]:
    forecast, observation, latitudes, climatology = _validate(payload)
    weights = _weights(latitudes)
    errors = [prediction - truth for prediction, truth in zip(forecast, observation)]
    mse = sum(weight * error**2 for weight, error in zip(weights, errors))
    mae = sum(weight * abs(error) for weight, error in zip(weights, errors))
    bias = sum(weight * error for weight, error in zip(weights, errors))

    forecast_anomaly = [value - climate for value, climate in zip(forecast, climatology)]
    observation_anomaly = [value - climate for value, climate in zip(observation, climatology)]
    numerator = sum(weight * left * right for weight, left, right in zip(weights, forecast_anomaly, observation_anomaly))
    forecast_energy = sum(weight * value**2 for weight, value in zip(weights, forecast_anomaly))
    observation_energy = sum(weight * value**2 for weight, value in zip(weights, observation_anomaly))
    denominator = math.sqrt(forecast_energy * observation_energy)
    if denominator == 0:
        raise StatisticalEvaluationBlocked("ACC anomaly variance must be non-zero.")

    reproducibility_input = {
        key: payload[key]
        for key in sorted(payload)
        if key not in {"calculated_at", "calculation_result", "expected_result"}
    }
    input_hash = hashlib.sha256(
        json.dumps(reproducibility_input, sort_keys=True, separators=(",", ":")).encode("utf-8")
    ).hexdigest()
    return {
        "evaluation_id": payload["evaluation_id"],
        "registry_id": payload["registry_id"],
        "formula_version": FORMULA_VERSION,
        "input_sha256": input_hash,
        "sample_count": len(forecast),
        "metrics": {
            "latitude_weighted_mse": mse,
            "latitude_weighted_rmse": math.sqrt(mse),
            "latitude_weighted_mae": mae,
            "latitude_weighted_bias": bias,
            "latitude_weighted_acc": numerator / denominator,
        },
        "evidence_state": "synthetic_calculation_evidence",
        "claim_boundary": "No real model score, rank, fitness conclusion or admission decision.",
    }
