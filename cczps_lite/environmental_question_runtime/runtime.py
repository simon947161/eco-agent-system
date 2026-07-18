"""Supervised real-question planning and fictional highland-town rehearsal."""

from __future__ import annotations

import hashlib
import json
import sqlite3
import time
import uuid
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

SCHEMA_ID = "climateos.meaningful_environmental_question_runtime.v0.1"
BOUNDARY = "FICTIONAL_HIGHLAND_TOWN / LOCAL_ONLY / NOT_ENVIRONMENTAL_EVIDENCE"
FIXTURE_ID = "TINY-SYNTH-HIGHLAND-TOWN-001"
FIXTURE_PATH = Path(__file__).resolve().parent / "fixtures" / "fictional_highland_town.json"
MAX_QUESTION = 4000


class RuntimeStateError(ValueError):
    """The requested transition is not available in the current state."""


class RuntimeBoundaryError(ValueError):
    """The request would cross the real/synthetic execution boundary."""


def _now() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def _canonical(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def _digest(value: Any) -> str:
    return "sha256:" + hashlib.sha256(_canonical(value).encode()).hexdigest()


def _id(prefix: str, value: Any) -> str:
    return f"{prefix}-{hashlib.sha256(_canonical(value).encode()).hexdigest()[:16].upper()}"


def _plan(question: str, session_id: str) -> dict[str, Any]:
    modules = [
        {
            "module": "CLIMATE_AND_SNOW_OUTLOOK",
            "human_question": "Are recent low-water and low-snow observations consistent with current conditions, and what outlook is justified?",
            "evidence_needed": ["Bureau of Meteorology observations and seasonal outlooks", "snow observations with dates and station metadata", "current ENSO outlook with probability and issue date"],
            "cannot_claim_yet": "No claim that next year is definitely El Niño, dry, or low-snow."
        },
        {
            "module": "BUSHFIRE_RISK",
            "human_question": "How could climate, fuels, terrain and ignition exposure affect future bushfire risk?",
            "evidence_needed": ["NSW RFS district information and current fire danger products", "fuel condition and land-management evidence", "weather and antecedent moisture observations"],
            "cannot_claim_yet": "No real fire probability, severity forecast or safety advice."
        },
        {
            "module": "DRINKING_WATER_SECURITY",
            "human_question": "How exposed are source water, treatment capacity, demand and contingency supplies to a dry period?",
            "evidence_needed": ["council source-water, storage and restriction records", "treatment capacity and demand time series", "drought and emergency water plans"],
            "cannot_claim_yet": "No shortage probability, timing or volume estimate."
        },
        {
            "module": "WASTEWATER_RESILIENCE",
            "human_question": "What wastewater work exists, what capacity and constraints does it have, and what adaptation role could it play?",
            "evidence_needed": ["council wastewater strategy, asset and project records", "NSW EPA licence and compliance records", "inflow, treatment, reuse, discharge, energy and capacity data"],
            "cannot_claim_yet": "No claim about current project completion, compliance or maximum reuse potential."
        },
        {
            "module": "CROSS_SYSTEM_INTEGRATION",
            "human_question": "Which wastewater actions could reduce potable demand or environmental stress, and what limits or trade-offs apply?",
            "evidence_needed": ["fit-for-purpose recycled-water demand", "public-health and environmental requirements", "energy, cost, storage, salinity and seasonal-demand constraints"],
            "cannot_claim_yet": "No recommendation or climate-benefit claim without a water balance and expert review."
        },
    ]
    plan = {
        "plan_id": _id("MEQ-PLAN", {"session": session_id, "question": question}),
        "classification": "REAL_WORLD_PLAN_ONLY",
        "question_preserved_verbatim": question,
        "structured_research_question": "How do climate and snow conditions, bushfire exposure, drinking-water security and wastewater resilience interact, and which evidence would distinguish observation from defensible conclusion?",
        "modules": modules,
        "red_gates": [
            "CURRENT_AUTHORITATIVE_DATA_REQUIRED",
            "SOURCE_PROVENANCE_AND_LICENCE_REVIEW_REQUIRED",
            "PLACE_AND_TIME_MATCH_REQUIRED",
            "DOMAIN_EXPERT_REVIEW_REQUIRED",
            "SEPARATE_HUMAN_APPROVAL_BEFORE_REAL_ANALYSIS",
        ],
        "real_execution": "BLOCKED_NOT_AUTHORIZED",
        "assistant_kind": "DETERMINISTIC_RESEARCH_PLAN_TEMPLATE_NOT_LLM",
    }
    return plan


def _load_fixture() -> dict[str, Any]:
    fixture = json.loads(FIXTURE_PATH.read_text(encoding="utf-8"))
    if fixture.get("fixture_id") != FIXTURE_ID or fixture.get("not_environmental_evidence") is not True:
        raise RuntimeBoundaryError("fictional fixture identity or evidence boundary changed")
    if fixture.get("place_label") != "FICTIONAL AUSTRALIAN HIGHLAND TOWN — NOT COOMA":
        raise RuntimeBoundaryError("fixture may not impersonate the real place")
    if fixture.get("network_required") is not False or fixture.get("boundary_label") != BOUNDARY:
        raise RuntimeBoundaryError("fixture must remain offline and quarantined")
    return fixture


def _rehearsal_plan(real_plan: dict[str, Any], session_id: str) -> dict[str, Any]:
    body = {
        "session_id": session_id,
        "source_plan_id": real_plan["plan_id"],
        "fixture_id": FIXTURE_ID,
        "diagnostics": [
            "snowpack_index_change",
            "catchment_inflow_index_change",
            "bushfire_weather_index_change",
            "potable_demand_pressure_change",
            "wastewater_spare_capacity_change",
            "recycled_water_offset_change",
        ],
    }
    return {
        "rehearsal_plan_id": _id("MEQ-REHEARSAL", body),
        "source_plan_id": real_plan["plan_id"],
        "place": "FICTIONAL AUSTRALIAN HIGHLAND TOWN — NOT COOMA",
        "scenario": "fixed fictional baseline compared with a fixed fictional dry rehearsal",
        "hypothesis": "In the fictional dry rehearsal, lower snow and inflow coincide with higher fire-weather and potable-demand pressure; increased recycled-water offset may reduce some potable demand but does not remove source-water, capacity or safety constraints.",
        "diagnostics": body["diagnostics"],
        "falsification": ["computed diagnostic direction differs from the stated hypothesis", "fixture identity or quarantine boundary fails"],
        "limitations": ["indices are invented demonstration values", "relationships are not a calibrated model", "no transfer to Cooma or any real place"],
        "fixture_id": FIXTURE_ID,
        "fixture_digest": _digest(_load_fixture()),
        "network": "DENIED_BY_DESIGN",
        "cost_aud": 0,
        "approved": False,
        "boundary_label": BOUNDARY,
    }


class EnvironmentalQuestionRuntime:
    def __init__(self, db_path: str | Path) -> None:
        self.db_path = Path(db_path)
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        with self._connect() as db:
            db.executescript("""
                CREATE TABLE IF NOT EXISTS environmental_question_sessions (
                    session_id TEXT PRIMARY KEY, state TEXT NOT NULL,
                    record_json TEXT NOT NULL, updated_at TEXT NOT NULL
                );
            """)

    def _connect(self) -> sqlite3.Connection:
        db = sqlite3.connect(self.db_path, timeout=2)
        db.row_factory = sqlite3.Row
        return db

    def _save(self, record: dict[str, Any], event: str, actor: str, detail: dict[str, Any]) -> dict[str, Any]:
        previous = record["audit_events"][-1]["event_digest"] if record["audit_events"] else "GENESIS"
        event_body = {
            "sequence": len(record["audit_events"]) + 1,
            "event": event,
            "actor": actor,
            "state": record["state"],
            "detail": detail,
            "predecessor_digest": previous,
            "created_at": _now(),
        }
        event_body["event_digest"] = _digest(event_body)
        record["audit_events"].append(event_body)
        record["updated_at"] = event_body["created_at"]
        with self._connect() as db:
            db.execute(
                "INSERT OR REPLACE INTO environmental_question_sessions VALUES(?,?,?,?)",
                (record["session_id"], record["state"], _canonical(record), record["updated_at"]),
            )
        return self.get_session(record["session_id"])

    def get_session(self, session_id: str) -> dict[str, Any]:
        with self._connect() as db:
            row = db.execute("SELECT record_json FROM environmental_question_sessions WHERE session_id=?", (session_id,)).fetchone()
        if row is None:
            raise KeyError(session_id)
        record = json.loads(row["record_json"])
        previous = "GENESIS"
        valid = True
        for event in record["audit_events"]:
            saved = event["event_digest"]
            body = {key: value for key, value in event.items() if key != "event_digest"}
            if body["predecessor_digest"] != previous or _digest(body) != saved:
                valid = False
            previous = saved
        record["audit_chain_valid"] = valid
        return record

    def create_question(self, question: str) -> dict[str, Any]:
        if not isinstance(question, str) or not 20 <= len(question.strip()) <= MAX_QUESTION:
            raise RuntimeBoundaryError("question must be 20..4000 characters of text")
        question = question.strip()
        session_id = f"MEQ-SESSION-{uuid.uuid4().hex[:16].upper()}"
        record = {
            "schema_id": SCHEMA_ID,
            "session_id": session_id,
            "state": "REAL_WORLD_PLAN_PROPOSED",
            "question": question,
            "real_world_plan": _plan(question, session_id),
            "rehearsal_plan": None,
            "result": None,
            "receipt": None,
            "passport": None,
            "human_review": None,
            "audit_events": [],
            "created_at": _now(),
            "updated_at": _now(),
        }
        return self._save(record, "REAL_QUESTION_STRUCTURED_PLAN_ONLY", "LOCAL_STRUCTURING_ASSISTANT", {"question_digest": _digest(question), "real_execution": "BLOCKED"})

    def create_rehearsal(self, session_id: str) -> dict[str, Any]:
        record = self.get_session(session_id)
        if record["state"] != "REAL_WORLD_PLAN_PROPOSED":
            raise RuntimeStateError("fictional rehearsal requires REAL_WORLD_PLAN_PROPOSED")
        record["rehearsal_plan"] = _rehearsal_plan(record["real_world_plan"], session_id)
        record["state"] = "SYNTHETIC_PLAN_AWAITING_APPROVAL"
        return self._save(record, "FICTIONAL_REHEARSAL_PROPOSED", "LOCAL_STRUCTURING_ASSISTANT", {"rehearsal_plan_id": record["rehearsal_plan"]["rehearsal_plan_id"]})

    def decide(self, session_id: str, decision: str, reviewer: str, reason: str) -> dict[str, Any]:
        record = self.get_session(session_id)
        if record["state"] != "SYNTHETIC_PLAN_AWAITING_APPROVAL":
            raise RuntimeStateError("decision requires SYNTHETIC_PLAN_AWAITING_APPROVAL")
        if decision not in {"APPROVE", "REJECT"}:
            raise RuntimeBoundaryError("decision must be APPROVE or REJECT")
        if not reviewer.strip() or len(reason.strip()) < 10:
            raise RuntimeBoundaryError("reviewer and a meaningful reason are required")
        record["state"] = "SYNTHETIC_APPROVED_TO_RUN" if decision == "APPROVE" else "SYNTHETIC_REJECTED_BEFORE_RUN"
        record["rehearsal_plan"]["approved"] = decision == "APPROVE"
        return self._save(record, f"HUMAN_{decision}_SYNTHETIC_PLAN", "HUMAN_REVIEWER", {"reviewer": reviewer.strip(), "reason": reason.strip()})

    def run(self, session_id: str) -> dict[str, Any]:
        record = self.get_session(session_id)
        if record["state"] != "SYNTHETIC_APPROVED_TO_RUN" or record["rehearsal_plan"]["approved"] is not True:
            raise RuntimeStateError("exact human approval is required before synthetic execution")
        fixture = _load_fixture()
        started = time.monotonic()
        baseline, dry = fixture["baseline"], fixture["dry_rehearsal"]
        values = {
            "snowpack_index_change": dry["snowpack_index"] - baseline["snowpack_index"],
            "catchment_inflow_index_change": dry["catchment_inflow_index"] - baseline["catchment_inflow_index"],
            "bushfire_weather_index_change": dry["bushfire_weather_index"] - baseline["bushfire_weather_index"],
            "potable_demand_pressure_change": dry["potable_demand_index"] - baseline["potable_demand_index"],
            "wastewater_spare_capacity_change": (dry["wastewater_capacity_index"] - dry["wastewater_inflow_index"]) - (baseline["wastewater_capacity_index"] - baseline["wastewater_inflow_index"]),
            "recycled_water_offset_change": dry["recycled_water_offset_index"] - baseline["recycled_water_offset_index"],
        }
        result = {
            "result_id": _id("MEQ-RESULT", {"session": session_id, "values": values}),
            "values": values,
            "plain_language": [
                "In the invented dry rehearsal, snowpack and catchment-inflow indices are lower.",
                "The invented fire-weather and potable-demand-pressure indices are higher.",
                "The invented wastewater spare-capacity index is lower while the recycled-water offset is higher.",
                "This demonstrates a joined-up question structure; it does not describe Cooma."
            ],
            "quarantine_state": "QUARANTINED_SYNTHETIC_ONLY",
        }
        elapsed = round(time.monotonic() - started, 6)
        receipt = {
            "receipt_id": _id("MEQ-RUN-RECEIPT", result),
            "termination": "FIXED_LOCAL_EXECUTOR_COMPLETED",
            "wall_time_seconds": elapsed,
            "network_used": False,
            "cost_aud": 0,
            "fixture_id": FIXTURE_ID,
            "fixture_digest": _digest(fixture),
            "result_digest": _digest(result),
        }
        passport = {
            "passport_id": _id("MEQ-EVIDENCE-PASSPORT", receipt),
            "state": "SUPPORTED_SYNTHETIC_ONLY",
            "supports": "workflow rehearsal and deterministic arithmetic only",
            "does_not_support": ["Cooma environmental conclusion", "ENSO forecast", "bushfire forecast", "drinking-water shortage estimate", "wastewater project or capacity conclusion"],
            "real_world_plan_id": record["real_world_plan"]["plan_id"],
            "human_review_required": True,
            "boundary_label": BOUNDARY,
        }
        record.update(state="SYNTHETIC_RUN_COMPLETED_QUARANTINED", result=result, receipt=receipt, passport=passport)
        return self._save(record, "FIXED_SYNTHETIC_RUN_COMPLETED", "LOCAL_FIXED_EXECUTOR", {"receipt_id": receipt["receipt_id"], "network_used": False})

    def review(self, session_id: str, decision: str, reviewer: str, reason: str) -> dict[str, Any]:
        record = self.get_session(session_id)
        if record["state"] != "SYNTHETIC_RUN_COMPLETED_QUARANTINED":
            raise RuntimeStateError("review requires a quarantined synthetic result")
        states = {"ACCEPT_DEMO": "REVIEWED_DEMO_ACCEPTED", "QUESTION": "REVIEWED_RESULT_QUESTIONED", "REVISE": "REVIEWED_REVISION_REQUESTED", "REJECT": "REVIEWED_DEMO_REJECTED"}
        if decision not in states:
            raise RuntimeBoundaryError("review decision must be ACCEPT_DEMO, QUESTION, REVISE or REJECT")
        if not reviewer.strip() or len(reason.strip()) < 10:
            raise RuntimeBoundaryError("reviewer and a meaningful reason are required")
        record["state"] = states[decision]
        record["human_review"] = {"decision": decision, "reviewer": reviewer.strip(), "reason": reason.strip(), "real_environmental_release": False}
        return self._save(record, f"HUMAN_{decision}", "HUMAN_REVIEWER", record["human_review"])
