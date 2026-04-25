from __future__ import annotations

import json
import re
import ssl
import urllib.request
from pathlib import Path
from urllib.parse import urlparse

from tools.argos.protocols.direct import fetch_direct


ARK_PATTERN = re.compile(r"(ark:/\d+/[^\s?#]+)", re.IGNORECASE)
EUROPEANA_ARK_PATTERN = re.compile(r"ark__(\d+)_([^/?#]+)", re.IGNORECASE)
EUROPEANA_ITEM_PATTERN = re.compile(r"/item/(\d+)/(.+?)(?:\?|$)")
LOC_RESOURCE_PATTERN = re.compile(r"/resource/([a-z]+)\.(\w+)/?")
LOC_ITEM_PATTERN = re.compile(r"/item/(\d+)/?")


def _normalize_gallica_ark(ark: str) -> str:
    clean = re.sub(r"^https?://gallica\.bnf\.fr/", "", ark)
    clean = re.sub(r"^/?ark:/", "ark:/", clean)
    if not clean.startswith("ark:"):
        clean = f"ark:/12148/{clean}"
    return clean


def gallica_manifest_from_ark(ark: str) -> str:
    """Build the Gallica IIIF manifest URL for an ARK."""

    return f"https://gallica.bnf.fr/iiif/{_normalize_gallica_ark(ark)}/manifest.json"


def _gallica_image_from_ark(ark: str) -> str:
    return f"https://gallica.bnf.fr/iiif/{_normalize_gallica_ark(ark)}/f1/full/full/0/native.jpg"


def _ark_from_text(value: str | None) -> str | None:
    if not value:
        return None
    match = ARK_PATTERN.search(value)
    if match:
        return match.group(1).rstrip("/.,;)]")
    return None


def _ark_from_europeana_url(url: str | None) -> str | None:
    if not url:
        return None
    match = EUROPEANA_ARK_PATTERN.search(url)
    if not match:
        return None
    return f"ark:/{match.group(1)}/{match.group(2)}"


_SSL_UNVERIFIED = ssl.create_default_context()
_SSL_UNVERIFIED.check_hostname = False
_SSL_UNVERIFIED.verify_mode = ssl.CERT_NONE


def _resolve_loc_item_image(json_url: str) -> str | None:
    try:
        req = urllib.request.Request(json_url, headers={"User-Agent": "ARGOS/1.0"})
        with urllib.request.urlopen(req, timeout=15, context=_SSL_UNVERIFIED) as resp:
            data = json.loads(resp.read())
    except Exception:
        return None

    for resource in data.get("resources", []):
        image = resource.get("image", {})
        full = image.get("full")
        if full and isinstance(full, str):
            return full

    for resource in data.get("resources", []):
        files = resource.get("files", [])
        for group in files:
            for variant in group if isinstance(group, list) else [group]:
                url = variant.get("url") if isinstance(variant, dict) else None
                mimetype = variant.get("mimetype", "") if isinstance(variant, dict) else ""
                if url and mimetype.startswith("image/"):
                    return url

    return None


def _discover_loc(item: dict) -> dict | None:
    thumb = item.get("thumbnail_url", "") or ""
    url = item.get("url", "") or ""

    match = LOC_RESOURCE_PATTERN.search(thumb)
    if match:
        prefix, num = match.group(1), match.group(2)
        digits = re.sub(r"\D", "", num)
        if len(digits) >= 5:
            folder = digits[:5] + "000"
            service_id = f"service:pnp:{prefix}:{folder}:{prefix}{num}"
            manifest = f"https://tile.loc.gov/image-services/iiif/{service_id}/info.json"
            image_url = f"https://tile.loc.gov/image-services/iiif/{service_id}/full/pct:100/0/default.jpg"
            return {
                "iiif_source": "loc",
                "manifest_url": manifest,
                "image_url": image_url,
            }

    match = LOC_ITEM_PATTERN.search(url)
    if match:
        item_id = match.group(1)
        json_url = f"https://www.loc.gov/item/{item_id}/?fo=json"
        image_url = _resolve_loc_item_image(json_url)
        return {
            "iiif_source": "loc_api",
            "manifest_url": json_url,
            "image_url": image_url,
        }

    return None


def discover_iiif(item: dict) -> dict | None:
    """Discover likely IIIF endpoints from known URL patterns.

    This is intentionally pattern-based discovery for common archives, not a full
    IIIF manifest parser or crawler.
    """

    url = item.get("url", "") or ""
    thumb = item.get("thumbnail_url", "") or ""

    ark = _ark_from_text(url)
    if "gallica.bnf.fr" in url and ark:
        return {
            "iiif_source": "gallica",
            "manifest_url": gallica_manifest_from_ark(ark),
            "image_url": _gallica_image_from_ark(ark),
        }

    ark = _ark_from_text(thumb)
    if "gallica.bnf.fr/iiif" in thumb and ark:
        return {
            "iiif_source": "gallica",
            "manifest_url": gallica_manifest_from_ark(ark),
            "image_url": _gallica_image_from_ark(ark),
        }

    if "europeana.eu" in url:
        ark = _ark_from_europeana_url(url)
        if ark:
            return {
                "iiif_source": "europeana_gallica",
                "manifest_url": gallica_manifest_from_ark(ark),
                "image_url": _gallica_image_from_ark(ark),
            }

        match = EUROPEANA_ITEM_PATTERN.search(url)
        if match:
            provider, local = match.group(1), match.group(2)
            return {
                "iiif_source": "europeana",
                "manifest_url": f"https://iiif.europeana.eu/presentation/{provider}/{local}/manifest",
                "image_url": None,
            }

    if "loc.gov" in url:
        return _discover_loc(item)

    return None


def fetch_iiif_image(item: dict, dest_path: Path) -> dict:
    """Fetch via a discovered IIIF image URL when one is inferable from patterns."""

    discovered = discover_iiif(item)
    if not discovered:
        return {
            "success": False,
            "protocol": "iiif",
            "dest_path": str(Path(dest_path)),
            "bytes_written": 0,
            "status_code": None,
            "failure_class": "iiif_unavailable",
            "error": "No supported IIIF pattern discovered",
        }

    image_url = discovered.get("image_url")
    if not image_url:
        return {
            "success": False,
            "protocol": "iiif",
            "dest_path": str(Path(dest_path)),
            "bytes_written": 0,
            "status_code": None,
            "failure_class": "iiif_image_unavailable",
            "error": "Discovered IIIF manifest but no fetchable image URL",
            "manifest_url": discovered.get("manifest_url"),
            "iiif_source": discovered.get("iiif_source"),
        }

    result = fetch_direct(image_url, dest_path)
    result["protocol"] = "iiif"
    result["manifest_url"] = discovered.get("manifest_url")
    result["iiif_source"] = discovered.get("iiif_source")
    result["source_url"] = image_url
    result["source_domain"] = urlparse(image_url).netloc
    return result
