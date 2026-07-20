"""SQLite persistence and append-only audit for the minimum runtime."""

from __future__ import annotations

import json
import sqlite3
from contextlib import contextmanager
from pathlib import Path
from typing import Iterator

from .contracts import BOUNDARY_LABEL, canonical_json, digest

SCHEMA_VERSION = 1


class StoreError(ValueError):
    pass


def connect(path: str | Path) -> sqlite3.Connection:
    db_path = Path(path)
    db_path.parent.mkdir(parents=True, exist_ok=True)
    connection = sqlite3.connect(db_path, timeout=2)
    connection.row_factory = sqlite3.Row
    connection.execute("PRAGMA foreign_keys = ON")
    connection.execute("PRAGMA busy_timeout = 2000")
    return connection


@contextmanager
def managed_connection(path: str | Path) -> Iterator[sqlite3.Connection]:
    connection = connect(path)
    try:
        with connection:
            yield connection
    finally:
        connection.close()


@contextmanager
def transaction(path: str | Path) -> Iterator[sqlite3.Connection]:
    connection = connect(path)
    try:
        connection.execute("BEGIN IMMEDIATE")
        yield connection
        connection.commit()
    except BaseException:
        connection.rollback()
        raise
    finally:
        connection.close()


def initialize(path: str | Path) -> None:
    with managed_connection(path) as connection:
        connection.executescript(
            """
            CREATE TABLE IF NOT EXISTS schema_version (
                version INTEGER PRIMARY KEY,
                applied_at TEXT NOT NULL
            );
            CREATE TABLE IF NOT EXISTS scientist_sessions (
                session_id TEXT PRIMARY KEY,
                state TEXT NOT NULL,
                record_json TEXT NOT NULL,
                created_at TEXT NOT NULL,
                updated_at TEXT NOT NULL
            );
            CREATE TABLE IF NOT EXISTS scientist_audit_events (
                sequence_number INTEGER PRIMARY KEY AUTOINCREMENT,
                event_id TEXT NOT NULL UNIQUE,
                session_id TEXT NOT NULL,
                event_type TEXT NOT NULL,
                actor_role TEXT NOT NULL,
                state_before TEXT NOT NULL,
                state_after TEXT NOT NULL,
                detail_json TEXT NOT NULL,
                predecessor_digest TEXT NOT NULL,
                event_digest TEXT NOT NULL,
                created_at TEXT NOT NULL,
                boundary_label TEXT NOT NULL,
                FOREIGN KEY (session_id) REFERENCES scientist_sessions(session_id)
            );
            CREATE INDEX IF NOT EXISTS idx_scientist_audit_session
                ON scientist_audit_events(session_id, sequence_number);
            """
        )
        connection.execute(
            "INSERT OR IGNORE INTO schema_version(version, applied_at) VALUES (?, datetime('now'))",
            (SCHEMA_VERSION,),
        )


class RuntimeStore:
    def __init__(self, db_path: str | Path) -> None:
        self.db_path = Path(db_path)
        initialize(self.db_path)

    def close(self) -> None:
        """Close store resources; every connection is operation-scoped."""
        return None

    def create(self, record: dict) -> None:
        with transaction(self.db_path) as connection:
            connection.execute(
                "INSERT INTO scientist_sessions(session_id,state,record_json,created_at,updated_at) VALUES(?,?,?,?,?)",
                (record["session_id"], record["state"], canonical_json(record), record["created_at"], record["updated_at"]),
            )

    def import_exported_session(self, exported: dict) -> None:
        """Restore one trusted local export so a later human can append review.

        The existing audit chain is verified before any row is written. This is
        a local continuation path, not an admission path for external evidence.
        """
        record = dict(exported)
        events = record.pop("audit_events", None)
        if not isinstance(events, list) or not events:
            raise StoreError("exported session must include its audit events")
        if record.get("boundary_label") != BOUNDARY_LABEL:
            raise StoreError("exported session boundary changed")
        predecessor = "GENESIS"
        for expected_sequence, event in enumerate(events, start=1):
            if event.get("sequence_number") != expected_sequence:
                raise StoreError("exported audit sequence is incomplete")
            body = {key: event[key] for key in (
                "event_id", "session_id", "event_type", "actor_role", "state_before",
                "state_after", "detail", "predecessor_digest", "created_at", "boundary_label"
            )}
            if event["session_id"] != record.get("session_id"):
                raise StoreError("exported audit session identity mismatch")
            if event["predecessor_digest"] != predecessor or digest(body) != event.get("event_digest"):
                raise StoreError("exported audit chain verification failed")
            predecessor = event["event_digest"]
        record["audit_chain_valid"] = True
        with transaction(self.db_path) as connection:
            exists = connection.execute(
                "SELECT 1 FROM scientist_sessions WHERE session_id=?", (record["session_id"],)
            ).fetchone()
            if exists is not None:
                raise StoreError("session already exists")
            connection.execute(
                "INSERT INTO scientist_sessions(session_id,state,record_json,created_at,updated_at) VALUES(?,?,?,?,?)",
                (record["session_id"], record["state"], canonical_json(record), record["created_at"], record["updated_at"]),
            )
            for event in events:
                connection.execute(
                    """INSERT INTO scientist_audit_events
                    (sequence_number,event_id,session_id,event_type,actor_role,state_before,state_after,
                     detail_json,predecessor_digest,event_digest,created_at,boundary_label)
                    VALUES(?,?,?,?,?,?,?,?,?,?,?,?)""",
                    (
                        event["sequence_number"], event["event_id"], event["session_id"],
                        event["event_type"], event["actor_role"], event["state_before"],
                        event["state_after"], canonical_json(event["detail"]),
                        event["predecessor_digest"], event["event_digest"], event["created_at"],
                        event["boundary_label"],
                    ),
                )
        if not self.verify_audit_chain(record["session_id"]):
            raise StoreError("imported audit chain failed post-write verification")

    def get(self, session_id: str) -> dict:
        with managed_connection(self.db_path) as connection:
            row = connection.execute(
                "SELECT record_json FROM scientist_sessions WHERE session_id = ?", (session_id,)
            ).fetchone()
        if row is None:
            raise KeyError(session_id)
        return json.loads(row["record_json"])

    def update_and_audit(
        self,
        record: dict,
        *,
        event_id: str,
        event_type: str,
        actor_role: str,
        state_before: str,
        detail: dict,
    ) -> dict:
        session_id = record["session_id"]
        with transaction(self.db_path) as connection:
            current = connection.execute(
                "SELECT state FROM scientist_sessions WHERE session_id = ?", (session_id,)
            ).fetchone()
            if current is None:
                raise KeyError(session_id)
            if state_before != "NONE" and current["state"] != state_before:
                raise StoreError(
                    f"stale session transition: stored={current['state']} expected={state_before}"
                )
            predecessor = connection.execute(
                "SELECT event_digest FROM scientist_audit_events WHERE session_id = ? ORDER BY sequence_number DESC LIMIT 1",
                (session_id,),
            ).fetchone()
            predecessor_digest = predecessor["event_digest"] if predecessor else "GENESIS"
            event_body = {
                "event_id": event_id,
                "session_id": session_id,
                "event_type": event_type,
                "actor_role": actor_role,
                "state_before": state_before,
                "state_after": record["state"],
                "detail": detail,
                "predecessor_digest": predecessor_digest,
                "created_at": record["updated_at"],
                "boundary_label": BOUNDARY_LABEL,
            }
            event_digest = digest(event_body)
            cursor = connection.execute(
                """INSERT INTO scientist_audit_events
                (event_id,session_id,event_type,actor_role,state_before,state_after,detail_json,
                 predecessor_digest,event_digest,created_at,boundary_label)
                VALUES(?,?,?,?,?,?,?,?,?,?,?)""",
                (
                    event_id,
                    session_id,
                    event_type,
                    actor_role,
                    state_before,
                    record["state"],
                    canonical_json(detail),
                    predecessor_digest,
                    event_digest,
                    record["updated_at"],
                    BOUNDARY_LABEL,
                ),
            )
            connection.execute(
                "UPDATE scientist_sessions SET state=?,record_json=?,updated_at=? WHERE session_id=?",
                (record["state"], canonical_json(record), record["updated_at"], session_id),
            )
        return {
            **event_body,
            "sequence_number": cursor.lastrowid,
            "event_digest": event_digest,
        }

    def audit_events(self, session_id: str) -> list[dict]:
        with managed_connection(self.db_path) as connection:
            rows = connection.execute(
                "SELECT * FROM scientist_audit_events WHERE session_id=? ORDER BY sequence_number", (session_id,)
            ).fetchall()
        return [
            {
                "sequence_number": row["sequence_number"],
                "event_id": row["event_id"],
                "session_id": row["session_id"],
                "event_type": row["event_type"],
                "actor_role": row["actor_role"],
                "state_before": row["state_before"],
                "state_after": row["state_after"],
                "detail": json.loads(row["detail_json"]),
                "predecessor_digest": row["predecessor_digest"],
                "event_digest": row["event_digest"],
                "created_at": row["created_at"],
                "boundary_label": row["boundary_label"],
            }
            for row in rows
        ]

    def verify_audit_chain(self, session_id: str) -> bool:
        predecessor = "GENESIS"
        for event in self.audit_events(session_id):
            body = {key: event[key] for key in (
                "event_id", "session_id", "event_type", "actor_role", "state_before",
                "state_after", "detail", "predecessor_digest", "created_at", "boundary_label"
            )}
            if event["predecessor_digest"] != predecessor or digest(body) != event["event_digest"]:
                return False
            predecessor = event["event_digest"]
        return True
