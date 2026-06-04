"""Tests for the CCZPS-Lite Validation Layer Runtime."""

from __future__ import annotations

import csv
import unittest
from pathlib import Path

from cczps_lite.engine.scenario_compare import main as run_scenario_compare
from cczps_lite.engine.validation_layer import (
    classify_validation_status,
    derive_validation_reading,
    summarize_validation_layer,
)

REPO_ROOT = Path(__file__).resolve().parents[1]


class ValidationLayerRuntimeTests(unittest.TestCase):
    """Verify evidence-aware validation scoring, gaps, and summaries."""

    def test_high_evidence_and_medium_confidence_increase_validation_score(self) -> None:
        result = derive_validation_reading(
            {"confidence_level": "medium", "validation_required": False},
            {},
            {"forcing_candidates": ["Microclimate Buffer Support"], "forcing_priority": "Medium"},
            {"evidence_strength": "High", "human_review_required": False},
        )

        self.assertGreaterEqual(result["validation_score"], 9.0)
        self.assertEqual(result["validation_status"], "Validated Enough for Concept Review")

    def test_low_evidence_reduces_validation_score(self) -> None:
        high = derive_validation_reading(
            {"confidence_level": "medium", "validation_required": False},
            {},
            {"forcing_candidates": ["Microclimate Buffer Support"], "forcing_priority": "Medium"},
            {"evidence_strength": "High", "human_review_required": False},
        )
        low = derive_validation_reading(
            {"confidence_level": "medium", "validation_required": False},
            {},
            {"forcing_candidates": ["Microclimate Buffer Support"], "forcing_priority": "Medium"},
            {"evidence_strength": "Low", "human_review_required": False},
        )

        self.assertLess(low["validation_score"], high["validation_score"])

    def test_low_evidence_plus_validation_required_flags_insufficient_or_technical(self) -> None:
        result = derive_validation_reading(
            {"confidence_level": "low", "validation_required": True},
            {},
            {"forcing_candidates": ["Heat Exposure"], "forcing_priority": "High"},
            {"evidence_strength": "Low", "human_review_required": True},
        )

        self.assertIn(result["validation_status"], {"Insufficient Evidence", "Requires Technical Validation"})
        self.assertLess(result["validation_score"], 6.0)

    def test_status_classifier_requires_technical_validation_when_needed(self) -> None:
        self.assertEqual(
            classify_validation_status(5.5, True, "Medium"),
            "Requires Technical Validation",
        )

    def test_heat_and_evaporation_forcing_adds_observation_gap(self) -> None:
        result = derive_validation_reading(
            {"confidence_level": "medium", "validation_required": False},
            {},
            {"forcing_candidates": ["Heat Exposure", "Evaporation Pressure"], "forcing_priority": "Medium"},
            {"evidence_strength": "Medium", "human_review_required": False},
        )

        self.assertIn("Need local temperature, humidity, and evaporation observation", result["validation_gaps"])

    def test_water_storage_deficit_adds_hydrological_gap(self) -> None:
        result = derive_validation_reading(
            {"confidence_level": "medium", "validation_required": False},
            {},
            {"forcing_candidates": ["Water Storage Deficit"], "forcing_priority": "Medium"},
            {"evidence_strength": "Medium", "human_review_required": False},
        )

        self.assertIn("Need hydrological or soil moisture validation", result["validation_gaps"])

    def test_fire_exposure_adds_bushfire_review_gap(self) -> None:
        result = derive_validation_reading(
            {"confidence_level": "medium", "validation_required": False},
            {},
            {"forcing_candidates": ["Fire Exposure"], "forcing_priority": "Medium"},
            {"evidence_strength": "Medium", "human_review_required": False},
        )

        self.assertIn("Need bushfire exposure and vegetation management review", result["validation_gaps"])

    def test_vegetation_stress_adds_ecological_review_gap(self) -> None:
        result = derive_validation_reading(
            {"confidence_level": "medium", "validation_required": False},
            {},
            {"forcing_candidates": ["Vegetation Stress", "Microclimate Buffer Loss"], "forcing_priority": "Medium"},
            {"evidence_strength": "Medium", "human_review_required": False},
        )

        self.assertIn("Need ecological condition and canopy-cover review", result["validation_gaps"])

    def test_validation_summary_is_non_empty_and_cautious(self) -> None:
        summary = summarize_validation_layer(
            {
                "validation_score": 6.0,
                "validation_status": "Requires Local Validation",
                "evidence_strength": "Medium",
            }
        )

        self.assertTrue(summary)
        self.assertIn("cautiously", summary)
        self.assertIn("local validation", summary)

    def test_scenario_compare_output_includes_validation_fields(self) -> None:
        run_scenario_compare()
        comparison_path = REPO_ROOT / "cczps_lite" / "output" / "comparison_matrix.csv"
        with comparison_path.open("r", encoding="utf-8", newline="") as file_obj:
            rows = list(csv.DictReader(file_obj))

        self.assertEqual(len(rows), 3)
        self.assertIn("validation_score", rows[0])
        self.assertIn("validation_status", rows[0])
        self.assertIn("validation_gaps", rows[0])
        self.assertIn("validation_summary", rows[0])


if __name__ == "__main__":
    unittest.main()
