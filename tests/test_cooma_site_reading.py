import copy
import json
import tempfile
import unittest
from pathlib import Path

from cczps_lite.site_reading.cooma import SiteReadingError, build_site_reading, run

ROOT = Path(__file__).resolve().parents[1]


class CoomaSiteReadingTests(unittest.TestCase):
    def setUp(self):
        self.real = json.loads((ROOT / "cczps_lite/output/cooma_official_real_data_pilot_receipt.json").read_text(encoding="utf-8"))
        hydro_dir = ROOT / "cczps_lite/output/waternsw_near_current_evidence_admission"
        self.hydro = json.loads(sorted(hydro_dir.glob("*.json"))[0].read_text(encoding="utf-8"))

    def test_blocker_does_not_stop_bounded_reading(self):
        reading = build_site_reading(self.real, self.hydro, generated_at="2026-09-04T00:00:00Z")
        self.assertEqual(reading["comparison"]["status"], "NOT_COMPARABLE_YET")
        self.assertEqual(reading["evidence_maturity"], "S0")
        self.assertEqual(reading["maximum_conclusion_level"], "L1")
        self.assertTrue(reading["human_review"]["required"])
        self.assertFalse(reading["human_review"]["professional_signoff_simulated"])

    def test_rejects_input_with_environmental_conclusion(self):
        changed = copy.deepcopy(self.real); changed["environmental_conclusion"] = "unsafe"
        with self.assertRaises(SiteReadingError):
            build_site_reading(changed, self.hydro, generated_at="2026-09-04T00:00:00Z")

    def test_run_writes_reading_passport_receipt_and_founder_view(self):
        with tempfile.TemporaryDirectory() as temp:
            paths = run(temp, repo_root=ROOT, generated_at="2026-09-04T00:00:00Z")
            self.assertEqual(set(paths), {"reading", "passport", "receipt", "markdown"})
            self.assertTrue(all(path.exists() for path in paths.values()))
            receipt = json.loads(paths["receipt"].read_text(encoding="utf-8"))
            self.assertFalse(receipt["network_used"])
            self.assertIn("TREND_DEFERRED", receipt["limitations"])


if __name__ == "__main__":
    unittest.main()

