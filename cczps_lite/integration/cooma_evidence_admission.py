"""Offline Cooma evidence-admission boundary for ClimateOS Task1671–1680.

The module validates repository-authored fictional records only. It contains no
source client, environmental data, model, monitor, compliance engine, customer
record, worksite record, legal interpretation, or operational WorkOS function.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

SCHEMA_ID = "climateos.cooma_evidence_admission.v0.1"
FIXTURE_ROOT = Path(__file__).resolve().parents[1] / "input"
SCALE_CLASSES = {
    "GLOBAL_CLIMATE": 1,
    "SOUTHEAST_AUSTRALIA_REGION": 2,
    "COOMA_REGIONAL_CONTEXT": 3,
    "TOWN_CATCHMENT": 4,
    "OBSERVATION_STATION": 5,
    "PROPERTY_OR_WORKSITE": 6,
}
EVIDENCE_CLASSES = {
    "OFFICIAL_PLANNING_INSTRUMENT_METADATA",
    "WATER_CATCHMENT_HYDROLOGY",
    "METEOROLOGICAL_OBSERVATION",
    "CLIMATE_REANALYSIS_OR_MODEL_OUTPUT",
    "WATER_WASTEWATER_INFRASTRUCTURE",
    "ECOLOGICAL_ENVIRONMENTAL",
    "LOCAL_OPERATIONAL_KNOWLEDGE",
    "PRIVATE_WORKSITE_RECORD",
    "EXPERT_REVIEW",
}
LICENCE_STATES = {"LICENCE_UNKNOWN", "RESTRICTED", "PRIVATE_WORKSITE", "QUARANTINED"}
REQUIRED_TRANSLATION_CHECKS = {
    "SOURCE_IDENTITY",
    "LICENCE",
    "SPATIAL_OVERLAP_DISTANCE_ELEVATION",
    "TEMPORAL_ALIGNMENT",
    "METHOD_COMPATIBILITY",
    "UNCERTAINTY_PROPAGATION",
    "STATIONARITY",
    "HUMAN_REVIEW",
}
ROLE_CLASSES = {
    "ENVIRONMENTAL_EVIDENCE_STEWARD",
    "WATER_SYSTEMS_REVIEWER",
    "PLANNING_INSTRUMENT_REVIEWER",
    "GIS_SPATIAL_REVIEWER",
    "DOMAIN_EXPERT",
    "WORKOS_ACCOUNTABLE_OFFICER",
}
REQUIRED_INTERFACE_BLOCKS = {
    "CUSTOMER_OR_PERSON_IDENTITY",
    "PROPERTY_OR_WORKSITE_ADDRESS",
    "INSPECTION_NOTES",
    "ENFORCEMENT_STATE",
    "COMPLIANCE_DECISION",
    "LEGAL_ADVICE",
    "OPERATIONAL_JOB_INSTRUCTION",
    "PRIVATE_WORKOS_RECORD",
}
REQUIRED_INTERFACE_ALLOWED = {
    "PLACE_ANCHOR",
    "EVIDENCE_ID_AND_CLASS",
    "SCALE_AND_TIME_SCOPE",
    "LICENCE_AND_VISIBILITY_STATE",
    "UNCERTAINTY_AND_STATIONARITY",
    "PROHIBITED_USES",
    "HUMAN_REVIEW_STATE",
}


class CoomaAdmissionError(ValueError):
    """Raised when a record tries to cross the authorized boundary."""


def _strict(value: Any, fields: set[str], label: str) -> dict[str, Any]:
    if not isinstance(value, dict):
        raise CoomaAdmissionError(f"{label} must be an object")
    missing = fields - set(value)
    unknown = set(value) - fields
    if missing or unknown:
        raise CoomaAdmissionError(
            f"{label} fields invalid; missing={sorted(missing)}, unknown={sorted(unknown)}"
        )
    return value


def _text(value: Any, label: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise CoomaAdmissionError(f"{label} must be a non-empty string")
    return value


def _strings(value: Any, label: str, *, non_empty: bool = False) -> list[str]:
    if not isinstance(value, list) or (non_empty and not value):
        raise CoomaAdmissionError(f"{label} must be a{' non-empty' if non_empty else ''} list")
    result = [_text(item, label) for item in value]
    if len(result) != len(set(result)):
        raise CoomaAdmissionError(f"{label} must contain unique values")
    return result


def load_fictional_cooma_pack(path: str | Path) -> dict[str, Any]:
    """Load and validate a repository-local fictional Cooma pack."""
    if isinstance(path, str) and "://" in path:
        raise CoomaAdmissionError("URL and network sources are blocked")
    fixture = Path(path).resolve()
    try:
        fixture.relative_to(FIXTURE_ROOT.resolve())
    except ValueError as exc:
        raise CoomaAdmissionError("Cooma fixtures must stay under cczps_lite/input") from exc
    with fixture.open("r", encoding="utf-8") as stream:
        pack = json.load(stream)
    validate_cooma_admission_pack(pack)
    return pack


def validate_cooma_admission_pack(value: Any) -> None:
    fields = {
        "schema_id", "research_anchor", "scale_objects", "evidence_classes",
        "candidate_records", "translation_rules", "review_roles",
        "climateos_workos_interface", "boundaries",
    }
    pack = _strict(value, fields, "root")
    if pack["schema_id"] != SCHEMA_ID:
        raise CoomaAdmissionError("Unsupported schema_id")
    _validate_anchor(pack["research_anchor"])
    _validate_boundaries(pack["boundaries"])

    evidence_classes = set(_strings(pack["evidence_classes"], "evidence_classes", non_empty=True))
    if evidence_classes != EVIDENCE_CLASSES:
        raise CoomaAdmissionError("The complete bounded evidence-class registry is required")
    scale_ids = _validate_scales(pack["scale_objects"])
    _validate_candidates(pack["candidate_records"], scale_ids, evidence_classes)
    _validate_translations(pack["translation_rules"], scale_ids)
    _validate_roles(pack["review_roles"])
    _validate_interface(pack["climateos_workos_interface"])


def _validate_anchor(value: Any) -> None:
    fields = {
        "place_name", "anchor_status", "purpose", "future_work_context",
        "exact_worksite", "planning_terms_state", "local_conclusion_state",
    }
    anchor = _strict(value, fields, "research_anchor")
    expected = {
        "place_name": "Cooma",
        "anchor_status": "NAMED_REAL_PLACE_NO_SOURCE_VERIFICATION",
        "purpose": "LONG_TERM_ENVIRONMENTAL_CONTEXT_AND_WATER_PROTECTION_SUPPORT",
        "future_work_context": "SEPARATE_WORKOS_BACKFLOW_LIQUID_TRADE_WASTE",
        "exact_worksite": "NOT_PROVIDED_NOT_REQUIRED",
        "planning_terms_state": "RP_DCP_TERMS_REQUIRE_FUTURE_OFFICIAL_VERIFICATION",
        "local_conclusion_state": "NONE",
    }
    for field, expected_value in expected.items():
        if anchor[field] != expected_value:
            raise CoomaAdmissionError(f"{field} crosses the authorized Cooma anchor boundary")


def _validate_boundaries(value: Any) -> None:
    fields = {
        "network_used", "source_accessed", "real_data_acquired", "model_executed",
        "monitoring_active", "external_action", "private_worksite_data_included",
        "customer_or_person_data_included", "compliance_decision_formed",
        "local_environmental_conclusion_formed", "cost_aud", "human_review_required",
    }
    boundaries = _strict(value, fields, "boundaries")
    false_fields = fields - {"cost_aud", "human_review_required"}
    if any(boundaries[field] is not False for field in false_fields):
        raise CoomaAdmissionError("Source, data, model, monitoring, private data, action and conclusions must remain false")
    if boundaries["cost_aud"] != 0 or isinstance(boundaries["cost_aud"], bool):
        raise CoomaAdmissionError("cost_aud must remain zero")
    if boundaries["human_review_required"] is not True:
        raise CoomaAdmissionError("human_review_required must remain true")


def _validate_scales(value: Any) -> set[str]:
    if not isinstance(value, list) or len(value) != len(SCALE_CLASSES):
        raise CoomaAdmissionError("Exactly six scale objects are required")
    fields = {"scale_id", "scale_class", "rank", "label", "boundary_status", "automatic_translation_allowed"}
    scale_ids: set[str] = set()
    seen_classes: set[str] = set()
    seen_ranks: set[int] = set()
    for item in value:
        scale = _strict(item, fields, "scale object")
        scale_id = _text(scale["scale_id"], "scale_id")
        scale_class = scale["scale_class"]
        if scale_class not in SCALE_CLASSES or scale["rank"] != SCALE_CLASSES[scale_class]:
            raise CoomaAdmissionError("Scale class and rank do not match the controlled hierarchy")
        if scale["boundary_status"] != "CONCEPT_ONLY_NOT_ACQUIRED":
            raise CoomaAdmissionError("Scale boundaries have not been acquired")
        if scale["automatic_translation_allowed"] is not False:
            raise CoomaAdmissionError("Automatic scale translation is blocked")
        _text(scale["label"], "scale label")
        if scale_id in scale_ids or scale_class in seen_classes or scale["rank"] in seen_ranks:
            raise CoomaAdmissionError("Scale IDs, classes and ranks must be unique")
        scale_ids.add(scale_id)
        seen_classes.add(scale_class)
        seen_ranks.add(scale["rank"])
    if seen_classes != set(SCALE_CLASSES):
        raise CoomaAdmissionError("The complete controlled scale hierarchy is required")
    return scale_ids


def _validate_candidates(value: Any, scale_ids: set[str], evidence_classes: set[str]) -> None:
    if not isinstance(value, list) or not value:
        raise CoomaAdmissionError("candidate_records must be a non-empty list")
    fields = {
        "record_id", "fictional", "title", "evidence_class", "authority_state",
        "source_identity_state", "external_locator", "scale_id", "spatial_footprint_state",
        "licence_state", "visibility_state", "observed_time", "published_time",
        "retrieved_time", "revision_state", "content_retained", "temporal_alignment_state",
        "uncertainty", "review_state", "admission_decision", "allowed_uses", "prohibited_uses",
    }
    record_ids: set[str] = set()
    for item in value:
        record = _strict(item, fields, "candidate record")
        record_id = _text(record["record_id"], "record_id")
        _text(record["title"], "candidate title")
        if record_id in record_ids:
            raise CoomaAdmissionError(f"Duplicate candidate record_id: {record_id}")
        record_ids.add(record_id)
        if record["fictional"] is not True:
            raise CoomaAdmissionError("Only fictional candidate records are authorized")
        if record["evidence_class"] not in evidence_classes or record["scale_id"] not in scale_ids:
            raise CoomaAdmissionError("Candidate references an unknown evidence class or scale")
        expected = {
            "authority_state": "UNVERIFIED_FIXTURE",
            "source_identity_state": "NOT_ACCESSED",
            "spatial_footprint_state": "NOT_ACQUIRED",
            "revision_state": "FICTIONAL_V0",
            "temporal_alignment_state": "NOT_TESTABLE_NO_SOURCE",
            "review_state": "NOT_REVIEWED",
            "admission_decision": "BLOCKED_NO_SOURCE_ACCESS",
        }
        for field, expected_value in expected.items():
            if record[field] != expected_value:
                raise CoomaAdmissionError(f"Candidate {field} is not authorized")
        if record["external_locator"] is not None or record["content_retained"] is not False:
            raise CoomaAdmissionError("External locator and retained content are blocked")
        if any(record[field] is not None for field in ("observed_time", "published_time", "retrieved_time")):
            raise CoomaAdmissionError("Real observation, publication and retrieval times are blocked")
        if record["licence_state"] not in LICENCE_STATES:
            raise CoomaAdmissionError("Unverified records cannot claim reuse permission")
        if record["visibility_state"] not in {"NOT_CHECKED", "PRIVATE_NOT_INCLUDED"}:
            raise CoomaAdmissionError("Source visibility has not been checked")
        if record["allowed_uses"] != ["INTERFACE_TEST_ONLY"]:
            raise CoomaAdmissionError("Candidate use must remain interface-test-only")
        _strings(record["prohibited_uses"], "prohibited_uses", non_empty=True)
        _validate_uncertainty(record["uncertainty"])


def _validate_uncertainty(value: Any) -> None:
    fields = {
        "data_quality", "spatial_representativeness", "temporal_alignment",
        "stationarity", "alternative_explanations",
    }
    uncertainty = _strict(value, fields, "uncertainty")
    if any(uncertainty[field] != "NOT_ASSESSED" for field in fields):
        raise CoomaAdmissionError("Uncertainty cannot be assessed without admitted evidence")


def _validate_translations(value: Any, scale_ids: set[str]) -> None:
    if not isinstance(value, list) or not value:
        raise CoomaAdmissionError("translation_rules must be a non-empty list")
    fields = {
        "rule_id", "from_scale_id", "to_scale_id", "status", "required_checks",
        "automatic_translation", "output_state", "prohibited_inference",
    }
    rule_ids: set[str] = set()
    for item in value:
        rule = _strict(item, fields, "translation rule")
        rule_id = _text(rule["rule_id"], "rule_id")
        if rule_id in rule_ids:
            raise CoomaAdmissionError(f"Duplicate translation rule_id: {rule_id}")
        rule_ids.add(rule_id)
        if rule["from_scale_id"] not in scale_ids or rule["to_scale_id"] not in scale_ids:
            raise CoomaAdmissionError("Translation references an unknown scale")
        if rule["from_scale_id"] == rule["to_scale_id"]:
            raise CoomaAdmissionError("Translation must cross explicitly named scales")
        if set(_strings(rule["required_checks"], "required_checks", non_empty=True)) != REQUIRED_TRANSLATION_CHECKS:
            raise CoomaAdmissionError("Every translation gate must retain all required checks")
        if rule["status"] != "SPECIFICATION_ONLY" or rule["automatic_translation"] is not False:
            raise CoomaAdmissionError("Translation remains specification-only and manual")
        if rule["output_state"] != "BLOCKED_PENDING_EVIDENCE_AND_HUMAN_REVIEW":
            raise CoomaAdmissionError("Translation output must remain blocked")
        _text(rule["prohibited_inference"], "prohibited_inference")


def _validate_roles(value: Any) -> None:
    if not isinstance(value, list) or not value:
        raise CoomaAdmissionError("review_roles must be a non-empty list")
    fields = {"role_id", "role_class", "appointment_state", "decision_authority"}
    role_ids: set[str] = set()
    role_classes: set[str] = set()
    for item in value:
        role = _strict(item, fields, "review role")
        role_id = _text(role["role_id"], "role_id")
        if role_id in role_ids or role["role_class"] in role_classes:
            raise CoomaAdmissionError("Review role IDs and classes must be unique")
        role_ids.add(role_id)
        role_classes.add(role["role_class"])
        if role["role_class"] not in ROLE_CLASSES:
            raise CoomaAdmissionError("Unsupported review role")
        if role["appointment_state"] != "UNASSIGNED" or role["decision_authority"] != "NONE_IN_THIS_BATCH":
            raise CoomaAdmissionError("No reviewer appointment or authority is authorized")
    if role_classes != ROLE_CLASSES:
        raise CoomaAdmissionError("The complete review-role boundary is required")


def _validate_interface(value: Any) -> None:
    fields = {
        "interface_status", "climateos_role", "workos_role", "allowed_context_fields",
        "blocked_fields", "writeback_state",
    }
    interface = _strict(value, fields, "ClimateOS-WorkOS interface")
    expected = {
        "interface_status": "SPECIFICATION_ONLY",
        "climateos_role": "REGIONAL_ENVIRONMENTAL_CONTEXT_AND_EVIDENCE_GOVERNANCE",
        "workos_role": "FUTURE_OPERATIONAL_BACKFLOW_LIQUID_TRADE_WASTE_WORK",
        "writeback_state": "BLOCKED_PENDING_SEPARATE_AUTHORIZATION",
    }
    for field, expected_value in expected.items():
        if interface[field] != expected_value:
            raise CoomaAdmissionError(f"Interface {field} crosses the authorized boundary")
    allowed = set(_strings(interface["allowed_context_fields"], "allowed_context_fields", non_empty=True))
    blocked = set(_strings(interface["blocked_fields"], "blocked_fields", non_empty=True))
    if allowed != REQUIRED_INTERFACE_ALLOWED:
        raise CoomaAdmissionError("Interface context fields must match the fixed safe allowlist")
    if not REQUIRED_INTERFACE_BLOCKS <= blocked:
        raise CoomaAdmissionError("Private, compliance, legal and operational fields must remain blocked")
    if allowed & blocked:
        raise CoomaAdmissionError("Allowed and blocked interface fields must be disjoint")


def build_cooma_admission_preview(pack: dict[str, Any]) -> dict[str, Any]:
    """Build a deterministic preview; it admits no evidence or local conclusion."""
    validate_cooma_admission_pack(pack)
    records_by_class: dict[str, int] = {}
    for record in pack["candidate_records"]:
        evidence_class = record["evidence_class"]
        records_by_class[evidence_class] = records_by_class.get(evidence_class, 0) + 1
    return {
        "schema_id": SCHEMA_ID,
        "place_name": "Cooma",
        "classification": "FICTIONAL_EVIDENCE_ADMISSION_PREVIEW_ONLY",
        "scale_count": len(pack["scale_objects"]),
        "candidate_record_count": len(pack["candidate_records"]),
        "candidate_records_by_class": dict(sorted(records_by_class.items())),
        "translation_rule_count": len(pack["translation_rules"]),
        "review_role_count": len(pack["review_roles"]),
        "admitted_evidence_count": 0,
        "source_access_count": 0,
        "local_environmental_conclusion": "NONE",
        "compliance_decision": "NONE",
        "workos_interface_status": "SPECIFICATION_ONLY_NO_PRIVATE_OR_OPERATIONAL_DATA",
        "next_gate": "FOUNDER_DECISION_BEFORE_ANY_REAL_SOURCE_OR_TASK1681",
    }
