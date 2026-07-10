from pathlib import Path
from time import perf_counter
from typing import Any

from .repository import PrototypeRepository
from .schemas import CandidateCreate


def create_synthetic_records(repository: PrototypeRepository, count: int) -> list[dict[str, Any]]:
    if count < 1 or count > 5000:
        raise ValueError("Synthetic record count must be between 1 and 5000.")
    created = []
    for index in range(1, count + 1):
        record_id = f"SYN-{index:05d}"
        try:
            repository.get_candidate(record_id)
            continue
        except KeyError:
            pass
        payload = CandidateCreate(
            record_type="source_candidate",
            title=f"Synthetic source candidate {index}",
            summary="Deterministic synthetic candidate for local hardening tests.",
            readiness_label="Candidate only",
            risk_flags=["RF-SYN"],
            human_review_need="Synthetic review placeholder.",
            founder_gate_need="None for local synthetic test.",
        )
        created.append(repository.create_candidate(payload, actor_label="synthetic fixture generator", record_id=record_id))
    return created


def run_performance_baseline(db_path: str | Path, scales: list[int] | None = None) -> dict[str, Any]:
    repository = PrototypeRepository(db_path)
    scales = scales or [100]
    results = []
    for count in scales:
        start = perf_counter()
        created = create_synthetic_records(repository, count)
        create_elapsed = perf_counter() - start
        start = perf_counter()
        listed = repository.list_candidates()
        list_elapsed = perf_counter() - start
        results.append(
            {
                "scale": count,
                "created": len(created),
                "total_candidates": len(listed),
                "create_seconds": round(create_elapsed, 4),
                "list_seconds": round(list_elapsed, 4),
            }
        )
    return {"status": "completed", "boundary_label": "Prototype / Candidate / Non-Operational", "results": results}
