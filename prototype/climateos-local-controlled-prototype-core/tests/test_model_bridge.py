import pytest
from fastapi.testclient import TestClient

from climateos_local_prototype.api import create_app
from climateos_local_prototype.repository import PrototypeRepository
from climateos_local_prototype.seed import seed_database


@pytest.fixture()
def client(tmp_path):
    db_path = tmp_path / "prototype.sqlite3"
    repository = PrototypeRepository(db_path)
    seed_database(repository)
    return TestClient(create_app(db_path))


def test_prompt_bundle_and_mock_response_are_suggestions_only(client):
    bundle = client.post("/api/model/prompt-bundle", json=[]).json()
    assert bundle["boundary_label"] == "Prototype / Candidate / Non-Operational"
    assert "do not verify" in " ".join(bundle["instructions"]).lower()

    response = client.post("/api/model/mock-response", json=[]).json()
    assert response["source_label"] == "deterministic mock adapter"
    assert response["suggestions"]
    assert all("suggestion" in item["category"] or "draft" in item["category"] for item in response["suggestions"])


def test_imported_model_response_does_not_change_candidate_status(client):
    record_before = client.get("/api/candidates/S001").json()
    mock = client.post("/api/model/mock-response", json=["S001"]).json()
    imported = client.post("/api/model/import-response", json=mock)
    assert imported.status_code == 201
    record_after = client.get("/api/candidates/S001").json()
    assert record_after["status"] == record_before["status"]

    suggestion_id = imported.json()[0]["id"]
    decision = client.post(
        f"/api/model/suggestions/{suggestion_id}/decision",
        json={
            "action": "defer",
            "reviewer_label": "Reviewer A",
            "reason": "Manual reviewer deferred this suggestion for later review.",
        },
    )
    assert decision.status_code == 200
    assert decision.json()["disposition"] == "defer"


def test_two_mock_responses_import_sequentially_and_duplicate_conflicts(client):
    record_before = client.get("/api/candidates/S001").json()
    first = client.post("/api/model/mock-response", json=["S001"]).json()
    second = client.post("/api/model/mock-response", json=["S001"]).json()

    first_ids = {item["suggestion_id"] for item in first["suggestions"]}
    second_ids = {item["suggestion_id"] for item in second["suggestions"]}
    assert first["response_id"] != second["response_id"]
    assert first_ids.isdisjoint(second_ids)

    first_import = client.post("/api/model/import-response", json=first)
    second_import = client.post("/api/model/import-response", json=second)
    assert first_import.status_code == 201
    assert second_import.status_code == 201

    duplicate_import = client.post("/api/model/import-response", json=first)
    assert duplicate_import.status_code == 409
    assert "already been imported" in duplicate_import.json()["detail"]

    record_after = client.get("/api/candidates/S001").json()
    assert record_after["status"] == record_before["status"]


def test_malformed_model_response_is_rejected(client):
    response = client.post(
        "/api/model/import-response",
        json={"response_id": "bad", "source_label": "manual import", "suggestions": [{"category": "bad"}]},
    )
    assert response.status_code == 422
