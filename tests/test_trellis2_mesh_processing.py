import json
import tempfile
import unittest
from pathlib import Path

import trimesh

SCRIPT = Path(__file__).resolve().parents[1] / "experiments/001-nyfasi-reconstruction/scripts/process_trellis2_mesh.py"
import importlib.util
SPEC = importlib.util.spec_from_file_location("process_trellis2_mesh", SCRIPT)
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


class TrellisMeshProcessingTests(unittest.TestCase):
    def test_reports_mesh_metrics_without_claiming_physical_units(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            source = root / "box.glb"
            report_path = root / "report.json"
            trimesh.creation.box().export(source)
            report = MODULE.process_glb(source, report_path, None)
            saved = json.loads(report_path.read_text())
            self.assertEqual(report["source_sha256"], MODULE.sha256(source))
            self.assertIn("not physically calibrated", report["interpretation"])
            self.assertTrue(saved["geometry"][0]["before"]["is_watertight"])
            self.assertEqual(saved["units"], "unknown; TRELLIS.2 output is not physically calibrated")

    def test_repair_never_overwrites_source(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            source = root / "box.glb"
            repaired = root / "box_repaired.glb"
            report_path = root / "report.json"
            trimesh.creation.box().export(source)
            original_hash = MODULE.sha256(source)
            MODULE.process_glb(source, report_path, repaired)
            self.assertEqual(MODULE.sha256(source), original_hash)
            self.assertTrue(repaired.exists())
            self.assertNotEqual(repaired, source)


if __name__ == "__main__":
    unittest.main()
