from pathlib import Path
import argparse
import json
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from climateos_local_prototype.config import DEFAULT_DB_PATH, LOCAL_BACKUP_DIR  # noqa: E402
from climateos_local_prototype.maintenance import create_backup  # noqa: E402


def main() -> None:
    parser = argparse.ArgumentParser(description="Create a manual local backup of the prototype SQLite database.")
    parser.add_argument("--db-path", default=str(DEFAULT_DB_PATH))
    parser.add_argument("--backup-root", default=str(LOCAL_BACKUP_DIR))
    parser.add_argument("--label", default="manual")
    parser.add_argument("--actor-label", default="local operator")
    args = parser.parse_args()

    result = create_backup(
        Path(args.db_path),
        backup_root=Path(args.backup_root),
        label=args.label,
        actor_label=args.actor_label,
    )
    print(json.dumps(result, indent=2, ensure_ascii=True))


if __name__ == "__main__":
    main()
