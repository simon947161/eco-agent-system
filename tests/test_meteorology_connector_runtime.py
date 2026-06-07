"""Tests for the transparent CCZPS-Lite meteorology connector."""

from __future__ import annotations

import json
import unittest
from pathlib import Path

from cczps_lite.engine.evidence_layer import meteorology_evidence_record
from cczps_lite.engine.meteorology_connector import (
    load_source_configuration,
    parse_observation,
    retrieve_observation,
)
from cczps_lite.engine.meteorology_runtime import build_meteorology_output

REPO_ROOT = Path(__file__).resolve().parents[1]


class MeteorologyConnectorRuntimeTests(unittest.TestCase):
    def test_source_configuration_loads_public_sources(self) -> None:
        config = load_source_configuration()
        self.assertEqual(
            set(config["sources"]), {"bom", "nasa_power", "noaa_cdo", "era5"}
        )
        for source in config["sources"].values():
            self.assertTrue(source["documentation_url"].startswith("http"))
            self.assertIn("field_map", source)

    def test_nasa_power_observation_is_standardised(self) -> None:
        payload = {
            "observation_timestamp": "2026-06-06T00:00:00Z",
            "T2M": 12.5,
            "PRECTOTCORR": 3.2,
            "RH2M": 78,
            "WS2M_KMH": 15,
            "WD2M": 220,
            "ALLSKY_SFC_SW_DWN": 8.4,
            "EVPTRNS": 1.1,
        }
        reading = parse_observation("nasa_power", "Batlow", payload)
        self.assertEqual(reading["observation_date"], "2026-06-06")
        self.assertEqual(reading["temperature_c"], 12.5)
        self.assertEqual(reading["rainfall_mm"], 3.2)
        self.assertEqual(reading["retrieval_status"], "success")
        self.assertEqual(reading["confidence"], "medium")

    def test_evidence_integration_is_supporting_only(self) -> None:
        reading = parse_observation(
            "nasa_power",
            "Batlow",
            {
                "observation_timestamp": "2026-06-06T00:00:00Z",
                "T2M": 12.5,
                "PRECTOTCORR": 3.2,
                "RH2M": 78,
            },
        )
        evidence = meteorology_evidence_record(reading)
        self.assertEqual(evidence["strength"], "medium")
        self.assertEqual(evidence["source"], "meteorological observation")
        self.assertIn("recent rainfall", evidence["indicators"])
        self.assertIn("no conclusion or score change", evidence["notes"])

    def test_missing_data_and_retrieval_failure_are_explicit(self) -> None:
        missing = parse_observation(
            "nasa_power",
            "Kunlun",
            {"observation_timestamp": "2026-06-06T00:00:00Z"},
        )
        self.assertEqual(missing["retrieval_status"], "missing_data")
        self.assertEqual(missing["confidence"], "low")

        failed = retrieve_observation(
            "nasa_power",
            "Iraq",
            {},
            fetcher=lambda source, request: (_ for _ in ()).throw(TimeoutError()),
        )
        self.assertEqual(failed["retrieval_status"], "retrieval_failed")
        self.assertIsNone(failed["temperature_c"])

    def test_supported_scenario_locations_are_configured(self) -> None:
        path = REPO_ROOT / "cczps_lite" / "input" / "meteorology_scenarios.json"
        with path.open("r", encoding="utf-8") as file_obj:
            scenarios = json.load(file_obj)["scenarios"]
        self.assertEqual(
            set(scenarios), {"batlow", "kunlun", "iraq", "baiyangdian_xiongan"}
        )

    def test_all_supported_scenarios_emit_meteorology_records(self) -> None:
        output = build_meteorology_output()
        self.assertEqual(len(output["scenarios"]), 4)
        for record in output["scenarios"].values():
            reading = record["meteorology_reading"]
            self.assertIn("source", reading)
            self.assertIn("observation_timestamp", reading)
            self.assertIn("retrieval_status", reading)
            self.assertIn("confidence", reading)
            self.assertEqual(reading["retrieval_status"], "not_retrieved")


if __name__ == "__main__":
    unittest.main()
