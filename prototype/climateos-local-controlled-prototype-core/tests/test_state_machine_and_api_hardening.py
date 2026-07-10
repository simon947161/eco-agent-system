from fastapi.testclient import TestClient

from climateos_local_prototype.api import create_app
from climateos_local_prototype.config import MAX_REQUEST_BYTES
from climateos_local_prototype.repository import PrototypeRepository
from climateos_local_prototype.seed import seed_database


def _client(tmp_path) -> TestClient:
    db_path = tmp_path / "prototype.sqlite3"
    repository = PrototypeRepository(db_path)
    seed_database(repository)
    return TestClient(create_app(db_path))


def test_state_machine_blocks_direct_review_jump_and_records_audit(tmp_path):
    client = _client(tmp_path)
    blocked = client.post(
        "/api/candidates/S001/review-transition",
        json={
            "new_status": "Human-Reviewed Candidate",
            "reviewer_label": "Reviewer A",
            "reason": "Direct jump should be blocked by local state-machine rules.",
        },
    )
    assert blocked.status_code == 409

    needs_review = client.post(
        "/api/candidates/S001/review-transition",
        json={
            "new_status": "Needs Human Review",
            "reviewer_label": "Reviewer A",
            "reason": "Source verification passed to human review queue locally.",
        },
    )
    assert needs_review.status_code == 200

    reviewed = client.post(
        "/api/candidates/S001/review-transition",
        json={
            "new_status": "Human-Reviewed Candidate",
            "reviewer_label": "Reviewer A",
            "reason": "Human review status recorded for local prototype candidate only.",
        },
    )
    assert reviewed.status_code == 200
    assert reviewed.json()["status"] == "Human-Reviewed Candidate"

    audit = client.get("/api/audit-events").json()
    assert any(event["event_type"] == "blocked_status_transition" for event in audit)


def test_blocked_and_founder_gate_transitions_require_risk_context(tmp_path):
    client = _client(tmp_path)
    blocked = client.post(
        "/api/candidates/S001/review-transition",
        json={
            "new_status": "Blocked",
            "reviewer_label": "Reviewer A",
            "reason": "Blocked status should require explicit risk linkage.",
        },
    )
    assert blocked.status_code == 409

    missing_trigger = client.post(
        "/api/candidates/S001/review-transition",
        json={
            "new_status": "Founder Gate Required",
            "reviewer_label": "Reviewer A",
            "reason": "Founder gate transition should require an explicit trigger.",
            "linked_risk_flags": ["RF-001"],
        },
    )
    assert missing_trigger.status_code == 409

    accepted = client.post(
        "/api/candidates/S001/review-transition",
        json={
            "new_status": "Founder Gate Required",
            "reviewer_label": "Reviewer A",
            "reason": "Founder gate transition has explicit risk and trigger.",
            "linked_risk_flags": ["RF-001"],
            "founder_gate_trigger": "External-use boundary review",
        },
    )
    assert accepted.status_code == 200


def test_relationship_duplicate_and_founder_gate_history(tmp_path):
    client = _client(tmp_path)
    relationship = {
        "from_record_id": "S001",
        "to_record_id": "KO-005",
        "relationship_type": "supports candidate cluster",
        "created_by": "Reviewer A",
        "reason": "Manual relationship for local prototype review.",
    }
    assert client.post("/api/relationships", json=relationship).status_code == 201
    assert client.post("/api/relationships", json=relationship).status_code == 409

    first = client.post(
        "/api/founder-gates",
        json={
            "gate_trigger": "External-use boundary review",
            "affected_record_ids": ["S001"],
            "decision_date": "2026-07-10",
            "decision_status": "Founder Review Required",
            "founder_instruction_text": "Founder review required before external use.",
        },
    )
    assert first.status_code == 201
    second = client.post(
        "/api/founder-gates",
        json={
            "gate_trigger": "External-use boundary review",
            "affected_record_ids": ["S001"],
            "decision_date": "2026-07-10",
            "decision_status": "Deferred",
            "founder_instruction_text": "Founder deferred external use review.",
            "supersedes_gate_id": first.json()["id"],
        },
    )
    assert second.status_code == 201
    payload = second.json()
    assert payload["decision_version"] == 2
    assert payload["supersedes_gate_id"] == first.json()["id"]


def test_import_preview_is_dry_run_and_security_controls_are_local(tmp_path):
    client = _client(tmp_path)
    mock = client.post("/api/model/mock-response", json=["S001"]).json()
    preview = client.post("/api/model/import-preview", json=mock)
    assert preview.status_code == 200
    assert preview.json()["will_write"] is False
    assert client.post("/api/model/import-response", json=mock).status_code == 201

    conflict_preview = client.post("/api/model/import-preview", json=mock)
    assert conflict_preview.status_code == 200
    assert conflict_preview.json()["status"] == "conflict"

    health = client.get("/api/health")
    assert health.status_code == 200
    assert health.headers["X-Frame-Options"] == "DENY"
    assert health.headers["Cache-Control"] == "no-store"

    assert client.get("/api/health", headers={"host": "example.com"}).status_code == 400
    too_large = b" " * (MAX_REQUEST_BYTES + 1)
    assert client.post("/api/candidates", content=too_large, headers={"content-type": "application/json"}).status_code == 413
