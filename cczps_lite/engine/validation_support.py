"""Generate deterministic, local-only professional validation support artifacts."""
from __future__ import annotations
import json
from pathlib import Path

PROJECT_DIR=Path(__file__).resolve().parent.parent
OUTPUT_DIR=PROJECT_DIR/"output"
HYPOTHESES_PATH=OUTPUT_DIR/"planning_hypotheses.json"
SCHEMA_VERSION="1.0"
SAFETY_BOUNDARY=("Planning support only. Outputs do not constitute professional validation, planning approval, engineering design, construction advice, simulation readiness, or an autonomous decision. Qualified human review is required.")
REVIEW_CATEGORIES=["planning_validity","environmental_validity","hydrology_terrain_relevance","energy_infrastructure_relevance","evidence_sufficiency","uncertainty_level","recommendation_status"]
SPATIAL_CATEGORIES=[
 {"category":"terrain_and_dem","required_layers":["DEM tile","elevation","slope","aspect"],"purpose":"Terrain context, elevation gradients, and highland/lowland comparison.","quality_limits":["resolution","vertical datum","voids","terrain modification date"]},
 {"category":"hydrology","required_layers":["watershed boundary","flow direction","flow accumulation","stream network"],"purpose":"Upstream/downstream interpretation and runoff pathway review.","quality_limits":["delineation method","seasonality","engineered drainage","field verification"]},
 {"category":"land_surface","required_layers":["land cover","vegetation","soil or surface class","land use"],"purpose":"Ecological transition, restoration, runoff, and exposure context.","quality_limits":["classification date","classification accuracy","local change"]},
 {"category":"infrastructure_and_boundaries","required_layers":["infrastructure","administrative boundary","site boundary polygon","risk-relevant spatial layers"],"purpose":"Access, service, jurisdiction, hazard, and planning constraint review.","quality_limits":["completeness","authority","currency","licensing"]},
]

def _load_hypotheses(path=HYPOTHESES_PATH):
    if not path.exists() or not path.read_text(encoding="utf-8").strip(): return {"hypotheses":{}}
    return json.loads(path.read_text(encoding="utf-8"))

def build_gis_dem_access_plan():
    return {"schema_version":SCHEMA_VERSION,"artifact":"GIS / DEM Data Access Plan","implementation_status":"planning_only","provider_required":False,"core_inputs":["latitude","longitude","boundary polygon","analysis radius"],"spatial_data_categories":SPATIAL_CATEGORIES,"candidate_sources":{"open_public":["SRTM DEM","Copernicus DEM","NASA / USGS elevation products","OpenStreetMap","public hydrology datasets","public land cover datasets"],"commercial_platform":["Google Earth","Google Earth Engine","ESRI ArcGIS","other mapping and spatial computation platforms"],"specialist_model_oriented":["QGIS","GRASS GIS","TauDEM","WhiteboxTools","hydrological preprocessing tools","CFD / microclimate model inputs where relevant"]},"connector_metadata":["data source","retrieval status","spatial resolution","date or version","license or access condition","uncertainty notes","cost owner","confidence level"],"connector_architecture":["User-selected core location","GIS / DEM Connector","Spatial Feature Extraction","Reference Point Suggestion","Evidence Layer","Planning Hypothesis Runtime","Validation Layer"],"governance":{"usage_cost_governance_required":True,"budget_guard_required":True,"manual_approval_for_external_or_paid_resources":True,"cache_first_where_permitted":True,"hidden_cost_absorption_permitted":False,"cost_distinctions":["user cost","platform service fee","external provider cost"],"principle":"The system should not block advanced spatial tools. It should enable them responsibly."},"future_capabilities":["elevation profile extraction","upstream / downstream classification","highland / lowland comparison","watershed-scale transect support","wind-corridor and terrain-channel interpretation","dryland runoff pathway interpretation","ecological transition-zone identification","desertification and restoration context support"],"human_verification_required":True,"safety_boundary":SAFETY_BOUNDARY}

def build_professional_validation_interface(hypotheses):
    reviews={}
    for key,item in hypotheses.get("hypotheses",{}).items():
        reviews[key]={"scenario":item.get("scenario",key),"hypothesis_id":item.get("hypothesis_id"),"hypothesis_status":item.get("hypothesis_status"),"review_status":"awaiting_professional_review","review_categories":{category:{"finding":None,"evidence_references":[],"confidence_level":"not_assessed","required_follow_up":[]} for category in REVIEW_CATEGORIES},"required_disciplines":["qualified planner","environmental specialist","GIS / terrain or hydrology specialist where relevant","infrastructure or energy specialist where relevant","local and community knowledge holder"],"human_sign_off_required":True}
    return {"schema_version":SCHEMA_VERSION,"artifact":"Professional Validation Interface","allowed_confidence_levels":["not_assessed","low","medium","high"],"allowed_recommendation_statuses":["not_reviewed","rejected","conditional","supported_for_further_assessment"],"reviews":reviews,"safety_boundary":SAFETY_BOUNDARY}

def build_expert_review_records(interface):
    records=[]
    for key,review in interface.get("reviews",{}).items():
        records.append({"record_id":f"{key}_expert_review_001","reviewer_role":None,"review_date":None,"reviewed_scenario_or_module":review["scenario"],"review_category":None,"finding":None,"evidence_reference":[],"confidence_level":"not_assessed","required_follow_up":[],"decision_status":"not_reviewed","human_authored":True,"record_status":"template"})
    return {"schema_version":SCHEMA_VERSION,"artifact":"Expert Review Record Layer","allowed_decision_statuses":["not_reviewed","approved_for_further_assessment","conditional","rejected"],"audit_requirements":["preserve reviewer role and review date","preserve evidence references","do not overwrite prior signed records","record revisions as new records"],"records":records,"safety_boundary":SAFETY_BOUNDARY}

def build_planning_approval_support_report(hypotheses,gis_plan,interface,review_records):
    decisions={r["reviewed_scenario_or_module"]:r["decision_status"] for r in review_records.get("records",[])}
    scenarios=[]
    for key,item in hypotheses.get("hypotheses",{}).items():
        scenario=item.get("scenario",key)
        scenarios.append({"scenario":scenario,"scenario_background":item.get("problem_statement"),"planning_hypothesis":item.get("planning_assumption"),"data_sources_required":[c["category"] for c in gis_plan["spatial_data_categories"]],"gis_dem_readiness":"planning_only_not_acquired","validation_status":interface.get("reviews",{}).get(key,{}).get("review_status","awaiting_professional_review"),"expert_review_outcome":decisions.get(scenario,"not_reviewed"),"evidence_strength":item.get("hypothesis_status"),"unresolved_risks":item.get("failure_conditions",[]),"human_approval_boundary":"CCZPS-Lite cannot grant planning, regulatory, engineering, environmental, or construction approval.","recommended_next_steps":["confirm required spatial datasets and licensing","complete relevant professional validation categories","record expert findings with evidence references","resolve material uncertainty before any approval process"],"approval_support_status":"not_ready_for_approval"})
    return {"schema_version":SCHEMA_VERSION,"artifact":"Planning Approval Support Report","report_status":"planning_support_only","scenarios":scenarios,"human_approval_required":True,"safety_boundary":SAFETY_BOUNDARY}

def _render(title,data):
    lines=[f"# {title}","",SAFETY_BOUNDARY,"",f"Schema version: {data['schema_version']}",""]
    if "scenarios" in data:
        for item in data["scenarios"]: lines += [f"## {item['scenario']}","",f"- GIS / DEM readiness: {item['gis_dem_readiness']}",f"- Validation status: {item['validation_status']}",f"- Expert review outcome: {item['expert_review_outcome']}",f"- Approval support status: {item['approval_support_status']}",""]
    elif "reviews" in data:
        for item in data["reviews"].values(): lines += [f"## {item['scenario']}","",f"- Review status: {item['review_status']}",f"- Human sign-off required: {item['human_sign_off_required']}",f"- Categories: {', '.join(item['review_categories'])}",""]
    elif "records" in data:
        for item in data["records"]: lines += [f"## {item['reviewed_scenario_or_module']}","",f"- Record ID: {item['record_id']}","- Finding: Not recorded","- Decision: not_reviewed",""]
    else:
        lines += ["## Connector Architecture","",*[f"{i}. {step}" for i,step in enumerate(data["connector_architecture"],1)],"","> The system should not block advanced spatial tools. It should enable them responsibly.",""]
    return "\n".join(lines).rstrip()+"\n"

def build_validation_support_outputs():
    hypotheses=_load_hypotheses(); gis=build_gis_dem_access_plan(); interface=build_professional_validation_interface(hypotheses); reviews=build_expert_review_records(interface); report=build_planning_approval_support_report(hypotheses,gis,interface,reviews)
    return {"gis_dem_access_plan":(gis,_render("GIS / DEM Data Access Plan",gis)),"professional_validation_interface":(interface,_render("Professional Validation Interface",interface)),"expert_review_records":(reviews,_render("Expert Review Record Layer",reviews)),"planning_approval_support_report":(report,_render("Planning Approval Support Report",report))}

def write_validation_support_outputs(outputs=None,output_dir=OUTPUT_DIR):
    output_dir.mkdir(parents=True,exist_ok=True)
    for name,(data,markdown) in (outputs or build_validation_support_outputs()).items():
        (output_dir/f"{name}.json").write_text(json.dumps(data,indent=2,ensure_ascii=True)+"\n",encoding="utf-8")
        (output_dir/f"{name}.md").write_text(markdown,encoding="utf-8")

def main():
    write_validation_support_outputs(); print(f"Wrote validation support artifacts to {OUTPUT_DIR}")
if __name__=="__main__": main()
