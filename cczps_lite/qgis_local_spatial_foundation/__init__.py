"""Local-only QGIS spatial foundation contracts for the Cooma learning project."""

from .contract import (
    BOOKMARKS,
    DEFAULT_VIEW_EXTENT,
    PROJECT_FILENAME,
    PROJECT_LAYER_GROUPS,
    PROVISIONAL_SCOPE_STATUS,
    REVISION_PROJECT_FILENAME,
    RUNTIME_RELATIVE_ROOT,
    WORKSPACE_DIRECTORIES,
)
from .workspace import SpatialWorkspaceError, ensure_local_workspace

__all__ = [
    "BOOKMARKS",
    "DEFAULT_VIEW_EXTENT",
    "PROJECT_FILENAME",
    "PROJECT_LAYER_GROUPS",
    "PROVISIONAL_SCOPE_STATUS",
    "REVISION_PROJECT_FILENAME",
    "RUNTIME_RELATIVE_ROOT",
    "WORKSPACE_DIRECTORIES",
    "SpatialWorkspaceError",
    "ensure_local_workspace",
]
