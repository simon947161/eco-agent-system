import copy
import json
import math
from pathlib import Path

import pytest

from statistical_evaluation import StatisticalEvaluationBlocked, evaluate_synthetic_slice


ROOT = Path(__file__).parents[1]
STATISTICAL = ROOT / "statistical_evaluation"


def fixtures():
    source = json.loads((STATISTICAL / "synthetic_statistical_fixtures.json").read_text(encoding="utf-8"))
    result = []
    for case in source["cases"]:
        result.append({**source["shared"], **case, "fixture_only": source["fixture_only"]})
    return result


def test_contract_is_bounded_and_forbids_score_rank_and_admission():
    contract = json.loads((STATISTICAL / "statistical_evaluation_contract.json").read_text(encoding="utf-8"))
    assert contract["task_range"] == "Task1220-1239"
    assert {"latitude_weighted_mse", "latitude_weighted_rmse", "latitude_weighted_mae", "latitude_weighted_bias", "latitude_weighted_acc"} == set(contract["implemented_metrics"])
    assert {"overall_model_score", "model_rank", "better_model_claim", "model_admission"}.issubset(contract["forbidden_outputs"])


def test_all_synthetic_cases_calculate_separately_without_ranking():
    calculable = [item for item in fixtures() if item["expected_result"] == "synthetic_calculation_evidence"]
    results = [evaluate_synthetic_slice(item) for item in calculable]
    assert len(results) == 2
    for result in results:
        assert result["evidence_state"] == "synthetic_calculation_evidence"
        assert set(result["metrics"]) == {"latitude_weighted_mse", "latitude_weighted_rmse", "latitude_weighted_mae", "latitude_weighted_bias", "latitude_weighted_acc"}
        assert "rank" not in result and "score" not in result and "admission" not in result


def test_climatology_baseline_records_undefined_acc_instead_of_inventing_a_value():
    climatology = next(item for item in fixtures() if item["baseline_type"] == "synthetic_climatology")
    assert climatology["expected_result"] == "blocked_acc_zero_anomaly_variance"
    with pytest.raises(StatisticalEvaluationBlocked, match="ACC anomaly variance"):
        evaluate_synthetic_slice(climatology)


def test_rmse_is_square_root_of_aggregated_mse_and_hash_is_reproducible():
    payload = fixtures()[0]
    first = evaluate_synthetic_slice(payload)
    second = evaluate_synthetic_slice(copy.deepcopy(payload))
    assert math.isclose(first["metrics"]["latitude_weighted_rmse"] ** 2, first["metrics"]["latitude_weighted_mse"])
    assert first["input_sha256"] == second["input_sha256"]


@pytest.mark.parametrize(
    ("change", "message"),
    [
        ({"fixture_only": False}, "Only fixture_only"),
        ({"forecast_units": "different_unit"}, "units must match"),
        ({"forecast_values": [1.0]}, "dimensions must match"),
        ({"forecast_values": []}, "must not be empty"),
        ({"forecast_values": [float("nan"), 1.0, 2.0, 3.0]}, "must be finite"),
        ({"latitudes": [-35.0, -36.0, -37.0, 95.0]}, "between -90 and 90"),
        ({"evaluation_period": {"start": "2000-01-15", "end": "2000-02-02"}}, "must not overlap"),
        ({"leakage_declaration": ""}, "leakage declaration"),
        ({"responsible_human": ""}, "responsible human"),
    ],
)
def test_unauthorized_or_invalid_inputs_are_blocked(change, message):
    payload = fixtures()[0]
    payload.update(change)
    with pytest.raises(StatisticalEvaluationBlocked, match=message):
        evaluate_synthetic_slice(payload)


def test_acc_requires_nonzero_anomaly_variance():
    payload = fixtures()[0]
    payload["forecast_values"] = payload["climatology_values"].copy()
    with pytest.raises(StatisticalEvaluationBlocked, match="ACC anomaly variance"):
        evaluate_synthetic_slice(payload)
