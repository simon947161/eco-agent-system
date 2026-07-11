import copy
import json
from pathlib import Path

from .alpha_runtime import (
    ALPHA_BOUNDARY,
    AlphaReviewAction,
    AlphaRollbackRequest,
    AlphaRuntimeStore,
    DeliberationCreate,
    EvidenceContractCreate,
)
from .database import connect, write_transaction


SYNTHETIC_CROSS_DOMAIN_SCENARIOS = [
    {
        "id": "SYNTH-CLIMATE-WATER-001",
        "domains": ["climate", "water"],
        "title": "Synthetic rainfall timing and catchment response",
        "uncertainty": "Timing and catchment response are invented for review-flow testing.",
        "boundary": "Synthetic / Public-safe / No environmental conclusion",
    },
    {
        "id": "SYNTH-WATER-LAND-001",
        "domains": ["water", "land"],
        "title": "Synthetic soil moisture and runoff interaction",
        "uncertainty": "Values are fixtures and do not describe a real place.",
        "boundary": "Synthetic / Public-safe / No environmental conclusion",
    },
    {
        "id": "SYNTH-LAND-BIODIVERSITY-001",
        "domains": ["land", "biodiversity"],
        "title": "Synthetic habitat condition challenge",
        "uncertainty": "Species and habitat signals are deliberately non-real.",
        "boundary": "Synthetic / Public-safe / No biodiversity conclusion",
    },
    {
        "id": "SYNTH-ENERGY-CLIMATE-001",
        "domains": ["energy", "climate"],
        "title": "Synthetic energy demand and heat challenge",
        "uncertainty": "Demand and weather signals are fabricated fixtures.",
        "boundary": "Synthetic / Public-safe / No energy or climate conclusion",
    },
]


def _canonical_json(value: dict) -> str:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


class PersistentAlphaRuntimeStore(AlphaRuntimeStore):
    """SQLite-backed, localhost-only Alpha review store.

    The inherited transition rules remain authoritative. This adapter persists
    every accepted state and every audit event without deleting prior history.
    """

    def __init__(self, db_path: str | Path) -> None:
        super().__init__()
        self.db_path = Path(db_path)
        self._load()

    def _load(self) -> None:
        with connect(self.db_path) as connection:
            evidence_rows = connection.execute(
                "SELECT record_json FROM alpha_evidence_contracts ORDER BY created_at, id"
            ).fetchall()
            deliberation_rows = connection.execute(
                "SELECT record_json FROM alpha_deliberations ORDER BY created_at, id"
            ).fetchall()
            audit_rows = connection.execute(
                "SELECT * FROM alpha_audit_events ORDER BY sequence_number"
            ).fetchall()
        self._evidence = {item["id"]: item for item in (json.loads(row["record_json"]) for row in evidence_rows)}
        self._deliberations = {
            item["id"]: item for item in (json.loads(row["record_json"]) for row in deliberation_rows)
        }
        self._audit = [
            {
                "id": row["id"],
                "sequence_number": row["sequence_number"],
                "event_type": row["event_type"],
                "actor_label": row["actor_label"],
                "record_id": row["record_id"],
                "detail": json.loads(row["detail_json"]),
                "created_at": row["created_at"],
                "boundary_label": row["boundary_label"],
            }
            for row in audit_rows
        ]

    def _audit_event(self, event_type: str, actor_label: str, record_id: str, detail: dict) -> dict:
        event = super()._audit_event(event_type, actor_label, record_id, detail)
        with write_transaction(self.db_path) as connection:
            cursor = connection.execute(
                """INSERT INTO alpha_audit_events
                (id, event_type, actor_label, record_id, detail_json, created_at, boundary_label)
                VALUES (?, ?, ?, ?, ?, ?, ?)""",
                (
                    event["id"], event_type, actor_label, record_id,
                    _canonical_json(detail), event["created_at"], ALPHA_BOUNDARY,
                ),
            )
            event["sequence_number"] = cursor.lastrowid
        self._audit[-1] = copy.deepcopy(event)
        return event

    def _persist_evidence(self, record: dict) -> None:
        with write_transaction(self.db_path) as connection:
            connection.execute(
                """INSERT INTO alpha_evidence_contracts
                (id, domain, state, revision, record_json, created_at, updated_at)
                VALUES (?, ?, ?, ?, ?, ?, ?)
                ON CONFLICT(id) DO UPDATE SET
                    domain=excluded.domain, state=excluded.state,
                    revision=excluded.revision, record_json=excluded.record_json,
                    updated_at=excluded.updated_at""",
                (
                    record["id"], record["domain"], record["state"], record["revision"],
                    _canonical_json(record), record["created_at"], record["updated_at"],
                ),
            )
            connection.execute(
                """INSERT OR IGNORE INTO alpha_evidence_revisions
                (evidence_id, revision, snapshot_json, created_at) VALUES (?, ?, ?, ?)""",
                (record["id"], record["revision"], _canonical_json(record), record["updated_at"]),
            )

    def capabilities(self) -> dict:
        result = super().capabilities()
        result.update({"persistent": True, "restart_clears_state": False, "schema_version": 3})
        result["capabilities"] = [
            item.replace("append-only-in-memory-audit", "append-only-sqlite-audit")
            for item in result["capabilities"]
        ] + ["restart-recovery", "persistent-revision-replay"]
        return result

    def scenarios(self) -> list[dict]:
        return copy.deepcopy(SYNTHETIC_CROSS_DOMAIN_SCENARIOS)

    def create_evidence(self, payload: EvidenceContractCreate) -> dict:
        record = super().create_evidence(payload)
        self._persist_evidence(record)
        return record

    def review_evidence(self, record_id: str, payload: AlphaReviewAction) -> dict:
        record = super().review_evidence(record_id, payload)
        self._persist_evidence(record)
        return record

    def rollback_evidence(self, record_id: str, payload: AlphaRollbackRequest) -> dict:
        record = super().rollback_evidence(record_id, payload)
        self._persist_evidence(record)
        return record

    def create_deliberation(self, payload: DeliberationCreate) -> dict:
        record = super().create_deliberation(payload)
        with write_transaction(self.db_path) as connection:
            connection.execute(
                "INSERT INTO alpha_deliberations (id, record_json, created_at) VALUES (?, ?, ?)",
                (record["id"], _canonical_json(record), record["created_at"]),
            )
        return record

    def diagnostics(self) -> dict:
        result = super().diagnostics()
        with connect(self.db_path) as connection:
            revision_count = connection.execute(
                "SELECT COUNT(*) AS count FROM alpha_evidence_revisions"
            ).fetchone()["count"]
            persisted_audit_count = connection.execute(
                "SELECT COUNT(*) AS count FROM alpha_audit_events"
            ).fetchone()["count"]
        result.update(
            {
                "persistent": True,
                "restart_clears_state": False,
                "revision_snapshot_count": revision_count,
                "persisted_audit_count": persisted_audit_count,
                "persistence_counts_match": persisted_audit_count == len(self._audit),
            }
        )
        if not result["persistence_counts_match"]:
            result["status"] = "unhealthy"
        return result
