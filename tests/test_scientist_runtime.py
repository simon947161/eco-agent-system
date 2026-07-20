import copy
import json
import sqlite3
import tempfile
import unittest
from contextlib import closing
from pathlib import Path

from cczps_lite.scientist_runtime import RuntimeBoundaryError, RuntimeStateError, ScientistRuntime
from cczps_lite.scientist_runtime.contracts import (
    BOUNDARY_LABEL,
    RESOURCE_CEILING,
    ContractError,
    digest,
    validate_object_graph,
)
from cczps_lite.scientist_runtime.runtime import FIXTURE_PATH, execute_fixed_fixture

ROOT = Path(__file__).resolve().parents[1]
RUNTIME_SOURCE = ROOT / "cczps_lite" / "scientist_runtime" / "runtime.py"


class ScientistRuntimeTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.db_path = Path(self.temp.name) / "runtime.sqlite3"
        self.runtime = ScientistRuntime(self.db_path)
        self.addCleanup(self.runtime.close)
        self.question = (
            "In the fictional sealed scalar box, does the fixed perturbation "
            "increase the response index compared with baseline?"
        )

    def proposed(self):
        session = self.runtime.create_session(self.question)
        return self.runtime.propose_hypothesis(session["session_id"])

    def approved(self):
        session = self.proposed()
        return self.runtime.decide_before_run(
            session["session_id"],
            decision="APPROVE",
            reviewer_label="Human test reviewer",
            reason="Approve this exact fictional fixture for bounded workflow testing only.",
        )

    def test_question_to_structured_hypothesis_builds_linked_object_graph(self):
        session = self.proposed()
        graph = session["object_graph"]
        self.assertEqual(session["state"], "HYPOTHESIS_PROPOSED")
        validate_object_graph(graph)
        self.assertEqual(graph["experiment_design"]["hypothesis_id"], graph["hypothesis"]["hypothesis_id"])
        self.assertEqual(graph["run_request"]["configuration_id"], graph["configuration_identity"]["configuration_id"])
        self.assertEqual(graph["resource_ceiling"], RESOURCE_CEILING)
        self.assertIn("falsification_criteria", graph["hypothesis"])
        self.assertGreaterEqual(len(graph["hypothesis"]["alternative_explanations"]), 2)

    def test_repeated_question_creates_distinct_auditable_sessions(self):
        first = self.runtime.create_session(self.question, session_label="repeat")
        second = self.runtime.create_session(self.question, session_label="repeat")
        self.assertNotEqual(first["session_id"], second["session_id"])
        self.assertEqual(first["question"], second["question"])

    def test_real_regions_and_external_models_are_refused(self):
        for term in ("Bondo", "Riverina", "Tumut", "Cooma", "GraphCast", "WRF"):
            with self.subTest(term=term), self.assertRaises(ContractError):
                self.runtime.create_session(
                    f"Does {term} show a real environmental response in this proposed study?",
                    session_label=term,
                )

    def test_execution_is_refused_without_exact_human_approval(self):
        session = self.proposed()
        with self.assertRaises(RuntimeStateError):
            self.runtime.run(session["session_id"])
        graph = copy.deepcopy(session["object_graph"])
        with self.assertRaises(RuntimeBoundaryError):
            execute_fixed_fixture(graph)

    def test_human_can_revise_wording_without_replacing_identity_or_fixture(self):
        session = self.proposed()
        hypothesis = copy.deepcopy(session["object_graph"]["hypothesis"])
        hypothesis["revision_id"] = f'{hypothesis["hypothesis_id"]}-R2'
        hypothesis["hypothesis_statement"] = (
            "For this fictional offline box, the higher fixed test input will "
            "produce a higher output score."
        )
        revised = self.runtime.revise_hypothesis(
            session["session_id"], hypothesis,
            reviewer_label="Founder reviewer",
            reason="Clarify the wording without changing the fixed local execution package.",
        )
        self.assertEqual(revised["state"], "HYPOTHESIS_PROPOSED")
        self.assertEqual(revised["object_graph"]["hypothesis"]["revision_id"], hypothesis["revision_id"])
        self.assertEqual(revised["object_graph"]["hypothesis"]["fixture_id"], "TINY-SYNTH-SCALAR-001")
        self.assertEqual(revised["audit_events"][-1]["event_type"], "HUMAN_HYPOTHESIS_REVISED")

    def test_human_revision_cannot_cross_the_real_region_boundary(self):
        session = self.proposed()
        hypothesis = copy.deepcopy(session["object_graph"]["hypothesis"])
        hypothesis["revision_id"] = f'{hypothesis["hypothesis_id"]}-R2'
        hypothesis["hypothesis_statement"] = "Use this fictional result to make a Bondo project conclusion."
        with self.assertRaises(ContractError):
            self.runtime.revise_hypothesis(
                session["session_id"], hypothesis,
                reviewer_label="Founder reviewer",
                reason="This deliberate boundary violation must be refused by the Runtime.",
            )

    def test_reject_and_stop_are_terminal_before_run(self):
        for decision, state in (("REJECT", "REJECTED_BEFORE_RUN"), ("STOP", "STOPPED_BEFORE_RUN")):
            runtime = ScientistRuntime(Path(self.temp.name) / f"{decision}.sqlite3")
            created = runtime.create_session(self.question, session_label=decision)
            proposed = runtime.propose_hypothesis(created["session_id"])
            result = runtime.decide_before_run(
                proposed["session_id"], decision=decision, reviewer_label="Human reviewer",
                reason="This deliberate refusal tests the supervised stop path."
            )
            self.assertEqual(result["state"], state)
            with self.assertRaises(RuntimeStateError):
                runtime.run(result["session_id"])

    def test_approved_fixed_run_generates_receipt_and_quarantined_passport(self):
        approved = self.approved()
        session = self.runtime.run(approved["session_id"])
        self.assertEqual(session["state"], "RUN_COMPLETED_QUARANTINED")
        self.assertEqual(session["receipt"]["receipt_state"], "RECEIPT_STRUCTURALLY_ACCEPTED")
        self.assertEqual(session["passport"]["state"], "SUPPORTED_SYNTHETIC_ONLY")
        self.assertEqual(session["passport"]["diagnostics"]["response_index_delta"], 3.5)
        self.assertIsNone(session["passport"]["scientific_claim"])
        self.assertIsNone(session["passport"]["regional_conclusion"])
        self.assertTrue(session["passport"]["human_review_required"])
        self.assertIn("QUARANTINED", session["passport"]["quarantine_state"])

    def test_observed_resources_and_no_egress_boundary_are_recorded(self):
        session = self.runtime.run(self.approved()["session_id"])
        observed = session["receipt"]["resources_observed"]
        self.assertFalse(observed["network_used"])
        self.assertFalse(observed["secrets_used"])
        self.assertFalse(observed["subprocess_used"])
        self.assertEqual(observed["cost_aud"], 0)
        for key in ("logical_cpu_workers", "wall_time_seconds", "incremental_memory_mib", "output_bytes", "cost_aud"):
            self.assertLessEqual(observed[key], RESOURCE_CEILING[key])

    def test_post_run_human_review_preserves_non_environmental_quarantine(self):
        run = self.runtime.run(self.approved()["session_id"])
        reviewed = self.runtime.review(
            run["session_id"],
            decision="EVIDENCE_INSUFFICIENT",
            reviewer_label="Human test reviewer",
            reason="The workflow is reviewable but the fixture is not scientific evidence.",
        )
        self.assertEqual(reviewed["state"], "REVIEWED_EVIDENCE_INSUFFICIENT")
        self.assertFalse(reviewed["human_review"]["scientific_signoff"])
        self.assertFalse(reviewed["human_review"]["release_as_environmental_evidence"])
        self.assertEqual(reviewed["passport"]["quarantine_state"], "REVIEWED_BUT_REMAINS_NON_ENVIRONMENTAL_DEMO")

    def test_audit_is_persistent_append_only_and_hash_chained(self):
        run = self.runtime.run(self.approved()["session_id"])
        restarted = ScientistRuntime(self.db_path)
        try:
            loaded = restarted.get_session(run["session_id"])
            self.assertEqual(len(loaded["audit_events"]), 4)
            self.assertTrue(loaded["audit_chain_valid"])
            with closing(sqlite3.connect(self.db_path)) as connection:
                with connection:
                    connection.execute(
                        "UPDATE scientist_audit_events SET detail_json='{}' WHERE sequence_number=2"
                    )
            self.assertFalse(restarted.get_session(run["session_id"])["audit_chain_valid"])
        finally:
            restarted.close()

    def test_fixture_is_repository_authored_closed_and_fictional(self):
        fixture = json.loads(FIXTURE_PATH.read_text(encoding="utf-8"))
        self.assertEqual(fixture["origin"], "REPOSITORY_AUTHORED_FICTIONAL_TINY_SYNTHETIC")
        self.assertTrue(fixture["not_environmental_evidence"])
        self.assertEqual(fixture["boundary_label"], BOUNDARY_LABEL)
        self.assertEqual(fixture["seed"], 17)

    def test_runtime_has_no_network_subprocess_or_external_client_import(self):
        source = RUNTIME_SOURCE.read_text(encoding="utf-8")
        for prohibited in (
            "import socket", "import requests", "import httpx", "urlopen(",
            "import subprocess", "os.system(", "FastAPI", "openai"
        ):
            self.assertNotIn(prohibited, source)

    def test_export_is_a_bounded_local_artifact_set(self):
        run = self.runtime.run(self.approved()["session_id"])
        reviewed = self.runtime.review(
            run["session_id"], decision="ACCEPT_RUNTIME_DEMO", reviewer_label="Human test reviewer",
            reason="The local workflow mechanics completed while scientific release remains blocked."
        )
        paths = self.runtime.export_session(reviewed["session_id"], Path(self.temp.name) / "export")
        self.assertEqual(set(paths), {"session", "receipt", "passport"})
        for path in paths.values():
            self.assertTrue(Path(path).is_file())
        exported = json.loads(Path(paths["session"]).read_text(encoding="utf-8"))
        self.assertEqual(exported["session_id"], reviewed["session_id"])
        self.assertEqual(digest(exported["passport"]), digest(reviewed["passport"]))

    def test_export_can_be_verified_restored_and_reviewed_later(self):
        run = self.runtime.run(self.approved()["session_id"])
        export_dir = Path(self.temp.name) / "continuation"
        paths = self.runtime.export_session(run["session_id"], export_dir)
        continued = ScientistRuntime(Path(self.temp.name) / "continued.sqlite3")
        restored = continued.import_session_export(paths["session"])
        self.assertEqual(restored["state"], "RUN_COMPLETED_QUARANTINED")
        self.assertTrue(restored["audit_chain_valid"])
        reviewed = continued.review(
            restored["session_id"], decision="ACCEPT_RUNTIME_DEMO",
            reviewer_label="Founder human reviewer",
            reason="The Founder accepts the supervised Runtime demonstration while retaining every evidence boundary."
        )
        self.assertEqual(reviewed["state"], "REVIEWED_DEMO_ACCEPTED")
        self.assertEqual(len(reviewed["audit_events"]), 5)
        self.assertTrue(reviewed["audit_chain_valid"])


if __name__ == "__main__":
    unittest.main()
