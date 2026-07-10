from pathlib import Path
import argparse
import json
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from climateos_local_prototype.config import DEFAULT_DB_PATH  # noqa: E402
from climateos_local_prototype.diagnostics import run_data_integrity_diagnostics  # noqa: E402


def main() -> None:
    parser = argparse.ArgumentParser(description="Run local prototype data integrity diagnostics.")
    parser.add_argument("--db-path", default=str(DEFAULT_DB_PATH))
    args = parser.parse_args()

    print(json.dumps(run_data_integrity_diagnostics(Path(args.db_path)), indent=2, ensure_ascii=True))


if __name__ == "__main__":
    main()
