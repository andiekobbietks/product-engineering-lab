import importlib.util
import unittest
from pathlib import Path

SCRIPT = Path(__file__).resolve().parents[1] / "experiments/001-nyfasi-reconstruction/scripts/fit_dimensions.py"
SPEC = importlib.util.spec_from_file_location("fit_dimensions", SCRIPT)
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)

class MetricFitTests(unittest.TestCase):
    def test_inverse_variance_fit_and_provenance(self):
        rows = [
            {"value_mm": 100.0, "sigma_mm": 1.0, "source_id": "A", "view_id": "top", "calibration_id": "C1"},
            {"value_mm": 102.0, "sigma_mm": 1.0, "source_id": "B", "view_id": "side", "calibration_id": "C2"},
        ]
        fit = MODULE.fit_group(rows)
        self.assertAlmostEqual(fit["estimate_mm"], 101.0, places=3)
        self.assertEqual(fit["classification"], "MEASURED")
        self.assertEqual(fit["independent_views"], 2)

    def test_single_view_stays_image_estimated(self):
        rows = [{"value_mm": 24.0, "sigma_mm": 2.0, "source_id": "A", "view_id": "front", "calibration_id": "C1"}]
        self.assertEqual(MODULE.fit_group(rows)["classification"], "IMAGE_ESTIMATED")

    def test_missing_calibration_is_rejected(self):
        with self.assertRaises(ValueError):
            MODULE.build_report({"observations": [{"parameter": "housing_w", "value_mm": 100}]}, {"parameters": {"housing_w": {}}})

if __name__ == "__main__":
    unittest.main()
