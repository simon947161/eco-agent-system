"""Persistent research programs, monthly cycles and governed source snapshots."""

from __future__ import annotations

import hashlib
import json
import re
import sqlite3
import urllib.request
import uuid
from calendar import monthrange
from datetime import UTC, date, datetime
from pathlib import Path
from threading import RLock
from typing import Any, Callable
from urllib.parse import urlparse

PROGRAM_SCHEMA = "climateos.persistent_research_program.v0.1"
CYCLE_SCHEMA = "climateos.monthly_review_cycle.v0.1"
PROGRAM_ID = "COOMA-WATER-FIRE-WASTEWATER-WATCH"
ALLOWLIST_PATH = Path(__file__).resolve().parent / "official_source_allowlist.json"
MAX_RESPONSE_BYTES = 2 * 1024 * 1024
QUESTION = (
    "I observed less water and snow around Cooma. What could this mean for future bushfire risk "
    "and drinking-water security? What wastewater work exists, what are its practical limits, "
    "and how could wastewater management contribute to climate adaptation?"
)
MODULES = (
    "CLIMATE_AND_SNOW_OUTLOOK",
    "BUSHFIRE_RISK",
    "DRINKING_WATER_SECURITY",
    "WASTEWATER_RESILIENCE",
    "CROSS_SYSTEM_INTEGRATION",
)
OBSERVATION_CATEGORIES = {"WATER", "SNOW", "FIRE", "VEGETATION", "WASTEWATER", "WEATHER", "OTHER"}
REVIEW_DECISIONS = {"ACCEPT_CYCLE", "QUESTION_CYCLE", "REVISE_CYCLE", "REJECT_CYCLE"}


class ProgramContractError(ValueError):
    """Persistent-program input or evidence boundary violation."""


class ProgramStateError(ValueError):
    """Invalid persistent-program lifecycle transition."""


def _now() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def _json(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def _digest(value: Any) -> str:
    payload = value if isinstance(value, bytes) else _json(value).encode("utf-8")
    return "sha256:" + hashlib.sha256(payload).hexdigest()


def _stable_id(prefix: str, value: Any) -> str:
    return f"{prefix}-{hashlib.sha256(_json(value).encode()).hexdigest()[:16].upper()}"


def _require_text(value: Any, label: str, minimum: int = 2, maximum: int = 4000) -> str:
    if not isinstance(value, str) or not minimum <= len(value.strip()) <= maximum:
        raise ProgramContractError(f"{label} must be {minimum}..{maximum} characters of text")
    return value.strip()


def _allowlist() -> dict[str, Any]:
    value = json.loads(ALLOWLIST_PATH.read_text(encoding="utf-8"))
    if value.get("program_id") != PROGRAM_ID or value.get("policy") != {
        "https_only": True,
        "manual_approval_each_refresh": True,
        "raw_content_retained": False,
        "cost_aud": 0,
        "change_is_conclusion": False,
    }:
        raise ProgramContractError("official-source allowlist policy changed")
    sources = value.get("sources", [])
    if not isinstance(sources, list) or not 1 <= len(sources) <= 10:
        raise ProgramContractError("official-source allowlist must contain 1..10 sources")
    source_ids = [source.get("source_id") for source in sources]
    if len(set(source_ids)) != len(source_ids) or any(not item for item in source_ids):
        raise ProgramContractError("official-source identities must be non-empty and unique")
    for source in sources:
        parsed = urlparse(source.get("url", ""))
        if parsed.scheme != "https" or parsed.hostname != source.get("allowed_host"):
            raise ProgramContractError("source URL is outside its exact HTTPS host allowlist")
        if source.get("module") not in MODULES:
            raise ProgramContractError("source module is outside the research program")
    return value


def _default_fetch(source: dict[str, Any]) -> dict[str, Any]:
    request = urllib.request.Request(
        source["url"],
        headers={"User-Agent": "ClimateOS-Evidence-Monitor/0.1 (+human-reviewed; no-raw-retention)"},
    )
    with urllib.request.urlopen(request, timeout=15) as response:
        final_url = response.geturl()
        parsed = urlparse(final_url)
        if parsed.scheme != "https" or parsed.hostname != source["allowed_host"]:
            raise ProgramContractError("source redirected outside its exact allowlisted HTTPS host")
        body = response.read(MAX_RESPONSE_BYTES + 1)
        if len(body) > MAX_RESPONSE_BYTES:
            raise ProgramContractError("source response exceeded 2 MiB ceiling")
        return {
            "http_status": int(response.status),
            "final_url": final_url,
            "content_type": response.headers.get("Content-Type", ""),
            "etag": response.headers.get("ETag"),
            "last_modified": response.headers.get("Last-Modified"),
            "body": body,
        }


class PersistentResearchRuntime:
    def __init__(self, db_path: str | Path) -> None:
        self.db_path = Path(db_path)
        self._cycle_transition_lock = RLock()
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        with self._connect() as db:
            db.executescript("""
                CREATE TABLE IF NOT EXISTS research_programs (
                    program_id TEXT PRIMARY KEY, record_json TEXT NOT NULL, updated_at TEXT NOT NULL
                );
                CREATE TABLE IF NOT EXISTS research_cycles (
                    cycle_id TEXT PRIMARY KEY, program_id TEXT NOT NULL, year_month TEXT NOT NULL,
                    state TEXT NOT NULL, record_json TEXT NOT NULL, updated_at TEXT NOT NULL,
                    FOREIGN KEY(program_id) REFERENCES research_programs(program_id)
                );
                CREATE TABLE IF NOT EXISTS research_observations (
                    observation_id TEXT PRIMARY KEY, cycle_id TEXT NOT NULL, record_json TEXT NOT NULL,
                    created_at TEXT NOT NULL, FOREIGN KEY(cycle_id) REFERENCES research_cycles(cycle_id)
                );
                CREATE TABLE IF NOT EXISTS official_source_snapshots (
                    snapshot_id TEXT PRIMARY KEY, cycle_id TEXT NOT NULL, source_id TEXT NOT NULL,
                    record_json TEXT NOT NULL, fetched_at TEXT NOT NULL,
                    UNIQUE(cycle_id, source_id), FOREIGN KEY(cycle_id) REFERENCES research_cycles(cycle_id)
                );
                CREATE TABLE IF NOT EXISTS annual_research_reports (
                    report_id TEXT PRIMARY KEY, program_id TEXT NOT NULL, report_year INTEGER NOT NULL,
                    record_json TEXT NOT NULL, created_at TEXT NOT NULL,
                    UNIQUE(program_id, report_year),
                    FOREIGN KEY(program_id) REFERENCES research_programs(program_id)
                );
            """)
        self.ensure_cooma_program()

    def _connect(self) -> sqlite3.Connection:
        db = sqlite3.connect(self.db_path, timeout=3)
        db.row_factory = sqlite3.Row
        db.execute("PRAGMA foreign_keys=ON")
        db.execute("PRAGMA busy_timeout=3000")
        return db

    def ensure_cooma_program(self) -> dict[str, Any]:
        try:
            record = self.get_program(PROGRAM_ID)
            record.pop("cycles", None)
            changed = False
            cadence_defaults = {
                "monthly_review": True,
                "monthly_due_rule": "LAST_CALENDAR_DAY",
                "material_event_review": True,
                "annual_report_rule": "AFTER_REVIEWED_DECEMBER_CYCLE",
                "unattended_scheduler_installed": False,
            }
            for key, value in cadence_defaults.items():
                if key not in record["cadence"]:
                    record["cadence"][key] = value
                    changed = True
            if "conversation_bridge_state" not in record["boundaries"]:
                record["boundaries"]["conversation_bridge_state"] = "CONTRACT_DEFINED_NOT_CONNECTED_TO_LOCALHOST"
                changed = True
            if (
                record.get("state") == "ACTIVE_HUMAN_REVIEWED_RESEARCH_PROGRAM"
                and record.get("last_reviewed_cycle_id") is None
            ):
                record["state"] = "ACTIVE_AWAITING_FIRST_HUMAN_REVIEW"
                changed = True
            if changed:
                self._save_program(record)
            return self.get_program(PROGRAM_ID)
        except KeyError:
            now = _now()
            record = {
                "schema_id": PROGRAM_SCHEMA,
                "program_id": PROGRAM_ID,
                "title": "Cooma Water–Fire–Wastewater Living Research Program",
                "question": QUESTION,
                "place_scope": "Cooma / Snowy Monaro public-evidence research scope",
                "modules": list(MODULES),
                "cadence": {
                    "monthly_review": True,
                    "monthly_due_rule": "LAST_CALENDAR_DAY",
                    "material_event_review": True,
                    "annual_report_rule": "AFTER_REVIEWED_DECEMBER_CYCLE",
                    "unattended_scheduler_installed": False,
                },
                "state": "ACTIVE_AWAITING_FIRST_HUMAN_REVIEW",
                "current_hypothesis_version": 0,
                "last_reviewed_cycle_id": None,
                "boundaries": {
                    "public_official_sources_only": True,
                    "human_observations_are_unverified": True,
                    "private_council_or_customer_data_prohibited": True,
                    "automatic_environmental_conclusion": False,
                    "human_review_required": True,
                    "conversation_bridge_state": "CONTRACT_DEFINED_NOT_CONNECTED_TO_LOCALHOST",
                },
                "created_at": now,
                "updated_at": now,
            }
            with self._connect() as db:
                db.execute("INSERT INTO research_programs VALUES(?,?,?)", (PROGRAM_ID, _json(record), now))
            return record

    def get_program(self, program_id: str = PROGRAM_ID) -> dict[str, Any]:
        with self._connect() as db:
            row = db.execute("SELECT record_json FROM research_programs WHERE program_id=?", (program_id,)).fetchone()
        if row is None:
            raise KeyError(program_id)
        record = json.loads(row["record_json"])
        record["cycles"] = self.list_cycles(program_id)
        return record

    def _save_program(self, record: dict[str, Any]) -> None:
        record["updated_at"] = _now()
        with self._connect() as db:
            db.execute("UPDATE research_programs SET record_json=?,updated_at=? WHERE program_id=?", (_json(record), record["updated_at"], record["program_id"]))

    def list_cycles(self, program_id: str = PROGRAM_ID) -> list[dict[str, Any]]:
        with self._connect() as db:
            rows = db.execute("SELECT record_json FROM research_cycles WHERE program_id=? ORDER BY year_month,cycle_id", (program_id,)).fetchall()
        return [json.loads(row["record_json"]) for row in rows]

    def get_cycle(self, cycle_id: str) -> dict[str, Any]:
        with self._connect() as db:
            row = db.execute("SELECT record_json FROM research_cycles WHERE cycle_id=?", (cycle_id,)).fetchone()
        if row is None:
            raise KeyError(cycle_id)
        cycle = json.loads(row["record_json"])
        cycle["observations"] = self.observations(cycle_id)
        cycle["source_snapshots"] = self.source_snapshots(cycle_id)
        return cycle

    def _save_cycle(self, cycle: dict[str, Any]) -> dict[str, Any]:
        cycle["updated_at"] = _now()
        stored = {key: value for key, value in cycle.items() if key not in {"observations", "source_snapshots"}}
        with self._connect() as db:
            db.execute("UPDATE research_cycles SET state=?,record_json=?,updated_at=? WHERE cycle_id=?", (cycle["state"], _json(stored), cycle["updated_at"], cycle["cycle_id"]))
        return self.get_cycle(cycle["cycle_id"])

    def start_cycle(self, year_month: str, program_id: str = PROGRAM_ID, trigger: str = "MONTHLY") -> dict[str, Any]:
        if not re.fullmatch(r"20\d{2}-(0[1-9]|1[0-2])", year_month):
            raise ProgramContractError("year_month must use YYYY-MM")
        if trigger not in {"MONTHLY", "MATERIAL_EVENT"}:
            raise ProgramContractError("trigger must be MONTHLY or MATERIAL_EVENT")
        self.get_program(program_id)
        previous = self.list_cycles(program_id)
        if previous and year_month < previous[-1]["year_month"]:
            raise ProgramStateError("a new cycle cannot precede the latest recorded program month")
        if trigger == "MONTHLY" and any(item["year_month"] == year_month and item["trigger"] == "MONTHLY" for item in previous):
            raise ProgramStateError("this program already has a monthly cycle for that month")
        previous_id = previous[-1]["cycle_id"] if previous else None
        identity = {"program": program_id, "year_month": year_month, "trigger": trigger}
        if trigger == "MATERIAL_EVENT":
            identity["event_nonce"] = uuid.uuid4().hex
        cycle_id = _stable_id("COOMA-CYCLE", identity)
        now = _now()
        year, month = (int(item) for item in year_month.split("-"))
        period_start = date(year, month, 1).isoformat()
        period_end = date(year, month, monthrange(year, month)[1]).isoformat()
        cycle = {
            "schema_id": CYCLE_SCHEMA,
            "cycle_id": cycle_id,
            "program_id": program_id,
            "year_month": year_month,
            "period_start": period_start,
            "period_end": period_end,
            "review_due_on": period_end,
            "trigger": trigger,
            "previous_cycle_id": previous_id,
            "state": "COLLECTING_EVIDENCE",
            "source_refresh_state": "NOT_REQUESTED",
            "source_refresh_started_at": None,
            "source_refresh_completed_at": None,
            "comparison": None,
            "hypothesis_version": None,
            "receipt": None,
            "passport": None,
            "human_review": None,
            "created_at": now,
            "updated_at": now,
        }
        with self._connect() as db:
            db.execute("INSERT INTO research_cycles VALUES(?,?,?,?,?,?)", (cycle_id, program_id, year_month, cycle["state"], _json(cycle), now))
        return self.get_cycle(cycle_id)

    def observations(self, cycle_id: str) -> list[dict[str, Any]]:
        with self._connect() as db:
            rows = db.execute("SELECT record_json FROM research_observations WHERE cycle_id=? ORDER BY created_at,observation_id", (cycle_id,)).fetchall()
        return [json.loads(row["record_json"]) for row in rows]

    def add_observation(self, cycle_id: str, *, category: str, observed_on: str, note: str, location_scope: str, public_safe_confirmation: bool) -> dict[str, Any]:
        cycle = self.get_cycle(cycle_id)
        if cycle["state"] != "COLLECTING_EVIDENCE":
            raise ProgramStateError("observations may be added only while collecting evidence")
        if category not in OBSERVATION_CATEGORIES:
            raise ProgramContractError("observation category is not admitted")
        try:
            date.fromisoformat(observed_on)
        except (TypeError, ValueError) as exc:
            raise ProgramContractError("observed_on must use YYYY-MM-DD") from exc
        if public_safe_confirmation is not True:
            raise ProgramContractError("confirm that the note contains no private Council, customer, personal or non-public worksite data")
        clean_note = _require_text(note, "note", 5, 2000)
        clean_location = _require_text(location_scope, "location_scope", 2, 200)
        now = _now()
        observation = {
            "observation_id": f"FIELD-OBS-{uuid.uuid4().hex[:16].upper()}",
            "cycle_id": cycle_id,
            "category": category,
            "observed_on": observed_on,
            "reported_at": now,
            "location_scope": clean_location,
            "note": clean_note,
            "verbatim_human_report": clean_note,
            "structured_record": {
                "observed_on": observed_on,
                "location_scope": clean_location,
                "category": category,
                "structuring_state": "HUMAN_ENTERED_AND_CONFIRMED",
            },
            "report_channel": "LOCAL_WEB_FORM",
            "evidence_class": "HUMAN_FIELD_OBSERVATION_UNVERIFIED",
            "does_not_prove": "measurement, trend, cause, forecast, compliance state or operational condition",
            "public_safe_confirmed": True,
            "created_at": now,
        }
        with self._connect() as db:
            db.execute("INSERT INTO research_observations VALUES(?,?,?,?)", (observation["observation_id"], cycle_id, _json(observation), now))
        return observation

    def source_snapshots(self, cycle_id: str) -> list[dict[str, Any]]:
        with self._connect() as db:
            rows = db.execute("SELECT record_json FROM official_source_snapshots WHERE cycle_id=? ORDER BY source_id", (cycle_id,)).fetchall()
        return [json.loads(row["record_json"]) for row in rows]

    def refresh_official_sources(self, cycle_id: str, *, human_approval: bool, fetcher: Callable[[dict[str, Any]], dict[str, Any]] | None = None) -> dict[str, Any]:
        with self._cycle_transition_lock:
            cycle = self.get_cycle(cycle_id)
            if cycle["state"] != "COLLECTING_EVIDENCE":
                raise ProgramStateError("source refresh requires COLLECTING_EVIDENCE")
            if human_approval is not True:
                raise ProgramContractError("explicit human approval is required for every live refresh")
            if cycle["source_snapshots"]:
                raise ProgramStateError("this cycle already has an immutable official-source snapshot set")
            refresh_state = cycle.get("source_refresh_state", "NOT_REQUESTED")
            if refresh_state not in {"NOT_REQUESTED", "REFRESH_INTERRUPTED_RETRY_ALLOWED"}:
                raise ProgramStateError(f"source refresh is not admitted from {refresh_state}")
            cycle["source_refresh_state"] = "REFRESH_IN_PROGRESS"
            cycle["source_refresh_started_at"] = _now()
            cycle["source_refresh_completed_at"] = None
            cycle = self._save_cycle(cycle)
        fetch = fetcher or _default_fetch
        previous = self.get_cycle(cycle["previous_cycle_id"]) if cycle["previous_cycle_id"] else None
        previous_by_source = {item["source_id"]: item for item in (previous["source_snapshots"] if previous else [])}
        results = []
        sources = _allowlist()["sources"]
        try:
            for source in sources:
                fetched_at = _now()
                try:
                    response = fetch(source)
                    body = response.pop("body")
                    if not isinstance(body, bytes):
                        raise ProgramContractError("fetcher body must be bytes")
                    if len(body) > MAX_RESPONSE_BYTES:
                        raise ProgramContractError("source response exceeded 2 MiB ceiling")
                    final = urlparse(response.get("final_url", ""))
                    if final.scheme != "https" or final.hostname != source["allowed_host"]:
                        raise ProgramContractError("retrieved source is outside its exact allowlisted HTTPS host")
                    status = response.get("http_status")
                    if not isinstance(status, int) or not 200 <= status < 300:
                        raise ProgramContractError("official source did not return a successful HTTP status")
                    content_digest = _digest(body)
                    previous_snapshot = previous_by_source.get(source["source_id"])
                    change_state = "BASELINE_CAPTURED" if previous_snapshot is None else (
                        "POTENTIAL_CONTENT_CHANGE" if previous_snapshot.get("content_digest") != content_digest else "NO_CONTENT_DIGEST_CHANGE"
                    )
                    snapshot = {
                        "snapshot_id": _stable_id("SOURCE-SNAPSHOT", {"cycle": cycle_id, "source": source["source_id"], "digest": content_digest}),
                        "cycle_id": cycle_id,
                        "source_id": source["source_id"],
                        "module": source["module"],
                        "publisher": source["publisher"],
                        "title": source["title"],
                        "requested_url": source["url"],
                        "final_url": response["final_url"],
                        "http_status": response["http_status"],
                        "content_type": response.get("content_type", ""),
                        "etag": response.get("etag"),
                        "last_modified": response.get("last_modified"),
                        "content_bytes": len(body),
                        "content_digest": content_digest,
                        "change_state": change_state,
                        "admission_state": "SOURCE_FRESHNESS_METADATA_ONLY",
                        "raw_content_retained": False,
                        "environmental_conclusion": None,
                        "fetched_at": fetched_at,
                        "cost_aud": 0,
                    }
                except Exception as exc:
                    snapshot = {
                        "snapshot_id": _stable_id("SOURCE-SNAPSHOT-FAILED", {"cycle": cycle_id, "source": source["source_id"], "time": fetched_at}),
                        "cycle_id": cycle_id,
                        "source_id": source["source_id"],
                        "module": source["module"],
                        "publisher": source["publisher"],
                        "title": source["title"],
                        "requested_url": source["url"],
                        "change_state": "RETRIEVAL_FAILED_VISIBLE",
                        "admission_state": "NOT_ADMITTED_RETRIEVAL_FAILED",
                        "error_type": type(exc).__name__,
                        "error_detail": str(exc)[:500],
                        "raw_content_retained": False,
                        "environmental_conclusion": None,
                        "fetched_at": fetched_at,
                        "cost_aud": 0,
                    }
                results.append(snapshot)
        except BaseException:
            with self._cycle_transition_lock:
                interrupted = self.get_cycle(cycle_id)
                if interrupted["state"] == "COLLECTING_EVIDENCE":
                    interrupted["source_refresh_state"] = "REFRESH_INTERRUPTED_RETRY_ALLOWED"
                    interrupted["source_refresh_completed_at"] = _now()
                    self._save_cycle(interrupted)
            raise
        rows = [
            (item["snapshot_id"], cycle_id, item["source_id"], _json(item), item["fetched_at"])
            for item in results
        ]
        with self._cycle_transition_lock:
            completed = self.get_cycle(cycle_id)
            if completed["state"] != "COLLECTING_EVIDENCE":
                raise ProgramStateError("cycle changed state before source refresh completed")
            if completed.get("source_refresh_state") != "REFRESH_IN_PROGRESS":
                raise ProgramStateError("source refresh state changed before atomic commit")
            completed["source_refresh_state"] = "COMPLETE_ATOMIC_SET"
            completed["source_refresh_completed_at"] = _now()
            completed["updated_at"] = _now()
            stored = {
                key: value for key, value in completed.items()
                if key not in {"observations", "source_snapshots"}
            }
            with self._connect() as db:
                db.executemany("INSERT INTO official_source_snapshots VALUES(?,?,?,?,?)", rows)
                db.execute(
                    "UPDATE research_cycles SET state=?,record_json=?,updated_at=? WHERE cycle_id=?",
                    (completed["state"], _json(stored), completed["updated_at"], cycle_id),
                )
        return {
            "cycle_id": cycle_id,
            "network_used": True,
            "human_approval_recorded": True,
            "snapshot_set_state": "COMPLETE_ATOMIC_SET",
            "expected_source_count": len(sources),
            "recorded_source_count": len(results),
            "raw_content_retained": False,
            "cost_aud": 0,
            "snapshots": results,
        }

    def compile_cycle(self, cycle_id: str) -> dict[str, Any]:
        with self._cycle_transition_lock:
            cycle = self.get_cycle(cycle_id)
            if cycle["state"] != "COLLECTING_EVIDENCE":
                raise ProgramStateError("cycle compilation requires COLLECTING_EVIDENCE")
            refresh_state = cycle.get("source_refresh_state", "NOT_REQUESTED")
            if refresh_state == "REFRESH_IN_PROGRESS":
                raise ProgramStateError("source refresh is still in progress; compilation is locked")
            if refresh_state == "REFRESH_INTERRUPTED_RETRY_ALLOWED":
                raise ProgramStateError("source refresh was interrupted; retry it before compilation")
            if refresh_state not in {"NOT_REQUESTED", "COMPLETE_ATOMIC_SET"}:
                raise ProgramStateError(f"cycle compilation is not admitted from source refresh state {refresh_state}")
            observations, snapshots = cycle["observations"], cycle["source_snapshots"]
            expected_source_ids = {item["source_id"] for item in _allowlist()["sources"]}
            recorded_source_ids = {item["source_id"] for item in snapshots}
            if refresh_state == "COMPLETE_ATOMIC_SET" and recorded_source_ids != expected_source_ids:
                missing = sorted(expected_source_ids - recorded_source_ids)
                unexpected = sorted(recorded_source_ids - expected_source_ids)
                raise ProgramStateError(
                    "official-source snapshot set is incomplete or unexpected; "
                    f"missing={missing}, unexpected={unexpected}"
                )
            if refresh_state == "NOT_REQUESTED" and snapshots:
                raise ProgramStateError("source snapshots exist without a completed refresh state")
            changes = [item for item in snapshots if item["change_state"] == "POTENTIAL_CONTENT_CHANGE"]
            failures = [item for item in snapshots if item["change_state"] == "RETRIEVAL_FAILED_VISIBLE"]
            previous = self.get_cycle(cycle["previous_cycle_id"]) if cycle["previous_cycle_id"] else None
            comparison = {
                "comparison_state": "FIRST_CYCLE_BASELINE" if previous is None else "COMPARED_WITH_PREVIOUS_CYCLE",
                "previous_cycle_id": cycle["previous_cycle_id"],
                "new_human_observation_count": len(observations),
                "source_refresh_state": refresh_state,
                "expected_source_count": len(expected_source_ids),
                "source_snapshot_count": len(snapshots),
                "potential_source_change_count": len(changes),
                "retrieval_failure_count": len(failures),
                "change_candidates": [
                    {"source_id": item["source_id"], "module": item["module"], "state": item["change_state"], "meaning": "human must inspect the official source; digest change is not environmental change"}
                    for item in changes
                ],
            }
            program = self.get_program(cycle["program_id"])
            version = program["current_hypothesis_version"] + 1
            hypothesis = {
                "version": version,
                "state": "EVIDENCE_CHANGE_REVIEW_REQUIRED" if changes else "NO_REVIEWED_ENVIRONMENTAL_CHANGE_ESTABLISHED",
                "module_states": {module: "UNRESOLVED_REQUIRES_EVIDENCE_AND_HUMAN_REVIEW" for module in MODULES},
                "environmental_conclusion": None,
                "forecast": None,
                "recommendation": None,
                "reason": "A source-page digest or field observation is a research signal only; no admitted analysis establishes a Cooma environmental change.",
            }
            receipt_body = {"cycle": cycle_id, "comparison": comparison, "hypothesis": hypothesis}
            receipt = {
                "receipt_id": _stable_id("PROGRAM-CYCLE-RECEIPT", receipt_body),
                "termination": "MONTHLY_REVIEW_COMPILED_AWAITING_HUMAN_REVIEW",
                "network_snapshot_count": len(snapshots),
                "network_used": bool(snapshots),
                "cost_aud": 0,
                "comparison_digest": _digest(comparison),
                "hypothesis_digest": _digest(hypothesis),
            }
            passport = {
                "passport_id": _stable_id("PROGRAM-CYCLE-PASSPORT", receipt),
                "state": "REAL_SOURCE_METADATA_AND_UNVERIFIED_OBSERVATIONS_QUARANTINED",
                "supports": "a versioned record of source freshness, field observations and review workflow",
                "does_not_support": ["Cooma environmental trend", "ENSO or seasonal forecast interpretation", "bushfire warning", "drinking-water shortage estimate", "wastewater asset, compliance or capacity conclusion"],
                "human_review_required": True,
                "release_as_environmental_evidence": False,
            }
            cycle.update(state="COMPILED_AWAITING_HUMAN_REVIEW", comparison=comparison, hypothesis_version=hypothesis, receipt=receipt, passport=passport)
            return self._save_cycle(cycle)

    def review_cycle(self, cycle_id: str, *, decision: str, reviewer: str, reason: str) -> dict[str, Any]:
        cycle = self.get_cycle(cycle_id)
        if cycle["state"] != "COMPILED_AWAITING_HUMAN_REVIEW":
            raise ProgramStateError("review requires COMPILED_AWAITING_HUMAN_REVIEW")
        if decision not in REVIEW_DECISIONS:
            raise ProgramContractError("review decision is not admitted")
        clean_reviewer = _require_text(reviewer, "reviewer", 2, 200)
        clean_reason = _require_text(reason, "reason", 10, 2000)
        cycle["state"] = {
            "ACCEPT_CYCLE": "CYCLE_REVIEWED_ACCEPTED_AS_RESEARCH_RECORD",
            "QUESTION_CYCLE": "CYCLE_REVIEWED_QUESTIONED",
            "REVISE_CYCLE": "CYCLE_REVIEWED_REVISION_REQUIRED",
            "REJECT_CYCLE": "CYCLE_REVIEWED_REJECTED",
        }[decision]
        cycle["human_review"] = {
            "decision": decision,
            "reviewer": clean_reviewer,
            "reason": clean_reason,
            "environmental_signoff": False,
            "operational_release": False,
            "reviewed_at": _now(),
        }
        reviewed = self._save_cycle(cycle)
        program = self.get_program(cycle["program_id"])
        program.pop("cycles", None)
        if decision == "ACCEPT_CYCLE":
            program["state"] = "ACTIVE_HUMAN_REVIEWED_RESEARCH_PROGRAM"
            program["current_hypothesis_version"] = cycle["hypothesis_version"]["version"]
            program["last_reviewed_cycle_id"] = cycle_id
            self._save_program(program)
        return reviewed

    def annual_report(self, report_year: int, program_id: str = PROGRAM_ID) -> dict[str, Any]:
        if not isinstance(report_year, int) or not 2000 <= report_year <= 2100:
            raise ProgramContractError("report_year must be an integer in 2000..2100")
        program = self.get_program(program_id)
        cycles = [item for item in program["cycles"] if item["year_month"].startswith(f"{report_year}-")]
        december = [item for item in cycles if item["year_month"] == f"{report_year}-12"]
        reviewed_states = {
            "CYCLE_REVIEWED_ACCEPTED_AS_RESEARCH_RECORD",
            "CYCLE_REVIEWED_QUESTIONED",
            "CYCLE_REVIEWED_REVISION_REQUIRED",
            "CYCLE_REVIEWED_REJECTED",
        }
        if not december or december[-1]["state"] not in reviewed_states:
            raise ProgramStateError("annual report requires a reviewed December cycle")
        detailed = [self.get_cycle(item["cycle_id"]) for item in cycles]
        category_counts = {category: 0 for category in sorted(OBSERVATION_CATEGORIES)}
        for cycle in detailed:
            for observation in cycle["observations"]:
                category_counts[observation["category"]] += 1
        months_present = sorted({item["year_month"] for item in cycles})
        expected = {f"{report_year}-{month:02d}" for month in range(1, 13)}
        summary = {
            "report_year": report_year,
            "cycle_count": len(cycles),
            "months_present": months_present,
            "missing_months": sorted(expected - set(months_present)),
            "field_observation_count": sum(category_counts.values()),
            "field_observation_counts_by_category": category_counts,
            "official_source_snapshot_count": sum(len(item["source_snapshots"]) for item in detailed),
            "potential_source_change_count": sum(
                1 for item in detailed for snapshot in item["source_snapshots"]
                if snapshot["change_state"] == "POTENTIAL_CONTENT_CHANGE"
            ),
            "retrieval_failure_count": sum(
                1 for item in detailed for snapshot in item["source_snapshots"]
                if snapshot["change_state"] == "RETRIEVAL_FAILED_VISIBLE"
            ),
            "review_decisions": [item["human_review"]["decision"] for item in detailed if item.get("human_review")],
            "hypothesis_versions": [item["hypothesis_version"] for item in detailed if item.get("hypothesis_version")],
        }
        receipt = {
            "receipt_id": _stable_id("ANNUAL-REPORT-RECEIPT", {"program": program_id, "summary": summary}),
            "termination": "ANNUAL_RESEARCH_RECORD_COMPILED",
            "report_digest": _digest(summary),
            "network_calls_during_report_generation": 0,
            "cost_aud": 0,
        }
        passport = {
            "passport_id": _stable_id("ANNUAL-REPORT-PASSPORT", receipt),
            "state": "ANNUAL_RESEARCH_RECORD_NOT_ENVIRONMENTAL_CERTIFICATION",
            "supports": "annual inventory of recorded cycles, observations, source snapshots and human reviews",
            "does_not_support": [
                "complete monthly coverage when months are missing",
                "Cooma environmental trend or causal conclusion",
                "bushfire, drinking-water, wastewater, engineering or compliance decision",
            ],
            "human_review_required": True,
        }
        report = {
            "report_id": _stable_id("COOMA-ANNUAL-REPORT", {"program": program_id, "year": report_year}),
            "program_id": program_id,
            "report_year": report_year,
            "title": f"Cooma Water–Fire–Wastewater Research Record {report_year}",
            "summary": summary,
            "receipt": receipt,
            "passport": passport,
            "environmental_conclusion": None,
            "created_at": _now(),
        }
        with self._connect() as db:
            try:
                db.execute(
                    "INSERT INTO annual_research_reports VALUES(?,?,?,?,?)",
                    (report["report_id"], program_id, report_year, _json(report), report["created_at"]),
                )
            except sqlite3.IntegrityError as exc:
                raise ProgramStateError("this program already has an immutable annual report for that year") from exc
        return report
