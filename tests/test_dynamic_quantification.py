"""Real archived replay plus explicitly mutated negative software fixtures."""
import copy
import hashlib
import json
import unittest

from cczps_lite.integration import dynamic_quantification as dq


class DynamicQuantificationTest(unittest.TestCase):
    def setUp(self):
        self.request = json.loads((dq.EVIDENCE_DIR / "request.json").read_text(encoding="utf-8"))
        self.receipt = json.loads((dq.EVIDENCE_DIR / "noaa-receipt.json").read_text(encoding="utf-8"))
        self.raw = (dq.EVIDENCE_DIR / "noaa-daily.json").read_bytes()

    def run_request(self, **changes):
        return dq.run_agent({**self.request, **changes}, self.raw, self.receipt)

    def mutate_rows(self, transform):
        rows = json.loads(self.raw)
        transform(rows)
        raw = json.dumps(rows).encode()
        receipt = {**self.receipt, "sha256": hashlib.sha256(raw).hexdigest()}
        # Synthetic mutation with a test-only receipt; not live evidence.
        return dq.run_agent(self.request, raw, receipt)

    def test_real_replay_semantics_and_trace(self):
        result = dq.replay()
        self.assertEqual(result["status"], "OBSERVATION_DESCRIPTIVE_SLICE_PASSED")
        self.assertAlmostEqual(result["result"]["means"]["daily_max_temperature"], 80 / 3)
        self.assertAlmostEqual(result["result"]["means"]["daily_mean_wind_speed"], 4.7 / 3)
        self.assertEqual(result["trace"], ["get_environmental_context", "query_observations", "run_verified_model", "check_regulatory_context", "generate_evidence_report"])
        self.assertNotIn("observation_timestamp", result["observations"]["records"][0])
        self.assertEqual(result["regulatory"]["legal_effect"], "NONE")

    def test_request_refusals_have_no_results(self):
        cases = [({"variables": {"daily_max_temperature": "K"}}, "UNIT_OR_VARIABLE_MISMATCH"),
                 ({"coordinates": [148.15, -35.52]}, "SPACE_MISMATCH"),
                 ({"crs": "EPSG:3857"}, "SPACE_MISMATCH"),
                 ({"time_basis": "UTC"}, "TIME_BASIS_MISMATCH"),
                 ({"start_date": "2025-05-10"}, "INVALID_TIME"),
                 ({"start_date": "bad"}, "INVALID_TIME"),
                 ({"start_date": "2025-04-30"}, "INSUFFICIENT_TEMPORAL_COVERAGE"),
                 ({"end_date": "2025-05-02"}, "INSUFFICIENT_EVIDENCE_MIN_3_DAYS"),
                 ({"model_id": "methane_inversion"}, "MODEL_NOT_AUTHORIZED"),
                 ({"source_id": "methane_d3"}, "DATA_NOT_READY_OR_SOURCE_NOT_ADMITTED"),
                 ({"permission": "write"}, "PERMISSION_DENIED")]
        for changes, reason in cases:
            with self.subTest(changes=changes):
                output = self.run_request(**changes)
                self.assertEqual(output.get("reason"), reason)
                self.assertNotIn("result", output)

    def test_missing_and_tampered_data(self):
        self.assertEqual(dq.run_agent(self.request)["reason"], "MISSING_DATA")
        self.assertEqual(dq.run_agent(self.request, self.raw + b" ", self.receipt)["reason"], "HASH_MISMATCH")
        receipt = {**self.receipt, "rights_review": "UNKNOWN"}
        self.assertEqual(dq.run_agent(self.request, self.raw, receipt)["reason"], "SOURCE_RIGHTS_NOT_ADMITTED")

    def test_quality_missing_nonfinite_duplicates_and_wrong_station(self):
        for key, value, expected in [("TMAX", None, "MISSING_OR_INVALID_DATA"),
                                     ("AWND", "NaN", "MISSING_OR_INVALID_DATA"),
                                     ("AWND", "inf", "MISSING_OR_INVALID_DATA"),
                                     ("AWND", -1, "RANGE_CHECK_FAILED"),
                                     ("TMAX_ATTRIBUTES", ",D,W", "QUALITY_FLAG_REJECTED"),
                                     ("AWND_ATTRIBUTES", None, "QUALITY_FLAGS_MISSING"),
                                     ("STATION", "other", "STATION_MISMATCH")]:
            with self.subTest(key=key, value=value):
                output = self.mutate_rows(lambda rows: rows[0].__setitem__(key, value))
                self.assertEqual(output["reason"], expected)
                self.assertNotIn("result", output)
        self.assertEqual(self.mutate_rows(lambda rows: rows.append(copy.deepcopy(rows[0])))["reason"], "DUPLICATE_DAY")
        self.assertEqual(self.mutate_rows(lambda rows: rows.pop())["reason"], "INSUFFICIENT_TEMPORAL_COVERAGE")

    def test_scenarios_never_silently_compute(self):
        with self.assertRaisesRegex(dq.Refusal, "SCENARIO_MODEL_NOT_ADMITTED"):
            dq.compare_scenarios(self.request, self.request)


if __name__ == "__main__":
    unittest.main()
