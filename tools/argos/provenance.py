"""Sidecar provenance metadata for downloaded binaries.

For every successful acquisition, ARGOS writes ``{item_id}.meta.json``
alongside the binary. This file records the exact URL fetched, the
protocol that succeeded, the sha256, a timestamp, and a human-readable
user agent. Together with the corpus record and the drive-manifest,
this closes the traceability loop demanded by CLAUDE.md.
"""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from . import USER_AGENT


def write_sidecar(
    binary_path: Path,
    item_id: str,
    source_url: str,
    fetched_url: str,
    protocol: str,
    sha256: str,
    bytes_: int,
    country: str,
    license_hint: str | None = None,
) -> Path:
    """Write a ``*.meta.json`` sidecar next to the binary and return its path."""

    meta: dict[str, Any] = {
        "schema": "argos-provenance/1.0",
        "item_id": item_id,
        "country": country,
        "source_url": source_url,
        "fetched_url": fetched_url,
        "protocol": protocol,
        "sha256": sha256,
        "bytes": bytes_,
        "fetched_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "user_agent": USER_AGENT,
        "license_hint": license_hint,
    }
    sidecar = binary_path.with_suffix(binary_path.suffix + ".meta.json")
    sidecar.write_text(json.dumps(meta, indent=2, ensure_ascii=False), encoding="utf-8")
    return sidecar
