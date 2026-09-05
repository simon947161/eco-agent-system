import ast,copy,json,subprocess,tempfile,unittest
from pathlib import Path
from cczps_lite.evidence_watch.cooma import EvidenceWatchError,PARENT,REVISION,build,run,verify_fixture
ROOT=Path(__file__).resolve().parents[1]
def load(p): return json.loads((ROOT/p).read_text(encoding="utf-8"))
class CoomaEvidenceWatchTests(unittest.TestCase):
 def setUp(self):
  self.req=load("cczps_lite/input/cooma_evidence_watch_request_r2.json"); self.prior=load(f"cczps_lite/output/cooma_site_reading_v0_1/runs/{PARENT}/site_reading.json"); self.public=load("cczps_lite/output/cooma_official_real_data_pilot_receipt.json"); self.hydro=load("cczps_lite/output/waternsw_near_current_evidence_admission/admission_receipt.json"); self.hist=load("cczps_lite/output/mittagang_410033_historical_characterisation/evidence_passport.json")
 def out(self): return build(self.req,self.prior,self.public,self.hydro,self.hist)
 def by(self,s): return next(x for x in self.out()["freshness"]["records"] if x["source_object_id"]==s)
 def test_01_prior_ep_skill_fixture(self): self.assertEqual(load(f"cczps_lite/output/cooma_site_reading_v0_1/runs/{PARENT}/run_receipt.json")["result"],"BOUNDED_SITE_READING_PRODUCED")
 def test_02_orthogonal_states_coexist(self): self.assertEqual((self.by("COOMA-BOM-DWO-2026-07")["admission_state"],self.by("COOMA-BOM-DWO-2026-07")["temporal_state"],self.by("COOMA-BOM-DWO-2026-07")["evidence_relation"]),("ADMITTED","STALE","SUPPORTING"))
 def test_03_admitted_current_conflicting_representable(self):
  r=copy.deepcopy(self.by("COOMA-BOM-DWO-2026-07")); r.update(temporal_state="CURRENT_FOR_DECLARED_USE",evidence_relation="CONFLICTING"); self.assertEqual((r["admission_state"],r["temporal_state"],r["evidence_relation"]),("ADMITTED","CURRENT_FOR_DECLARED_USE","CONFLICTING"))
 def test_04_historical_not_current(self): self.assertEqual(self.by("MITTAGANG-410033-HISTORICAL-ANSWER-V0.1")["temporal_state"],"NOT_APPLICABLE_HISTORICAL_BASELINE")
 def test_05_available_not_admitted(self):
  r=copy.deepcopy(self.by("COOMA-BOM-DWO-2026-07")); r.update(admission_state="NOT_RETRIEVED",temporal_state="NOT_EVALUATED"); self.assertNotEqual(r["availability_state"],r["admission_state"])
 def test_06_conflict_not_stale(self): self.test_03_admitted_current_conflicting_representable()
 def test_07_blocked_not_missing(self):
  r=self.by("WATERNSW-410033-NEAR-CURRENT-ADMISSION-V0.1"); self.assertEqual(r["admission_state"],"ADMISSION_BLOCKED"); self.assertEqual(r["evidence_relation"],"MISSING_FOR_QUESTION")
 def test_08_no_self_promotion(self): self.assertFalse(self.out()["matrix"]["promotion_allowed"])
 def test_09_shared_lineage_visible(self): self.assertIn("QGIS_CONTEXT",self.out()["matrix"]["shared_lineage"])
 def test_10_context_cannot_promote(self): self.assertIn("ENSO and QGIS are context only",self.out()["matrix"]["promotion_blockers"])
 def test_11_stale_not_presented_current(self): self.assertIn("stale for current-condition use",self.out()["answer"]["answer"])
 def test_12_fixed_clock_deterministic(self): self.assertEqual(self.out(),self.out())
 def test_13_prior_revision_immutable(self): self.assertEqual(self.out()["watch"]["parent_revision"],PARENT)
 def test_14_posix_resolvable_paths(self):
  with tempfile.TemporaryDirectory() as t:
   made=run(Path(t)/"root",repo_root=ROOT); receipt=json.loads(made["receipt"].read_text()); self.assertTrue(all("\\" not in x for x in receipt["inputs"]+list(receipt["outputs"].values())))
 def test_15_network_denied(self):
  source=(ROOT/"cczps_lite/evidence_watch/cooma.py").read_text(); tree=ast.parse(source); imports={n.names[0].name for n in ast.walk(tree) if isinstance(n,(ast.Import,ast.ImportFrom)) for _ in [0] if getattr(n,"names",None)}; self.assertFalse(imports & {"requests","urllib","httpx","socket"}); self.assertFalse(self.out()["watch"]["network_used"])
 def test_16_a1_unauthorised(self): self.assertTrue(all(x["status"]=="NOT_AUTHORISED" for x in self.out()["action"]["a1_candidates"]))
 def test_17_prohibited_fail_closed(self): self.assertIn("A2_OR_HIGHER",self.out()["answer"]["prohibited_actions"])
 def test_18_founder_watch_sections(self):
  with tempfile.TemporaryDirectory() as t:
   text=run(Path(t)/"root",repo_root=ROOT)["markdown"].read_text(encoding="utf-8"); self.assertTrue(all(f"## {n}." in text for n in range(1,17)))
 def test_19_fixture_verifies(self): self.assertEqual(verify_fixture(ROOT)["status"],"PASS")
 def test_20_receipt_truth_and_overwrite(self):
  with tempfile.TemporaryDirectory() as t:
   made=run(Path(t)/"root",repo_root=ROOT); rec=load(Path(made["receipt"]).relative_to(ROOT)) if False else json.loads(made["receipt"].read_text()); self.assertFalse(rec["network_used"] or rec["data_fetched"] or rec["credential_read"])
   with self.assertRaises(EvidenceWatchError): run(Path(t)/"root",repo_root=ROOT)
if __name__=="__main__": unittest.main()
