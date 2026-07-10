import json
import sqlite3
from pathlib import Path
from typing import Any, get_args

from .database import REQUIRED_TABLES, connect, get_schema_version
from .schemas import CandidateStatus


VALID_STATUSES = set(get_args(CandidateStatus))


def _issue(kind: str, severity: str, detail: str, record_id: str = "") -> dict[str, str]:
    return {"kind": kind, "severity": severity, "detail": detail, "record_id": record_id}


def run_data_integrity_diagnostics(db_path: str | Path) -> dict[str, Any]:
    issues: list[dict[str, str]] = []
    with connect(db_path) as connection:
        existing_tables = {
            row["name"]
            for row in connection.execute("SELECT name FROM sqlite_master WHERE type = 'table'").fetchall()
        }
        for table in sorted(REQUIRED_TABLES - existing_tables):
            issues.append(_issue("missing_table", "failed", f"Missing required table: {table}"))
        if issues:
            return {"status": "failed", "schema_version": get_schema_version(connection), "issues": issues}

        for row in connection.execute("PRAGMA foreign_key_check").fetchall():
            issues.append(
                _issue(
                    "foreign_key_violation",
                    "failed",
                    f"Foreign-key violation in {row['table']} row {row['rowid']}.",
                )
            )

        for row in connection.execute(
            "SELECT id, status, archived_at FROM candidate_records"
        ).fetchall():
            if row["status"] not in VALID_STATUSES:
                issues.append(_issue("invalid_status", "failed", f"Invalid candidate status {row['status']}.", row["id"]))
            if row["status"] == "Archived" and not row["archived_at"]:
                issues.append(_issue("archive_state", "warning", "Archived record has no archived_at timestamp.", row["id"]))
            if row["status"] != "Archived" and row["archived_at"]:
                issues.append(_issue("archive_state", "warning", "Non-archived record has archived_at timestamp.", row["id"]))

        duplicate_rows = connection.execute(
            """
            SELECT from_record_id, to_record_id, relationship_type, COUNT(*) AS count
            FROM relationships
            GROUP BY from_record_id, to_record_id, relationship_type
            HAVING COUNT(*) > 1
            """
        ).fetchall()
        for row in duplicate_rows:
            issues.append(
                _issue(
                    "duplicate_relationship",
                    "warning",
                    f"Duplicate relationship {row['from_record_id']}->{row['to_record_id']} ({row['relationship_type']}).",
                )
            )

        for row in connection.execute(
            """
            SELECT human_reviews.id
            FROM human_reviews
            LEFT JOIN candidate_records ON human_reviews.record_id = candidate_records.id
            WHERE candidate_records.id IS NULL
            """
        ).fetchall():
            issues.append(_issue("orphan_human_review", "failed", "Human Review record has no candidate.", row["id"]))

        candidate_ids = {
            row["id"] for row in connection.execute("SELECT id FROM candidate_records").fetchall()
        }
        for row in connection.execute("SELECT id, affected_record_ids FROM founder_gates").fetchall():
            try:
                affected = json.loads(row["affected_record_ids"] or "[]")
            except json.JSONDecodeError:
                issues.append(_issue("founder_gate_reference", "failed", "Founder Gate affected_record_ids is invalid JSON.", row["id"]))
                continue
            for record_id in affected:
                if record_id not in candidate_ids:
                    issues.append(
                        _issue(
                            "founder_gate_reference",
                            "failed",
                            f"Founder Gate references missing candidate {record_id}.",
                            row["id"],
                        )
                    )

        superseded_records = connection.execute(
            "SELECT id FROM candidate_records WHERE status = 'Superseded'"
        ).fetchall()
        for row in superseded_records:
            replacement = connection.execute(
                """
                SELECT id FROM relationships
                WHERE from_record_id = ? AND lower(relationship_type) LIKE '%supersed%'
                LIMIT 1
                """,
                (row["id"],),
            ).fetchone()
            if replacement is None:
                issues.append(_issue("superseded_linkage", "warning", "Superseded record has no replacement linkage.", row["id"]))

    status = "healthy"
    if any(issue["severity"] == "failed" for issue in issues):
        status = "failed"
    elif issues:
        status = "warning"
    with connect(db_path) as connection:
        schema_version = get_schema_version(connection)
    return {"status": status, "schema_version": schema_version, "issues": issues}


def safe_integrity_check(db_path: str | Path) -> dict[str, Any]:
    try:
        with connect(db_path) as connection:
            integrity_rows = [row[0] for row in connection.execute("PRAGMA integrity_check").fetchall()]
            foreign_rows = [dict(row) for row in connection.execute("PRAGMA foreign_key_check").fetchall()]
            status = "healthy" if integrity_rows == ["ok"] and not foreign_rows else "failed"
            return {
                "status": status,
                "integrity_check": integrity_rows,
                "foreign_key_check": foreign_rows,
                "schema_version": get_schema_version(connection),
            }
    except (sqlite3.DatabaseError, OSError) as exc:
        return {"status": "failed", "error": str(exc), "integrity_check": [], "foreign_key_check": []}
