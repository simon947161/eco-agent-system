import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1] / "regional_fitness"


def load(name):
    return json.loads((ROOT / name).read_text(encoding="utf-8"))


def test_two_authorized_regions_are_explicit_and_not_global_proxies():
    contract = load("region_registry_contract.json")
    regions = {item["region_id"]: item for item in contract["regions"]}
    assert set(regions) == {"CN-XJ-KARAMAY", "AU-NSW-SOUTH-EAST-TABLELANDS"}
    assert "must not represent all Xinjiang or China" in regions["CN-XJ-KARAMAY"]["climate_context"]
    assert regions["AU-NSW-SOUTH-EAST-TABLELANDS"]["human_review_required"] is True


def test_event_contract_keeps_regional_and_compound_boundaries():
    contract = load("extreme_event_contract.json")
    events = {item["event_type"]: item for item in contract["event_families"]}
    assert len(events) == 6
    assert events["dust_or_sand"]["region_restriction"] == ["CN-XJ-KARAMAY"]
    assert "not automatically" in events["hot_dry_windy_compound"]["prohibited_inference"]
    assert contract["automatic_score_rank_or_admission"] is False


def test_warning_threshold_cannot_become_admission_threshold():
    contract = load("threshold_governance_contract.json")
    assert "operational warnings are not model admission thresholds" in contract["rules"]
    assert contract["default_status"] == "not_established"
    assert contract["human_review_required"] is True


def test_sample_gate_has_no_invented_universal_minimum():
    contract = load("sample_nonstationarity_ood_gate_contract.json")
    assert contract["numeric_universal_minimum"] is None
    assert "independent_event_count" in contract["sample_fields"]
    assert "test-period threshold tuning" in contract["blocked_practices"]
    assert contract["automatic_fitness_conclusion"] is False


def test_ood_dimensions_cover_region_time_intensity_and_reference():
    contract = load("sample_nonstationarity_ood_gate_contract.json")
    for dimension in ("spatial", "climate_regime", "temporal", "event_magnitude", "reference_product"):
        assert dimension in contract["ood_dimensions"]
    assert set(contract["ood_statuses"]) == {"in_distribution", "ood_suspected", "ood_confirmed", "cannot_determine"}


def test_passport_has_evidence_not_decision_fields():
    contract = load("regional_fitness_evidence_passport_contract.json")
    assert contract["decision_fields"] == []
    assert "licence_and_cost_review" in contract["required_sections"]
    assert "model ranking" in contract["prohibited_outputs"]


def test_controlled_sources_are_official_candidates_and_no_values_are_invented():
    registry = load("controlled_source_registry.json")
    providers = {item["provider"] for item in registry["sources"]}
    assert "Australian Bureau of Meteorology" in providers
    assert "NSW Government AdaptNSW" in providers
    assert "China Meteorological Administration data service" in providers
    assert registry["environmental_observation_values_ingested"] == 0
    assert all("licence_status" in source for source in registry["sources"])


def test_synthetic_fixtures_block_missing_threshold_sample_and_dust_variable():
    fixtures = load("tiny_synthetic_regional_fitness_fixtures.json")
    assert fixtures["fixture_boundary"].startswith("synthetic_only")
    assert all(item["expected_gate"].startswith("blocked") for item in fixtures["fixtures"])
    dust = next(item for item in fixtures["fixtures"] if item["event_type"] == "dust_or_sand")
    assert "visibility_or_weather_phenomenon_code" not in dust["available_variables"]


def test_repository_agent_constitution_contains_founder_cost_gate():
    repository_root = Path(__file__).resolve().parents[3]
    agents = (repository_root / "AGENTS.md").read_text(encoding="utf-8")
    policy = (repository_root / "00_PROJECT_CONTROL" / "FOUNDER_RESOURCE_AND_COST_CONTROL_PRINCIPLE.md").read_text(encoding="utf-8")
    assert "Do not purchase, subscribe" in agents
    assert "Silence is not approval" in policy
    assert "Real data should be used" in policy
