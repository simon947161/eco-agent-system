from pathlib import Path
import argparse
import json
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from climateos_local_prototype.config import DEFAULT_DB_PATH  # noqa: E402
from climateos_local_prototype.maintenance import restore_backup, validate_backup  # noqa: E402


def main() -> None:
    parser = argparse.ArgumentParser(description="Validate or restore a manual local prototype backup.")
    parser.add_argument("backup_dir")
    parser.add_argument("--target-db-path", default=str(DEFAULT_DB_PATH))
    parser.add_argument("--actor-label", default="local operator")
    parser.add_argument("--validate-only", action="store_true")
    args = parser.parse_args()

    if args.validate_only:
        result = validate_backup(Path(args.backup_dir))
    else:
        result = restore_backup(
            Path(args.backup_dir),
            Path(args.target_db_path),
            actor_label=args.actor_label,
        )
    print(json.dumps(result, indent=2, ensure_ascii=True))


if __name__ == "__main__":
    main()
