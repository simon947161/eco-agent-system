"""Tests for the CCZPS-Lite multi-scale scenario validation pack."""

from __future__ import annotations

import csv
import unittest
from pathlib import Path

from cczps_lite.engine.scenario_compare import main as run_scenario_compare
from cczps_lite.engine.scenario_validation_pack import derive_watershed_continuity

REPO_ROOT = Path(__file__).resolve().parents[1]


class MultiScaleValidationPackTests(unittest.TestCase):
    def test_watershed_continuity_bands(self) -> None:
        point_ids = ["source", "wetland", "urban"]
        high_rows = [
            {"scenario_id": point, "water_security": 7, "ecological_resilience": 7, "evidence_strength": "Medium"}
            for point in point_ids
        ]
        moderate_rows = [
            {"scenario_id": "source", "water_security": 8, "ecological_resilience": 8, "evidence_strength": "Medium"},
            {"scenario_id": "wetland", "water_security": 6, "ecological_resilience": 7, "evidence_strength": "Medium"},
            {"scenario_id": "urban", "water_security": 5, "ecological_resilience": 6, "evidence_strength": "Low"},
        ]
        fragmented_rows = [
            {"scenario_id": point, "water_security": 3, "ecological_resilience": 5, "evidence_strength": "Low"}
            for point in point_ids
        ]
        self.assertEqual(derive_watershed_continuity(high_rows, point_ids), "High Continuity")
        self.assertEqual(derive_watershed_continuity(moderate_rows, point_ids), "Moderate Continuity")
        self.assertEqual(derive_watershed_continuity(fragmented_rows, point_ids), "Fragmented Continuity")

    def test_generated_pack_contains_all_validation_contexts(self) -> None:
        run_scenario_compare()
        output_dir = REPO_ROOT / "cczps_lite" / "output"
        with (output_dir / "comparison_matrix.csv").open("r", encoding="utf-8", newline="") as file_obj:
            rows = list(csv.DictReader(file_obj))
        contexts = {row["validation_context"] for row in rows}
        self.assertIn("Scenario A — Batlow Energy Resilience", contexts)
        self.assertIn("Scenario B — Kunlun Eco-Water System", contexts)
        self.assertIn("Scenario C — Iraq Agriculture Recovery", contexts)
        self.assertIn("Scenario D1 — Wutai Mountain Headwaters", contexts)
        self.assertIn("Scenario D2 — Baiyangdian Wetland Core", contexts)
        self.assertIn("Scenario D3 — Xiong'an and Downstream Region", contexts)

        pack_text = (output_dir / "scenario_validation_pack.md").read_text(encoding="utf-8")
        for phrase in (
            "Scenario inputs",
            "Evidence assumptions",
            "Runtime outputs",
            "Validation results",
            "Prioritised response",
            "Limitations",
            "human review required",
            "Watershed Continuity Reading",
        ):
            self.assertIn(phrase, pack_text)


if __name__ == "__main__":
    unittest.main()
