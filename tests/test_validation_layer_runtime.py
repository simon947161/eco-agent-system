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
    def test_high_evidence_and_medium_confidence_increase_validation_score(self) -> None:
        result = derive_validation_reading(
            {"confidence_level": "medium", "validation_required": False}, {},
            {"forcing_candidates": ["Microclimate Buffer Support"], "forcing_priority": "Medium"},
            {"evidence_strength": "High", "human_review_required": False},
        )
        self.assertGreaterEqual(result["validation_score"], 9.0)
        self.assertEqual(result["validation_status"], "Validated Enough for Concept Review")

    def test_low_evidence_reduces_validation_score(self) -> None:
        high = derive_validation_reading(
            {"confidence_level": "medium", "validation_required": False}, {},
            {"forcing_candidates": ["Microclimate Buffer Support"], "forcing_priority": "Medium"},
            {"evidence_strength": "High", "human_review_required": False},
        )
        low = derive_validation_reading(
            {"confidence_level": "medium", "validation_required": False}, {},
            {"forcing_candidates": ["Microclimate Buffer Support"], "forcing_priority": "Medium"},
            {"evidence_strength": "Low", "human_review_required": False},
        )
        self.assertLess(low["validation_score"], high["validation_score"])

    def test_low_evidence_plus_validation_required_flags_attention(self) -> None:
        result = derive_validation_reading(
            {"confidence_level": "low", "validation_required": True}, {},
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

    def test_forcings_add_domain_validation_gaps(self) -> None:
        cases = (
            (["Heat Exposure", "Evaporation Pressure"], "Need local temperature, humidity, and evaporation observation"),
            (["Water Storage Deficit"], "Need hydrological or soil moisture validation"),
            (["Fire Exposure"], "Need bushfire exposure and vegetation management review"),
            (["Vegetation Stress"], "Need ecological condition and canopy-cover review"),
        )
        for candidates, gap in cases:
            with self.subTest(candidates=candidates):
                result = derive_validation_reading(
                    {"confidence_level": "medium", "validation_required": False}, {},
                    {"forcing_candidates": candidates, "forcing_priority": "Medium"},
                    {"evidence_strength": "Medium", "human_review_required": False},
                )
                self.assertIn(gap, result["validation_gaps"])

    def test_validation_summary_is_non_empty_and_cautious(self) -> None:
        summary = summarize_validation_layer({
            "validation_score": 6.0,
            "validation_status": "Requires Local Validation",
            "evidence_strength": "Medium",
        })
        self.assertIn("cautiously", summary)
        self.assertIn("local validation", summary)

    def test_scenario_compare_output_includes_validation_fields(self) -> None:
        run_scenario_compare()
        path = REPO_ROOT / "cczps_lite" / "output" / "comparison_matrix.csv"
        with path.open("r", encoding="utf-8", newline="") as file_obj:
            rows = list(csv.DictReader(file_obj))
        self.assertEqual(len(rows), 8)
        for field in ("validation_score", "validation_status", "validation_gaps", "validation_summary"):
            self.assertIn(field, rows[0])


if __name__ == "__main__":
    unittest.main()
