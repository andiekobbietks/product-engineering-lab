import importlib.util
import unittest
from pathlib import Path

SCRIPT = Path(__file__).resolve().parents[1] / "experiments/001-nyfasi-reconstruction/scripts/download_reference_images.py"
SPEC = importlib.util.spec_from_file_location("download_reference_images", SCRIPT)
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)

class ReferenceImageSourceTests(unittest.TestCase):
    def test_sources_have_unique_ids_and_filenames(self):
        ids=[row["id"] for row in MODULE.SOURCES]
        names=[row["filename"] for row in MODULE.SOURCES]
        self.assertEqual(len(ids),len(set(ids)))
        self.assertEqual(len(names),len(set(names)))
        self.assertGreaterEqual(len(ids),4)

    def test_sources_have_attribution_and_rights_notes(self):
        for row in MODULE.SOURCES:
            self.assertTrue(row["url"].startswith("https://"))
            self.assertTrue(row["attribution"])
            self.assertTrue(row["rights"])
            self.assertTrue(row["purpose"])

if __name__=="__main__": unittest.main()
