import json
from typing import Any

from .config import BOUNDARY_LABEL
from .repository import new_id
from .schemas import ModelResponseImport, PromptBundle

PROMPT_INSTRUCTIONS = [
    "Return suggestions only; do not verify, approve, score, certify, assure, or conclude.",
    "Keep every output labelled Prototype / Candidate / Non-Operational.",
    "Do not alter Human Review, Founder Gate, evidence admission, or archive approval status.",
    "Use the provided response schema exactly; a human must import and decide on each suggestion.",
]


def generate_prompt_bundle(candidate_records: list[dict[str, Any]]) -> PromptBundle:
    return PromptBundle(
        bundle_id=new_id("PB"),
        boundary_label=BOUNDARY_LABEL,
        instructions=PROMPT_INSTRUCTIONS,
        candidate_records=candidate_records,
    )


def deterministic_mock_response(bundle: PromptBundle) -> ModelResponseImport:
    response_id = new_id("MR")
    suggestions = []
    for index, record in enumerate(bundle.candidate_records[:3], start=1):
        suggestions.append(
            {
                "suggestion_id": f"{response_id}-SUG-{index:03d}",
                "category": "review-note draft",
                "target_record_id": record.get("id", ""),
                "suggestion_text": (
                    "Draft review note: keep this record candidate-only and confirm "
                    "source, translation, risk, and Founder Gate needs before future use."
                ),
                "provenance": "deterministic mock adapter",
            }
        )
    return ModelResponseImport(
        response_id=response_id,
        source_label="deterministic mock adapter",
        suggestions=suggestions,
    )


def parse_imported_response(raw_json: str) -> ModelResponseImport:
    data = json.loads(raw_json)
    return ModelResponseImport.model_validate(data)
