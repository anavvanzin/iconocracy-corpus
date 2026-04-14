from __future__ import annotations

import importlib
from pathlib import Path
from urllib.parse import urlparse


RESTRICTED_DOMAINS = {
    "numista.com",
    "colnect.com",
}


def _source_domain(url: str) -> str:
    return urlparse(url).netloc.lower()


def _restricted_domain(domain: str) -> str | None:
    for restricted in RESTRICTED_DOMAINS:
        if domain == restricted or domain.endswith(f".{restricted}"):
            return restricted
    return None


def _result(dest_path: Path, **extra) -> dict:
    payload = {
        "success": False,
        "protocol": "playwright",
        "dest_path": str(dest_path),
        "bytes_written": 0,
        "status_code": None,
        "failure_class": None,
        "error": None,
        "manual_required": False,
        "source_url": None,
        "source_domain": None,
        "notes": [],
    }
    payload.update(extra)
    return payload


def _load_playwright_module():
    return importlib.import_module("playwright.sync_api")


def playwright_available() -> bool:
    try:
        _load_playwright_module()
    except ImportError:
        return False
    return True


def _default_browser_factory():
    sync_api = _load_playwright_module()
    return sync_api.sync_playwright()


def fetch_with_playwright(
    url: str,
    dest_path: Path,
    *,
    timeout: int = 30,
    playwright_allowed: bool = False,
    headless: bool = True,
    browser_factory=None,
) -> dict:
    """Capture a modest Playwright fallback screenshot when explicitly allowed."""

    dest_path = Path(dest_path)
    dest_path.parent.mkdir(parents=True, exist_ok=True)
    domain = _source_domain(url)
    restricted = _restricted_domain(domain)

    if restricted and not playwright_allowed:
        dest_path.unlink(missing_ok=True)
        return _result(
            dest_path,
            failure_class="manual_required",
            error=f"Playwright fallback for {restricted} requires manual review unless explicitly allowed",
            manual_required=True,
            source_url=url,
            source_domain=domain,
            notes=[f"Restricted domain policy matched: {restricted}"],
        )

    factory = browser_factory or _default_browser_factory
    try:
        context_manager = factory()
    except ImportError:
        dest_path.unlink(missing_ok=True)
        return _result(
            dest_path,
            failure_class="playwright_unavailable",
            error="Playwright is not installed in this environment",
            manual_required=True,
            source_url=url,
            source_domain=domain,
            notes=["Optional dependency playwright.sync_api is unavailable"],
        )

    browser = None
    try:
        with context_manager as playwright:
            browser = playwright.chromium.launch(headless=headless)
            page = browser.new_page()
            response = page.goto(url, wait_until="networkidle", timeout=timeout * 1000)
            page.screenshot(path=str(dest_path), full_page=True)

        bytes_written = dest_path.stat().st_size if dest_path.exists() else 0
        if bytes_written <= 0:
            dest_path.unlink(missing_ok=True)
            return _result(
                dest_path,
                failure_class="playwright_empty_capture",
                error="Playwright completed without writing output",
                source_url=url,
                source_domain=domain,
            )

        return _result(
            dest_path,
            success=True,
            bytes_written=bytes_written,
            status_code=getattr(response, "status", None),
            source_url=url,
            source_domain=domain,
        )
    except Exception as error:
        dest_path.unlink(missing_ok=True)
        return _result(
            dest_path,
            failure_class="playwright_error",
            error=str(error),
            source_url=url,
            source_domain=domain,
        )
    finally:
        if browser is not None:
            try:
                browser.close()
            except Exception:
                pass
