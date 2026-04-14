import unittest

from tools.argos.protocols.html import extract_landing_page_candidates


class HtmlExtractionTests(unittest.TestCase):
    def test_extracts_og_image_candidate(self):
        html = """
        <html>
          <head>
            <title>Example object</title>
            <meta property="og:image" content="https://cdn.example.org/images/object-1234.jpg">
          </head>
        </html>
        """

        result = extract_landing_page_candidates(html, "https://example.org/object/1234")

        self.assertEqual(result["page_url"], "https://example.org/object/1234")
        self.assertEqual(result["page_title"], "Example object")
        self.assertEqual(result["candidates"][0]["url"], "https://cdn.example.org/images/object-1234.jpg")
        self.assertEqual(result["candidates"][0]["kind"], "image")
        self.assertEqual(result["candidates"][0]["source_hint"], "meta:og:image")
        self.assertEqual(result["iiif_manifest_candidates"], [])

    def test_normalizes_relative_img_src(self):
        html = """
        <html>
          <body>
            <img src="/media/hero.jpg" alt="hero">
          </body>
        </html>
        """

        result = extract_landing_page_candidates(html, "https://images.example.org/collection/item-7")

        self.assertEqual(result["candidates"][0]["url"], "https://images.example.org/media/hero.jpg")
        self.assertEqual(result["candidates"][0]["source_hint"], "img:src")

    def test_detects_iiif_manifest_url_inside_json(self):
        html = """
        <html>
          <head><title>IIIF object</title></head>
          <body>
            <script type="application/ld+json">
              {
                "manifest": "https://iiif.example.org/iiif/3/book-1/manifest"
              }
            </script>
          </body>
        </html>
        """

        result = extract_landing_page_candidates(html, "https://example.org/object/book-1")

        self.assertEqual(result["iiif_manifest_candidates"], ["https://iiif.example.org/iiif/3/book-1/manifest"])
        self.assertEqual(result["candidates"], [])

    def test_prefers_explicit_high_resolution_download(self):
        html = """
        <html>
          <body>
            <img src="https://media.example.org/thumbs/object-9-small.jpg">
            <a href="https://media.example.org/downloads/object-9-full-4000x3000.jpg">Download JPG 4000x3000</a>
            <a href="https://media.example.org/downloads/object-9-preview.jpg">Preview</a>
            <source srcset="https://media.example.org/object-9-640.jpg 640w, https://media.example.org/object-9-2048.jpg 2048w">
          </body>
        </html>
        """

        result = extract_landing_page_candidates(html, "https://example.org/object/9")

        top_candidate = result["candidates"][0]
        self.assertEqual(top_candidate["url"], "https://media.example.org/downloads/object-9-full-4000x3000.jpg")
        self.assertEqual(top_candidate["kind"], "download")
        self.assertEqual(top_candidate["source_hint"], "a:download")
        self.assertGreater(top_candidate["score"], result["candidates"][1]["score"])


if __name__ == "__main__":
    unittest.main()
