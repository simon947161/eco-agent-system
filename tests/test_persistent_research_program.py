import tempfile
import unittest
from pathlib import Path

from cczps_lite.environmental_question_runtime.program import (
    PROGRAM_ID,
    PersistentResearchRuntime,
    ProgramContractError,
    ProgramStateError,
)


def fake_fetch(source):
    return {
        "http_status": 200,
        "final_url": source["url"],
        "content_type": "text/html",
        "etag": None,
        "last_modified": "Fri, 17 Jul 2026 00:00:00 GMT",
        "body": f"first snapshot for {source['source_id']}".encode(),
    }


class PersistentResearchProgramTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.runtime = PersistentResearchRuntime(Path(self.temp.name) / "program.sqlite3")

    def test_cooma_question_is_saved_as_first_durable_program(self):
        program = self.runtime.get_program()
        self.assertEqual(program["program_id"], PROGRAM_ID)
        self.assertIn("less water and snow around Cooma", program["question"])
        self.assertTrue(program["cadence"]["monthly_review"])
        self.assertTrue(program["cadence"]["material_event_review"])
        self.assertFalse(program["cadence"]["unattended_scheduler_installed"])
        self.assertTrue(program["boundaries"]["private_council_or_customer_data_prohibited"])

    def test_monthly_cycles_are_unique_append_only_records(self):
        first = self.runtime.start_cycle("2026-07")
        self.assertEqual(first["state"], "COLLECTING_EVIDENCE")
        with self.assertRaises(ProgramStateError):
            self.runtime.start_cycle("2026-07")
        second = self.runtime.start_cycle("2026-08")
        self.assertEqual(second["previous_cycle_id"], first["cycle_id"])
        self.assertEqual(len(self.runtime.get_program()["cycles"]), 2)
        event = self.runtime.start_cycle("2026-08", trigger="MATERIAL_EVENT")
        self.assertNotEqual(event["cycle_id"], second["cycle_id"])
        with self.assertRaises(ProgramStateError):
            self.runtime.start_cycle("2026-06")

    def test_field_observation_is_unverified_and_privacy_confirmation_is_mandatory(self):
        cycle = self.runtime.start_cycle("2026-07")
        with self.assertRaises(ProgramContractError):
            self.runtime.add_observation(
                cycle["cycle_id"], category="WATER", observed_on="2026-07-18",
                note="The visible river level appeared low from a public lookout.",
                location_scope="Cooma public area", public_safe_confirmation=False,
            )
        observation = self.runtime.add_observation(
            cycle["cycle_id"], category="WATER", observed_on="2026-07-18",
            note="The visible river level appeared low from a public lookout; no instrument reading was taken.",
            location_scope="Cooma public area", public_safe_confirmation=True,
        )
        self.assertEqual(observation["evidence_class"], "HUMAN_FIELD_OBSERVATION_UNVERIFIED")
        self.assertIn("does_not_prove", observation)

    def test_live_refresh_requires_approval_and_retains_no_raw_body(self):
        cycle = self.runtime.start_cycle("2026-07")
        with self.assertRaises(ProgramContractError):
            self.runtime.refresh_official_sources(cycle["cycle_id"], human_approval=False, fetcher=fake_fetch)
        result = self.runtime.refresh_official_sources(cycle["cycle_id"], human_approval=True, fetcher=fake_fetch)
        self.assertTrue(result["network_used"])
        self.assertEqual(result["cost_aud"], 0)
        self.assertEqual(len(result["snapshots"]), 5)
        for snapshot in result["snapshots"]:
            self.assertEqual(snapshot["change_state"], "BASELINE_CAPTURED")
            self.assertFalse(snapshot["raw_content_retained"])
            self.assertNotIn("body", snapshot)
            self.assertIsNone(snapshot["environmental_conclusion"])
        with self.assertRaises(ProgramStateError):
            self.runtime.refresh_official_sources(cycle["cycle_id"], human_approval=True, fetcher=fake_fetch)

    def test_second_cycle_detects_digest_change_but_forms_no_conclusion(self):
        first = self.runtime.start_cycle("2026-07")
        self.runtime.refresh_official_sources(first["cycle_id"], human_approval=True, fetcher=fake_fetch)
        compiled = self.runtime.compile_cycle(first["cycle_id"])
        self.runtime.review_cycle(
            first["cycle_id"], decision="ACCEPT_CYCLE", reviewer="Founder reviewer",
            reason="Accept the first source-freshness baseline as a research record only.",
        )
        second = self.runtime.start_cycle("2026-08")

        def changed_fetch(source):
            result = fake_fetch(source)
            if source["source_id"] == "COOMA-MON-SMRC-WATER-WASTEWATER":
                result["body"] = b"changed public page bytes"
            return result

        self.runtime.refresh_official_sources(second["cycle_id"], human_approval=True, fetcher=changed_fetch)
        compiled = self.runtime.compile_cycle(second["cycle_id"])
        self.assertEqual(compiled["comparison"]["potential_source_change_count"], 1)
        self.assertEqual(compiled["hypothesis_version"]["state"], "EVIDENCE_CHANGE_REVIEW_REQUIRED")
        self.assertIsNone(compiled["hypothesis_version"]["environmental_conclusion"])
        self.assertIn("Cooma environmental trend", compiled["passport"]["does_not_support"])

    def test_review_updates_program_version_without_environmental_signoff(self):
        cycle = self.runtime.start_cycle("2026-07")
        compiled = self.runtime.compile_cycle(cycle["cycle_id"])
        reviewed = self.runtime.review_cycle(
            cycle["cycle_id"], decision="ACCEPT_CYCLE", reviewer="Founder reviewer",
            reason="The empty baseline is accepted as an auditable monthly research record.",
        )
        self.assertEqual(reviewed["state"], "CYCLE_REVIEWED_ACCEPTED_AS_RESEARCH_RECORD")
        self.assertFalse(reviewed["human_review"]["environmental_signoff"])
        program = self.runtime.get_program()
        self.assertEqual(program["current_hypothesis_version"], compiled["hypothesis_version"]["version"])
        self.assertEqual(program["last_reviewed_cycle_id"], cycle["cycle_id"])


if __name__ == "__main__":
    unittest.main()
