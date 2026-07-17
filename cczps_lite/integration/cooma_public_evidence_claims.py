"""Offline validator for the Task1691–1700 Cooma structured-claim pilot.

The committed pack contains controlled paraphrases of three manually inspected
official HTML pages.  This module has no HTTP client, downloader, model,
monitor, WorkOS connector, or conclusion engine.
"""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any

SCHEMA_ID = "climateos.cooma_public_evidence_claims.v0.1"
BASE_MAIN_SHA = "b6c495b81e0a74afac1971f5b18366cb1aa1f99c"
ACCESS_DATE = "2026-07-17"
FIXTURE_ROOT = Path(__file__).resolve().parents[1] / "input"

SOURCE_REGISTRY = {
    "COOMA-SRC-006": {
        "publisher": "Snowy Monaro Regional Council",
        "canonical_url": "https://www.snowymonaro.nsw.gov.au/Water-and-Wastewater/Water-Supply/Where-Does-My-Water-Come-From",
        "source_kind": "COUNCIL_WATER_SOURCE_LANDING",
    },
    "COOMA-SRC-007": {
        "publisher": "Australian Bureau of Meteorology",
        "canonical_url": "https://www.bom.gov.au/climate/averages/tables/cw_070217.shtml",
        "source_kind": "STATION_METADATA",
    },
    "COOMA-SRC-009": {
        "publisher": "Australian Government Department of Climate Change, Energy, the Environment and Water",
        "canonical_url": "https://www.dcceew.gov.au/cewh/water-region/murrumbidgee-river-valley/about",
        "source_kind": "FEDERAL_CATCHMENT_CONTEXT",
    },
}
CLAIM_TYPES = {
    "WATER_SOURCE_DESCRIPTION",
    "WATER_TREATMENT_DESCRIPTION",
    "STATION_IDENTITY",
    "STATION_LOCATION_METADATA",
    "BROAD_VALLEY_GEOGRAPHY",
}
CLAIM_TYPE_TO_SOURCE = {
    "WATER_SOURCE_DESCRIPTION": "COOMA-SRC-006",
    "WATER_TREATMENT_DESCRIPTION": "COOMA-SRC-006",
    "STATION_IDENTITY": "COOMA-SRC-007",
    "STATION_LOCATION_METADATA": "COOMA-SRC-007",
    "BROAD_VALLEY_GEOGRAPHY": "COOMA-SRC-009",
}
CLAIM_TYPE_TO_GEOGRAPHY = {
    "WATER_SOURCE_DESCRIPTION": "DIRECT_COOMA",
    "WATER_TREATMENT_DESCRIPTION": "DIRECT_COOMA",
    "STATION_IDENTITY": "OBSERVATION_STATION",
    "STATION_LOCATION_METADATA": "OBSERVATION_STATION",
    "BROAD_VALLEY_GEOGRAPHY": "MURRUMBIDGEE_VALLEY",
}
GEOGRAPHIES = {"DIRECT_COOMA", "OBSERVATION_STATION", "MURRUMBIDGEE_VALLEY"}
RELATION_OUTCOMES = {
    "REJECTED_SCALE_AND_REVIEW_GAPS",
    "REJECTED_NO_REPRESENTATIVENESS_OR_OBSERVATIONS",
}
GATE_FIELDS = {
    "source_identity", "licence", "geography", "temporal_alignment",
    "uncertainty", "stationarity", "expert_review",
}
SOURCE_ID_RE = re.compile(r"COOMA-SRC-[0-9]{3}")
CLAIM_ID_RE = re.compile(r"COOMA-CLAIM-[0-9]{3}")
RELATION_ID_RE = re.compile(r"COOMA-REL-TRIAL-[0-9]{3}")


class CoomaClaimError(ValueError):
    """Raised when a claim pack crosses the authorized admission boundary."""


def _strict(value: Any, fields: set[str], label: str) -> dict[str, Any]:
    if not isinstance(value, dict):
        raise CoomaClaimError(f"{label} must be an object")
    missing = fields - set(value)
    unknown = set(value) - fields
    if missing or unknown:
        raise CoomaClaimError(
            f"{label} fields invalid; missing={sorted(missing)}, unknown={sorted(unknown)}"
        )
    return value


def _text(value: Any, label: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise CoomaClaimError(f"{label} must be a non-empty string")
    return value


def _strings(value: Any, label: str, *, non_empty: bool = False) -> list[str]:
    if not isinstance(value, list) or (non_empty and not value):
        raise CoomaClaimError(f"{label} must be a list")
    result = [_text(item, label) for item in value]
    if len(result) != len(set(result)):
        raise CoomaClaimError(f"{label} must contain unique values")
    return result


def load_cooma_claim_pack(path: str | Path) -> dict[str, Any]:
    """Load a repository-local claim pack; runtime URL loading is blocked."""
    if isinstance(path, str) and "://" in path:
        raise CoomaClaimError("Runtime URL loading is blocked")
    fixture = Path(path).resolve()
    try:
        fixture.relative_to(FIXTURE_ROOT.resolve())
    except ValueError as exc:
        raise CoomaClaimError("Claim fixtures must stay under cczps_lite/input") from exc
    with fixture.open("r", encoding="utf-8") as stream:
        pack = json.load(stream)
    validate_cooma_claim_pack(pack)
    return pack


def validate_cooma_claim_pack(value: Any) -> None:
    pack = _strict(
        value,
        {"schema_id", "pilot", "selected_sources", "claims", "relation_trials", "transition_review", "boundaries"},
        "root",
    )
    if pack["schema_id"] != SCHEMA_ID:
        raise CoomaClaimError("Unsupported schema_id")
    _validate_pilot(pack["pilot"])
    source_ids = _validate_sources(pack["selected_sources"])
    claim_sources, claim_ids = _validate_claims(pack["claims"], source_ids)
    _validate_source_claim_counts(pack["selected_sources"], claim_sources)
    _validate_relations(pack["relation_trials"], claim_ids)
    _validate_transition(pack["transition_review"], len(claim_ids))
    _validate_boundaries(pack["boundaries"], len(source_ids), len(claim_ids))


def _validate_pilot(value: Any) -> None:
    pilot = _strict(value, {"base_main_sha", "place_name", "accessed_on", "mode", "purpose"}, "pilot")
    expected = {
        "base_main_sha": BASE_MAIN_SHA,
        "place_name": "Cooma",
        "accessed_on": ACCESS_DATE,
        "mode": "ZERO_DOWNLOAD_OFFICIAL_HTML_STRUCTURED_CLAIMS",
        "purpose": "SOURCE_ASSERTION_ADMISSION_AND_RELATION_TRANSITION_GATE",
    }
    if pilot != expected:
        raise CoomaClaimError("Pilot identity or authorization boundary changed")


def _validate_sources(value: Any) -> set[str]:
    if not isinstance(value, list) or not 1 <= len(value) <= 3:
        raise CoomaClaimError("One to three selected sources are allowed")
    fields = {
        "source_id", "publisher", "canonical_url", "source_kind", "accessed_on",
        "page_format", "licence_state", "reuse_permission", "raw_page_body_retained",
        "verbatim_excerpt_retained", "file_downloaded", "dataset_downloaded", "claim_count",
    }
    seen: set[str] = set()
    for item in value:
        source = _strict(item, fields, "selected source")
        source_id = _text(source["source_id"], "source_id")
        if SOURCE_ID_RE.fullmatch(source_id) is None or source_id not in SOURCE_REGISTRY or source_id in seen:
            raise CoomaClaimError("Selected source must be a unique registered Cooma source")
        seen.add(source_id)
        registered = SOURCE_REGISTRY[source_id]
        for field in ("publisher", "canonical_url", "source_kind"):
            if source[field] != registered[field]:
                raise CoomaClaimError(f"Selected source {field} does not match the admitted registry")
        if source["accessed_on"] != ACCESS_DATE or source["page_format"] != "HTML":
            raise CoomaClaimError("Only official HTML inspected on the pilot date is allowed")
        if source["licence_state"] != "NOT_ASSESSED_REFERENCE_ONLY" or source["reuse_permission"] != "NOT_CLAIMED":
            raise CoomaClaimError("Content reuse permission cannot be claimed")
        if any(source[field] is not False for field in (
            "raw_page_body_retained", "verbatim_excerpt_retained", "file_downloaded", "dataset_downloaded"
        )):
            raise CoomaClaimError("Raw content, excerpts, files and datasets are blocked")
        if not isinstance(source["claim_count"], int) or isinstance(source["claim_count"], bool) or source["claim_count"] < 1:
            raise CoomaClaimError("Each selected source must support at least one claim")
    return seen


def _validate_claims(value: Any, source_ids: set[str]) -> tuple[dict[str, int], set[str]]:
    if not isinstance(value, list) or not 1 <= len(value) <= 5:
        raise CoomaClaimError("One to five structured claims are allowed")
    fields = {
        "claim_id", "source_id", "claim_type", "claim_form", "controlled_paraphrase",
        "verbatim_excerpt", "locator_type", "locator_label", "subject", "predicate",
        "object_text", "geographic_relevance", "time_scope", "version_state",
        "licence_state", "admission_state", "evidence_relation_eligible",
        "uncertainty_flags", "prohibited_inferences", "human_review_state",
    }
    counts = {source_id: 0 for source_id in source_ids}
    claim_ids: set[str] = set()
    for item in value:
        claim = _strict(item, fields, "claim")
        claim_id = _text(claim["claim_id"], "claim_id")
        if CLAIM_ID_RE.fullmatch(claim_id) is None or claim_id in claim_ids:
            raise CoomaClaimError("Claim IDs must be unique COOMA-CLAIM-NNN identifiers")
        claim_ids.add(claim_id)
        source_id = claim["source_id"]
        if source_id not in source_ids:
            raise CoomaClaimError("Claim must bind to a selected registered source")
        counts[source_id] += 1
        claim_type = claim["claim_type"]
        if claim_type not in CLAIM_TYPES or claim["geographic_relevance"] not in GEOGRAPHIES:
            raise CoomaClaimError("Unknown claim type or geography")
        if CLAIM_TYPE_TO_SOURCE[claim_type] != source_id:
            raise CoomaClaimError("Claim type must remain bound to its inspected official source")
        if CLAIM_TYPE_TO_GEOGRAPHY[claim_type] != claim["geographic_relevance"]:
            raise CoomaClaimError("Claim type and geographic scale must remain aligned")
        if claim["claim_form"] != "CONTROLLED_PARAPHRASE" or claim["verbatim_excerpt"] is not None:
            raise CoomaClaimError("Only controlled paraphrases without excerpts are allowed")
        for field in ("controlled_paraphrase", "locator_label", "subject", "predicate", "object_text", "version_state"):
            _text(claim[field], field)
        if claim["locator_type"] != "HTML_HEADING_AND_FIELD" or claim["time_scope"] != "PAGE_STATE_AT_ACCESS":
            raise CoomaClaimError("Claims require bounded HTML locators and point-in-time scope")
        expected = {
            "licence_state": "NOT_ASSESSED_REFERENCE_ONLY",
            "admission_state": "SOURCE_ASSERTION_REFERENCE_ONLY",
            "evidence_relation_eligible": False,
            "human_review_state": "UNASSIGNED_NOT_APPROVED",
        }
        for field, expected_value in expected.items():
            if claim[field] != expected_value:
                raise CoomaClaimError(f"Claim {field} exceeds the reference-only boundary")
        _strings(claim["uncertainty_flags"], "uncertainty_flags", non_empty=True)
        _strings(claim["prohibited_inferences"], "prohibited_inferences", non_empty=True)
    return counts, claim_ids


def _validate_source_claim_counts(sources: list[dict[str, Any]], counts: dict[str, int]) -> None:
    for source in sources:
        if source["claim_count"] != counts[source["source_id"]]:
            raise CoomaClaimError("Selected-source claim_count must match bound claims")


def _validate_relations(value: Any, claim_ids: set[str]) -> None:
    if not isinstance(value, list) or len(value) != 2:
        raise CoomaClaimError("Exactly two bounded relation trials are required")
    fields = {
        "relation_trial_id", "claim_ids", "proposed_relation", "gate_checks",
        "outcome", "evidence_relation_promoted", "mechanism_candidate_activated",
        "reason", "human_review_required",
    }
    seen: set[str] = set()
    for item in value:
        relation = _strict(item, fields, "relation trial")
        relation_id = _text(relation["relation_trial_id"], "relation_trial_id")
        if RELATION_ID_RE.fullmatch(relation_id) is None or relation_id in seen:
            raise CoomaClaimError("Relation trial IDs must be unique")
        seen.add(relation_id)
        referenced = set(_strings(relation["claim_ids"], "relation claim_ids", non_empty=True))
        if len(referenced) < 2 or not referenced <= claim_ids:
            raise CoomaClaimError("Relation trials require at least two admitted claim references")
        _text(relation["proposed_relation"], "proposed_relation")
        checks = _strict(relation["gate_checks"], GATE_FIELDS, "gate_checks")
        if checks["source_identity"] != "PASS_METADATA_BOUND":
            raise CoomaClaimError("Relation source identities must be metadata-bound")
        for field in GATE_FIELDS - {"source_identity"}:
            if not _text(checks[field], f"gate_checks.{field}").startswith("BLOCKED_"):
                raise CoomaClaimError("Unreviewed relation gates must remain explicitly blocked")
        if relation["outcome"] not in RELATION_OUTCOMES:
            raise CoomaClaimError("Unknown relation rejection outcome")
        if relation["evidence_relation_promoted"] is not False or relation["mechanism_candidate_activated"] is not False:
            raise CoomaClaimError("Evidence promotion and Task1701 activation are blocked")
        _text(relation["reason"], "relation reason")
        if relation["human_review_required"] is not True:
            raise CoomaClaimError("Human review remains required")


def _validate_transition(value: Any, claim_count: int) -> None:
    fields = {
        "task1500_1700_state", "source_assertions_admitted", "evidence_relations_promoted",
        "carried_task1701_candidate_ids", "candidate_state", "task1701_execution_justified",
        "recommendation", "next_gate",
    }
    transition = _strict(value, fields, "transition_review")
    expected = {
        "task1500_1700_state": "CLOSED_BOUNDED_PROTOTYPE_NO_EVIDENCE_RELATION_PROMOTED",
        "source_assertions_admitted": claim_count,
        "evidence_relations_promoted": 0,
        "candidate_state": "SYNTHETIC_HYPOTHESES_ONLY_NOT_ACTIVATED",
        "task1701_execution_justified": False,
        "recommendation": "DO_NOT_START_TASK1701_FROM_THIS_PILOT",
        "next_gate": "SEPARATE_FOUNDER_AUTHORIZATION_REQUIRED_FOR_TASK1701_PLUS",
    }
    for field, expected_value in expected.items():
        if transition[field] != expected_value:
            raise CoomaClaimError("Task1700 transition boundary changed")
    if set(_strings(transition["carried_task1701_candidate_ids"], "candidate ids")) != {
        "TASK1701-CANDIDATE-001", "TASK1701-CANDIDATE-002", "TASK1701-CANDIDATE-003"
    }:
        raise CoomaClaimError("The three synthetic candidates must remain inactive and traceable")


def _validate_boundaries(value: Any, source_count: int, claim_count: int) -> None:
    fields = {
        "network_used", "public_html_accessed", "selected_source_count", "structured_claim_count",
        "raw_page_body_retained", "verbatim_excerpt_retained", "pdf_or_document_downloaded",
        "dataset_downloaded", "real_observations_acquired", "cloud_service_used",
        "external_contact_made", "model_executed", "monitoring_active",
        "private_worksite_data_included", "customer_or_person_data_included",
        "local_environmental_conclusion_formed", "planning_or_legal_conclusion_formed",
        "work_or_compliance_conclusion_formed", "scientific_causal_conclusion_formed",
        "project_performance_conclusion_formed", "cost_aud", "human_review_required",
    }
    boundaries = _strict(value, fields, "boundaries")
    if boundaries["network_used"] is not True or boundaries["public_html_accessed"] is not True:
        raise CoomaClaimError("Authorized public HTML access must be recorded truthfully")
    if boundaries["selected_source_count"] != source_count or source_count > 3:
        raise CoomaClaimError("Selected-source count exceeds or misstates the authorization")
    if boundaries["structured_claim_count"] != claim_count or claim_count > 5:
        raise CoomaClaimError("Structured-claim count exceeds or misstates the authorization")
    false_fields = fields - {
        "network_used", "public_html_accessed", "selected_source_count", "structured_claim_count",
        "cost_aud", "human_review_required",
    }
    if any(boundaries[field] is not False for field in false_fields):
        raise CoomaClaimError("Downloads, observations, private data, execution and conclusions remain blocked")
    if boundaries["cost_aud"] != 0 or isinstance(boundaries["cost_aud"], bool):
        raise CoomaClaimError("cost_aud must remain zero")
    if boundaries["human_review_required"] is not True:
        raise CoomaClaimError("human_review_required must remain true")


def build_cooma_claim_preview(pack: dict[str, Any]) -> dict[str, Any]:
    """Build a deterministic non-conclusive Task1700 transition preview."""
    validate_cooma_claim_pack(pack)
    return {
        "schema_id": SCHEMA_ID,
        "place_name": "Cooma",
        "selected_source_count": len(pack["selected_sources"]),
        "structured_claim_count": len(pack["claims"]),
        "source_assertions_admitted_reference_only": len(pack["claims"]),
        "relation_trials": len(pack["relation_trials"]),
        "evidence_relations_promoted": 0,
        "raw_page_bodies_retained": 0,
        "verbatim_excerpts_retained": 0,
        "documents_or_datasets_downloaded": 0,
        "real_observations_acquired": 0,
        "local_or_scientific_conclusion": "NONE",
        "task1500_1700_state": pack["transition_review"]["task1500_1700_state"],
        "task1701_execution": "NOT_AUTHORIZED_NOT_JUSTIFIED_BY_THIS_PILOT",
        "next_gate": pack["transition_review"]["next_gate"],
    }
