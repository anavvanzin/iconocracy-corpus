import importlib
import unittest


class ArgosSmokeTests(unittest.TestCase):
    def test_argos_modules_are_importable(self):
        self.assertIsNotNone(importlib.import_module("tools.argos"))
        self.assertIsNotNone(importlib.import_module("tools.argos.protocols"))
