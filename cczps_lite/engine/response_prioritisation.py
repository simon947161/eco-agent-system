"""Response Prioritisation Runtime for CCZPS-Lite.

This module orders candidate adaptive responses for concept-level review using
small, transparent rules. It does not make autonomous planning, construction,
implementation, or regulatory decisions.
"""

from __future__ import annotations


URGENCY_RANK = {"Routine": 1, "Moderate": 2, "Critical": 3}
BENEFIT_RANK = {
    "Implementation readiness improvement": 1,
    "Confidence improvement": 2,
    "Ecological resilience improvement": 3,
    "Hydrological resilience improvement": 4,
    "Risk reduction and asset protection": 5,
}


def _as_list(values) -> list[str]:
    if isinstance(values, str):
        return [value.strip() for value in values.split(";") if value.strip()]
    return [str(value).strip() for value in (values or []) if str(value).strip()]


def classify_urgency_level(response_priority, forcing_priority):
    """Classify urgency from response priority and the forcing signal."""
    signal = str(forcing_priority or "").lower()
    if any(term in signal for term in (
        "fire exposure", "extreme heat exposure", "water storage deficit"
    )):
        return "Critical"
    if any(term in signal for term in (
        "vegetation stress", "evaporation pressure", "microclimate buffer loss"
    )):
        return "Moderate"
    if any(term in signal for term in (
        "microclimate buffer support", "concept refinement", "governance consultation"
    )):
        return "Routine"
    if str(response_priority).title() == "High" and str(forcing_priority).title() == "High":
        return "Critical"
    if str(response_priority).title() in {"High", "Medium"}:
        return "Moderate"
    return "Routine"


def estimate_expected_benefit(response_option, primary_forcing):
    """Estimate the main concept-level benefit of one candidate response."""
    signal = f"{response_option or ''} {primary_forcing or ''}".lower()
    if any(term in signal for term in (
        "water", "hydrolog", "soil moisture", "irrigation", "evaporation"
    )):
        return "Hydrological resilience improvement"
    if any(term in signal for term in (
        "fire", "bushfire", "asset protection", "fuel management"
    )):
        return "Risk reduction and asset protection"
    if any(term in signal for term in (
        "vegetation", "canopy", "ecological", "shelterbelt", "windbreak", "planting"
    )):
        return "Ecological resilience improvement"
    if any(term in signal for term in (
        "evidence", "observation", "monitoring", "expert review"
    )):
        return "Confidence improvement"
    return "Implementation readiness improvement"


def _option_urgency(response_option: str) -> str:
    option = response_option.lower()
    if any(term in option for term in (
        "bushfire", "fire access", "water storage", "microclimate shade"
    )):
        return "Critical"
    if any(term in option for term in (
        "soil moisture", "irrigation", "evaporation", "vegetation", "canopy",
        "ecological", "shelterbelt", "windbreak", "night cooling"
    )):
        return "Moderate"
    return "Routine"


def rank_response_options(response_options, urgency_level):
    """Return the single highest-ranked candidate response."""
    options = _as_list(response_options)
    if not options:
        return "No candidate response identified"

    def rank(option: str) -> tuple[int, int, int, int]:
        option_urgency = _option_urgency(option)
        benefit = estimate_expected_benefit(option, "")
        evidence_bonus = 1 if "evidence" in option.lower() else 0
        return (
            URGENCY_RANK[option_urgency],
            URGENCY_RANK.get(urgency_level, 1),
            BENEFIT_RANK[benefit],
            evidence_bonus,
        )

    return max(enumerate(options), key=lambda item: (rank(item[1]), -item[0]))[1]


def summarize_response_prioritisation(result):
    """Create a cautious explanation of the suggested first response."""
    return (
        "Response prioritisation suggests considering "
        f"{result.get('prioritised_response', 'local review').lower()} first at "
        f"{result.get('implementation_priority', 'Medium').lower()} implementation priority. "
        f"Its expected concept-level benefit is {result.get('expected_benefit', 'implementation readiness improvement').lower()}. "
        "This suggested implementation sequence requires review and should be checked locally."
    )


def derive_response_prioritisation(response_result, validation_result, forcing_result):
    """Derive the response prioritisation reading from existing runtime layers."""
    validation_status = validation_result.get("validation_status", "Requires Local Validation")
    response_priority = response_result.get("response_priority", "Medium")
    forcing_priority = forcing_result.get("forcing_priority", "Medium")
    primary_forcing = forcing_result.get("primary_forcing", "")

    if validation_status == "Insufficient Evidence" or response_priority == "High" or forcing_priority == "High":
        implementation_priority = "High"
    elif validation_status in {"Requires Technical Validation", "Requires Local Validation"}:
        implementation_priority = "Medium"
    elif validation_status == "Validated Enough for Concept Review":
        implementation_priority = "Low"
    else:
        implementation_priority = "Medium"

    urgency_level = classify_urgency_level(response_priority, primary_forcing or forcing_priority)
    prioritised_response = rank_response_options(
        response_result.get("response_options", []), urgency_level
    )
    result = {
        "implementation_priority": implementation_priority,
        "urgency_level": urgency_level,
        "expected_benefit": estimate_expected_benefit(prioritised_response, primary_forcing),
        "prioritised_response": prioritised_response,
    }
    result["prioritisation_summary"] = summarize_response_prioritisation(result)
    return result
