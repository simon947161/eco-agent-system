"""Validate the Task1681–1690 Cooma zero-download source metadata pilot.

This module has no HTTP client or download path. It validates a committed record
of official public HTML page identities inspected manually on 2026-07-17.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any
from urllib.parse import urlparse

SCHEMA_ID = "climateos.cooma_official_source_metadata.v0.1"
BASE_MAIN_SHA = "708aa9f5231e52aea85f4d280214070618ef1c52"
ACCESS_DATE = "2026-07-17"
FIXTURE_ROOT = Path(__file__).resolve().parents[1] / "input"

SOURCE_TIERS = {
    "STATUTORY_PRIMARY",
    "STATE_GOVERNMENT_PRIMARY",
    "COUNCIL_PRIMARY",
    "PROJECT_PROPONENT_PRIMARY",
    "SCIENTIFIC_AGENCY_PRIMARY",
    "OFFICIAL_NEWS_DISCOVERY",
}
ALLOWED_DOMAINS = {
    "snowymonaro.nsw.gov.au",
    "legislation.nsw.gov.au",
    "planning.nsw.gov.au",
    "bom.gov.au",
    "snowyhydro.com.au",
    "dcceew.gov.au",
}
SOURCE_KINDS = {
    "PLANNING_CONTROL_LANDING",
    "STATUTORY_INSTRUMENT",
    "REGIONAL_PLAN_LANDING",
    "REGIONAL_PLAN_DELIVERY",
    "COUNCIL_SERVICE_LANDING",
    "COUNCIL_WATER_SOURCE_LANDING",
    "STATION_METADATA",
    "PROJECT_PROPONENT_LANDING",
    "FEDERAL_CATCHMENT_CONTEXT",
    "OFFICIAL_NEWS_ITEM",
}
RETAINED_FIELDS = {
    "TITLE",
    "PUBLISHER",
    "CANONICAL_URL",
    "VISIBLE_DATE_OR_VERSION",
    "DECLARED_GEOGRAPHY",
    "ACCESS_DATE",
    "ADMISSION_STATE",
}
GEOGRAPHIC_RELEVANCE = {
    "DIRECT_COOMA",
    "FORMER_COOMA_MONARO",
    "SNOWY_MONARO_LGA",
    "SOUTH_EAST_TABLELANDS_REGION",
    "MURRUMBIDGEE_VALLEY",
    "SNOWY_SCHEME_PROJECT",
}


class CoomaSourceMetadataError(ValueError):
    """Raised when metadata crosses the bounded public-reference contract."""


def _strict(value: Any, fields: set[str], label: str) -> dict[str, Any]:
    if not isinstance(value, dict):
        raise CoomaSourceMetadataError(f"{label} must be an object")
    missing = fields - set(value)
    unknown = set(value) - fields
    if missing or unknown:
        raise CoomaSourceMetadataError(
            f"{label} fields invalid; missing={sorted(missing)}, unknown={sorted(unknown)}"
        )
    return value


def _text(value: Any, label: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise CoomaSourceMetadataError(f"{label} must be a non-empty string")
    return value


def _strings(value: Any, label: str, *, non_empty: bool = False) -> list[str]:
    if not isinstance(value, list) or (non_empty and not value):
        raise CoomaSourceMetadataError(f"{label} must be a list")
    result = [_text(item, label) for item in value]
    if len(result) != len(set(result)):
        raise CoomaSourceMetadataError(f"{label} must contain unique values")
    return result


def load_cooma_source_metadata(path: str | Path) -> dict[str, Any]:
    """Load a repository-local metadata record; URLs are never fetched here."""
    if isinstance(path, str) and "://" in path:
        raise CoomaSourceMetadataError("Runtime URL loading is blocked")
    fixture = Path(path).resolve()
    try:
        fixture.relative_to(FIXTURE_ROOT.resolve())
    except ValueError as exc:
        raise CoomaSourceMetadataError("Metadata fixtures must stay under cczps_lite/input") from exc
    with fixture.open("r", encoding="utf-8") as stream:
        pack = json.load(stream)
    validate_cooma_source_metadata(pack)
    return pack


def validate_cooma_source_metadata(value: Any) -> None:
    pack = _strict(
        value,
        {"schema_id", "pilot", "source_tiers", "records", "deferred_candidates", "governance", "boundaries"},
        "root",
    )
    if pack["schema_id"] != SCHEMA_ID:
        raise CoomaSourceMetadataError("Unsupported schema_id")
    _validate_pilot(pack["pilot"])
    if set(_strings(pack["source_tiers"], "source_tiers", non_empty=True)) != SOURCE_TIERS:
        raise CoomaSourceMetadataError("The complete source-tier registry is required")
    _validate_records(pack["records"])
    _validate_deferred(pack["deferred_candidates"])
    _validate_governance(pack["governance"])
    _validate_boundaries(pack["boundaries"])


def _validate_pilot(value: Any) -> None:
    pilot = _strict(value, {"base_main_sha", "place_name", "accessed_on", "mode", "purpose"}, "pilot")
    expected = {
        "base_main_sha": BASE_MAIN_SHA,
        "place_name": "Cooma",
        "accessed_on": ACCESS_DATE,
        "mode": "PUBLIC_OFFICIAL_HTML_METADATA_ONLY",
        "purpose": "SOURCE_IDENTITY_VERSION_SCOPE_AND_REUSE_BOUNDARY",
    }
    if pilot != expected:
        raise CoomaSourceMetadataError("Pilot identity or authorization boundary changed")


def _validate_records(value: Any) -> None:
    if not isinstance(value, list) or not value:
        raise CoomaSourceMetadataError("records must be a non-empty list")
    fields = {
        "source_id", "title", "publisher", "tier", "source_kind", "canonical_url",
        "domain", "accessed_on", "page_format", "identity_status", "visible_date",
        "version_state", "geography_scope", "geographic_relevance",
        "retained_metadata_fields", "licence_state", "reuse_permission",
        "raw_content_retained", "file_downloaded", "dataset_downloaded",
        "admission_state", "claim_boundary", "does_not_prove", "human_review_required",
    }
    source_ids: set[str] = set()
    urls: set[str] = set()
    news_count = 0
    for item in value:
        record = _strict(item, fields, "source record")
        source_id = _text(record["source_id"], "source_id")
        if source_id in source_ids:
            raise CoomaSourceMetadataError(f"Duplicate source_id: {source_id}")
        source_ids.add(source_id)
        _text(record["title"], "title")
        _text(record["publisher"], "publisher")
        if record["tier"] not in SOURCE_TIERS or record["source_kind"] not in SOURCE_KINDS:
            raise CoomaSourceMetadataError("Unknown source tier or kind")
        url = _text(record["canonical_url"], "canonical_url")
        parsed = urlparse(url)
        if parsed.scheme != "https" or parsed.username or parsed.password or parsed.query or parsed.fragment:
            raise CoomaSourceMetadataError("Canonical URL must be clean public HTTPS metadata")
        domain = parsed.netloc.lower().removeprefix("www.")
        if domain not in ALLOWED_DOMAINS or record["domain"] != domain:
            raise CoomaSourceMetadataError("Canonical URL must use an approved official domain")
        if url in urls:
            raise CoomaSourceMetadataError("Canonical URLs must be unique")
        urls.add(url)
        if record["accessed_on"] != ACCESS_DATE or record["page_format"] != "HTML":
            raise CoomaSourceMetadataError("Only HTML metadata accessed on the pilot date is authorized")
        if record["identity_status"] != "VERIFIED_PUBLIC_PAGE":
            raise CoomaSourceMetadataError("Only verified public page identities are recorded")
        if record["visible_date"] is not None:
            _text(record["visible_date"], "visible_date")
        _text(record["version_state"], "version_state")
        _text(record["geography_scope"], "geography_scope")
        if record["geographic_relevance"] not in GEOGRAPHIC_RELEVANCE:
            raise CoomaSourceMetadataError("Unknown geographic relevance")
        if set(_strings(record["retained_metadata_fields"], "retained_metadata_fields", non_empty=True)) != RETAINED_FIELDS:
            raise CoomaSourceMetadataError("Only the fixed metadata field set may be retained")
        if record["licence_state"] != "NOT_ASSESSED_REFERENCE_ONLY" or record["reuse_permission"] != "NOT_CLAIMED":
            raise CoomaSourceMetadataError("The pilot cannot claim content reuse permission")
        if any(record[field] is not False for field in ("raw_content_retained", "file_downloaded", "dataset_downloaded")):
            raise CoomaSourceMetadataError("Raw content, file and dataset retention are blocked")
        _text(record["claim_boundary"], "claim_boundary")
        _strings(record["does_not_prove"], "does_not_prove", non_empty=True)
        if record["human_review_required"] is not True:
            raise CoomaSourceMetadataError("Human review remains required")
        is_news = record["source_kind"] == "OFFICIAL_NEWS_ITEM" or record["tier"] == "OFFICIAL_NEWS_DISCOVERY"
        if is_news:
            news_count += 1
            if record["source_kind"] != "OFFICIAL_NEWS_ITEM" or record["tier"] != "OFFICIAL_NEWS_DISCOVERY":
                raise CoomaSourceMetadataError("News kind and tier must remain aligned")
            if record["admission_state"] != "DISCOVERY_ONLY_QUARANTINED":
                raise CoomaSourceMetadataError("Official news remains discovery-only")
        elif record["admission_state"] != "METADATA_ADMITTED_REFERENCE_ONLY":
            raise CoomaSourceMetadataError("Primary pages admit metadata for reference only")
    if news_count != 1:
        raise CoomaSourceMetadataError("Exactly one official-news quarantine example is required")


def _validate_deferred(value: Any) -> None:
    if not isinstance(value, list) or len(value) != 2:
        raise CoomaSourceMetadataError("Exactly two deferred candidate classes are required")
    fields = {"candidate_id", "candidate_class", "state", "reason"}
    expected = {
        "CSIRO_COOMA_SPECIFIC_SOURCE": "NOT_IDENTIFIED_IN_BOUNDED_OFFICIAL_SEARCH",
        "INTERNAL_COUNCIL_DATABASE": "OUT_OF_SCOPE_NOT_ACCESSED",
    }
    seen: set[str] = set()
    for item in value:
        candidate = _strict(item, fields, "deferred candidate")
        candidate_class = candidate["candidate_class"]
        if candidate_class in seen or expected.get(candidate_class) != candidate["state"]:
            raise CoomaSourceMetadataError("Deferred candidate class or state changed")
        seen.add(candidate_class)
        _text(candidate["candidate_id"], "candidate_id")
        _text(candidate["reason"], "reason")
    if seen != set(expected):
        raise CoomaSourceMetadataError("The complete deferred boundary is required")


def _validate_governance(value: Any) -> None:
    fields = {
        "website_completeness_status", "conflict_policy", "news_policy", "document_policy",
        "evidence_promotion", "local_environmental_conclusion", "planning_conclusion",
        "legal_conclusion", "operational_or_compliance_conclusion",
    }
    governance = _strict(value, fields, "governance")
    expected = {
        "website_completeness_status": "NOT_ASSUMED_COMPLETE",
        "conflict_policy": "RECORD_WITHOUT_RESOLUTION",
        "news_policy": "DISCOVERY_ONLY_REQUIRES_PRIMARY_CORROBORATION",
        "document_policy": "HTML_METADATA_ONLY_NO_PDF_OR_DATASET_DOWNLOAD",
        "evidence_promotion": "BLOCKED_PENDING_SEPARATE_AUTHORIZATION",
        "local_environmental_conclusion": "NONE",
        "planning_conclusion": "NONE",
        "legal_conclusion": "NONE",
        "operational_or_compliance_conclusion": "NONE",
    }
    if governance != expected:
        raise CoomaSourceMetadataError("Governance or conclusion boundary changed")


def _validate_boundaries(value: Any) -> None:
    fields = {
        "network_used", "public_pages_accessed", "real_page_metadata_retained",
        "raw_page_content_retained", "pdf_or_document_downloaded", "dataset_downloaded",
        "cloud_service_used", "external_contact_made", "monitoring_active", "model_executed",
        "private_worksite_data_included", "customer_or_person_data_included",
        "local_conclusion_formed", "cost_aud", "human_review_required",
    }
    boundaries = _strict(value, fields, "boundaries")
    for field in ("network_used", "public_pages_accessed", "real_page_metadata_retained"):
        if boundaries[field] is not True:
            raise CoomaSourceMetadataError(f"{field} must truthfully remain true")
    false_fields = fields - {
        "network_used", "public_pages_accessed", "real_page_metadata_retained",
        "cost_aud", "human_review_required",
    }
    if any(boundaries[field] is not False for field in false_fields):
        raise CoomaSourceMetadataError("Downloads, private data, compute, contact and conclusions remain blocked")
    if boundaries["cost_aud"] != 0 or isinstance(boundaries["cost_aud"], bool):
        raise CoomaSourceMetadataError("cost_aud must remain zero")
    if boundaries["human_review_required"] is not True:
        raise CoomaSourceMetadataError("human_review_required must remain true")


def build_cooma_source_metadata_preview(pack: dict[str, Any]) -> dict[str, Any]:
    """Build a deterministic, non-evidentiary source identity summary."""
    validate_cooma_source_metadata(pack)
    counts: dict[str, int] = {}
    for record in pack["records"]:
        counts[record["tier"]] = counts.get(record["tier"], 0) + 1
    return {
        "schema_id": SCHEMA_ID,
        "place_name": "Cooma",
        "accessed_on": ACCESS_DATE,
        "source_record_count": len(pack["records"]),
        "records_by_tier": dict(sorted(counts.items())),
        "metadata_admitted_reference_only": sum(
            record["admission_state"] == "METADATA_ADMITTED_REFERENCE_ONLY"
            for record in pack["records"]
        ),
        "news_discovery_quarantined": sum(
            record["admission_state"] == "DISCOVERY_ONLY_QUARANTINED"
            for record in pack["records"]
        ),
        "raw_documents_downloaded": 0,
        "datasets_downloaded": 0,
        "evidence_relations_promoted": 0,
        "website_completeness": "NOT_ASSUMED_COMPLETE",
        "local_environmental_conclusion": "NONE",
        "planning_or_legal_conclusion": "NONE",
        "operational_or_compliance_conclusion": "NONE",
        "next_gate": "FOUNDER_DECISION_BEFORE_TASK1691_OR_ANY_CONTENT_ACQUISITION",
    }
