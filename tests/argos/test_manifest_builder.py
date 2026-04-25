import importlib.util
import io
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

from tools.argos.manifest import build_manifest


def load_argos_build_manifest_module():
    repo_root = Path(__file__).resolve().parents[2]
    script_path = repo_root / "tools" / "scripts" / "argos_build_manifest.py"
    module_name = "tests.argos._argos_build_manifest"
    spec = importlib.util.spec_from_file_location(module_name, script_path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


class ManifestBuilderTests(unittest.TestCase):
    def test_build_manifest_only_includes_pending_items_with_source_metadata(self):
        corpus = [
            {
                "id": "FR-001",
                "title": "Gallica item",
                "url": "https://gallica.bnf.fr/ark:/12148/example",
                "thumbnail_url": None,
            },
            {
                "id": "UK-001",
                "title": "Already acquired",
                "url": "https://commons.wikimedia.org/wiki/File:Example.jpg",
                "thumbnail_url": "https://upload.wikimedia.org/example.jpg",
            },
            {
                "id": "NO-URL",
                "title": "Missing source URL",
                "url": None,
                "thumbnail_url": None,
            },
        ]
        drive_manifest = {"items": [{"item_id": "UK-001"}]}

        manifest = build_manifest(
            corpus,
            drive_manifest,
            storage_root="data/raw/.staging",
            storage_tier="repo-staging",
        )

        self.assertEqual(manifest["summary"]["total_items"], 1)
        self.assertEqual(manifest["summary"]["pending"], 1)
        self.assertEqual(manifest["summary"]["success"], 0)
        self.assertEqual(len(manifest["items"]), 1)

        item = manifest["items"][0]
        self.assertEqual(item["item_id"], "FR-001")
        self.assertEqual(item["status"], "pending")
        self.assertEqual(item["source_url"], corpus[0]["url"])
        self.assertEqual(item["source_domain"], "gallica.bnf.fr")
        self.assertEqual(item["protocol"], "iiif")
        self.assertEqual(item["provenance"]["agent"], "argos")
        self.assertEqual(item["provenance"]["method"], "iiif")
        self.assertEqual(
            item["provenance"]["metadata"],
            {
                "thumbnail_missing": True,
                "dispatch_group": "gallica.bnf.fr",
            },
        )

    def test_build_manifest_applies_limit_after_filtering_pending_items(self):
        corpus = [
            {
                "id": "FR-001",
                "title": "One",
                "url": "https://gallica.bnf.fr/ark:/12148/one",
                "thumbnail_url": None,
            },
            {
                "id": "AT-001",
                "title": "Two",
                "url": "https://www.loc.gov/item/two/",
                "thumbnail_url": "https://www.loc.gov/thumb/two.jpg",
            },
        ]

        manifest = build_manifest(
            corpus,
            {"items": []},
            storage_root="data/raw/.staging",
            storage_tier="repo-staging",
            limit=1,
        )

        self.assertEqual(manifest["summary"]["total_items"], 1)
        self.assertEqual([item["item_id"] for item in manifest["items"]], ["FR-001"])


class ManifestBuilderCliTests(unittest.TestCase):
    def setUp(self):
        self.repo_root = Path(__file__).resolve().parents[2]
        self.script_path = self.repo_root / "tools" / "scripts" / "argos_build_manifest.py"

    def test_cli_dry_run_reports_without_writing_output(self):
        corpus = [
            {
                "id": "FR-001",
                "title": "Gallica item",
                "url": "https://gallica.bnf.fr/ark:/12148/example",
                "thumbnail_url": None,
            }
        ]
        drive_manifest = {"items": []}

        with tempfile.TemporaryDirectory() as tmp_dir:
            tmp_path = Path(tmp_dir)
            corpus_path = tmp_path / "corpus-data.json"
            drive_manifest_path = tmp_path / "drive-manifest.json"
            output_path = tmp_path / "manifest.json"
            corpus_path.write_text(json.dumps(corpus), encoding="utf-8")
            drive_manifest_path.write_text(json.dumps(drive_manifest), encoding="utf-8")

            result = subprocess.run(
                [
                    "python",
                    str(self.script_path),
                    "--dry-run",
                    "--output",
                    str(output_path),
                    "--corpus",
                    str(corpus_path),
                    "--drive-manifest",
                    str(drive_manifest_path),
                ],
                capture_output=True,
                text=True,
                cwd=self.repo_root,
                check=False,
            )

            self.assertEqual(result.returncode, 0, result.stderr or result.stdout)
            self.assertIn("Pending items: 1", result.stdout)
            self.assertIn("iiif: 1", result.stdout)
            self.assertFalse(output_path.exists())

    def test_cli_non_dry_run_skips_write_when_no_pending_items(self):
        module = load_argos_build_manifest_module()
        corpus = [
            {
                "id": "FR-001",
                "title": "Already acquired",
                "url": "https://gallica.bnf.fr/ark:/12148/example",
                "thumbnail_url": None,
            }
        ]
        drive_manifest = {"items": [{"item_id": "FR-001"}]}

        with tempfile.TemporaryDirectory() as tmp_dir:
            tmp_path = Path(tmp_dir)
            corpus_path = tmp_path / "corpus-data.json"
            drive_manifest_path = tmp_path / "drive-manifest.json"
            output_path = tmp_path / "manifest.json"
            corpus_path.write_text(json.dumps(corpus), encoding="utf-8")
            drive_manifest_path.write_text(json.dumps(drive_manifest), encoding="utf-8")

            argv = [
                "argos_build_manifest.py",
                "--output",
                str(output_path),
                "--corpus",
                str(corpus_path),
                "--drive-manifest",
                str(drive_manifest_path),
            ]
            stdout = io.StringIO()
            with mock.patch.object(sys, "argv", argv), mock.patch("sys.stdout", stdout):
                exit_code = module.main()

            self.assertEqual(exit_code, 0)
            self.assertIn("Pending items: 0", stdout.getvalue())
            self.assertIn("No pending items remain.", stdout.getvalue())
            self.assertFalse(output_path.exists())

    def test_cli_non_dry_run_overwrites_stale_manifest_when_no_pending_items(self):
        module = load_argos_build_manifest_module()
        corpus = [
            {
                "id": "FR-001",
                "title": "Already acquired",
                "url": "https://gallica.bnf.fr/ark:/12148/example",
                "thumbnail_url": None,
            }
        ]
        drive_manifest = {"items": [{"item_id": "FR-001"}]}

        with tempfile.TemporaryDirectory() as tmp_dir:
            tmp_path = Path(tmp_dir)
            corpus_path = tmp_path / "corpus-data.json"
            drive_manifest_path = tmp_path / "drive-manifest.json"
            output_path = tmp_path / "manifest.json"
            corpus_path.write_text(json.dumps(corpus), encoding="utf-8")
            drive_manifest_path.write_text(json.dumps(drive_manifest), encoding="utf-8")
            output_path.write_text('{"stale": true}', encoding="utf-8")

            argv = [
                "argos_build_manifest.py",
                "--output",
                str(output_path),
                "--corpus",
                str(corpus_path),
                "--drive-manifest",
                str(drive_manifest_path),
            ]
            stdout = io.StringIO()
            with mock.patch.object(sys, "argv", argv), mock.patch("sys.stdout", stdout):
                exit_code = module.main()

            self.assertEqual(exit_code, 0)
            self.assertIn("overwrites stale data", stdout.getvalue())
            self.assertTrue(output_path.exists())
            written = json.loads(output_path.read_text(encoding="utf-8"))
            self.assertNotIn("stale", written)

    def test_cli_non_dry_run_writes_schema_valid_manifest_when_pending_items_exist(self):
        corpus = [
            {
                "id": "FR-001",
                "title": "Gallica item",
                "url": "https://gallica.bnf.fr/ark:/12148/example",
                "thumbnail_url": None,
            }
        ]
        drive_manifest = {"items": []}

        with tempfile.TemporaryDirectory() as tmp_dir:
            tmp_path = Path(tmp_dir)
            corpus_path = tmp_path / "corpus-data.json"
            drive_manifest_path = tmp_path / "drive-manifest.json"
            output_path = tmp_path / "manifest.json"
            corpus_path.write_text(json.dumps(corpus), encoding="utf-8")
            drive_manifest_path.write_text(json.dumps(drive_manifest), encoding="utf-8")

            result = subprocess.run(
                [
                    "python",
                    str(self.script_path),
                    "--output",
                    str(output_path),
                    "--corpus",
                    str(corpus_path),
                    "--drive-manifest",
                    str(drive_manifest_path),
                    "--limit",
                    "1",
                ],
                capture_output=True,
                text=True,
                cwd=self.repo_root,
                check=False,
            )
            self.assertEqual(result.returncode, 0, result.stderr or result.stdout)
            self.assertTrue(output_path.exists())

            validate_result = subprocess.run(
                [
                    "python",
                    "tools/scripts/validate_schemas.py",
                    str(output_path),
                    "--schema",
                    "argos-manifest",
                ],
                capture_output=True,
                text=True,
                cwd=self.repo_root,
                check=False,
            )

            self.assertEqual(validate_result.returncode, 0, validate_result.stderr or validate_result.stdout)
            manifest = json.loads(output_path.read_text(encoding="utf-8"))
            self.assertEqual(manifest["summary"]["pending"], 1)
            self.assertEqual(len(manifest["items"]), 1)

    def test_cli_manifest_metadata_reflects_storage_resolution(self):
        module = load_argos_build_manifest_module()
        corpus = [
            {
                "id": "FR-001",
                "title": "Gallica item",
                "url": "https://gallica.bnf.fr/ark:/12148/example",
                "thumbnail_url": None,
            }
        ]
        drive_manifest = {"items": []}

        with tempfile.TemporaryDirectory() as tmp_dir:
            tmp_path = Path(tmp_dir)
            corpus_path = tmp_path / "corpus-data.json"
            drive_manifest_path = tmp_path / "drive-manifest.json"
            output_path = tmp_path / "manifest.json"
            resolved_storage_root = tmp_path / "resolved-storage"
            corpus_path.write_text(json.dumps(corpus), encoding="utf-8")
            drive_manifest_path.write_text(json.dumps(drive_manifest), encoding="utf-8")
            resolved_storage_root.mkdir()

            argv = [
                "argos_build_manifest.py",
                "--output",
                str(output_path),
                "--corpus",
                str(corpus_path),
                "--drive-manifest",
                str(drive_manifest_path),
            ]
            stdout = io.StringIO()
            with mock.patch.object(sys, "argv", argv), mock.patch("sys.stdout", stdout), mock.patch.object(
                module,
                "resolve_storage_root",
                return_value=(resolved_storage_root, "repo-staging"),
            ) as resolve_mock:
                exit_code = module.main()

            self.assertEqual(exit_code, 0)
            resolve_mock.assert_called_once_with(module.REPO_ROOT)
            manifest = json.loads(output_path.read_text(encoding="utf-8"))
            self.assertEqual(manifest["storage_root"], str(resolved_storage_root))
            self.assertEqual(manifest["storage_tier"], "repo-staging")


if __name__ == "__main__":
    unittest.main()
