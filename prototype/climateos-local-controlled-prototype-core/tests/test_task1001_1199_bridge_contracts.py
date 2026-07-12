import json
from pathlib import Path


ROOT = Path(__file__).parents[1]
CONTRACTS = ROOT / "bridge_contracts"


def load(name):
    return json.loads((CONTRACTS / name).read_text(encoding="utf-8"))


def test_all_bridge_contracts_are_versioned_and_bounded():
    names = sorted(path.name for path in CONTRACTS.glob("*_contract.json"))
    assert len(names) == 7
    for name in names:
        contract = load(name)
        assert contract["contract_version"] == "1.0"
        assert contract["required"]


def test_node_and_spatial_contracts_preserve_local_to_regional_meaning():
    nodes = load("node_identity_contract.json")
    spatial = load("spatial_evidence_contract.json")
    assert nodes["node_types"] == ["local", "project", "ngo", "regional"]
    assert "legal_boundary" in spatial["forbidden_inferences"]
    assert "spatial_uncertainty" in spatial["required"]


def test_observation_tiers_cannot_promote_automatically():
    contract = load("observation_tier_contract.json")
    assert contract["tiers"] == ["casual", "structured", "professional", "validated"]
    assert "No tier is promoted automatically" in contract["rule"]
    assert "named_human_reviewer" in contract["promotion_requires"]


def test_source_and_evidence_asset_contracts_keep_dispute_and_rights():
    source = load("source_admission_contract.json")
    asset = load("evidence_asset_lifecycle_contract.json")
    assert "disputed" in source["admission_states"]
    assert "attach_counter_evidence" in asset["events"]
    assert "financial_asset" in asset["forbidden_claims"]


def test_carbon_esg_contract_cannot_create_governance_conclusions():
    contract = load("carbon_esg_translation_contract.json")
    assert "method_version" in contract["required"]
    assert "counter_evidence" in contract["esg_plus_requires"]
    assert {"compliance", "assurance", "certification", "financial_advice"}.issubset(contract["forbidden_claims"])


def test_scientific_readiness_stops_before_task1200():
    contract = load("scientific_input_readiness_contract.json")
    assert "physical_consistency_evaluation" in contract["task1200_gate_requires"]
    assert "cannot start Task1200" in contract["rule"]


def test_fixture_is_synthetic_and_declares_human_responsibility():
    fixture = load("synthetic_bridge_fixture.json")
    assert fixture["fixture_only"] is True
    assert fixture["node"]["responsibility_status"] == "declared_unverified"
    assert fixture["observation"]["tier"] == "casual"
    assert "No real source" in fixture["boundary"]
