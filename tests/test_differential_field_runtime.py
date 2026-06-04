"""Tests for the CCZPS-Lite Differential Field Runtime."""

from __future__ import annotations

import unittest
from pathlib import Path

from cczps_lite.engine.differential_field import (
    calculate_gradient,
    classify_gradient,
    derive_differential_field,
    load_differential_context,
    summarize_differential_field,
)

REPO_ROOT = Path(__file__).resolve().parents[1]
CONTEXT_PATH = REPO_ROOT / "cczps_lite" / "input" / "differential_context.json"
REQUIRED_FIELDS = {
    "water_gradient",
    "water_gradient_class",
    "heat_gradient",
    "heat_gradient_class",
    "vegetation_gradient",
    "vegetation_gradient_class",
    "fire_gradient",
    "fire_gradient_class",
    "differential_status",
    "differential_summary",
    "reference_record_count",
}


class DifferentialFieldRuntimeTests(unittest.TestCase):
    """Verify representative differential runtime behavior."""

    def test_differential_context_json_loads_successfully(self) -> None:
        context = load_differential_context(CONTEXT_PATH)

        self.assertEqual(context["location_id"], "batlow_nsw_001")
        self.assertEqual(context["context_type"], "representative_differential_sample")
        self.assertEqual(len(context["records"]), 3)

    def test_calculate_gradient_returns_target_minus_reference(self) -> None:
        self.assertEqual(calculate_gradient(8, 6.5), 1.5)
        self.assertEqual(calculate_gradient(4, 6.5), -2.5)

    def test_classify_gradient_thresholds(self) -> None:
        self.assertEqual(classify_gradient(2.0), "strong_positive")
        self.assertEqual(classify_gradient(0.75), "moderate_positive")
        self.assertEqual(classify_gradient(0.0), "neutral")
        self.assertEqual(classify_gradient(-0.75), "moderate_negative")
        self.assertEqual(classify_gradient(-2.0), "strong_negative")

    def test_derive_differential_field_returns_required_fields(self) -> None:
        context = load_differential_context(CONTEXT_PATH)
        result = derive_differential_field(
            {
                "water_security": 9,
                "ecological_resilience": 7,
                "fire_resilience": 6,
            },
            context["records"],
        )

        self.assertTrue(REQUIRED_FIELDS.issubset(result))
        self.assertEqual(result["reference_record_count"], 3)

    def test_positive_water_and_negative_heat_can_indicate_water_advantage(self) -> None:
        context_records = [
            {
                "water_security": 5,
                "heat_exposure": 7,
                "vegetation_condition": 6,
                "fire_exposure": 6,
            }
        ]
        result = derive_differential_field(
            {
                "water_security": 8,
                "ecological_resilience": 6,
                "fire_resilience": 6,
            },
            context_records,
        )

        self.assertEqual(result["water_gradient_class"], "strong_positive")
        self.assertEqual(result["heat_gradient_class"], "strong_negative")
        self.assertEqual(result["differential_status"], "water_advantage_with_heat_relief")

    def test_negative_water_and_positive_heat_can_indicate_water_stress(self) -> None:
        context_records = [
            {
                "water_security": 7,
                "heat_exposure": 4,
                "vegetation_condition": 6,
                "fire_exposure": 6,
            }
        ]
        result = derive_differential_field(
            {
                "water_security": 4,
                "ecological_resilience": 6,
                "fire_resilience": 6,
            },
            context_records,
        )

        self.assertEqual(result["water_gradient_class"], "strong_negative")
        self.assertEqual(result["heat_gradient_class"], "strong_positive")
        self.assertEqual(result["differential_status"], "water_stress_with_heat_pressure")

    def test_summary_is_non_empty_and_cautious(self) -> None:
        result = {
            "differential_status": "mixed_or_neutral_differential",
            "water_gradient_class": "neutral",
            "heat_gradient_class": "neutral",
            "vegetation_gradient_class": "neutral",
            "fire_gradient_class": "neutral",
        }
        summary = summarize_differential_field(result)

        self.assertTrue(summary)
        self.assertIn("cautiously", summary)
        self.assertIn("representative Batlow context", summary)


if __name__ == "__main__":
    unittest.main()
