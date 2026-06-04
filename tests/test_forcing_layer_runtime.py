"""Tests for the CCZPS-Lite Forcing Layer Runtime."""

from __future__ import annotations

import unittest

from cczps_lite.engine.forcing_layer import (
    classify_forcing_priority,
    derive_forcing_candidates,
    summarize_forcing_layer,
)


class ForcingLayerRuntimeTests(unittest.TestCase):
    """Verify candidate forcing rules remain transparent and cautious."""

    def test_water_stress_with_heat_pressure_produces_core_forcings(self) -> None:
        result = derive_forcing_candidates(
            {
                "water_gradient_class": "strong_negative",
                "heat_gradient_class": "moderate_positive",
                "vegetation_gradient_class": "neutral",
                "fire_gradient_class": "neutral",
                "differential_status": "water_stress_with_heat_pressure",
            }
        )

        self.assertIn("Water Storage Deficit", result["forcing_candidates"])
        self.assertIn("Heat Exposure", result["forcing_candidates"])
        self.assertIn("Evaporation Pressure", result["forcing_candidates"])
        self.assertEqual(result["forcing_priority"], "High")

    def test_positive_heat_gradient_produces_heat_and_evaporation(self) -> None:
        result = derive_forcing_candidates(
            {
                "water_gradient_class": "neutral",
                "heat_gradient_class": "strong_positive",
                "vegetation_gradient_class": "neutral",
                "fire_gradient_class": "neutral",
                "differential_status": "mixed_or_neutral_differential",
            }
        )

        self.assertEqual(result["forcing_candidates"], ["Heat Exposure", "Evaporation Pressure"])
        self.assertEqual(result["primary_forcing"], "Heat Exposure")

    def test_negative_vegetation_gradient_produces_stress_and_buffer_loss(self) -> None:
        result = derive_forcing_candidates(
            {
                "water_gradient_class": "neutral",
                "heat_gradient_class": "neutral",
                "vegetation_gradient_class": "moderate_negative",
                "fire_gradient_class": "neutral",
                "differential_status": "mixed_or_neutral_differential",
            }
        )

        self.assertIn("Vegetation Stress", result["forcing_candidates"])
        self.assertIn("Microclimate Buffer Loss", result["forcing_candidates"])

    def test_positive_fire_gradient_produces_fire_exposure(self) -> None:
        result = derive_forcing_candidates(
            {
                "water_gradient_class": "neutral",
                "heat_gradient_class": "neutral",
                "vegetation_gradient_class": "neutral",
                "fire_gradient_class": "moderate_positive",
                "differential_status": "elevated_fire_exposure",
            }
        )

        self.assertIn("Fire Exposure", result["forcing_candidates"])
        self.assertIn("Vegetation Stress", result["forcing_candidates"])

    def test_water_advantage_with_heat_relief_produces_buffer_support(self) -> None:
        result = derive_forcing_candidates(
            {
                "water_gradient_class": "strong_positive",
                "heat_gradient_class": "strong_negative",
                "vegetation_gradient_class": "neutral",
                "fire_gradient_class": "neutral",
                "differential_status": "water_advantage_with_heat_relief",
            }
        )

        self.assertEqual(result["forcing_candidates"], ["Microclimate Buffer Support"])
        self.assertEqual(result["primary_forcing"], "Microclimate Buffer Support")

    def test_unclear_differentials_produce_mixed_unclear_forcing(self) -> None:
        result = derive_forcing_candidates(
            {
                "water_gradient_class": "neutral",
                "heat_gradient_class": "neutral",
                "vegetation_gradient_class": "neutral",
                "fire_gradient_class": "neutral",
                "differential_status": "mixed_or_neutral_differential",
            }
        )

        self.assertEqual(result["forcing_candidates"], ["Mixed / Unclear Forcing"])
        self.assertEqual(result["forcing_priority"], "Low")

    def test_priority_classification_high_for_combined_heat_fire_or_water_evaporation(self) -> None:
        self.assertEqual(classify_forcing_priority(["Fire Exposure", "Heat Exposure"]), "High")
        self.assertEqual(classify_forcing_priority(["Water Storage Deficit", "Evaporation Pressure"]), "High")

    def test_forcing_summary_is_non_empty_and_cautious(self) -> None:
        summary = summarize_forcing_layer(
            {
                "forcing_candidates": ["Heat Exposure", "Evaporation Pressure"],
                "primary_forcing": "Heat Exposure",
                "forcing_priority": "Medium",
            }
        )

        self.assertTrue(summary)
        self.assertIn("cautiously", summary)
        self.assertIn("candidate", summary)


if __name__ == "__main__":
    unittest.main()
