"""Filesystem JSON storage for snapshots and classifications.

All persisted artifacts are plain JSON so the repository stays human-readable
and the dataset is reproducible from disk alone.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import TypeVar

from pydantic import BaseModel

from fossil.config import get_logger
from fossil.core.exceptions import StorageError

T = TypeVar("T", bound=BaseModel)

logger = get_logger(__name__)


def _safe_name(full_name: str) -> str:
    """Turn 'owner/name' into a filesystem-safe stem."""
    return full_name.replace("/", "__")


def write_model(model: BaseModel, path: Path) -> Path:
    """Serialize a pydantic model to pretty JSON at ``path``."""
    try:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(model.model_dump_json(indent=2), encoding="utf-8")
    except OSError as exc:  # pragma: no cover - filesystem failure
        raise StorageError(f"Failed writing {path}: {exc}") from exc
    logger.debug("Wrote %s", path)
    return path


def read_model(model_type: type[T], path: Path) -> T:
    """Load and validate a pydantic model from JSON at ``path``."""
    try:
        raw = path.read_text(encoding="utf-8")
    except OSError as exc:
        raise StorageError(f"Failed reading {path}: {exc}") from exc
    return model_type.model_validate_json(raw)


def write_json(data: object, path: Path) -> Path:
    """Write arbitrary JSON-serializable data."""
    try:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(data, indent=2, default=str), encoding="utf-8")
    except OSError as exc:  # pragma: no cover
        raise StorageError(f"Failed writing {path}: {exc}") from exc
    return path


def snapshot_path(base: Path, full_name: str) -> Path:
    return base / f"{_safe_name(full_name)}.json"
