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

    def test_build_dispatch_groups_returns_empty_for_empty_input(self):
        self.assertEqual(build_dispatch_groups([]), [])
        self.assertEqual(build_dispatch_groups(None), [])

    def test_build_dispatch_groups_returns_empty_when_nothing_is_pending(self):
        items = [
            {"item_id": "DONE-001", "source_domain": "loc.gov", "protocol": "iiif", "status": "success"},
            {"item_id": "FAIL-001", "source_domain": "gallica.bnf.fr", "protocol": "iiif", "status": "failed"},
            "malformed-entry",
        ]

        self.assertEqual(build_dispatch_groups(items), [])

    def test_build_dispatch_groups_rejects_invalid_max_groups(self):
        with self.assertRaisesRegex(ValueError, "max_groups must be at least 1"):
            build_dispatch_groups([], max_groups=0)

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

    def test_build_dispatch_groups_merges_longtail_when_cap_is_exceeded_without_special_protocols(self):
        items = [
            {"item_id": "ALPHA-001", "source_domain": "alpha.example", "protocol": "direct", "status": "pending"},
            {"item_id": "BETA-001", "source_domain": "beta.example", "protocol": "direct", "status": "pending"},
            {"item_id": "GAMMA-001", "source_domain": "gamma.example", "protocol": "direct", "status": "pending"},
            {"item_id": "DELTA-001", "source_domain": "delta.example", "protocol": "direct", "status": "pending"},
        ]

        groups = build_dispatch_groups(items, max_groups=3)

        self.assertEqual([group["group_name"] for group in groups], ["alpha.example", "beta.example", "longtail"])
        self.assertEqual(groups[-1]["protocol"], "direct")
        self.assertEqual(groups[-1]["item_ids"], ["DELTA-001", "GAMMA-001"])
        self.assertIn("delta.example, gamma.example", groups[-1]["prompt_hint"])
        self.assertIn("direct", groups[-1]["prompt_hint"])

    def test_build_dispatch_groups_normalizes_missing_domain_protocol_and_item_id(self):
        items = [
            {"item_id": "KNOWN-001", "source_domain": "example.org", "protocol": "iiif", "status": "pending"},
            {"item_id": None, "source_domain": "", "protocol": None, "status": "pending"},
            {"source_domain": None, "status": "pending"},
            "malformed-entry",
        ]

        groups = build_dispatch_groups(items, max_groups=6)

        self.assertEqual([group["group_name"] for group in groups], ["unknown", "example.org"])
        self.assertEqual(groups[0]["protocol"], "unknown")
        self.assertEqual(groups[0]["item_ids"], ["unknown", "unknown"])
        self.assertEqual(groups[1]["protocol"], "iiif")
        self.assertEqual(groups[1]["item_ids"], ["KNOWN-001"])

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
