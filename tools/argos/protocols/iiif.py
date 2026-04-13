"""IIIF discovery and fetch.

Archive-specific patterns (Gallica ARK, LoC ``/manifest.json``,
Europeana record API, Rijksmuseum object API) are used to discover the
IIIF Presentation manifest for a given source URL. Once found, the
image API endpoint is reduced to ``/full/max/0/default.jpg``.

Derived from the patterns in ``tools/scripts/enrich_iiif.py``.
"""

from __future__ import annotations

import re
from typing import Any
from urllib.parse import urlparse

try:
    import requests

    HAS_REQUESTS = True
except ImportError:  # pragma: no cover
    HAS_REQUESTS = False

from .. import USER_AGENT
from . import direct

GALLICA_ARK_RE = re.compile(r"ark:/(\d+/[^./]+)")
LOC_ITEM_RE = re.compile(r"loc\.gov/(?:item|resource)/([^/?#]+)")
EUROPEANA_RECORD_RE = re.compile(r"europeana\.eu/(?:[a-z]+/)?item/([^/?#]+)/([^/?#]+)")
RIJKS_OBJECT_RE = re.compile(r"rijksmuseum\.nl/.*?/([A-Z]{2}-[A-Z0-9-]+)")


def discover(source_url: str) -> dict[str, Any]:
    """Return ``{'image_url', 'manifest_url', 'archive'}`` or empty dict."""

    if not source_url:
        return {}
    host = (urlparse(source_url).hostname or "").lower()

    # Gallica (BnF) — ARK-based image API
    m = GALLICA_ARK_RE.search(source_url)
    if m and ("gallica" in host or "bnf.fr" in host):
        ark = m.group(1)
        return {
            "archive": "gallica",
            "manifest_url": f"https://gallica.bnf.fr/iiif/ark:/{ark}/manifest.json",
            "image_url": f"https://gallica.bnf.fr/iiif/ark:/{ark}/f1/full/max/0/native.jpg",
            "image_url_alt": f"https://gallica.bnf.fr/iiif/ark:/{ark}/f1/full/full/0/native.jpg",
            "thumbnail_url": f"https://gallica.bnf.fr/ark:/{ark}/f1.thumbnail",
        }

    # Library of Congress
    m = LOC_ITEM_RE.search(source_url)
    if m and "loc.gov" in host:
        item_id = m.group(1).rstrip("/")
        return {
            "archive": "loc",
            "manifest_url": f"https://www.loc.gov/item/{item_id}/manifest.json",
            "image_url": None,  # resolve via manifest; set in _resolve_loc
        }

    # Europeana
    m = EUROPEANA_RECORD_RE.search(source_url)
    if m and "europeana" in host:
        rid = f"{m.group(1)}/{m.group(2)}"
        return {
            "archive": "europeana",
            "manifest_url": f"https://api.europeana.eu/record/v2/{rid}.json?wskey=api2demo",
            "image_url": None,
        }

    # Rijksmuseum — IIIF image service keyed by object number
    m = RIJKS_OBJECT_RE.search(source_url)
    if m and "rijksmuseum" in host:
        obj = m.group(1)
        return {
            "archive": "rijksmuseum",
            "manifest_url": (
                f"https://www.rijksmuseum.nl/api/en/collection/{obj}"
                "?key=0fiuZFh4"  # public demo key
            ),
            "image_url": None,
        }

    return {}


def _resolve_via_manifest(manifest_url: str) -> str | None:
    """Fetch a IIIF manifest and extract the first image service URL."""

    if not HAS_REQUESTS:
        return None
    try:
        resp = requests.get(
            manifest_url,
            headers={"User-Agent": USER_AGENT, "Accept": "application/json"},
            timeout=15,
        )
        if resp.status_code >= 400:
            return None
        data = resp.json()
    except (requests.RequestException, ValueError):
        return None

    # IIIF Presentation v2
    sequences = data.get("sequences") or []
    if sequences:
        canvases = sequences[0].get("canvases") or []
        if canvases:
            images = canvases[0].get("images") or []
            if images:
                resource = images[0].get("resource") or {}
                service = resource.get("service") or {}
                if service.get("@id"):
                    return service["@id"].rstrip("/") + "/full/max/0/default.jpg"
                if resource.get("@id"):
                    return resource["@id"]

    # IIIF Presentation v3
    items = data.get("items") or []
    if items:
        try:
            body = items[0]["items"][0]["items"][0].get("body", {})
            service = body.get("service") or []
            if service:
                svc = service[0] if isinstance(service, list) else service
                if svc.get("id"):
                    return svc["id"].rstrip("/") + "/full/max/0/default.jpg"
            if body.get("id"):
                return body["id"]
        except (KeyError, IndexError, TypeError):
            pass

    # Europeana record JSON envelope
    obj = data.get("object")
    if isinstance(obj, dict):
        aggs = obj.get("aggregations") or []
        for agg in aggs:
            shown = agg.get("edmIsShownBy") or agg.get("edmObject")
            if shown:
                return shown

    # Rijksmuseum object envelope
    art = data.get("artObject") or {}
    web = art.get("webImage") or {}
    if web.get("url"):
        return web["url"]

    return None


def resolve_image_url(source_url: str) -> dict[str, Any]:
    """Return the best-guess image URL for ``source_url`` via IIIF discovery."""

    info = discover(source_url)
    if not info:
        return {}
    if info.get("image_url"):
        return info
    manifest_url = info.get("manifest_url")
    if manifest_url:
        resolved = _resolve_via_manifest(manifest_url)
        if resolved:
            info["image_url"] = resolved
    return info


def fetch(source_url: str, dest_path) -> dict[str, Any]:
    """IIIF pipeline: discover → resolve → GET. Returns a direct.fetch-style dict."""

    info = resolve_image_url(source_url)
    if not info or not info.get("image_url"):
        return {
            "ok": False,
            "status_code": None,
            "bytes": 0,
            "error": "iiif_not_found",
            "iiif_manifest_url": (info or {}).get("manifest_url"),
        }
    url = info["image_url"]
    result = direct.fetch(url, dest_path)
    result["fetched_url"] = url
    result["iiif_manifest_url"] = info.get("manifest_url")
    # Try the /full/full fallback for Gallica if /full/max returns 404.
    if not result["ok"] and info.get("image_url_alt"):
        result = direct.fetch(info["image_url_alt"], dest_path)
        result["fetched_url"] = info["image_url_alt"]
        result["iiif_manifest_url"] = info.get("manifest_url")
    return result
