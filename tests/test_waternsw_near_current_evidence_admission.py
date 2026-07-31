import json
import unittest

from cczps_lite.integration.waternsw_near_current_evidence_admission import (
    WaterNSWAdmissionError,
    admit_response,
    blocked_receipt,
)


class WaterNSWNearCurrentAdmissionTests(unittest.TestCase):
    def setUp(self):
        self.retrieval = {
            "source_url": "https://api.example.waternsw.invalid/water-data",
            "retrieved_at": "2026-07-28T09:45:00Z",
            "http_status": 200,
            "station_id": "410033",
            "parameter": "FlowRate",
            "unit": "ML/day",
        }

    def test_missing_raw_response_is_a_block_not_an_admission(self):
        receipt = blocked_receipt(
            attempted_at="2026-07-31T00:00:00Z",
            reason="exact response bytes unavailable",
        )
        self.assertEqual(
            receipt["admission_status"],
            "ADMISSION_BLOCKED_MISSING_RAW_RESPONSE",
        )
        self.assertIsNone(receipt["response_content_digest"])
        self.assertIsNone(receipt["environmental_conclusion"])
        self.assertFalse(receipt["trend_assessment"]["performed"])

    def test_empty_response_cannot_be_reconstructed_from_summary(self):
        with self.assertRaises(WaterNSWAdmissionError):
            admit_response(
                b"",
                self.retrieval,
                admitted_at="2026-07-31T00:00:00Z",
            )

    def test_exact_json_response_can_be_admitted_only_to_l1(self):
        raw = json.dumps(
            {"station": "410033", "parameter": "FlowRate", "value": 194.296},
            separators=(",", ":"),
        ).encode()
        receipt = admit_response(
            raw,
            self.retrieval,
            admitted_at="2026-07-31T00:00:00Z",
        )
        self.assertEqual(receipt["admission_status"], "L1_EVIDENCE_ADMITTED")
        self.assertTrue(
            receipt["source"]["response_content_digest"].startswith("sha256:")
        )
        self.assertTrue(receipt["retrieval_receipt_digest"].startswith("sha256:"))
        self.assertEqual(receipt["maximum_conclusion_level"], "L1")
        self.assertEqual(receipt["measurement_semantics"], "UNRESOLVED")
        self.assertIsNone(receipt["comparison_statistics"])
        self.assertIsNone(receipt["environmental_conclusion"])

    def test_wrong_station_is_rejected(self):
        retrieval = {**self.retrieval, "station_id": "different"}
        with self.assertRaises(WaterNSWAdmissionError):
            admit_response(
                b'{"value":1}',
                retrieval,
                admitted_at="2026-07-31T00:00:00Z",
            )


if __name__ == "__main__":
    unittest.main()
