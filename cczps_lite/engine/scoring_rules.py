"""Transparent scoring rules for CCZPS-Lite.

All scoring is indicative and intended for methodology demonstration only.
"""

RESILIENCE_FIELDS = (
    "water_security",
    "energy_resilience",
    "ecological_resilience",
    "fire_resilience",
)


def _average(values):
    return sum(values) / len(values) if values else 0.0


def calculate_resilience_score(scores: dict) -> float:
    """Average core environmental and infrastructure resilience scores."""
    values = [scores.get(field, 0) for field in RESILIENCE_FIELDS]
    return round(_average(values), 2)


def calculate_governance_score(scores: dict) -> float:
    """Estimate governance readiness with a simple complexity penalty."""
    community_acceptance = scores.get("community_acceptance", 0)
    investment_feasibility = scores.get("investment_feasibility", 0)
    implementation_complexity = scores.get("implementation_complexity", 0)
    base_score = _average([community_acceptance, investment_feasibility])
    complexity_penalty = implementation_complexity * 0.15
    return round(max(0.0, base_score - complexity_penalty), 2)


def calculate_risk_adjusted_score(scores: dict) -> float:
    """Combine resilience and governance scores while penalizing validation need."""
    resilience_score = calculate_resilience_score(scores)
    governance_score = calculate_governance_score(scores)
    validation_penalty = scores.get("validation_need", 0) * 0.2
    combined_score = (resilience_score * 0.6) + (governance_score * 0.4)
    return round(max(0.0, combined_score - validation_penalty), 2)


def classify_recommendation(score: float) -> str:
    """Convert an indicative score into a cautious recommendation class."""
    if score >= 7.0:
        return "High Priority"
    if score >= 5.5:
        return "Promising but Requires Validation"
    if score >= 4.0:
        return "Moderate Priority"
    return "Low Priority"
