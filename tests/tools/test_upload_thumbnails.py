from __future__ import annotations

import ssl
import tempfile
import unittest
from pathlib import Path
from unittest import mock

from tools.scripts import upload_thumbnails


class _FakeResponse:
    def __init__(self, payload: bytes, status: int = 200, content_type: str = "image/png"):
        self._payload = payload
        self.status = status
        self.headers = {"Content-Type": content_type}

    def read(self) -> bytes:
        return self._payload

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc, tb):
        return False


class UploadThumbnailsTests(unittest.TestCase):
    @staticmethod
    def _path_exists_without_deploy_sync(path_obj):
        if str(path_obj).endswith("/deploy/iconocracia-companion/public/analytics.html"):
            return False
        return Path.is_file(path_obj) or Path.is_dir(path_obj)

    def test_clean_url_strips_query_and_normalizes_wikimedia_and_numista(self):
        wiki = "https://commons.wikimedia.org/thumb/a/b/file.jpg/120px-file.jpg?foo=1"
        numista = "https://en.numista.com/catalogue/photos/thumbs/123_456/abc.jpg?bar=2"

        self.assertEqual(
            upload_thumbnails.clean_url(wiki),
            "https://commons.wikimedia.org/a/b/file.jpg/120px-file.jpg",
        )
        self.assertEqual(
            upload_thumbnails.clean_url(numista),
            "https://en.numista.com/catalogue/photos/images/abc.jpg",
        )

    def test_fetch_image_bytes_uses_ssl_fallback_when_cert_verification_fails(self):
        payload = b"image-bytes"

        with mock.patch(
            "tools.scripts.upload_thumbnails.urllib.request.urlopen",
            side_effect=[
                ssl.SSLCertVerificationError("bad cert"),
                _FakeResponse(payload),
            ],
        ) as urlopen_mock:
            result = upload_thumbnails.fetch_image_bytes("https://example.com/img.png")

        self.assertEqual(result, payload)
        self.assertEqual(urlopen_mock.call_count, 2)
        self.assertIn("context", urlopen_mock.call_args_list[1].kwargs)

    def test_upload_to_r2_requires_credentials(self):
        with mock.patch.dict("os.environ", {}, clear=True):
            self.assertIsNone(upload_thumbnails.upload_to_r2(b"thumb", "A-1-thumb.webp"))

    def test_upload_to_r2_returns_public_path_on_success(self):
        with mock.patch.dict(
            "os.environ",
            {"R2_ACCOUNT_ID": "acct", "CLOUDFLARE_API_TOKEN": "token", "R2_BUCKET": "bucket"},
            clear=True,
        ), mock.patch(
            "tools.scripts.upload_thumbnails.urllib.request.urlopen",
            return_value=_FakeResponse(b"", status=201),
        ):
            result = upload_thumbnails.upload_to_r2(b"thumb", "A-1-thumb.webp")

        self.assertEqual(result, "/images/A-1-thumb.webp")

    def test_write_analytics_data_replaces_only_data_block(self):
        original = (
            "prefix\n"
            "const DATA = [\n"
            "{\"id\":\"old\"}\n"
            "];\n\n"
            "const CORES = [\"x\"];\n"
            "suffix\n"
        )
        with tempfile.TemporaryDirectory() as tmp_dir:
            html_path = Path(tmp_dir) / "analytics.html"
            html_path.write_text(original, encoding="utf-8")

            upload_thumbnails.write_analytics_data(html_path, [{"id": "NEW-1", "thumbnail_url": "thumb.webp"}])
            content = html_path.read_text(encoding="utf-8")

        self.assertIn("prefix\n", content)
        self.assertIn('"id": "NEW-1"', content)
        self.assertIn("const CORES = [\"x\"];", content)
        self.assertIn("suffix\n", content)
        self.assertNotIn('"id":"old"', content)

    def test_main_updates_existing_local_thumbnail_url_and_writes_file(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            base = Path(tmp_dir)
            analytics = base / "analytics.html"
            analytics.write_text("const DATA = []\nconst CORES = []", encoding="utf-8")
            thumbs = base / "thumbnails"
            thumbs.mkdir()
            local_thumb = thumbs / "BR-001-thumb.webp"
            local_thumb.write_bytes(b"existing")
            item = {"id": "BR-001", "url": "https://example.com/a.png", "thumbnail_url": ""}

            with mock.patch("tools.scripts.upload_thumbnails.ANALYTICS_HTML", analytics), mock.patch(
                "tools.scripts.upload_thumbnails.THUMBNAILS_DIR", thumbs
            ), mock.patch(
                "tools.scripts.upload_thumbnails.parse_analytics_data",
                return_value=[item],
            ), mock.patch(
                "pathlib.Path.exists",
                autospec=True,
                side_effect=self._path_exists_without_deploy_sync,
            ), mock.patch(
                "tools.scripts.upload_thumbnails.write_analytics_data"
            ) as write_mock, mock.patch(
                "tools.scripts.upload_thumbnails.sys.argv",
                ["upload_thumbnails.py", "--limit", "5"],
            ), mock.patch(
                "tools.scripts.upload_thumbnails.fetch_image_bytes"
            ) as fetch_mock:
                upload_thumbnails.main()

        self.assertEqual(item["thumbnail_url"], "thumbnails/BR-001-thumb.webp")
        fetch_mock.assert_not_called()
        write_mock.assert_called_once()

    def test_main_uses_r2_url_when_enabled_and_upload_succeeds(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            base = Path(tmp_dir)
            analytics = base / "analytics.html"
            analytics.write_text("const DATA = []\nconst CORES = []", encoding="utf-8")
            thumbs = base / "thumbnails"
            thumbs.mkdir()
            item = {"id": "FR-002", "url": "https://example.com/b.png", "thumbnail_url": ""}

            with mock.patch.dict("os.environ", {"CLOUDFLARE_API_TOKEN": "token"}, clear=False), mock.patch(
                "tools.scripts.upload_thumbnails.ANALYTICS_HTML", analytics
            ), mock.patch(
                "tools.scripts.upload_thumbnails.THUMBNAILS_DIR", thumbs
            ), mock.patch(
                "tools.scripts.upload_thumbnails.parse_analytics_data",
                return_value=[item],
            ), mock.patch(
                "tools.scripts.upload_thumbnails.fetch_image_bytes",
                return_value=b"img",
            ), mock.patch(
                "tools.scripts.upload_thumbnails.make_thumbnail",
                return_value=b"thumb",
            ), mock.patch(
                "tools.scripts.upload_thumbnails.upload_to_r2",
                return_value="/images/FR-002-thumb.webp",
            ) as upload_mock, mock.patch(
                "pathlib.Path.exists",
                autospec=True,
                side_effect=self._path_exists_without_deploy_sync,
            ), mock.patch(
                "tools.scripts.upload_thumbnails.write_analytics_data"
            ), mock.patch(
                "tools.scripts.upload_thumbnails.time.sleep"
            ), mock.patch(
                "tools.scripts.upload_thumbnails.sys.argv",
                ["upload_thumbnails.py", "--r2", "--limit", "1"],
            ):
                upload_thumbnails.main()

        self.assertEqual(item["thumbnail_url"], "/images/FR-002-thumb.webp")
        upload_mock.assert_called_once()

    def test_main_falls_back_to_local_url_when_r2_upload_fails(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            base = Path(tmp_dir)
            analytics = base / "analytics.html"
            analytics.write_text("const DATA = []\nconst CORES = []", encoding="utf-8")
            thumbs = base / "thumbnails"
            thumbs.mkdir()
            item = {"id": "US-003", "url": "https://example.com/c.png", "thumbnail_url": ""}

            with mock.patch.dict("os.environ", {"CLOUDFLARE_API_TOKEN": "token"}, clear=False), mock.patch(
                "tools.scripts.upload_thumbnails.ANALYTICS_HTML", analytics
            ), mock.patch(
                "tools.scripts.upload_thumbnails.THUMBNAILS_DIR", thumbs
            ), mock.patch(
                "tools.scripts.upload_thumbnails.parse_analytics_data",
                return_value=[item],
            ), mock.patch(
                "tools.scripts.upload_thumbnails.fetch_image_bytes",
                return_value=b"img",
            ), mock.patch(
                "tools.scripts.upload_thumbnails.make_thumbnail",
                return_value=b"thumb",
            ), mock.patch(
                "tools.scripts.upload_thumbnails.upload_to_r2",
                return_value=None,
            ), mock.patch(
                "pathlib.Path.exists",
                autospec=True,
                side_effect=self._path_exists_without_deploy_sync,
            ), mock.patch(
                "tools.scripts.upload_thumbnails.write_analytics_data"
            ), mock.patch(
                "tools.scripts.upload_thumbnails.time.sleep"
            ), mock.patch(
                "tools.scripts.upload_thumbnails.sys.argv",
                ["upload_thumbnails.py", "--r2", "--limit", "1"],
            ):
                upload_thumbnails.main()

        self.assertEqual(item["thumbnail_url"], "thumbnails/US-003-thumb.webp")


if __name__ == "__main__":
    unittest.main()
