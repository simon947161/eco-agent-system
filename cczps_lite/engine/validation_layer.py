"""Validation Layer Runtime for CCZPS-Lite.

This module combines runtime fields, differential signals, candidate forcings,
and evidence metadata into a cautious concept-level validation reading. It does
not claim scientific validation and does not replace local or technical review.
"""

from __future__ import annotations

LOW_EVIDENCE_GAP = "Need stronger field evidence or technical assessment"
HEAT_EVAPORATION_GAP = "Need local temperature, humidity, and evaporation observation"
WATER_STORAGE_GAP = "Need hydrological or soil moisture validation"
FIRE_EXPOSURE_GAP = "Need bushfire exposure and vegetation management review"
VEGETATION_STRESS_GAP = "Need ecological condition and canopy-cover review"
NO_MAJOR_GAP = "No major validation gap identified at concept level"


def _normalise_evidence_strength(evidence_strength):
    return str(evidence_strength or "Low").strip().title()


def _as_bool(value) -> bool:
    if isinstance(value, bool):
        return value
    if isinstance(value, str):
        return value.strip().lower() in {"true", "yes", "1", "required"}
    return bool(value)


def _forcing_candidates(forcing_result) -> list[str]:
    candidates = forcing_result.get("forcing_candidates", [])
    if isinstance(candidates, str):
        return [candidate.strip() for candidate in candidates.split(";") if candidate.strip()]
    return [str(candidate) for candidate in candidates]


def _add_gap(gaps, gap):
    if gap not in gaps:
        gaps.append(gap)


def classify_validation_status(validation_score, validation_required, evidence_strength):
    """Classify a concept-level validation score into a cautious status."""
    normalised_evidence = _normalise_evidence_strength(evidence_strength)
    if normalised_evidence == "Low" and validation_score < 5:
        return "Insufficient Evidence"
    if _as_bool(validation_required) and validation_score < 6:
        return "Requires Technical Validation"
    if validation_score >= 7:
        return "Validated Enough for Concept Review"
    return "Requires Local Validation"


def derive_validation_reading(runtime_fields, differential_result, forcing_result, evidence_result):
    """Derive an evidence-aware validation reading from existing runtime layers."""
    evidence_strength = _normalise_evidence_strength(evidence_result.get("evidence_strength"))
    confidence_level = str(runtime_fields.get("confidence_level", "low")).strip().lower()
    validation_required = _as_bool(runtime_fields.get("validation_required", True))
    human_review_required = _as_bool(evidence_result.get("human_review_required", False))
    forcing_priority = str(forcing_result.get("forcing_priority", "Medium")).strip().title()
    candidates = _forcing_candidates(forcing_result)

    validation_score = 6.0
    if evidence_strength == "High":
        validation_score += 2
    elif evidence_strength == "Medium":
        validation_score += 1
    elif evidence_strength == "Low":
        validation_score -= 2

    if confidence_level == "medium":
        validation_score += 1
    elif confidence_level == "low":
        validation_score -= 1

    if validation_required:
        validation_score -= 1
    if human_review_required:
        validation_score -= 1
    if forcing_priority == "High" and evidence_strength == "Low":
        validation_score -= 1

    validation_score = round(min(10.0, max(0.0, validation_score)), 2)
    validation_status = classify_validation_status(
        validation_score,
        validation_required,
        evidence_strength,
    )

    gaps = []
    if evidence_strength == "Low":
        _add_gap(gaps, LOW_EVIDENCE_GAP)
    if "Heat Exposure" in candidates or "Evaporation Pressure" in candidates:
        _add_gap(gaps, HEAT_EVAPORATION_GAP)
    if "Water Storage Deficit" in candidates:
        _add_gap(gaps, WATER_STORAGE_GAP)
    if "Fire Exposure" in candidates:
        _add_gap(gaps, FIRE_EXPOSURE_GAP)
    if "Vegetation Stress" in candidates or "Microclimate Buffer Loss" in candidates:
        _add_gap(gaps, VEGETATION_STRESS_GAP)
    if not gaps:
        gaps.append(NO_MAJOR_GAP)

    validation_result = {
        "validation_score": validation_score,
        "validation_status": validation_status,
        "validation_gaps": gaps,
        "evidence_strength": evidence_strength,
        "validation_required": validation_required,
        "forcing_priority": forcing_priority,
    }
    validation_result["validation_summary"] = summarize_validation_layer(validation_result)
    return validation_result


def summarize_validation_layer(validation_result):
    """Create one cautious sentence for the validation layer reading."""
    status = validation_result.get("validation_status", "Requires Local Validation")
    evidence_strength = str(validation_result.get("evidence_strength", "Low")).lower()
    score = validation_result.get("validation_score", 0)

    if status == "Validated Enough for Concept Review":
        return (
            "Validation layer cautiously considers this pathway sufficient for "
            f"concept-level review (score {score}), but local consultation and site checks remain necessary."
        )
    if status == "Insufficient Evidence":
        return (
            "Validation layer cautiously rates this pathway as insufficient evidence "
            f"because evidence is {evidence_strength} and candidate assumptions remain unresolved."
        )
    if status == "Requires Technical Validation":
        return (
            "Validation layer cautiously rates this pathway as requiring technical validation "
            f"due to {evidence_strength} evidence and unresolved candidate forcing assumptions."
        )
    return (
        "Validation layer cautiously rates this pathway as requiring local validation "
        f"because evidence is {evidence_strength} and forcing remains candidate-only."
    )
