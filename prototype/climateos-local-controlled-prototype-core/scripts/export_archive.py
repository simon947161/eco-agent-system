from pathlib import Path
import argparse
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from climateos_local_prototype.archive import generate_archive_bundle  # noqa: E402
from climateos_local_prototype.config import DEFAULT_DB_PATH  # noqa: E402
from climateos_local_prototype.repository import PrototypeRepository  # noqa: E402
from climateos_local_prototype.schemas import ArchiveRequest  # noqa: E402


def main() -> None:
    parser = argparse.ArgumentParser(description="Create a local review archive export.")
    parser.add_argument("--case-id", required=True)
    parser.add_argument("--reviewer-label", required=True)
    parser.add_argument("--reason", required=True)
    parser.add_argument("--db-path", default=str(DEFAULT_DB_PATH))
    parser.add_argument("--output-root", default=None)
    args = parser.parse_args()

    repository = PrototypeRepository(Path(args.db_path))
    result = generate_archive_bundle(
        repository,
        ArchiveRequest(
            case_id=args.case_id,
            reviewer_label=args.reviewer_label,
            reason=args.reason,
        ),
        output_root=args.output_root,
    )
    print(result["bundle_dir"])


if __name__ == "__main__":
    main()
