"""Offline Task1701-1710 no-run mechanism experiment return gate."""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any

SCHEMA_ID = "climateos.mechanism_return_gate.v0.1"
BASE_MAIN_SHA = "5bfc2312b8d93783de7e94af57d8a86351f71563"
ASSESSMENT_DATE = "2026-07-17"
INPUT_ROOT = Path(__file__).resolve().parents[1] / "input"

REFERENCE_REGISTRY = {
    "MECH-REF-001": ("PAPER", "PAPER_REFERENCE_ONLY", "PREPRINT"),
    "MECH-REF-002": ("SUPPORTING_REPOSITORY", "MIT_ARTIFACTS_THIRD_PARTY_SEPARATE", "CURATED_ARTIFACTS_NOT_FULL_RUNTIME"),
    "MECH-REF-003": ("MODEL_REPOSITORY", "PUBLIC_DOMAIN_NOTICE_TRADEMARK_RESERVED", "RELEASE_BRANCH_CANDIDATE"),
    "MECH-REF-004": ("ALTERNATIVE_AGENT_SYSTEM", "RESPONSIBLE_SOURCE_LICENCE_REVIEW_REQUIRED", "PUBLIC_AUTONOMOUS_CODEBASE"),
    "MECH-REF-005": ("PAPER", "PAPER_REFERENCE_ONLY", "PREPRINT"),
}
COMPONENT_NAMES = {
    "WRF_CORE", "WRF_CHEM", "WPS", "PHYSICS_AND_CHEMISTRY_OPTIONS",
    "INPUT_AND_BOUNDARY_ASSETS", "COMPUTE_ENVIRONMENT",
}
HYPOTHESIS_FIELDS = {
    "research_question", "hypothesis", "mechanism_chain", "expected_direction",
    "required_diagnostics", "alternative_explanations", "falsification_criteria",
    "evidence_threshold", "scale_and_time_assumptions", "expert_owner",
}
EXPERIMENT_FIELDS = {
    "baseline", "perturbation", "control", "sensitivity", "model_version",
    "configuration_hash", "input_identity", "boundary_identity", "diagnostics",
    "stop_conditions", "compute_ceiling", "failure_log",
}
OUTCOMES = {
    "READY_FOR_TINY_SYNTHETIC_DESIGN_GATE", "REFERENCE_REVIEW_INCOMPLETE",
    "LICENCE_OR_VERSION_BLOCKED", "DATA_OR_COMPUTE_NOT_READY",
    "EXPERT_REVIEW_REQUIRED", "NOT_TESTABLE", "DO_NOT_PROCEED",
}
BOUNDARY_FALSE_FIELDS = {
    "repository_cloned", "archive_downloaded", "dataset_downloaded",
    "observation_acquired", "model_installed", "model_executed", "cloud_used",
    "api_key_used", "monitoring_active", "workos_data_used",
    "scientific_conclusion_formed", "local_conclusion_formed",
}


class MechanismReturnGateError(ValueError):
    """Raised when a pack crosses the no-run return-gate boundary."""


def _strict(value: Any, fields: set[str], label: str) -> dict[str, Any]:
    if not isinstance(value, dict):
        raise MechanismReturnGateError(f"{label} must be an object")
    missing, unknown = fields - set(value), set(value) - fields
    if missing or unknown:
        raise MechanismReturnGateError(f"{label} fields invalid: missing={sorted(missing)} unknown={sorted(unknown)}")
    return value


def _text(value: Any, label: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise MechanismReturnGateError(f"{label} must be non-empty text")
    return value


def _unique_strings(value: Any, label: str) -> set[str]:
    if not isinstance(value, list) or not value or any(not isinstance(x, str) or not x for x in value):
        raise MechanismReturnGateError(f"{label} must be a non-empty string list")
    if len(value) != len(set(value)):
        raise MechanismReturnGateError(f"{label} must be unique")
    return set(value)


def load_mechanism_return_gate(path: str | Path) -> dict[str, Any]:
    if isinstance(path, str) and "://" in path:
        raise MechanismReturnGateError("Runtime URL loading is blocked")
    candidate = Path(path).resolve()
    try:
        candidate.relative_to(INPUT_ROOT.resolve())
    except ValueError as exc:
        raise MechanismReturnGateError("Gate packs must stay under cczps_lite/input") from exc
    with candidate.open("r", encoding="utf-8") as stream:
        pack = json.load(stream)
    validate_mechanism_return_gate(pack)
    return pack


def validate_mechanism_return_gate(value: Any) -> None:
    root_fields = {"schema_id", "gate", "references", "model_components", "hypothesis_contract", "experiment_contract", "readiness", "trials", "decision", "boundaries"}
    pack = _strict(value, root_fields, "root")
    if pack["schema_id"] != SCHEMA_ID:
        raise MechanismReturnGateError("Unsupported schema ID")
    _validate_gate(pack["gate"])
    _validate_references(pack["references"])
    _validate_components(pack["model_components"])
    _validate_contracts(pack["hypothesis_contract"], pack["experiment_contract"])
    _validate_readiness(pack["readiness"])
    _validate_trials(pack["trials"])
    _validate_decision(pack["decision"])
    _validate_boundaries(pack["boundaries"])


def _validate_gate(value: Any) -> None:
    gate = _strict(value, {"base_main_sha", "task_range", "mode", "assessed_on"}, "gate")
    expected = {"base_main_sha": BASE_MAIN_SHA, "task_range": "TASK1701_1710", "mode": "NO_RUN_REFERENCE_REVALIDATION", "assessed_on": ASSESSMENT_DATE}
    if gate != expected:
        raise MechanismReturnGateError("Gate identity or authorized base changed")


def _validate_references(value: Any) -> None:
    if not isinstance(value, list) or len(value) != 5:
        raise MechanismReturnGateError("Exactly five bounded references are required")
    fields = {"reference_id", "name", "kind", "canonical_url", "identity", "licence_state", "artifact_state", "runtime_state", "climateos_use"}
    seen = set()
    for item in value:
        ref = _strict(item, fields, "reference")
        ref_id = _text(ref["reference_id"], "reference_id")
        if re.fullmatch(r"MECH-REF-[0-9]{3}", ref_id) is None or ref_id not in REFERENCE_REGISTRY or ref_id in seen:
            raise MechanismReturnGateError("Reference ID must be unique and registered")
        seen.add(ref_id)
        if (ref["kind"], ref["licence_state"], ref["artifact_state"]) != REFERENCE_REGISTRY[ref_id]:
            raise MechanismReturnGateError("Reference kind, licence and artifact state are fixed")
        if not _text(ref["canonical_url"], "canonical_url").startswith("https://"):
            raise MechanismReturnGateError("Reference URL must use HTTPS")
        _text(ref["name"], "reference name"); _text(ref["identity"], "reference identity")
        if ref["runtime_state"] != "NOT_ADMITTED_NOT_EXECUTED" or ref["climateos_use"] != "REFERENCE_ONLY":
            raise MechanismReturnGateError("References cannot become runtime dependencies")


def _validate_components(value: Any) -> None:
    if not isinstance(value, list) or len(value) != 6:
        raise MechanismReturnGateError("Exactly six separated model components are required")
    fields = {"component_id", "name", "role", "version_identity", "licence_state", "dependency_state", "admission_state"}
    names, ids = set(), set()
    for item in value:
        component = _strict(item, fields, "model component")
        component_id = _text(component["component_id"], "component_id")
        if re.fullmatch(r"MECH-COMP-[0-9]{3}", component_id) is None or component_id in ids:
            raise MechanismReturnGateError("Component IDs must be unique MECH-COMP-NNN values")
        ids.add(component_id); names.add(component["name"])
        for field in ("role", "version_identity", "licence_state", "dependency_state"):
            _text(component[field], field)
        if component["admission_state"] not in {"REFERENCE_CANDIDATE_ONLY", "UNRESOLVED_BLOCKED"}:
            raise MechanismReturnGateError("Model component cannot be admitted for execution")
    if names != COMPONENT_NAMES:
        raise MechanismReturnGateError("WRF components must remain explicitly separated")


def _validate_contracts(hypothesis_value: Any, experiment_value: Any) -> None:
    hypothesis = _strict(hypothesis_value, {"required_fields", "causal_claim_prohibited", "expert_owner_required", "not_testable_is_valid"}, "hypothesis contract")
    if _unique_strings(hypothesis["required_fields"], "hypothesis fields") != HYPOTHESIS_FIELDS:
        raise MechanismReturnGateError("Hypothesis contract fields changed")
    if any(hypothesis[field] is not True for field in ("causal_claim_prohibited", "expert_owner_required", "not_testable_is_valid")):
        raise MechanismReturnGateError("Hypothesis safeguards must remain enabled")
    experiment = _strict(experiment_value, {"required_fields", "immutable_registration_required", "run_permission", "allowed_outcomes"}, "experiment contract")
    if _unique_strings(experiment["required_fields"], "experiment fields") != EXPERIMENT_FIELDS:
        raise MechanismReturnGateError("Experiment contract fields changed")
    if experiment["immutable_registration_required"] is not True or experiment["run_permission"] != "NOT_AUTHORIZED":
        raise MechanismReturnGateError("Experiment execution is not authorized")
    if _unique_strings(experiment["allowed_outcomes"], "allowed outcomes") != OUTCOMES:
        raise MechanismReturnGateError("Return-gate outcomes changed")


def _validate_readiness(value: Any) -> None:
    fields = {"reference_identity", "version", "licence", "data", "compute", "expert", "reproducibility", "overall"}
    readiness = _strict(value, fields, "readiness")
    expected = {"reference_identity": "PARTIAL_PASS", "version": "CANDIDATE_LOCK_REQUIRES_RELEASE_RECHECK", "licence": "COMPONENT_LEVEL_REVIEW_REQUIRED", "data": "NOT_ADMITTED", "compute": "NOT_ADMITTED", "expert": "UNASSIGNED", "reproducibility": "CURATED_ARTIFACTS_NOT_FULL_REPRODUCTION", "overall": "REFERENCE_REVIEW_INCOMPLETE"}
    if readiness != expected:
        raise MechanismReturnGateError("Readiness cannot be promoted by this batch")


def _validate_trials(value: Any) -> None:
    if not isinstance(value, list) or len(value) != 2:
        raise MechanismReturnGateError("Exactly two no-run trials are required")
    expected = {"REGISTER_NO_RUN_CONTRACT": "ALLOW_STATIC_REGISTRATION", "START_WRF_CHEM_EXPERIMENT": "REJECT_EXECUTION"}
    fields = {"trial_id", "request", "expected", "actual", "run_performed", "reason"}
    seen = set()
    for item in value:
        trial = _strict(item, fields, "trial")
        trial_id = _text(trial["trial_id"], "trial_id")
        if re.fullmatch(r"MECH-GATE-TRIAL-[0-9]{3}", trial_id) is None or trial_id in seen:
            raise MechanismReturnGateError("Trial IDs must be unique")
        seen.add(trial_id)
        if trial["request"] not in expected or trial["expected"] != expected[trial["request"]] or trial["actual"] != expected[trial["request"]]:
            raise MechanismReturnGateError("Trial result violates the no-run gate")
        if trial["run_performed"] is not False:
            raise MechanismReturnGateError("No scientific run may be performed")
        _text(trial["reason"], "trial reason")


def _validate_decision(value: Any) -> None:
    fields = {"state", "model_run_authorized", "tiny_synthetic_execution_authorized", "task1711_authorized", "reason", "next_gate"}
    decision = _strict(value, fields, "decision")
    if decision["state"] != "REFERENCE_REVIEW_INCOMPLETE" or decision["next_gate"] != "SEPARATE_FOUNDER_AUTHORIZATION_REQUIRED":
        raise MechanismReturnGateError("Decision cannot cross the independent Founder gate")
    if any(decision[field] is not False for field in ("model_run_authorized", "tiny_synthetic_execution_authorized", "task1711_authorized")):
        raise MechanismReturnGateError("Execution and Task1711 remain unauthorized")
    _text(decision["reason"], "decision reason")


def _validate_boundaries(value: Any) -> None:
    fields = BOUNDARY_FALSE_FIELDS | {"public_metadata_read", "cost_aud", "human_review_required"}
    boundary = _strict(value, fields, "boundaries")
    if boundary["public_metadata_read"] is not True or boundary["human_review_required"] is not True or boundary["cost_aud"] != 0:
        raise MechanismReturnGateError("Metadata, cost or review boundary changed")
    if any(boundary[field] is not False for field in BOUNDARY_FALSE_FIELDS):
        raise MechanismReturnGateError("A prohibited runtime, data or conclusion boundary was crossed")


def build_mechanism_return_gate_preview(pack: dict[str, Any]) -> dict[str, Any]:
    validate_mechanism_return_gate(pack)
    return {
        "schema_id": pack["schema_id"],
        "base_main_sha": pack["gate"]["base_main_sha"],
        "reference_count": len(pack["references"]),
        "component_count": len(pack["model_components"]),
        "wrf_candidate": next(x["identity"] for x in pack["references"] if x["reference_id"] == "MECH-REF-003"),
        "readiness": pack["decision"]["state"],
        "model_run": "NOT_AUTHORIZED_NOT_EXECUTED",
        "task1711": "SEPARATE_FOUNDER_GATE",
        "cost_aud": pack["boundaries"]["cost_aud"],
    }
