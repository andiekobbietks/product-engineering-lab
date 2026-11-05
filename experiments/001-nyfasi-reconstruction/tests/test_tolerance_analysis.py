"""Regression tests for tolerance calculations and sensitivity to changed inputs."""
import copy
import json
import sys
import unittest
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parents[1] / "scripts"
sys.path.insert(0, str(SCRIPT_DIR))
from analyse_interaction import calculate_stackups  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]


class ToleranceCalculationTests(unittest.TestCase):
    """Verify the derived interface limits respond to source-ledger changes."""

    @classmethod
    def setUpClass(cls):
        cls.parameters = {
            key: float(item["value"])
            for key, item in json.loads((ROOT / "models" / "cad-parameters.json").read_text())["parameters"].items()
        }
        cls.ledger = json.loads((ROOT / "models" / "tolerance-stackup.json").read_text())

    def test_band_slot_stack_is_derived_from_dimensions(self):
        result = calculate_stackups(self.parameters, self.ledger)["roller_band_to_wall_slot"]
        self.assertAlmostEqual(result["nominal"], 0.0)
        self.assertAlmostEqual(result["worst_case_min"], -0.25)
        self.assertAlmostEqual(result["worst_case_max"], 0.25)

    def test_changing_tolerance_changes_reported_limits(self):
        ledger = copy.deepcopy(self.ledger)
        ledger["interfaces"]["roller_band_to_wall_slot"]["slot_width_tolerance"] = 0.20
        result = calculate_stackups(self.parameters, ledger)["roller_band_to_wall_slot"]
        self.assertAlmostEqual(result["worst_case_min"], -0.30)
        self.assertAlmostEqual(result["worst_case_max"], 0.30)

    def test_axial_alignment_is_calculated_from_tolerance_inputs(self):
        result = calculate_stackups(self.parameters, self.ledger)["band_to_slot_axial_alignment"]
        self.assertAlmostEqual(result["worst_case_absolute_offset"], 0.25)

    def test_seal_interfaces_use_current_cad_dimensions(self):
        results = calculate_stackups(self.parameters, self.ledger)
        self.assertAlmostEqual(results["spindle_pin_to_elastomer_seal"]["nominal"], 0.20)
        self.assertAlmostEqual(results["elastomer_seal_to_bearing_bore"]["nominal"], 0.10)

    def test_negative_tolerance_is_rejected(self):
        ledger = copy.deepcopy(self.ledger)
        ledger["interfaces"]["roller_band_to_wall_slot"]["slot_width_tolerance"] = -0.01
        with self.assertRaises(ValueError):
            calculate_stackups(self.parameters, ledger)


if __name__ == "__main__":
    unittest.main()
