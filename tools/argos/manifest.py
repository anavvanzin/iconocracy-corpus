from __future__ import annotations

from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from typing import Iterable

from tools.argos.classifier import classify_source


MANIFEST_VERSION = "1.0"


def _utc_timestamp() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).strftime("%Y-%m-%dT%H:%M:%SZ")


def _pending_item_ids(drive_manifest: dict) -> set[str]:
    return {
        item.get("item_id")
        for item in drive_manifest.get("items", [])
        if item.get("item_id")
    }


def _build_manifest_item(item: dict) -> dict:
    source_url = item["url"]
    classification = classify_source(source_url)

    return {
        "item_id": item["id"],
        "title": item.get("title", ""),
        "source_url": source_url,
        "source_domain": classification.domain,
        "protocol": classification.protocol,
        "status": "pending",
        "failure_class": "",
        "failure_reason": "",
        "attempts": 0,
        "local_path": "",
        "sha256": "",
        "provenance": {
            "agent": "argos",
            "method": classification.protocol,
            "metadata": {
                "thumbnail_missing": not bool(item.get("thumbnail_url")),
                "dispatch_group": classification.domain,
            },
        },
    }


def build_manifest(
    corpus_items: Iterable[dict],
    drive_manifest: dict,
    *,
    storage_root: str | Path,
    storage_tier: str,
    limit: int | None = None,
) -> dict:
    existing_ids = _pending_item_ids(drive_manifest)

    pending_items = [
        _build_manifest_item(item)
        for item in corpus_items
        if item.get("url") and item.get("id") not in existing_ids
    ]

    if limit is not None:
        pending_items = pending_items[:limit]

    return {
        "manifest_version": MANIFEST_VERSION,
        "generated_at": _utc_timestamp(),
        "storage_root": str(storage_root),
        "storage_tier": storage_tier,
        "summary": {
            "total_items": len(pending_items),
            "pending": len(pending_items),
            "success": 0,
            "partial": 0,
            "failed": 0,
            "manual": 0,
        },
        "items": pending_items,
    }


def protocol_breakdown(manifest: dict) -> dict[str, int]:
    counts = Counter(item["protocol"] for item in manifest.get("items", []))
    return dict(sorted(counts.items()))
