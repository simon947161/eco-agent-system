"""Tests for the bounded WeatherBench-X reference adapter prototype."""

from __future__ import annotations

import copy
import math
import unittest
from pathlib import Path

from cczps_lite.integration.weatherbench_synthetic_adapter import (
    RESULT_CLASSIFICATION,
    SyntheticAdapterContractError,
    evaluate_synthetic_case,
    load_synthetic_case,
)

REPO_ROOT = Path(__file__).resolve().parents[1]
FIXTURE_PATH = REPO_ROOT / "cczps_lite" / "input" / "weatherbench_tiny_synthetic_case.json"


class WeatherBenchSyntheticAdapterTests(unittest.TestCase):
    def setUp(self) -> None:
        self.record = load_synthetic_case(FIXTURE_PATH)

    def test_tiny_fixture_produces_expected_weighted_metrics(self) -> None:
        result = evaluate_synthetic_case(self.record)

        self.assertTrue(math.isclose(result["metrics"]["latitude_weighted_rmse"], math.sqrt(2)))
        self.assertTrue(math.isclose(result["metrics"]["latitude_weighted_mae"], 1.25))
        self.assertTrue(math.isclose(result["metrics"]["latitude_weighted_bias"], 0.5))
        self.assertEqual(result["grid_point_count"], 6)

    def test_result_cannot_be_described_as_a_weatherbench_score(self) -> None:
        result = evaluate_synthetic_case(self.record)

        self.assertEqual(result["result_classification"], RESULT_CLASSIFICATION)
        self.assertFalse(result["upstream_code_executed"])
        self.assertFalse(result["external_data_accessed"])
        self.assertFalse(result["network_or_cloud_used"])
        self.assertEqual(result["model_admission_state"], "NOT_EVALUATED")
        self.assertTrue(result["human_review_required"])

    def test_non_synthetic_data_are_blocked(self) -> None:
        record = copy.deepcopy(self.record)
        record["data_classification"] = "REAL_DATA"

        with self.assertRaisesRegex(SyntheticAdapterContractError, "SYNTHETIC_ONLY"):
            evaluate_synthetic_case(record)

    def test_external_origin_is_blocked(self) -> None:
        record = copy.deepcopy(self.record)
        record["origin"] = "REMOTE_URL"

        with self.assertRaisesRegex(SyntheticAdapterContractError, "repository-inline"):
            evaluate_synthetic_case(record)

    def test_fixture_loader_rejects_paths_outside_repository_input(self) -> None:
        with self.assertRaisesRegex(SyntheticAdapterContractError, "cczps_lite/input"):
            load_synthetic_case(REPO_ROOT / "README.md")

    def test_url_or_any_unknown_field_is_blocked(self) -> None:
        record = copy.deepcopy(self.record)
        record["url"] = "https://example.invalid/forecast.zarr"

        with self.assertRaisesRegex(SyntheticAdapterContractError, "Unknown fields"):
            evaluate_synthetic_case(record)

    def test_grid_shape_mismatch_is_blocked(self) -> None:
        record = copy.deepcopy(self.record)
        record["forecast_values"] = record["forecast_values"][:-1]

        with self.assertRaisesRegex(SyntheticAdapterContractError, "row-major grid size"):
            evaluate_synthetic_case(record)

    def test_time_and_lead_mismatch_is_blocked(self) -> None:
        record = copy.deepcopy(self.record)
        record["lead_time_hours"] = 12

        with self.assertRaisesRegex(SyntheticAdapterContractError, "does not match"):
            evaluate_synthetic_case(record)

    def test_variable_and_unit_contract_is_fixed(self) -> None:
        record = copy.deepcopy(self.record)
        record["unit"] = "degC"

        with self.assertRaisesRegex(SyntheticAdapterContractError, "Unit mismatch"):
            evaluate_synthetic_case(record)


if __name__ == "__main__":
    unittest.main()
