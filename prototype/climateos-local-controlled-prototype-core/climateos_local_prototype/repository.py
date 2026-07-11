import json
import sqlite3
import uuid
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from .config import BOUNDARY_LABEL
from .database import connect, initialize_database, write_transaction
from .schemas import (
    CandidateCreate,
    CandidateUpdate,
    FounderGateCreate,
    ModelResponseImport,
    RelationshipCreate,
    ReviewTransition,
    SuggestionDecision,
)
from .state_machine import InvalidTransitionError, validate_transition


def now_iso() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def new_id(prefix: str) -> str:
    return f"{prefix}-{uuid.uuid4().hex[:12]}"


def _json(value: Any) -> str:
    return json.dumps(value, ensure_ascii=True, sort_keys=True)


def _list(value: str) -> list[Any]:
    return json.loads(value or "[]")


def _row_to_candidate(row: Any) -> dict[str, Any]:
    return {
        "id": row["id"],
        "record_type": row["record_type"],
        "title": row["title"],
        "status": row["status"],
        "summary": row["summary"],
        "source_ids": _list(row["source_ids"]),
        "signal_ids": _list(row["signal_ids"]),
        "claim_ids": _list(row["claim_ids"]),
        "knowledge_object_ids": _list(row["knowledge_object_ids"]),
        "evidence_ids": _list(row["evidence_ids"]),
        "readiness_label": row["readiness_label"],
        "risk_flags": _list(row["risk_flags"]),
        "human_review_need": row["human_review_need"],
        "founder_gate_need": row["founder_gate_need"],
        "boundary_label": row["boundary_label"],
        "created_at": row["created_at"],
        "updated_at": row["updated_at"],
        "archived_at": row["archived_at"],
    }


class DuplicateModelResponseError(ValueError):
    pass


class DuplicateRelationshipError(ValueError):
    pass


class PrototypeRepository:
    def __init__(self, db_path: str | Path):
        self.db_path = Path(db_path)
        initialize_database(self.db_path)

    def _build_audit_event(
        self,
        event_type: str,
        actor_type: str,
        actor_label: str,
        record_id: str | None,
        detail: dict[str, Any],
    ) -> dict[str, Any]:
        return {
            "id": new_id("AUD"),
            "event_type": event_type,
            "actor_type": actor_type,
            "actor_label": actor_label,
            "record_id": record_id,
            "detail_json": _json(detail),
            "operation_id": new_id("OP"),
            "created_at": now_iso(),
        }

    @staticmethod
    def _insert_audit_event(connection: sqlite3.Connection, event: dict[str, Any]) -> None:
        event["sequence_number"] = connection.execute(
            "SELECT COALESCE(MAX(sequence_number), 0) + 1 AS sequence_number FROM audit_events"
        ).fetchone()["sequence_number"]
        connection.execute(
            """
            INSERT INTO audit_events
            (id, event_type, actor_type, actor_label, record_id, detail_json,
             sequence_number, operation_id, created_at)
            VALUES (:id, :event_type, :actor_type, :actor_label, :record_id, :detail_json,
             :sequence_number, :operation_id, :created_at)
            """,
            event,
        )

    def audit(
        self,
        event_type: str,
        actor_type: str,
        actor_label: str,
        record_id: str | None,
        detail: dict[str, Any],
    ) -> dict[str, Any]:
        event = self._build_audit_event(
            event_type, actor_type, actor_label, record_id, detail
        )
        with write_transaction(self.db_path) as connection:
            self._insert_audit_event(connection, event)
        return event

    def create_candidate(
        self,
        payload: CandidateCreate,
        actor_label: str = "local manual entry",
        record_id: str | None = None,
    ) -> dict[str, Any]:
        timestamp = now_iso()
        candidate = {
            "id": record_id or new_id("REC"),
            "record_type": payload.record_type,
            "title": payload.title,
            "status": payload.status,
            "summary": payload.summary,
            "source_ids": _json(payload.source_ids),
            "signal_ids": _json(payload.signal_ids),
            "claim_ids": _json(payload.claim_ids),
            "knowledge_object_ids": _json(payload.knowledge_object_ids),
            "evidence_ids": _json(payload.evidence_ids),
            "readiness_label": payload.readiness_label,
            "risk_flags": _json(payload.risk_flags),
            "human_review_need": payload.human_review_need,
            "founder_gate_need": payload.founder_gate_need,
            "boundary_label": BOUNDARY_LABEL,
            "created_at": timestamp,
            "updated_at": timestamp,
            "archived_at": None,
        }
        audit_event = self._build_audit_event(
            "candidate_created",
            "human_action",
            actor_label,
            candidate["id"],
            {"record_type": payload.record_type, "status": payload.status},
        )
        with write_transaction(self.db_path) as connection:
            connection.execute(
                """
                INSERT INTO candidate_records
                (id, record_type, title, status, summary, source_ids, signal_ids, claim_ids,
                 knowledge_object_ids, evidence_ids, readiness_label, risk_flags, human_review_need,
                 founder_gate_need, boundary_label, created_at, updated_at, archived_at)
                VALUES
                (:id, :record_type, :title, :status, :summary, :source_ids, :signal_ids, :claim_ids,
                 :knowledge_object_ids, :evidence_ids, :readiness_label, :risk_flags, :human_review_need,
                 :founder_gate_need, :boundary_label, :created_at, :updated_at, :archived_at)
                """,
                candidate,
            )
            self._insert_audit_event(connection, audit_event)
        return self.get_candidate(candidate["id"])

    def list_candidates(
        self,
        record_type: str | None = None,
        status: str | None = None,
        risk_flag: str | None = None,
        text_query: str | None = None,
        limit: int = 250,
        offset: int = 0,
    ) -> list[dict[str, Any]]:
        limit = max(1, min(limit, 1000))
        offset = max(0, offset)
        where: list[str] = []
        values: list[Any] = []
        if record_type:
            where.append("record_type = ?")
            values.append(record_type)
        if status:
            where.append("status = ?")
            values.append(status)
        if risk_flag:
            where.append("risk_flags LIKE ?")
            values.append(f"%{risk_flag}%")
        if text_query:
            where.append("(title LIKE ? OR summary LIKE ?)")
            values.extend([f"%{text_query}%", f"%{text_query}%"])
        where_sql = f"WHERE {' AND '.join(where)}" if where else ""
        values.extend([limit, offset])
        with connect(self.db_path) as connection:
            rows = connection.execute(
                f"SELECT * FROM candidate_records {where_sql} ORDER BY created_at, id LIMIT ? OFFSET ?",
                tuple(values),
            ).fetchall()
        return [_row_to_candidate(row) for row in rows]

    def get_candidate(self, record_id: str) -> dict[str, Any]:
        with connect(self.db_path) as connection:
            row = connection.execute(
                "SELECT * FROM candidate_records WHERE id = ?", (record_id,)
            ).fetchone()
        if row is None:
            raise KeyError(record_id)
        return _row_to_candidate(row)

    def update_candidate(
        self,
        record_id: str,
        payload: CandidateUpdate,
        actor_label: str = "local manual entry",
    ) -> dict[str, Any]:
        current = self.get_candidate(record_id)
        update = payload.model_dump(exclude_unset=True)
        if not update:
            return current

        json_fields = {
            "source_ids",
            "signal_ids",
            "claim_ids",
            "knowledge_object_ids",
            "evidence_ids",
            "risk_flags",
        }
        assignments: list[str] = []
        values: list[Any] = []
        for key, value in update.items():
            assignments.append(f"{key} = ?")
            values.append(_json(value) if key in json_fields else value)
        assignments.append("updated_at = ?")
        values.append(now_iso())
        values.append(record_id)

        with connect(self.db_path) as connection:
            connection.execute(
                f"UPDATE candidate_records SET {', '.join(assignments)} WHERE id = ?",
                tuple(values),
            )
        self.audit("candidate_revised", "human_action", actor_label, record_id, update)
        return self.get_candidate(record_id)

    def transition_status(self, record_id: str, payload: ReviewTransition) -> dict[str, Any]:
        current = self.get_candidate(record_id)
        validate_transition(
            current["status"],
            payload.new_status,
            payload.linked_risk_flags,
            payload.founder_gate_trigger,
        )
        timestamp = now_iso()
        review_id = new_id("HR")
        with connect(self.db_path) as connection:
            connection.execute(
                """
                INSERT INTO human_reviews
                (id, record_id, previous_status, new_status, reviewer_label, review_reason,
                 linked_risk_flags, founder_gate_trigger, created_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    review_id,
                    record_id,
                    current["status"],
                    payload.new_status,
                    payload.reviewer_label,
                    payload.reason,
                    _json(payload.linked_risk_flags),
                    payload.founder_gate_trigger,
                    timestamp,
                ),
            )
            connection.execute(
                """
                UPDATE candidate_records
                SET status = ?, updated_at = ?
                WHERE id = ?
                """,
                (payload.new_status, timestamp, record_id),
            )
        self.audit(
            "human_review_transition",
            "human_action",
            payload.reviewer_label,
            record_id,
            {
                "previous_status": current["status"],
                "new_status": payload.new_status,
                "reason": payload.reason,
                "linked_risk_flags": payload.linked_risk_flags,
                "founder_gate_trigger": payload.founder_gate_trigger,
            },
        )
        return self.get_candidate(record_id)

    def archive_candidate(
        self, record_id: str, reviewer_label: str, reason: str
    ) -> dict[str, Any]:
        transition = ReviewTransition(
            new_status="Archived",
            reviewer_label=reviewer_label,
            reason=reason,
            linked_risk_flags=["RF-ARCHIVE"],
        )
        record = self.transition_status(record_id, transition)
        with connect(self.db_path) as connection:
            connection.execute(
                "UPDATE candidate_records SET archived_at = ?, updated_at = ? WHERE id = ?",
                (now_iso(), now_iso(), record_id),
            )
        self.audit(
            "candidate_archived",
            "human_action",
            reviewer_label,
            record_id,
            {"reason": reason},
        )
        return self.get_candidate(record_id)

    def create_relationship(self, payload: RelationshipCreate) -> dict[str, Any]:
        self.get_candidate(payload.from_record_id)
        self.get_candidate(payload.to_record_id)
        with connect(self.db_path) as connection:
            existing = connection.execute(
                """
                SELECT id FROM relationships
                WHERE from_record_id = ? AND to_record_id = ? AND relationship_type = ?
                LIMIT 1
                """,
                (payload.from_record_id, payload.to_record_id, payload.relationship_type),
            ).fetchone()
        if existing is not None:
            raise DuplicateRelationshipError("Relationship already exists.")
        relationship = {
            "id": new_id("REL"),
            "from_record_id": payload.from_record_id,
            "to_record_id": payload.to_record_id,
            "relationship_type": payload.relationship_type,
            "created_by": payload.created_by,
            "reason": payload.reason,
            "created_at": now_iso(),
        }
        with connect(self.db_path) as connection:
            connection.execute(
                """
                INSERT INTO relationships
                (id, from_record_id, to_record_id, relationship_type, created_by, reason, created_at)
                VALUES (:id, :from_record_id, :to_record_id, :relationship_type, :created_by, :reason, :created_at)
                """,
                relationship,
            )
        self.audit(
            "relationship_created",
            "human_action",
            payload.created_by,
            relationship["id"],
            relationship,
        )
        return relationship

    def create_founder_gate(self, payload: FounderGateCreate) -> dict[str, Any]:
        for record_id in payload.affected_record_ids:
            self.get_candidate(record_id)
        if payload.supersedes_gate_id:
            with connect(self.db_path) as connection:
                prior_gate = connection.execute(
                    "SELECT id FROM founder_gates WHERE id = ?", (payload.supersedes_gate_id,)
                ).fetchone()
            if prior_gate is None:
                raise KeyError(payload.supersedes_gate_id)
        with connect(self.db_path) as connection:
            version_row = connection.execute(
                "SELECT COALESCE(MAX(decision_version), 0) + 1 AS version FROM founder_gates WHERE gate_trigger = ?",
                (payload.gate_trigger,),
            ).fetchone()
        gate = {
            "id": new_id("FG"),
            "gate_trigger": payload.gate_trigger,
            "affected_record_ids": _json(payload.affected_record_ids),
            "decision_date": payload.decision_date,
            "decision_status": payload.decision_status,
            "founder_instruction_text": payload.founder_instruction_text,
            "scope_allowed": payload.scope_allowed,
            "scope_prohibited": payload.scope_prohibited,
            "review_or_expiry_requirement": payload.review_or_expiry_requirement,
            "archive_reference": payload.archive_reference,
            "supersedes_gate_id": payload.supersedes_gate_id,
            "decision_version": version_row["version"],
            "created_at": now_iso(),
        }
        with connect(self.db_path) as connection:
            connection.execute(
                """
                INSERT INTO founder_gates
                (id, gate_trigger, affected_record_ids, decision_date, decision_status,
                 founder_instruction_text, scope_allowed, scope_prohibited,
                 review_or_expiry_requirement, archive_reference, supersedes_gate_id,
                 decision_version, created_at)
                VALUES
                (:id, :gate_trigger, :affected_record_ids, :decision_date, :decision_status,
                 :founder_instruction_text, :scope_allowed, :scope_prohibited,
                 :review_or_expiry_requirement, :archive_reference, :supersedes_gate_id,
                 :decision_version, :created_at)
                """,
                gate,
            )
        self.audit(
            "founder_gate_recorded",
            "founder_instruction",
            "manual founder gate entry",
            gate["id"],
            {
                "decision_status": payload.decision_status,
                "affected_record_ids": payload.affected_record_ids,
            },
        )
        gate["affected_record_ids"] = payload.affected_record_ids
        return gate

    def import_model_response(self, payload: ModelResponseImport) -> list[dict[str, Any]]:
        imported: list[dict[str, Any]] = []
        timestamp = now_iso()
        with connect(self.db_path) as connection:
            existing_response = connection.execute(
                "SELECT 1 FROM model_suggestions WHERE response_id = ? LIMIT 1",
                (payload.response_id,),
            ).fetchone()
            if existing_response is not None:
                raise DuplicateModelResponseError("Model response has already been imported.")
            suggestion_ids = [suggestion.suggestion_id for suggestion in payload.suggestions]
            if suggestion_ids:
                placeholders = ",".join("?" for _ in suggestion_ids)
                existing_suggestion = connection.execute(
                    f"SELECT id FROM model_suggestions WHERE id IN ({placeholders}) LIMIT 1",
                    tuple(suggestion_ids),
                ).fetchone()
                if existing_suggestion is not None:
                    raise DuplicateModelResponseError("Model suggestion has already been imported.")
            for suggestion in payload.suggestions:
                item = {
                    "id": suggestion.suggestion_id,
                    "response_id": payload.response_id,
                    "category": suggestion.category,
                    "target_record_id": suggestion.target_record_id,
                    "suggestion_text": suggestion.suggestion_text,
                    "provenance": suggestion.provenance,
                    "created_at": timestamp,
                }
                try:
                    connection.execute(
                        """
                        INSERT INTO model_suggestions
                        (id, response_id, category, target_record_id, suggestion_text, provenance, created_at)
                        VALUES
                        (:id, :response_id, :category, :target_record_id, :suggestion_text, :provenance, :created_at)
                        """,
                        item,
                    )
                except sqlite3.IntegrityError as exc:
                    raise DuplicateModelResponseError("Model response import conflicts with an existing suggestion.") from exc
                imported.append({**item, "disposition": "pending"})
        self.audit(
            "model_response_imported",
            "imported_suggestion",
            payload.source_label,
            payload.response_id,
            {"suggestion_count": len(imported)},
        )
        return imported

    def preview_model_response(self, payload: ModelResponseImport) -> dict[str, Any]:
        suggestion_ids = [suggestion.suggestion_id for suggestion in payload.suggestions]
        with connect(self.db_path) as connection:
            existing_response = connection.execute(
                "SELECT COUNT(*) AS count FROM model_suggestions WHERE response_id = ?",
                (payload.response_id,),
            ).fetchone()["count"]
            duplicate_suggestions = 0
            if suggestion_ids:
                placeholders = ",".join("?" for _ in suggestion_ids)
                duplicate_suggestions = connection.execute(
                    f"SELECT COUNT(*) AS count FROM model_suggestions WHERE id IN ({placeholders})",
                    tuple(suggestion_ids),
                ).fetchone()["count"]
        return {
            "status": "conflict" if existing_response or duplicate_suggestions else "ready",
            "response_id": payload.response_id,
            "proposed_count": len(payload.suggestions),
            "duplicate_response_count": existing_response,
            "duplicate_suggestion_count": duplicate_suggestions,
            "will_write": False,
        }

    def decide_suggestion(
        self, suggestion_id: str, payload: SuggestionDecision
    ) -> dict[str, Any]:
        timestamp = now_iso()
        with connect(self.db_path) as connection:
            row = connection.execute(
                "SELECT * FROM model_suggestions WHERE id = ?", (suggestion_id,)
            ).fetchone()
            if row is None:
                raise KeyError(suggestion_id)
            connection.execute(
                """
                UPDATE model_suggestions
                SET disposition = ?, reviewer_label = ?, disposition_reason = ?, decided_at = ?
                WHERE id = ?
                """,
                (
                    payload.action,
                    payload.reviewer_label,
                    payload.reason,
                    timestamp,
                    suggestion_id,
                ),
            )
        self.audit(
            "model_suggestion_disposition",
            "human_action",
            payload.reviewer_label,
            suggestion_id,
            {"action": payload.action, "reason": payload.reason},
        )
        return self.get_suggestion(suggestion_id)

    def get_suggestion(self, suggestion_id: str) -> dict[str, Any]:
        with connect(self.db_path) as connection:
            row = connection.execute(
                "SELECT * FROM model_suggestions WHERE id = ?", (suggestion_id,)
            ).fetchone()
        if row is None:
            raise KeyError(suggestion_id)
        return dict(row)

    def list_audit_events(self) -> list[dict[str, Any]]:
        with connect(self.db_path) as connection:
            rows = connection.execute(
                "SELECT * FROM audit_events ORDER BY sequence_number, created_at, id"
            ).fetchall()
        return [dict(row) for row in rows]

    def list_human_reviews(self) -> list[dict[str, Any]]:
        with connect(self.db_path) as connection:
            rows = connection.execute(
                "SELECT * FROM human_reviews ORDER BY created_at, id"
            ).fetchall()
        return [dict(row) for row in rows]

    def list_founder_gates(self) -> list[dict[str, Any]]:
        with connect(self.db_path) as connection:
            rows = connection.execute(
                "SELECT * FROM founder_gates ORDER BY created_at, id"
            ).fetchall()
        gates = []
        for row in rows:
            item = dict(row)
            item["affected_record_ids"] = _list(item["affected_record_ids"])
            gates.append(item)
        return gates

    def record_archive_event(
        self, case_id: str, export_path: str, reviewer_label: str, reason: str
    ) -> dict[str, Any]:
        event = {
            "id": new_id("ARC"),
            "case_id": case_id,
            "export_path": export_path,
            "reviewer_label": reviewer_label,
            "reason": reason,
            "created_at": now_iso(),
        }
        with connect(self.db_path) as connection:
            connection.execute(
                """
                INSERT INTO archive_events
                (id, case_id, export_path, reviewer_label, reason, created_at)
                VALUES (:id, :case_id, :export_path, :reviewer_label, :reason, :created_at)
                """,
                event,
            )
        self.audit(
            "archive_export_created",
            "human_action",
            reviewer_label,
            event["id"],
            {"case_id": case_id, "export_path": export_path, "reason": reason},
        )
        return event
