"""Run the Founder-approved gauge 410033 official flow intake."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from cczps_lite.integration.mittagang_410033_flow_intake import run_intake


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--output-root",
        type=Path,
        default=Path("runtime_data/mittagang_410033_flow_intake"),
    )
    parser.add_argument(
        "--approve-official-download",
        action="store_true",
        help="Confirm this manual, zero-cost retrieval of the fixed BoM HRS product.",
    )
    args = parser.parse_args()
    _, public_receipt = run_intake(
        args.output_root,
        human_approval=args.approve_official_download,
    )
    print(json.dumps(public_receipt, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
