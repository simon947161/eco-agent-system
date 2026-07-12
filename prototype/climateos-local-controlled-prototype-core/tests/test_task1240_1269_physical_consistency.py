import json
from pathlib import Path


ROOT = Path(__file__).parents[1]
PHYSICAL = ROOT / "physical_consistency"


def load(name):
    return json.loads((PHYSICAL / name).read_text(encoding="utf-8"))


def test_catalog_contains_nine_metrics_across_all_three_physical_types():
    catalog = load("physical_metric_catalog_contract.json")
    assert catalog["task_range"] == "Task1240-1269"
    assert len(catalog["metrics"]) == 9
    assert {item["category"] for item in catalog["metrics"]} == {"conservation", "spectral", "dynamical_balance", "thermodynamic_stability"}
    assert catalog["implemented_calculations"] == []
    assert {"physical_consistency_score", "model_rank", "pass_fail", "model_admission"}.issubset(catalog["forbidden_outputs"])


def test_metric_variable_and_level_requirements_remain_explicit():
    metrics = {item["metric_id"]: item for item in load("physical_metric_catalog_contract.json")["metrics"]}
    assert set(metrics["anomaly_energy_drift"]["variables"]) == {"temperature", "specific_humidity", "geopotential", "u_wind", "v_wind"}
    assert metrics["effective_resolution"]["vertical_requirement"] == "500_hpa"
    assert metrics["mean_lapse_rate_wasserstein"]["vertical_requirement"] == "500_and_850_hpa"
    assert metrics["hydrostatic_rmse"]["vertical_requirement"] == "adjacent_pressure_level_pairs"


def test_variable_gate_requires_source_licence_grid_units_time_and_human():
    gate = load("physical_variable_gate_contract.json")
    required = set(gate["required_dataset_declarations"])
    assert {"canonical_source", "version_or_snapshot", "licence_status", "variables", "units", "pressure_levels_hpa", "grid_type", "regridding_method", "surface_pressure_method", "forecast_leads", "responsible_human"}.issubset(required)
    assert {"missing_required_variable", "unit_mismatch", "missing_or_insufficient_pressure_levels", "prediction_reference_grid_mismatch", "undeclared_regridding"}.issubset(gate["blocking_conditions"])
    assert "does not authorize data access" in gate["rule"]


def test_tolerances_are_not_invented_and_research_parameter_is_not_admission_line():
    tolerance = load("physical_tolerance_governance_contract.json")
    assert tolerance["global_default"] == "not_established"
    assert set(tolerance["other_metric_tolerances"].values()) == {"not_established"}
    effective = tolerance["effective_resolution_algorithm_parameters"]
    assert effective["energy_retention_fraction"] == 0.5
    assert effective["consecutive_wavenumbers"] == 5
    assert "not a pass/fail or admission threshold" in effective["boundary"]
    assert "automatic_pass_fail" in tolerance["forbidden_actions"]


def test_passport_preserves_missing_evidence_dispute_and_reference_sensitivity():
    passport = load("physical_consistency_evidence_passport_contract.json")
    assert {"reference_sensitivity_status", "tolerance_status", "missing_evidence", "disputes", "counter_evidence", "revision_history_refs", "audit_refs"}.issubset(passport["required"])
    assert "metric_value_from_real_data" in passport["forbidden_outputs"]
    assert "does not calculate or conclude physical consistency" in passport["rule"]


def test_synthetic_fixtures_separate_complete_declarations_from_blocked_one():
    fixtures = load("synthetic_physical_consistency_fixtures.json")
    gate = load("physical_variable_gate_contract.json")
    assert fixtures["fixture_only"] is True
    assert len(fixtures["declarations"]) == 3
    for declaration in fixtures["declarations"]:
        assert set(gate["required_dataset_declarations"]).issubset(declaration)
    assert [item["gate_result"] for item in fixtures["declarations"]] == ["declaration_complete_no_execution", "declaration_complete_no_execution", "blocked"]
    assert fixtures["passport_fixture"]["tolerance_status"] == "not_established"
    assert fixtures["passport_fixture"]["metric_evidence_items"][0]["value"] is None
    assert "No external code" in fixtures["boundary"]
