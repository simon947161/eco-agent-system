from pathlib import Path

import pytest
from fastapi.testclient import TestClient

from climateos_local_prototype.api import create_app


STATIC_DIR = Path(__file__).parents[1] / "static"


def synthetic_payload(domain="biodiversity"):
    return {
        "title": "Synthetic human-use evidence",
        "domain": domain,
        "object_type": "synthetic_observation_candidate",
        "summary": "Fabricated fixture for local human-use testing only.",
        "source_refs": ["LOCAL-USE-TRIAL-FIXTURE"],
        "provenance": "Generated locally; no external or live source.",
        "assumptions": ["Demonstration only"],
        "uncertainty": "No real-world inference is permitted.",
        "permissions": "synthetic/public-safe fixture",
        "human_review_required": True,
    }


def test_workbench_keeps_authority_and_identity_warnings_visible():
    page = (STATIC_DIR / "index.html").read_text(encoding="utf-8")
    assert "Reviewer labels are locally declared labels, not verified identities" in page
    assert "cannot prove scientific truth" in page
    assert "Every workflow must abstain from real-world conclusions" in page
    assert 'id="alpha-create-form"' in page
    assert 'id="alpha-review-form"' in page


def test_synthetic_use_trial_supports_human_review_without_truth_claim(tmp_path):
    client = TestClient(create_app(tmp_path / "trial.sqlite3"))
    created_response = client.post("/api/alpha/evidence-contracts", json=synthetic_payload())
    assert created_response.status_code == 201
    created = created_response.json()
    assert created["state"] == "candidate"
    assert created["human_review_required"] is True

    reviewed_response = client.post(
        f"/api/alpha/evidence-contracts/{created['id']}/review-actions",
        json={
            "action": "dispute",
            "reviewer_label": "Declared local reviewer",
            "reason": "Synthetic evidence cannot support a real biodiversity conclusion.",
        },
    )
    assert reviewed_response.status_code == 200
    reviewed = reviewed_response.json()
    assert reviewed["state"] == "disputed"
    assert reviewed["review_history"][-1]["action"] == "dispute"
    assert "real biodiversity conclusion" in reviewed["review_history"][-1]["reason"]

    audit = client.get("/api/alpha/audit-events").json()
    assert [event["event_type"] for event in audit] == [
        "alpha_evidence_created",
        "alpha_evidence_dispute",
    ]


@pytest.mark.parametrize(
    ("action", "expected_state"),
    [
        ("review", "reviewed"),
        ("dispute", "disputed"),
        ("reject", "rejected"),
        ("mark_stale", "stale"),
        ("escalate", "disputed"),
    ],
)
def test_declared_human_actions_are_auditable(action, expected_state, tmp_path):
    client = TestClient(create_app(tmp_path / f"{action}.sqlite3"))
    created = client.post("/api/alpha/evidence-contracts", json=synthetic_payload()).json()
    response = client.post(
        f"/api/alpha/evidence-contracts/{created['id']}/review-actions",
        json={
            "action": action,
            "reviewer_label": "Declared trial reviewer",
            "reason": "Record a bounded synthetic human action without issuing a conclusion.",
        },
    )
    assert response.status_code == 200
    assert response.json()["state"] == expected_state
    assert response.json()["escalation_required"] is (action == "escalate")
    event = client.get("/api/alpha/audit-events").json()[-1]
    assert event["event_type"] == f"alpha_evidence_{action}"
    assert event["actor_label"] == "Declared trial reviewer"


def test_correction_requires_summary_and_preserves_prior_revision(tmp_path):
    client = TestClient(create_app(tmp_path / "correction.sqlite3"))
    created = client.post("/api/alpha/evidence-contracts", json=synthetic_payload()).json()
    refused = client.post(
        f"/api/alpha/evidence-contracts/{created['id']}/review-actions",
        json={
            "action": "correct",
            "reviewer_label": "Declared trial reviewer",
            "reason": "A correction must explain the synthetic change clearly.",
            "correction_summary": "",
        },
    )
    assert refused.status_code == 409

    corrected = client.post(
        f"/api/alpha/evidence-contracts/{created['id']}/review-actions",
        json={
            "action": "correct",
            "reviewer_label": "Declared trial reviewer",
            "reason": "Correct the fixture wording while preserving uncertainty.",
            "correction_summary": "Synthetic wording corrected; no conclusion added.",
        },
    )
    assert corrected.status_code == 200
    record = corrected.json()
    assert record["revision"] == 2
    assert len(record["revision_history"]) == 1
    assert record["revision_history"][0]["revision"] == 1


def test_correction_updates_editable_fields_without_erasing_history(tmp_path):
    client = TestClient(create_app(tmp_path / "alpha.sqlite3"))
    created = client.post("/api/alpha/evidence-contracts", json=synthetic_payload()).json()
    corrected = client.post(
        f"/api/alpha/evidence-contracts/{created['id']}/review-actions",
        json={"action": "correct", "reviewer_label": "Founder", "reason": "Correct fields while preserving the prior revision.",
              "corrected_title": "Corrected synthetic title", "correction_summary": "Corrected synthetic summary.",
              "corrected_uncertainty": "Corrected uncertainty remains synthetic."},
    ).json()
    assert corrected["revision"] == 2
    assert corrected["title"] == "Corrected synthetic title"
    assert corrected["revision_history"][0]["title"] == created["title"]
    assert client.get("/api/alpha/audit-events").json()[-1]["event_type"] == "alpha_evidence_correct"
