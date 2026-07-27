"""Run the manually approved Cooma official real-data pilot."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from cczps_lite.integration.cooma_official_real_data_pilot import run_pilot


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--output-root",
        type=Path,
        default=Path("runtime_data/cooma_official_real_data_pilot/2026-07"),
    )
    parser.add_argument(
        "--approve-official-download",
        action="store_true",
        help="Confirm this manual, zero-cost retrieval of the two exact BoM sources.",
    )
    args = parser.parse_args()
    _, public_receipt = run_pilot(
        args.output_root,
        human_approval=args.approve_official_download,
    )
    print(json.dumps(public_receipt, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
