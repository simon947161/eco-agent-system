"""Deterministic, offline EP-SKILL-002 Cooma Evidence Watch v0.1."""
from __future__ import annotations
import hashlib, json, tempfile
from pathlib import Path, PurePosixPath

SKILL_ID, VERSION = "EP-SKILL-002", "0.1"
REVISION = "SRQ-COOMA-001-R2-20260905"
PARENT = "SRQ-COOMA-001-R1-20260904"
ROOT_NAME = "cczps_lite/output/cooma_evidence_watch_v0_1"

class EvidenceWatchError(ValueError): pass
def digest(value): return "sha256:"+hashlib.sha256(json.dumps(value,sort_keys=True,separators=(",",":"),ensure_ascii=False).encode()).hexdigest()
def load(path): return json.loads(path.read_text(encoding="utf-8"))
def posix(path,root): return PurePosixPath(path.relative_to(root)).as_posix()

def record(source_id, role, availability, admission, temporal, relation, *, observed_at=None, retrieved_at=None, admitted_at=None, fresh_until=None, policy, basis, spatial, temporal_fit, question_fit, lineage, group, limitations=()):
 return {"schema_id":"climateos.evidence_freshness_record.v0.1","source_object_id":source_id,"source_identity":source_id,"evidence_role":role,"availability_state":availability,"admission_state":admission,"temporal_state":temporal,"evidence_relation":relation,"observed_at":observed_at,"observed_at_null_reason":None if observed_at else "No single observation time applies to this evidence role","retrieved_at":retrieved_at,"retrieved_at_null_reason":None if retrieved_at else "No admitted retrieval receipt exists","admitted_at":admitted_at,"admitted_at_null_reason":None if admitted_at else "Evidence is not admitted","evidence_cutoff":"2026-07-27","fresh_until":fresh_until,"freshness_policy_id":policy,"freshness_basis":basis,"expiry_reason":None if temporal not in {"STALE","EXPIRED"} else basis,"update_trigger":"New separately authorised and admitted evidence or source/method revision","spatial_fitness":spatial,"temporal_fitness":temporal_fit,"question_fitness":question_fit,"source_lineage":lineage,"independence_group":group,"review_state":"PENDING_HUMAN_REVIEW","limitations":list(limitations)}

def build(request, prior, public, hydro, historical):
 if request.get("revision_id")!=REVISION or request.get("parent_revision")!=PARENT: raise EvidenceWatchError("R2 immutable lineage mismatch")
 if request.get("network_authorised") is not False or request.get("maximum_intervention_class")!="A0": raise EvidenceWatchError("Option B must remain offline and A0")
 if prior.get("revision_id")!=PARENT: raise EvidenceWatchError("Prior EP-SKILL-001 revision missing")
 if hydro.get("admission_status")!="ADMISSION_BLOCKED_MISSING_RAW_RESPONSE": raise EvidenceWatchError("WaterNSW block must be preserved")
 retrieved=public["retrieved_at"]
 freshness=[
  record("COOMA-BOM-DWO-2026-07","CURRENT_OBSERVATION","AVAILABLE","ADMITTED","STALE","SUPPORTING",observed_at="2026-07-27",retrieved_at=retrieved,admitted_at=retrieved,fresh_until="2026-07-28T23:59:59Z",policy="FIXTURE-DAILY-CURRENT-USE-V0.1",basis="Fixed fixture policy: daily observations are stale for present-condition use after the next completed day; operational values require domain review",spatial="LOCAL_WEATHER_CONTEXT_ONLY",temporal_fit="STALE_FOR_CURRENT_CONDITION",question_fit="HISTORICAL_CONTEXT_ONLY",lineage="BoM DWO IDCJDW2033; stations 070278/070217",group="BOM_OBSERVATION_LINEAGE"),
  record("BOM-ENSO-MONITORING-2026-07-14","LARGE_SCALE_CONTEXT","AVAILABLE","ADMITTED","STALE","CONTEXT_ONLY",observed_at="2026-07-14",retrieved_at=retrieved,admitted_at=retrieved,fresh_until="2026-08-14T23:59:59Z",policy="FIXTURE-OUTLOOK-CONTEXT-V0.1",basis="Fixed fixture review interval only; not a scientific universal freshness window",spatial="LARGE_SCALE_NOT_LOCAL",temporal_fit="STALE_CONTEXT",question_fit="CONTEXT_ONLY_NO_LOCAL_IMPACT",lineage="BoM ENSO monitoring archive",group="BOM_OUTLOOK_LINEAGE"),
  record("MITTAGANG-410033-HISTORICAL-ANSWER-V0.1","HISTORICAL_BASELINE","AVAILABLE","ADMITTED","NOT_APPLICABLE_HISTORICAL_BASELINE","SUPPORTING",observed_at="1964-03-01/2024-02-29",retrieved_at="2026-07-30T12:30:00Z",admitted_at="2026-07-30T12:30:00Z",policy="SOURCE-DIGEST-AND-METHOD-V0.1",basis="Historical validity depends on source digest, station identity, quality definitions and method, not age",spatial="STATION_410033_ONLY",temporal_fit="VALID_FOR_DECLARED_HISTORICAL_USE",question_fit="HISTORICAL_BASELINE_ONLY",lineage=historical["source_identity"]["content_digest"],group="BOM_HRS_410033_LINEAGE"),
  record("WATERNSW-410033-NEAR-CURRENT-ADMISSION-V0.1","MISSING_REQUIRED_LINE","ACCESS_BLOCKED","ADMISSION_BLOCKED","NOT_EVALUATED","MISSING_FOR_QUESTION",policy="NO_RAW_RESPONSE_NO_ADMISSION-V0.1",basis="Exact response bytes and retrieval receipt are absent",spatial="STATION_ID_ONLY",temporal_fit="UNKNOWN",question_fit="REQUIRED_FOR_CURRENT_COMPARISON",lineage="WaterNSW candidate path; measurement lineage unresolved",group="WATERNSW_410033_CANDIDATE",limitations=("ADMISSION_BLOCKED_MISSING_RAW_RESPONSE","No credential read")),
 ]
 for sid in ("COOMA-LOCALITY","COOMA-TERRAIN-DEM","COOMA-WATERCOURSES","COOMA-CATCHMENTS","COOMA-ROADS-SETTLEMENT"):
  freshness.append(record(sid,"SPATIAL_CONTEXT","AVAILABLE","ADMITTED","NOT_EVALUATED","CONTEXT_ONLY",admitted_at="2026-09-04T02:00:00Z",policy="SPATIAL-VERSION-IDENTITY-V0.1",basis="Spatial context validity follows source version, identity, CRS, extent and transformation digest",spatial="ACCEPTED_ORIENTATION_CONTEXT",temporal_fit="NOT_AN_ENVIRONMENTAL_TIME_SIGNAL",question_fit="CONTEXT_ONLY",lineage="Accepted QGIS spatial reference",group="QGIS_SPATIAL_CONTEXT",limitations=("Spatial presence is not environmental condition",)))
 matrix={"schema_id":"climateos.evidence_convergence_matrix.v0.1","matrix_id":f"ECM-{REVISION}","question":request["environmental_question"],"signal_or_state":"CURRENT_COOMA_HYDROLOGICAL_CONDITION_UNKNOWN","supporting_lines":["MITTAGANG-410033-HISTORICAL-ANSWER-V0.1"],"conflicting_lines":["Historical all-published and A+B summaries differ; sensitivity remains visible"],"context_only_lines":["BOM-ENSO-MONITORING-2026-07-14","COOMA-LOCALITY","COOMA-TERRAIN-DEM","COOMA-WATERCOURSES","COOMA-CATCHMENTS","COOMA-ROADS-SETTLEMENT"],"blocked_lines":["WATERNSW-410033-NEAR-CURRENT-ADMISSION-V0.1"],"missing_required_lines":["ADMITTED_EQUIVALENT_NEAR_CURRENT_FLOW","QUALIFIED_HYDROLOGY_REVIEW","LOCAL_OBSERVATIONS"],"source_independence":"INSUFFICIENT_FOR_PROMOTION","independence_basis":"Object count is not independence; publisher, instrument, measurement and processing lineage are preserved categorically","shared_lineage":{"QGIS_CONTEXT":"five objects share a context role and are not five independent signals","BOM":"DWO, ENSO and HRS differ in product and scale but publisher count alone is not independence"},"spatial_alignment":"PARTIAL_STATION_AND_ORIENTATION_ONLY","temporal_alignment":"NOT_ALIGNED_FOR_CURRENT_COMPARISON","method_alignment":"NOT_COMPARABLE_YET","alternative_explanations":historical.get("limitations",{}).get("missing_critical_evidence",[]),"evidence_maturity_ceiling":"S0","conclusion_level_ceiling":"L2","promotion_allowed":False,"promotion_blockers":["No admitted near-current flow","Stale local weather for current use","ENSO and QGIS are context only","Qualified hydrology review pending"],"review_state":"PENDING_HUMAN_REVIEW"}
 plan=[]
 for sid,role,reason,method,state,fallback in [
  ("COOMA-BOM-DWO","CURRENT_OBSERVATION","Committed daily evidence is stale for current use","FUTURE_EXACT_BOM_HTTPS_GET","NETWORK_NOT_AUTHORISED","Prepare exact-source request"),
  ("BOM-ENSO-MONITORING","LARGE_SCALE_CONTEXT","Committed outlook is stale context","FUTURE_EXACT_BOM_HTTPS_GET","NETWORK_NOT_AUTHORISED","Retain context-only state"),
  ("WATERNSW-410033","CURRENT_OBSERVATION","Raw response and credential absent","FUTURE_SEPARATELY_AUTHORISED_API","ADMISSION_BLOCKED_MISSING_RAW_RESPONSE","Request an alternative equivalent official flow source; do not substitute silently"),
  ("LOCAL-OBSERVATIONS","CURRENT_OBSERVATION","No admitted local observation","HUMAN_EVIDENCE_REQUEST","MISSING_FOR_QUESTION","Request bounded inspection with named owner")]:
  plan.append({"source_object_id":sid,"refresh_needed":True,"reason":reason,"required_evidence_role":role,"proposed_access_method":method,"network_authorised":False,"cost_ceiling":{"currency":"AUD","amount":0},"admission_test":"Identity, provenance, digest, licence, spatial/temporal/question fitness and review gates","failure_state":state,"fallback_request":fallback,"next_review_time":request["valid_until"],"owner_role":"FOUNDER_OR_NAMED_REVIEWER"})
 answer={"schema_id":"climateos.time_bounded_environmental_answer.v0.1","answer_id":f"TBEA-{REVISION}","question":request["environmental_question"],"decision_use":request["decision_use"],"place":request["place"],"spatial_boundary":"Cooma locality +10 km orientation; gauge 410033 remains station-bounded","assessment_period":"Offline evaluation of committed evidence at fixed clock 2026-09-05T03:00:00Z","evidence_cutoff":request["evidence_cutoff"],"issued_at":request["evaluation_time"],"valid_until":request["valid_until"],"conclusion_level":"L2","evidence_maturity":"S0","answer":"The historical Mittagang L2 baseline remains valid for historical use. Committed July weather and ENSO context are stale for current-condition use; ENSO and QGIS remain context only. Current hydrology is unknown because near-current flow is not admitted.","confidence":"High for offline state classification; none for current hydrological condition","supporting_evidence":matrix["supporting_lines"],"conflicting_evidence":matrix["conflicting_lines"],"missing_critical_evidence":matrix["missing_required_lines"],"local_translation_path":["freshness records","convergence matrix","human review"],"alternative_explanations":matrix["alternative_explanations"],"consequence_if_true":"An auditable refresh plan is available without claiming a real refresh","consequence_if_false":"Demote this revision and correct inputs or policy in a new immutable revision","intervention_window":"A0 only","permitted_actions":["EVIDENCE_FRESHNESS_INSPECTION","EVIDENCE_REQUEST_PREPARATION","RECORD_PRESERVATION","MONITORING_PREPARATION","INTERNAL_WATCH_GENERATION","PROFESSIONAL_REVIEW_REQUEST"],"prohibited_actions":["A2_OR_HIGHER","PUBLIC_WARNING","CURRENT_FLOW_CLAIM","DROUGHT_DECLARATION","DRINKING_WATER_CONCLUSION","ENGINEERING","REGULATORY","PROCUREMENT","AUTONOMOUS_OPERATION","PRIVATE_COUNCIL_DATA_USE"],"update_triggers":["new separately authorised admitted evidence","source or method revision","professional review"],"demotion_triggers":["identity/provenance failure","calculation error","expiry","material review defect"],"stop_conditions":["attempted current-condition claim","network attempt","A2+ or public action"],"human_review":{"status":"PENDING_FOUNDER_REVIEW","professional_gate":"PR #115 remains parallel and non-blocking"},"official_confirmation":{"scope":"source facts only","relationship_to_answer":"No current local confirmation"},"retrospective_validation":{"status":"PLANNED","plan":"Compare immutable revisions after authorised evidence update"}}
 a1=[{"candidate":"SCHEDULE_LOW_REGRET_INSPECTION","status":"NOT_AUTHORISED","authority_required":"NAMED_HUMAN_APPROVAL_REQUIRED"},{"candidate":"INCREASE_MONITORING_FREQUENCY","status":"NOT_AUTHORISED","authority_required":"NAMED_HUMAN_APPROVAL_REQUIRED"},{"candidate":"PRESERVE_OPTIONS","status":"NOT_AUTHORISED","authority_required":"NAMED_HUMAN_APPROVAL_REQUIRED"},{"candidate":"COMMUNICATE_UNCERTAINTY_INTERNALLY","status":"NOT_AUTHORISED","authority_required":"NAMED_HUMAN_APPROVAL_REQUIRED"}]
 action={"schema_id":"climateos.planner.pc13.action_passport.v0.1","action_passport_id":f"PC13-{REVISION}","revision_id":REVISION,"parent_revision":PARENT,"maximum_intervention_class":"A0","permitted_a0_actions":answer["permitted_actions"],"a1_candidates":a1,"prohibited_actions":answer["prohibited_actions"],"status":"READY_FOR_HUMAN_REVIEW"}
 contracts={"PC-01":{"state":"NO_NEW_OBSERVATION","revision_id":REVISION,"parent_revision":PARENT},"PC-02":{"state":"OPEN","revision_id":REVISION,"parent_revision":PARENT,"requests":matrix["missing_required_lines"]},"PC-03":{"state":"PENDING","revision_id":REVISION,"parent_revision":PARENT,"reference":"PR #115 parallel human hydrology review"},"PC-04":{"state":"UNKNOWN","revision_id":REVISION,"parent_revision":PARENT,"value":None,"current_flow":None},"PC-13":action}
 passport={"schema_id":"climateos.environmental_evidence_passport.v0.1","passport_id":f"EEP-{REVISION}","subject":"Cooma Evidence Watch offline readiness fixture","source_identity":{"prior_revision":PARENT,"committed_inputs_only":True},"method":{"skill_id":SKILL_ID,"version":VERSION,"fixed_clock":request["evaluation_time"],"network_used":False},"derived_claim":{"answer_id":answer["answer_id"],"convergence_matrix_id":matrix["matrix_id"],"evidence_maturity":"S0","conclusion_level":"L2"},"limitations":{"current_flow":None,"comparison_status":"NOT_COMPARABLE_YET","trend_status":"TREND_DEFERRED"},"review":{"status":"PENDING_FOUNDER_REVIEW"}}
 watch={"schema_id":"climateos.cooma_evidence_watch.v0.1","watch_id":f"WATCH-{REVISION}","title":"Cooma Evidence Watch v0.1 — Offline Readiness Fixture","revision_id":REVISION,"parent_revision":PARENT,"network_used":False,"data_fetched":False,"freshness_record_ids":[x["source_object_id"] for x in freshness],"convergence_matrix_id":matrix["matrix_id"],"refresh_plan_count":len(plan),"answer_id":answer["answer_id"],"passport_id":passport["passport_id"],"action_passport_id":action["action_passport_id"],"evidence_maturity":"S0","conclusion_level":"L2","current_hydrology":{"admission_status":"ADMISSION_BLOCKED_MISSING_RAW_RESPONSE","comparison_status":"NOT_COMPARABLE_YET","trend_status":"TREND_DEFERRED","current_flow":None},"result":"OFFLINE_READINESS_WATCH_NO_REAL_REFRESH"}
 watch["content_digest"]=digest(watch)
 return {"watch":watch,"freshness":{"schema_id":"climateos.evidence_freshness_record_set.v0.1","records":freshness},"matrix":matrix,"plan":{"schema_id":"climateos.refresh_plan.v0.1","plans":plan},"answer":answer,"passport":passport,"action":action,"contracts":contracts}

def render(o):
 return f"""# Cooma Evidence Watch v0.1 — Offline Readiness Fixture

## 1. What question is being watched?
{o['answer']['question']}

## 2. Which evidence is admitted?
Committed BoM DWO, ENSO archive, Mittagang historical L2 and accepted QGIS references are admitted for their bounded roles.

## 3. Which evidence remains a valid historical baseline?
Mittagang 410033 remains `ADMITTED / NOT_APPLICABLE_HISTORICAL_BASELINE / SUPPORTING` for historical use only.

## 4. Which evidence is stale or expired for current-condition use?
July 2026 DWO and ENSO objects are `STALE` under explicit fixture policies. These are not universal scientific windows.

## 5. Which evidence is context only?
ENSO is large-scale context only. QGIS locality, terrain, waterways, catchments and roads are spatial context only.

## 6. Which evidence conflicts?
Historical all-published and A+B summaries differ; this sensitivity remains visible and is not treated as temporal staleness.

## 7. Which evidence is blocked or missing?
WaterNSW is `ACCESS_BLOCKED / ADMISSION_BLOCKED / MISSING_FOR_QUESTION`. Current equivalent flow, qualified review and local observations are missing.

## 8. Why do source counts not equal independence?
Objects may share publisher, instrument, measurement, processing or context lineage. Five QGIS objects are not five local environmental signals.

## 9. What S-stage and L-level are supportable?
Ceiling: `S0/L2`.

## 10. Why did no promotion occur?
There is no admitted near-current flow, temporal/method alignment or independent local convergence. Context-only evidence cannot promote local hydrology.

## 11. When does this Watch expire?
`{o['answer']['valid_until']}`, or earlier on an update, demotion or stop trigger.

## 12. What must be refreshed next?
See `refresh_plan.json`: current observations, exact near-current flow, and bounded local observations require separately authorised evidence paths.

## 13. What A0 action is proportionate?
Inspect freshness, prepare evidence requests, preserve records, prepare monitoring and request professional review.

## 14. Which A1 candidates remain unauthorised?
All listed A1 candidates are `NOT_AUTHORISED / NAMED_HUMAN_APPROVAL_REQUIRED`.

## 15. What would promote, demote or stop the Watch?
Promotion needs new admitted independent evidence and review. Identity/provenance error or expiry demotes. Network attempts, current-condition claims or A2+/public action stop.

## 16. Where are the audit objects?
`freshness_records.json`, `convergence_matrix.json`, `refresh_plan.json`, `time_bounded_environmental_answer.json`, `evidence_passport.json`, `action_passport.json`, `planner_contracts.json`, `evidence_watch.json`, and `run_receipt.json`.
"""

def run(output_root, *, repo_root=None, request_path=None):
 root=Path(repo_root) if repo_root else Path(__file__).resolve().parents[2]
 reqp=Path(request_path) if request_path else root/"cczps_lite/input/cooma_evidence_watch_request_r2.json"
 if not reqp.is_absolute(): reqp=root/reqp
 priorp=root/"cczps_lite/output/cooma_site_reading_v0_1/runs"/PARENT/"site_reading.json"
 paths={"public":root/"cczps_lite/output/cooma_official_real_data_pilot_receipt.json","hydro":root/"cczps_lite/output/waternsw_near_current_evidence_admission/admission_receipt.json","historical":root/"cczps_lite/output/mittagang_410033_historical_characterisation/evidence_passport.json"}
 req=load(reqp); inputs={k:load(v) for k,v in paths.items()}; o=build(req,load(priorp),inputs["public"],inputs["hydro"],inputs["historical"])
 rev=Path(output_root)/"runs"/req["revision_id"]
 if rev.exists(): raise EvidenceWatchError("Immutable revision already exists")
 rev.mkdir(parents=True)
 names={"watch":"evidence_watch.json","freshness":"freshness_records.json","matrix":"convergence_matrix.json","plan":"refresh_plan.json","answer":"time_bounded_environmental_answer.json","passport":"evidence_passport.json","action":"action_passport.json","contracts":"planner_contracts.json"}; result={}
 for key,name in names.items():
  p=rev/name; p.write_text(json.dumps(o[key],indent=2,ensure_ascii=False)+"\n",encoding="utf-8"); result[key]=p
 md=rev/"FOUNDER_EVIDENCE_WATCH.md"; md.write_text(render(o),encoding="utf-8"); result["markdown"]=md
 artifact_root=posix(Path(output_root),root) if Path(output_root).is_absolute() and Path(output_root).is_relative_to(root) else PurePosixPath(Path(output_root)).as_posix()
 receipt={"schema_id":"climateos.cooma_evidence_watch.run_receipt.v0.1","skill_id":SKILL_ID,"skill_version":VERSION,"revision_id":REVISION,"parent_revision":PARENT,"issued_at":req["evaluation_time"],"artifact_root":artifact_root,"network_authorised":False,"network_used":False,"data_fetched":False,"credential_read":False,"inputs":[posix(reqp,root),posix(priorp,root),*[posix(p,root) for p in paths.values()]],"outputs":{k:PurePosixPath(p.relative_to(Path(output_root))).as_posix() for k,p in result.items()},"watch_digest":o["watch"]["content_digest"],"result":"OFFLINE_READINESS_WATCH_NO_REAL_REFRESH","limitations":["ADMISSION_BLOCKED_MISSING_RAW_RESPONSE","NOT_COMPARABLE_YET","TREND_DEFERRED","current_flow = null"]}
 rp=rev/"run_receipt.json"; rp.write_text(json.dumps(receipt,indent=2)+"\n",encoding="utf-8"); result["receipt"]=rp
 return result

def verify_fixture(repo_root=None):
 root=Path(repo_root) if repo_root else Path(__file__).resolve().parents[2]; committed=root/ROOT_NAME/"runs"/REVISION
 with tempfile.TemporaryDirectory() as t:
  made=run(Path(t)/"root",repo_root=root)
  for p in made.values():
   if p.name=="run_receipt.json": continue
   expected=committed/p.name
   if not expected.is_file() or expected.read_bytes()!=p.read_bytes(): raise EvidenceWatchError(f"Fixture mismatch: {p.name}")
  actual=load(made["receipt"]); expected=load(committed/"run_receipt.json")
  for field in ("revision_id","parent_revision","issued_at","network_authorised","network_used","data_fetched","credential_read","inputs","outputs","watch_digest","result","limitations"):
   if actual.get(field)!=expected.get(field): raise EvidenceWatchError(f"Fixture receipt mismatch: {field}")
 return {"status":"PASS","revision_id":REVISION,"verified_files":len(list(committed.iterdir())),"network_used":False,"data_fetched":False,"tracked_files_modified":False}
