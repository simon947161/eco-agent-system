"""Read-only SMRC policy context in the existing research Console.

This packet is not an environmental assessment or a statutory crosswalk.
Local file availability and historical document review are separate facts.
"""
import hashlib
import json

from tools.smrc_policy_console import CONFIG, build_packet, configured_directories


def console_packet(config=None, source_dirs=None):
    if config is None:
        config = json.loads(CONFIG.read_text(encoding="utf-8"))
    packet = build_packet(config, configured_directories() if source_dirs is None else source_dirs)
    sources = {item["id"]: item for item in packet["sources"]}
    lines = []
    for line in packet["research_lines"]:
        references = ["SMRC-CSP-2035-V3", "SMRC-LSPS-2020"]
        references.extend(item["source_id"] for item in line.get("dp", []))
        references = list(dict.fromkeys(references))
        unavailable = [key for key in references if key not in sources or
                       sources[key]["local_copy_state"] != "MATCHED_RECORDED_VERSION"]
        lines.append(dict(line, source_ids=references, evidence_gaps=unavailable,
                          review_state="RESEARCH_INTERPRETATION_REQUIRES_REVIEW",
                          conclusion_level="L0", evidence_maturity="S0",
                          execution_status="NOT_AUTHORISED_BY_POLICY_REFERENCE"))
    packet["research_lines"] = lines
    packet["as_of"] = config.get("as_of")
    packet["current_execution_documents_verified"] = False
    packet["assessment_created"] = False
    packet["continuity"] = {
        "program_id": "COOMA-WATER-FIRE-WASTEWATER-WATCH",
        "parent_issue": 128, "orchestration_issue": 126, "bridge_pr": 127,
        "bridge_dependency": "SEPARATE_DRAFT_NOT_MERGED",
        "receipt_passport": "Use the existing monthly cycle workflow; policy views do not mint assessment receipts.",
    }
    payload = json.dumps(packet, sort_keys=True, ensure_ascii=False, separators=(",", ":"))
    packet["packet_digest"] = hashlib.sha256(payload.encode()).hexdigest()
    return packet

