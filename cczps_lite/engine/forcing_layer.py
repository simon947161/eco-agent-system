"""Forcing Layer Runtime for CCZPS-Lite.

This module interprets differential field signals as candidate environmental
pressures. It is a transparent rule-based layer for review only, not causal
proof, validation, live weather analysis, GIS analysis, or physical modelling.
"""

from __future__ import annotations

NEGATIVE_CLASSES = {"moderate_negative", "strong_negative"}
POSITIVE_CLASSES = {"moderate_positive", "strong_positive"}
UNCLEAR_FORCING = "Mixed / Unclear Forcing"
PROTECTIVE_FORCING = "Microclimate Buffer Support"


def _add_candidate(candidates, candidate):
    if candidate not in candidates:
        candidates.append(candidate)


def derive_forcing_candidates(differential_result, scenario_scores=None):
    """Derive candidate forcing signals from differential field output.

    ``scenario_scores`` is accepted for future compatibility with scenario-aware
    rules, but Task 08 intentionally uses only differential runtime fields.
    """
    candidates = []
    water_class = differential_result.get("water_gradient_class")
    heat_class = differential_result.get("heat_gradient_class")
    vegetation_class = differential_result.get("vegetation_gradient_class")
    fire_class = differential_result.get("fire_gradient_class")
    differential_status = differential_result.get("differential_status")

    if water_class in NEGATIVE_CLASSES and heat_class in POSITIVE_CLASSES:
        _add_candidate(candidates, "Water Storage Deficit")
        _add_candidate(candidates, "Heat Exposure")
        _add_candidate(candidates, "Evaporation Pressure")

    if heat_class in POSITIVE_CLASSES:
        _add_candidate(candidates, "Heat Exposure")
        _add_candidate(candidates, "Evaporation Pressure")

    if vegetation_class in NEGATIVE_CLASSES:
        _add_candidate(candidates, "Vegetation Stress")
        _add_candidate(candidates, "Microclimate Buffer Loss")

    if fire_class in POSITIVE_CLASSES:
        _add_candidate(candidates, "Fire Exposure")
        _add_candidate(candidates, "Vegetation Stress")

    if differential_status == "water_advantage_with_heat_relief":
        _add_candidate(candidates, PROTECTIVE_FORCING)

    if not candidates:
        candidates.append(UNCLEAR_FORCING)

    forcing_result = {
        "forcing_candidates": candidates,
        "primary_forcing": candidates[0],
        "forcing_priority": classify_forcing_priority(candidates),
    }
    forcing_result["forcing_summary"] = summarize_forcing_layer(forcing_result)
    return forcing_result


def classify_forcing_priority(candidates):
    """Classify forcing priority using a small explainable rule set."""
    candidate_set = set(candidates)
    if {"Fire Exposure", "Heat Exposure"}.issubset(candidate_set):
        return "High"
    if {"Water Storage Deficit", "Evaporation Pressure"}.issubset(candidate_set):
        return "High"
    if candidate_set == {UNCLEAR_FORCING}:
        return "Low"
    if len(candidates) >= 2:
        return "Medium"
    return "Medium"


def summarize_forcing_layer(forcing_result):
    """Create a short cautious forcing-layer interpretation."""
    candidates = forcing_result.get("forcing_candidates", [])
    if isinstance(candidates, str):
        candidates = [candidate.strip() for candidate in candidates.split(";") if candidate.strip()]

    if not candidates or candidates == [UNCLEAR_FORCING]:
        return "Forcing layer does not identify a dominant candidate driver from the current representative gradients."

    if candidates == [PROTECTIVE_FORCING]:
        return "Forcing layer cautiously identifies microclimate buffer support as a possible protective influence."

    candidate_text = ", ".join(candidate.lower() for candidate in candidates)
    return (
        "Forcing layer cautiously identifies "
        f"{candidate_text} as candidate drivers behind the observed differential field."
    )
