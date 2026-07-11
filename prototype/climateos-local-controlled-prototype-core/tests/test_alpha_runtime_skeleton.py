from fastapi.testclient import TestClient

from climateos_local_prototype.api import create_app


def evidence_payload(**overrides):
    payload = {
        "title": "Synthetic catchment observation",
        "domain": "water",
        "object_type": "observation_candidate",
        "summary": "Synthetic example for local Alpha Runtime review.",
        "source_refs": ["FIXTURE-WATER-001"],
        "provenance": "Generated fixture; no live source.",
        "assumptions": ["Demonstration only"],
        "uncertainty": "No real-world inference is permitted.",
        "permissions": "synthetic/public-safe fixture",
        "human_review_required": True,
    }
    payload.update(overrides)
    return payload


def test_capabilities_and_fixture_domains(tmp_path):
    client = TestClient(create_app(tmp_path / "alpha.sqlite3"))

    capabilities = client.get("/api/alpha/capabilities").json()
    assert capabilities["persistent"] is False
    assert capabilities["localhost_only"] is True
    assert capabilities["human_review_required"] is True

    domains = client.get("/api/alpha/domains").json()
    assert {item["name"] for item in domains} == {
        "climate", "water", "land", "energy", "carbon", "biodiversity"
    }
    assert all(item["mode"] == "fixture-only" for item in domains)


def test_evidence_contract_review_dispute_correction_and_audit(tmp_path):
    client = TestClient(create_app(tmp_path / "alpha.sqlite3"))
    created = client.post("/api/alpha/evidence-contracts", json=evidence_payload())
    assert created.status_code == 201
    record = created.json()
    assert record["state"] == "candidate"
    assert record["revision"] == 1

    reviewed = client.post(
        f"/api/alpha/evidence-contracts/{record['id']}/review-actions",
        json={"action": "review", "reviewer_label": "Reviewer", "reason": "Reviewed only as a synthetic candidate."},
    )
    assert reviewed.status_code == 200
    assert reviewed.json()["state"] == "reviewed"

    disputed = client.post(
        f"/api/alpha/evidence-contracts/{record['id']}/review-actions",
        json={"action": "dispute", "reviewer_label": "Challenger", "reason": "The assumptions require explicit challenge."},
    )
    assert disputed.status_code == 200
    assert disputed.json()["state"] == "disputed"

    corrected = client.post(
        f"/api/alpha/evidence-contracts/{record['id']}/review-actions",
        json={
            "action": "correct",
            "reviewer_label": "Reviewer",
            "reason": "Return the disputed item for bounded correction.",
            "correction_summary": "Corrected synthetic summary; still not a conclusion.",
        },
    )
    assert corrected.status_code == 200
    assert corrected.json()["state"] == "candidate"

    audit = client.get("/api/alpha/audit-events").json()
    assert [item["sequence_number"] for item in audit] == list(range(1, len(audit) + 1))
    assert client.get("/api/alpha/diagnostics").json()["status"] == "healthy"


def test_refusal_escalation_invalid_transition_and_rollback(tmp_path):
    client = TestClient(create_app(tmp_path / "alpha.sqlite3"))
    record = client.post("/api/alpha/evidence-contracts", json=evidence_payload()).json()

    escalated = client.post(
        f"/api/alpha/evidence-contracts/{record['id']}/review-actions",
        json={"action": "escalate", "reviewer_label": "Reviewer", "reason": "Human specialist review is required before reuse."},
    ).json()
    assert escalated["state"] == "disputed"
    assert escalated["escalation_required"] is True

    rejected = client.post(
        f"/api/alpha/evidence-contracts/{record['id']}/review-actions",
        json={"action": "reject", "reviewer_label": "Reviewer", "reason": "Reject this synthetic candidate as unsupported."},
    )
    assert rejected.status_code == 200

    blocked = client.post(
        f"/api/alpha/evidence-contracts/{record['id']}/review-actions",
        json={"action": "review", "reviewer_label": "Reviewer", "reason": "Attempted invalid review after rejection."},
    )
    assert blocked.status_code == 409
    assert client.get("/api/alpha/audit-events").json()[-1]["event_type"] == "alpha_transition_refused"

    rollback = client.post(
        f"/api/alpha/evidence-contracts/{record['id']}/rollback",
        json={"target_revision": 1, "reviewer_label": "Reviewer", "reason": "Restore the original synthetic candidate for inspection."},
    )
    assert rollback.status_code == 200
    assert rollback.json()["state"] == "candidate"
    assert rollback.json()["revision"] == 4

    same_revision = client.post(
        f"/api/alpha/evidence-contracts/{record['id']}/rollback",
        json={"target_revision": 4, "reviewer_label": "Reviewer", "reason": "A no-op rollback must be refused and audited."},
    )
    assert same_revision.status_code == 409
    assert client.get("/api/alpha/audit-events").json()[-1]["event_type"] == "alpha_rollback_refused"


def test_deliberation_requires_known_evidence_and_abstention(tmp_path):
    client = TestClient(create_app(tmp_path / "alpha.sqlite3"))
    evidence = client.post("/api/alpha/evidence-contracts", json=evidence_payload()).json()
    payload = {
        "claim_text": "Synthetic water condition may affect a fixture habitat.",
        "evidence_contract_ids": [evidence["id"]],
        "challenge_text": "The fixture cannot establish a real causal relationship.",
        "counter_evidence_contract_ids": [],
        "uncertainty": "No live observation or model was used.",
        "abstains_from_conclusion": True,
        "human_decision": "Human specialist review required",
    }
    created = client.post("/api/alpha/deliberations", json=payload)
    assert created.status_code == 201
    assert created.json()["status"] == "human_decision_required"

    missing = {**payload, "evidence_contract_ids": ["ALPHA-EVIDENCE-MISSING"]}
    assert client.post("/api/alpha/deliberations", json=missing).status_code == 404

    conclusion = {**payload, "abstains_from_conclusion": False}
    assert client.post("/api/alpha/deliberations", json=conclusion).status_code == 422


def test_human_review_and_conclusion_boundaries_are_enforced(tmp_path):
    client = TestClient(create_app(tmp_path / "alpha.sqlite3"))
    no_review = evidence_payload(human_review_required=False)
    assert client.post("/api/alpha/evidence-contracts", json=no_review).status_code == 422

    record = client.post("/api/alpha/evidence-contracts", json=evidence_payload()).json()
    no_correction = client.post(
        f"/api/alpha/evidence-contracts/{record['id']}/review-actions",
        json={"action": "correct", "reviewer_label": "Reviewer", "reason": "Correction requires an explicit revised summary."},
    )
    assert no_correction.status_code == 409
