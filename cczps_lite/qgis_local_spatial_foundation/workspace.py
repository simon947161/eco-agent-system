"""Create the controlled, git-ignored local QGIS workspace without overwrite."""

from __future__ import annotations

import json
from pathlib import Path

from .contract import (
    REVISION_PROJECT_FILENAME,
    RUNTIME_RELATIVE_ROOT,
    WORKSPACE_DIRECTORIES,
    legacy_workspace_contract,
    workspace_contract,
)


class SpatialWorkspaceError(ValueError):
    """Raised when the local-only workspace contract would be violated."""


def _assert_no_symlink_components(path: Path) -> None:
    current = path
    while True:
        if current.exists() and current.is_symlink():
            raise SpatialWorkspaceError(f"workspace path must not contain symlinks: {current}")
        if current.parent == current:
            return
        current = current.parent


def ensure_local_workspace(repo_root: Path, *, test_root: Path | None = None) -> dict[str, object]:
    """Create or verify the fixed local workspace.

    Production callers cannot select an arbitrary output path. ``test_root`` is
    available only for tiny synthetic temporary-directory tests.
    """

    repo_root = repo_root.resolve()
    root = test_root.resolve() if test_root is not None else (repo_root / RUNTIME_RELATIVE_ROOT).resolve()
    expected_root = (repo_root / RUNTIME_RELATIVE_ROOT).resolve()
    if test_root is None and root != expected_root:
        raise SpatialWorkspaceError("production workspace must use the controlled runtime_data path")
    _assert_no_symlink_components(root)
    root.mkdir(parents=True, exist_ok=True)
    for name in WORKSPACE_DIRECTORIES:
        child = root / name
        if child.exists() and not child.is_dir():
            raise SpatialWorkspaceError(f"workspace entry is not a directory: {child}")
        if child.is_symlink():
            raise SpatialWorkspaceError(f"workspace directory must not be a symlink: {child}")
        child.mkdir(exist_ok=True)

    contract = workspace_contract()
    contract_path = root / "manifests" / "workspace_contract.json"
    serialized = json.dumps(contract, indent=2, sort_keys=True, ensure_ascii=False) + "\n"
    active_contract_path = contract_path
    if contract_path.exists():
        if contract_path.is_symlink() or not contract_path.is_file():
            raise SpatialWorkspaceError("workspace contract must be a regular file")
        if contract_path.read_text(encoding="utf-8") != serialized:
            legacy_serialized = (
                json.dumps(legacy_workspace_contract(), indent=2, sort_keys=True, ensure_ascii=False)
                + "\n"
            )
            if contract_path.read_text(encoding="utf-8") != legacy_serialized:
                raise SpatialWorkspaceError("existing workspace contract differs; overwrite refused")
            active_contract_path = root / "manifests" / "workspace_contract_ux_revision.json"
            if active_contract_path.exists():
                if active_contract_path.read_text(encoding="utf-8") != serialized:
                    raise SpatialWorkspaceError("existing UX revision contract differs; overwrite refused")
            else:
                with active_contract_path.open("x", encoding="utf-8", newline="\n") as handle:
                    handle.write(serialized)
    else:
        with contract_path.open("x", encoding="utf-8", newline="\n") as handle:
            handle.write(serialized)

    return {
        "root": root,
        "project_path": root / "project" / contract["project_filename"],
        "revision_project_path": root / "project" / REVISION_PROJECT_FILENAME,
        "contract_path": active_contract_path,
        "directories": tuple(root / name for name in WORKSPACE_DIRECTORIES),
        "contract": contract,
    }
