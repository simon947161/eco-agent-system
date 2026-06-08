"""Tests for conservative meteorology trend readings."""
from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from cczps_lite.engine.meteorology_runtime import (
    TREND_MINIMUM_OBSERVATIONS,
    build_trend_output,
    write_trend_outputs,
)


def observation(date: str, **values) -> dict:
    reading = {
        "temperature_c": values.get("temperature_c"),
        "rainfall_mm": values.get("rainfall_mm"),
        "humidity_percent": values.get("humidity_percent"),
        "wind_speed_kmh": values.get("wind_speed_kmh"),
        "solar_radiation_mj_m2": values.get("solar_radiation_mj_m2"),
        "evaporation_mm": values.get("evaporation_mm"),
    }
    return {
        "scenario_id": "batlow",
        "location_name": "Batlow",
        "observation_date": date,
        "retrieval_status": "success",
        "meteorology_reading": reading,
    }


def trend_for(variable: str, records: list[dict]) -> dict:
    output = build_trend_output({"observations": records})
    return output["scenarios"]["batlow"]["variables"][variable]


class MeteorologyTrendTests(unittest.TestCase):
    def test_increasing_trend_is_rule_based(self) -> None:
        trend = trend_for("temperature_c", [
            observation("2026-01-01", temperature_c=10),
            observation("2026-01-02", temperature_c=11),
            observation("2026-01-03", temperature_c=12),
        ])
        self.assertEqual(trend["trend_classification"], "increasing")
        self.assertEqual(trend["sample_count"], TREND_MINIMUM_OBSERVATIONS)
        self.assertEqual(trend["change"], 2.0)

    def test_decreasing_trend_is_rule_based(self) -> None:
        trend = trend_for("rainfall_mm", [
            observation("2026-01-01", rainfall_mm=8),
            observation("2026-01-02", rainfall_mm=5),
            observation("2026-01-03", rainfall_mm=2),
        ])
        self.assertEqual(trend["trend_classification"], "decreasing")
        self.assertEqual(trend["change"], -6.0)

    def test_stable_trend_uses_variable_threshold(self) -> None:
        trend = trend_for("wind_speed_kmh", [
            observation("2026-01-01", wind_speed_kmh=10),
            observation("2026-01-02", wind_speed_kmh=10.4),
            observation("2026-01-03", wind_speed_kmh=10.8),
        ])
        self.assertEqual(trend["trend_classification"], "stable")

    def test_insufficient_data_is_explicit(self) -> None:
        trend = trend_for("humidity_percent", [
            observation("2026-01-01", humidity_percent=60),
            observation("2026-01-02", humidity_percent=62),
        ])
        self.assertEqual(trend["trend_classification"], "insufficient_data")
        self.assertEqual(trend["sample_count"], 2)

    def test_missing_data_is_explicit(self) -> None:
        trend = trend_for("solar_radiation_mj_m2", [
            observation("2026-01-01"),
            observation("2026-01-02"),
            observation("2026-01-03"),
        ])
        self.assertEqual(trend["trend_classification"], "missing_data")
        self.assertEqual(trend["sample_count"], 0)

    def test_non_successful_observations_are_ignored(self) -> None:
        records = [
            observation("2026-01-01", temperature_c=10),
            observation("2026-01-02", temperature_c=11),
            observation("2026-01-03", temperature_c=12),
        ]
        records[-1]["retrieval_status"] = "missing_data"
        output = build_trend_output({"observations": records})
        self.assertEqual(output["scenarios"]["batlow"]["sample_count"], 2)
        self.assertEqual(
            output["scenarios"]["batlow"]["variables"]["temperature_c"]["trend_classification"],
            "insufficient_data",
        )

    def test_trend_outputs_include_json_and_markdown_reports(self) -> None:
        output = build_trend_output({"observations": [
            observation("2026-01-01", temperature_c=10),
            observation("2026-01-02", temperature_c=11),
            observation("2026-01-03", temperature_c=12),
        ]})
        with tempfile.TemporaryDirectory() as directory:
            json_path = Path(directory) / "meteorology_trends.json"
            md_path = Path(directory) / "meteorology_trends.md"
            write_trend_outputs(output, json_path, md_path)
            self.assertIn("Meteorology Trend Reading", md_path.read_text(encoding="utf-8"))
            self.assertIn("temperature_c", json_path.read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main()
