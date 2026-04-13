"""Headless-browser fallback for JS-heavy catalogs.

Soft-imports Playwright. If the library or its chromium binary is not
installed, the ``fetch`` function returns a result describing the
unavailability so the caller can mark the item for manual intervention.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

try:
    from playwright.sync_api import sync_playwright  # type: ignore[import]

    HAS_PLAYWRIGHT = True
except Exception:  # broad except: catches missing dep + missing binary
    HAS_PLAYWRIGHT = False

from .. import USER_AGENT

PLAYWRIGHT_TIMEOUT_MS = 45_000


def fetch(source_url: str, dest_path: Path) -> dict[str, Any]:
    """Load ``source_url`` in headless Chromium and save the largest image."""

    if not HAS_PLAYWRIGHT:
        return {
            "ok": False,
            "status_code": None,
            "bytes": 0,
            "error": "playwright_unavailable",
            "content_type": None,
            "final_url": source_url,
        }

    try:  # pragma: no cover - requires chromium binary
        with sync_playwright() as pw:
            browser = pw.chromium.launch(headless=True)
            context = browser.new_context(user_agent=USER_AGENT)
            page = context.new_page()
            page.set_default_timeout(PLAYWRIGHT_TIMEOUT_MS)
            try:
                page.goto(source_url, wait_until="networkidle")
            except Exception as exc:  # timeout or nav error
                browser.close()
                return {
                    "ok": False,
                    "status_code": None,
                    "bytes": 0,
                    "error": f"playwright_nav: {exc}",
                    "content_type": None,
                    "final_url": source_url,
                }

            # Find the largest <img> on the page.
            candidates = page.evaluate(
                """() => {
                    return [...document.querySelectorAll('img')]
                        .map(img => ({
                            src: img.currentSrc || img.src,
                            w: img.naturalWidth || 0,
                            h: img.naturalHeight || 0
                        }))
                        .filter(c => c.src && c.w >= 200 && c.h >= 200)
                        .sort((a, b) => (b.w * b.h) - (a.w * a.h));
                }"""
            )

            if not candidates:
                # Fallback: screenshot main content.
                page.screenshot(path=str(dest_path), full_page=False)
                size = Path(dest_path).stat().st_size
                browser.close()
                return {
                    "ok": True,
                    "status_code": 200,
                    "bytes": size,
                    "content_type": "image/png",
                    "final_url": source_url,
                    "fetched_url": source_url,
                    "note": "screenshot_fallback",
                    "error": None,
                }

            target = candidates[0]["src"]
            try:
                resp = context.request.get(target, timeout=PLAYWRIGHT_TIMEOUT_MS)
                if resp.ok:
                    Path(dest_path).write_bytes(resp.body())
                    size = Path(dest_path).stat().st_size
                    content_type = resp.headers.get("content-type")
                    browser.close()
                    return {
                        "ok": True,
                        "status_code": resp.status,
                        "bytes": size,
                        "content_type": content_type,
                        "final_url": source_url,
                        "fetched_url": target,
                        "error": None,
                    }
                browser.close()
                return {
                    "ok": False,
                    "status_code": resp.status,
                    "bytes": 0,
                    "error": f"playwright_image_http_{resp.status}",
                    "content_type": None,
                    "final_url": source_url,
                    "fetched_url": target,
                }
            except Exception as exc:
                browser.close()
                return {
                    "ok": False,
                    "status_code": None,
                    "bytes": 0,
                    "error": f"playwright_download: {exc}",
                    "content_type": None,
                    "final_url": source_url,
                    "fetched_url": target,
                }
    except Exception as exc:
        return {
            "ok": False,
            "status_code": None,
            "bytes": 0,
            "error": f"playwright_launch: {exc}",
            "content_type": None,
            "final_url": source_url,
        }
