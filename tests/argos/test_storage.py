import tempfile
import unittest
from pathlib import Path

from tools.argos.provenance import build_provenance
from tools.argos.storage import resolve_storage_root


class ResolveStorageRootTests(unittest.TestCase):
    def test_prefers_ssd_root_when_present(self):
        with tempfile.TemporaryDirectory() as repo_dir, tempfile.TemporaryDirectory() as ssd_dir:
            repo_root = Path(repo_dir)
            ssd_root = Path(ssd_dir)

            resolved_path, tier = resolve_storage_root(repo_root, ssd_root=ssd_root)

            self.assertEqual(resolved_path, ssd_root)
            self.assertEqual(tier, "ssd")
            self.assertFalse((repo_root / "data" / "raw" / ".staging").exists())

    def test_falls_back_to_repo_staging_and_creates_directory(self):
        with tempfile.TemporaryDirectory() as repo_dir:
            repo_root = Path(repo_dir)
            missing_ssd = repo_root / "missing-ssd"

            resolved_path, tier = resolve_storage_root(repo_root, ssd_root=missing_ssd)

            self.assertEqual(resolved_path, repo_root / "data" / "raw" / ".staging")
            self.assertEqual(tier, "repo-staging")
            self.assertTrue(resolved_path.exists())
            self.assertTrue(resolved_path.is_dir())


class ProvenanceBuilderTests(unittest.TestCase):
    def test_builds_provenance_with_required_keys_and_metadata(self):
        provenance = build_provenance(
            fetched_by="argos",
            protocol="iiif",
            storage_tier="ssd",
            source_url="https://gallica.bnf.fr/ark:/12148/example",
            record_id="CC-001",
        )

        self.assertEqual(provenance["fetched_by"], "argos")
        self.assertEqual(provenance["protocol"], "iiif")
        self.assertEqual(provenance["storage_tier"], "ssd")
        self.assertRegex(provenance["fetched_at"], r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z$")
        self.assertEqual(
            provenance["metadata"],
            {
                "source_url": "https://gallica.bnf.fr/ark:/12148/example",
                "source_domain": "gallica.bnf.fr",
                "record_id": "CC-001",
            },
        )

    def test_merges_extra_metadata_and_omits_null_values(self):
        provenance = build_provenance(
            fetched_by="argos",
            protocol="direct",
            storage_tier="repo-staging",
            source_url=None,
            extra_metadata={"filename": "image-001.jpg", "sha256": "abc123"},
        )

        self.assertEqual(provenance["metadata"], {"filename": "image-001.jpg", "sha256": "abc123"})


if __name__ == "__main__":
    unittest.main()
