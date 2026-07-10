from pathlib import Path
import argparse
import json
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from climateos_local_prototype.config import DEFAULT_DB_PATH  # noqa: E402
from climateos_local_prototype.diagnostics import run_data_integrity_diagnostics, safe_integrity_check  # noqa: E402


def main() -> None:
    parser = argparse.ArgumentParser(description="Run local SQLite integrity and prototype data diagnostics.")
    parser.add_argument("--db-path", default=str(DEFAULT_DB_PATH))
    parser.add_argument("--data-diagnostics", action="store_true")
    args = parser.parse_args()

    db_path = Path(args.db_path)
    result = run_data_integrity_diagnostics(db_path) if args.data_diagnostics else safe_integrity_check(db_path)
    print(json.dumps(result, indent=2, ensure_ascii=True))


if __name__ == "__main__":
    main()
