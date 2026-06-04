"""Tests for the EcoEngine v1.9.2b compatibility bridge."""

from __future__ import annotations

import unittest
from pathlib import Path

from cczps_lite.integration.ecoengine_v192b_adapter import (
    load_ecoengine_record,
    map_ecoengine_to_runtime_fields,
    summarize_ecoengine_bridge,
)

REPO_ROOT = Path(__file__).resolve().parents[1]
SAMPLE_PATH = REPO_ROOT / "cczps_lite" / "input" / "ecoengine_sample_output.json"


class EcoEngineV192bBridgeTests(unittest.TestCase):
    """Verify tolerant mapping from EcoEngine-style records to runtime fields."""

    def test_sample_ecoengine_record_loads_successfully(self) -> None:
        record = load_ecoengine_record(SAMPLE_PATH)

        self.assertEqual(record["source"], "ecoengine_v1_9_2b_sample")
        self.assertEqual(record["location_id"], "batlow_nsw_001")
        self.assertIn("runtime_fields", record)

    def test_nested_runtime_fields_map_correctly(self) -> None:
        record = load_ecoengine_record(SAMPLE_PATH)
        mapped = map_ecoengine_to_runtime_fields(record)

        self.assertEqual(mapped["risk_index"], 4.1)
        self.assertEqual(mapped["water_balance_signal"], "watch")
        self.assertEqual(mapped["ecological_signal"], "moderate")
        self.assertEqual(mapped["evaporation_pressure"], "high")
        self.assertEqual(mapped["confidence_level"], "medium")
        self.assertTrue(mapped["validation_required"])

    def test_root_level_fallback_fields_map_correctly(self) -> None:
        record = {
            "risk_index": 3.8,
            "water_balance_signal": "stressed",
            "ecological_resilience": "limited",
            "evaporation_pressure": "medium",
            "confidence_level": "medium",
            "validation_required": False,
        }
        mapped = map_ecoengine_to_runtime_fields(record)

        self.assertEqual(mapped["risk_index"], 3.8)
        self.assertEqual(mapped["water_balance_signal"], "stressed")
        self.assertEqual(mapped["ecological_signal"], "limited")
        self.assertEqual(mapped["evaporation_pressure"], "medium")
        self.assertEqual(mapped["confidence_level"], "medium")
        self.assertFalse(mapped["validation_required"])

    def test_instability_pathway_fallback_infers_dry_runtime_signals(self) -> None:
        record = {
            "instability_pathways": [
                "evaporation_dominated",
                "wind_exposed_dry",
            ]
        }
        mapped = map_ecoengine_to_runtime_fields(record)

        self.assertEqual(mapped["water_balance_signal"], "watch")
        self.assertEqual(mapped["evaporation_pressure"], "high")

    def test_soil_degradation_fallback_infers_limited_ecological_signal(self) -> None:
        record = {"instability_pathways": ["soil_degradation"]}
        mapped = map_ecoengine_to_runtime_fields(record)

        self.assertEqual(mapped["ecological_signal"], "limited")

    def test_low_confidence_triggers_validation_required(self) -> None:
        record = {
            "confidence_level": "low",
            "validation_required": False,
        }
        mapped = map_ecoengine_to_runtime_fields(record)

        self.assertTrue(mapped["validation_required"])

    def test_bridge_summary_contains_regime_or_instability_information(self) -> None:
        record = load_ecoengine_record(SAMPLE_PATH)
        summary = summarize_ecoengine_bridge(record)

        self.assertTrue(summary)
        self.assertIn("dry_inland", summary)
        self.assertIn("evaporation_dominated", summary)
        self.assertIn("validation_required=True", summary)


if __name__ == "__main__":
    unittest.main()
