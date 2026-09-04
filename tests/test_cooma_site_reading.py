import copy,json,subprocess,sys,tempfile,unittest
from datetime import datetime
from pathlib import Path
from cczps_lite.site_reading.cooma import SiteReadingError,build_outputs,resolve_sources,run,validate_request,verify_fixture
ROOT=Path(__file__).resolve().parents[1]
def load(p): return json.loads((ROOT/p).read_text(encoding="utf-8"))
class CoomaSiteReadingR1Tests(unittest.TestCase):
 def setUp(self):
  self.req=load("cczps_lite/input/cooma_site_reading_request_r1.json"); self.real=load("cczps_lite/output/cooma_official_real_data_pilot_receipt.json"); self.hydro=load("cczps_lite/output/waternsw_near_current_evidence_admission/admission_receipt.json"); base="cczps_lite/output/mittagang_410033_historical_characterisation/"; self.ha=load(base+"time_bounded_environmental_answer.json"); self.hp=load(base+"evidence_passport.json"); self.hr=load(base+"run_receipt.json")
 def build(self): return build_outputs(self.req,self.real,self.hydro,self.ha,self.hp,self.hr,issued_at="2026-09-04T01:00:00Z")
 def test_01_request_contract_validation(self):
  validate_request(self.req); bad=copy.deepcopy(self.req); del bad["environmental_question"]
  with self.assertRaises(SiteReadingError): validate_request(bad)
  bad=copy.deepcopy(self.req); bad["maximum_intervention_class"]="A1"
  with self.assertRaises(SiteReadingError): validate_request(bad)
 def test_02_source_resolution_is_order_independent(self):
  rev=copy.deepcopy(self.real); rev["sources"].reverse(); self.assertEqual(resolve_sources(rev),resolve_sources(self.real))
 def test_03_reject_missing_duplicate_wrong_source(self):
  for mutate in (lambda x:x["sources"].pop(),lambda x:x["sources"].append(copy.deepcopy(x["sources"][0])),lambda x:x["sources"][0].update({"publisher":"wrong"})):
   bad=copy.deepcopy(self.real); mutate(bad)
   with self.assertRaises(SiteReadingError): resolve_sources(bad)
 def test_04_reasoning_and_no_observation_semantics(self):
  r=self.build()["reading"]; self.assertEqual(r["direct_observation_status"],"NONE_ADMITTED_FOR_THIS_READING"); self.assertNotIn("OBSERVED",{c["reasoning_type"] for c in r["claims"]}); self.assertTrue({"KNOWN_FROM_ADMITTED_EVIDENCE","DERIVED","INFERRED","UNKNOWN","MISSING_EVIDENCE","PROHIBITED_CONCLUSION"}<={c["reasoning_type"] for c in r["claims"]})
 def test_05_historical_l2_and_spatial_context_consumed(self):
  r=self.build()["reading"]; self.assertEqual((r["historical_hydrology"]["maturity"],r["historical_hydrology"]["conclusion_level"],r["historical_hydrology"]["evidence_cutoff"]),("S0","L2","2024-02-29")); self.assertEqual(len(r["spatial_context"]),5); self.assertIn("does not itself establish",r["spatial_context_warning"])
 def test_06_existing_contracts_and_validity_reused(self):
  o=self.build(); self.assertEqual(o["answer"]["schema_id"],"climateos.time_bounded_environmental_answer.v0.1"); self.assertEqual(o["passport"]["schema_id"],"climateos.environmental_evidence_passport.v0.1"); self.assertTrue(o["answer"]["valid_until"]); self.assertTrue(o["answer"]["update_triggers"] and o["answer"]["demotion_triggers"] and o["answer"]["stop_conditions"])
 def test_07_pc_contracts_and_a0_only(self):
  o=self.build(); self.assertEqual(set(o["contracts"]),{"pc01","pc02","pc03","pc04"}); ap=o["action_passport"]; self.assertEqual(ap["status"],"READY_FOR_HUMAN_REVIEW"); self.assertEqual(ap["authority"]["maximum_intervention_class"],"A0"); self.assertIn("A1_OR_HIGHER",ap["prohibited_actions"]); self.assertFalse(o["contracts"]["pc03"]["professional_signoff_simulated"])
 def test_08_hydrology_locks_and_prohibited_conclusions(self):
  r=self.build()["reading"]; self.assertEqual(r["current_hydrology"],{"admission_status":"ADMISSION_BLOCKED_MISSING_RAW_RESPONSE","comparison_status":"NOT_COMPARABLE_YET","trend_status":"TREND_DEFERRED","current_flow":None})
 def test_09_deterministic_fixed_identity(self): self.assertEqual(self.build(),self.build())
 def test_10_immutable_revision_and_posix_paths(self):
  with tempfile.TemporaryDirectory() as t:
   paths=run(t,repo_root=ROOT,issued_at="2026-09-04T01:00:00Z"); rec=json.loads(paths["receipt"].read_text()); self.assertTrue(all("\\" not in p for p in rec["inputs"]+list(rec["outputs"].values())))
   with self.assertRaisesRegex(SiteReadingError,"Immutable revision"): run(t,repo_root=ROOT,issued_at="2026-09-04T01:00:00Z")
 def test_11_founder_output_has_required_sections(self):
  with tempfile.TemporaryDirectory() as t:
   text=run(t,repo_root=ROOT,issued_at="2026-09-04T01:00:00Z")["markdown"].read_text(encoding="utf-8")
   for n in range(1,18): self.assertIn(f"## {n}",text)
   for term in ("NONE_ADMITTED_FOR_THIS_READING","27 dated rows","2024-02-29","NOT_COMPARABLE_YET","A0 Action Passport","No H1-H8 sign-off"): self.assertIn(term,text)
 def test_12_rejects_historical_or_hydrology_drift(self):
  bad=copy.deepcopy(self.ha); bad["evidence_cutoff"]="2025-01-01"
  with self.assertRaises(SiteReadingError): build_outputs(self.req,self.real,self.hydro,bad,self.hp,self.hr,issued_at="x")
  badh=copy.deepcopy(self.hydro); badh["admission_status"]="L1_EVIDENCE_ADMITTED"
  with self.assertRaises(SiteReadingError): build_outputs(self.req,self.real,badh,self.ha,self.hp,self.hr,issued_at="x")
 def test_13_verify_fixture_changes_no_tracked_files(self):
  before=subprocess.run(["git","status","--porcelain"],cwd=ROOT,text=True,capture_output=True,check=True).stdout
  result=verify_fixture(repo_root=ROOT)
  after=subprocess.run(["git","status","--porcelain"],cwd=ROOT,text=True,capture_output=True,check=True).stdout
  self.assertEqual(result["status"],"PASS"); self.assertEqual(before,after)
 def test_14_cli_requires_mode_and_help_explains_modes(self):
  cmd=[sys.executable,str(ROOT/"run_cooma_site_reading.py")]
  no_mode=subprocess.run(cmd,cwd=ROOT,text=True,capture_output=True); self.assertNotEqual(no_mode.returncode,0); self.assertIn("required",no_mode.stderr)
  help_run=subprocess.run(cmd+["--help"],cwd=ROOT,text=True,capture_output=True,check=True); self.assertIn("--verify-fixture",help_run.stdout); self.assertIn("unique",help_run.stdout); self.assertIn("revision_id",help_run.stdout)
 def test_15_legacy_outputs_absent_and_parent_nondangling(self):
  base=ROOT/"cczps_lite/output/cooma_site_reading_v0_1"
  for name in ("FOUNDER_SITE_READING.md","evidence_passport.json","run_receipt.json","site_reading.json"): self.assertFalse((base/name).exists())
  self.assertIsNone(self.req["parent_revision"])
 def test_16_artifact_root_paths_resolve(self):
  base=ROOT/"cczps_lite/output/cooma_site_reading_v0_1"; run_dir=base/"runs"/self.req["revision_id"]
  receipt=json.loads((run_dir/"run_receipt.json").read_text(encoding="utf-8")); self.assertEqual(receipt["artifact_root"],"cczps_lite/output/cooma_site_reading_v0_1")
  root=ROOT/receipt["artifact_root"]
  for rel in receipt["outputs"].values(): self.assertNotIn("\\",rel); self.assertTrue((root/rel).is_file(),rel)
 def test_17_machine_validity_basis_and_expiry(self):
  tc=self.req["temporal_context"]; datetime.fromisoformat(tc["valid_until"].replace("Z","+00:00")); self.assertTrue(tc["validity_basis"]); self.assertTrue(tc["expiry_conditions"])
  answer=self.build()["answer"]; self.assertEqual(answer["valid_until"],tc["valid_until"]); self.assertEqual(answer["validity_basis"],tc["validity_basis"])
 def test_18_enso_context_is_bounded(self):
  claims=[c["statement"] for c in self.build()["reading"]["claims"]]
  enso=next(c for c in claims if "ENSO" not in c and "El Nino" in c)
  self.assertIn("no local Cooma impact is inferred",enso); self.assertIn("separately admitted local evidence",enso)
 def test_19_pc_common_envelope_complete_and_bounded(self):
  o=self.build(); objects=[*o["contracts"].values(),o["action_passport"]]
  required={"object_id","object_type","schema_version","revision_id","parent_revision","supersedes","created_at","issued_at","author_role","place_scope","spatial_boundary_id","spatial_boundary_reference","time_scope","evidence_cutoff","intended_use","prohibited_uses","source_object_ids","uncertainties","review_state","maximum_conclusion_level","maximum_intervention_class","valid_until","stop_reasons"}
  for obj in objects:
   self.assertFalse(required-set(obj)); self.assertEqual(obj["maximum_intervention_class"],"A0"); self.assertIn(obj["maximum_conclusion_level"],{"L0","L1","L2"})
if __name__=="__main__": unittest.main()
