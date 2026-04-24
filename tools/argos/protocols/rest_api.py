"""REST-API adapters for archives that expose structured JSON endpoints.

For domains whose image URL is only reachable via a typed API call
(bildindex, V&A, IWM), this module translates a source URL into an
image URL that ``direct.fetch`` can consume. Falls back to IIIF
discovery on failure.
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

from . import direct, iiif

USER_AGENT = direct.USER_AGENT

VAM_OBJECT_RE = re.compile(r"/(?:[^/]+/)*O(\d+)(?:/|$)")
IWM_ITEM_RE = re.compile(r"^/collections/item/object/(\d+)(?:/|$)")
MET_OBJECT_RE = re.compile(r"^/art/collection/search/(\d+)(?:/|$)")


def _host_matches(host: str, domain: str) -> bool:
    """Return True for an exact domain or one of its subdomains."""

    return host == domain or host.endswith(f".{domain}")


def _get_json(url: str) -> dict[str, Any] | None:
    if not HAS_REQUESTS:
        return None
    try:
        resp = requests.get(
            url,
            headers={"User-Agent": USER_AGENT, "Accept": "application/json"},
            timeout=15,
        )
        if resp.status_code >= 400:
            return None
        return resp.json()
    except (requests.RequestException, ValueError):
        return None


def resolve(source_url: str) -> dict[str, Any]:
    """Return ``{'image_url', 'archive'}`` or empty dict."""

    parsed = urlparse(source_url)
    host = (parsed.hostname or "").lower()
    path = parsed.path

    # V&A Museum
    m = VAM_OBJECT_RE.search(path)
    if m and _host_matches(host, "vam.ac.uk"):
        obj = m.group(1)
        data = _get_json(
            f"https://api.vam.ac.uk/v2/objects/search?id_object=O{obj}&images=1"
        )
        if data and data.get("records"):
            record = data["records"][0]
            iiif_base = record.get("_images", {}).get("_iiif_image_base_url")
            if iiif_base:
                return {
                    "archive": "vam",
                    "image_url": iiif_base.rstrip("/") + "/full/full/0/default.jpg",
                }
        return {}

    # IWM
    m = IWM_ITEM_RE.search(path)
    if m and _host_matches(host, "iwm.org.uk"):
        obj = m.group(1)
        data = _get_json(
            f"https://www.iwm.org.uk/collections/item/object/{obj}.json"
        )
        if data and data.get("image_url"):
            return {"archive": "iwm", "image_url": data["image_url"]}
        return {}

    # Met Museum public Collection API
    m = MET_OBJECT_RE.search(path)
    if m and _host_matches(host, "metmuseum.org"):
        obj = m.group(1)
        data = _get_json(
            f"https://collectionapi.metmuseum.org/public/collection/v1/objects/{obj}"
        )
        if data and data.get("primaryImage"):
            return {"archive": "met", "image_url": data["primaryImage"]}
        return {}

    return {}


def fetch(source_url: str, dest_path) -> dict[str, Any]:
    """REST-API pipeline with IIIF fallback.

    Returns a direct.fetch-style dict.
    """

    info = resolve(source_url)
    if info and info.get("image_url"):
        result = direct.fetch(info["image_url"], dest_path)
        result["fetched_url"] = info["image_url"]
        return result
    # No REST adapter — fall through to IIIF discovery.
    return iiif.fetch(source_url, dest_path)
