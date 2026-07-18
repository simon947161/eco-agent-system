"""Start the next ClimateOS environmental-question Runtime on localhost."""

from __future__ import annotations

import argparse

from cczps_lite.environmental_question_runtime.server import serve


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--db", default="runtime_data/task2002_environmental_questions.sqlite3")
    parser.add_argument("--port", type=int, default=8766)
    args = parser.parse_args()
    serve(args.db, port=args.port)


if __name__ == "__main__":
    main()
