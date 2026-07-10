from pathlib import Path
import argparse
import json
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from climateos_local_prototype.config import DEFAULT_DB_PATH  # noqa: E402
from climateos_local_prototype.synthetic import run_performance_baseline  # noqa: E402


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate deterministic synthetic local records for performance review.")
    parser.add_argument("--db-path", default=str(DEFAULT_DB_PATH))
    parser.add_argument("--scale", type=int, action="append", default=None)
    args = parser.parse_args()

    result = run_performance_baseline(Path(args.db_path), scales=args.scale)
    print(json.dumps(result, indent=2, ensure_ascii=True))


if __name__ == "__main__":
    main()
