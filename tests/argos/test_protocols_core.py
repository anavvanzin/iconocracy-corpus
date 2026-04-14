import unittest

from tools.argos.protocols.direct import classify_http_failure
from tools.argos.protocols.iiif import discover_iiif, gallica_manifest_from_ark


class ProtocolCoreTests(unittest.TestCase):
    def test_gallica_manifest_from_ark(self):
        manifest_url = gallica_manifest_from_ark("ark:/12148/btv1b12345")

        self.assertTrue(manifest_url.endswith("manifest.json"))
        self.assertIn("ark:/12148/btv1b12345", manifest_url)

    def test_403_maps_to_blocked_failure(self):
        self.assertEqual(classify_http_failure(403), "403_block")

    def test_discover_iiif_from_gallica_item(self):
        item = {"url": "https://gallica.bnf.fr/ark:/12148/btv1b12345"}

        discovered = discover_iiif(item)

        self.assertEqual(discovered["iiif_source"], "gallica")
        self.assertTrue(discovered["manifest_url"].endswith("manifest.json"))
        self.assertIn("/f1/full/full/0/native.jpg", discovered["image_url"])

    def test_discover_iiif_returns_none_when_no_known_pattern_matches(self):
        self.assertIsNone(discover_iiif({"url": "https://example.com/object/123"}))


if __name__ == "__main__":
    unittest.main()
