"""Regression tests for tolerance calculations and sensitivity to changed inputs."""
import copy
import json
import sys
import unittest
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parents[1] / "scripts"
sys.path.insert(0, str(SCRIPT_DIR))
from analyse_interaction import calculate_stackups, _pin_seal_interpretation  # noqa: E402

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

    def test_seal_interfaces_use_current_cad_dimensions_and_worst_case_bounds(self):
        results = calculate_stackups(self.parameters, self.ledger)
        pin_seal = results["spindle_pin_to_elastomer_seal"]
        seal_bearing = results["elastomer_seal_to_bearing_bore"]
        self.assertAlmostEqual(pin_seal["nominal"], 0.20)
        self.assertAlmostEqual(pin_seal["worst_case_min"], 0.05)
        self.assertAlmostEqual(pin_seal["worst_case_max"], 0.35)
        self.assertAlmostEqual(seal_bearing["nominal"], 0.10)
        self.assertAlmostEqual(seal_bearing["worst_case_min"], -0.05)
        self.assertAlmostEqual(seal_bearing["worst_case_max"], 0.25)

    def test_shared_physical_feature_tolerances_update_every_related_stack(self):
        ledger = copy.deepcopy(self.ledger)
        baseline = calculate_stackups(self.parameters, ledger)
        ledger["shared_tolerances"]["spindle_pin_diameter"] = 0.10
        ledger["shared_tolerances"]["bearing_bore_diameter"] = 0.10
        updated = calculate_stackups(self.parameters, ledger)
        for name in (
            "spindle_pin_to_bearing_bore",
            "spindle_pin_to_elastomer_seal",
            "elastomer_seal_to_bearing_bore",
        ):
            self.assertGreater(
                baseline[name]["worst_case_max"] - baseline[name]["nominal"],
                0.0,
            )
            self.assertGreater(
                updated[name]["worst_case_max"],
                baseline[name]["worst_case_max"],
            )

    def test_pin_seal_sign_convention_reports_interference_and_clearance(self):
        self.assertEqual(_pin_seal_interpretation(0.05, 0.35), "INTERFERENCE")
        self.assertEqual(_pin_seal_interpretation(-0.35, -0.05), "CLEARANCE")
        self.assertEqual(
            _pin_seal_interpretation(-0.05, 0.05),
            "INTERFERENCE_AND_CLEARANCE_POSSIBLE",
        )

    def test_negative_tolerance_is_rejected(self):
        ledger = copy.deepcopy(self.ledger)
        ledger["interfaces"]["roller_band_to_wall_slot"]["slot_width_tolerance"] = -0.01
        with self.assertRaises(ValueError):
            calculate_stackups(self.parameters, ledger)


if __name__ == "__main__":
    unittest.main()
