from typing import Any, Dict, List

def run_delivery_agent(eco_data: Dict[str, Any]) -> Dict[str, Any]:
    print("[delivery_agent] processing")
    risk_index = float(eco_data.get("risk_index", 0))
    evaporation_pressure = float(eco_data.get("evaporation_pressure", 0))
    resilience = float(eco_data.get("resilience", 0))
    if risk_index >= 60:
        risk_level = "critical"
    elif risk_index >= 30:
        risk_level = "high"
    elif risk_index >= 15:
        risk_level = "moderate"
    else:
        risk_level = "controlled"
    whs_flags: List[str] = []
    environmental_controls: List[str] = []
    if evaporation_pressure >= 20:
        whs_flags.append("heat_stress_watch")
        environmental_controls.append("evaporation_reduction_plan")
    if risk_index >= 30:
        whs_flags.append("site_safety_review")
        environmental_controls.append("active_environmental_monitoring")
    if resilience < 0.5:
        environmental_controls.append("resilience_support_required")
    if not whs_flags:
        whs_flags.append("standard_site_safety_monitoring")
    if not environmental_controls:
        environmental_controls.append("standard_environmental_controls")
    esg = {
        "E": "active_environmental_control_required" if environmental_controls != ["standard_environmental_controls"] else "standard_environmental_control",
        "S": "worker_and_community_risk_attention_required" if risk_level in ["critical", "high"] else "managed_worker_and_community_risk",
        "G": "enhanced_site_governance" if risk_level in ["critical", "high"] else "standard_site_governance",
    }
    return {
        "agent_name": "Project Delivery & Risk Agent",
        "stage": "during_project",
        "risk_level": risk_level,
        "whs_flags": whs_flags,
        "environmental_controls": environmental_controls,
        "esg_flags": esg,
        "professional_note": "This agent translates Eco Engine outputs into project delivery, WHS/OHS, and construction-stage environmental risk language.",
    }
