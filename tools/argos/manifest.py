from __future__ import annotations

import json
import os
import tempfile
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from typing import Iterable

import fcntl

from tools.argos.classifier import classify_source
from tools.scripts.validate_schemas import validate_record


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


def _summary_from_items(items: list[dict]) -> dict[str, int]:
    counts = Counter(item.get("status", "") for item in items)
    return {
        "total_items": len(items),
        "pending": counts.get("pending", 0),
        "success": counts.get("success", 0),
        "partial": counts.get("partial", 0),
        "failed": counts.get("failed", 0),
        "manual": counts.get("manual", 0),
    }


def _default_lock_path(path: Path) -> Path:
    return path.with_name("manifest.lock")


def _load_manifest(path: Path) -> dict:
    try:
        raw = path.read_text(encoding="utf-8")
    except FileNotFoundError as exc:
        raise ValueError(f"Manifest file not found: {path}") from exc

    if not raw.strip():
        raise ValueError(f"Manifest file is empty: {path}")

    try:
        manifest = json.loads(raw)
    except json.JSONDecodeError as exc:
        raise ValueError(f"Manifest file contains invalid JSON: {path}") from exc

    if not isinstance(manifest, dict):
        raise ValueError("Manifest root must be a JSON object")

    return manifest


def _validate_manifest(manifest: dict) -> None:
    is_valid, errors = validate_record(manifest, "argos-manifest")
    if not is_valid:
        raise ValueError("Manifest failed schema validation after update: " + "; ".join(errors))


def _fsync_directory(path: Path) -> None:
    if os.name == "nt":
        return

    try:
        directory_fd = os.open(path, os.O_RDONLY)
    except OSError:
        return

    try:
        os.fsync(directory_fd)
    except OSError:
        pass
    finally:
        os.close(directory_fd)


def _recursive_merge(base: dict, patch: dict) -> dict:
    merged = dict(base)
    for key, value in patch.items():
        existing = merged.get(key)
        if isinstance(existing, dict) and isinstance(value, dict):
            merged[key] = _recursive_merge(existing, value)
        else:
            merged[key] = value
    return merged


def _write_atomic_json(path: Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    serialized = json.dumps(payload, ensure_ascii=False, indent=2) + "\n"

    fd, tmp_name = tempfile.mkstemp(prefix=f"{path.stem}-", suffix=".tmp", dir=path.parent)
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as handle:
            handle.write(serialized)
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(tmp_name, path)
        _fsync_directory(path.parent)
    except Exception:
        if os.path.exists(tmp_name):
            os.unlink(tmp_name)
        raise


def locked_update_manifest(path: str | Path, item_id: str, patch: dict, lock_path: str | Path | None = None) -> dict:
    manifest_path = Path(path)
    resolved_lock_path = Path(lock_path) if lock_path is not None else _default_lock_path(manifest_path)

    if not isinstance(patch, dict) or not patch:
        raise ValueError("Patch must be a non-empty JSON object")

    resolved_lock_path.parent.mkdir(parents=True, exist_ok=True)
    with resolved_lock_path.open("a+", encoding="utf-8") as lock_handle:
        fcntl.flock(lock_handle.fileno(), fcntl.LOCK_EX)
        manifest = _load_manifest(manifest_path)
        items = manifest.get("items")
        if not isinstance(items, list):
            raise ValueError("Manifest items must be a list")

        updated_items = []
        matched = False
        for index, item in enumerate(items):
            if not isinstance(item, dict):
                raise ValueError("Manifest items must be JSON objects")

            existing_item_id = item.get("item_id")
            if not isinstance(existing_item_id, str) or not existing_item_id:
                raise ValueError(f"Manifest item at index {index} is missing item_id")

            if existing_item_id == item_id:
                updated_items.append(_recursive_merge(item, patch))
                matched = True
            else:
                updated_items.append(item)

        if not matched:
            raise KeyError(f"Manifest item not found: {item_id}")

        updated_manifest = dict(manifest)
        updated_manifest["items"] = updated_items
        updated_manifest["summary"] = _summary_from_items(updated_items)
        _validate_manifest(updated_manifest)

        _write_atomic_json(manifest_path.with_suffix(".json.bak"), manifest)
        _write_atomic_json(manifest_path, updated_manifest)
        return updated_manifest


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


def pending_item_count(manifest: dict) -> int:
    return int(manifest.get("summary", {}).get("pending", len(manifest.get("items", []))))


def protocol_breakdown(manifest: dict) -> dict[str, int]:
    counts = Counter(item["protocol"] for item in manifest.get("items", []))
    return dict(sorted(counts.items()))
