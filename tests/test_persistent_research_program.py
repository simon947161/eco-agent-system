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
        self.assertEqual(program["cadence"]["monthly_due_rule"], "LAST_CALENDAR_DAY")
        self.assertEqual(program["cadence"]["annual_report_rule"], "AFTER_REVIEWED_DECEMBER_CYCLE")
        self.assertTrue(program["cadence"]["material_event_review"])
        self.assertFalse(program["cadence"]["unattended_scheduler_installed"])
        self.assertTrue(program["boundaries"]["private_council_or_customer_data_prohibited"])

    def test_monthly_cycles_are_unique_append_only_records(self):
        first = self.runtime.start_cycle("2026-07")
        self.assertEqual(first["state"], "COLLECTING_EVIDENCE")
        self.assertEqual(first["period_start"], "2026-07-01")
        self.assertEqual(first["period_end"], "2026-07-31")
        self.assertEqual(first["review_due_on"], "2026-07-31")
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
        self.assertEqual(observation["verbatim_human_report"], observation["note"])
        self.assertIn("reported_at", observation)
        self.assertEqual(observation["structured_record"]["structuring_state"], "HUMAN_ENTERED_AND_CONFIRMED")
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

    def test_annual_report_requires_reviewed_december_and_preserves_missing_months(self):
        with self.assertRaises(ProgramStateError):
            self.runtime.annual_report(2026)
        december = self.runtime.start_cycle("2026-12")
        self.runtime.add_observation(
            december["cycle_id"], category="SNOW", observed_on="2026-12-14",
            note="A public-area visual snow observation was reported without an instrument measurement.",
            location_scope="Cooma public area", public_safe_confirmation=True,
        )
        self.runtime.compile_cycle(december["cycle_id"])
        self.runtime.review_cycle(
            december["cycle_id"], decision="ACCEPT_CYCLE", reviewer="Founder reviewer",
            reason="Accept the December cycle as a research record before annual compilation.",
        )
        report = self.runtime.annual_report(2026)
        self.assertEqual(report["summary"]["cycle_count"], 1)
        self.assertEqual(report["summary"]["field_observation_count"], 1)
        self.assertIn("2026-01", report["summary"]["missing_months"])
        self.assertNotIn("2026-12", report["summary"]["missing_months"])
        self.assertIsNone(report["environmental_conclusion"])
        self.assertEqual(report["receipt"]["network_calls_during_report_generation"], 0)
        with self.assertRaises(ProgramStateError):
            self.runtime.annual_report(2026)


if __name__ == "__main__":
    unittest.main()
