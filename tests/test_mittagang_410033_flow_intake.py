import copy
import csv
import io
import json
import tempfile
import unittest
from pathlib import Path

from cczps_lite.integration.mittagang_410033_flow_intake import (
    SOURCE_URL,
    MittagangFlowIntakeError,
    parse_daily_flow,
    run_intake,
    validate_public_receipt,
)


def fixture_csv() -> bytes:
    stream = io.StringIO()
    writer = csv.writer(stream, lineterminator="\n")
    writer.writerow(["#", "Australian Bureau of Meteorology"])
    writer.writerow(["#", "Hydrologic Reference Stations"])
    writer.writerow(["#", "Dataset version:", "August, 2024"])
    writer.writerow(["#", "Daily streamflow (ML/day) and quality code"])
    writer.writerow(["#", "Murrumbidgee River at Mittagang Crossing (410033)"])
    writer.writerow(["#", "Source used:", "WISKI (validated data only)"])
    writer.writerow(
        [
            "#",
            "Extraction method:",
            "daily discharge total (cubic metres), reported at 9am local time for the previous 24 hours.",
        ]
    )
    writer.writerow(["#", "Data extraction date:", "14/06/2024"])
    writer.writerow(["Date", "Flow (ML)", "Bureau QCode"])
    writer.writerow(["2024-02-27", "89.856", "A"])
    writer.writerow(["2024-02-28", "81.7344", "B"])
    writer.writerow(["2024-02-29", "75.6864", "E"])
    return stream.getvalue().encode()


def fake_fetch():
    return {
        "body": fixture_csv(),
        "http_status": 200,
        "final_url": SOURCE_URL,
        "content_type": "text/csv",
        "etag": None,
        "last_modified": None,
    }


class Mittagang410033FlowIntakeTests(unittest.TestCase):
    def test_parser_validates_identity_units_coverage_quality_and_timezone_limit(self):
        result = parse_daily_flow(fixture_csv())
        self.assertEqual(result["station_id"], "410033")
        self.assertEqual(result["canonical_unit"], "ML/day")
        self.assertEqual(result["coverage_start"], "2024-02-27")
        self.assertEqual(result["coverage_end"], "2024-02-29")
        self.assertEqual(result["missing_calendar_date_count"], 0)
        self.assertEqual(result["duplicate_date_count"], 0)
        self.assertEqual(result["quality_code_counts"]["E"], 1)
        self.assertEqual(result["day_boundary_local_time"], "09:00")
        self.assertIsNone(result["timezone_identifier"])

    def test_manual_approval_is_required(self):
        with tempfile.TemporaryDirectory() as temp:
            with self.assertRaisesRegex(MittagangFlowIntakeError, "approval"):
                run_intake(temp, human_approval=False, fetcher=fake_fetch)

    def test_run_retains_raw_locally_and_publishes_only_l1_metadata(self):
        with tempfile.TemporaryDirectory() as temp:
            full, public = run_intake(
                temp,
                human_approval=True,
                fetcher=fake_fetch,
                retrieved_at="2026-07-28T08:40:00Z",
            )
            self.assertTrue(Path(full["source"]["local_raw_path"]).exists())
            self.assertEqual(public["maximum_conclusion_level"], "L1")
            self.assertIsNone(public["environmental_conclusion"])
            self.assertEqual(
                public["water_supply_sufficiency_status"], "NOT_EVALUATED"
            )
            self.assertFalse(public["source"]["raw_content_retained_publicly"])
            self.assertNotIn("observation_rows", public["source"])

    def test_redirect_and_unknown_quality_code_are_rejected(self):
        def redirected():
            result = fake_fetch()
            result["final_url"] = "https://example.invalid/flow.csv"
            return result

        with tempfile.TemporaryDirectory() as temp:
            with self.assertRaisesRegex(MittagangFlowIntakeError, "URL changed"):
                run_intake(temp, human_approval=True, fetcher=redirected)
        changed = fixture_csv().replace(b",E\n", b",Z\n")
        with self.assertRaisesRegex(MittagangFlowIntakeError, "unknown quality"):
            parse_daily_flow(changed)

    def test_public_receipt_rejects_raw_rows_and_environmental_claims(self):
        with tempfile.TemporaryDirectory() as temp:
            _, public = run_intake(temp, human_approval=True, fetcher=fake_fetch)
            changed = copy.deepcopy(public)
            changed["source"]["observation_rows"] = [["2024-02-29", 75.68]]
            with self.assertRaises(MittagangFlowIntakeError):
                validate_public_receipt(changed)
            changed = copy.deepcopy(public)
            changed["environmental_conclusion"] = "Cooma has enough water."
            with self.assertRaises(MittagangFlowIntakeError):
                validate_public_receipt(changed)

    def test_committed_real_run_receipt_is_valid(self):
        receipt_path = (
            Path(__file__).resolve().parents[1]
            / "cczps_lite"
            / "output"
            / "mittagang_410033_flow_intake_receipt.json"
        )
        receipt = json.loads(receipt_path.read_text(encoding="utf-8"))
        validate_public_receipt(receipt)
        metadata = receipt["source"]["parsed_metadata"]
        self.assertEqual(metadata["row_count"], 21915)
        self.assertEqual(metadata["coverage_start"], "1964-03-01")
        self.assertEqual(metadata["coverage_end"], "2024-02-29")
        self.assertEqual(metadata["missing_calendar_date_count"], 0)
        self.assertEqual(metadata["duplicate_date_count"], 0)


if __name__ == "__main__":
    unittest.main()
