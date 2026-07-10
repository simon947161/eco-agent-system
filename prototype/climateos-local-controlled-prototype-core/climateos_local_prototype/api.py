from pathlib import Path

from fastapi import Body, FastAPI, HTTPException
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from .archive import generate_archive_bundle
from .config import BOUNDARY_LABEL, DEFAULT_DB_PATH, STATIC_DIR, validate_local_host
from .database import initialize_database
from .model_bridge import deterministic_mock_response, generate_prompt_bundle
from .repository import PrototypeRepository
from .schemas import (
    ArchiveRequest,
    CandidateCreate,
    CandidateUpdate,
    FounderGateCreate,
    ModelResponseImport,
    RelationshipCreate,
    ReviewTransition,
    SuggestionDecision,
)


def create_app(db_path: str | Path | None = None) -> FastAPI:
    path = Path(db_path) if db_path else DEFAULT_DB_PATH
    initialize_database(path)
    app = FastAPI(
        title="ClimateOS Evidence Passport Local Controlled Prototype Core",
        version="0.1.0",
        description="Local-only candidate workflow prototype. Not operational.",
    )
    app.state.db_path = path
    app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")

    def repo() -> PrototypeRepository:
        return PrototypeRepository(app.state.db_path)

    def require_candidate(record_id: str) -> dict:
        try:
            return repo().get_candidate(record_id)
        except KeyError as exc:
            raise HTTPException(status_code=404, detail="Candidate record not found") from exc

    @app.get("/")
    def index() -> FileResponse:
        return FileResponse(STATIC_DIR / "index.html")

    @app.get("/api/health")
    def health() -> dict:
        return {
            "status": "local prototype ready",
            "boundary_label": BOUNDARY_LABEL,
            "localhost_only": True,
            "operational": False,
        }

    @app.get("/api/candidates")
    def list_candidates() -> list[dict]:
        return repo().list_candidates()

    @app.post("/api/candidates", status_code=201)
    def create_candidate(payload: CandidateCreate) -> dict:
        return repo().create_candidate(payload)

    @app.get("/api/candidates/{record_id}")
    def get_candidate(record_id: str) -> dict:
        return require_candidate(record_id)

    @app.patch("/api/candidates/{record_id}")
    def update_candidate(record_id: str, payload: CandidateUpdate) -> dict:
        require_candidate(record_id)
        return repo().update_candidate(record_id, payload)

    @app.post("/api/candidates/{record_id}/archive")
    def archive_candidate(record_id: str, payload: ReviewTransition) -> dict:
        require_candidate(record_id)
        if payload.new_status != "Archived":
            raise HTTPException(status_code=400, detail="Archive route only accepts Archived status")
        return repo().archive_candidate(record_id, payload.reviewer_label, payload.reason)

    @app.post("/api/candidates/{record_id}/review-transition")
    def review_transition(record_id: str, payload: ReviewTransition) -> dict:
        require_candidate(record_id)
        return repo().transition_status(record_id, payload)

    @app.post("/api/relationships", status_code=201)
    def create_relationship(payload: RelationshipCreate) -> dict:
        try:
            return repo().create_relationship(payload)
        except KeyError as exc:
            raise HTTPException(status_code=404, detail="Linked candidate record not found") from exc

    @app.post("/api/founder-gates", status_code=201)
    def create_founder_gate(payload: FounderGateCreate) -> dict:
        return repo().create_founder_gate(payload)

    @app.get("/api/audit-events")
    def list_audit_events() -> list[dict]:
        return repo().list_audit_events()

    @app.post("/api/model/prompt-bundle")
    def create_prompt_bundle(record_ids: list[str] | None = Body(default=None)) -> dict:
        candidates = repo().list_candidates()
        if record_ids:
            selected = [item for item in candidates if item["id"] in set(record_ids)]
        else:
            selected = candidates[:5]
        return generate_prompt_bundle(selected).model_dump()

    @app.post("/api/model/mock-response")
    def create_mock_response(record_ids: list[str] | None = Body(default=None)) -> dict:
        candidates = repo().list_candidates()
        selected = [item for item in candidates if not record_ids or item["id"] in set(record_ids)]
        bundle = generate_prompt_bundle(selected[:5])
        return deterministic_mock_response(bundle).model_dump()

    @app.post("/api/model/import-response", status_code=201)
    def import_model_response(payload: ModelResponseImport) -> list[dict]:
        return repo().import_model_response(payload)

    @app.post("/api/model/suggestions/{suggestion_id}/decision")
    def decide_suggestion(suggestion_id: str, payload: SuggestionDecision) -> dict:
        try:
            return repo().decide_suggestion(suggestion_id, payload)
        except KeyError as exc:
            raise HTTPException(status_code=404, detail="Suggestion not found") from exc

    @app.post("/api/archive/export", status_code=201)
    def export_archive(payload: ArchiveRequest) -> dict:
        return generate_archive_bundle(repo(), payload)

    return app


def assert_allowed_host(host: str) -> str:
    return validate_local_host(host)
