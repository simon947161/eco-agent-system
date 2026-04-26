import json
from pathlib import Path
from typing import Any, Dict

def load_json(file_path: str) -> Dict[str, Any]:
    path = Path(file_path)
    print(f"[loader] Loading JSON from: {path}")
    if not path.exists():
        raise FileNotFoundError(f"JSON file not found: {path}")
    with path.open("r", encoding="utf-8") as f:
        data = json.load(f)
    print("[loader] JSON loaded successfully")
    return data
