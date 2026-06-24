import json
import subprocess
import tempfile
import unittest
from pathlib import Path

from tools.scripts.validate_schemas import load_schema, validate_record


class ManifestSchemaTests(unittest.TestCase):
    def make_manifest(self, *, status="pending"):
        return {
            "manifest_version": "1.0",
            "generated_at": "2026-04-13T20:12:00Z",
            "storage_root": "/Volumes/ICONOCRACIA/argos",
            "storage_tier": "ssd",
            "summary": {
                "total_items": 1,
                "pending": 1 if status == "pending" else 0,
                "success": 1 if status == "success" else 0,
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
                    "status": status,
                    "failure_class": "",
                    "failure_reason": "",
                    "attempts": 0,
                    "local_path": "downloads/FR-001.jpg" if status == "success" else "",
                    "sha256": "abc123" if status == "success" else "",
                    "provenance": {
                        "retrieved_at": "2026-04-13T20:15:00Z",
                        "retrieved_from": "https://gallica.bnf.fr/iiif/ark:/12148/example/full/full/0/native.jpg",
                        "agent": "argos",
                        "method": "iiif",
                        "metadata": {"page": 1},
                    },
                }
            ],
        }

    def test_argos_manifest_schema_loads(self):
        schema = load_schema("argos-manifest")

        self.assertEqual(schema["title"], "ArgosManifest")

    def test_valid_manifest_record_passes_validation(self):
        manifest = self.make_manifest()

        is_valid, errors = validate_record(manifest, "argos-manifest")

        self.assertTrue(is_valid, errors)
        self.assertEqual(errors, [])

    def test_invalid_datetime_or_uri_is_rejected(self):
        manifest = self.make_manifest()
        manifest["generated_at"] = "not-a-datetime"
        manifest["items"][0]["source_url"] = "not-a-uri"

        is_valid, errors = validate_record(manifest, "argos-manifest")

        self.assertFalse(is_valid)
        self.assertTrue(any("generated_at" in error and "date-time" in error for error in errors), errors)
        self.assertTrue(any("items.0.source_url" in error and "uri" in error for error in errors), errors)

    def test_success_item_missing_local_path_or_sha256_is_rejected(self):
        manifest = self.make_manifest(status="success")
        manifest["items"][0]["local_path"] = ""
        manifest["items"][0]["sha256"] = ""

        is_valid, errors = validate_record(manifest, "argos-manifest")

        self.assertFalse(is_valid)
        self.assertTrue(any("items.0.local_path" in error for error in errors), errors)
        self.assertTrue(any("items.0.sha256" in error for error in errors), errors)

    def test_validator_cli_accepts_argos_manifest_schema(self):
        manifest = self.make_manifest()

        repo_root = Path(__file__).resolve().parents[2]
        script_path = repo_root / "tools" / "scripts" / "validate_schemas.py"

        with tempfile.TemporaryDirectory() as tmp_dir:
            manifest_path = Path(tmp_dir) / "manifest.json"
            manifest_path.write_text(json.dumps(manifest), encoding="utf-8")

            result = subprocess.run(
                [
                    "python",
                    str(script_path),
                    str(manifest_path),
                    "--schema",
                    "argos-manifest",
                ],
                capture_output=True,
                text=True,
                cwd=repo_root,
                check=False,
            )

        self.assertEqual(result.returncode, 0, result.stderr or result.stdout)
        self.assertIn("All records are valid", result.stdout)


if __name__ == "__main__":
    unittest.main()
