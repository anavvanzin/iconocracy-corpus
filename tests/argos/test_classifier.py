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
