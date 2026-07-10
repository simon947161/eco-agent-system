from typing import Any, Literal

from pydantic import BaseModel, Field, field_validator

from .config import BOUNDARY_LABEL, PROHIBITED_STATUS_TERMS

RecordType = Literal[
    "source_candidate",
    "signal_candidate",
    "claim_candidate",
    "knowledge_object_candidate",
    "evidence_candidate",
]

CandidateStatus = Literal[
    "Draft Candidate",
    "Needs Source Verification",
    "Needs Translation Review",
    "Needs Human Review",
    "Blocked",
    "Founder Gate Required",
    "Human-Reviewed Candidate",
    "Archived",
    "Superseded",
]

GateStatus = Literal[
    "Not Opened",
    "Founder Review Required",
    "Deferred",
    "Rejected",
    "Limited Authorization Recorded",
    "Closed",
]

SuggestionCategory = Literal[
    "source-summary suggestion",
    "claim-candidate suggestion",
    "signal-clustering suggestion",
    "risk-flag suggestion",
    "readiness-label suggestion",
    "review-note draft",
    "archive-summary draft",
]

SuggestionAction = Literal["accept", "reject", "revise", "defer", "escalate"]


class CandidateCreate(BaseModel):
    record_type: RecordType
    title: str = Field(min_length=3, max_length=240)
    status: CandidateStatus = "Draft Candidate"
    summary: str = Field(default="", max_length=3000)
    source_ids: list[str] = Field(default_factory=list)
    signal_ids: list[str] = Field(default_factory=list)
    claim_ids: list[str] = Field(default_factory=list)
    knowledge_object_ids: list[str] = Field(default_factory=list)
    evidence_ids: list[str] = Field(default_factory=list)
    readiness_label: str = Field(default="Candidate only", max_length=120)
    risk_flags: list[str] = Field(default_factory=list)
    human_review_need: str = Field(default="", max_length=1000)
    founder_gate_need: str = Field(default="", max_length=1000)
    boundary_label: str = BOUNDARY_LABEL

    @field_validator("status")
    @classmethod
    def status_must_stay_candidate_only(cls, value: str) -> str:
        lowered = value.lower()
        if any(term in lowered for term in PROHIBITED_STATUS_TERMS):
            raise ValueError("Authoritative or conclusion-like statuses are prohibited.")
        return value


class CandidateUpdate(BaseModel):
    title: str | None = Field(default=None, min_length=3, max_length=240)
    summary: str | None = Field(default=None, max_length=3000)
    source_ids: list[str] | None = None
    signal_ids: list[str] | None = None
    claim_ids: list[str] | None = None
    knowledge_object_ids: list[str] | None = None
    evidence_ids: list[str] | None = None
    readiness_label: str | None = Field(default=None, max_length=120)
    risk_flags: list[str] | None = None
    human_review_need: str | None = Field(default=None, max_length=1000)
    founder_gate_need: str | None = Field(default=None, max_length=1000)


class RelationshipCreate(BaseModel):
    from_record_id: str = Field(min_length=1, max_length=80)
    to_record_id: str = Field(min_length=1, max_length=80)
    relationship_type: str = Field(min_length=3, max_length=120)
    created_by: str = Field(min_length=2, max_length=120)
    reason: str = Field(min_length=5, max_length=1000)


class ReviewTransition(BaseModel):
    new_status: CandidateStatus
    reviewer_label: str = Field(min_length=2, max_length=120)
    reason: str = Field(min_length=10, max_length=1200)
    linked_risk_flags: list[str] = Field(default_factory=list)
    founder_gate_trigger: str = Field(default="", max_length=1000)


class FounderGateCreate(BaseModel):
    gate_trigger: str = Field(min_length=5, max_length=1000)
    affected_record_ids: list[str] = Field(default_factory=list)
    decision_date: str = Field(min_length=4, max_length=80)
    decision_status: GateStatus
    founder_instruction_text: str = Field(min_length=5, max_length=2000)
    scope_allowed: str = Field(default="", max_length=2000)
    scope_prohibited: str = Field(default="", max_length=2000)
    review_or_expiry_requirement: str = Field(default="", max_length=1000)
    archive_reference: str = Field(default="", max_length=240)


class ModelSuggestion(BaseModel):
    suggestion_id: str = Field(min_length=1, max_length=120)
    category: SuggestionCategory
    target_record_id: str = Field(default="", max_length=80)
    suggestion_text: str = Field(min_length=3, max_length=3000)
    provenance: str = Field(default="deterministic mock adapter", max_length=240)


class ModelResponseImport(BaseModel):
    response_id: str = Field(min_length=1, max_length=120)
    source_label: str = Field(min_length=2, max_length=240)
    suggestions: list[ModelSuggestion]


class SuggestionDecision(BaseModel):
    action: SuggestionAction
    reviewer_label: str = Field(min_length=2, max_length=120)
    reason: str = Field(min_length=10, max_length=1200)


class ArchiveRequest(BaseModel):
    case_id: str = Field(min_length=3, max_length=120)
    reviewer_label: str = Field(min_length=2, max_length=120)
    reason: str = Field(min_length=10, max_length=1200)


class PromptBundle(BaseModel):
    bundle_id: str
    boundary_label: str = BOUNDARY_LABEL
    instructions: list[str]
    candidate_records: list[dict[str, Any]]
