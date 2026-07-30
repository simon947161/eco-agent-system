"""Run the Founder-approved bounded historical flow characterisation."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from cczps_lite.analysis.mittagang_410033_historical_characterisation import (
    run_characterisation,
)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--raw-csv",
        type=Path,
        default=Path(
            "runtime_data/mittagang_410033_flow_intake/raw/410033_daily_ts.csv"
        ),
    )
    parser.add_argument(
        "--retrieval-receipt",
        type=Path,
        default=Path("runtime_data/mittagang_410033_flow_intake/full_receipt.json"),
    )
    parser.add_argument(
        "--output-root",
        type=Path,
        default=Path(
            "cczps_lite/output/mittagang_410033_historical_characterisation"
        ),
    )
    parser.add_argument("--issued-at")
    args = parser.parse_args()
    result, output_digests = run_characterisation(
        args.raw_csv,
        args.output_root,
        issued_at=args.issued_at,
        retrieval_receipt_path=args.retrieval_receipt,
    )
    print(
        json.dumps(
            {
                "run_id": result["run_id"],
                "source_digest": result["source"]["content_digest"],
                "conclusion_level": result["maximum_conclusion_level"],
                "evidence_maturity": result["evidence_maturity"],
                "output_digests": output_digests,
            },
            indent=2,
            ensure_ascii=False,
        )
    )


if __name__ == "__main__":
    main()
