import json
from pathlib import Path


ROOT = Path(__file__).parents[1]
REGISTRY = ROOT / "model_registry"


def load(name):
    return json.loads((REGISTRY / name).read_text(encoding="utf-8"))


def test_registry_contract_requires_identity_provenance_licence_and_interfaces():
    contract = load("model_registry_contract.json")
    assert contract["contract_version"] == "0.1"
    assert contract["task_range"] == "Task1200-1219"
    assert {
        "model_name", "model_owner_or_maintainer", "model_version",
        "canonical_source", "source_version_or_commit", "licence_status",
        "input_contract", "output_contract", "training_data_declaration",
        "evaluation_data_declaration", "known_limitations", "uncertainty",
    }.issubset(contract["required"])


def test_registry_distinguishes_status_and_blocks_incomplete_metadata():
    contract = load("model_registry_contract.json")
    assert {"research", "experimental", "operational_service_claimed", "unknown"}.issubset(contract["model_statuses"])
    assert {"verified", "review_required", "unknown", "restricted", "incompatible"}.issubset(contract["licence_states"])
    assert "licence_review_required_or_worse" in contract["blocking_conditions"]
    assert "not execution, validation, scoring, ranking, recommendation or model admission" in contract["rule"]


def test_model_evidence_passport_preserves_challenge_and_reserves_future_work():
    contract = load("model_evidence_passport_contract.json")
    assert {"disputes", "counter_evidence", "revision", "revision_history_refs", "audit_refs"}.issubset(contract["required"])
    assert "statistical_skill_evaluation" in contract["future_sections_reserved_not_implemented"]
    assert "physical_consistency_evaluation" in contract["future_sections_reserved_not_implemented"]
    assert {"model_score", "model_rank", "model_admission"}.issubset(contract["forbidden_outputs"])


def test_synthetic_fixtures_are_complete_and_never_admit_a_model():
    fixtures = load("synthetic_model_registry_fixtures.json")
    registry = load("model_registry_contract.json")
    assert fixtures["fixture_only"] is True
    assert len(fixtures["records"]) == 2
    for record in fixtures["records"]:
        assert set(registry["required"]).issubset(record)
        assert record["registration_result"].endswith("no_admission_decision")
    assert fixtures["records"][1]["licence_status"] == "unknown"
    assert "No external model" in fixtures["boundary"]
