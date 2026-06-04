"""Differential Field Runtime for CCZPS-Lite.

This module compares scenario scores with representative context records to
produce lightweight gradient signals. Values are indicative runtime signals for
review, not validated field measurements or physical modelling outputs.
"""

from __future__ import annotations

import json
from pathlib import Path

_CONTEXT_FIELDS = (
    "water_security",
    "heat_exposure",
    "vegetation_condition",
    "fire_exposure",
)


def load_differential_context(path):
    """Load a local differential context JSON file."""
    with Path(path).open("r", encoding="utf-8") as file_obj:
        return json.load(file_obj)


def calculate_gradient(target_value, reference_value):
    """Return target minus reference as a rounded gradient value."""
    return round(float(target_value) - float(reference_value), 2)


def classify_gradient(value):
    """Classify a numeric gradient into an explainable threshold band."""
    if value >= 2.0:
        return "strong_positive"
    if value >= 0.75:
        return "moderate_positive"
    if value > -0.75:
        return "neutral"
    if value > -2.0:
        return "moderate_negative"
    return "strong_negative"


def _average_context_value(context_records, field_name):
    values = [record.get(field_name) for record in context_records if record.get(field_name) is not None]
    if not values:
        return 0.0
    return sum(float(value) for value in values) / len(values)


def _is_positive(gradient_class):
    return gradient_class in {"moderate_positive", "strong_positive"}


def _is_negative(gradient_class):
    return gradient_class in {"moderate_negative", "strong_negative"}


def _derive_differential_status(water_class, heat_class, vegetation_class, fire_class):
    if _is_positive(water_class) and _is_negative(heat_class):
        return "water_advantage_with_heat_relief"
    if _is_negative(water_class) and _is_positive(heat_class):
        return "water_stress_with_heat_pressure"
    if _is_positive(vegetation_class) and _is_negative(fire_class):
        return "vegetation_buffer_advantage"
    if _is_positive(fire_class):
        return "elevated_fire_exposure"
    return "mixed_or_neutral_differential"


def derive_differential_field(scenario_scores, context_records):
    """Compare scenario scores with representative context averages."""
    records = context_records or []
    reference_averages = {
        field_name: _average_context_value(records, field_name)
        for field_name in _CONTEXT_FIELDS
    }

    water_target = scenario_scores.get("water_security", 0)
    heat_target = 10 - scenario_scores.get("water_security", 0)
    vegetation_target = scenario_scores.get("ecological_resilience", 0)
    fire_target = scenario_scores.get("fire_resilience", 0)

    water_gradient = calculate_gradient(water_target, reference_averages["water_security"])
    heat_gradient = calculate_gradient(heat_target, reference_averages["heat_exposure"])
    vegetation_gradient = calculate_gradient(vegetation_target, reference_averages["vegetation_condition"])
    fire_gradient = calculate_gradient(fire_target, reference_averages["fire_exposure"])

    water_class = classify_gradient(water_gradient)
    heat_class = classify_gradient(heat_gradient)
    vegetation_class = classify_gradient(vegetation_gradient)
    fire_class = classify_gradient(fire_gradient)

    result = {
        "water_gradient": water_gradient,
        "water_gradient_class": water_class,
        "heat_gradient": heat_gradient,
        "heat_gradient_class": heat_class,
        "vegetation_gradient": vegetation_gradient,
        "vegetation_gradient_class": vegetation_class,
        "fire_gradient": fire_gradient,
        "fire_gradient_class": fire_class,
        "differential_status": _derive_differential_status(
            water_class,
            heat_class,
            vegetation_class,
            fire_class,
        ),
        "reference_record_count": len(records),
    }
    result["differential_summary"] = summarize_differential_field(result)
    return result


def summarize_differential_field(differential_result):
    """Create a cautious one-sentence differential field interpretation."""
    status = differential_result.get("differential_status", "mixed_or_neutral_differential")
    water_class = differential_result.get("water_gradient_class", "unknown")
    heat_class = differential_result.get("heat_gradient_class", "unknown")
    vegetation_class = differential_result.get("vegetation_gradient_class", "unknown")
    fire_class = differential_result.get("fire_gradient_class", "unknown")

    if status == "water_advantage_with_heat_relief":
        reading = "water advantage with reduced heat pressure"
    elif status == "water_stress_with_heat_pressure":
        reading = "water stress with increased heat pressure"
    elif status == "vegetation_buffer_advantage":
        reading = "vegetation buffer advantage with comparatively lower fire exposure"
    elif status == "elevated_fire_exposure":
        reading = "elevated fire exposure"
    else:
        reading = "mixed or neutral gradients"

    return (
        "Differential field cautiously indicates "
        f"{reading} compared with representative Batlow context "
        f"(water={water_class}, heat={heat_class}, vegetation={vegetation_class}, fire={fire_class})."
    )
