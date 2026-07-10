import json
from pathlib import Path
from typing import Any

from .config import BOUNDARY_LABEL, RUNTIME_EXPORT_DIR
from .repository import PrototypeRepository, now_iso
from .schemas import ArchiveRequest


def _write_json(path: Path, data: Any) -> None:
    path.write_text(json.dumps(data, indent=2, ensure_ascii=True) + "\n", encoding="utf-8")


def _write_register(path: Path, title: str, records: list[dict[str, Any]]) -> None:
    lines = [f"# {title}", "", BOUNDARY_LABEL, ""]
    if not records:
        lines.append("No records in this local archive export.")
    for record in records:
        lines.extend(
            [
                f"## {record.get('id', 'record')}",
                "",
                f"- Type: {record.get('record_type', '')}",
                f"- Title: {record.get('title', '')}",
                f"- Status: {record.get('status', '')}",
                f"- Readiness: {record.get('readiness_label', '')}",
                f"- Risk flags: {', '.join(record.get('risk_flags', []))}",
                f"- Boundary: {record.get('boundary_label', BOUNDARY_LABEL)}",
                "",
            ]
        )
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def generate_archive_bundle(
    repository: PrototypeRepository,
    request: ArchiveRequest,
    output_root: str | Path | None = None,
) -> dict[str, Any]:
    root = Path(output_root) if output_root else RUNTIME_EXPORT_DIR
    timestamp = now_iso().replace(":", "").replace("-", "")
    bundle_dir = root / f"{request.case_id}-{timestamp}"
    bundle_dir.mkdir(parents=True, exist_ok=True)

    candidates = repository.list_candidates()
    audit_events = repository.list_audit_events()
    human_reviews = repository.list_human_reviews()
    founder_gates = repository.list_founder_gates()

    manifest = {
        "case_id": request.case_id,
        "created_at": now_iso(),
        "boundary_label": BOUNDARY_LABEL,
        "reviewer_label": request.reviewer_label,
        "reason": request.reason,
        "record_count": len(candidates),
        "human_review_count": len(human_reviews),
        "founder_gate_count": len(founder_gates),
        "operational_status": "Not operational",
    }

    _write_json(bundle_dir / "case-manifest.json", manifest)
    _write_register(
        bundle_dir / "source-candidate-register.md",
        "Source Candidate Register",
        [item for item in candidates if item["record_type"] == "source_candidate"],
    )
    _write_register(
        bundle_dir / "signal-register.md",
        "Signal Register",
        [item for item in candidates if item["record_type"] == "signal_candidate"],
    )
    _write_register(
        bundle_dir / "claim-candidate-register.md",
        "Claim Candidate Register",
        [item for item in candidates if item["record_type"] == "claim_candidate"],
    )
    _write_register(
        bundle_dir / "knowledge-object-register.md",
        "Knowledge Object Register",
        [item for item in candidates if item["record_type"] == "knowledge_object_candidate"],
    )
    _write_register(
        bundle_dir / "evidence-candidate-register.md",
        "Evidence Candidate Register",
        [item for item in candidates if item["record_type"] == "evidence_candidate"],
    )
    _write_json(bundle_dir / "evidence-readiness-record.json", candidates)
    _write_json(bundle_dir / "risk-flag-register.json", [item["risk_flags"] for item in candidates])
    _write_json(bundle_dir / "human-review-record.json", human_reviews)
    _write_json(bundle_dir / "founder-gate-record.json", founder_gates)
    _write_json(bundle_dir / "audit-log.json", audit_events)
    (bundle_dir / "closure-summary.md").write_text(
        "\n".join(
            [
                "# Closure Summary",
                "",
                BOUNDARY_LABEL,
                "",
                "This local archive export is a review package only.",
                "It does not commit, push, publish, deploy, certify, assure, score, or admit evidence.",
                "",
            ]
        ),
        encoding="utf-8",
    )
    archive_event = repository.record_archive_event(
        request.case_id, str(bundle_dir), request.reviewer_label, request.reason
    )
    return {"bundle_dir": str(bundle_dir), "manifest": manifest, "archive_event": archive_event}
