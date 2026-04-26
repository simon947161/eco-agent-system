from typing import Any, Dict, List

def run_planning_agent(eco_data: Dict[str, Any]) -> Dict[str, Any]:
    print("[planning_agent] processing")
    water_balance = float(eco_data.get("water_balance", 0))
    risk_index = float(eco_data.get("risk_index", 0))
    scenario = str(eco_data.get("scenario", "unknown"))
    risk_class = str(eco_data.get("risk_class", "unknown"))
    early_risks: List[str] = [f"scenario:{scenario}", f"risk_class:{risk_class}"]
    if water_balance < 0:
        early_risks.append("water_balance_deficit")
    if risk_index >= 50:
        early_risks.append("high_environmental_risk")
    elif risk_index >= 25:
        early_risks.append("moderate_environmental_risk")
    esg = {
        "E": "environmental_constraints_require_design_response" if water_balance < 0 or risk_index >= 25 else "environmental_condition_currently_manageable",
        "S": "community_and_land_use_impacts_should_be_screened" if risk_index >= 25 else "standard_social_screening",
        "G": "planning_controls_and_approval_pathway_required",
    }
    return {
        "agent_name": "Planning & Approval Agent",
        "stage": "before_project",
        "approval_path": ["site_context_review", "environmental_pre_assessment", "planning_controls_check", "approval_pathway_identification"],
        "early_risks": early_risks,
        "esg_flags": esg,
        "professional_note": "This agent translates Eco Engine outputs into early planning, approval, and ESG++ pre-screening language.",
    }
