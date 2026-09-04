"""Request-driven, evidence-bounded Cooma Site Reading v0.1 R1."""
from __future__ import annotations
import hashlib, json
from datetime import UTC, datetime
from pathlib import Path, PurePosixPath
from typing import Any

SKILL_ID, SKILL_VERSION = "EP-SKILL-001", "0.1-r1"
REQUEST_SCHEMA_ID = "climateos.site_reading_request.v0.1"
TBEA_SCHEMA_ID = "climateos.time_bounded_environmental_answer.v0.1"
PASSPORT_SCHEMA_ID = "climateos.environmental_evidence_passport.v0.1"
REAL_SCHEMA_ID = "climateos.cooma_official_real_data_public_receipt.v0.1"
HYDRO_SCHEMA_ID = "climateos.waternsw_near_current_admission.v0.1"
HIST_RUN_SCHEMA_ID = "climateos.mittagang_410033_historical_characterisation.v0.1"
REQUIRED_REQUEST_FIELDS = {"request_id","revision_id","parent_revision","place","environmental_question","decision_use","evidence_object_ids","spatial_context_ids","temporal_context","known_constraints","requested_at","maximum_intervention_class"}
EXPECTED_SOURCES = {
 "COOMA-BOM-DWO-2026-07": ("OFFICIAL_OBSERVATION","Australian Bureau of Meteorology","IDCJDW2033.202607"),
 "BOM-ENSO-MONITORING-2026-07-14": ("OFFICIAL_OUTLOOK","Australian Bureau of Meteorology",None),
}
SPATIAL_CONTEXT = {
 "COOMA-LOCALITY":{"class":"LOCALITY_BOUNDARY","reference":"docs/tasks/task2031_2040_qgis_cooma_terrain_boundary_pack/QGIS_COOMA_TERRAIN_REVIEW_GUIDE.md","boundary":"Official NSW Cooma locality; not an LGA, catchment, hydrological boundary or final scientific study boundary."},
 "COOMA-TERRAIN-DEM":{"class":"TERRAIN_DEM","reference":"docs/tasks/task2031_2040_qgis_cooma_terrain_boundary_pack/TASK2031_2040_QGIS_COOMA_TERRAIN_BOUNDARY_PACK_REPORT.md","boundary":"Bounded GA SRTM DEM and derived terrain context within the locality plus 10 km orientation extent."},
 "COOMA-WATERCOURSES":{"class":"HYDROLOGY_WATERCOURSE","reference":"docs/tasks/task2041_2050_qgis_cooma_hydrology_pack/TASK2041_2050_QGIS_COOMA_HYDROLOGY_PACK_REPORT.md","boundary":"Official main-watercourse spatial context; presence is not flow, quality or condition."},
 "COOMA-CATCHMENTS":{"class":"CATCHMENT_CONTEXT","reference":"docs/tasks/task2041_2050_qgis_cooma_hydrology_pack/TASK2041_2050_QGIS_COOMA_HYDROLOGY_PACK_REPORT.md","boundary":"Contracted and stream-segment catchment context; none is identified as a drinking-water supply catchment."},
 "COOMA-ROADS-SETTLEMENT":{"class":"ROADS_SETTLEMENT","reference":"docs/tasks/task2051_2060_qgis_cooma_integrated_experience/TASK2051_2060_QGIS_COOMA_INTEGRATED_EXPERIENCE_REPORT.md","boundary":"Official roads and locality context bounded to the Cooma plus 10 km orientation extent."},
}
class SiteReadingError(ValueError): pass
def _digest(v:Any)->str: return "sha256:"+hashlib.sha256(json.dumps(v,sort_keys=True,separators=(",",":"),ensure_ascii=False).encode()).hexdigest()
def _posix(path:Path,root:Path)->str: return PurePosixPath(path.relative_to(root)).as_posix()

def validate_request(r:dict[str,Any])->None:
 missing=sorted(REQUIRED_REQUEST_FIELDS-r.keys())
 if r.get("schema_id")!=REQUEST_SCHEMA_ID or missing: raise SiteReadingError(f"Invalid SiteReadingRequest; missing={missing}")
 for f in ("request_id","revision_id","place","environmental_question","decision_use","requested_at"):
  if not r.get(f): raise SiteReadingError(f"SiteReadingRequest {f} is required")
 for f in ("evidence_object_ids","spatial_context_ids","known_constraints"):
  if not isinstance(r.get(f),list): raise SiteReadingError(f"SiteReadingRequest {f} must be an array")
 if not isinstance(r.get("temporal_context"),dict) or not {"assessment_period","valid_until"}<=r["temporal_context"].keys(): raise SiteReadingError("Temporal context is incomplete")
 if r["maximum_intervention_class"]!="A0": raise SiteReadingError("EP-SKILL-001 R1 permits A0 only")
 if set(r["spatial_context_ids"])-SPATIAL_CONTEXT.keys(): raise SiteReadingError("Unknown spatial context ID")

def resolve_sources(receipt:dict[str,Any])->dict[str,dict[str,Any]]:
 if receipt.get("schema_id")!=REAL_SCHEMA_ID or receipt.get("environmental_conclusion") is not None: raise SiteReadingError("Invalid bounded Cooma public receipt")
 out={}
 for s in receipt.get("sources",[]):
  sid=s.get("source_id")
  if sid not in EXPECTED_SOURCES or sid in out: raise SiteReadingError("Missing, duplicate or unexpected source identity")
  ec,pub,product=EXPECTED_SOURCES[sid]
  if s.get("evidence_class")!=ec or s.get("publisher")!=pub: raise SiteReadingError("Source class or publisher mismatch")
  if product and s.get("parsed_metadata",{}).get("product_id")!=product: raise SiteReadingError("Product identity mismatch")
  out[sid]=s
 if set(out)!=set(EXPECTED_SOURCES): raise SiteReadingError("Missing expected source identity")
 return out

def validate_inputs(req,real,hydro,ha,hp,hr):
 validate_request(req); sources=resolve_sources(real)
 if hydro.get("schema_id")!=HYDRO_SCHEMA_ID or hydro.get("admission_status")!="ADMISSION_BLOCKED_MISSING_RAW_RESPONSE" or hydro.get("environmental_conclusion") is not None: raise SiteReadingError("Expected blocked WaterNSW receipt is required")
 if ha.get("schema_id")!=TBEA_SCHEMA_ID or ha.get("evidence_cutoff")!="2024-02-29" or (ha.get("evidence_maturity"),ha.get("conclusion_level"))!=("S0","L2"): raise SiteReadingError("Expected historical S0/L2 Time-Bounded Answer is required")
 if hp.get("schema_id")!=PASSPORT_SCHEMA_ID or hp.get("derived_claim",{}).get("answer_id")!=ha.get("answer_id"): raise SiteReadingError("Historical Environmental Evidence Passport mismatch")
 if hr.get("schema_id")!=HIST_RUN_SCHEMA_ID or hr.get("run_id")!=hp.get("method",{}).get("run_id"): raise SiteReadingError("Historical Run Receipt mismatch")
 ids={real["pilot_id"],hydro["run_id"],ha["answer_id"],hp["passport_id"],hr["run_id"]}
 if not ids<=set(req["evidence_object_ids"]): raise SiteReadingError("Request does not bind every required evidence object")
 return sources

def build_outputs(req,real,hydro,ha,hp,hr,*,issued_at):
 src=validate_inputs(req,real,hydro,ha,hp,hr); weather=src["COOMA-BOM-DWO-2026-07"]
 spatial=[{"spatial_context_id":sid,**SPATIAL_CONTEXT[sid]} for sid in req["spatial_context_ids"]]
 env={"skill_id":SKILL_ID,"skill_version":SKILL_VERSION,"request_id":req["request_id"],"revision_id":req["revision_id"],"parent_revision":req["parent_revision"],"issued_at":issued_at,"evidence_cutoff":"2026-07-27","valid_until":req["temporal_context"]["valid_until"],"maximum_intervention_class":"A0"}
 claims=[
  {"reasoning_type":"KNOWN_FROM_ADMITTED_EVIDENCE","statement":f"The admitted BoM product records {weather['parsed_metadata']['row_count']} dated rows covering {weather['parsed_metadata']['coverage_start']} to {weather['parsed_metadata']['coverage_end']}.","evidence_ids":[weather["source_id"]]},
  {"reasoning_type":"KNOWN_FROM_ADMITTED_EVIDENCE","statement":f"The admitted Mittagang 410033 historical answer covers {ha['assessment_period']} at S0/L2 with cutoff {ha['evidence_cutoff']}.","evidence_ids":[ha["answer_id"],hp["passport_id"],hr["run_id"]]},
  {"reasoning_type":"DERIVED","method":"Cross-object boundary check without calculating a flow comparison","statement":"Historical L2 context exists, but the missing exact near-current response prevents a current comparison.","evidence_ids":[ha["answer_id"],hydro["run_id"]]},
  {"reasoning_type":"INFERRED","assumptions":["Spatial layers are orientation context only","No station-to-locality representativeness is assumed"],"statement":"Spatial references help scope later evidence requests but do not establish environmental condition.","evidence_ids":req["spatial_context_ids"]},
  {"reasoning_type":"UNKNOWN","statement":"Current Mittagang flow and current Cooma catchment condition are unknown."},
  {"reasoning_type":"MISSING_EVIDENCE","statement":"Exact near-current WaterNSW response bytes and qualified hydrology review are missing."},
  {"reasoning_type":"PROHIBITED_CONCLUSION","statement":"No current flow, trend, water security, water quality, causation, planning approval, engineering, regulatory or public-warning conclusion is permitted."},]
 pc01={**env,"schema_id":"climateos.planner.pc01.site_observation.v0.1","object_id":f"PC01-{req['revision_id']}","state":"EVIDENCE_REQUIRED","observation_status":"NONE_ADMITTED_FOR_THIS_READING","observation_method":None,"geometry":None,"observed_at":None,"limitations":["No direct human/instrument observation with time, method and geometry was admitted"]}
 pc02={**env,"schema_id":"climateos.planner.pc02.evidence_request.v0.1","object_id":f"PC02-{req['revision_id']}","state":"OPEN","question_served":req["environmental_question"],"requested_objects":["Exact WaterNSW 410033 near-current response and receipt","Qualified hydrology review","Admitted local ecological/soil/land-cover observations"],"acceptable_source_class":"AUTHORITATIVE_AND_LAWFULLY_ADMITTED","network_limit":"SEPARATE_AUTHORIZATION_REQUIRED","cost_limit_aud":0,"fulfilment_test":"Identity, provenance, temporal/spatial fitness and review gates pass"}
 pc03={**env,"schema_id":"climateos.planner.pc03.professional_review_gate_reference.v0.1","object_id":f"PC03-{req['revision_id']}","state":"PENDING","domain":"HYDROLOGY","reference":"PR #115 / H1-H8 professional review card","evidence_version":hp["passport_id"],"review_questions":ha["human_review"]["review_questions"],"signature":None,"professional_signoff_simulated":False}
 pc04={**env,"schema_id":"climateos.planner.pc04.environmental_state.v0.1","object_id":f"PC04-{req['revision_id']}","state":"UNKNOWN","state_variable":"CURRENT_COOMA_AND_MITTAGANG_HYDROLOGICAL_CONDITION","assertion_class":"UNKNOWN","value":None,"supporting_evidence":[ha["answer_id"]],"blocked_evidence":[hydro["run_id"]],"derivation":"No current-state derivation performed","confidence_basis":"Historical baseline reproducible; current evidence blocked"}
 pc13={**env,"schema_id":"climateos.planner.pc13.action_passport.v0.1","action_passport_id":f"PC13-{req['revision_id']}","status":"READY_FOR_HUMAN_REVIEW","question":req["environmental_question"],"environmental_state_ids":[pc04["object_id"]],"permissible_claims":["Historical S0/L2 context exists","Current comparison remains blocked"],"recommended_consideration":"Preserve records, request missing evidence and prepare qualified review","permitted_a0_actions":["MONITORING_PREPARATION","EVIDENCE_REQUEST","RECORD_PRESERVATION","REVIEW_PREPARATION"],"prohibited_actions":["A1_OR_HIGHER","ENGINEERING","REGULATORY","PROCUREMENT","PUBLIC_WARNING"],"authority":{"accountable_human_role":"Founder or authorised reviewer","maximum_intervention_class":"A0"},"professional_review_gates":[pc03["object_id"]]}
 answer={"schema_id":TBEA_SCHEMA_ID,"answer_id":f"TBEA-{req['revision_id']}","question":req["environmental_question"],"decision_use":req["decision_use"],"place":req["place"],"spatial_boundary":"Cooma locality and +10 km orientation context; Mittagang gauge 410033 remains station-bounded; no catchment-wide inference","assessment_period":req["temporal_context"]["assessment_period"],"evidence_cutoff":env["evidence_cutoff"],"issued_at":issued_at,"valid_until":env["valid_until"],"conclusion_level":"L2","evidence_maturity":"S0","answer":"Admitted official and spatial context supports a bounded Site Reading and historical Mittagang L2 baseline. No direct site observation is admitted; current hydrology, comparison and trend remain blocked/deferred.","confidence":"High for identity and historical provenance; none for current condition because near-current raw evidence and professional review are absent.","supporting_evidence":[real["pilot_id"],ha["answer_id"],hp["passport_id"],hr["run_id"],*req["spatial_context_ids"]],"conflicting_evidence":["All-published and A+B historical summaries differ; sensitivity is preserved","ADMISSION_BLOCKED_MISSING_RAW_RESPONSE","NOT_COMPARABLE_YET","TREND_DEFERRED"],"missing_critical_evidence":[c["statement"] for c in claims if c["reasoning_type"] in {"UNKNOWN","MISSING_EVIDENCE"}],"local_translation_path":["official evidence","bounded spatial context","historical L2 baseline","current evidence gate","human review"],"alternative_explanations":ha["alternative_explanations"],"consequence_if_true":"A reusable bounded evidence request and review package is available.","consequence_if_false":"Demote and preserve this revision; correct inputs or method in a new revision.","intervention_window":"A0 evidence, monitoring preparation, record preservation and review preparation only.","permitted_actions":pc13["permitted_a0_actions"],"prohibited_actions":pc13["prohibited_actions"],"update_triggers":["new admitted evidence","source or method version change","spatial context revision","professional review finding"],"demotion_triggers":["source identity/provenance failure","calculation or contract error","evidence expiry","material professional-review defect"],"stop_conditions":["attempted A1+ use","attempted current flow/trend claim","unresolved identity mismatch","attempted engineering/regulatory/procurement/public-warning use"],"human_review":{"status":"PENDING_HUMAN_REVIEW","professional_gate_id":pc03["object_id"],"professional_signoff_simulated":False},"official_confirmation":{"scope":"Source identity and admitted facts only","relationship_to_answer":"Does not confirm local current condition or Site Reading interpretation"},"retrospective_validation":{"status":"PLANNED","plan":"On trigger, rerun with immutable prior revision retained; compare digests, explain changes and obtain review."}}
 passport={"schema_id":PASSPORT_SCHEMA_ID,"passport_id":f"EEP-{req['revision_id']}","subject":"Cooma bounded Site Reading","source_identity":{"request_id":req["request_id"],"evidence_object_ids":req["evidence_object_ids"],"input_digests":[_digest(x) for x in (real,hydro,ha,hp,hr)]},"method":{"skill_id":SKILL_ID,"version":SKILL_VERSION,"revision_id":req["revision_id"],"parent_revision":req["parent_revision"],"method":"Validated resolution and boundary-preserving synthesis; no new environmental calculation"},"derived_claim":{"answer_id":answer["answer_id"],"conclusion_level":"L2","evidence_maturity":"S0","evidence_cutoff":answer["evidence_cutoff"]},"limitations":{"missing_critical_evidence":answer["missing_critical_evidence"],"prohibited_actions":answer["prohibited_actions"],"trend_status":"TREND_DEFERRED"},"review":answer["human_review"],"retrospective_validation":answer["retrospective_validation"]}
 reading={**env,"schema_id":"climateos.cooma_site_reading.v0.1-r1","reading_id":f"SITE-READING-{req['revision_id']}","place":req["place"],"question":req["environmental_question"],"decision_use":req["decision_use"],"direct_observation_status":"NONE_ADMITTED_FOR_THIS_READING","spatial_context":spatial,"spatial_context_warning":"Spatial presence does not itself establish environmental condition.","claims":claims,"historical_hydrology":{"answer_id":ha["answer_id"],"passport_id":hp["passport_id"],"run_id":hr["run_id"],"evidence_cutoff":"2024-02-29","maturity":"S0","conclusion_level":"L2","answer":ha["answer"]},"current_hydrology":{"admission_status":"ADMISSION_BLOCKED_MISSING_RAW_RESPONSE","comparison_status":"NOT_COMPARABLE_YET","trend_status":"TREND_DEFERRED","current_flow":None},"contracts":{"PC-01":pc01,"PC-02":pc02,"PC-03":pc03,"PC-04":pc04,"PC-13":pc13},"time_bounded_answer_id":answer["answer_id"],"evidence_passport_id":passport["passport_id"],"review_state":"PENDING_HUMAN_REVIEW"}
 reading["content_digest"]=_digest(reading)
 return {"reading":reading,"answer":answer,"passport":passport,"action_passport":pc13,"contracts":{"pc01":pc01,"pc02":pc02,"pc03":pc03,"pc04":pc04}}

def render_founder(o,receipt_name):
 r,a,ap=o["reading"],o["answer"],o["action_passport"]
 known="\n".join(f"- **{c['reasoning_type']}** — {c['statement']}" for c in r["claims"]); spatial="\n".join(f"- **{x['class']}** (`{x['spatial_context_id']}`): {x['boundary']}" for x in r["spatial_context"])
 nxt="\n".join(f"- {x}" for x in o["contracts"]["pc02"]["requested_objects"])
 known_by={c["reasoning_type"]:c["statement"] for c in r["claims"]}
 admitted="\n".join(f"- {c['statement']}" for c in r["claims"] if c["reasoning_type"]=="KNOWN_FROM_ADMITTED_EVIDENCE")
 return f"""# Cooma Site Reading v0.1 - R1

## 1. Question asked
{r['question']}
Decision use: {r['decision_use']}

## 2. Place and spatial boundary
{r['place']}. {a['spatial_boundary']}

{spatial}

**Boundary:** {r['spatial_context_warning']}

## 3. Direct observations
`OBSERVED: NONE_ADMITTED_FOR_THIS_READING`. No direct human/instrument observation with observation time, method and geometry was admitted.

## 4. Known from admitted official evidence
{admitted}

## 5. Historical hydrology at L2
The admitted Mittagang 410033 TBEA is `S0 / L2`, covers `1964-03-01/2024-02-29`, and has cutoff `2024-02-29`. It is historical only, not a current-flow statement.

## 6. Current hydrology boundary
`ADMISSION_BLOCKED_MISSING_RAW_RESPONSE`; `NOT_COMPARABLE_YET`; `TREND_DEFERRED`. No current flow value is inferred.

## 7. Derived result
{known_by['DERIVED']}

## 8. Inferred interpretation
{known_by['INFERRED']}

## 9. Unknowns
{known_by['UNKNOWN']}

## 10. Conflicting or blocked evidence
{known_by['MISSING_EVIDENCE']} Historical quality-screen sensitivity is preserved rather than averaged away.

## 11. Maturity and authority ceiling
Evidence maturity `S0`; conclusion ceiling `L2`; intervention ceiling `A0`.

## 12. Expiry and triggers
Issued: `{a['issued_at']}`. Evidence cutoff: `{a['evidence_cutoff']}`. Valid until: `{a['valid_until']}`.

- Update: {'; '.join(a['update_triggers'])}.
- Demote: {'; '.join(a['demotion_triggers'])}.
- Stop: {'; '.join(a['stop_conditions'])}.

## 13. Permitted low-regret A0 action
{ap['recommended_consideration']}. Allowed: {', '.join(ap['permitted_a0_actions'])}. Status: `{ap['status']}`.

## 14. Prohibited conclusions and actions
{'; '.join(a['prohibited_actions'])}. No engineering, regulatory, procurement or public-warning action is authorised.

## 15. Evidence to obtain next
{nxt}

## 16. Human/professional review
Founder review and PR #115 hydrology professional gate remain pending. No H1-H8 sign-off is simulated.

## 17. Audit artifacts
- Time-Bounded Answer: `time_bounded_environmental_answer.json`
- Environmental Evidence Passport: `evidence_passport.json`
- A0 Action Passport: `action_passport.json`
- Run Receipt: `{receipt_name}`
- PC-01-PC-04 contracts: `planner_contracts.json`
"""

def run(output_root,*,request_path=None,repo_root=None,issued_at=None):
 root=Path(repo_root) if repo_root else Path(__file__).resolve().parents[2]
 req_path=Path(request_path) if request_path else root/"cczps_lite/input/cooma_site_reading_request_r1.json"
 if not req_path.is_absolute(): req_path=root/req_path
 pin={"real":root/"cczps_lite/output/cooma_official_real_data_pilot_receipt.json","hydro":root/"cczps_lite/output/waternsw_near_current_evidence_admission/admission_receipt.json","answer":root/"cczps_lite/output/mittagang_410033_historical_characterisation/time_bounded_environmental_answer.json","passport":root/"cczps_lite/output/mittagang_410033_historical_characterisation/evidence_passport.json","run":root/"cczps_lite/output/mittagang_410033_historical_characterisation/run_receipt.json"}
 req=json.loads(req_path.read_text(encoding="utf-8")); d={k:json.loads(p.read_text(encoding="utf-8")) for k,p in pin.items()}; stamp=issued_at or datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00","Z"); o=build_outputs(req,d["real"],d["hydro"],d["answer"],d["passport"],d["run"],issued_at=stamp)
 rev=Path(output_root)/"runs"/req["revision_id"]
 if rev.exists(): raise SiteReadingError(f"Immutable revision already exists: {req['revision_id']}")
 rev.mkdir(parents=True); names={"reading":"site_reading.json","answer":"time_bounded_environmental_answer.json","passport":"evidence_passport.json","action_passport":"action_passport.json","contracts":"planner_contracts.json"}; result={}
 for k,n in names.items():
  p=rev/n; p.write_text(json.dumps(o[k],indent=2,ensure_ascii=False)+"\n",encoding="utf-8"); result[k]=p
 rec={"schema_id":"climateos.cooma_site_reading.run_receipt.v0.1-r1","skill_id":SKILL_ID,"skill_version":SKILL_VERSION,"request_id":req["request_id"],"revision_id":req["revision_id"],"parent_revision":req["parent_revision"],"issued_at":stamp,"network_used":False,"inputs":[_posix(req_path,root),*[_posix(p,root) for p in pin.values()]],"outputs":{k:PurePosixPath(*p.parts[-4:]).as_posix() for k,p in result.items()},"reading_digest":o["reading"]["content_digest"],"result":"BOUNDED_SITE_READING_PRODUCED","limitations":["ADMISSION_BLOCKED_MISSING_RAW_RESPONSE","NOT_COMPARABLE_YET","TREND_DEFERRED"]}
 rp=rev/"run_receipt.json"; rp.write_text(json.dumps(rec,indent=2,ensure_ascii=False)+"\n",encoding="utf-8"); result["receipt"]=rp
 md=rev/"FOUNDER_SITE_READING.md"; md.write_text(render_founder(o,rp.name),encoding="utf-8"); result["markdown"]=md
 return result
