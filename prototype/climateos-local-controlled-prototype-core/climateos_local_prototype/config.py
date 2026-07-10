from pathlib import Path

BOUNDARY_LABEL = "Prototype / Candidate / Non-Operational"
DEFAULT_HOST = "127.0.0.1"
DEFAULT_PORT = 8765
LOCAL_HOSTS = {"127.0.0.1", "localhost"}
PROHIBITED_PUBLIC_HOST = "0.0.0.0"

PACKAGE_ROOT = Path(__file__).resolve().parents[1]
LOCAL_DATA_DIR = PACKAGE_ROOT / "local_data"
DEFAULT_DB_PATH = LOCAL_DATA_DIR / "climateos_local_prototype.sqlite3"
RUNTIME_EXPORT_DIR = PACKAGE_ROOT / "runtime_exports"
STATIC_DIR = PACKAGE_ROOT / "static"
SEED_DATA_PATH = PACKAGE_ROOT / "data" / "seed_candidates.json"

PROHIBITED_STATUS_TERMS = {
    "certified",
    "assured",
    "compliant",
    "final truth",
    "officially verified",
    "approved esg performance",
    "verified carbon outcome",
    "regulatory acceptance",
}


def validate_local_host(host: str) -> str:
    normalized = (host or "").strip().lower()
    if normalized not in LOCAL_HOSTS:
        raise ValueError(
            "ClimateOS local prototype may bind only to 127.0.0.1 or localhost."
        )
    return normalized
