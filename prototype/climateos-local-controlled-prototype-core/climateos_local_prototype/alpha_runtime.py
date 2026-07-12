import copy
import uuid
from datetime import UTC, datetime
from threading import RLock
from typing import Literal

from pydantic import BaseModel, Field, field_validator

ALPHA_BOUNDARY = "Alpha Skeleton / Synthetic / Localhost / Non-Operational"

DomainName = Literal["climate", "water", "land", "energy", "carbon", "biodiversity"]
EvidenceState = Literal["candidate", "reviewed", "disputed", "rejected", "stale", "superseded"]
ReviewActionName = Literal["review", "dispute", "reject", "mark_stale", "supersede", "correct", "escalate"]

DOMAIN_FIXTURES = [
    {"id": "DOMAIN-CLIMATE", "name": "climate", "mode": "fixture-only", "review_authority": "human climate reviewer"},
    {"id": "DOMAIN-WATER", "name": "water", "mode": "fixture-only", "review_authority": "human water reviewer"},
    {"id": "DOMAIN-LAND", "name": "land", "mode": "fixture-only", "review_authority": "human land reviewer"},
    {"id": "DOMAIN-ENERGY", "name": "energy", "mode": "fixture-only", "review_authority": "human energy reviewer"},
    {"id": "DOMAIN-CARBON", "name": "carbon", "mode": "fixture-only", "review_authority": "human carbon reviewer"},
    {"id": "DOMAIN-BIODIVERSITY", "name": "biodiversity", "mode": "fixture-only", "review_authority": "human ecology reviewer"},
]


def _now_iso() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def _id(prefix: str) -> str:
    return f"{prefix}-{uuid.uuid4().hex[:12]}"


class EvidenceContractCreate(BaseModel):
    title: str = Field(min_length=3, max_length=240)
    domain: DomainName
    object_type: str = Field(min_length=3, max_length=120)
    summary: str = Field(min_length=3, max_length=3000)
    source_refs: list[str] = Field(default_factory=list, max_length=50)
    provenance: str = Field(min_length=3, max_length=1000)
    assumptions: list[str] = Field(default_factory=list, max_length=50)
    uncertainty: str = Field(min_length=3, max_length=1200)
    permissions: str = Field(default="synthetic/public-safe fixture", min_length=3, max_length=500)
    human_review_required: bool = True

    @field_validator("human_review_required")
    @classmethod
    def human_review_cannot_be_disabled(cls, value: bool) -> bool:
        if not value:
            raise ValueError("Alpha skeleton evidence always requires human review.")
        return value


class AlphaReviewAction(BaseModel):
    action: ReviewActionName
    reviewer_label: str = Field(min_length=2, max_length=120)
    reason: str = Field(min_length=10, max_length=1200)
    correction_summary: str = Field(default="", max_length=3000)
    corrected_title: str = Field(default="", max_length=240)
    corrected_uncertainty: str = Field(default="", max_length=1200)
    supersedes_id: str = Field(default="", max_length=120)


class AlphaRollbackRequest(BaseModel):
    target_revision: int = Field(ge=1)
    reviewer_label: str = Field(min_length=2, max_length=120)
    reason: str = Field(min_length=10, max_length=1200)


class DeliberationCreate(BaseModel):
    claim_text: str = Field(min_length=5, max_length=2000)
    evidence_contract_ids: list[str] = Field(default_factory=list, max_length=50)
    challenge_text: str = Field(min_length=5, max_length=2000)
    counter_evidence_contract_ids: list[str] = Field(default_factory=list, max_length=50)
    uncertainty: str = Field(min_length=3, max_length=1200)
    abstains_from_conclusion: bool = True
    human_decision: str = Field(default="Human decision required", max_length=1000)

    @field_validator("abstains_from_conclusion")
    @classmethod
    def deliberation_must_abstain(cls, value: bool) -> bool:
        if not value:
            raise ValueError("Alpha skeleton deliberation cannot issue a conclusion.")
        return value


class InvalidAlphaTransitionError(ValueError):
    pass


class AlphaRuntimeStore:
    _ACTION_STATE: dict[str, EvidenceState] = {
        "review": "reviewed",
        "dispute": "disputed",
        "reject": "rejected",
        "mark_stale": "stale",
        "supersede": "superseded",
        "correct": "candidate",
        "escalate": "disputed",
    }

    def __init__(self) -> None:
        self._lock = RLock()
        self._evidence: dict[str, dict] = {}
        self._deliberations: dict[str, dict] = {}
        self._audit: list[dict] = []

    def _audit_event(self, event_type: str, actor_label: str, record_id: str, detail: dict) -> dict:
        event = {
            "id": _id("ALPHA-AUDIT"),
            "sequence_number": len(self._audit) + 1,
            "event_type": event_type,
            "actor_label": actor_label,
            "record_id": record_id,
            "detail": copy.deepcopy(detail),
            "created_at": _now_iso(),
            "boundary_label": ALPHA_BOUNDARY,
        }
        self._audit.append(event)
        return copy.deepcopy(event)

    def capabilities(self) -> dict:
        return {
            "boundary_label": ALPHA_BOUNDARY,
            "persistent": False,
            "restart_clears_state": True,
            "localhost_only": True,
            "synthetic_or_public_safe_only": True,
            "human_review_required": True,
            "capabilities": [
                "evidence-contract-candidate",
                "fixture-domain-registry",
                "human-review-and-refusal",
                "claim-challenge-counter-evidence",
                "append-only-in-memory-audit",
                "revision-rollback",
            ],
            "prohibited": ["conclusion", "scoring", "certification", "automation", "external-model-call"],
        }

    def domains(self) -> list[dict]:
        return copy.deepcopy(DOMAIN_FIXTURES)

    def create_evidence(self, payload: EvidenceContractCreate) -> dict:
        with self._lock:
            record_id = _id("ALPHA-EVIDENCE")
            now = _now_iso()
            record = {
                "id": record_id,
                **payload.model_dump(),
                "state": "candidate",
                "revision": 1,
                "escalation_required": False,
                "review_history": [],
                "revision_history": [],
                "boundary_label": ALPHA_BOUNDARY,
                "created_at": now,
                "updated_at": now,
            }
            self._evidence[record_id] = record
            self._audit_event("alpha_evidence_created", "human_submitter", record_id, {"domain": payload.domain})
            return copy.deepcopy(record)

    def list_evidence(self) -> list[dict]:
        with self._lock:
            return [copy.deepcopy(item) for item in self._evidence.values()]

    def get_evidence(self, record_id: str) -> dict:
        with self._lock:
            if record_id not in self._evidence:
                raise KeyError(record_id)
            return copy.deepcopy(self._evidence[record_id])

    def review_evidence(self, record_id: str, payload: AlphaReviewAction) -> dict:
        with self._lock:
            if record_id not in self._evidence:
                raise KeyError(record_id)
            record = self._evidence[record_id]
            if record["state"] in {"rejected", "superseded"} and payload.action not in {"correct"}:
                self._audit_event(
                    "alpha_transition_refused",
                    payload.reviewer_label,
                    record_id,
                    {"state": record["state"], "attempted_action": payload.action},
                )
                raise InvalidAlphaTransitionError(
                    f"State {record['state']} only permits a documented correction into candidate state."
                )
            if payload.action == "supersede" and not payload.supersedes_id:
                self._audit_event(
                    "alpha_transition_refused",
                    payload.reviewer_label,
                    record_id,
                    {"state": record["state"], "attempted_action": payload.action, "reason": "missing supersedes_id"},
                )
                raise InvalidAlphaTransitionError("Supersede action requires supersedes_id.")
            if payload.action == "correct" and not any(
                [payload.correction_summary, payload.corrected_title, payload.corrected_uncertainty]
            ):
                self._audit_event(
                    "alpha_transition_refused",
                    payload.reviewer_label,
                    record_id,
                    {"state": record["state"], "attempted_action": payload.action, "reason": "missing correction summary"},
                )
                raise InvalidAlphaTransitionError("Correction action requires at least one corrected field.")

            snapshot = copy.deepcopy(record)
            snapshot.pop("revision_history", None)
            record["revision_history"].append(snapshot)
            previous_state = record["state"]
            record["state"] = self._ACTION_STATE[payload.action]
            record["revision"] += 1
            record["updated_at"] = _now_iso()
            record["escalation_required"] = payload.action == "escalate"
            if payload.correction_summary:
                record["summary"] = payload.correction_summary
            if payload.corrected_title:
                record["title"] = payload.corrected_title
            if payload.corrected_uncertainty:
                record["uncertainty"] = payload.corrected_uncertainty
            record["review_history"].append(
                {
                    "action": payload.action,
                    "previous_state": previous_state,
                    "new_state": record["state"],
                    "reviewer_label": payload.reviewer_label,
                    "reason": payload.reason,
                    "supersedes_id": payload.supersedes_id,
                    "created_at": record["updated_at"],
                }
            )
            self._audit_event(
                f"alpha_evidence_{payload.action}",
                payload.reviewer_label,
                record_id,
                {"previous_state": previous_state, "new_state": record["state"], "revision": record["revision"]},
            )
            return copy.deepcopy(record)

    def rollback_evidence(self, record_id: str, payload: AlphaRollbackRequest) -> dict:
        with self._lock:
            if record_id not in self._evidence:
                raise KeyError(record_id)
            record = self._evidence[record_id]
            if payload.target_revision == record["revision"]:
                self._audit_event(
                    "alpha_rollback_refused",
                    payload.reviewer_label,
                    record_id,
                    {"target_revision": payload.target_revision, "reason": "already current"},
                )
                raise InvalidAlphaTransitionError("Requested revision is already current.")
            candidates = [record, *record["revision_history"]]
            target = next((item for item in candidates if item["revision"] == payload.target_revision), None)
            if target is None:
                self._audit_event(
                    "alpha_rollback_refused",
                    payload.reviewer_label,
                    record_id,
                    {"target_revision": payload.target_revision, "reason": "revision unavailable"},
                )
                raise InvalidAlphaTransitionError("Requested revision is not available for rollback.")
            current_snapshot = copy.deepcopy(record)
            current_snapshot.pop("revision_history", None)
            prior_history = copy.deepcopy(record["revision_history"])
            restored = copy.deepcopy(target)
            restored["revision_history"] = [*prior_history, current_snapshot]
            restored["revision"] = record["revision"] + 1
            restored["updated_at"] = _now_iso()
            restored["review_history"] = [
                *record["review_history"],
                {
                    "action": "rollback",
                    "previous_state": record["state"],
                    "new_state": target["state"],
                    "reviewer_label": payload.reviewer_label,
                    "reason": payload.reason,
                    "target_revision": payload.target_revision,
                    "created_at": restored["updated_at"],
                },
            ]
            self._evidence[record_id] = restored
            self._audit_event(
                "alpha_evidence_rollback",
                payload.reviewer_label,
                record_id,
                {"target_revision": payload.target_revision, "new_revision": restored["revision"]},
            )
            return copy.deepcopy(restored)

    def create_deliberation(self, payload: DeliberationCreate) -> dict:
        with self._lock:
            linked_ids = set(payload.evidence_contract_ids + payload.counter_evidence_contract_ids)
            missing = sorted(linked_ids.difference(self._evidence))
            if missing:
                raise KeyError(",".join(missing))
            record_id = _id("ALPHA-DELIBERATION")
            record = {
                "id": record_id,
                **payload.model_dump(),
                "status": "human_decision_required",
                "boundary_label": ALPHA_BOUNDARY,
                "created_at": _now_iso(),
            }
            self._deliberations[record_id] = record
            self._audit_event(
                "alpha_deliberation_created",
                "human_reviewer",
                record_id,
                {"evidence_count": len(linked_ids), "abstains_from_conclusion": True},
            )
            return copy.deepcopy(record)

    def list_deliberations(self) -> list[dict]:
        with self._lock:
            return [copy.deepcopy(item) for item in self._deliberations.values()]

    def audit_events(self) -> list[dict]:
        with self._lock:
            return copy.deepcopy(self._audit)

    def diagnostics(self) -> dict:
        with self._lock:
            sequences = [item["sequence_number"] for item in self._audit]
            expected = list(range(1, len(sequences) + 1))
            return {
                "status": "healthy" if sequences == expected else "unhealthy",
                "boundary_label": ALPHA_BOUNDARY,
                "evidence_count": len(self._evidence),
                "deliberation_count": len(self._deliberations),
                "audit_event_count": len(self._audit),
                "audit_sequence_contiguous": sequences == expected,
                "persistent": False,
            }
