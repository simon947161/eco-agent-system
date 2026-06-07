"""Evidence layer for CCZPS-Lite.

This module converts scenario evidence records into transparent governance
fields. It does not validate the evidence externally, connect to live services,
or make scientific claims beyond the local input file.
"""

_ALLOWED_STRENGTHS = {"low": "Low", "medium": "Medium", "high": "High"}
_SOURCE_BASIS = {
    "local observations": "Local Observation",
    "historical bushfire experience": "Historical Experience",
    "historical experience": "Historical Experience",
    "concept study": "Concept Study",
    "literature review": "Literature Review",
    "expert judgement": "Expert Judgement",
    "regional understanding": "Expert Judgement",
    "meteorological observation": "Meteorological Observation",
}
_UNCERTAINTY_BY_STRENGTH = {
    "Low": "Limited quantitative evidence available. Concept-level assumptions only.",
    "Medium": "Regional evidence available but site-specific validation required.",
    "High": "Evidence basis is comparatively strong, but final decisions still require human review.",
}
_UNCERTAINTY_BY_SOURCE = {
    "Local Observation": "Further hydrological validation recommended.",
    "Concept Study": "Concept-level assumptions only.",
    "Expert Judgement": "Regional evidence available but site-specific validation required.",
}


def _records(evidence):
    if not evidence:
        return []
    if "strength" in evidence or "source" in evidence:
        return [evidence]
    return [record for record in evidence.values() if isinstance(record, dict)]


def derive_evidence_strength(evidence):
    """Return Low, Medium, or High for one evidence record or a group of records."""
    records = _records(evidence)
    if not records:
        return "Low"

    strengths = [
        _ALLOWED_STRENGTHS.get(str(record.get("strength", "low")).lower(), "Low")
        for record in records
    ]
    rank = {"Low": 1, "Medium": 2, "High": 3}
    weakest = min(strengths, key=lambda item: rank[item])
    return weakest


def derive_source_basis(evidence):
    """Describe where assumptions come from using standard source categories."""
    records = _records(evidence)
    if not records:
        return "Mixed Sources"

    sources = {
        _SOURCE_BASIS.get(str(record.get("source", "")).lower(), "Mixed Sources")
        for record in records
    }
    sources.discard("")
    if len(sources) == 1:
        return sources.pop()
    return "Mixed Sources"


def derive_uncertainty_notes(evidence):
    """Generate a short uncertainty statement for an evidence record or group."""
    strength = derive_evidence_strength(evidence)
    source_basis = derive_source_basis(evidence)
    if source_basis in _UNCERTAINTY_BY_SOURCE:
        return _UNCERTAINTY_BY_SOURCE[source_basis]
    return _UNCERTAINTY_BY_STRENGTH[strength]


def derive_human_review_required(evidence):
    """Require human review when the evidence strength is Low."""
    return derive_evidence_strength(evidence) == "Low"


def meteorology_evidence_record(reading):
    """Convert a meteorology reading into supporting evidence without conclusions."""
    if not reading or reading.get("retrieval_status") != "success":
        return {
            "strength": "low",
            "source": "meteorological observation",
            "notes": "Meteorology observation unavailable; no observational inference made.",
            "meteorology_reading": reading or {},
            "indicators": [],
        }
    confidence = str(reading.get("confidence", "low")).lower()
    strength = confidence if confidence in _ALLOWED_STRENGTHS else "low"
    indicators = []
    indicator_fields = {
        "rainfall_mm": "recent rainfall",
        "temperature_c": "air temperature",
        "evaporation_mm": "evaporation indicator",
        "humidity_percent": "relative humidity",
    }
    for field, label in indicator_fields.items():
        if reading.get(field) is not None:
            indicators.append(label)
    return {
        "strength": strength,
        "source": "meteorological observation",
        "notes": "Observational values are supporting evidence only; no conclusion or score change is applied.",
        "meteorology_reading": reading,
        "indicators": indicators,
    }
