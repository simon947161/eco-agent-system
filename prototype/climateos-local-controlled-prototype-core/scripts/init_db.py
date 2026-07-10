from pathlib import Path
import argparse
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from climateos_local_prototype.config import DEFAULT_DB_PATH  # noqa: E402
from climateos_local_prototype.database import reset_database  # noqa: E402
from climateos_local_prototype.repository import PrototypeRepository  # noqa: E402
from climateos_local_prototype.seed import seed_database  # noqa: E402


def main() -> None:
    parser = argparse.ArgumentParser(description="Initialize the local ClimateOS prototype database.")
    parser.add_argument("--db-path", default=str(DEFAULT_DB_PATH))
    parser.add_argument("--reset", action="store_true", help="Reset the local prototype database first.")
    parser.add_argument("--seed", action="store_true", help="Load deterministic candidate fixtures.")
    args = parser.parse_args()

    db_path = Path(args.db_path)
    if args.reset:
        reset_database(db_path)
    repository = PrototypeRepository(db_path)
    created = seed_database(repository) if args.seed else []
    print(f"Database ready: {db_path}")
    print(f"Seed records created: {len(created)}")


if __name__ == "__main__":
    main()
