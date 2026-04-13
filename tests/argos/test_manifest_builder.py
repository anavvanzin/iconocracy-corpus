import json
import subprocess
import tempfile
import unittest
from pathlib import Path

from tools.argos.manifest import build_manifest


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
    def test_cli_dry_run_reports_without_writing_output(self):
        repo_root = Path(__file__).resolve().parents[2]
        script_path = repo_root / "tools" / "scripts" / "argos_build_manifest.py"

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
                    str(script_path),
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
                cwd=repo_root,
                check=False,
            )

        self.assertEqual(result.returncode, 0, result.stderr or result.stdout)
        self.assertIn("Pending items: 1", result.stdout)
        self.assertIn("iiif: 1", result.stdout)
        self.assertFalse(output_path.exists())


if __name__ == "__main__":
    unittest.main()
