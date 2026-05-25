import tempfile
import unittest
import urllib.error
from email.message import Message
from pathlib import Path
from unittest import mock

from tools.argos.protocols.direct import classify_http_failure, fetch_direct
from tools.argos.protocols.iiif import discover_iiif, fetch_iiif_image, gallica_manifest_from_ark


class FakeResponse:
    def __init__(self, payload: bytes, content_type: str = "image/jpeg"):
        self.payload = payload
        self.offset = 0
        self.headers = Message()
        self.headers["Content-Type"] = content_type

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc, tb):
        return False

    def read(self, size: int = -1) -> bytes:
        if self.offset >= len(self.payload):
            return b""
        if size < 0:
            size = len(self.payload) - self.offset
        chunk = self.payload[self.offset : self.offset + size]
        self.offset += len(chunk)
        return chunk


class ProtocolCoreTests(unittest.TestCase):
    def test_gallica_manifest_from_ark(self):
        manifest_url = gallica_manifest_from_ark("ark:/12148/btv1b12345")

        self.assertTrue(manifest_url.endswith("manifest.json"))
        self.assertIn("ark:/12148/btv1b12345", manifest_url)

    def test_403_maps_to_blocked_failure(self):
        self.assertEqual(classify_http_failure(403), "403_block")

    def test_500_maps_to_upstream_failure(self):
        self.assertEqual(classify_http_failure(500), "5xx_upstream")

    def test_discover_iiif_from_gallica_item(self):
        item = {"url": "https://gallica.bnf.fr/ark:/12148/btv1b12345"}

        discovered = discover_iiif(item)

        self.assertEqual(discovered["iiif_source"], "gallica")
        self.assertTrue(discovered["manifest_url"].endswith("manifest.json"))
        self.assertIn("/f1/full/full/0/native.jpg", discovered["image_url"])

    def test_discover_iiif_from_europeana_item_path(self):
        item = {"url": "https://www.europeana.eu/en/item/9200519/ark__12148_btv1b10526007b"}

        discovered = discover_iiif(item)

        self.assertEqual(discovered["iiif_source"], "europeana_gallica")
        self.assertIn("ark:/12148/btv1b10526007b", discovered["manifest_url"])
        self.assertIn("/f1/full/full/0/native.jpg", discovered["image_url"])

    def test_discover_iiif_returns_none_when_no_known_pattern_matches(self):
        self.assertIsNone(discover_iiif({"url": "https://example.com/object/123"}))

    def test_fetch_direct_retries_retryable_http_error_and_succeeds(self):
        payload = b"x" * 800
        http_error = urllib.error.HTTPError(
            "https://example.com/image.jpg",
            500,
            "Server Error",
            hdrs=Message(),
            fp=None,
        )
        success_response = FakeResponse(payload)

        with tempfile.TemporaryDirectory() as tmpdir:
            dest_path = Path(tmpdir) / "image.jpg"
            with mock.patch(
                "tools.argos.protocols.direct.urllib.request.urlopen",
                side_effect=[http_error, success_response],
            ) as mocked_urlopen, mock.patch("tools.argos.protocols.direct.time.sleep") as mocked_sleep:
                result = fetch_direct("https://example.com/image.jpg", dest_path, retries=2)

        self.assertTrue(result["success"])
        self.assertEqual(result["bytes_written"], len(payload))
        self.assertEqual(result["ssl_verification"], "verified")
        mocked_sleep.assert_called_once()
        self.assertEqual(mocked_urlopen.call_count, 2)

    def test_fetch_iiif_image_returns_expected_failure_when_no_pattern_matches(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            dest_path = Path(tmpdir) / "missing.jpg"
            result = fetch_iiif_image({"url": "https://example.com/object/123"}, dest_path)

        self.assertFalse(result["success"])
        self.assertEqual(result["failure_class"], "iiif_unavailable")
        self.assertIn("No supported IIIF pattern discovered", result["error"])


if __name__ == "__main__":
    unittest.main()
