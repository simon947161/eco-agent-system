from concurrent.futures import ThreadPoolExecutor

from fastapi.testclient import TestClient

from climateos_local_prototype.api import create_app
from climateos_local_prototype.database import connect, get_schema_version


def payload(domain="water", suffix="one"):
    return {
        "title": f"Synthetic persistent evidence {suffix}",
        "domain": domain,
        "object_type": "synthetic_observation_candidate",
        "summary": "Fabricated fixture for persistent review testing only.",
        "source_refs": [f"FIXTURE-{domain.upper()}-{suffix}"],
        "provenance": "Generated locally; no external or live source.",
        "assumptions": ["Demonstration only"],
        "uncertainty": "No real-world inference is permitted.",
        "permissions": "synthetic/public-safe fixture",
        "human_review_required": True,
    }


def test_schema_v3_is_additive_and_idempotent(tmp_path):
    db_path = tmp_path / "alpha.sqlite3"
    create_app(db_path)
    create_app(db_path)
    with connect(db_path) as connection:
        assert get_schema_version(connection) == 3
        tables = {
            row["name"]
            for row in connection.execute("SELECT name FROM sqlite_master WHERE type='table'")
        }
    assert {"candidate_records", "audit_events", "alpha_evidence_contracts",
            "alpha_evidence_revisions", "alpha_audit_events", "alpha_deliberations"} <= tables


def test_evidence_review_audit_and_deliberation_survive_restart(tmp_path):
    db_path = tmp_path / "alpha.sqlite3"
    first = TestClient(create_app(db_path))
    water = first.post("/api/alpha/evidence-contracts", json=payload()).json()
    land = first.post("/api/alpha/evidence-contracts", json=payload("land", "two")).json()
    first.post(
        f"/api/alpha/evidence-contracts/{water['id']}/review-actions",
        json={"action": "review", "reviewer_label": "Human reviewer",
              "reason": "Synthetic evidence reviewed only for workflow testing."},
    )
    deliberation = first.post(
        "/api/alpha/deliberations",
        json={
            "claim_text": "Synthetic water timing may interact with fixture land response.",
            "evidence_contract_ids": [water["id"]],
            "challenge_text": "Fixture values cannot establish a real causal relation.",
            "counter_evidence_contract_ids": [land["id"]],
            "uncertainty": "No observations, models, or private assets were used.",
            "abstains_from_conclusion": True,
            "human_decision": "Human specialist review required",
        },
    ).json()

    restarted = TestClient(create_app(db_path))
    assert restarted.get(f"/api/alpha/evidence-contracts/{water['id']}").json()["state"] == "reviewed"
    assert restarted.get("/api/alpha/deliberations").json()[0]["id"] == deliberation["id"]
    diagnostics = restarted.get("/api/alpha/diagnostics").json()
    assert diagnostics["status"] == "healthy"
    assert diagnostics["persistent"] is True
    assert diagnostics["persistence_counts_match"] is True


def test_correction_rollback_preserves_revision_history_across_restart(tmp_path):
    db_path = tmp_path / "alpha.sqlite3"
    client = TestClient(create_app(db_path))
    record = client.post("/api/alpha/evidence-contracts", json=payload()).json()
    corrected = client.post(
        f"/api/alpha/evidence-contracts/{record['id']}/review-actions",
        json={"action": "correct", "reviewer_label": "Human reviewer",
              "reason": "Document a bounded synthetic correction for review.",
              "correction_summary": "Corrected synthetic fixture; still no conclusion."},
    ).json()
    rolled_back = client.post(
        f"/api/alpha/evidence-contracts/{record['id']}/rollback",
        json={"target_revision": 1, "reviewer_label": "Human reviewer",
              "reason": "Replay the original fixture without deleting history."},
    ).json()
    assert corrected["revision"] == 2
    assert rolled_back["revision"] == 3

    restarted = TestClient(create_app(db_path))
    recovered = restarted.get(f"/api/alpha/evidence-contracts/{record['id']}").json()
    assert recovered["revision"] == 3
    assert len(recovered["revision_history"]) == 2
    assert restarted.get("/api/alpha/audit-events").json()[-1]["event_type"] == "alpha_evidence_rollback"


def test_synthetic_cross_domain_scenarios_and_mandatory_abstention(tmp_path):
    client = TestClient(create_app(tmp_path / "alpha.sqlite3"))
    scenarios = client.get("/api/alpha/synthetic-scenarios").json()
    pairs = {tuple(item["domains"]) for item in scenarios}
    assert {("climate", "water"), ("water", "land"),
            ("land", "biodiversity"), ("energy", "climate")} <= pairs
    assert all("Synthetic" in item["boundary"] for item in scenarios)

    evidence = client.post("/api/alpha/evidence-contracts", json=payload()).json()
    result = client.post(
        "/api/alpha/deliberations",
        json={"claim_text": "A fixture-only cross-domain claim.",
              "evidence_contract_ids": [evidence["id"]],
              "challenge_text": "The evidence is synthetic and insufficient.",
              "counter_evidence_contract_ids": [],
              "uncertainty": "Complete real-world uncertainty.",
              "abstains_from_conclusion": False,
              "human_decision": "Human review required"},
    )
    assert result.status_code == 422


def test_bounded_concurrent_creates_keep_audit_sequence_contiguous(tmp_path):
    db_path = tmp_path / "alpha.sqlite3"
    client = TestClient(create_app(db_path))

    def create(index):
        return client.post(
            "/api/alpha/evidence-contracts", json=payload("climate", str(index))
        ).status_code

    with ThreadPoolExecutor(max_workers=4) as pool:
        assert list(pool.map(create, range(20))) == [201] * 20
    audit = client.get("/api/alpha/audit-events").json()
    assert [item["sequence_number"] for item in audit] == list(range(1, 21))
    assert client.get("/api/alpha/diagnostics").json()["status"] == "healthy"
