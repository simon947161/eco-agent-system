import pytest
from fastapi.testclient import TestClient

from climateos_local_prototype.api import assert_allowed_host, create_app
from climateos_local_prototype.repository import PrototypeRepository
from climateos_local_prototype.seed import seed_database


@pytest.fixture()
def client(tmp_path):
    db_path = tmp_path / "prototype.sqlite3"
    repository = PrototypeRepository(db_path)
    seed_database(repository)
    return TestClient(create_app(db_path))


def test_localhost_binding_guard_blocks_public_host():
    assert assert_allowed_host("127.0.0.1") == "127.0.0.1"
    assert assert_allowed_host("localhost") == "localhost"
    with pytest.raises(ValueError):
        assert_allowed_host("0.0.0.0")


def test_health_boundary_is_candidate_non_operational(client):
    response = client.get("/api/health")
    assert response.status_code == 200
    payload = response.json()
    assert payload["localhost_only"] is True
    assert payload["operational"] is False
    assert payload["boundary_label"] == "Prototype / Candidate / Non-Operational"


def test_candidate_crud_and_validation(client):
    create_response = client.post(
        "/api/candidates",
        json={
            "record_type": "source_candidate",
            "title": "Manual source candidate",
            "summary": "Manually entered candidate only.",
            "risk_flags": ["RF-001"],
        },
    )
    assert create_response.status_code == 201
    record = create_response.json()
    assert record["status"] == "Draft Candidate"

    read_response = client.get(f"/api/candidates/{record['id']}")
    assert read_response.status_code == 200
    assert read_response.json()["title"] == "Manual source candidate"

    invalid_response = client.post(
        "/api/candidates",
        json={"record_type": "source_candidate", "title": "No", "status": "Certified"},
    )
    assert invalid_response.status_code == 422


def test_human_review_transition_requires_reason(client):
    record_id = client.get("/api/candidates").json()[0]["id"]
    rejected = client.post(
        f"/api/candidates/{record_id}/review-transition",
        json={
            "new_status": "Human-Reviewed Candidate",
            "reviewer_label": "HR",
            "reason": "short",
        },
    )
    assert rejected.status_code == 422

    accepted = client.post(
        f"/api/candidates/{record_id}/review-transition",
        json={
            "new_status": "Human-Reviewed Candidate",
            "reviewer_label": "Reviewer A",
            "reason": "Manual review recorded for candidate-only status.",
            "linked_risk_flags": ["RF-001"],
        },
    )
    assert accepted.status_code == 200
    assert accepted.json()["status"] == "Human-Reviewed Candidate"

    audit = client.get("/api/audit-events").json()
    assert any(event["event_type"] == "human_review_transition" for event in audit)


def test_founder_gate_is_manual_record_not_auto_pass(client):
    response = client.post(
        "/api/founder-gates",
        json={
            "gate_trigger": "External-use boundary review",
            "affected_record_ids": ["S001"],
            "decision_date": "2026-07-10",
            "decision_status": "Founder Review Required",
            "founder_instruction_text": "Founder review required before external use.",
        },
    )
    assert response.status_code == 201
    payload = response.json()
    assert payload["decision_status"] == "Founder Review Required"
    assert "Passed" not in payload["decision_status"]


def test_relationship_requires_existing_candidates(client):
    response = client.post(
        "/api/relationships",
        json={
            "from_record_id": "S001",
            "to_record_id": "KO-005",
            "relationship_type": "supports candidate cluster",
            "created_by": "Reviewer A",
            "reason": "Manual relationship for local prototype review.",
        },
    )
    assert response.status_code == 201

    missing = client.post(
        "/api/relationships",
        json={
            "from_record_id": "S001",
            "to_record_id": "MISSING",
            "relationship_type": "bad link",
            "created_by": "Reviewer A",
            "reason": "Manual relationship should fail for missing record.",
        },
    )
    assert missing.status_code == 404
