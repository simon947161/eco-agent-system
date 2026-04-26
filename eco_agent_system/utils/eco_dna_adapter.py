from typing import Any, Dict

def normalize_eco_dna(raw_data: Dict[str, Any]) -> Dict[str, Any]:
    if "state_vector" in raw_data or "risk" in raw_data or "recovery" in raw_data:
        state = raw_data.get("state_vector", {})
        risk = raw_data.get("risk", {})
        recovery = raw_data.get("recovery", {})
        meta = raw_data.get("meta", {})
        return {
            "water_balance": state.get("water_balance_signal", 0),
            "risk_index": risk.get("risk_index", 0),
            "evaporation_pressure": state.get("evaporation_pressure", 0),
            "resilience": state.get("ecological_resilience", 0),
            "scenario": meta.get("scenario_id", "unknown"),
            "risk_class": risk.get("ecosystem_risk_class", "unknown"),
            "recovery_phase": recovery.get("current_phase", "unknown"),
            "dependency_level": recovery.get("dependency_level", "unknown"),
            "self_recovery_potential": recovery.get("self_recovery_potential", "unknown"),
        }
    return {
        "water_balance": raw_data.get("water_balance", 0),
        "risk_index": raw_data.get("risk_index", 0),
        "evaporation_pressure": raw_data.get("evaporation_pressure", 0),
        "resilience": raw_data.get("resilience", 0),
        "scenario": raw_data.get("scenario", "unknown"),
        "risk_class": raw_data.get("risk_class", "unknown"),
        "recovery_phase": raw_data.get("recovery_phase", "unknown"),
        "dependency_level": raw_data.get("dependency_level", "unknown"),
        "self_recovery_potential": raw_data.get("self_recovery_potential", "unknown"),
    }
