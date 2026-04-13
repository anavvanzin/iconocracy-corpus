import unittest

from tools.argos.classifier import classify_source


class ClassifierTests(unittest.TestCase):
    def test_gallica_is_iiif(self):
        result = classify_source("https://gallica.bnf.fr/ark:/12148/btv1b...")
        self.assertEqual(result.protocol, "iiif")
        self.assertEqual(result.domain, "gallica.bnf.fr")

    def test_numista_requires_playwright(self):
        result = classify_source("https://en.numista.com/catalogue/exonumia123.html")
        self.assertEqual(result.protocol, "playwright-required")

    def test_british_museum_is_blocked_prone(self):
        result = classify_source("https://www.britishmuseum.org/collection/object/...")
        self.assertEqual(result.protocol, "blocked")

    def test_unknown_domain_is_unknown(self):
        result = classify_source("https://example.org/item/123")
        self.assertEqual(result.protocol, "unknown")
        self.assertEqual(result.domain, "example.org")

    def test_uppercase_host_is_normalized(self):
        result = classify_source("https://GALlica.BNF.FR/ark:/12148/btv1b...")
        self.assertEqual(result.protocol, "iiif")
        self.assertEqual(result.domain, "gallica.bnf.fr")

    def test_no_scheme_url_is_treated_as_url_like_input(self):
        result = classify_source("LOC.GOV/pictures/item/2003664368/")
        self.assertEqual(result.protocol, "iiif")
        self.assertEqual(result.domain, "loc.gov")

    def test_domain_with_port_strips_port_before_lookup(self):
        result = classify_source("https://www.europeana.eu:443/item/92062/BibliographicResource_1000126651795")
        self.assertEqual(result.protocol, "iiif")
        self.assertEqual(result.domain, "www.europeana.eu")

    def test_direct_protocol_source_is_classified(self):
        result = classify_source("https://commons.wikimedia.org/wiki/File:Example.jpg")
        self.assertEqual(result.protocol, "direct")
        self.assertEqual(result.domain, "commons.wikimedia.org")

    def test_loc_variants_are_both_iiif(self):
        for url in (
            "https://loc.gov/resource/ds.00296/",
            "https://www.loc.gov/resource/ds.00296/",
        ):
            with self.subTest(url=url):
                result = classify_source(url)
                self.assertEqual(result.protocol, "iiif")
