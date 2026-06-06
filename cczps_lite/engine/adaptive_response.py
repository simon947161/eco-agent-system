"""Adaptive Response Runtime for CCZPS-Lite.

This module translates validation, review, forcing, and evidence readings into
cautious concept-level response suggestions. It does not provide final design,
engineering, construction, financial, environmental, or regulatory advice.
"""

from __future__ import annotations


RESPONSE_MODES = {
    "Insufficient Evidence": "Evidence-building response",
    "Requires Technical Validation": "Technical validation response",
    "Requires Local Validation": "Local consultation response",
    "Validated Enough for Concept Review": "Concept refinement response",
}


def _as_list(values) -> list[str]:
    if isinstance(values, str):
        return [value.strip() for value in values.split(";") if value.strip()]
    return [str(value).strip() for value in (values or []) if str(value).strip()]


def _add_options(options: list[str], candidates: tuple[str, ...]) -> None:
    for candidate in candidates:
        if candidate not in options:
            options.append(candidate)


def classify_response_priority(validation_status, review_priority, forcing_priority):
    """Classify the urgency of a candidate concept-level response."""
    if validation_status == "Insufficient Evidence" or review_priority == "High":
        return "High"
    if forcing_priority == "High" and validation_status != "Validated Enough for Concept Review":
        return "High"
    if validation_status in {"Requires Technical Validation", "Requires Local Validation"}:
        return "Medium"
    if review_priority == "Medium":
        return "Medium"
    if validation_status == "Validated Enough for Concept Review" or review_priority == "Low":
        return "Low"
    return "Medium"


def derive_response_options(validation_gaps, review_owner, primary_forcing):
    """Derive ordered, duplicate-free practical response suggestions."""
    signal_text = " ".join(
        _as_list(validation_gaps) + [str(review_owner or ""), str(primary_forcing or "")]
    ).lower()
    options: list[str] = []

    if any(term in signal_text for term in ("water storage", "hydrolog", "soil moisture")):
        _add_options(options, (
            "Water storage audit",
            "Soil moisture monitoring",
            "Irrigation timing review",
        ))
    if any(term in signal_text for term in ("heat exposure", "evaporation", "temperature")):
        _add_options(options, (
            "Microclimate shade strategy",
            "Night cooling / ventilation review",
            "Evaporation reduction planting",
        ))
    if any(term in signal_text for term in ("fire exposure", "bushfire")):
        _add_options(options, (
            "Bushfire buffer review",
            "Fire access and asset protection check",
            "Vegetation fuel management review",
        ))
    if any(term in signal_text for term in (
        "vegetation stress", "microclimate buffer loss", "ecological", "canopy-cover"
    )):
        _add_options(options, (
            "Canopy-cover assessment",
            "Shelterbelt / windbreak review",
            "Ecological buffer restoration",
        ))
    if any(term in signal_text for term in (
        "stronger field evidence", "low evidence", "evidence coordinator"
    )):
        _add_options(options, (
            "Field evidence collection plan",
            "Local observation protocol",
            "Expert review checklist",
        ))
    if "no major validation gap" in signal_text:
        _add_options(options, (
            "Concept design refinement",
            "Governance consultation",
            "Implementation pathway review",
        ))

    if not options:
        _add_options(options, (
            "Local conditions review",
            "Governance consultation",
            "Expert review checklist",
        ))
    return options


def summarize_adaptive_response(response_result):
    """Create a cautious summary of the suggested response direction."""
    options = _as_list(response_result.get("response_options", []))
    option_text = ", ".join(options[:2]).lower() if options else "local review"
    return (
        f"Adaptive response suggests a {response_result.get('response_mode', 'Local consultation response').lower()} "
        f"at {response_result.get('response_priority', 'Medium').lower()} priority, beginning with "
        f"{option_text}. These are candidate concept-level options, require review, and should be "
        "checked locally; they are not final design advice."
    )


def derive_adaptive_response(validation_result, review_result, forcing_result, evidence_result):
    """Derive the complete adaptive response reading from existing layers."""
    validation_status = validation_result.get("validation_status", "Requires Local Validation")
    response_result = {
        "response_priority": classify_response_priority(
            validation_status,
            review_result.get("review_priority", "Medium"),
            forcing_result.get("forcing_priority", "Medium"),
        ),
        "response_options": derive_response_options(
            validation_result.get("validation_gaps", []),
            review_result.get("review_owner", "Governance reviewer"),
            forcing_result.get("primary_forcing", ""),
        ),
        "response_mode": RESPONSE_MODES.get(validation_status, "Local consultation response"),
    }
    response_result["response_summary"] = summarize_adaptive_response(response_result)
    return response_result
