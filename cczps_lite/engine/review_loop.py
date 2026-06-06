"""Validation Feedback / Review Loop Runtime for CCZPS-Lite.

This module converts concept-level validation results into transparent review
routing. It does not initiate external workflows or replace professional,
community, or site-specific review.
"""

from __future__ import annotations


REVIEW_ACTIONS = {
    "Insufficient Evidence": "Hold and collect evidence",
    "Requires Technical Validation": "Escalate to technical review",
    "Requires Local Validation": "Send to local review",
    "Validated Enough for Concept Review": "Proceed to concept review",
}


def _as_list(values) -> list[str]:
    if isinstance(values, str):
        return [value.strip() for value in values.split(";") if value.strip()]
    return [str(value).strip() for value in (values or []) if str(value).strip()]


def classify_review_priority(validation_status, validation_score, validation_gaps):
    """Classify how promptly a pathway should enter concept-level review."""
    if validation_score < 4 or validation_status == "Insufficient Evidence":
        return "High"
    if validation_status in {"Requires Technical Validation", "Requires Local Validation"}:
        return "Medium"
    if validation_status == "Validated Enough for Concept Review":
        return "Low"
    return "Medium" if _as_list(validation_gaps) else "Low"


def derive_review_owner(validation_gaps, primary_forcing):
    """Route review to the most relevant concept-level reviewer."""
    review_text = " ".join(_as_list(validation_gaps) + [str(primary_forcing or "")]).lower()
    owner_rules = (
        (("hydrolog", "soil moisture", "water storage"), "Water / hydrology reviewer"),
        (("temperature", "evaporation", "heat exposure"), "Microclimate reviewer"),
        (("bushfire", "fire exposure", "vegetation management"), "Fire resilience reviewer"),
        (("ecological", "canopy-cover", "canopy cover", "vegetation stress"), "Ecology reviewer"),
        (("stronger field evidence", "technical assessment"), "Evidence coordinator"),
    )
    for terms, owner in owner_rules:
        if any(term in review_text for term in terms):
            return owner
    return "Governance reviewer"


def summarize_review_loop(review_result):
    """Create a cautious sentence describing the next review step."""
    return (
        "Review loop recommends "
        f"{review_result.get('review_action', 'Send to local review').lower()} at "
        f"{review_result.get('review_priority', 'Medium').lower()} priority, led by the "
        f"{review_result.get('review_owner', 'Governance reviewer')}. This is a concept-level "
        "routing suggestion and remains subject to human judgement."
    )


def derive_review_action(validation_result, evidence_result, forcing_result):
    """Derive the complete review-loop reading from existing runtime outputs."""
    validation_status = validation_result.get("validation_status", "Requires Local Validation")
    validation_score = validation_result.get("validation_score", 0)
    validation_gaps = _as_list(validation_result.get("validation_gaps", []))
    primary_forcing = forcing_result.get("primary_forcing", "")
    triggers = list(validation_gaps)
    if primary_forcing and primary_forcing not in triggers:
        triggers.append(primary_forcing)

    review_result = {
        "review_action": REVIEW_ACTIONS.get(validation_status, "Send to local review"),
        "review_priority": classify_review_priority(
            validation_status,
            validation_score,
            validation_gaps,
        ),
        "review_owner": derive_review_owner(validation_gaps, primary_forcing),
        "review_triggers": triggers,
    }
    review_result["review_summary"] = summarize_review_loop(review_result)
    return review_result
