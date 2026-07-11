from pathlib import Path

from fastapi import Body, FastAPI, HTTPException, Query, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles

from .alpha_runtime import (
    AlphaReviewAction,
    AlphaRollbackRequest,
    AlphaRuntimeStore,
    DeliberationCreate,
    EvidenceContractCreate,
    InvalidAlphaTransitionError,
)
from .archive import generate_archive_bundle
from .config import BOUNDARY_LABEL, DEFAULT_DB_PATH, MAX_REQUEST_BYTES, STATIC_DIR, validate_local_host
from .database import initialize_database
from .diagnostics import run_data_integrity_diagnostics, safe_integrity_check
from .maintenance import create_backup, restore_backup, validate_backup
from .migrations import migrate_database, migration_preflight
from .model_bridge import deterministic_mock_response, generate_prompt_bundle
from .repository import DuplicateModelResponseError, DuplicateRelationshipError, PrototypeRepository
from .schemas import (
    ArchiveRequest,
    BackupRequest,
    CandidateCreate,
    CandidateUpdate,
    FounderGateCreate,
    MigrationRequest,
    ModelResponseImport,
    RelationshipCreate,
    RestoreRequest,
    ReviewTransition,
    SuggestionDecision,
)
from .state_machine import InvalidTransitionError


def create_app(db_path: str | Path | None = None) -> FastAPI:
    path = Path(db_path) if db_path else DEFAULT_DB_PATH
    initialize_database(path)
    app = FastAPI(
        title="ClimateOS Evidence Passport Local Controlled Prototype Core",
        version="0.1.0",
        description="Local-only candidate workflow prototype. Not operational.",
    )
    app.state.db_path = path
    app.state.alpha_runtime = AlphaRuntimeStore()
    app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")

    @app.middleware("http")
    async def local_security_controls(request: Request, call_next):
        host = request.headers.get("host", "").split(":")[0]
        if host and host not in {"127.0.0.1", "localhost", "testserver"}:
            return JSONResponse(status_code=400, content={"error": "invalid_host", "detail": "Local prototype accepts localhost requests only."})
        content_length = request.headers.get("content-length")
        if content_length and int(content_length) > MAX_REQUEST_BYTES:
            return JSONResponse(status_code=413, content={"error": "request_too_large", "detail": "Request exceeds local prototype size limit."})
        response = await call_next(request)
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["Referrer-Policy"] = "no-referrer"
        response.headers["Cache-Control"] = "no-store"
        return response

    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(request: Request, exc: RequestValidationError):
        errors = []
        for error in exc.errors():
            sanitized = dict(error)
            if "ctx" in sanitized:
                sanitized["ctx"] = {key: str(value) for key, value in sanitized["ctx"].items()}
            errors.append(sanitized)
        return JSONResponse(
            status_code=422,
            content={"error": "validation_error", "detail": errors},
        )

    def repo() -> PrototypeRepository:
        return PrototypeRepository(app.state.db_path)

    def alpha() -> AlphaRuntimeStore:
        return app.state.alpha_runtime

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

    @app.get("/api/alpha/capabilities")
    def alpha_capabilities() -> dict:
        return alpha().capabilities()

    @app.get("/api/alpha/domains")
    def alpha_domains() -> list[dict]:
        return alpha().domains()

    @app.post("/api/alpha/evidence-contracts", status_code=201)
    def alpha_create_evidence(payload: EvidenceContractCreate) -> dict:
        return alpha().create_evidence(payload)

    @app.get("/api/alpha/evidence-contracts")
    def alpha_list_evidence() -> list[dict]:
        return alpha().list_evidence()

    @app.get("/api/alpha/evidence-contracts/{record_id}")
    def alpha_get_evidence(record_id: str) -> dict:
        try:
            return alpha().get_evidence(record_id)
        except KeyError as exc:
            raise HTTPException(status_code=404, detail="Alpha evidence contract not found") from exc

    @app.post("/api/alpha/evidence-contracts/{record_id}/review-actions")
    def alpha_review_evidence(record_id: str, payload: AlphaReviewAction) -> dict:
        try:
            return alpha().review_evidence(record_id, payload)
        except KeyError as exc:
            raise HTTPException(status_code=404, detail="Alpha evidence contract not found") from exc
        except InvalidAlphaTransitionError as exc:
            raise HTTPException(status_code=409, detail=str(exc)) from exc

    @app.post("/api/alpha/evidence-contracts/{record_id}/rollback")
    def alpha_rollback_evidence(record_id: str, payload: AlphaRollbackRequest) -> dict:
        try:
            return alpha().rollback_evidence(record_id, payload)
        except KeyError as exc:
            raise HTTPException(status_code=404, detail="Alpha evidence contract not found") from exc
        except InvalidAlphaTransitionError as exc:
            raise HTTPException(status_code=409, detail=str(exc)) from exc

    @app.post("/api/alpha/deliberations", status_code=201)
    def alpha_create_deliberation(payload: DeliberationCreate) -> dict:
        try:
            return alpha().create_deliberation(payload)
        except KeyError as exc:
            raise HTTPException(status_code=404, detail=f"Linked alpha evidence contract not found: {exc}") from exc

    @app.get("/api/alpha/deliberations")
    def alpha_list_deliberations() -> list[dict]:
        return alpha().list_deliberations()

    @app.get("/api/alpha/audit-events")
    def alpha_audit_events() -> list[dict]:
        return alpha().audit_events()

    @app.get("/api/alpha/diagnostics")
    def alpha_diagnostics() -> dict:
        return alpha().diagnostics()

    @app.get("/api/candidates")
    def list_candidates(
        record_type: str | None = None,
        status: str | None = None,
        risk_flag: str | None = None,
        q: str | None = Query(default=None, max_length=120),
        limit: int = Query(default=250, ge=1, le=1000),
        offset: int = Query(default=0, ge=0),
    ) -> list[dict]:
        return repo().list_candidates(record_type, status, risk_flag, q, limit, offset)

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
        try:
            return repo().transition_status(record_id, payload)
        except InvalidTransitionError as exc:
            repo().audit("blocked_status_transition", "system_validation", payload.reviewer_label, record_id, {"reason": str(exc)})
            raise HTTPException(status_code=409, detail=str(exc)) from exc

    @app.post("/api/relationships", status_code=201)
    def create_relationship(payload: RelationshipCreate) -> dict:
        try:
            return repo().create_relationship(payload)
        except KeyError as exc:
            raise HTTPException(status_code=404, detail="Linked candidate record not found") from exc
        except DuplicateRelationshipError as exc:
            raise HTTPException(status_code=409, detail=str(exc)) from exc

    @app.post("/api/founder-gates", status_code=201)
    def create_founder_gate(payload: FounderGateCreate) -> dict:
        try:
            return repo().create_founder_gate(payload)
        except KeyError as exc:
            raise HTTPException(status_code=404, detail=f"Referenced record or prior gate not found: {exc}") from exc

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
        try:
            return repo().import_model_response(payload)
        except DuplicateModelResponseError as exc:
            raise HTTPException(status_code=409, detail=str(exc)) from exc

    @app.post("/api/model/import-preview")
    def preview_model_response(payload: ModelResponseImport) -> dict:
        return repo().preview_model_response(payload)

    @app.post("/api/model/suggestions/{suggestion_id}/decision")
    def decide_suggestion(suggestion_id: str, payload: SuggestionDecision) -> dict:
        try:
            return repo().decide_suggestion(suggestion_id, payload)
        except KeyError as exc:
            raise HTTPException(status_code=404, detail="Suggestion not found") from exc

    @app.post("/api/archive/export", status_code=201)
    def export_archive(payload: ArchiveRequest) -> dict:
        try:
            return generate_archive_bundle(repo(), payload)
        except ValueError as exc:
            raise HTTPException(status_code=400, detail=str(exc)) from exc

    @app.get("/api/maintenance/integrity")
    def integrity_check() -> dict:
        return safe_integrity_check(app.state.db_path)

    @app.get("/api/maintenance/diagnostics")
    def diagnostics() -> dict:
        return run_data_integrity_diagnostics(app.state.db_path)

    @app.post("/api/maintenance/backup", status_code=201)
    def backup_database(payload: BackupRequest) -> dict:
        return create_backup(app.state.db_path, label=payload.label, actor_label=payload.actor_label)

    @app.post("/api/maintenance/backup/validate")
    def validate_backup_route(backup_dir: str = Body(..., embed=True)) -> dict:
        return validate_backup(backup_dir)

    @app.post("/api/maintenance/restore")
    def restore_database(payload: RestoreRequest) -> dict:
        target = Path(payload.target_db_path) if payload.target_db_path else app.state.db_path
        try:
            return restore_backup(payload.backup_dir, target, actor_label=payload.actor_label)
        except ValueError as exc:
            raise HTTPException(status_code=400, detail=str(exc)) from exc

    @app.get("/api/maintenance/migration/preflight")
    def migration_preflight_route() -> dict:
        return migration_preflight(app.state.db_path)

    @app.post("/api/maintenance/migration/run")
    def migration_run_route(payload: MigrationRequest) -> dict:
        try:
            return migrate_database(app.state.db_path, dry_run=payload.dry_run, actor_label=payload.actor_label)
        except ValueError as exc:
            raise HTTPException(status_code=400, detail=str(exc)) from exc

    return app


def assert_allowed_host(host: str) -> str:
    return validate_local_host(host)
