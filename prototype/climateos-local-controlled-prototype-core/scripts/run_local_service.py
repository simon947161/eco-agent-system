from pathlib import Path
import argparse
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

import uvicorn  # noqa: E402

from climateos_local_prototype.api import create_app  # noqa: E402
from climateos_local_prototype.config import DEFAULT_DB_PATH, DEFAULT_HOST, DEFAULT_PORT, validate_local_host  # noqa: E402


def main() -> None:
    parser = argparse.ArgumentParser(description="Run the local ClimateOS Evidence Passport prototype.")
    parser.add_argument("--host", default=DEFAULT_HOST, help="Allowed values: 127.0.0.1 or localhost.")
    parser.add_argument("--port", default=DEFAULT_PORT, type=int)
    parser.add_argument("--db-path", default=str(DEFAULT_DB_PATH))
    args = parser.parse_args()

    host = validate_local_host(args.host)
    app = create_app(Path(args.db_path))
    uvicorn.run(app, host=host, port=args.port)


if __name__ == "__main__":
    main()
