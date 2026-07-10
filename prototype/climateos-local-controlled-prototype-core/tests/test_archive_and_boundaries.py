from pathlib import Path

from fastapi.testclient import TestClient

from climateos_local_prototype.api import create_app
from climateos_local_prototype.repository import PrototypeRepository
from climateos_local_prototype.seed import seed_database


def test_archive_export_creates_local_review_bundle(tmp_path):
    db_path = tmp_path / "prototype.sqlite3"
    repository = PrototypeRepository(db_path)
    seed_database(repository)
    client = TestClient(create_app(db_path))

    response = client.post(
        "/api/archive/export",
        json={
            "case_id": "CASE-MOCK-001",
            "reviewer_label": "Reviewer A",
            "reason": "Manual local archive export for controlled prototype review.",
        },
    )
    assert response.status_code == 201
    bundle_dir = Path(response.json()["bundle_dir"])
    assert (bundle_dir / "case-manifest.json").exists()
    assert (bundle_dir / "audit-log.json").exists()
    assert (bundle_dir / "closure-summary.md").exists()


def test_no_task541_directory_exists():
    repo_root = Path(__file__).resolve().parents[3]
    assert not (repo_root / "docs" / "tasks" / "task541_600").exists()
    assert not (repo_root / "prototype" / "climateos-task541").exists()


def test_static_frontend_avoids_candidate_innerhtml():
    app_js = Path(__file__).resolve().parents[1] / "static" / "app.js"
    content = app_js.read_text(encoding="utf-8")
    assert ".innerHTML" not in content
    assert "textContent" in content


def test_no_live_provider_or_github_automation_dependency():
    root = Path(__file__).resolve().parents[1]
    text = "\n".join(
        path.read_text(encoding="utf-8")
        for path in root.rglob("*")
        if path.is_file()
        and ".venv" not in path.parts
        and path.suffix in {".py", ".js", ".html", ".md", ".txt", ".json"}
    )
    prohibited = [
        "api." + "openai.com",
        "anthropic" + ".com",
        "generativelanguage" + ".googleapis.com",
        "github.com" + "/repos",
        "schedule" + ".every",
        "Background" + "Tasks",
        "O" + "Auth",
        "docker" + " compose",
        "ver" + "cel",
    ]
    for token in prohibited:
        assert token not in text
