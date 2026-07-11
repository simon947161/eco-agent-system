from concurrent.futures import ThreadPoolExecutor
import sqlite3
from threading import Barrier

import pytest

from climateos_local_prototype.repository import PrototypeRepository
from climateos_local_prototype.schemas import CandidateCreate
from climateos_local_prototype.synthetic import run_performance_baseline


def test_concurrent_local_writes_complete_without_background_workers(tmp_path):
    db_path = tmp_path / "concurrent.sqlite3"
    repository = PrototypeRepository(db_path)
    writer_count = 4
    writes_per_writer = 3
    start = Barrier(writer_count)

    def create_batch(writer_index: int) -> list[str]:
        local_repository = PrototypeRepository(db_path)
        start.wait()
        created: list[str] = []
        for item_index in range(writes_per_writer):
            record_id = f"CON-{writer_index:02d}-{item_index:02d}"
            record = local_repository.create_candidate(
                CandidateCreate(
                    record_type="source_candidate",
                    title=f"Concurrent source candidate {record_id}",
                    summary="Concurrent foreground write for local SQLite hardening review.",
                    risk_flags=["RF-CONCURRENT"],
                ),
                actor_label="concurrency test",
                record_id=record_id,
            )
            created.append(record["id"])
        return created

    with ThreadPoolExecutor(max_workers=writer_count) as executor:
        created_batches = list(executor.map(create_batch, range(writer_count)))
    created = [record_id for batch in created_batches for record_id in batch]

    candidates = repository.list_candidates()
    audit_events = repository.list_audit_events()
    assert len(created) == writer_count * writes_per_writer
    assert {candidate["id"] for candidate in candidates} == set(created)
    assert {event["record_id"] for event in audit_events} == set(created)
    assert sorted(event["sequence_number"] for event in audit_events) == list(
        range(1, len(created) + 1)
    )
    assert len({event["operation_id"] for event in audit_events}) == len(created)


def test_candidate_and_audit_write_roll_back_together(tmp_path, monkeypatch):
    repository = PrototypeRepository(tmp_path / "atomic.sqlite3")

    def fail_audit_insert(connection, event):
        raise sqlite3.IntegrityError("deterministic audit failure")

    monkeypatch.setattr(repository, "_insert_audit_event", fail_audit_insert)
    with pytest.raises(sqlite3.IntegrityError, match="deterministic audit failure"):
        repository.create_candidate(
            CandidateCreate(
                record_type="source_candidate",
                title="Atomic candidate and audit rollback",
                summary="Failure injection must roll back both records.",
            ),
            actor_label="atomicity test",
            record_id="CON-ATOMIC-001",
        )

    assert repository.list_candidates() == []
    assert repository.list_audit_events() == []


def test_synthetic_performance_baseline_is_local_and_bounded(tmp_path):
    db_path = tmp_path / "synthetic.sqlite3"
    result = run_performance_baseline(db_path, scales=[25])
    assert result["status"] == "completed"
    assert result["boundary_label"] == "Prototype / Candidate / Non-Operational"
    assert result["results"][0]["scale"] == 25
    assert result["results"][0]["total_candidates"] >= 25
