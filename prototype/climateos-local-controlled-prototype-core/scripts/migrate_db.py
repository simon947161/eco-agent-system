from pathlib import Path
import argparse
import json
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from climateos_local_prototype.config import DEFAULT_DB_PATH  # noqa: E402
from climateos_local_prototype.migrations import migrate_database, migration_preflight  # noqa: E402


def main() -> None:
    parser = argparse.ArgumentParser(description="Run local schema migration preflight or migration.")
    parser.add_argument("--db-path", default=str(DEFAULT_DB_PATH))
    parser.add_argument("--run", action="store_true", help="Apply migration. Without this flag, preflight only.")
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--actor-label", default="local operator")
    args = parser.parse_args()

    db_path = Path(args.db_path)
    if args.run:
        result = migrate_database(db_path, dry_run=args.dry_run, actor_label=args.actor_label)
    else:
        result = migration_preflight(db_path)
    print(json.dumps(result, indent=2, ensure_ascii=True))


if __name__ == "__main__":
    main()
