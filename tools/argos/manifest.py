"""Build and safely update the ARGOS acquisition manifest.

Two operations:

1. ``build_manifest`` — scan ``corpus/corpus-data.json`` for pending items
   (those lacking ``thumbnail_url`` or otherwise missing from
   ``data/raw/drive-manifest.json``) and write an initial manifest.

2. ``locked_update`` — atomically merge a patch for a single item into
   the manifest. Every subagent call goes through this helper so
   concurrent writes do not corrupt the file. An advisory ``fcntl.flock``
   on ``manifest.lock`` serialises writers; a ``.bak`` copy is written
   before each commit.
"""

from __future__ import annotations

import fcntl
import json
import os
import tempfile
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from . import classifier
from . import storage

MANIFEST_PATH = storage.REPO_ROOT / "data" / "raw" / "argos" / "manifest.json"
LOCK_PATH = MANIFEST_PATH.with_name("manifest.lock")
BACKUP_PATH = MANIFEST_PATH.with_suffix(".json.bak")

MANIFEST_VERSION = "1.0"


# ---------------------------------------------------------------------------
# Builder
# ---------------------------------------------------------------------------


def _is_pending(corpus_item: dict[str, Any], drive_items: set[str]) -> bool:
    """Return True if ``corpus_item`` still needs image acquisition."""

    if corpus_item["id"] in drive_items:
        return False
    # Missing thumbnail → pending.
    if not corpus_item.get("thumbnail_url"):
        return True
    # Also treat items whose source URL we can classify as acquirable, but
    # where only a thumbnail exists (low-res) — leave for operator decision
    # by NOT marking pending. Keeping conservative: thumbnail present → skip.
    return False


def _load_drive_items() -> set[str]:
    """Return the set of item_ids already recorded in ``drive-manifest.json``."""

    path = storage.REPO_ROOT / "data" / "raw" / "drive-manifest.json"
    if not path.exists():
        return set()
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return set()
    return {entry.get("item_id") for entry in data.get("items", []) if entry.get("item_id")}


def _make_entry(corpus_item: dict[str, Any]) -> dict[str, Any]:
    """Transform a corpus-data.json row into an ARGOS manifest entry."""

    url = corpus_item.get("url") or ""
    domain = classifier.domain_for(url)
    protocol = classifier.classify(url)
    tos = classifier.is_tos_restricted(url)
    has_url = bool(url.strip())
    if not has_url:
        status, fc, fr = "manual", "no_source_url", "Corpus entry has no source URL."
    elif tos:
        status, fc, fr = (
            "tos_restricted",
            "tos_restricted",
            "Domain flagged TOS-restricted; acquisition requires explicit opt-in.",
        )
    else:
        status, fc, fr = "pending", None, None
    entry: dict[str, Any] = {
        "item_id": corpus_item["id"],
        "title": corpus_item.get("title"),
        "country": corpus_item.get("country"),
        "source_archive": corpus_item.get("source_archive"),
        "source_domain": domain,
        "source_url": url,
        "protocol": protocol,
        "iiif_manifest_url": None,
        "status": status,
        "failure_class": fc,
        "failure_reason": fr,
        "attempts": [],
        "local_path": None,
        "bytes": None,
        "sha256": None,
        "provenance": None,
    }
    return entry


def build_manifest(dry_run: bool = False) -> dict[str, Any]:
    """Scan corpus-data.json and write a fresh manifest.

    Returns the manifest dictionary. When ``dry_run`` is True the file
    is not written.
    """

    corpus_path = storage.REPO_ROOT / "corpus" / "corpus-data.json"
    corpus = json.loads(corpus_path.read_text(encoding="utf-8"))
    drive_items = _load_drive_items()

    pending = [item for item in corpus if _is_pending(item, drive_items)]
    entries = [_make_entry(item) for item in pending]

    root, tier = storage.resolve_root()
    manifest = {
        "manifest_version": MANIFEST_VERSION,
        "generated_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "storage_root": str(root),
        "storage_tier": tier,
        "total_items": len(entries),
        "items": entries,
    }

    if not dry_run:
        MANIFEST_PATH.parent.mkdir(parents=True, exist_ok=True)
        _atomic_write(manifest)
    return manifest


# ---------------------------------------------------------------------------
# Atomic locked update
# ---------------------------------------------------------------------------


def _atomic_write(manifest: dict[str, Any]) -> None:
    """Write ``manifest.json`` atomically via temp-file + rename.

    Also refreshes ``manifest.json.bak`` with the previous contents.
    """

    MANIFEST_PATH.parent.mkdir(parents=True, exist_ok=True)

    # Backup existing file before overwriting.
    if MANIFEST_PATH.exists():
        BACKUP_PATH.write_bytes(MANIFEST_PATH.read_bytes())

    # Refuse to overwrite with obviously-bad data.
    if not isinstance(manifest, dict) or "items" not in manifest:
        raise ValueError("Refusing to write manifest without 'items' key")

    tmp_fd, tmp_name = tempfile.mkstemp(
        prefix="manifest.", suffix=".json", dir=str(MANIFEST_PATH.parent)
    )
    try:
        with os.fdopen(tmp_fd, "w", encoding="utf-8") as fh:
            json.dump(manifest, fh, indent=2, ensure_ascii=False)
            fh.flush()
            os.fsync(fh.fileno())
        os.replace(tmp_name, MANIFEST_PATH)
    except Exception:
        try:
            os.unlink(tmp_name)
        except OSError:
            pass
        raise


def load_manifest() -> dict[str, Any]:
    """Read the current manifest (no lock held — callers in locked_update hold it)."""

    return json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))


def locked_update(item_id: str, patch: dict[str, Any]) -> dict[str, Any]:
    """Acquire an exclusive lock, merge ``patch`` into the item, rewrite.

    ``patch`` may include any top-level item fields. ``attempts`` is a
    list and is *appended* to rather than replaced.
    """

    LOCK_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(LOCK_PATH, "a+") as lockfile:
        fcntl.flock(lockfile.fileno(), fcntl.LOCK_EX)
        try:
            manifest = load_manifest()
            found = False
            for entry in manifest["items"]:
                if entry["item_id"] == item_id:
                    new_attempts = patch.pop("attempts", None)
                    if new_attempts:
                        entry.setdefault("attempts", []).extend(new_attempts)
                    entry.update(patch)
                    found = True
                    break
            if not found:
                raise KeyError(f"item_id not in manifest: {item_id}")
            manifest["updated_at"] = datetime.now(timezone.utc).isoformat(
                timespec="seconds"
            )
            _atomic_write(manifest)
            return manifest
        finally:
            fcntl.flock(lockfile.fileno(), fcntl.LOCK_UN)
