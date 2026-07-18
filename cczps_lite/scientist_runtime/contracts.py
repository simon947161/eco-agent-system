"""Closed contracts for the minimum ClimateOS scientist runtime."""

from __future__ import annotations

import hashlib
import json
import re
from typing import Any

SCHEMA_ID = "climateos.minimum_scientist_runtime.v0.1"
BOUNDARY_LABEL = "FICTIONAL_TINY_SYNTHETIC / LOCAL_ONLY / NOT_ENVIRONMENTAL_EVIDENCE"
FIXTURE_ID = "TINY-SYNTH-SCALAR-001"

SESSION_STATES = {
    "QUESTION_RECORDED",
    "HYPOTHESIS_PROPOSED",
    "APPROVED_TO_RUN",
    "REJECTED_BEFORE_RUN",
    "STOPPED_BEFORE_RUN",
    "RUN_COMPLETED_QUARANTINED",
    "RUN_FAILED_QUARANTINED",
    "REVIEWED_DEMO_ACCEPTED",
    "REVIEWED_EVIDENCE_INSUFFICIENT",
    "REVIEWED_DEMO_REJECTED",
}
PRE_RUN_DECISIONS = {"APPROVE", "REJECT", "STOP"}
POST_RUN_DECISIONS = {"ACCEPT_RUNTIME_DEMO", "EVIDENCE_INSUFFICIENT", "REJECT_RUNTIME_DEMO"}
PASSPORT_STATES = {
    "SUPPORTED_SYNTHETIC_ONLY",
    "PARTIAL_SYNTHETIC_ONLY",
    "INCOMPLETE",
    "CONTRADICTED_SYNTHETIC_ONLY",
    "NOT_TESTABLE",
    "MODEL_FAILURE",
}

RESOURCE_CEILING = {
    "logical_cpu_workers": 1,
    "incremental_memory_mib": 64,
    "wall_time_seconds": 5,
    "output_bytes": 100_000,
    "cost_aud": 0,
}

PROHIBITED_QUESTION_TERMS = {
    "bondo",
    "riverina",
    "tumut",
    "batlow",
    "wagga",
    "cooma",
    "graphcast",
    "wrf",
    "wrf-chem",
    "tianji",
}


class ContractError(ValueError):
    """Raised when a runtime object violates the closed local contract."""


def canonical_json(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def digest(value: Any) -> str:
    return "sha256:" + hashlib.sha256(canonical_json(value).encode("utf-8")).hexdigest()


def stable_id(prefix: str, value: Any) -> str:
    token = hashlib.sha256(canonical_json(value).encode("utf-8")).hexdigest()[:16].upper()
    return f"{prefix}-{token}"


def require_text(value: Any, label: str, *, minimum: int = 3, maximum: int = 3000) -> str:
    if not isinstance(value, str):
        raise ContractError(f"{label} must be text")
    result = value.strip()
    if not minimum <= len(result) <= maximum:
        raise ContractError(f"{label} length must be {minimum}..{maximum}")
    return result


def validate_question(question: Any) -> str:
    result = require_text(question, "question", minimum=10, maximum=500)
    lowered = result.casefold()
    matched = sorted(term for term in PROHIBITED_QUESTION_TERMS if re.search(rf"\b{re.escape(term)}\b", lowered))
    if matched:
        raise ContractError("Real-region or external-model terms are blocked: " + ", ".join(matched))
    return result


def validate_hypothesis(value: Any) -> dict[str, Any]:
    fields = {
        "hypothesis_id",
        "revision_id",
        "research_question",
        "hypothesis_statement",
        "mechanism_chain",
        "expected_direction",
        "diagnostics",
        "alternative_explanations",
        "falsification_criteria",
        "evidence_threshold",
        "scale_and_time_assumptions",
        "expert_owner_role",
        "limitations",
        "fixture_id",
        "boundary_label",
    }
    if not isinstance(value, dict) or set(value) != fields:
        raise ContractError("hypothesis object fields are not closed")
    validate_question(value["research_question"])
    for key in (
        "hypothesis_id",
        "revision_id",
        "hypothesis_statement",
        "expected_direction",
        "evidence_threshold",
        "scale_and_time_assumptions",
        "expert_owner_role",
    ):
        require_text(value[key], key)
    for key, minimum in (("mechanism_chain", 2), ("diagnostics", 1), ("alternative_explanations", 2), ("falsification_criteria", 1), ("limitations", 2)):
        items = value[key]
        if not isinstance(items, list) or len(items) < minimum or any(not isinstance(item, str) or not item.strip() for item in items):
            raise ContractError(f"{key} requires at least {minimum} non-empty text items")
    if value["fixture_id"] != FIXTURE_ID or value["boundary_label"] != BOUNDARY_LABEL:
        raise ContractError("hypothesis must remain bound to the fictional fixture")
    return value


def validate_resource_ceiling(value: Any) -> dict[str, int]:
    if value != RESOURCE_CEILING:
        raise ContractError("resource ceiling cannot be expanded")
    return value


def validate_object_graph(graph: Any) -> dict[str, Any]:
    required = {
        "schema_id",
        "session_id",
        "hypothesis",
        "experiment_design",
        "reproducibility_manifest",
        "configuration_identity",
        "run_request",
        "resource_ceiling",
        "boundary_label",
    }
    if not isinstance(graph, dict) or set(graph) != required:
        raise ContractError("runtime object graph fields are not closed")
    if graph["schema_id"] != SCHEMA_ID or graph["boundary_label"] != BOUNDARY_LABEL:
        raise ContractError("runtime object graph boundary changed")
    validate_hypothesis(graph["hypothesis"])
    validate_resource_ceiling(graph["resource_ceiling"])
    hypothesis_id = graph["hypothesis"]["hypothesis_id"]
    design = graph["experiment_design"]
    manifest = graph["reproducibility_manifest"]
    config = graph["configuration_identity"]
    request = graph["run_request"]
    if design.get("hypothesis_id") != hypothesis_id:
        raise ContractError("experiment design must bind the exact hypothesis")
    if manifest.get("experiment_id") != design.get("experiment_id"):
        raise ContractError("manifest must bind the exact experiment")
    if config.get("manifest_id") != manifest.get("manifest_id"):
        raise ContractError("configuration must bind the exact manifest")
    expected = {
        "session_id": graph["session_id"],
        "hypothesis_id": hypothesis_id,
        "experiment_id": design.get("experiment_id"),
        "manifest_id": manifest.get("manifest_id"),
        "configuration_id": config.get("configuration_id"),
    }
    for key, expected_value in expected.items():
        if request.get(key) != expected_value:
            raise ContractError(f"run request {key} identity mismatch")
    if request.get("fixture_id") != FIXTURE_ID or request.get("approved") is not False:
        raise ContractError("new run requests must start unapproved and fixture-bound")
    if manifest.get("network") != "DENIED_BY_DESIGN" or manifest.get("secrets") != "NOT_USED":
        raise ContractError("manifest network and secret boundaries changed")
    return graph
