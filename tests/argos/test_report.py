import json
import subprocess
import tempfile
import unittest
from pathlib import Path

from tools.argos.report import build_report_markdown


class ReportTests(unittest.TestCase):
    def setUp(self):
        self.repo_root = Path(__file__).resolve().parents[2]
        self.script_path = self.repo_root / "tools" / "scripts" / "argos_report.py"

    def make_manifest(self):
        return {
            "manifest_version": "1.0",
            "generated_at": "2026-04-13T20:12:00Z",
            "storage_root": "/Volumes/ICONOCRACIA/argos",
            "storage_tier": "ssd",
            "summary": {
                "total_items": 4,
                "pending": 0,
                "success": 1,
                "partial": 1,
                "failed": 1,
                "manual": 1,
            },
            "items": [
                {
                    "item_id": "FR-001",
                    "title": "République debout",
                    "source_url": "https://gallica.bnf.fr/ark:/12148/example",
                    "source_domain": "gallica.bnf.fr",
                    "protocol": "iiif",
                    "status": "success",
                    "failure_class": "",
                    "failure_reason": "",
                    "attempts": 1,
                    "local_path": "downloads/FR-001.jpg",
                    "sha256": "abc123",
                    "provenance": {
                        "retrieved_at": "2026-04-13T20:15:00Z",
                        "retrieved_from": "https://gallica.bnf.fr/iiif/ark:/12148/example/full/full/0/native.jpg",
                        "agent": "argos",
                        "method": "iiif",
                        "metadata": {"page": 1},
                    },
                },
                {
                    "item_id": "UK-001",
                    "title": "Britannia seated",
                    "source_url": "https://www.britishmuseum.org/collection/object/X",
                    "source_domain": "britishmuseum.org",
                    "protocol": "blocked",
                    "status": "manual",
                    "failure_class": "403_block",
                    "failure_reason": "Browser challenge requires manual retrieval",
                    "attempts": 2,
                    "local_path": "",
                    "sha256": "",
                    "provenance": {
                        "agent": "argos",
                        "method": "blocked",
                        "metadata": {"dispatch_group": "britishmuseum.org"},
                    },
                },
                {
                    "item_id": "EU-001",
                    "title": "Europa allegory",
                    "source_url": "https://europeana.eu/item/example",
                    "source_domain": "europeana.eu",
                    "protocol": "iiif",
                    "status": "partial",
                    "failure_class": "iiif_image_unavailable",
                    "failure_reason": "Manifest discovered but no stable image URL",
                    "attempts": 1,
                    "local_path": "",
                    "sha256": "",
                    "provenance": {
                        "agent": "argos",
                        "method": "iiif",
                        "metadata": {},
                    },
                },
                {
                    "item_id": "DE-001",
                    "title": "Germania token",
                    "source_url": "https://example.org/germania",
                    "source_domain": "example.org",
                    "protocol": "direct",
                    "status": "failed",
                    "failure_class": "404_not_found",
                    "failure_reason": "Remote file no longer exists",
                    "attempts": 2,
                    "local_path": "",
                    "sha256": "",
                    "provenance": {
                        "agent": "argos",
                        "method": "direct",
                        "metadata": {},
                    },
                },
            ],
        }

    def test_report_includes_required_sections_and_manual_case(self):
        text = build_report_markdown(self.make_manifest())

        self.assertIn("# ARGOS acquisition report", text)
        self.assertIn("## 1. Run metadata", text)
        self.assertIn("## 2. Summary counts", text)
        self.assertIn("## 3. Per-domain breakdown", text)
        self.assertIn("## 4. Failure taxonomy", text)
        self.assertIn("## 5. Manual-intervention checklist", text)
        self.assertIn("## 6. Next-action suggestions", text)
        self.assertIn("UK-001", text)
        self.assertIn("britishmuseum.org", text)
        self.assertIn("403_block", text)

    def test_report_suggests_actions_from_failures(self):
        text = build_report_markdown(self.make_manifest())

        self.assertIn("Prioritize manual retrieval for blocked domains", text)
        self.assertIn("Re-check direct URLs returning permanent client errors", text)
        self.assertIn("Retry IIIF discovery or image extraction", text)

    def test_cli_writes_markdown_report(self):
        with tempfile.TemporaryDirectory() as tmp:
            manifest_path = Path(tmp) / "manifest.json"
            output_path = Path(tmp) / "report.md"
            manifest_path.write_text(json.dumps(self.make_manifest()), encoding="utf-8")

            result = subprocess.run(
                [
                    "python",
                    str(self.script_path),
                    "--manifest",
                    str(manifest_path),
                    "--output",
                    str(output_path),
                ],
                capture_output=True,
                text=True,
                cwd=self.repo_root,
                check=False,
            )

            self.assertEqual(result.returncode, 0, result.stderr or result.stdout)
            self.assertTrue(output_path.exists())
            report_text = output_path.read_text(encoding="utf-8")
            self.assertIn("# ARGOS acquisition report", report_text)
            self.assertIn("Manual-intervention checklist", report_text)
            self.assertIn("Report written to", result.stdout)


if __name__ == "__main__":
    unittest.main()
