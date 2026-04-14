import hashlib
import importlib.util
import io
import json
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock


def load_module(relative_path: str, module_name: str):
    repo_root = Path(__file__).resolve().parents[2]
    script_path = repo_root / relative_path
    spec = importlib.util.spec_from_file_location(module_name, script_path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


class AcquireItemTests(unittest.TestCase):
    def setUp(self):
        self.repo_root = Path(__file__).resolve().parents[2]
        self.worker = load_module("tools/scripts/argos_acquire_item.py", "tests.argos._argos_acquire_item")
        self.log_agent_run = load_module("tools/scripts/log_agent_run.py", "tests.argos._log_agent_run")

    def make_manifest(self):
        return {
            "manifest_version": "1.0",
            "generated_at": "2026-04-13T20:12:00Z",
            "storage_root": "/Volumes/ICONOCRACIA/argos",
            "storage_tier": "ssd",
            "summary": {
                "total_items": 1,
                "pending": 1,
                "success": 0,
                "partial": 0,
                "failed": 0,
                "manual": 0,
            },
            "items": [
                {
                    "item_id": "FR-013",
                    "title": "République",
                    "source_url": "https://example.com/image.jpg",
                    "source_domain": "example.com",
                    "protocol": "direct",
                    "status": "pending",
                    "failure_class": "",
                    "failure_reason": "",
                    "attempts": 0,
                    "local_path": "",
                    "sha256": "",
                    "provenance": {
                        "agent": "argos",
                        "method": "direct",
                        "metadata": {"dispatch_group": "example.com"},
                    },
                }
            ],
        }

    def test_403_moves_to_iiif_discovery(self):
        attempt = {"status_code": 403, "failure_class": "403_block"}
        self.assertEqual(self.worker.infer_next_step(protocol="direct", last_attempt=attempt), "iiif-discovery")

    def test_infer_next_step_moves_from_iiif_to_playwright_when_still_blocked(self):
        attempt = {"status_code": 429, "failure_class": "429_rate_limited"}
        self.assertEqual(self.worker.infer_next_step(protocol="iiif", last_attempt=attempt), "playwright-fallback")

    def test_dry_run_prints_attempt_plan_and_does_not_mutate_manifest(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            tmp_path = Path(tmp_dir)
            manifest_path = tmp_path / "manifest.json"
            original_manifest = self.make_manifest()
            manifest_path.write_text(json.dumps(original_manifest), encoding="utf-8")

            argv = [
                "argos_acquire_item.py",
                "--manifest",
                str(manifest_path),
                "--item-id",
                "FR-013",
                "--dry-run",
            ]
            stdout = io.StringIO()
            with mock.patch.object(sys, "argv", argv), mock.patch("sys.stdout", stdout), mock.patch.object(
                self.worker, "resolve_storage_root", return_value=(tmp_path / "storage", "repo-staging")
            ):
                exit_code = self.worker.main()

            self.assertEqual(exit_code, 0)
            output = stdout.getvalue()
            self.assertIn("Dry run for FR-013", output)
            self.assertIn("1. direct", output)
            self.assertIn("2. iiif-discovery-on-block", output)
            self.assertIn("3. playwright-fallback-when-allowed", output)
            self.assertEqual(json.loads(manifest_path.read_text(encoding="utf-8")), original_manifest)

    def test_successful_acquisition_writes_sidecar_updates_manifest_and_logs_argos(self):
        payload = b"image-bytes-for-argos" * 40
        expected_sha = hashlib.sha256(payload).hexdigest()

        with tempfile.TemporaryDirectory() as tmp_dir:
            tmp_path = Path(tmp_dir)
            manifest_path = tmp_path / "manifest.json"
            manifest_path.write_text(json.dumps(self.make_manifest()), encoding="utf-8")
            storage_root = tmp_path / "storage"
            storage_root.mkdir()

            logged_runs = []

            def fake_log_run(**kwargs):
                logged_runs.append(kwargs)
                return kwargs

            def fake_fetch_direct(url, dest_path):
                Path(dest_path).parent.mkdir(parents=True, exist_ok=True)
                Path(dest_path).write_bytes(payload)
                return {
                    "success": True,
                    "protocol": "direct",
                    "dest_path": str(dest_path),
                    "bytes_written": len(payload),
                    "status_code": 200,
                    "source_url": url,
                    "source_domain": "example.com",
                    "notes": [],
                }

            with mock.patch.object(self.worker, "resolve_storage_root", return_value=(storage_root, "repo-staging")), mock.patch.object(
                self.worker,
                "fetch_direct",
                side_effect=fake_fetch_direct,
            ), mock.patch.object(self.worker, "discover_iiif", return_value=None), mock.patch.object(
                self.worker, "fetch_iiif_image"
            ) as iiif_mock, mock.patch.object(self.worker, "fetch_with_playwright") as playwright_mock, mock.patch.object(
                self.worker, "log_run", side_effect=fake_log_run
            ):
                result = self.worker.acquire_item(manifest_path=manifest_path, item_id="FR-013")

            item_dir = storage_root / "repo-staging"
            asset_path = item_dir / "FR-013.jpg"
            sidecar_path = item_dir / "FR-013.meta.json"
            self.assertEqual(result["status"], "success")
            self.assertTrue(asset_path.exists())
            self.assertEqual(asset_path.read_bytes(), payload)
            self.assertTrue(sidecar_path.exists())
            sidecar = json.loads(sidecar_path.read_text(encoding="utf-8"))
            self.assertEqual(sidecar["item_id"], "FR-013")
            self.assertEqual(sidecar["sha256"], expected_sha)
            manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
            item = manifest["items"][0]
            self.assertEqual(item["status"], "success")
            self.assertEqual(item["sha256"], expected_sha)
            self.assertEqual(item["attempts"], 1)
            self.assertEqual(item["local_path"], str(asset_path))
            self.assertEqual(manifest["summary"]["success"], 1)
            self.assertEqual(manifest["summary"]["pending"], 0)
            self.assertEqual(len(logged_runs), 1)
            self.assertEqual(logged_runs[0]["agent"], "argos")
            self.assertEqual(logged_runs[0]["status"], "success")
            iiif_mock.assert_not_called()
            playwright_mock.assert_not_called()

    def test_blocked_direct_attempt_falls_through_iiif_discovery_to_playwright_when_allowed(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            tmp_path = Path(tmp_dir)
            manifest_path = tmp_path / "manifest.json"
            manifest_path.write_text(json.dumps(self.make_manifest()), encoding="utf-8")
            storage_root = tmp_path / "storage"
            storage_root.mkdir()

            payload = b"playwright-fallback" * 80

            def fake_playwright(url, dest_path, playwright_allowed):
                Path(dest_path).parent.mkdir(parents=True, exist_ok=True)
                Path(dest_path).write_bytes(payload)
                return {
                    "success": True,
                    "protocol": "playwright",
                    "dest_path": str(dest_path),
                    "bytes_written": len(payload),
                    "status_code": 200,
                    "source_url": url,
                    "source_domain": "example.com",
                    "notes": ["fallback screenshot"],
                }

            with mock.patch.object(self.worker, "resolve_storage_root", return_value=(storage_root, "repo-staging")), mock.patch.object(
                self.worker,
                "fetch_direct",
                return_value={
                    "success": False,
                    "protocol": "direct",
                    "dest_path": str(storage_root / "repo-staging" / "FR-013.jpg"),
                    "bytes_written": 0,
                    "status_code": 403,
                    "failure_class": "403_block",
                    "error": "HTTP 403: Forbidden",
                    "notes": [],
                },
            ) as direct_mock, mock.patch.object(self.worker, "discover_iiif", return_value=None) as discover_mock, mock.patch.object(
                self.worker, "fetch_iiif_image"
            ) as iiif_mock, mock.patch.object(
                self.worker, "fetch_with_playwright", side_effect=fake_playwright
            ) as playwright_mock, mock.patch.object(self.worker, "log_run"):
                result = self.worker.acquire_item(
                    manifest_path=manifest_path,
                    item_id="FR-013",
                    playwright_allowed=True,
                )

            self.assertEqual(result["status"], "success")
            self.assertEqual([attempt["step"] for attempt in result["attempts"]], ["direct", "iiif", "playwright"])
            direct_mock.assert_called_once()
            discover_mock.assert_called_once_with(
                {
                    "item_id": "FR-013",
                    "title": "République",
                    "source_url": "https://example.com/image.jpg",
                    "source_domain": "example.com",
                    "protocol": "direct",
                    "status": "pending",
                    "failure_class": "",
                    "failure_reason": "",
                    "attempts": 0,
                    "local_path": "",
                    "sha256": "",
                    "provenance": {
                        "agent": "argos",
                        "method": "direct",
                        "metadata": {"dispatch_group": "example.com"},
                    },
                    "url": "https://example.com/image.jpg",
                }
            )
            iiif_mock.assert_not_called()
            playwright_mock.assert_called_once()
            self.assertEqual(result["attempts"][1]["failure_class"], "iiif_unavailable")
            manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
            self.assertEqual(manifest["items"][0]["status"], "success")
            self.assertEqual(manifest["items"][0]["attempts"], 3)

    def test_blocked_direct_attempt_tries_iiif_fetch_before_playwright_when_discovery_succeeds_but_fetch_fails(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            tmp_path = Path(tmp_dir)
            manifest_path = tmp_path / "manifest.json"
            manifest_path.write_text(json.dumps(self.make_manifest()), encoding="utf-8")
            storage_root = tmp_path / "storage"
            storage_root.mkdir()

            payload = b"playwright-after-iiif" * 70

            def fake_playwright(url, dest_path, playwright_allowed):
                Path(dest_path).parent.mkdir(parents=True, exist_ok=True)
                Path(dest_path).write_bytes(payload)
                return {
                    "success": True,
                    "protocol": "playwright",
                    "dest_path": str(dest_path),
                    "bytes_written": len(payload),
                    "status_code": 200,
                    "source_url": url,
                    "source_domain": "example.com",
                    "notes": [],
                }

            with mock.patch.object(self.worker, "resolve_storage_root", return_value=(storage_root, "repo-staging")), mock.patch.object(
                self.worker,
                "fetch_direct",
                return_value={
                    "success": False,
                    "protocol": "direct",
                    "dest_path": str(storage_root / "repo-staging" / "FR-013.jpg"),
                    "bytes_written": 0,
                    "status_code": 429,
                    "failure_class": "429_rate_limited",
                    "error": "HTTP 429: Too Many Requests",
                    "notes": [],
                },
            ), mock.patch.object(
                self.worker,
                "discover_iiif",
                return_value={
                    "iiif_source": "gallica",
                    "manifest_url": "https://gallica.bnf.fr/iiif/ark:/12148/foo/manifest.json",
                    "image_url": "https://gallica.bnf.fr/iiif/ark:/12148/foo/f1/full/full/0/native.jpg",
                },
            ) as discover_mock, mock.patch.object(
                self.worker,
                "fetch_iiif_image",
                return_value={
                    "success": False,
                    "protocol": "iiif",
                    "dest_path": str(storage_root / "repo-staging" / "FR-013.jpg"),
                    "bytes_written": 0,
                    "status_code": 403,
                    "failure_class": "403_block",
                    "error": "HTTP 403: Forbidden",
                    "notes": [],
                },
            ) as iiif_mock, mock.patch.object(
                self.worker, "fetch_with_playwright", side_effect=fake_playwright
            ) as playwright_mock, mock.patch.object(self.worker, "log_run"):
                result = self.worker.acquire_item(
                    manifest_path=manifest_path,
                    item_id="FR-013",
                    playwright_allowed=True,
                )

            self.assertEqual(result["status"], "success")
            self.assertEqual([attempt["step"] for attempt in result["attempts"]], ["direct", "iiif", "playwright"])
            discover_mock.assert_called_once()
            iiif_mock.assert_called_once()
            iiif_item = iiif_mock.call_args.args[0]
            self.assertEqual(iiif_item["url"], "https://example.com/image.jpg")
            self.assertEqual(iiif_item["source_url"], "https://example.com/image.jpg")
            playwright_mock.assert_called_once()

    def test_log_agent_run_accepts_argos_choice(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            runs_path = Path(tmp_dir) / "agent-runs.json"
            argv = [
                "log_agent_run.py",
                "--agent",
                "argos",
                "--status",
                "success",
                "--items",
                "1",
                "--duration",
                "2",
                "--details",
                "worker ok",
            ]
            stdout = io.StringIO()
            with mock.patch.object(sys, "argv", argv), mock.patch("sys.stdout", stdout), mock.patch.object(
                self.log_agent_run, "RUNS_FILE", str(runs_path)
            ):
                self.log_agent_run.main()

            logged = json.loads(runs_path.read_text(encoding="utf-8"))
            self.assertEqual(logged[0]["agent"], "argos")
            self.assertIn("Logged: argos [success]", stdout.getvalue())


if __name__ == "__main__":
    unittest.main()
