"""Offline public-data slice. Trusted local caller; NOT production authentication.

No generated reasoning, networking, arbitrary files, or scientific model calls.
Frozen raw/receipt hashes are repository trust roots, not provider signatures.
"""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

from cczps_lite.integration import dynamic_quantification as dq

VERSION = "client-ai-public/1"
QUESTION = "请核查 Central Park 2025年5月1日至3日公开气温与风速的覆盖、坐标和描述统计。"
RAW_SHA = "0d2d7217aa912df6418c69117b6f1b2bfde6f888ff3a8cf152830f9b630f6bbb"
RECEIPT_SHA = "56198fb881fb1f133622030688d4c766fa647bb900bd5a2573e50cb448c4aa43"
ROOT = Path(__file__).resolve().parents[2]
DATA = "docs/tasks/climateos_dynamic_quant_001/evidence/"
FILES = {DATA + "noaa-daily.json": RAW_SHA, DATA + "noaa-receipt.json": RECEIPT_SHA}
KEYS = {"schema_version", "question", "source_id", "crs", "coordinates", "start_date",
        "end_date", "time_basis", "variables", "permission", "model_id", "tenant_id",
        "topic", "basis", "raw_path", "receipt_path"}


def admitted_file(relative):
    """Exact registered file only; reject traversal, links/junctions, and tampering."""
    dq._require(isinstance(relative, str) and relative in FILES, "FILE_NOT_REGISTERED")
    path = ROOT / relative
    dq._require(path.resolve() == path.absolute(), "LINK_OR_PATH_ESCAPE")
    dq._require(path.is_file() and path.stat().st_size <= 100000, "INVALID_FILE")
    raw = path.read_bytes()
    # Git checkout may convert LF to CRLF in this repository-authored receipt.
    # Only that text receipt is LF-normalized; provider observation bytes never are.
    if relative == DATA + "noaa-receipt.json":
        raw = raw.replace(b"\r\n", b"\n")
    dq._require(hashlib.sha256(raw).hexdigest() == FILES[relative], "PINNED_HASH_MISMATCH")
    return raw


def execute(request, *, principal="public-demo-reader"):
    """Principal is trusted local harness input, never an authenticated web identity."""
    trace = ["closed_question_router"]
    try:
        dq._require(isinstance(request, dict) and set(request) == KEYS, "REQUEST_SCHEMA")
        dq._require(request["question"] == QUESTION, "UNSUPPORTED_OR_UNSAFE_QUESTION")
        trace.append("local_policy_simulation")
        dq._require(principal == "public-demo-reader" and request["tenant_id"] == "public-demo", "TENANT_OR_ROLE_DENIED")
        dq._require(request["topic"] == "meteorology" and request["basis"] == "station_daily", "PHASE_OR_BASIS_NOT_ADMITTED")
        dq._require(request["start_date"] == "2025-05-01" and request["end_date"] == "2025-05-03", "QUESTION_TIME_MISMATCH")
        dq._require(request["model_id"] == dq.MODEL, "MODEL_NOT_AUTHORIZED")
        dq._require(request["raw_path"] == DATA + "noaa-daily.json" and request["receipt_path"] == DATA + "noaa-receipt.json", "FILE_NOT_REGISTERED")
        trace.append("pinned_public_source_and_licence")
        raw = admitted_file(request["raw_path"])
        receipt = json.loads(admitted_file(request["receipt_path"]))
        dq._require(receipt.get("source_url") and receipt.get("rights_source") and receipt.get("rights_review") == "PUBLIC_RESEARCH_WITH_ATTRIBUTION", "SOURCE_OR_LICENCE_MISSING")
        output = dq.run_agent(request, raw, receipt)
        dq._require(output["status"] != "REFUSED", output.get("reason", "CORE_REFUSAL"))
        trace += output["trace"]
        spatial = {"type": "FeatureCollection", "bbox": dq.POINT + dq.POINT,
                   "features": [{"type": "Feature", "id": dq.SOURCE,
                                 "geometry": {"type": "Point", "coordinates": dq.POINT.copy()},
                                 "properties": {"source_sha256": RAW_SHA, "coordinate_accuracy_m": "UNKNOWN",
                                                "crs_basis": "inherited EPSG:4326 contract; datum not independently surveyed",
                                                "observation_count": len(output["observations"]["records"]),
                                                "spatial_scope": "single station; no parcel or receptor proximity"}}]}
        return {"status": "LOCAL_VERIFIED_PUBLIC_DESCRIPTIVE_SLICE", "schema_version": VERSION,
                "route": "PUBLIC_OPEN_DATA_ADAPTER", "trace": trace,
                "input_hashes": FILES.copy(), "source_receipt": receipt,
                "hash_basis": {"observations": "exact raw bytes", "receipt": "repository text with CRLF normalized to LF"},
                "scientific_evidence_grade": "REAL_DATA_STRUCTURAL_QC",
                "scientific_admission": "UNCHANGED_PENDING", "reviewer": "PENDING_CHATGPT",
                "validation_holds": ["provider day timezone UNKNOWN", "coordinate accuracy UNKNOWN",
                                     "no field or customer ground truth", "no production identity security"],
                "rejected_rows": [], "observation_result": output, "spatial_result": spatial}
    except (dq.Refusal, OSError, ValueError, TypeError) as exc:
        reason = str(exc) if isinstance(exc, dq.Refusal) else "INPUT_READ_OR_FORMAT_ERROR"
        return {"status": "REFUSED", "reason": reason, "schema_version": VERSION,
                "trace": trace, "scientific_admission": "UNCHANGED_PENDING"}
