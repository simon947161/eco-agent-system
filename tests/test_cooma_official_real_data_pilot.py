import copy
import csv
import io
import json
import tempfile
import unittest
from pathlib import Path

from cczps_lite.integration.cooma_official_real_data_pilot import (
    ALLOWED_HOST,
    CoomaRealDataPilotError,
    SOURCES,
    parse_bom_enso_archive,
    parse_cooma_daily_weather,
    run_pilot,
    validate_public_receipt,
)


def weather_csv() -> bytes:
    stream = io.StringIO()
    writer = csv.writer(stream, lineterminator="\n")
    writer.writerow(["Daily Weather Observations for Cooma, New South Wales for July 2026"])
    writer.writerow(["Prepared at 00:36 UTC on Monday 27 July 2026   IDCJDW2033.202607"])
    writer.writerow(["Copyright 2003 Commonwealth Bureau of Meteorology"])
    writer.writerow(["Most observations from Cooma, but some from Cooma Airport."])
    writer.writerow(["Temperature and rainfall observations are from station 070278"])
    writer.writerow(["Wind and pressure observations are from station 070217"])
    writer.writerow([])
    writer.writerow(["", "Date", "Minimum temperature (°C)", "Rainfall (mm)"])
    writer.writerow(["", "2026-07-1", "3.0", "0.3"])
    writer.writerow(["", "2026-07-2", "6.0", "12.2"])
    return stream.getvalue().encode()


def enso_html() -> bytes:
    return b"""
    <html><body>
    <p>El Ni\xc3\xb1o is underway.</p>
    <p>The relative Nino index for the week ending 12 July 2026 is +1.47,
    above the +0.80 threshold. The 30-day SOI is \xe2\x80\x9325.8.</p>
    </body></html>
    """


def fake_fetch(source):
    body = weather_csv() if source["media_type"] == "text/csv" else enso_html()
    return {
        "body": body,
        "http_status": 200,
        "final_url": source["url"],
        "content_type": source["media_type"],
        "etag": None,
        "last_modified": None,
    }


class CoomaOfficialRealDataPilotTests(unittest.TestCase):
    def test_sources_are_two_exact_https_bom_products(self):
        self.assertEqual(len(SOURCES), 2)
        self.assertEqual({source["publisher"] for source in SOURCES}, {"Australian Bureau of Meteorology"})
        for source in SOURCES:
            self.assertTrue(source["url"].startswith(f"https://{ALLOWED_HOST}/"))

    def test_manual_approval_is_mandatory(self):
        with tempfile.TemporaryDirectory() as temp:
            with self.assertRaisesRegex(CoomaRealDataPilotError, "human approval"):
                run_pilot(temp, human_approval=False, fetcher=fake_fetch)

    def test_daily_weather_parser_records_coverage_not_public_values(self):
        result = parse_cooma_daily_weather(weather_csv())
        self.assertEqual(result["product_id"], "IDCJDW2033.202607")
        self.assertEqual(result["station_ids"], ["070278", "070217"])
        self.assertEqual(result["row_count"], 2)
        self.assertEqual(result["coverage_start"], "2026-07-1")
        self.assertEqual(result["coverage_end"], "2026-07-2")
        self.assertFalse(result["quantitative_values_publicly_retained"])

    def test_enso_archive_is_admitted_as_official_outlook_not_local_impact(self):
        result = parse_bom_enso_archive(enso_html())
        self.assertEqual(result["state"], "EL_NINO_UNDERWAY")
        self.assertEqual(result["relative_nino34_c"], 1.47)
        self.assertIsNone(result["local_cooma_impact_claim"])

    def test_real_pilot_retains_raw_locally_and_redacts_public_receipt(self):
        with tempfile.TemporaryDirectory() as temp:
            full, public = run_pilot(
                temp,
                human_approval=True,
                fetcher=fake_fetch,
                retrieved_at="2026-07-27T01:30:00Z",
            )
            self.assertTrue(full["network_used"])
            self.assertEqual(full["source_count"], 2)
            self.assertEqual(public["maximum_conclusion_level"], "L1")
            self.assertEqual(public["cooma_water_balance_status"], "BLOCKED_MISSING_REQUIRED_TERMS")
            self.assertIsNone(public["environmental_conclusion"])
            for record in full["sources"]:
                self.assertTrue(Path(record["local_raw_path"]).exists())
                self.assertTrue(record["content_digest"].startswith("sha256:"))
            for record in public["sources"]:
                self.assertFalse(record["raw_content_retained_publicly"])
                self.assertNotIn("body", record)
                self.assertNotIn("observation_rows", record)

    def test_public_receipt_rejects_raw_content_and_conclusions(self):
        with tempfile.TemporaryDirectory() as temp:
            _, public = run_pilot(temp, human_approval=True, fetcher=fake_fetch)
            changed = copy.deepcopy(public)
            changed["sources"][0]["body"] = "raw"
            with self.assertRaises(CoomaRealDataPilotError):
                validate_public_receipt(changed)
            changed = copy.deepcopy(public)
            changed["environmental_conclusion"] = "Cooma has enough water."
            with self.assertRaises(CoomaRealDataPilotError):
                validate_public_receipt(changed)

    def test_redirect_or_unbounded_payload_is_rejected(self):
        def redirected(source):
            result = fake_fetch(source)
            result["final_url"] = "https://example.invalid/data"
            return result

        with tempfile.TemporaryDirectory() as temp:
            with self.assertRaisesRegex(CoomaRealDataPilotError, "outside the allowlist"):
                run_pilot(temp, human_approval=True, fetcher=redirected)

    def test_committed_public_receipt_is_valid_and_contains_real_run_metadata(self):
        receipt_path = (
            Path(__file__).resolve().parents[1]
            / "cczps_lite"
            / "output"
            / "cooma_official_real_data_pilot_receipt.json"
        )
        receipt = json.loads(receipt_path.read_text(encoding="utf-8"))
        validate_public_receipt(receipt)
        self.assertTrue(receipt["network_used"])
        self.assertEqual(receipt["source_count"], 2)
        self.assertEqual(receipt["sources"][0]["parsed_metadata"]["row_count"], 27)
        self.assertEqual(receipt["sources"][0]["parsed_metadata"]["coverage_end"], "2026-07-27")
        self.assertEqual(receipt["sources"][1]["parsed_metadata"]["state"], "EL_NINO_UNDERWAY")


if __name__ == "__main__":
    unittest.main()
