"""Direct HTTP acquisition.

Simple GET against the image URL with the ARGOS user agent. Includes
exponential-backoff retry and honours ``Retry-After``. Pattern derived
from ``tools/scripts/download_corpus_images.py``.
"""

from __future__ import annotations

import time
from typing import Any

try:  # pragma: no cover - dependency presence varies
    import requests
    from requests import Response

    HAS_REQUESTS = True
except ImportError:  # pragma: no cover
    HAS_REQUESTS = False
    Response = Any  # type: ignore[assignment, misc]

from .. import USER_AGENT

DEFAULT_TIMEOUT = 20  # seconds
MAX_RETRIES = 3


def _headers() -> dict[str, str]:
    return {
        "User-Agent": USER_AGENT,
        "Accept": "image/*,*/*;q=0.8",
        "Accept-Language": "en,pt-BR;q=0.9,fr;q=0.8,de;q=0.7",
    }


def head_probe(url: str, timeout: int = 10) -> dict[str, Any]:
    """Return a summary dict of the HEAD response (no body)."""

    if not HAS_REQUESTS:
        return {"ok": False, "status_code": None, "error": "requests unavailable"}
    try:
        resp = requests.head(
            url, headers=_headers(), timeout=timeout, allow_redirects=True
        )
        return {
            "ok": 200 <= resp.status_code < 300,
            "status_code": resp.status_code,
            "content_type": resp.headers.get("Content-Type"),
            "content_length": resp.headers.get("Content-Length"),
            "final_url": resp.url,
            "error": None,
        }
    except requests.RequestException as exc:
        return {"ok": False, "status_code": None, "error": str(exc)}


def fetch(url: str, dest_path, timeout: int = DEFAULT_TIMEOUT) -> dict[str, Any]:
    """Download ``url`` to ``dest_path``.

    Returns a dict with ``ok``, ``status_code``, ``bytes``, ``content_type``,
    ``final_url``, ``error``. Does a best-effort retry loop.
    """

    if not HAS_REQUESTS:
        return {
            "ok": False,
            "status_code": None,
            "bytes": 0,
            "error": "requests not installed",
        }

    last_err: str | None = None
    last_status: int | None = None
    for attempt in range(MAX_RETRIES):
        try:
            resp = requests.get(
                url,
                headers=_headers(),
                timeout=timeout,
                stream=True,
                allow_redirects=True,
            )
            last_status = resp.status_code
            if resp.status_code == 429:
                retry_after = resp.headers.get("Retry-After")
                try:
                    wait = float(retry_after) if retry_after else 5.0 * (attempt + 1)
                except ValueError:
                    wait = 5.0 * (attempt + 1)
                time.sleep(min(wait, 30.0))
                continue
            if resp.status_code >= 400:
                last_err = f"HTTP {resp.status_code}"
                break
            total = 0
            with open(dest_path, "wb") as fh:
                for chunk in resp.iter_content(chunk_size=1 << 15):
                    if not chunk:
                        continue
                    fh.write(chunk)
                    total += len(chunk)
            return {
                "ok": True,
                "status_code": resp.status_code,
                "bytes": total,
                "content_type": resp.headers.get("Content-Type"),
                "final_url": resp.url,
                "error": None,
            }
        except requests.RequestException as exc:
            last_err = str(exc)
            time.sleep(2.0 * (attempt + 1))
    return {
        "ok": False,
        "status_code": last_status,
        "bytes": 0,
        "content_type": None,
        "final_url": url,
        "error": last_err or "exhausted retries",
    }
