import json
import subprocess
import tempfile
import unittest
from pathlib import Path

from tools.argos.manifest import locked_update_manifest


class ManifestUpdateTests(unittest.TestCase):
    def setUp(self):
        self.repo_root = Path(__file__).resolve().parents[2]
        self.script_path = self.repo_root / "tools" / "scripts" / "argos_manifest_update.py"

    def make_manifest(self):
        return {
            "manifest_version": "1.0",
            "generated_at": "2026-04-13T20:12:00Z",
            "storage_root": "/Volumes/ICONOCRACIA/argos",
            "storage_tier": "ssd",
            "summary": {
                "total_items": 2,
                "pending": 2,
                "success": 0,
                "partial": 0,
                "failed": 0,
                "manual": 0,
            },
            "items": [
                {
                    "item_id": "FR-001",
                    "title": "République debout",
                    "source_url": "https://gallica.bnf.fr/ark:/12148/example",
                    "source_domain": "gallica.bnf.fr",
                    "protocol": "iiif",
                    "status": "pending",
                    "failure_class": "",
                    "failure_reason": "",
                    "attempts": 0,
                    "local_path": "",
                    "sha256": "",
                    "provenance": {
                        "agent": "argos",
                        "method": "iiif",
                        "metadata": {"page": 1},
                    },
                },
                {
                    "item_id": "FR-002",
                    "title": "République assise",
                    "source_url": "https://gallica.bnf.fr/ark:/12148/example-2",
                    "source_domain": "gallica.bnf.fr",
                    "protocol": "iiif",
                    "status": "pending",
                    "failure_class": "",
                    "failure_reason": "",
                    "attempts": 0,
                    "local_path": "",
                    "sha256": "",
                    "provenance": {
                        "agent": "argos",
                        "method": "iiif",
                        "metadata": {"page": 2},
                    },
                },
            ],
        }

    def test_updates_single_item_without_dropping_others_and_writes_backup(self):
        with tempfile.TemporaryDirectory() as tmp:
            manifest_path = Path(tmp) / "manifest.json"
            original_manifest = self.make_manifest()
            manifest_path.write_text(json.dumps(original_manifest), encoding="utf-8")

            locked_update_manifest(
                manifest_path,
                "FR-001",
                {
                    "status": "success",
                    "local_path": "downloads/FR-001.jpg",
                    "sha256": "abc123",
                    "attempts": 1,
                    "provenance": {
                        "retrieved_at": "2026-04-13T20:15:00Z",
                        "retrieved_from": "https://gallica.bnf.fr/iiif/ark:/12148/example/full/full/0/native.jpg",
                        "agent": "argos",
                        "method": "iiif",
                        "metadata": {"page": 1},
                    },
                },
            )

            updated = json.loads(manifest_path.read_text(encoding="utf-8"))
            backup = json.loads(manifest_path.with_suffix(".json.bak").read_text(encoding="utf-8"))

            self.assertEqual(updated["items"][0]["status"], "success")
            self.assertEqual(updated["items"][0]["local_path"], "downloads/FR-001.jpg")
            self.assertEqual(updated["items"][0]["provenance"]["metadata"], {"page": 1})
            self.assertEqual(updated["items"][1]["status"], "pending")
            self.assertEqual(updated["summary"], {
                "total_items": 2,
                "pending": 1,
                "success": 1,
                "partial": 0,
                "failed": 0,
                "manual": 0,
            })
            self.assertEqual(backup, original_manifest)
            self.assertTrue((manifest_path.parent / "manifest.lock").exists())

    def test_rejects_empty_or_invalid_json_manifest(self):
        with tempfile.TemporaryDirectory() as tmp:
            empty_manifest_path = Path(tmp) / "empty.json"
            empty_manifest_path.write_text("", encoding="utf-8")
            with self.assertRaises(ValueError):
                locked_update_manifest(empty_manifest_path, "FR-001", {"status": "success"})

            invalid_manifest_path = Path(tmp) / "invalid.json"
            invalid_manifest_path.write_text("{not-json}", encoding="utf-8")
            with self.assertRaises(ValueError):
                locked_update_manifest(invalid_manifest_path, "FR-001", {"status": "success"})

    def test_rejects_schema_invalid_merge_before_replace(self):
        with tempfile.TemporaryDirectory() as tmp:
            manifest_path = Path(tmp) / "manifest.json"
            manifest_path.write_text(json.dumps(self.make_manifest()), encoding="utf-8")

            with self.assertRaises(ValueError):
                locked_update_manifest(manifest_path, "FR-001", {"status": "success"})

            data = json.loads(manifest_path.read_text(encoding="utf-8"))
            self.assertEqual(data["items"][0]["status"], "pending")

    def test_missing_item_id_raises_clean_error(self):
        with tempfile.TemporaryDirectory() as tmp:
            manifest_path = Path(tmp) / "manifest.json"
            manifest = self.make_manifest()
            del manifest["items"][0]["item_id"]
            manifest_path.write_text(json.dumps(manifest), encoding="utf-8")

            with self.assertRaisesRegex(ValueError, "Manifest item at index 0 is missing item_id"):
                locked_update_manifest(manifest_path, "FR-001", {"status": "manual"})

    def test_nested_provenance_patch_preserves_existing_nested_keys(self):
        with tempfile.TemporaryDirectory() as tmp:
            manifest_path = Path(tmp) / "manifest.json"
            manifest = self.make_manifest()
            manifest["items"][0]["provenance"]["metadata"] = {
                "page": 1,
                "thumbnail_missing": True,
                "dispatch_group": "gallica.bnf.fr",
            }
            manifest_path.write_text(json.dumps(manifest), encoding="utf-8")

            locked_update_manifest(
                manifest_path,
                "FR-001",
                {
                    "provenance": {
                        "metadata": {
                            "page": 7,
                        }
                    }
                },
            )

            updated = json.loads(manifest_path.read_text(encoding="utf-8"))
            self.assertEqual(
                updated["items"][0]["provenance"]["metadata"],
                {
                    "page": 7,
                    "thumbnail_missing": True,
                    "dispatch_group": "gallica.bnf.fr",
                },
            )
            self.assertEqual(updated["items"][0]["provenance"]["agent"], "argos")
            self.assertEqual(updated["items"][0]["provenance"]["method"], "iiif")

    def test_main_and_backup_remain_unchanged_when_validation_fails(self):
        with tempfile.TemporaryDirectory() as tmp:
            manifest_path = Path(tmp) / "manifest.json"
            original_manifest = self.make_manifest()
            manifest_path.write_text(json.dumps(original_manifest), encoding="utf-8")

            with self.assertRaises(ValueError):
                locked_update_manifest(manifest_path, "FR-001", {"status": "success"})

            self.assertEqual(
                json.loads(manifest_path.read_text(encoding="utf-8")),
                original_manifest,
            )
            self.assertFalse(manifest_path.with_suffix(".json.bak").exists())

    def test_cli_updates_manifest(self):
        with tempfile.TemporaryDirectory() as tmp:
            manifest_path = Path(tmp) / "manifest.json"
            manifest_path.write_text(json.dumps(self.make_manifest()), encoding="utf-8")

            result = subprocess.run(
                [
                    "python",
                    str(self.script_path),
                    "--manifest",
                    str(manifest_path),
                    "--item-id",
                    "FR-001",
                    "--patch",
                    '{"status":"success","local_path":"downloads/FR-001.jpg","sha256":"abc123","attempts":1,"provenance":{"retrieved_at":"2026-04-13T20:15:00Z","retrieved_from":"https://gallica.bnf.fr/iiif/ark:/12148/example/full/full/0/native.jpg","agent":"argos","method":"iiif","metadata":{"page":1}}}',
                ],
                capture_output=True,
                text=True,
                cwd=self.repo_root,
                check=False,
            )

            self.assertEqual(result.returncode, 0, result.stderr or result.stdout)
            data = json.loads(manifest_path.read_text(encoding="utf-8"))
            self.assertEqual(data["items"][0]["status"], "success")
            self.assertIn("Updated manifest item FR-001", result.stdout)

    def test_cli_reports_missing_item_id_cleanly(self):
        with tempfile.TemporaryDirectory() as tmp:
            manifest_path = Path(tmp) / "manifest.json"
            manifest = self.make_manifest()
            del manifest["items"][0]["item_id"]
            manifest_path.write_text(json.dumps(manifest), encoding="utf-8")

            result = subprocess.run(
                [
                    "python",
                    str(self.script_path),
                    "--manifest",
                    str(manifest_path),
                    "--item-id",
                    "FR-001",
                    "--patch",
                    '{"status":"manual","failure_class":"blocked","failure_reason":"missing id"}',
                ],
                capture_output=True,
                text=True,
                cwd=self.repo_root,
                check=False,
            )

            self.assertEqual(result.returncode, 1)
            self.assertEqual(result.stderr.strip(), "Manifest item at index 0 is missing item_id")


if __name__ == "__main__":
    unittest.main()
