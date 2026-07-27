"""Bounded official real-data intake for the first Cooma evidence pilot.

The pilot retrieves two exact Bureau of Meteorology products only after an
explicit manual approval flag. Raw responses and the full receipt stay under
gitignored ``runtime_data``. A public receipt exposes provenance and validation
metadata, but no copied observation rows or page body.
"""

from __future__ import annotations

import csv
import hashlib
import html
import json
import re
import urllib.request
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Callable
from urllib.parse import urlparse

SCHEMA_ID = "climateos.cooma_official_real_data_pilot.v0.1"
PUBLIC_RECEIPT_SCHEMA_ID = "climateos.cooma_official_real_data_public_receipt.v0.1"
PILOT_ID = "COOMA-OFFICIAL-REAL-DATA-PILOT-2026-07"
MAX_RESPONSE_BYTES = 2 * 1024 * 1024
ALLOWED_HOST = "www.bom.gov.au"
SOURCES = (
    {
        "source_id": "COOMA-BOM-DWO-2026-07",
        "publisher": "Australian Bureau of Meteorology",
        "title": "Daily Weather Observations for Cooma, July 2026",
        "url": "https://www.bom.gov.au/climate/dwo/202607/text/IDCJDW2033.202607.csv",
        "media_type": "text/csv",
        "local_filename": "IDCJDW2033.202607.csv",
        "evidence_class": "OFFICIAL_OBSERVATION",
    },
    {
        "source_id": "BOM-ENSO-MONITORING-2026-07-14",
        "publisher": "Australian Bureau of Meteorology",
        "title": "Southern Hemisphere monitoring history, 14 July 2026",
        "url": "https://www.bom.gov.au/climate/enso/wrap-up/archive/20260714.archive.shtml",
        "media_type": "text/html",
        "local_filename": "20260714.archive.shtml",
        "evidence_class": "OFFICIAL_OUTLOOK",
    },
)


class CoomaRealDataPilotError(ValueError):
    """Raised when acquisition, parsing, integrity or scope controls fail."""


def _timestamp() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def _digest(body: bytes) -> str:
    return "sha256:" + hashlib.sha256(body).hexdigest()


def _source(source_id: str) -> dict[str, str]:
    for item in SOURCES:
        if item["source_id"] == source_id:
            return item
    raise CoomaRealDataPilotError(f"Unknown source_id: {source_id}")


def _validate_source_contract(source: dict[str, str]) -> None:
    parsed = urlparse(source["url"])
    if (
        parsed.scheme != "https"
        or parsed.hostname != ALLOWED_HOST
        or parsed.username
        or parsed.password
        or parsed.query
        or parsed.fragment
    ):
        raise CoomaRealDataPilotError("Source is outside the exact HTTPS allowlist")
    if source["media_type"] not in {"text/csv", "text/html"}:
        raise CoomaRealDataPilotError("Unsupported source media type")


def _default_fetch(source: dict[str, str]) -> dict[str, Any]:
    request = urllib.request.Request(
        source["url"],
        headers={"User-Agent": "ClimateOS-Cooma-Official-Real-Data-Pilot/0.1"},
    )
    with urllib.request.urlopen(request, timeout=30) as response:  # nosec B310 - exact allowlist
        final_url = response.geturl()
        parsed = urlparse(final_url)
        if parsed.scheme != "https" or parsed.hostname != ALLOWED_HOST:
            raise CoomaRealDataPilotError("Official source redirected outside the allowlist")
        body = response.read(MAX_RESPONSE_BYTES + 1)
        if len(body) > MAX_RESPONSE_BYTES:
            raise CoomaRealDataPilotError("Official source exceeded the 2 MiB pilot ceiling")
        if int(response.status) != 200:
            raise CoomaRealDataPilotError(f"Official source returned HTTP {response.status}")
        return {
            "body": body,
            "http_status": int(response.status),
            "final_url": final_url,
            "content_type": response.headers.get("Content-Type", ""),
            "etag": response.headers.get("ETag"),
            "last_modified": response.headers.get("Last-Modified"),
        }


def _decode_csv(body: bytes) -> str:
    for encoding in ("utf-8-sig", "cp1252"):
        try:
            return body.decode(encoding)
        except UnicodeDecodeError:
            continue
    raise CoomaRealDataPilotError("Cooma CSV encoding is unsupported")


def parse_cooma_daily_weather(body: bytes) -> dict[str, Any]:
    """Parse source identity and coverage without publishing observation rows."""
    text = _decode_csv(body)
    rows = list(csv.reader(text.splitlines()))
    if len(rows) < 9 or "Daily Weather Observations for Cooma" not in rows[0][0]:
        raise CoomaRealDataPilotError("Unexpected Cooma daily-weather product identity")
    joined_header = "\n".join(",".join(row) for row in rows[:7])
    if "station 070278" not in joined_header or "station 070217" not in joined_header:
        raise CoomaRealDataPilotError("Expected Cooma station identities are missing")
    header_index = next(
        (index for index, row in enumerate(rows) if "Date" in row and "Rainfall (mm)" in row),
        None,
    )
    if header_index is None:
        raise CoomaRealDataPilotError("Daily-weather column header is missing")
    header = rows[header_index]
    date_index = header.index("Date")
    rainfall_index = header.index("Rainfall (mm)")
    data_rows = [
        row
        for row in rows[header_index + 1 :]
        if len(row) > max(date_index, rainfall_index) and re.fullmatch(r"2026-07-\d{1,2}", row[date_index])
    ]
    if not data_rows:
        raise CoomaRealDataPilotError("No July 2026 Cooma observation rows were found")
    dates = [row[date_index] for row in data_rows]
    rainfall_present = sum(bool(row[rainfall_index].strip()) for row in data_rows)
    return {
        "product_id": "IDCJDW2033.202607",
        "station_ids": ["070278", "070217"],
        "row_count": len(data_rows),
        "coverage_start": dates[0],
        "coverage_end": dates[-1],
        "column_count": len(header),
        "rainfall_observation_count": rainfall_present,
        "rainfall_missing_count": len(data_rows) - rainfall_present,
        "quantitative_values_publicly_retained": False,
    }


def parse_bom_enso_archive(body: bytes) -> dict[str, Any]:
    """Validate the dated official ENSO state and retain bounded source facts."""
    text = body.decode("utf-8", errors="replace")
    normalized = html.unescape(re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", text)))
    required = (
        "El Niño is underway",
        "week ending 12 July 2026",
        "+1.47",
        "+0.80",
        "–25.8",
    )
    missing = [item for item in required if item not in normalized]
    if missing:
        raise CoomaRealDataPilotError(f"Expected dated ENSO facts are missing: {missing}")
    return {
        "archive_date": "2026-07-14",
        "state": "EL_NINO_UNDERWAY",
        "nino34_week_ending": "2026-07-12",
        "relative_nino34_c": 1.47,
        "bom_el_nino_threshold_c": 0.80,
        "soi_30_day_to_2026_07_12": -25.8,
        "outlook_scope": "likely to persist until at least southern hemisphere summer",
        "local_cooma_impact_claim": None,
    }


def _public_source_receipt(record: dict[str, Any]) -> dict[str, Any]:
    return {
        "source_id": record["source_id"],
        "publisher": record["publisher"],
        "title": record["title"],
        "url": record["url"],
        "evidence_class": record["evidence_class"],
        "retrieved_at": record["retrieved_at"],
        "http_status": record["http_status"],
        "final_url": record["final_url"],
        "content_type": record["content_type"],
        "content_digest": record["content_digest"],
        "response_bytes": record["response_bytes"],
        "parsed_metadata": record["parsed_metadata"],
        "raw_content_retained_publicly": False,
        "raw_content_local_path": "REDACTED_LOCAL_GITIGNORED_PATH",
    }


def validate_public_receipt(receipt: dict[str, Any]) -> None:
    if receipt.get("schema_id") != PUBLIC_RECEIPT_SCHEMA_ID:
        raise CoomaRealDataPilotError("Unsupported public receipt schema")
    if receipt.get("pilot_id") != PILOT_ID or receipt.get("source_count") != len(SOURCES):
        raise CoomaRealDataPilotError("Public receipt pilot identity or source count changed")
    if receipt.get("environmental_conclusion") is not None:
        raise CoomaRealDataPilotError("The pilot cannot publish an environmental conclusion")
    for item in receipt.get("sources", []):
        if item.get("raw_content_retained_publicly") is not False:
            raise CoomaRealDataPilotError("Raw official content cannot enter the public receipt")
        if not str(item.get("content_digest", "")).startswith("sha256:"):
            raise CoomaRealDataPilotError("Every source requires a SHA-256 digest")
        if "body" in item or "observation_rows" in item:
            raise CoomaRealDataPilotError("Public receipt contains prohibited raw content")


def run_pilot(
    output_root: str | Path,
    *,
    human_approval: bool,
    fetcher: Callable[[dict[str, str]], dict[str, Any]] = _default_fetch,
    retrieved_at: str | None = None,
) -> tuple[dict[str, Any], dict[str, Any]]:
    """Retrieve, validate and locally retain the two fixed official sources."""
    if human_approval is not True:
        raise CoomaRealDataPilotError("Explicit human approval is required for real-data retrieval")
    root = Path(output_root)
    raw_root = root / "raw"
    raw_root.mkdir(parents=True, exist_ok=True)
    timestamp = retrieved_at or _timestamp()
    records: list[dict[str, Any]] = []
    for source in SOURCES:
        _validate_source_contract(source)
        result = fetcher(source)
        body = result.get("body")
        if not isinstance(body, bytes) or not body:
            raise CoomaRealDataPilotError("Official source returned no byte content")
        if len(body) > MAX_RESPONSE_BYTES:
            raise CoomaRealDataPilotError("Official source exceeded the 2 MiB pilot ceiling")
        final_url = str(result.get("final_url", ""))
        if urlparse(final_url).hostname != ALLOWED_HOST:
            raise CoomaRealDataPilotError("Retrieved source final URL is outside the allowlist")
        parsed = (
            parse_cooma_daily_weather(body)
            if source["media_type"] == "text/csv"
            else parse_bom_enso_archive(body)
        )
        local_path = raw_root / source["local_filename"]
        local_path.write_bytes(body)
        records.append(
            {
                **source,
                "retrieved_at": timestamp,
                "http_status": int(result.get("http_status", 0)),
                "final_url": final_url,
                "content_type": str(result.get("content_type", "")),
                "etag": result.get("etag"),
                "last_modified": result.get("last_modified"),
                "content_digest": _digest(body),
                "response_bytes": len(body),
                "local_raw_path": str(local_path),
                "parsed_metadata": parsed,
                "admission_state": "ADMITTED_FOR_BOUNDED_L1_SOURCE_FACTS",
                "maximum_conclusion_level": "L1",
            }
        )
    full_receipt = {
        "schema_id": SCHEMA_ID,
        "pilot_id": PILOT_ID,
        "retrieved_at": timestamp,
        "human_approval": True,
        "network_used": True,
        "cost_aud": 0,
        "source_count": len(records),
        "sources": records,
        "environmental_conclusion": None,
        "blocked_water_balance_terms": ["storage", "streamflow", "water_use", "ET", "wastewater_operations"],
    }
    public_receipt = {
        "schema_id": PUBLIC_RECEIPT_SCHEMA_ID,
        "pilot_id": PILOT_ID,
        "retrieved_at": timestamp,
        "network_used": True,
        "cost_aud": 0,
        "source_count": len(records),
        "sources": [_public_source_receipt(item) for item in records],
        "maximum_conclusion_level": "L1",
        "environmental_conclusion": None,
        "cooma_water_balance_status": "BLOCKED_MISSING_REQUIRED_TERMS",
        "missing_terms": ["storage", "streamflow", "water_use", "ET", "wastewater_operations"],
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
