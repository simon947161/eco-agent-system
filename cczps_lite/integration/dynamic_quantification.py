"""Bounded, offline Environmental Evidence Agent v0.1; no LLM or network.

Only a pinned NOAA daily-observation receipt is admitted. The statistic is
descriptive arithmetic, not a scientifically validated predictive model.
"""
from __future__ import annotations

import hashlib
import json
import math
from datetime import date
from pathlib import Path
from statistics import mean

from cczps_lite.engine.meteorology_connector import parse_observation

VERSION = "0.1"
MODEL = "daily_descriptive_mean/1"
SOURCE = "NOAA_GHCND_USW00094728"
POINT = [-73.96925, 40.77898]  # longitude, latitude; EPSG:4326
TIME_BASIS = "PROVIDER_OBSERVING_DAY"
VARIABLES = {"daily_max_temperature": "degC", "daily_mean_wind_speed": "m/s"}
EVIDENCE_DIR = Path(__file__).resolve().parents[2] / "docs/tasks/climateos_dynamic_quant_001/evidence"


class Refusal(ValueError):
    """An evidence gate refused a request; never a zero environmental result."""


def _require(condition, reason):
    if not condition:
        raise Refusal(reason)


def _number(value):
    _require(not isinstance(value, bool), "INVALID_NUMBER")
    try:
        result = float(value)
    except (ValueError, TypeError):
        raise Refusal("MISSING_OR_INVALID_DATA") from None
    _require(math.isfinite(result) and result not in (-999, -9999), "MISSING_OR_INVALID_DATA")
    return result


def get_environmental_context(request):
    """Validate the narrow point/date/units envelope, without guessing defaults."""
    _require(isinstance(request, dict), "INVALID_REQUEST")
    _require(request.get("schema_version") == VERSION, "SCHEMA_VERSION")
    _require(isinstance(request.get("question"), str) and bool(request["question"].strip()), "QUESTION_REQUIRED")
    _require(request.get("source_id") == SOURCE, "DATA_NOT_READY_OR_SOURCE_NOT_ADMITTED")
    _require(request.get("crs") == "EPSG:4326" and request.get("coordinates") == POINT, "SPACE_MISMATCH")
    _require(request.get("time_basis") == TIME_BASIS, "TIME_BASIS_MISMATCH")
    _require(request.get("variables") == VARIABLES, "UNIT_OR_VARIABLE_MISMATCH")
    _require(request.get("permission") == "public_read_only", "PERMISSION_DENIED")
    try:
        start = date.fromisoformat(request["start_date"])
        end = date.fromisoformat(request["end_date"])
    except (KeyError, TypeError, ValueError):
        raise Refusal("INVALID_TIME") from None
    _require(0 <= (end - start).days < 31, "INVALID_TIME")
    return {"start": start, "end": end, "data_class": "station_daily_observation",
            "timezone": "UNKNOWN_PROVIDER_DAY", "crs": "EPSG:4326"}


def query_observations(request, context, raw, receipt):
    """Parse archived bytes with a trusted, version-controlled acquisition receipt.

    The receipt is a local trust root, not a provider signature. Replacing the
    receipt requires human review. Provider flags are retained and checked.
    """
    _require(isinstance(raw, bytes) and len(raw) <= 100000, "INVALID_RAW_BYTES")
    _require(receipt.get("source_id") == SOURCE and receipt.get("rights_review") == "PUBLIC_RESEARCH_WITH_ATTRIBUTION", "SOURCE_RIGHTS_NOT_ADMITTED")
    _require(hashlib.sha256(raw).hexdigest() == receipt.get("sha256"), "HASH_MISMATCH")
    _require(receipt.get("units") == "metric" and receipt.get("time_basis") == TIME_BASIS, "SOURCE_METADATA_MISMATCH")
    try:
        rows = json.loads(raw)
    except (ValueError, UnicodeError):
        raise Refusal("INVALID_PAYLOAD") from None
    _require(isinstance(rows, list) and 0 < len(rows) <= 31, "MISSING_DATA")
    parsed, seen = [], set()
    for row in rows:
        _require(isinstance(row, dict), "INVALID_PAYLOAD")
        try:
            day = date.fromisoformat(row["DATE"])
        except (KeyError, TypeError, ValueError):
            raise Refusal("INVALID_TIME") from None
        _require(day not in seen, "DUPLICATE_DAY")
        seen.add(day)
        _require(row.get("STATION") == "USW00094728", "STATION_MISMATCH")
        _require([_number(row.get("LONGITUDE")), _number(row.get("LATITUDE"))] == POINT, "SPACE_MISMATCH")
        flags = {}
        for field in ("TMAX", "AWND"):
            attributes = row.get(field + "_ATTRIBUTES")
            _require(isinstance(attributes, str), "QUALITY_FLAGS_MISSING")
            parts = attributes.split(",")
            _require(len(parts) in (3, 4) and parts[1].strip() == "", "QUALITY_FLAG_REJECTED")
            flags[field] = attributes
        tmax, wind = _number(row.get("TMAX")), _number(row.get("AWND"))
        _require(-100 <= tmax <= 70 and 0 <= wind <= 150, "RANGE_CHECK_FAILED")
        # Reuse existing connector for numeric field mapping, but never give its
        # generic temperature field a daily-mean interpretation or invent UTC.
        config = {"sources": {"noaa_daily": {"name": SOURCE, "field_map": {
            "temperature_c": "TMAX", "wind_speed_kmh": "AWND_KMH"}}}}
        reading = parse_observation("noaa_daily", "Central Park", {"TMAX": tmax, "AWND_KMH": wind * 3.6}, config)
        if context["start"] <= day <= context["end"]:
            parsed.append({"date": day.isoformat(), "daily_max_temperature": reading["temperature_c"],
                           "daily_mean_wind_speed": reading["wind_speed_kmh"] / 3.6,
                           "provider_flags": flags})
    expected = (context["end"] - context["start"]).days + 1
    _require(len(parsed) == expected, "INSUFFICIENT_TEMPORAL_COVERAGE")
    return {"records": sorted(parsed, key=lambda r: r["date"]), "missing_days": 0,
            "source_sha256": receipt["sha256"], "units": VARIABLES.copy(),
            "data_class": context["data_class"], "time_basis": TIME_BASIS}


def run_verified_model(request, observations):
    """Historical interface name: only an allowlisted descriptive method exists."""
    _require(request.get("model_id") == MODEL, "MODEL_NOT_AUTHORIZED")
    rows = observations["records"]
    _require(len(rows) >= 3, "INSUFFICIENT_EVIDENCE_MIN_3_DAYS")
    return {"method_id": MODEL, "validation_status": "SOFTWARE_TESTED_NOT_SCIENTIFIC_MODEL_VALIDATED",
            "count": len(rows), "means": {key: mean(row[key] for row in rows) for key in VARIABLES},
            "units": VARIABLES.copy(), "uncertainty": "Instrument/representativeness uncertainty not quantified; no predictive confidence interval."}


def compare_scenarios(*args, **kwargs):
    raise Refusal("SCENARIO_MODEL_NOT_ADMITTED")


def check_regulatory_context(*args, **kwargs):
    return {"status": "NOT_ASSESSED", "legal_effect": "NONE", "reason": "No jurisdiction-specific current legal evidence admitted to this run."}


def generate_evidence_report(request, observations, result, regulatory):
    return (f"# 环境证据报告\n\n地点：纽约 Central Park 公开站点；不是 NSW 代表站。\n\n"
            f"{request['start_date']} 至 {request['end_date']}，共 {result['count']} 个提供方观测日；"
            "日界时区尚未核实，未强行转成 UTC。\n\n"
            f"日最高气温的算术平均：{result['means']['daily_max_temperature']:.3f} °C；"
            f"日平均风速的算术平均：{result['means']['daily_mean_wind_speed']:.3f} m/s。"
            "前者不是期间平均气温；后者没有方向，不能推算输送。\n\n"
            f"原始字节 SHA-256：{observations['source_sha256']}。"
            "通过完整覆盖、有限数值、站点坐标及提供方质量标志检查；空质量标志不保证没有误差。\n\n"
            "这是三天描述统计，不能证明趋势、气候变化、甲烷源强、生态收益或法律责任。"
            f"法规状态：{regulatory['status']}。未量化仪器和空间代表性误差。\n")


def run_agent(request, raw=None, receipt=None):
    """Deterministic bounded tool controller; failures contain no result values."""
    trace = []
    try:
        trace.append("get_environmental_context")
        context = get_environmental_context(request)
        _require(raw is not None and isinstance(receipt, dict), "MISSING_DATA")
        trace.append("query_observations")
        observations = query_observations(request, context, raw, receipt)
        trace.append("run_verified_model")
        result = run_verified_model(request, observations)
        trace.append("check_regulatory_context")
        regulatory = check_regulatory_context()
        trace.append("generate_evidence_report")
        report = generate_evidence_report(request, observations, result, regulatory)
        return {"status": "OBSERVATION_DESCRIPTIVE_SLICE_PASSED", "agent_version": VERSION,
                "trace": trace, "observations": observations, "result": result,
                "regulatory": regulatory, "report_zh": report}
    except Refusal as exc:
        return {"status": "REFUSED", "reason": str(exc), "agent_version": VERSION, "trace": trace}


def replay(evidence_dir=EVIDENCE_DIR):
    """Replay archived evidence without network access or modifying files."""
    path = Path(evidence_dir)
    request = json.loads((path / "request.json").read_text(encoding="utf-8"))
    receipt = json.loads((path / "noaa-receipt.json").read_text(encoding="utf-8"))
    return run_agent(request, (path / "noaa-daily.json").read_bytes(), receipt)


if __name__ == "__main__":
    print(json.dumps(replay(), ensure_ascii=False, indent=2, allow_nan=False))
