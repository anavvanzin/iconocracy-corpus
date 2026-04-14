import json
import subprocess
import tempfile
import unittest
from pathlib import Path

from tools.scripts.argos_prepare_dispatch import build_dispatch_groups


class DispatchTests(unittest.TestCase):
    def setUp(self):
        self.repo_root = Path(__file__).resolve().parents[2]
        self.script_path = self.repo_root / "tools" / "scripts" / "argos_prepare_dispatch.py"

    def test_build_dispatch_groups_caps_at_six_and_bundles_longtail(self):
        items = [
            {"item_id": "FR-001", "source_domain": "gallica.bnf.fr", "protocol": "iiif", "status": "pending"},
            {"item_id": "FR-002", "source_domain": "gallica.bnf.fr", "protocol": "iiif", "status": "pending"},
            {"item_id": "FR-003", "source_domain": "gallica.bnf.fr", "protocol": "iiif", "status": "pending"},
            {"item_id": "LOC-001", "source_domain": "loc.gov", "protocol": "iiif", "status": "pending"},
            {"item_id": "LOC-002", "source_domain": "loc.gov", "protocol": "iiif", "status": "pending"},
            {"item_id": "WM-001", "source_domain": "commons.wikimedia.org", "protocol": "direct", "status": "pending"},
            {"item_id": "WM-002", "source_domain": "commons.wikimedia.org", "protocol": "direct", "status": "pending"},
            {"item_id": "VAM-001", "source_domain": "collections.vam.ac.uk", "protocol": "direct", "status": "pending"},
            {"item_id": "BI-001", "source_domain": "bildindex.de", "protocol": "direct", "status": "pending"},
            {"item_id": "BI-002", "source_domain": "bildindex.de", "protocol": "direct", "status": "pending"},
            {"item_id": "BM-001", "source_domain": "britishmuseum.org", "protocol": "blocked", "status": "pending"},
            {"item_id": "UNK-001", "source_domain": "mystery.example", "protocol": "unknown", "status": "pending"},
            {"item_id": "DONE-001", "source_domain": "loc.gov", "protocol": "iiif", "status": "success"},
        ]

        groups = build_dispatch_groups(items, max_groups=6)

        self.assertEqual([group["group_name"] for group in groups], [
            "gallica.bnf.fr",
            "bildindex.de",
            "commons.wikimedia.org",
            "loc.gov",
            "collections.vam.ac.uk",
            "longtail",
        ])
        self.assertEqual(groups[-1]["protocol"], "mixed")
        self.assertEqual(groups[-1]["item_ids"], ["BM-001", "UNK-001"])
        self.assertIn("blocked", groups[-1]["prompt_hint"])
        self.assertIn("unknown", groups[-1]["prompt_hint"])
        self.assertNotIn("DONE-001", [item_id for group in groups for item_id in group["item_ids"]])

    def test_build_dispatch_groups_is_deterministic_for_tied_domain_counts(self):
        items = [
            {"item_id": "B-002", "source_domain": "beta.example", "protocol": "direct", "status": "pending"},
            {"item_id": "A-002", "source_domain": "alpha.example", "protocol": "direct", "status": "pending"},
            {"item_id": "B-001", "source_domain": "beta.example", "protocol": "direct", "status": "pending"},
            {"item_id": "A-001", "source_domain": "alpha.example", "protocol": "direct", "status": "pending"},
        ]

        groups = build_dispatch_groups(items, max_groups=6)

        self.assertEqual([group["group_name"] for group in groups], ["alpha.example", "beta.example"])
        self.assertEqual(groups[0]["item_ids"], ["A-001", "A-002"])
        self.assertEqual(groups[1]["item_ids"], ["B-001", "B-002"])

    def test_cli_prints_json_array(self):
        manifest = {
            "items": [
                {"item_id": "FR-001", "source_domain": "gallica.bnf.fr", "protocol": "iiif", "status": "pending"},
                {"item_id": "FR-002", "source_domain": "gallica.bnf.fr", "protocol": "iiif", "status": "pending"},
                {"item_id": "BM-001", "source_domain": "britishmuseum.org", "protocol": "blocked", "status": "pending"},
            ]
        }

        with tempfile.TemporaryDirectory() as tmp_dir:
            manifest_path = Path(tmp_dir) / "manifest.json"
            manifest_path.write_text(json.dumps(manifest), encoding="utf-8")

            result = subprocess.run(
                ["python", str(self.script_path), "--manifest", str(manifest_path)],
                capture_output=True,
                text=True,
                cwd=self.repo_root,
                check=False,
            )

        self.assertEqual(result.returncode, 0, result.stderr or result.stdout)
        payload = json.loads(result.stdout)
        self.assertEqual(payload[0]["group_name"], "gallica.bnf.fr")
        self.assertEqual(payload[0]["protocol"], "iiif")
        self.assertEqual(payload[0]["item_ids"], ["FR-001", "FR-002"])
        self.assertEqual(payload[1]["group_name"], "britishmuseum.org")


if __name__ == "__main__":
    unittest.main()
