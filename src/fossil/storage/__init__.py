"""Persistence layer: read/write JSON artifacts."""

from __future__ import annotations

from fossil.storage.json_store import (
    read_model,
    snapshot_path,
    write_json,
    write_model,
)

__all__ = ["read_model", "snapshot_path", "write_json", "write_model"]
