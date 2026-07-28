"""Controlled L1 intake for BoM HRS gauge 410033 daily streamflow."""

from __future__ import annotations

import csv
import hashlib
import json
import urllib.request
from collections import Counter
from datetime import UTC, date, datetime
from pathlib import Path
from typing import Any, Callable
from urllib.parse import urlparse

SCHEMA_ID = "climateos.mittagang_410033_flow_full_receipt.v0.1"
PUBLIC_SCHEMA_ID = "climateos.mittagang_410033_flow_public_receipt.v0.1"
RUN_ID = "MITTAGANG-410033-OFFICIAL-FLOW-INTAKE-V0.1"
SOURCE_URL = (
    "https://www.bom.gov.au/water/hrs/content/data/410033/"
    "410033_daily_ts.csv"
)
ALLOWED_HOST = "www.bom.gov.au"
MAX_RESPONSE_BYTES = 2 * 1024 * 1024
KNOWN_QUALITY_CODES = {"A", "B", "C", "E", "G"}


class MittagangFlowIntakeError(ValueError):
    """Raised when retrieval, parsing, integrity or scope controls fail."""


def _timestamp() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def _digest(body: bytes) -> str:
    return "sha256:" + hashlib.sha256(body).hexdigest()


def _default_fetch() -> dict[str, Any]:
    request = urllib.request.Request(
        SOURCE_URL,
        headers={"User-Agent": "ClimateOS-Mittagang-410033-Flow-Intake/0.1"},
    )
    with urllib.request.urlopen(request, timeout=60) as response:  # nosec B310
        final_url = response.geturl()
        parsed = urlparse(final_url)
        if parsed.scheme != "https" or parsed.hostname != ALLOWED_HOST:
            raise MittagangFlowIntakeError("Official source redirected outside allowlist")
        body = response.read(MAX_RESPONSE_BYTES + 1)
        if len(body) > MAX_RESPONSE_BYTES:
            raise MittagangFlowIntakeError("Official source exceeded 2 MiB ceiling")
        if int(response.status) != 200:
            raise MittagangFlowIntakeError(
                f"Official source returned HTTP {response.status}"
            )
        return {
            "body": body,
            "http_status": int(response.status),
            "final_url": final_url,
            "content_type": response.headers.get("Content-Type", ""),
            "etag": response.headers.get("ETag"),
            "last_modified": response.headers.get("Last-Modified"),
        }


def _comment_value(rows: list[list[str]], label: str) -> str:
    for row in rows:
        if len(row) <= 1 or row[0] != "#":
            continue
        field = row[1].strip()
        if field == label:
            return ",".join(part.strip() for part in row[2:] if part.strip())
        if field.startswith(label):
            return field.removeprefix(label).strip()
    raise MittagangFlowIntakeError(f"Required source metadata is missing: {label}")


def parse_daily_flow(body: bytes) -> dict[str, Any]:
    """Validate source identity and report coverage without exposing observations."""
    try:
        text = body.decode("utf-8-sig")
    except UnicodeDecodeError as exc:
        raise MittagangFlowIntakeError("Official CSV is not UTF-8") from exc
    rows = list(csv.reader(text.splitlines()))
    joined_header = "\n".join(",".join(row) for row in rows[:30])
    required_identity = (
        "Australian Bureau of Meteorology",
        "Hydrologic Reference Stations",
        "Murrumbidgee River at Mittagang Crossing (410033)",
        "Daily streamflow (ML/day) and quality code",
        "WISKI (validated data only)",
    )
    missing_identity = [item for item in required_identity if item not in joined_header]
    if missing_identity:
        raise MittagangFlowIntakeError(
            f"Unexpected official product identity: {missing_identity}"
        )
    try:
        header_index = rows.index(["Date", "Flow (ML)", "Bureau QCode"])
    except ValueError as exc:
        raise MittagangFlowIntakeError("Expected data columns are missing") from exc

    dates: list[date] = []
    blank_flow_count = 0
    invalid_row_count = 0
    quality_counts: Counter[str] = Counter()
    unknown_quality_codes: set[str] = set()
    for row in rows[header_index + 1 :]:
        if len(row) != 3:
            invalid_row_count += 1
            continue
        try:
            observation_date = date.fromisoformat(row[0])
            if row[1].strip():
                float(row[1])
            else:
                blank_flow_count += 1
        except ValueError:
            invalid_row_count += 1
            continue
        dates.append(observation_date)
        quality_counts[row[2]] += 1
        if row[2] not in KNOWN_QUALITY_CODES:
            unknown_quality_codes.add(row[2])
    if not dates:
        raise MittagangFlowIntakeError("Official product contains no valid rows")

    date_counts = Counter(dates)
    duplicate_date_count = sum(count - 1 for count in date_counts.values() if count > 1)
    expected_days = (max(dates) - min(dates)).days + 1
    missing_calendar_date_count = expected_days - len(date_counts)
    if invalid_row_count or unknown_quality_codes:
        raise MittagangFlowIntakeError(
            "Official product contains invalid rows or unknown quality codes"
        )
    return {
        "publisher": "Australian Bureau of Meteorology",
        "product_family": "Hydrologic Reference Stations",
        "station_id": "410033",
        "station_name": "Murrumbidgee River at Mittagang Crossing",
        "dataset_version": _comment_value(rows[:header_index], "Dataset version:"),
        "data_extraction_date": _comment_value(
            rows[:header_index], "Data extraction date:"
        ),
        "source_system": "WISKI (validated data only)",
        "measurement": "daily streamflow",
        "canonical_unit": "ML/day",
        "source_value_column": "Flow (ML)",
        "row_count": len(dates),
        "coverage_start": min(dates).isoformat(),
        "coverage_end": max(dates).isoformat(),
        "expected_calendar_day_count": expected_days,
        "missing_calendar_date_count": missing_calendar_date_count,
        "blank_flow_value_count": blank_flow_count,
        "duplicate_date_count": duplicate_date_count,
        "invalid_row_count": invalid_row_count,
        "quality_code_counts": {
            code: quality_counts.get(code, 0)
            for code in sorted(KNOWN_QUALITY_CODES)
        },
        "unknown_quality_codes": sorted(unknown_quality_codes),
        "day_boundary_local_time": "09:00",
        "aggregation_window": "previous 24 hours",
        "timezone_text_from_source": "local time",
        "timezone_identifier": None,
        "timezone_resolution_state": "SOURCE_DOES_NOT_DECLARE_IANA_TIMEZONE",
        "gap_fill_method_declared": "daily rainfall-runoff model",
        "raw_observation_rows_published_in_receipt": False,
    }


def validate_public_receipt(receipt: dict[str, Any]) -> None:
    if receipt.get("schema_id") != PUBLIC_SCHEMA_ID:
        raise MittagangFlowIntakeError("Unsupported public receipt schema")
    if receipt.get("run_id") != RUN_ID:
        raise MittagangFlowIntakeError("Unexpected run identity")
    if receipt.get("maximum_conclusion_level") != "L1":
        raise MittagangFlowIntakeError("Maximum conclusion level must remain L1")
    if receipt.get("environmental_conclusion") is not None:
        raise MittagangFlowIntakeError("Environmental conclusions are prohibited")
    source = receipt.get("source", {})
    if source.get("url") != SOURCE_URL:
        raise MittagangFlowIntakeError("Public receipt source changed")
    if not str(source.get("content_digest", "")).startswith("sha256:"):
        raise MittagangFlowIntakeError("SHA-256 identity is required")
    if source.get("raw_content_retained_publicly") is not False:
        raise MittagangFlowIntakeError("Raw rows cannot enter the public receipt")
    if "body" in source or "observation_rows" in source:
        raise MittagangFlowIntakeError("Public receipt contains raw observations")


def run_intake(
    output_root: str | Path,
    *,
    human_approval: bool,
    fetcher: Callable[[], dict[str, Any]] = _default_fetch,
    retrieved_at: str | None = None,
) -> tuple[dict[str, Any], dict[str, Any]]:
    """Retrieve, validate and locally retain the fixed official flow product."""
    if human_approval is not True:
        raise MittagangFlowIntakeError(
            "Explicit human approval is required for official data retrieval"
        )
    parsed_url = urlparse(SOURCE_URL)
    if (
        parsed_url.scheme != "https"
        or parsed_url.hostname != ALLOWED_HOST
        or parsed_url.query
        or parsed_url.fragment
    ):
        raise MittagangFlowIntakeError("Source is outside the exact HTTPS allowlist")
    result = fetcher()
    body = result.get("body")
    if not isinstance(body, bytes) or not body:
        raise MittagangFlowIntakeError("Official source returned no byte content")
    if len(body) > MAX_RESPONSE_BYTES:
        raise MittagangFlowIntakeError("Official source exceeded 2 MiB ceiling")
    final_url = str(result.get("final_url", ""))
    if final_url != SOURCE_URL:
        raise MittagangFlowIntakeError("Official source final URL changed")

    root = Path(output_root)
    raw_root = root / "raw"
    raw_root.mkdir(parents=True, exist_ok=True)
    raw_path = raw_root / "410033_daily_ts.csv"
    raw_path.write_bytes(body)
    timestamp = retrieved_at or _timestamp()
    metadata = parse_daily_flow(body)
    source_record = {
        "publisher": "Australian Bureau of Meteorology",
        "title": "HRS daily streamflow — gauge 410033",
        "url": SOURCE_URL,
        "licence": "CC BY 4.0 unless otherwise noted on HRS",
        "retrieved_at": timestamp,
        "http_status": int(result.get("http_status", 0)),
        "final_url": final_url,
        "content_type": str(result.get("content_type", "")),
        "etag": result.get("etag"),
        "last_modified": result.get("last_modified"),
        "response_bytes": len(body),
        "content_digest": _digest(body),
        "parsed_metadata": metadata,
    }
    full_receipt = {
        "schema_id": SCHEMA_ID,
        "run_id": RUN_ID,
        "human_approval": True,
        "network_used": True,
        "cost_aud": 0,
        "source": {**source_record, "local_raw_path": str(raw_path)},
        "maximum_conclusion_level": "L1",
        "environmental_conclusion": None,
    }
    public_receipt = {
        "schema_id": PUBLIC_SCHEMA_ID,
        "run_id": RUN_ID,
        "network_used": True,
        "cost_aud": 0,
        "source": {
            **source_record,
            "raw_content_retained_publicly": False,
            "raw_content_local_path": "REDACTED_LOCAL_GITIGNORED_PATH",
        },
        "maximum_conclusion_level": "L1",
        "environmental_conclusion": None,
        "water_supply_sufficiency_status": "NOT_EVALUATED",
        "qgis_changed": False,
        "council_non_public_data_accessed": False,
    }
    validate_public_receipt(public_receipt)
    (root / "full_receipt.json").write_text(
        json.dumps(full_receipt, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    (root / "public_receipt.json").write_text(
        json.dumps(public_receipt, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    return full_receipt, public_receipt
