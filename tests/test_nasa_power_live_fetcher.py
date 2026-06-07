"""Tests for the explicit NASA POWER live fetch pathway."""
from __future__ import annotations
import tempfile
import unittest
from pathlib import Path
from cczps_lite.engine.meteorology_runtime import build_live_meteorology_output, build_meteorology_output, parse_nasa_power_daily


def nasa_payload(include_humidity: bool = True) -> dict:
    parameter = {"T2M": {"20260606": 12.5}, "PRECTOTCORR": {"20260606": 3.2}, "WS2M": {"20260606": 4.0}, "ALLSKY_SFC_SW_DWN": {"20260606": 8.4}}
    if include_humidity:
        parameter["RH2M"] = {"20260606": 78}
    return {"properties": {"parameter": parameter}}


class NasaPowerLiveFetcherTests(unittest.TestCase):
    def test_mocked_payload_parses_correctly(self) -> None:
        reading = parse_nasa_power_daily(nasa_payload(), "Batlow", "20260606")
        self.assertEqual(reading["temperature_c"], 12.5)
        self.assertEqual(reading["rainfall_mm"], 3.2)
        self.assertEqual(reading["wind_speed_kmh"], 14.4)
        self.assertEqual(reading["retrieval_status"], "success")

    def test_missing_variable_is_null(self) -> None:
        reading = parse_nasa_power_daily(nasa_payload(False), "Batlow", "20260606")
        self.assertIsNone(reading["humidity_percent"])

    def test_non_live_build_does_not_call_fetcher(self) -> None:
        output = build_meteorology_output()
        self.assertEqual(output["scenarios"]["batlow"]["meteorology_reading"]["retrieval_status"], "not_retrieved")

    def test_budget_guard_blocks_fetch_without_manual_approval(self) -> None:
        calls = []
        with tempfile.TemporaryDirectory() as directory:
            output = build_live_meteorology_output("20260606", fetcher=lambda request: calls.append(request) or nasa_payload(), cache_path=Path(directory) / "cache.json")
        self.assertFalse(calls)
        self.assertTrue(all(record["retrieval_status"] == "blocked_by_budget_guard" for record in output["scenarios"].values()))

    def test_cache_prevents_repeated_fetch(self) -> None:
        calls = []
        with tempfile.TemporaryDirectory() as directory:
            cache = Path(directory) / "cache.json"
            fetcher = lambda request: calls.append(request) or nasa_payload()
            build_live_meteorology_output("20260606", True, True, fetcher, cache)
            output = build_live_meteorology_output("20260606", False, True, fetcher, cache)
        self.assertEqual(len(calls), 6)
        self.assertTrue(all(record["from_cache"] for record in output["scenarios"].values()))

    def test_force_refresh_bypasses_cache(self) -> None:
        calls = []
        with tempfile.TemporaryDirectory() as directory:
            cache = Path(directory) / "cache.json"
            fetcher = lambda request: calls.append(request) or nasa_payload()
            build_live_meteorology_output("20260606", True, True, fetcher, cache)
            build_live_meteorology_output("20260606", True, True, fetcher, cache)
        self.assertEqual(len(calls), 12)

    def test_output_contains_status_and_budget_guard(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            output = build_live_meteorology_output("20260606", fetcher=lambda request: nasa_payload(), cache_path=Path(directory) / "cache.json")
        record = output["scenarios"]["batlow"]
        self.assertIn("retrieval_status", record)
        self.assertIn("budget_guard_status", record)

    def test_dashboard_uses_local_output_only(self) -> None:
        script = (Path(__file__).resolve().parents[1] / "cczps_lite" / "dashboard" / "meteorology-dashboard.js").read_text(encoding="utf-8")
        self.assertIn("../output/meteorology_evidence.json", script)
        self.assertNotIn("power.larc.nasa.gov", script)


if __name__ == "__main__":
    unittest.main()
