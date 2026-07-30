import copy
import unittest

from cczps_lite.analysis.mittagang_410033_near_current_comparability import (
    evaluate_comparability,
)
from run_mittagang_410033_near_current_comparability import HISTORICAL, NEAR_CURRENT


class NearCurrentComparabilityTests(unittest.TestCase):
    def test_real_gate_blocks_unproven_equivalence(self):
        result = evaluate_comparability(
            HISTORICAL, NEAR_CURRENT, issued_at="2026-07-31T00:00:00Z"
        )
        self.assertEqual(result["gate_status"], "NOT_COMPARABLE_YET")
        self.assertEqual(result["maximum_conclusion_level"], "L1")
        self.assertIsNone(result["comparison_statistics"])
        self.assertIsNone(result["environmental_conclusion"])
        blocked = {
            row["dimension"]
            for row in result["checks"]
            if row["status"] == "BLOCKED"
        }
        self.assertEqual(
            blocked,
            {
                "measurement",
                "aggregation_window",
                "day_boundary",
                "timezone",
                "quality_semantics",
                "provenance",
            },
        )

    def test_same_station_and_unit_are_not_sufficient(self):
        result = evaluate_comparability(
            HISTORICAL, NEAR_CURRENT, issued_at="2026-07-31T00:00:00Z"
        )
        checks = {row["dimension"]: row["status"] for row in result["checks"]}
        self.assertEqual(checks["station_identity"], "PASS")
        self.assertEqual(checks["unit"], "PASS")
        self.assertNotEqual(result["gate_status"], "COMPARABLE")

    def test_gate_passes_only_when_every_dimension_is_proven(self):
        historical = copy.deepcopy(HISTORICAL)
        historical["timezone"] = "Australia/Sydney"
        current = copy.deepcopy(NEAR_CURRENT)
        current.update(
            {
                "measurement": historical["measurement"],
                "aggregation_window": historical["aggregation_window"],
                "day_boundary": historical["day_boundary"],
                "timezone": historical["timezone"],
                "quality_scheme": historical["quality_scheme"],
                "content_digest": "sha256:near-current",
                "retrieval_receipt_digest": "sha256:receipt",
            }
        )
        result = evaluate_comparability(
            historical, current, issued_at="2026-07-31T00:00:00Z"
        )
        self.assertEqual(result["gate_status"], "COMPARABLE")
        self.assertTrue(all(row["status"] == "PASS" for row in result["checks"]))
        self.assertIsNone(result["comparison_statistics"])

    def test_station_mismatch_is_a_failure(self):
        current = copy.deepcopy(NEAR_CURRENT)
        current["station_id"] = "different"
        result = evaluate_comparability(
            HISTORICAL, current, issued_at="2026-07-31T00:00:00Z"
        )
        station = next(
            row for row in result["checks"] if row["dimension"] == "station_identity"
        )
        self.assertEqual(station["status"], "FAIL")


if __name__ == "__main__":
    unittest.main()
