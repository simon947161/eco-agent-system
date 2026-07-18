import tempfile
import unittest
from pathlib import Path

from cczps_lite.environmental_question_runtime import EnvironmentalQuestionRuntime, RuntimeStateError


QUESTION = (
    "I observed less water and snow around Cooma. What could this mean for future bushfire risk "
    "and drinking-water security? What wastewater work exists, what are its practical limits, "
    "and how could wastewater management contribute to climate adaptation?"
)


class EnvironmentalQuestionRuntimeTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.runtime = EnvironmentalQuestionRuntime(Path(self.temp.name) / "runtime.sqlite3")

    def test_real_question_is_preserved_but_real_execution_is_blocked(self):
        session = self.runtime.create_question(QUESTION)
        self.assertEqual(session["question"], QUESTION)
        self.assertEqual(session["state"], "REAL_WORLD_PLAN_PROPOSED")
        plan = session["real_world_plan"]
        self.assertEqual(plan["classification"], "REAL_WORLD_PLAN_ONLY")
        self.assertEqual(plan["real_execution"], "BLOCKED_NOT_AUTHORIZED")
        self.assertEqual(len(plan["modules"]), 5)
        self.assertIn("No claim that next year is definitely El Niño", plan["modules"][0]["cannot_claim_yet"])

    def test_complete_approved_synthetic_rehearsal(self):
        created = self.runtime.create_question(QUESTION)
        rehearsal = self.runtime.create_rehearsal(created["session_id"])
        self.assertIn("NOT COOMA", rehearsal["rehearsal_plan"]["place"])
        approved = self.runtime.decide(
            created["session_id"], "APPROVE", "Founder human reviewer",
            "Approve the exact fictional rehearsal for workflow testing only."
        )
        self.assertEqual(approved["state"], "SYNTHETIC_APPROVED_TO_RUN")
        run = self.runtime.run(created["session_id"])
        self.assertEqual(run["state"], "SYNTHETIC_RUN_COMPLETED_QUARANTINED")
        self.assertFalse(run["receipt"]["network_used"])
        self.assertEqual(run["receipt"]["cost_aud"], 0)
        self.assertEqual(run["passport"]["state"], "SUPPORTED_SYNTHETIC_ONLY")
        self.assertIn("Cooma environmental conclusion", run["passport"]["does_not_support"])
        reviewed = self.runtime.review(
            created["session_id"], "ACCEPT_DEMO", "Founder human reviewer",
            "The workflow is useful while the values remain fictional and quarantined."
        )
        self.assertEqual(reviewed["state"], "REVIEWED_DEMO_ACCEPTED")
        self.assertTrue(reviewed["audit_chain_valid"])
        self.assertFalse(reviewed["human_review"]["real_environmental_release"])

    def test_run_without_human_approval_is_refused(self):
        created = self.runtime.create_question(QUESTION)
        self.runtime.create_rehearsal(created["session_id"])
        with self.assertRaises(RuntimeStateError):
            self.runtime.run(created["session_id"])


if __name__ == "__main__":
    unittest.main()
