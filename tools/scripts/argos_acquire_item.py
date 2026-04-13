#!/usr/bin/env python3
"""ARGOS per-item acquisition worker.

Subagents call this script once per item. It executes the full
acquisition state machine:

  1. Robots check (cached per domain per run).
  2. HEAD probe.
  3. Protocol dispatch (iiif / rest-api / direct / playwright-required).
  4. On 401/403/429/Cloudflare → IIIF discovery fallback.
  5. On still-failing → Playwright fallback (soft-imported).
  6. On success → write binary + sidecar, compute sha256.
  7. Writeback → locked update of manifest.json.

Usage:
    python tools/scripts/argos_acquire_item.py --item-id BR-001
    python tools/scripts/argos_acquire_item.py --domain gallica.bnf.fr --limit 3
"""

from __future__ import annotations

import argparse
import json
import re
import sys
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any
from urllib.parse import urlparse

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from argos import USER_AGENT, classifier, manifest as argos_manifest, provenance, storage
from argos.protocols import direct, iiif, playwright_fallback, rest_api

try:
    from urllib.robotparser import RobotFileParser

    import requests  # type: ignore[import]

    HAS_REQUESTS = True
except ImportError:  # pragma: no cover
    HAS_REQUESTS = False

# Rate-limit: polite intra-host sleep between items in the same run.
INTRA_HOST_SLEEP = 1.5
CLOUDFLARE_SIGNATURES = ("cloudflare", "attention required")


# ---------------------------------------------------------------------------
# Robots.txt (cached in-process for the duration of a single run)
# ---------------------------------------------------------------------------

_ROBOTS_CACHE: dict[str, RobotFileParser | None] = {}


def _robots_allows(url: str) -> tuple[bool, str | None]:
    """Return ``(allowed, reason)``. Unknown → allowed (conservative default)."""

    host = classifier.domain_for(url)
    if not host:
        return True, None
    if host in _ROBOTS_CACHE:
        rp = _ROBOTS_CACHE[host]
    else:
        if not HAS_REQUESTS:
            _ROBOTS_CACHE[host] = None
            return True, None
        robots_url = f"https://{host}/robots.txt"
        rp = RobotFileParser()
        rp.set_url(robots_url)
        try:
            resp = requests.get(
                robots_url, headers={"User-Agent": USER_AGENT}, timeout=5
            )
            if resp.status_code >= 400:
                _ROBOTS_CACHE[host] = None
                return True, None
            rp.parse(resp.text.splitlines())
            _ROBOTS_CACHE[host] = rp
        except requests.RequestException:
            _ROBOTS_CACHE[host] = None
            return True, None
    if rp is None:
        return True, None
    if not rp.can_fetch(USER_AGENT, url):
        return False, f"robots.txt denies {USER_AGENT}"
    return True, None


# ---------------------------------------------------------------------------
# Cloudflare heuristic
# ---------------------------------------------------------------------------


def _is_cloudflare_response(head_info: dict[str, Any]) -> bool:
    ct = (head_info.get("content_type") or "").lower()
    return head_info.get("status_code") == 403 and (
        "text/html" in ct
        or any(sig in (head_info.get("error") or "").lower() for sig in CLOUDFLARE_SIGNATURES)
    )


# ---------------------------------------------------------------------------
# Core per-item routine
# ---------------------------------------------------------------------------


def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def _ext_from_content_type(ct: str | None, url: str) -> str:
    if ct:
        ct = ct.split(";")[0].strip().lower()
        if ct == "image/jpeg":
            return ".jpg"
        if ct == "image/png":
            return ".png"
        if ct == "image/tiff":
            return ".tif"
        if ct == "image/webp":
            return ".webp"
        if ct == "image/gif":
            return ".gif"
    # Fallback: infer from URL path.
    path = urlparse(url).path.lower()
    for ext in (".jpg", ".jpeg", ".png", ".tif", ".tiff", ".webp", ".gif"):
        if path.endswith(ext):
            return ".jpg" if ext == ".jpeg" else ext
    return ".jpg"


def _infer_country_code(country: str | None) -> str:
    """Map a country name to a 2-3 letter code used for subdirectory naming."""

    if not country:
        return "UNK"
    mapping = {
        "Argentina": "AR",
        "Austria": "AT",
        "Belgium": "BE",
        "Brazil": "BR",
        "Brasil": "BR",
        "France": "FR",
        "Germany": "DE",
        "Italy": "IT",
        "Netherlands": "NL",
        "Portugal": "PT",
        "Spain": "ES",
        "United Kingdom": "UK",
        "UK": "UK",
        "United States": "US",
        "USA": "US",
    }
    return mapping.get(country, country[:3].upper())


def _dispatch(protocol: str, source_url: str, dest_path: Path) -> dict[str, Any]:
    """Call the appropriate protocol handler; return its result dict."""

    if protocol == "iiif":
        return iiif.fetch(source_url, dest_path)
    if protocol == "rest-api":
        return rest_api.fetch(source_url, dest_path)
    if protocol == "direct":
        return direct.fetch(source_url, dest_path)
    if protocol == "playwright-required":
        return playwright_fallback.fetch(source_url, dest_path)
    # unknown / blocked-prone → try direct first.
    return direct.fetch(source_url, dest_path)


def acquire_item(entry: dict[str, Any], dry_run: bool = False) -> dict[str, Any]:
    """Run the acquisition state machine for a single manifest entry.

    Returns the *patch* to be written back via locked_update().
    """

    item_id = entry["item_id"]
    source_url = entry.get("source_url") or ""
    protocol = entry.get("protocol") or "unknown"
    country = entry.get("country") or ""
    cc = _infer_country_code(country)

    attempts: list[dict[str, Any]] = []
    patch: dict[str, Any] = {"attempts": attempts}

    if not source_url:
        patch["status"] = "manual"
        patch["failure_class"] = "no_source_url"
        patch["failure_reason"] = "Corpus entry has no URL"
        return patch

    # 1. TOS
    if classifier.is_tos_restricted(source_url):
        patch["status"] = "tos_restricted"
        patch["failure_class"] = "tos_restricted"
        patch["failure_reason"] = "Domain is TOS-restricted; manual review required."
        return patch

    # 2. Robots
    allowed, reason = _robots_allows(source_url)
    if not allowed:
        patch["status"] = "manual"
        patch["failure_class"] = "robots_denied"
        patch["failure_reason"] = reason
        return patch

    if dry_run:
        patch["status"] = "pending"
        patch["dry_run"] = True
        patch["planned_protocol"] = protocol
        return patch

    # 3. HEAD probe
    head = direct.head_probe(source_url)
    attempts.append(
        {
            "ts": _now_iso(),
            "protocol": "head",
            "status_code": head.get("status_code"),
            "error": head.get("error"),
            "content_type": head.get("content_type"),
        }
    )

    # 4. Compute destination path (use .jpg as placeholder; refined later).
    country_dir = storage.country_dir(cc)
    dest = country_dir / f"{item_id}.jpg"

    # 5. Primary dispatch
    result = _dispatch(protocol, source_url, dest)
    attempts.append(
        {
            "ts": _now_iso(),
            "protocol": protocol,
            "status_code": result.get("status_code"),
            "error": result.get("error"),
            "bytes": result.get("bytes"),
            "fetched_url": result.get("fetched_url"),
        }
    )
    if result.get("iiif_manifest_url"):
        patch["iiif_manifest_url"] = result["iiif_manifest_url"]

    # 6. Fallback chain on failure
    if not result.get("ok"):
        status_code = result.get("status_code")
        cloudflare = _is_cloudflare_response(
            {
                "status_code": status_code,
                "content_type": head.get("content_type"),
                "error": result.get("error"),
            }
        )

        # 6a. IIIF discovery (unless we already tried it).
        if protocol != "iiif":
            iiif_result = iiif.fetch(source_url, dest)
            attempts.append(
                {
                    "ts": _now_iso(),
                    "protocol": "iiif-fallback",
                    "status_code": iiif_result.get("status_code"),
                    "error": iiif_result.get("error"),
                    "bytes": iiif_result.get("bytes"),
                    "fetched_url": iiif_result.get("fetched_url"),
                }
            )
            if iiif_result.get("iiif_manifest_url"):
                patch["iiif_manifest_url"] = iiif_result["iiif_manifest_url"]
            if iiif_result.get("ok"):
                result = iiif_result

        # 6b. Playwright fallback on still-failing.
        if not result.get("ok"):
            pw_result = playwright_fallback.fetch(source_url, dest)
            attempts.append(
                {
                    "ts": _now_iso(),
                    "protocol": "playwright-fallback",
                    "status_code": pw_result.get("status_code"),
                    "error": pw_result.get("error"),
                    "bytes": pw_result.get("bytes"),
                    "fetched_url": pw_result.get("fetched_url"),
                }
            )
            if pw_result.get("ok"):
                result = pw_result

        # 6c. Classify final failure.
        if not result.get("ok"):
            err = (result.get("error") or "").lower()
            if err == "playwright_unavailable":
                failure_class = "playwright_unavailable"
            elif err.startswith("playwright"):
                failure_class = "playwright_timeout"
            elif cloudflare:
                failure_class = "cloudflare"
            elif status_code == 403:
                failure_class = "403_block"
            elif status_code == 404:
                failure_class = "404_not_found"
            elif err == "iiif_not_found":
                failure_class = "iiif_not_found"
            elif status_code and 500 <= status_code < 600:
                failure_class = "server_error"
            else:
                failure_class = "network"
            patch["status"] = "manual" if failure_class == "playwright_unavailable" else "failed"
            patch["failure_class"] = failure_class
            patch["failure_reason"] = result.get("error") or f"HTTP {status_code}"
            return patch

    # 7. Success — rename to correct extension, compute sha256, write sidecar.
    try:
        content_type = result.get("content_type")
        ext = _ext_from_content_type(content_type, result.get("fetched_url") or source_url)
        if ext != dest.suffix:
            new_dest = dest.with_suffix(ext)
            try:
                dest.replace(new_dest)
                dest = new_dest
            except OSError:
                pass
        sha = storage.sha256_file(dest)
        provenance.write_sidecar(
            binary_path=dest,
            item_id=item_id,
            source_url=source_url,
            fetched_url=result.get("fetched_url") or source_url,
            protocol=attempts[-1]["protocol"] if attempts else protocol,
            sha256=sha,
            bytes_=result.get("bytes") or dest.stat().st_size,
            country=cc,
        )
        patch["status"] = "success"
        patch["local_path"] = storage.relpath(dest)
        patch["bytes"] = result.get("bytes") or dest.stat().st_size
        patch["sha256"] = sha
        patch["provenance"] = {
            "fetched_at": _now_iso(),
            "fetched_by": f"argos/acquire_item",
            "user_agent": USER_AGENT,
            "protocol_succeeded": attempts[-1]["protocol"] if attempts else protocol,
        }
    except Exception as exc:  # noqa: BLE001
        patch["status"] = "partial"
        patch["failure_class"] = "post_download"
        patch["failure_reason"] = f"Downloaded but failed to finalise: {exc}"
    return patch


def _select_items(
    data: dict[str, Any],
    item_id: str | None,
    domain: str | None,
    limit: int | None,
    include_tos: bool,
) -> list[dict[str, Any]]:
    entries = data["items"]
    if item_id:
        return [e for e in entries if e["item_id"] == item_id]
    if domain:
        entries = [e for e in entries if e.get("source_domain") == domain]
    # Skip TOS-restricted unless explicitly included.
    if not include_tos:
        entries = [e for e in entries if e.get("status") != "tos_restricted"]
    # Only attempt items still needing work.
    entries = [e for e in entries if e.get("status") in {"pending", "failed", "manual"}]
    if limit:
        entries = entries[:limit]
    return entries


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--item-id", help="Process a single item")
    parser.add_argument("--domain", help="Process all items with this source_domain")
    parser.add_argument("--limit", type=int, help="Cap the number of items processed")
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Report the plan without fetching or writing binaries",
    )
    parser.add_argument(
        "--allow-tos",
        action="store_true",
        help="Include items flagged TOS-restricted (use with caution)",
    )
    parser.add_argument(
        "--no-writeback",
        action="store_true",
        help="Do not call locked_update; print the patch to stdout instead",
    )
    args = parser.parse_args()

    if not any([args.item_id, args.domain]):
        parser.error("Provide --item-id or --domain")

    data = argos_manifest.load_manifest()
    entries = _select_items(
        data,
        item_id=args.item_id,
        domain=args.domain,
        limit=args.limit,
        include_tos=args.allow_tos,
    )
    if not entries:
        print("No matching items.")
        return 0

    last_host: str | None = None
    summary: list[dict[str, Any]] = []
    for entry in entries:
        host = entry.get("source_domain")
        if last_host == host and not args.dry_run:
            time.sleep(INTRA_HOST_SLEEP)
        last_host = host

        patch = acquire_item(entry, dry_run=args.dry_run)
        if args.no_writeback:
            print(json.dumps({"item_id": entry["item_id"], "patch": patch}, indent=2))
        else:
            try:
                argos_manifest.locked_update(entry["item_id"], patch)
            except Exception as exc:  # noqa: BLE001
                print(f"[writeback-failed] {entry['item_id']}: {exc}", file=sys.stderr)
        summary.append(
            {
                "item_id": entry["item_id"],
                "status": patch.get("status"),
                "failure_class": patch.get("failure_class"),
            }
        )

    print(json.dumps({"processed": len(summary), "results": summary}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
