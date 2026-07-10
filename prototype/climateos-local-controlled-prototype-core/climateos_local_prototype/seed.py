import json
from pathlib import Path

from .config import SEED_DATA_PATH
from .repository import PrototypeRepository
from .schemas import CandidateCreate


def load_seed_records(path: str | Path = SEED_DATA_PATH) -> list[dict]:
    return json.loads(Path(path).read_text(encoding="utf-8"))


def seed_database(repository: PrototypeRepository, path: str | Path = SEED_DATA_PATH) -> list[dict]:
    created = []
    existing_ids = {record["id"] for record in repository.list_candidates()}
    for item in load_seed_records(path):
        record_id = item.pop("id")
        if record_id in existing_ids:
            continue
        payload = CandidateCreate.model_validate(item)
        created.append(
            repository.create_candidate(
                payload,
                actor_label="deterministic seed fixture",
                record_id=record_id,
            )
        )
    return created
