from pathlib import Path
import unittest


class ArgosSmokeTests(unittest.TestCase):
    def test_argos_package_exists(self):
        self.assertTrue(Path("tools/argos/__init__.py").exists())
        self.assertTrue(Path("tools/argos/protocols/__init__.py").exists())
