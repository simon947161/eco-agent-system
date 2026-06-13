"""Generate deterministic local evidence traceability records without inference."""
from __future__ import annotations
import json
from pathlib import Path

PROJECT_DIR=Path(__file__).resolve().parent.parent
OUTPUT_DIR=PROJECT_DIR/"output"
OUTPUT_PATH=OUTPUT_DIR/"evidence_traceability.json"
REPORT_PATH=OUTPUT_DIR/"evidence_traceability.md"
SCHEMA_VERSION="1.0"
SAFETY_BOUNDARY="Traceability only. Records preserve existing source statements and do not create conclusions, governance decisions, professional review, approval readiness, engineering readiness, regulatory readiness, or recommendations."
REQUIRED_FIELDS=("trace_id","scenario_id","artifact_type","artifact_id","claim_or_output_summary","supporting_evidence_ids","evidence_source","evidence_type","evidence_strength","confidence","review_status","validation_references","human_review_required","limitations")
SCENARIOS={"batlow":{"name":"Batlow","meteorology_ids":["batlow"]},"kunlun":{"name":"Kunlun","meteorology_ids":["kunlun"]},"iraq":{"name":"Iraq","meteorology_ids":["iraq"]},"baiyangdian_xiongan":{"name":"Baiyangdian-Xiong'an","meteorology_ids":["xiongan_wutai_headwaters","xiongan_baiyangdian_wetland","xiongan_downstream"]}}
SOURCE_PATHS={"meteorology_evidence":OUTPUT_DIR/"meteorology_evidence.json","meteorology_trend":OUTPUT_DIR/"meteorology_trends.json","spatial_transect":OUTPUT_DIR/"spatial_transects.json","planning_hypothesis":OUTPUT_DIR/"planning_hypotheses.json","gis_dem_access_plan":OUTPUT_DIR/"gis_dem_access_plan.json","professional_validation_interface":OUTPUT_DIR/"professional_validation_interface.json","expert_review_record":OUTPUT_DIR/"expert_review_records.json","planning_approval_support_report":OUTPUT_DIR/"planning_approval_support_report.json"}

def _load(path):
    if not path.exists() or not path.read_text(encoding="utf-8").strip(): return None
    return json.loads(path.read_text(encoding="utf-8"))
def _ref(path,obj): return f"cczps_lite/output/{path.name}#{obj}"
def _record(scenario,kind,artifact,summary,ids,source,evidence_type,strength,confidence,status,validations,limits):
    return {"trace_id":f"{scenario}:{kind}:{artifact}","scenario_id":scenario,"artifact_type":kind,"artifact_id":artifact,"claim_or_output_summary":summary,"supporting_evidence_ids":ids,"evidence_source":source,"evidence_type":evidence_type,"evidence_strength":strength,"confidence":confidence,"review_status":status,"validation_references":validations,"human_review_required":True,"limitations":limits}
def _missing(scenario,kind,path):
    return _record(scenario,kind,f"{scenario}_{kind}_missing",f"No local {kind.replace('_',' ')} record was available.",[],f"cczps_lite/output/{path.name}","missing_local_artifact","insufficient_evidence","not_assessed","not_reviewed",[],["Source artifact or scenario record is missing; no claim can be traced."])
def _items(source,key): return (source or {}).get(key,{})

def _meteorology(scenario,config,source):
    path=SOURCE_PATHS["meteorology_evidence"]; found=[_items(source,"scenarios")[key] for key in config["meteorology_ids"] if key in _items(source,"scenarios")]
    if not found: return _missing(scenario,"meteorology_evidence",path)
    statuses=sorted({x.get("retrieval_status","unknown") for x in found}); strengths=sorted({x.get("evidence",{}).get("strength","insufficient_evidence") for x in found}); confidence=sorted({x.get("confidence","not_assessed") for x in found})
    return _record(scenario,"meteorology_evidence",f"{scenario}_meteorology_evidence",f"Local meteorology observations have retrieval status: {', '.join(statuses)}.",[f"{x.get('scenario_id')}:{x.get('observation_date')}" for x in found],_ref(path,",".join(config["meteorology_ids"])),"observational_meteorology",strengths[0] if len(strengths)==1 else "mixed",confidence[0] if len(confidence)==1 else "mixed","supporting_evidence_only",[],[(source or {}).get("decision_boundary","No source decision boundary recorded."),"Observations do not establish causation or approval readiness."])
def _trend(scenario,config,source):
    path=SOURCE_PATHS["meteorology_trend"]; found=[_items(source,"scenarios")[key] for key in config["meteorology_ids"] if key in _items(source,"scenarios")]
    if not found: return _missing(scenario,"meteorology_trend",path)
    statuses=sorted({x.get("trend_status","insufficient_data") for x in found}); strength="supporting_evidence" if statuses==["sufficient_observations"] else "insufficient_evidence"
    return _record(scenario,"meteorology_trend",f"{scenario}_meteorology_trend",f"Local trend records report: {', '.join(statuses)}.",[f"{x.get('scenario_id')}:trend" for x in found],_ref(path,",".join(config["meteorology_ids"])),"deterministic_trend_reading",strength,"not_assessed","supporting_evidence_only",[],[(source or {}).get("decision_boundary","No source decision boundary recorded."),"Trend classifications are not forecasts, conclusions, or recommendations."])
def _spatial(scenario,source):
    path=SOURCE_PATHS["spatial_transect"]; item=next((x for x in (source or {}).get("spatial_transects",[]) if x.get("scenario_id")==scenario),None)
    if not item: return _missing(scenario,"spatial_transect",path)
    status=item.get("validation",{}).get("status","not_assessed"); artifact=item.get("transect_id",f"{scenario}_transect")
    return _record(scenario,"spatial_transect",artifact,f"Configured spatial transect status is {status}.",[artifact],_ref(path,artifact),"configured_spatial_relationship","configured_evidence" if status=="valid_configured" else "insufficient_evidence","not_assessed",status,[],[(source or {}).get("safety_boundary","No source safety boundary recorded."),"Configured relationships are not GIS-derived or field-validated."])
def _hypothesis(scenario,source):
    path=SOURCE_PATHS["planning_hypothesis"]; item=(source or {}).get("hypotheses",{}).get(scenario)
    if not item: return _missing(scenario,"planning_hypothesis",path)
    artifact=item["hypothesis_id"]; context=item.get("evidence_context",{})
    return _record(scenario,"planning_hypothesis",artifact,item.get("hypothesis_summary",item.get("planning_assumption","")),[f"{scenario}:meteorology_trend",f"{scenario}:spatial_transect",*[f"{scenario}:scenario:{x}" for x in item.get("scenario_ids",[])]],_ref(path,artifact),"testable_planning_hypothesis",item.get("hypothesis_status","insufficient_evidence"),"not_assessed",item.get("hypothesis_status","requires_validation"),[str(x) for x in context.get("validation_statuses",[])],[*item.get("failure_conditions",[]),(source or {}).get("safety_boundary","No source safety boundary recorded.")])
def _gis(scenario,source):
    path=SOURCE_PATHS["gis_dem_access_plan"]
    if not source: return _missing(scenario,"gis_dem_access_plan",path)
    return _record(scenario,"gis_dem_access_plan","gis_dem_access_plan",f"GIS/DEM integration status is {source.get('implementation_status','planning_only')}.",[x["category"] for x in source.get("spatial_data_categories",[])],_ref(path,"gis_dem_access_plan"),"spatial_data_access_plan","insufficient_evidence","not_assessed","planning_only",[],[source.get("safety_boundary","No source safety boundary recorded."),"No GIS/DEM data has been acquired or processed."])
def _validation(scenario,source):
    path=SOURCE_PATHS["professional_validation_interface"]; item=(source or {}).get("reviews",{}).get(scenario)
    if not item: return _missing(scenario,"professional_validation_interface",path)
    return _record(scenario,"professional_validation_interface",f"{scenario}_professional_validation",f"Professional validation status is {item.get('review_status')}.",[item.get("hypothesis_id")],_ref(path,scenario),"professional_review_template","insufficient_evidence","not_assessed",item.get("review_status","awaiting_professional_review"),list(item.get("review_categories",{})),[(source or {}).get("safety_boundary","No source safety boundary recorded."),"Blank review fields are not professional findings."])
def _expert(scenario,config,source):
    path=SOURCE_PATHS["expert_review_record"]; item=next((x for x in (source or {}).get("records",[]) if x.get("reviewed_scenario_or_module")==config["name"]),None)
    if not item: return _missing(scenario,"expert_review_record",path)
    artifact=item["record_id"]
    return _record(scenario,"expert_review_record",artifact,f"Expert review record status is {item.get('decision_status','not_reviewed')}.",list(item.get("evidence_reference",[])),_ref(path,artifact),"expert_review_template","insufficient_evidence",item.get("confidence_level","not_assessed"),item.get("decision_status","not_reviewed"),[],[(source or {}).get("safety_boundary","No source safety boundary recorded."),"Template records are not completed expert opinions."])
def _approval(scenario,config,source):
    path=SOURCE_PATHS["planning_approval_support_report"]; item=next((x for x in (source or {}).get("scenarios",[]) if x.get("scenario")==config["name"]),None)
    if not item: return _missing(scenario,"planning_approval_support_report",path)
    return _record(scenario,"planning_approval_support_report",f"{scenario}_planning_approval_support",f"Approval support status remains {item.get('approval_support_status')}.",[f"{scenario}:planning_hypothesis",f"{scenario}:professional_validation",f"{scenario}:expert_review","gis_dem_access_plan"],_ref(path,scenario),"planning_approval_support_summary",item.get("evidence_strength","insufficient_evidence"),"not_assessed",item.get("approval_support_status","not_ready_for_approval"),[item.get("validation_status","awaiting_professional_review"),item.get("expert_review_outcome","not_reviewed")],[item.get("human_approval_boundary",""),*item.get("unresolved_risks",[]),(source or {}).get("safety_boundary","No source safety boundary recorded.")])

def build_evidence_traceability(sources=None):
    loaded=sources if sources is not None else {key:_load(path) for key,path in SOURCE_PATHS.items()}; records=[]
    for scenario,config in SCENARIOS.items():
        records += [_meteorology(scenario,config,loaded.get("meteorology_evidence")),_trend(scenario,config,loaded.get("meteorology_trend")),_spatial(scenario,loaded.get("spatial_transect")),_hypothesis(scenario,loaded.get("planning_hypothesis")),_gis(scenario,loaded.get("gis_dem_access_plan")),_validation(scenario,loaded.get("professional_validation_interface")),_expert(scenario,config,loaded.get("expert_review_record")),_approval(scenario,config,loaded.get("planning_approval_support_report"))]
    return {"schema_version":SCHEMA_VERSION,"runtime":"Evidence Traceability Layer","safety_boundary":SAFETY_BOUNDARY,"record_count":len(records),"required_fields":list(REQUIRED_FIELDS),"records":records}
def render_markdown_report(output):
    lines=["# Evidence Traceability Layer","",output["safety_boundary"],"",f"Trace records: {output['record_count']}",""]
    for scenario in SCENARIOS:
        lines += [f"## {SCENARIOS[scenario]['name']}",""]
        for record in (x for x in output["records"] if x["scenario_id"]==scenario):
            lines += [f"### {record['artifact_type'].replace('_',' ').title()}","",f"- Trace ID: `{record['trace_id']}`",f"- Artifact ID: `{record['artifact_id']}`",f"- Summary: {record['claim_or_output_summary']}",f"- Evidence source: `{record['evidence_source']}`",f"- Evidence strength: `{record['evidence_strength']}`",f"- Confidence: `{record['confidence']}`",f"- Review status: `{record['review_status']}`",f"- Human review required: `{record['human_review_required']}`",f"- Supporting evidence IDs: {', '.join(record['supporting_evidence_ids']) or 'None recorded'}",f"- Validation references: {', '.join(record['validation_references']) or 'None recorded'}","","Limitations:","",*[f"- {x}" for x in record["limitations"] if x],""]
    return "\n".join(lines).rstrip()+"\n"
def write_evidence_traceability_outputs(output,output_path=OUTPUT_PATH,report_path=REPORT_PATH):
    output_path.parent.mkdir(parents=True,exist_ok=True); output_path.write_text(json.dumps(output,indent=2,ensure_ascii=True)+"\n",encoding="utf-8"); report_path.write_text(render_markdown_report(output),encoding="utf-8")
def main():
    output=build_evidence_traceability(); write_evidence_traceability_outputs(output); print(f"Wrote evidence traceability outputs to {OUTPUT_DIR}")
if __name__=="__main__": main()
