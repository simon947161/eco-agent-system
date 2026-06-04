"""Runtime field derivation for CCZPS-Lite.

The fields are simple, transparent interpretations of scenario scores. They are
not live environmental measurements or scientific simulation outputs.
"""


def derive_runtime_fields(scores: dict) -> dict:
    """Derive indicative runtime fields from editable scenario scores."""
    water_security = scores.get("water_security", 0)
    ecological_resilience = scores.get("ecological_resilience", 0)
    fire_resilience = scores.get("fire_resilience", 0)
    validation_need = scores.get("validation_need", 0)

    risk_index = round((10 - water_security + 10 - fire_resilience + validation_need) / 3, 2)
    water_balance_signal = "stabilising" if water_security >= 8 else "watch" if water_security >= 6 else "stressed"
    ecological_signal = "strong" if ecological_resilience >= 8 else "moderate" if ecological_resilience >= 6 else "limited"
    evaporation_pressure = "high" if water_security <= 6 else "managed"
    confidence_level = "medium" if validation_need <= 5 else "low"
    validation_required = validation_need >= 6

    return {
        "risk_index": risk_index,
        "water_balance_signal": water_balance_signal,
        "ecological_signal": ecological_signal,
        "evaporation_pressure": evaporation_pressure,
        "confidence_level": confidence_level,
        "validation_required": validation_required,
    }
