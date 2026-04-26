from typing import Any, Dict, List

def run_operations_agent(eco_data: Dict[str, Any]) -> Dict[str, Any]:
    print("[operations_agent] processing")
    resilience = float(eco_data.get("resilience", 0))
    water_balance = float(eco_data.get("water_balance", 0))
    recovery_phase = str(eco_data.get("recovery_phase", "unknown"))
    risk_class = str(eco_data.get("risk_class", "unknown"))
    recovery_needed = resilience < 0.5 or water_balance < 0
    actions: List[str] = ["seasonal_inspection", "sensor_health_check", "maintenance_log_update"]
    if recovery_needed:
        actions.append("resilience_recovery_plan")
        actions.append("water_support_review")
    if recovery_phase in ["stabilizing", "starting"]:
        actions.append("do_not_reduce_support_too_early")
    value_score = round(max(0.0, min(1.0, resilience)), 2)
    tokenizable = value_score >= 0.6 and water_balance >= 0 and risk_class not in ["high", "critical"]
    esg = {
        "E": "ecological_recovery_still_required" if recovery_needed else "ecological_condition_improving",
        "S": "service_reliability_watch" if recovery_needed else "service_reliability_stable",
        "G": "tight_operational_governance" if recovery_needed else "normal_operational_governance",
    }
    return {
        "agent_name": "Operations & Maintenance Agent",
        "stage": "after_project",
        "resilience_score": f"{resilience:.2f}",
        "maintenance_actions": actions,
        "eco_asset_potential": {
            "eco_asset": {
                "type": "water_energy_recovery",
                "value_score": value_score,
                "tokenizable": tokenizable,
                "rwa_note": "This is an early screening flag only. Real RWA use requires verified data, audit trail, and legal compliance.",
            }
        },
        "esg_flags": esg,
        "professional_note": "This agent translates Eco Engine outputs into long-term operation, maintenance, resilience, and early eco-asset language.",
    }
