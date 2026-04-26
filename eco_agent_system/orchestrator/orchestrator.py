from typing import Any, Dict
from agents.planning_agent import run_planning_agent
from agents.delivery_agent import run_delivery_agent
from agents.operations_agent import run_operations_agent

def run_system(eco_data: Dict[str, Any]) -> Dict[str, Any]:
    print("[orchestrator] Starting professional agent system")
    planning = run_planning_agent(eco_data)
    delivery = run_delivery_agent(eco_data)
    operations = run_operations_agent(eco_data)
    final_report = {
        "planning": planning,
        "delivery": delivery,
        "operations": operations,
        "lifecycle_feedback": {
            "principle": "Operations feedback should inform future planning and delivery controls.",
            "next_step": "Use operations monitoring results to update planning assumptions and risk rules."
        }
    }
    print("[orchestrator] Agent system completed")
    return final_report
