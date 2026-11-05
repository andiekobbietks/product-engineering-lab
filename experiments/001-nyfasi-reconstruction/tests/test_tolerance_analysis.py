"""Regression tests for tolerance calculations and sensitivity to changed inputs."""
import copy
import io
import json
import sys
import unittest
from contextlib import redirect_stdout
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parents[1] / "scripts"
sys.path.insert(0, str(SCRIPT_DIR))
from analyse_interaction import (  # noqa: E402
    _pin_seal_interpretation,
    calculate_stackups,
    main,
)

ROOT = Path(__file__).resolve().parents[1]


class ToleranceCalculationTests(unittest.TestCase):
    """Verify derived interface limits, report classifications, and tolerance propagation."""

    @classmethod
    def setUpClass(cls):
        """Load the checked-in CAD parameter and tolerance fixtures once for this test class."""
        cls.parameters = {
            key: float(item["value"])
            for key, item in json.loads((ROOT / "models" / "cad-parameters.json").read_text())["parameters"].items()
        }
        cls.ledger = json.loads((ROOT / "models" / "tolerance-stackup.json").read_text())

    def test_band_slot_stack_is_derived_from_dimensions(self):
        """Check nominal and worst-case band-to-slot limits from the fixture dimensions."""
        result = calculate_stackups(self.parameters, self.ledger)["roller_band_to_wall_slot"]
        self.assertAlmostEqual(result["nominal"], 0.0)
        self.assertAlmostEqual(result["worst_case_min"], -0.25)
        self.assertAlmostEqual(result["worst_case_max"], 0.25)

    def test_changing_tolerance_changes_reported_limits(self):
        """Verify increasing one local slot tolerance widens its calculated interval."""
        ledger = copy.deepcopy(self.ledger)
        ledger["interfaces"]["roller_band_to_wall_slot"]["slot_width_tolerance"] = 0.20
        result = calculate_stackups(self.parameters, ledger)["roller_band_to_wall_slot"]
        self.assertAlmostEqual(result["worst_case_min"], -0.30)
        self.assertAlmostEqual(result["worst_case_max"], 0.30)

    def test_axial_alignment_is_calculated_from_tolerance_inputs(self):
        """Check axial alignment is derived from the two source position tolerances."""
        result = calculate_stackups(self.parameters, self.ledger)["band_to_slot_axial_alignment"]
        self.assertAlmostEqual(result["worst_case_absolute_offset"], 0.25)

    def test_seal_interfaces_use_current_cad_dimensions_and_worst_case_bounds(self):
        """Assert both seal interfaces use current dimensions and expected worst-case bounds."""
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
        """Vary each shared feature tolerance independently and verify only dependent stacks widen."""
        baseline = calculate_stackups(self.parameters, copy.deepcopy(self.ledger))
        affected_by_tolerance = {
            "spindle_pin_diameter": (
                "spindle_pin_to_bearing_bore",
                "spindle_pin_to_elastomer_seal",
            ),
            "bearing_bore_diameter": (
                "spindle_pin_to_bearing_bore",
                "elastomer_seal_to_bearing_bore",
            ),
        }
        for name in (
            "spindle_pin_to_bearing_bore",
            "spindle_pin_to_elastomer_seal",
            "elastomer_seal_to_bearing_bore",
        ):
            self.assertGreater(
                baseline[name]["worst_case_max"] - baseline[name]["nominal"],
                0.0,
            )

        for tolerance_name, affected_stacks in affected_by_tolerance.items():
            updated_ledger = copy.deepcopy(self.ledger)
            updated_ledger["shared_tolerances"][tolerance_name] = 0.10
            updated = calculate_stackups(self.parameters, updated_ledger)
            for name in affected_stacks:
                self.assertGreater(
                    updated[name]["worst_case_max"],
                    baseline[name]["worst_case_max"],
                    f"{tolerance_name} should widen {name}",
                )

    def test_pin_seal_sign_convention_reports_interference_and_clearance(self):
        """Verify the sign convention and mixed-outcome classification for pin-to-seal fits."""
        self.assertEqual(_pin_seal_interpretation(0.05, 0.35), "INTERFERENCE")
        self.assertEqual(_pin_seal_interpretation(-0.35, -0.05), "CLEARANCE")
        self.assertEqual(
            _pin_seal_interpretation(-0.05, 0.05),
            "INTERFERENCE_AND_CLEARANCE_POSSIBLE",
        )

    def test_near_zero_minimum_is_classified_at_report_precision(self):
        """Treat floating-point residue that prints as zero as a line-to-line boundary."""
        self.assertEqual(
            _pin_seal_interpretation(1.7e-16, 0.35),
            "INTERFERENCE_OR_LINE_TO_LINE",
        )
        self.assertEqual(
            _pin_seal_interpretation(-0.35, -1.7e-16),
            "CLEARANCE_OR_LINE_TO_LINE",
        )

    def test_report_uses_pin_seal_classification(self):
        """Assert the user-facing report emits the expected pin-to-seal interference label."""
        report = io.StringIO()
        with redirect_stdout(report):
            self.assertEqual(main(), 0)
        self.assertIn(
            "- spindle_pin_to_elastomer_seal: nominal 0.200 mm; "
            "0.050 to 0.350 mm [INTERFERENCE]",
            report.getvalue(),
        )

    def test_negative_tolerance_is_rejected(self):
        """Reject negative tolerance inputs rather than calculating misleading bounds."""
        ledger = copy.deepcopy(self.ledger)
        ledger["interfaces"]["roller_band_to_wall_slot"]["slot_width_tolerance"] = -0.01
        with self.assertRaises(ValueError):
            calculate_stackups(self.parameters, ledger)


if __name__ == "__main__":
    unittest.main()
