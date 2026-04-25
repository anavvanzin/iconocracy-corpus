#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import sys
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any
from urllib.parse import urlparse

REPO_ROOT = Path(__file__).resolve().parents[2]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from tools.argos.manifest import locked_update_manifest
from tools.argos.provenance import build_provenance
from tools.argos.protocols.direct import fetch_direct
from tools.argos.protocols.iiif import discover_iiif, fetch_iiif_image
from tools.argos.protocols.playwright_fallback import fetch_with_playwright
from tools.argos.storage import resolve_storage_root


def _load_log_run():
    module_path = REPO_ROOT / "tools" / "scripts" / "log_agent_run.py"
    spec = importlib.util.spec_from_file_location("tools.scripts.log_agent_run_runtime", module_path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module.log_run


log_run = _load_log_run()

DEFAULT_MANIFEST_PATH = REPO_ROOT / "data" / "raw" / "argos" / "manifest.json"
BLOCK_STEP_FAILURES = {"401_unauthorized", "403_block", "429_rate_limited", "blocked", "manual_required"}
BLOCK_STEP_STATUS_CODES = {401, 403, 429}


def _utc_timestamp() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).strftime("%Y-%m-%dT%H:%M:%SZ")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Acquire one ARGOS manifest item.")
    parser.add_argument("--manifest", type=Path, default=DEFAULT_MANIFEST_PATH, help="Path to manifest.json")
    parser.add_argument("--item-id", required=True, help="Manifest item_id to acquire")
    parser.add_argument("--dry-run", action="store_true", help="Print attempt plan without mutating manifest")
    parser.add_argument(
        "--playwright-allowed",
        action="store_true",
        help="Allow Playwright fallback on restricted domains when policy permits escalation",
    )
    return parser.parse_args()


def load_manifest(path: Path) -> dict[str, Any]:
    return json.loads(Path(path).read_text(encoding="utf-8"))


def load_manifest_item(path: Path, item_id: str) -> tuple[dict[str, Any], dict[str, Any]]:
    manifest = load_manifest(path)
    items = manifest.get("items", [])
    for item in items:
        if item.get("item_id") == item_id:
            return manifest, item
    raise KeyError(f"Manifest item not found: {item_id}")


def infer_next_step(protocol: str, last_attempt: dict[str, Any] | None) -> str:
    if not last_attempt:
        return "stop"

    if last_attempt.get("success"):
        return "complete"

    failure_class = str(last_attempt.get("failure_class") or "")
    status_code = last_attempt.get("status_code")
    if last_attempt.get("manual_required") or failure_class == "manual_required":
        return "stop"
    blocked = failure_class in BLOCK_STEP_FAILURES or status_code in BLOCK_STEP_STATUS_CODES or "block" in failure_class

    if blocked and protocol in {"direct", "unknown", "blocked"}:
        return "iiif-discovery"
    if blocked and protocol in {"iiif", "playwright-required"}:
        return "playwright-fallback"
    return "stop"


def _should_try_playwright(item: dict[str, Any], *, allow_restricted: bool) -> bool:
    protocol = item.get("protocol")
    if protocol == "playwright-required":
        return True
    if allow_restricted:
        return True
    return False


def _safe_suffix(url: str | None, fallback: str = ".jpg") -> str:
    path = urlparse(url or "").path
    suffix = Path(path).suffix.lower()
    if suffix in {".jpg", ".jpeg", ".png", ".tif", ".tiff", ".gif", ".webp"}:
        return suffix
    return fallback


def _destination_path(storage_root: Path, storage_tier: str, item: dict[str, Any]) -> Path:
    return storage_root / storage_tier / f"{item['item_id']}{_safe_suffix(item.get('source_url'))}"


def _iiif_discovery_item(item: dict[str, Any]) -> dict[str, Any]:
    discovery_item = dict(item)
    if not discovery_item.get("url"):
        discovery_item["url"] = item.get("source_url")
    return discovery_item


def _compute_sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with Path(path).open("rb") as handle:
        for chunk in iter(lambda: handle.read(65536), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def _cleanup_artifacts(*paths: Path | None) -> None:
    for path in paths:
        if path is None:
            continue
        try:
            Path(path).unlink(missing_ok=True)
        except OSError:
            pass


def _build_sidecar_payload(
    *,
    item: dict[str, Any],
    asset_path: Path,
    sha256: str,
    acquisition_result: dict[str, Any],
    storage_tier: str,
    attempts: list[dict[str, Any]],
) -> dict[str, Any]:
    provenance = build_provenance(
        fetched_by="argos",
        protocol=acquisition_result.get("protocol") or item.get("protocol") or "unknown",
        storage_tier=storage_tier,
        source_url=acquisition_result.get("source_url") or item.get("source_url"),
        record_id=item.get("item_id"),
        extra_metadata={
            "title": item.get("title"),
            "sha256": sha256,
            "local_path": str(asset_path),
            "source_domain": acquisition_result.get("source_domain") or item.get("source_domain"),
            "status_code": acquisition_result.get("status_code"),
            "bytes_written": acquisition_result.get("bytes_written"),
            "notes": acquisition_result.get("notes") or [],
        },
    )
    return {
        "item_id": item.get("item_id"),
        "title": item.get("title"),
        "local_path": str(asset_path),
        "sha256": sha256,
        "provenance": provenance,
        "attempts": attempts,
    }


def _manifest_patch(
    *,
    item: dict[str, Any],
    status: str,
    failure_class: str,
    failure_reason: str,
    attempts_count: int,
    asset_path: Path | None,
    sha256: str,
    acquisition_result: dict[str, Any] | None,
) -> dict[str, Any]:
    method = (acquisition_result or {}).get("protocol") or item.get("protocol") or "unknown"
    retrieved_from = (acquisition_result or {}).get("source_url") or item.get("source_url")
    metadata = dict(item.get("provenance", {}).get("metadata", {}))
    if acquisition_result:
        metadata.update(
            {
                "bytes_written": acquisition_result.get("bytes_written"),
                "status_code": acquisition_result.get("status_code"),
                "source_domain": acquisition_result.get("source_domain") or item.get("source_domain"),
                "notes": acquisition_result.get("notes") or [],
            }
        )
        for key in ("manifest_url", "iiif_source"):
            if acquisition_result.get(key):
                metadata[key] = acquisition_result[key]
    metadata = {key: value for key, value in metadata.items() if value is not None}
    return {
        "status": status,
        "failure_class": failure_class,
        "failure_reason": failure_reason,
        "attempts": attempts_count,
        "local_path": str(asset_path) if asset_path else "",
        "sha256": sha256,
        "provenance": {
            "retrieved_at": _utc_timestamp(),
            "retrieved_from": retrieved_from,
            "agent": "argos",
            "method": method,
            "metadata": metadata,
        },
    }


def _attempt_protocol(protocol: str, item: dict[str, Any], dest_path: Path, *, playwright_allowed: bool) -> dict[str, Any]:
    if protocol == "iiif":
        return fetch_iiif_image(_iiif_discovery_item(item), dest_path)
    if protocol == "playwright-required":
        return fetch_with_playwright(item["source_url"], dest_path, playwright_allowed=playwright_allowed)
    if protocol in {"direct", "unknown", "blocked"}:
        return fetch_direct(item["source_url"], dest_path)
    return {
        "success": False,
        "protocol": protocol,
        "dest_path": str(dest_path),
        "bytes_written": 0,
        "status_code": None,
        "failure_class": "unsupported_protocol",
        "error": f"Unsupported protocol: {protocol}",
        "notes": [],
    }


def _attempt_iiif_fallback(item: dict[str, Any], dest_path: Path) -> dict[str, Any]:
    discovery_item = _iiif_discovery_item(item)
    discovered = discover_iiif(discovery_item)
    if not discovered:
        return {
            "success": False,
            "protocol": "iiif",
            "dest_path": str(dest_path),
            "bytes_written": 0,
            "status_code": None,
            "failure_class": "iiif_unavailable",
            "error": "No supported IIIF pattern discovered",
            "notes": [],
        }

    image_url = discovered.get("image_url")
    if not image_url:
        return {
            "success": False,
            "protocol": "iiif",
            "dest_path": str(dest_path),
            "bytes_written": 0,
            "status_code": None,
            "failure_class": "iiif_image_unavailable",
            "error": "Discovered IIIF manifest but no fetchable image URL",
            "manifest_url": discovered.get("manifest_url"),
            "iiif_source": discovered.get("iiif_source"),
            "notes": [],
        }

    result = fetch_direct(image_url, dest_path)
    result["protocol"] = "iiif"
    result["manifest_url"] = discovered.get("manifest_url")
    result["iiif_source"] = discovered.get("iiif_source")
    result["source_url"] = image_url
    result.setdefault("notes", [])
    return result


def acquire_item(
    *,
    manifest_path: Path = DEFAULT_MANIFEST_PATH,
    item_id: str,
    playwright_allowed: bool = False,
    dry_run: bool = False,
) -> dict[str, Any]:
    started_at = time.time()
    manifest, item = load_manifest_item(manifest_path, item_id)
    storage_root, storage_tier = resolve_storage_root(REPO_ROOT)
    dest_path = _destination_path(Path(storage_root), storage_tier, item)

    attempt_plan = [item.get("protocol") or "unknown", "iiif-discovery-on-block", "playwright-fallback-when-allowed"]
    if dry_run:
        return {
            "status": "dry-run",
            "item_id": item_id,
            "storage_root": str(storage_root),
            "storage_tier": storage_tier,
            "attempt_plan": attempt_plan,
            "manifest_status": item.get("status"),
        }

    attempts: list[dict[str, Any]] = []
    current_protocol = item.get("protocol") or "unknown"
    result = _attempt_protocol(current_protocol, item, dest_path, playwright_allowed=playwright_allowed)
    attempts.append({"step": current_protocol, **result})

    next_step = infer_next_step(current_protocol, result)
    if next_step == "iiif-discovery":
        iiif_result = _attempt_iiif_fallback(item, dest_path)
        attempts.append({"step": "iiif", **iiif_result})
        result = iiif_result
        current_protocol = "iiif"
        next_step = infer_next_step(current_protocol, result)

    if next_step == "playwright-fallback" and _should_try_playwright(item, allow_restricted=playwright_allowed):
        playwright_result = fetch_with_playwright(
            item["source_url"],
            dest_path,
            playwright_allowed=playwright_allowed,
        )
        attempts.append({"step": "playwright", **playwright_result})
        result = playwright_result
        current_protocol = "playwright-required"
    elif next_step == "playwright-fallback":
        result = {
            "success": False,
            "manual_required": True,
            "failure_class": "manual_required",
            "error": "Blocked source requires manual browser retrieval (Playwright not allowed)",
        }

    if result.get("success"):
        asset_path = Path(result.get("dest_path") or dest_path)
        if not asset_path.exists():
            raise FileNotFoundError(f"Fetch reported success but file is missing: {asset_path}")
        sha256 = _compute_sha256(asset_path)
        sidecar_path = asset_path.with_suffix(".meta.json")
        sidecar_payload = _build_sidecar_payload(
            item=item,
            asset_path=asset_path,
            sha256=sha256,
            acquisition_result=result,
            storage_tier=storage_tier,
            attempts=attempts,
        )
        _write_json(sidecar_path, sidecar_payload)
        patch = _manifest_patch(
            item=item,
            status="success",
            failure_class="",
            failure_reason="",
            attempts_count=int(item.get("attempts", 0)) + len(attempts),
            asset_path=asset_path,
            sha256=sha256,
            acquisition_result=result,
        )
        try:
            locked_update_manifest(manifest_path, item_id, patch)
        except Exception:
            _cleanup_artifacts(sidecar_path, asset_path)
            raise
        duration = max(0, int(time.time() - started_at))
        log_run(agent="argos", status="success", items=1, duration=duration, details=f"Acquired {item_id}")
        return {
            "status": "success",
            "item_id": item_id,
            "asset_path": str(asset_path),
            "sidecar_path": str(sidecar_path),
            "sha256": sha256,
            "attempts": attempts,
        }

    failure_class = str(result.get("failure_class") or "acquisition_failed")
    failure_reason = str(result.get("error") or failure_class)
    patch = _manifest_patch(
        item=item,
        status="manual" if result.get("manual_required") else "failed",
        failure_class=failure_class,
        failure_reason=failure_reason,
        attempts_count=int(item.get("attempts", 0)) + len(attempts),
        asset_path=None,
        sha256="",
        acquisition_result=result,
    )
    locked_update_manifest(manifest_path, item_id, patch)
    duration = max(0, int(time.time() - started_at))
    log_status = "warning" if result.get("manual_required") else "error"
    log_run(agent="argos", status=log_status, items=1, duration=duration, details=f"{item_id}: {failure_reason}")
    return {
        "status": patch["status"],
        "item_id": item_id,
        "failure_class": failure_class,
        "failure_reason": failure_reason,
        "attempts": attempts,
    }


def main() -> int:
    args = parse_args()
    try:
        result = acquire_item(
            manifest_path=args.manifest,
            item_id=args.item_id,
            playwright_allowed=args.playwright_allowed,
            dry_run=args.dry_run,
        )
    except (KeyError, ValueError, FileNotFoundError) as exc:
        print(str(exc), file=sys.stderr)
        return 1

    if args.dry_run:
        print(f"Dry run for {args.item_id}")
        print(f"Storage root: {result['storage_root']}")
        print(f"Storage tier: {result['storage_tier']}")
        for index, step in enumerate(result["attempt_plan"], start=1):
            print(f"{index}. {step}")
        print("Manifest unchanged")
        return 0

    if result["status"] == "success":
        print(f"Acquired {args.item_id} -> {result['asset_path']}")
        print(f"SHA256: {result['sha256']}")
        return 0

    print(f"{args.item_id} -> {result['status']}: {result['failure_reason']}")
    return 1


if __name__ == "__main__":
    sys.exit(main())
