from concurrent.futures import ThreadPoolExecutor

from climateos_local_prototype.repository import PrototypeRepository
from climateos_local_prototype.schemas import CandidateCreate
from climateos_local_prototype.synthetic import run_performance_baseline


def test_concurrent_local_writes_complete_without_background_workers(tmp_path):
    db_path = tmp_path / "concurrent.sqlite3"
    repository = PrototypeRepository(db_path)

    def create(index: int) -> str:
        local_repository = PrototypeRepository(db_path)
        record = local_repository.create_candidate(
            CandidateCreate(
                record_type="source_candidate",
                title=f"Concurrent source candidate {index}",
                summary="Concurrent foreground write for local SQLite hardening review.",
                risk_flags=["RF-CONCURRENT"],
            ),
            actor_label="concurrency test",
            record_id=f"CON-{index:03d}",
        )
        return record["id"]

    with ThreadPoolExecutor(max_workers=4) as executor:
        created = list(executor.map(create, range(12)))

    assert len(created) == 12
    assert len(repository.list_candidates()) == 12
    audit_events = repository.list_audit_events()
    assert len(audit_events) == 12
    assert all(event["sequence_number"] > 0 for event in audit_events)


def test_synthetic_performance_baseline_is_local_and_bounded(tmp_path):
    db_path = tmp_path / "synthetic.sqlite3"
    result = run_performance_baseline(db_path, scales=[25])
    assert result["status"] == "completed"
    assert result["boundary_label"] == "Prototype / Candidate / Non-Operational"
    assert result["results"][0]["scale"] == 25
    assert result["results"][0]["total_candidates"] >= 25
