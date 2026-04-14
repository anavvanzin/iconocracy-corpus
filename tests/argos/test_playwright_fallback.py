import tempfile
import unittest
from pathlib import Path
from unittest import mock

from tools.argos.protocols.playwright_fallback import fetch_with_playwright, playwright_available


class _FakeResponse:
    def __init__(self, status=200):
        self.status = status


class _FakePage:
    def __init__(self, payload=b"playwright-fallback-image", status=200):
        self.payload = payload
        self.status = status
        self.goto_calls = []
        self.screenshot_calls = []

    def goto(self, url, wait_until=None, timeout=None):
        self.goto_calls.append({"url": url, "wait_until": wait_until, "timeout": timeout})
        return _FakeResponse(status=self.status)

    def screenshot(self, path, full_page=True):
        self.screenshot_calls.append({"path": path, "full_page": full_page})
        Path(path).write_bytes(self.payload)


class _EmptyCapturePage(_FakePage):
    def screenshot(self, path, full_page=True):
        self.screenshot_calls.append({"path": path, "full_page": full_page})
        Path(path).touch()


class _FakeBrowser:
    def __init__(self, page):
        self.page = page
        self.closed = False

    def new_page(self):
        return self.page

    def close(self):
        self.closed = True


class _FakeChromium:
    def __init__(self, browser):
        self.browser = browser
        self.launch_calls = []

    def launch(self, headless=True):
        self.launch_calls.append({"headless": headless})
        return self.browser


class _FakePlaywrightContext:
    def __init__(self, page):
        self.browser = _FakeBrowser(page)
        self.chromium = _FakeChromium(self.browser)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc, tb):
        return False


class PlaywrightFallbackTests(unittest.TestCase):
    def test_playwright_available_returns_false_when_module_missing(self):
        with mock.patch(
            "tools.argos.protocols.playwright_fallback.importlib.import_module",
            side_effect=ImportError("missing playwright"),
        ):
            self.assertFalse(playwright_available())

    def test_fetch_with_playwright_returns_manual_for_restricted_domain_by_default(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            dest_path = Path(tmpdir) / "numista.png"
            result = fetch_with_playwright("https://en.numista.com/catalogue/piece123.html", dest_path)

        self.assertFalse(result["success"])
        self.assertTrue(result["manual_required"])
        self.assertEqual(result["failure_class"], "manual_required")
        self.assertEqual(result["source_domain"], "en.numista.com")
        self.assertIn("explicitly allowed", result["error"])

    def test_fetch_with_playwright_treats_restricted_domain_with_port_as_restricted_by_default(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            dest_path = Path(tmpdir) / "numista-port.png"
            result = fetch_with_playwright("https://en.numista.com:8443/catalogue/piece123.html", dest_path)

        self.assertFalse(result["success"])
        self.assertTrue(result["manual_required"])
        self.assertEqual(result["failure_class"], "manual_required")
        self.assertEqual(result["source_domain"], "en.numista.com")
        self.assertIn("numista.com", result["notes"][0])

    def test_fetch_with_playwright_returns_unavailable_failure_when_dependency_missing(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            dest_path = Path(tmpdir) / "fallback.png"
            with mock.patch(
                "tools.argos.protocols.playwright_fallback.importlib.import_module",
                side_effect=ImportError("missing playwright"),
            ):
                result = fetch_with_playwright("https://example.com/object/1", dest_path, playwright_allowed=True)

        self.assertFalse(result["success"])
        self.assertTrue(result["manual_required"])
        self.assertEqual(result["failure_class"], "playwright_unavailable")
        self.assertEqual(result["protocol"], "playwright")
        self.assertFalse(dest_path.exists())

    def test_fetch_with_playwright_uses_browser_factory_when_allowed(self):
        page = _FakePage(payload=b"x" * 1024, status=202)

        with tempfile.TemporaryDirectory() as tmpdir:
            dest_path = Path(tmpdir) / "fallback.png"
            result = fetch_with_playwright(
                "https://example.com/object/1",
                dest_path,
                playwright_allowed=True,
                timeout=12,
                browser_factory=lambda: _FakePlaywrightContext(page),
            )

            written = dest_path.read_bytes()

        self.assertTrue(result["success"])
        self.assertEqual(result["bytes_written"], 1024)
        self.assertEqual(result["status_code"], 202)
        self.assertEqual(result["source_url"], "https://example.com/object/1")
        self.assertEqual(page.goto_calls[0]["wait_until"], "networkidle")
        self.assertEqual(page.goto_calls[0]["timeout"], 12000)
        self.assertEqual(written, b"x" * 1024)

    def test_fetch_with_playwright_allows_restricted_domain_when_explicitly_enabled(self):
        page = _FakePage(payload=b"restricted-ok", status=203)

        with tempfile.TemporaryDirectory() as tmpdir:
            dest_path = Path(tmpdir) / "restricted.png"
            result = fetch_with_playwright(
                "https://colnect.com/en/coins/item/1",
                dest_path,
                playwright_allowed=True,
                browser_factory=lambda: _FakePlaywrightContext(page),
            )

            written = dest_path.read_bytes()

        self.assertTrue(result["success"])
        self.assertEqual(result["status_code"], 203)
        self.assertEqual(result["source_domain"], "colnect.com")
        self.assertEqual(written, b"restricted-ok")

    def test_fetch_with_playwright_cleans_up_empty_capture_output(self):
        page = _EmptyCapturePage()

        with tempfile.TemporaryDirectory() as tmpdir:
            dest_path = Path(tmpdir) / "empty.png"
            result = fetch_with_playwright(
                "https://example.com/object/empty",
                dest_path,
                playwright_allowed=True,
                browser_factory=lambda: _FakePlaywrightContext(page),
            )

            exists_after = dest_path.exists()

        self.assertFalse(result["success"])
        self.assertEqual(result["failure_class"], "playwright_empty_capture")
        self.assertFalse(exists_after)


if __name__ == "__main__":
    unittest.main()
