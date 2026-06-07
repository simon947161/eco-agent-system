"""Tests for the persistent meteorology time-series store."""
from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from cczps_lite.engine.meteorology_runtime import (
    TIMESERIES_SCHEMA_VERSION,
    load_timeseries,
    update_timeseries,
)


def record(
    scenario: str,
    location: str,
    date: str,
    status: str = "success",
) -> dict:
    reading = {
        "location": location,
        "observation_date": date,
        "observation_timestamp": f"{date}T00:00:00Z",
        "temperature_c": 12.5,
        "rainfall_mm": 3.2,
        "humidity_percent": 78,
        "wind_speed_kmh": 14.4,
        "wind_direction_degrees": 180,
        "solar_radiation_mj_m2": 8.4,
        "evaporation_mm": None,
        "source": "NASA POWER",
        "retrieval_status": status,
        "confidence": "medium" if status == "success" else "low",
    }
    return {
        "scenario_id": scenario,
        "location_name": location,
        "observation_date": date,
        "meteorology_reading": reading,
        "source": "NASA POWER",
        "retrieval_status": status,
        "confidence": reading["confidence"],
        "budget_guard_status": "within_budget",
        "budget_guard_summary": "Request is within configured limits.",
        "from_cache": False,
    }


def output(*records: dict) -> dict:
    return {
        "runtime": "Meteorology Connector Runtime",
        "scenarios": {
            item["scenario_id"]: item
            for item in records
        },
    }


class MeteorologyTimeseriesTests(unittest.TestCase):
    def test_missing_and_empty_files_create_versioned_store(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "timeseries.json"
            self.assertEqual(load_timeseries(path)["schema_version"], TIMESERIES_SCHEMA_VERSION)
            path.write_text("", encoding="utf-8")
            self.assertEqual(load_timeseries(path)["observations"], [])

    def test_successful_observations_append_and_sort_deterministically(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "timeseries.json"
            update_timeseries(
                output(
                    record("kunlun", "Kunlun", "2026-06-06"),
                    record("batlow", "Batlow", "2026-05-01"),
                ),
                path,
            )
            update_timeseries(
                output(record("batlow", "Batlow", "2026-06-06")),
                path,
            )
            stored = json.loads(path.read_text(encoding="utf-8"))
        keys = [
            (item["observation_date"], item["scenario_id"], item["location_name"])
            for item in stored["observations"]
        ]
        self.assertEqual(
            keys,
            [
                ("2026-05-01", "batlow", "Batlow"),
                ("2026-06-06", "batlow", "Batlow"),
                ("2026-06-06", "kunlun", "Kunlun"),
            ],
        )

    def test_repeated_refresh_does_not_duplicate_location_date(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "timeseries.json"
            reading = output(record("batlow", "Batlow", "2026-06-06"))
            update_timeseries(reading, path)
            update_timeseries(reading, path)
            stored = load_timeseries(path)
        self.assertEqual(len(stored["observations"]), 1)

    def test_non_successful_records_are_not_stored(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "timeseries.json"
            update_timeseries(
                output(
                    record("batlow", "Batlow", "2026-06-06", "missing_data"),
                    record("kunlun", "Kunlun", "2026-06-06", "retrieval_failed"),
                    record("iraq", "Iraq", "2026-06-06", "blocked_by_budget_guard"),
                ),
                path,
            )
            stored = load_timeseries(path)
        self.assertEqual(stored["observations"], [])

    def test_legacy_list_is_migrated_to_versioned_schema(self) -> None:
        legacy = [{
            "scenario_id": "batlow",
            "location_name": "Batlow",
            "observation_date": "2026-05-01",
        }]
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "timeseries.json"
            path.write_text(json.dumps(legacy), encoding="utf-8")
            stored = load_timeseries(path)
        self.assertEqual(stored["schema_version"], TIMESERIES_SCHEMA_VERSION)
        self.assertEqual(stored["observations"], legacy)

    def test_cached_success_can_fill_missing_history_once(self) -> None:
        cached = record("batlow", "Batlow", "2026-06-06")
        cached["from_cache"] = True
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "timeseries.json"
            update_timeseries(output(cached), path)
            update_timeseries(output(cached), path)
            stored = load_timeseries(path)
        self.assertEqual(len(stored["observations"]), 1)
        self.assertNotIn("from_cache", stored["observations"][0])


if __name__ == "__main__":
    unittest.main()
