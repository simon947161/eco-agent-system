"""Supervised local question-to-receipt-to-review workflow."""

from __future__ import annotations

import copy
import json
import time
import tracemalloc
import uuid
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from .contracts import (
    BOUNDARY_LABEL,
    FIXTURE_ID,
    PASSPORT_STATES,
    POST_RUN_DECISIONS,
    PRE_RUN_DECISIONS,
    RESOURCE_CEILING,
    SCHEMA_ID,
    ContractError,
    canonical_json,
    digest,
    stable_id,
    validate_hypothesis,
    validate_object_graph,
    validate_question,
)
from .store import RuntimeStore

PACKAGE_ROOT = Path(__file__).resolve().parent
FIXTURE_PATH = PACKAGE_ROOT / "fixtures" / "tiny_synthetic_scalar_case.json"


class RuntimeStateError(ValueError):
    """Raised for a refused workflow transition."""


class RuntimeBoundaryError(ValueError):
    """Raised when execution would exceed the authorized local envelope."""


def _now() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def _load_fixture() -> dict[str, Any]:
    fixture = json.loads(FIXTURE_PATH.read_text(encoding="utf-8"))
    expected = {
        "schema_id",
        "fixture_id",
        "title",
        "origin",
        "not_environmental_evidence",
        "seed",
        "baseline",
        "perturbation",
        "diagnostic",
        "failure_mode",
        "boundary_label",
    }
    if set(fixture) != expected:
        raise RuntimeBoundaryError("fixture fields are not closed")
    if (
        fixture["fixture_id"] != FIXTURE_ID
        or fixture["origin"] != "REPOSITORY_AUTHORED_FICTIONAL_TINY_SYNTHETIC"
        or fixture["not_environmental_evidence"] is not True
        or fixture["boundary_label"] != BOUNDARY_LABEL
    ):
        raise RuntimeBoundaryError("fixture origin or boundary is not authorized")
    return fixture


def _default_hypothesis(question: str, session_id: str) -> dict[str, Any]:
    base = {
        "research_question": question,
        "fixture_id": FIXTURE_ID,
        "boundary_label": BOUNDARY_LABEL,
    }
    hypothesis_id = stable_id("MECH-HYP", base)
    result = {
        "hypothesis_id": hypothesis_id,
        "revision_id": f"{hypothesis_id}-R1",
        "research_question": question,
        "hypothesis_statement": "For the fictional sealed scalar box, the fixed perturbation will produce a larger response index than the fixed baseline.",
        "mechanism_chain": [
            "FICTIONAL_INPUT_INDEX --PROPOSED_INFLUENCE--> FICTIONAL_RESPONSE_INDEX",
            "FIXED_DIAGNOSTIC --DIAGNOSTIC_ONLY--> RESPONSE_INDEX_DELTA",
        ],
        "expected_direction": "POSITIVE response_index_delta",
        "diagnostics": ["response_index_delta = perturbation response index - baseline response index"],
        "alternative_explanations": [
            "The fixed fixture may encode the difference directly rather than represent a mechanism.",
            "The diagnostic may be structurally valid while having no relevance outside this fictional box.",
        ],
        "falsification_criteria": [
            "response_index_delta <= 0 contradicts the proposed positive direction",
            "missing, malformed or boundary-crossing fixture makes the hypothesis not testable",
        ],
        "evidence_threshold": "Synthetic support only when response_index_delta >= 2.0; never environmental support.",
        "scale_and_time_assumptions": "One timeless fictional scalar pair; no geographic, atmospheric or project scale.",
        "expert_owner_role": "human runtime reviewer; no scientific expert is assigned",
        "limitations": [
            "This is a deterministic workflow rehearsal, not a scientific experiment.",
            "No result may be transferred to a real place, model, forecast or project decision.",
        ],
        "fixture_id": FIXTURE_ID,
        "boundary_label": BOUNDARY_LABEL,
    }
    validate_hypothesis(result)
    return result


def _build_graph(question: str, session_id: str) -> dict[str, Any]:
    hypothesis = _default_hypothesis(question, session_id)
    experiment_id = stable_id("MECH-EXP", {"session_id": session_id, "hypothesis": hypothesis})
    experiment = {
        "experiment_id": experiment_id,
        "design_revision": f"{experiment_id}-R1",
        "hypothesis_id": hypothesis["hypothesis_id"],
        "baseline": "fixture.baseline",
        "perturbation": "fixture.perturbation",
        "control": "same fixed scalar fixture and diagnostic",
        "sensitivity": "none in v0.1",
        "diagnostics": ["response_index_delta"],
        "stop_conditions": ["missing approval", "fixture boundary failure", "resource ceiling expansion", "malformed scalar"],
        "status": "AWAITING_HUMAN_APPROVAL",
    }
    manifest_id = stable_id("MECH-MANIFEST", experiment)
    manifest = {
        "manifest_id": manifest_id,
        "experiment_id": experiment_id,
        "runtime": "python-standard-library-fixed-function-v0.1",
        "fixture_id": FIXTURE_ID,
        "fixture_digest": digest(_load_fixture()),
        "random_seed_policy": "fixed repository seed; executor is deterministic",
        "network": "DENIED_BY_DESIGN",
        "secrets": "NOT_USED",
        "external_dependencies": [],
    }
    configuration_id = stable_id("MECH-CONFIG", manifest)
    configuration = {
        "configuration_id": configuration_id,
        "manifest_id": manifest_id,
        "configuration_digest": digest({"manifest": manifest, "ceiling": RESOURCE_CEILING}),
        "resource_ceiling": copy.deepcopy(RESOURCE_CEILING),
        "executor": "fixed_scalar_delta",
    }
    run_request_id = stable_id("MECH-RUN-REQUEST", {"session_id": session_id, "configuration_id": configuration_id})
    graph = {
        "schema_id": SCHEMA_ID,
        "session_id": session_id,
        "hypothesis": hypothesis,
        "experiment_design": experiment,
        "reproducibility_manifest": manifest,
        "configuration_identity": configuration,
        "run_request": {
            "run_request_id": run_request_id,
            "session_id": session_id,
            "hypothesis_id": hypothesis["hypothesis_id"],
            "experiment_id": experiment_id,
            "manifest_id": manifest_id,
            "configuration_id": configuration_id,
            "fixture_id": FIXTURE_ID,
            "approved": False,
            "approval": None,
        },
        "resource_ceiling": copy.deepcopy(RESOURCE_CEILING),
        "boundary_label": BOUNDARY_LABEL,
    }
    validate_object_graph(graph)
    return graph


def execute_fixed_fixture(graph: dict[str, Any]) -> tuple[dict[str, Any], dict[str, Any]]:
    """Execute exactly one admitted scalar operation without subprocess or network."""
    validate_object_graph({**copy.deepcopy(graph), "run_request": {**graph["run_request"], "approved": False, "approval": None}})
    if graph["run_request"].get("approved") is not True or not graph["run_request"].get("approval"):
        raise RuntimeBoundaryError("an exact human approval is required before execution")
    fixture = _load_fixture()
    start_wall = time.monotonic()
    start_cpu = time.process_time()
    tracemalloc.start()
    before_current, before_peak = tracemalloc.get_traced_memory()
    try:
        baseline = float(fixture["baseline"]["response_index"])
        perturbation = float(fixture["perturbation"]["response_index"])
        delta = round(perturbation - baseline, 10)
        diagnostic = fixture["diagnostic"]
        if delta >= float(diagnostic["support_threshold"]):
            passport_state = "SUPPORTED_SYNTHETIC_ONLY"
        elif delta <= float(diagnostic["contradiction_threshold"]):
            passport_state = "CONTRADICTED_SYNTHETIC_ONLY"
        else:
            passport_state = "PARTIAL_SYNTHETIC_ONLY"
        output = {
            "fixture_id": FIXTURE_ID,
            "diagnostic": "response_index_delta",
            "baseline_response_index": baseline,
            "perturbation_response_index": perturbation,
            "response_index_delta": delta,
            "passport_state": passport_state,
            "quarantine_state": "QUARANTINED_NOT_ENVIRONMENTAL_EVIDENCE",
            "limitations": [
                "Repository-authored fictional scalar values only.",
                "No geographic, meteorological, wind-resource, project or causal conclusion.",
            ],
            "boundary_label": BOUNDARY_LABEL,
        }
        output_bytes = len(canonical_json(output).encode("utf-8"))
    finally:
        current, peak = tracemalloc.get_traced_memory()
        tracemalloc.stop()
    observed = {
        "logical_cpu_workers": 1,
        "wall_time_seconds": round(time.monotonic() - start_wall, 6),
        "cpu_time_seconds": round(time.process_time() - start_cpu, 6),
        "incremental_memory_mib": round(max(0, peak - before_peak, current - before_current) / (1024 * 1024), 6),
        "output_bytes": output_bytes,
        "cost_aud": 0,
        "network_used": False,
        "secrets_used": False,
        "subprocess_used": False,
    }
    ceiling = graph["resource_ceiling"]
    exceeded = [
        key for key in ("logical_cpu_workers", "wall_time_seconds", "incremental_memory_mib", "output_bytes", "cost_aud")
        if observed[key] > ceiling[key]
    ]
    if exceeded:
        raise RuntimeBoundaryError("observed resource ceiling exceeded: " + ", ".join(exceeded))
    return output, observed


class ScientistRuntime:
    def __init__(self, db_path: str | Path) -> None:
        self.store = RuntimeStore(db_path)

    def _audit(self, record: dict, event_type: str, actor_role: str, state_before: str, detail: dict) -> dict:
        event_id = stable_id("MECH-AUDIT-EVENT", {
            "session": record["session_id"],
            "event": event_type,
            "revision": len(self.store.audit_events(record["session_id"])) + 1,
            "detail": detail,
        })
        event = self.store.update_and_audit(
            record,
            event_id=event_id,
            event_type=event_type,
            actor_role=actor_role,
            state_before=state_before,
            detail=detail,
        )
        record["audit_chain_valid"] = self.store.verify_audit_chain(record["session_id"])
        return event

    def create_session(
        self,
        question: str,
        *,
        session_label: str = "founder-demo",
        questioner_role: str = "HUMAN_QUESTIONER",
    ) -> dict:
        clean_question = validate_question(question)
        session_id = f"MECH-SESSION-{uuid.uuid4().hex[:16].upper()}"
        now = _now()
        record = {
            "session_id": session_id,
            "state": "QUESTION_RECORDED",
            "question": clean_question,
            "session_label": session_label,
            "questioner_role": questioner_role,
            "object_graph": None,
            "receipt": None,
            "passport": None,
            "human_review": None,
            "audit_chain_valid": True,
            "boundary_label": BOUNDARY_LABEL,
            "created_at": now,
            "updated_at": now,
        }
        self.store.create(record)
        self._audit(record, "QUESTION_RECORDED", questioner_role, "NONE", {"question_digest": digest(clean_question)})
        return self.get_session(session_id)

    def propose_hypothesis(self, session_id: str) -> dict:
        record = self.store.get(session_id)
        if record["state"] != "QUESTION_RECORDED":
            raise RuntimeStateError("hypothesis proposal requires QUESTION_RECORDED")
        before = record["state"]
        record["object_graph"] = _build_graph(record["question"], session_id)
        record["state"] = "HYPOTHESIS_PROPOSED"
        record["updated_at"] = _now()
        self._audit(record, "AI_HYPOTHESIS_PROPOSED", "LOCAL_AI_ASSISTANT", before, {
            "hypothesis_id": record["object_graph"]["hypothesis"]["hypothesis_id"],
            "assistant_kind": "DETERMINISTIC_STRUCTURING_ASSISTANT_NOT_LLM",
        })
        return self.get_session(session_id)

    def revise_hypothesis(self, session_id: str, hypothesis: dict[str, Any]) -> dict:
        record = self.store.get(session_id)
        if record["state"] != "HYPOTHESIS_PROPOSED":
            raise RuntimeStateError("only a proposed hypothesis can be revised")
        validate_hypothesis(hypothesis)
        if hypothesis["hypothesis_id"] != record["object_graph"]["hypothesis"]["hypothesis_id"]:
            raise ContractError("revision cannot replace the stable hypothesis identity")
        record["object_graph"]["hypothesis"] = copy.deepcopy(hypothesis)
        record["object_graph"]["hypothesis"]["revision_id"] = hypothesis["revision_id"]
        record["updated_at"] = _now()
        self._audit(record, "HUMAN_HYPOTHESIS_REVISED", "HUMAN_REVIEWER", record["state"], {
            "revision_id": hypothesis["revision_id"], "hypothesis_digest": digest(hypothesis)
        })
        return self.get_session(session_id)

    def decide_before_run(self, session_id: str, *, decision: str, reviewer_label: str, reason: str) -> dict:
        record = self.store.get(session_id)
        if record["state"] != "HYPOTHESIS_PROPOSED":
            raise RuntimeStateError("pre-run decision requires HYPOTHESIS_PROPOSED")
        if decision not in PRE_RUN_DECISIONS:
            raise ContractError("unknown pre-run decision")
        reviewer = reviewer_label.strip()
        explanation = reason.strip()
        if len(reviewer) < 2 or len(explanation) < 10:
            raise ContractError("reviewer label and a meaningful reason are required")
        before = record["state"]
        if decision == "APPROVE":
            record["state"] = "APPROVED_TO_RUN"
            record["object_graph"]["experiment_design"]["status"] = "APPROVED_EXACT_SCOPE"
            record["object_graph"]["run_request"]["approved"] = True
            record["object_graph"]["run_request"]["approval"] = {
                "decision": decision,
                "reviewer_label": reviewer,
                "reason": explanation,
                "approved_at": _now(),
                "scope": "EXACT_FIXED_TINY_SYNTHETIC_REQUEST_ONLY",
            }
        elif decision == "REJECT":
            record["state"] = "REJECTED_BEFORE_RUN"
        else:
            record["state"] = "STOPPED_BEFORE_RUN"
        record["updated_at"] = _now()
        self._audit(record, f"HUMAN_{decision}_BEFORE_RUN", "HUMAN_APPROVER", before, {
            "reviewer_label": reviewer, "reason": explanation
        })
        return self.get_session(session_id)

    def run(self, session_id: str) -> dict:
        record = self.store.get(session_id)
        if record["state"] != "APPROVED_TO_RUN":
            raise RuntimeStateError("execution requires APPROVED_TO_RUN")
        before = record["state"]
        attempt_id = stable_id("MECH-RUN-ATTEMPT", {"session": session_id, "request": record["object_graph"]["run_request"]})
        started = _now()
        try:
            output, observed = execute_fixed_fixture(record["object_graph"])
            state = "RUN_COMPLETED_QUARANTINED"
            receipt_state = "RECEIPT_STRUCTURALLY_ACCEPTED"
            termination = "FIXED_EXECUTOR_COMPLETED"
        except (ContractError, RuntimeBoundaryError, TypeError, ValueError) as exc:
            output = {
                "passport_state": "MODEL_FAILURE",
                "quarantine_state": "QUARANTINED_EXECUTION_FAILURE",
                "error_class": type(exc).__name__,
                "boundary_label": BOUNDARY_LABEL,
            }
            observed = {
                "logical_cpu_workers": 1,
                "wall_time_seconds": 0,
                "incremental_memory_mib": 0,
                "output_bytes": len(canonical_json(output).encode("utf-8")),
                "cost_aud": 0,
                "network_used": False,
                "secrets_used": False,
                "subprocess_used": False,
            }
            state = "RUN_FAILED_QUARANTINED"
            receipt_state = "RECEIPT_REJECTED"
            termination = "FIXED_EXECUTOR_REFUSED_OR_FAILED"
        output_set_id = stable_id("MECH-OUTPUT-SET", {"attempt": attempt_id, "output": output})
        receipt_body = {
            "run_attempt_id": attempt_id,
            "run_request_id": record["object_graph"]["run_request"]["run_request_id"],
            "hypothesis_id": record["object_graph"]["hypothesis"]["hypothesis_id"],
            "experiment_id": record["object_graph"]["experiment_design"]["experiment_id"],
            "manifest_id": record["object_graph"]["reproducibility_manifest"]["manifest_id"],
            "configuration_id": record["object_graph"]["configuration_identity"]["configuration_id"],
            "output_set_id": output_set_id,
            "approval": record["object_graph"]["run_request"]["approval"],
            "requested_start": started,
            "observed_end": _now(),
            "termination": termination,
            "resource_ceiling": copy.deepcopy(RESOURCE_CEILING),
            "resources_observed": observed,
            "receipt_state": receipt_state,
            "output_digest": digest(output),
            "boundary_label": BOUNDARY_LABEL,
        }
        receipt = {
            "receipt_id": stable_id("MECH-RUN-RECEIPT", receipt_body),
            **receipt_body,
        }
        passport_state = output.get("passport_state", "MODEL_FAILURE")
        if passport_state not in PASSPORT_STATES:
            passport_state = "INCOMPLETE"
        passport_body = {
            "session_id": session_id,
            "hypothesis_id": receipt["hypothesis_id"],
            "run_receipt_id": receipt["receipt_id"],
            "output_set_id": output_set_id,
            "state": passport_state,
            "diagnostics": output,
            "quarantine_state": output["quarantine_state"],
            "scientific_claim": None,
            "regional_conclusion": None,
            "human_review_required": True,
            "limitations": [
                "This passport records a fictional runtime demonstration only.",
                "It is not an Environmental Evidence Passport and cannot support a real decision.",
            ],
            "boundary_label": BOUNDARY_LABEL,
        }
        record["receipt"] = receipt
        record["passport"] = {"passport_id": stable_id("MECH-EVIDENCE-PASSPORT", passport_body), **passport_body}
        record["state"] = state
        record["updated_at"] = _now()
        self._audit(record, "RUN_RECEIPT_AND_PASSPORT_QUARANTINED", "FIXED_LOCAL_EXECUTOR", before, {
            "receipt_id": receipt["receipt_id"],
            "passport_id": record["passport"]["passport_id"],
            "receipt_state": receipt_state,
            "passport_state": passport_state,
        })
        return self.get_session(session_id)

    def review(self, session_id: str, *, decision: str, reviewer_label: str, reason: str) -> dict:
        record = self.store.get(session_id)
        if record["state"] not in {"RUN_COMPLETED_QUARANTINED", "RUN_FAILED_QUARANTINED"}:
            raise RuntimeStateError("human review requires a quarantined run result")
        if decision not in POST_RUN_DECISIONS:
            raise ContractError("unknown post-run decision")
        if len(reviewer_label.strip()) < 2 or len(reason.strip()) < 10:
            raise ContractError("reviewer label and meaningful review reason are required")
        before = record["state"]
        state_map = {
            "ACCEPT_RUNTIME_DEMO": "REVIEWED_DEMO_ACCEPTED",
            "EVIDENCE_INSUFFICIENT": "REVIEWED_EVIDENCE_INSUFFICIENT",
            "REJECT_RUNTIME_DEMO": "REVIEWED_DEMO_REJECTED",
        }
        record["state"] = state_map[decision]
        record["human_review"] = {
            "decision": decision,
            "reviewer_label": reviewer_label.strip(),
            "reason": reason.strip(),
            "reviewed_at": _now(),
            "scientific_signoff": False,
            "release_as_environmental_evidence": False,
        }
        record["passport"]["quarantine_state"] = "REVIEWED_BUT_REMAINS_NON_ENVIRONMENTAL_DEMO"
        record["updated_at"] = _now()
        self._audit(record, "HUMAN_POST_RUN_REVIEW_RECORDED", "HUMAN_REVIEWER", before, record["human_review"])
        return self.get_session(session_id)

    def get_session(self, session_id: str) -> dict:
        record = self.store.get(session_id)
        record["audit_events"] = self.store.audit_events(session_id)
        record["audit_chain_valid"] = self.store.verify_audit_chain(session_id)
        return record

    def import_session_export(self, path: str | Path) -> dict:
        candidate = Path(path).resolve()
        value = json.loads(candidate.read_text(encoding="utf-8"))
        self.store.import_exported_session(value)
        return self.get_session(value["session_id"])

    def export_session(self, session_id: str, output_dir: str | Path) -> dict[str, str]:
        record = self.get_session(session_id)
        target = Path(output_dir)
        target.mkdir(parents=True, exist_ok=True)
        session_path = target / "task2000_runtime_session.json"
        receipt_path = target / "task2000_run_receipt.json"
        passport_path = target / "task2000_mechanism_evidence_passport.json"
        session_path.write_text(json.dumps(record, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        receipt_path.write_text(json.dumps(record["receipt"], indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        passport_path.write_text(json.dumps(record["passport"], indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        return {"session": str(session_path), "receipt": str(receipt_path), "passport": str(passport_path)}
