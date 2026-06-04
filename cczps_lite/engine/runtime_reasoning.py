"""Runtime reasoning statements for CCZPS-Lite."""


def derive_runtime_reasoning(scenario: dict, runtime_fields: dict) -> str:
    """Create a short human-readable interpretation for a scenario."""
    scenario_type = scenario.get("scenario_type", "")
    validation_text = "requires validation" if runtime_fields.get("validation_required") else "has moderate demonstrator confidence"

    if scenario_type == "water_priority":
        focus = "water security and drought resilience"
    elif scenario_type == "energy_resilience":
        focus = "energy continuity and emergency support"
    elif scenario_type == "ecology_fire_buffer_priority":
        focus = "ecological recovery and fire-buffer resilience"
    else:
        focus = "general resilience planning"

    return (
        f"This pathway emphasises {focus}. The runtime signal is "
        f"{runtime_fields.get('water_balance_signal')} for water balance and "
        f"{runtime_fields.get('ecological_signal')} for ecological resilience; it {validation_text}."
    )
