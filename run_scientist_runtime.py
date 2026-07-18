"""Start the bounded ClimateOS minimum human-AI scientist Runtime."""

from __future__ import annotations

import argparse
from pathlib import Path

from cczps_lite.scientist_runtime.server import serve


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--host", default="127.0.0.1", choices=("127.0.0.1", "localhost"))
    parser.add_argument("--port", type=int, default=8765)
    parser.add_argument("--db", type=Path, default=Path("runtime_data/scientist_runtime.sqlite3"))
    args = parser.parse_args()
    serve(args.db, args.host, args.port)


if __name__ == "__main__":
    main()
