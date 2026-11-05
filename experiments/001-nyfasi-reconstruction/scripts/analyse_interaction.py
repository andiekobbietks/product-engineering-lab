"""Calculate preliminary interface stack-ups from the CAD parameter and tolerance ledgers."""
from __future__ import annotations

import json
import math
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
PARAMETER_FILE = ROOT / "models" / "cad-parameters.json"
TOLERANCE_FILE = ROOT / "models" / "tolerance-stackup.json"
# The report renders dimensions to three decimal places. Values within half a
# displayed unit are classified as touching the zero boundary.
REPORT_ZERO_TOLERANCE_MM = 0.0005


def load_inputs() -> tuple[dict[str, float], dict[str, Any]]:
    """Load nominal CAD dimensions and assumed tolerance inputs from their source ledgers."""
    parameter_records = json.loads(PARAMETER_FILE.read_text(encoding="utf-8"))["parameters"]
    parameters = {name: float(record["value"]) for name, record in parameter_records.items()}
    ledger = json.loads(TOLERANCE_FILE.read_text(encoding="utf-8"))
    return parameters, ledger


def _tolerance_sum(values: dict[str, Any], *keys: str) -> float:
    """Return a validated arithmetic worst-case sum for the requested tolerance inputs."""
    tolerances = [float(values[key]) for key in keys]
    if any(not math.isfinite(value) or value < 0 for value in tolerances):
        raise ValueError(f"Tolerance inputs must be finite and non-negative: {keys}")
    return sum(tolerances)


def calculate_stackups(parameters: dict[str, float], ledger: dict[str, Any]) -> dict[str, dict[str, float]]:
    """Calculate nominal and worst-case interface clearances from current source dimensions."""
    interfaces = ledger["interfaces"]

    seat = interfaces["roller_to_curved_seat"]
    seat_nominal = parameters["roller_seat_clearance"]
    seat_delta = _tolerance_sum(seat, "roller_radius_tolerance", "seat_radius_tolerance")

    band = interfaces["roller_band_to_wall_slot"]
    band_nominal = parameters["slot_w"] - parameters["roller_band_width"]
    band_delta = _tolerance_sum(band, "slot_width_tolerance", "band_width_tolerance")

    shared = ledger["shared_tolerances"]
    bearing_nominal = 2 * parameters["bearing_bore_clearance"]
    bearing_delta = _tolerance_sum(shared, "spindle_pin_diameter", "bearing_bore_diameter")

    pin_seal = interfaces["spindle_pin_to_elastomer_seal"]
    pin_seal_nominal = parameters["spindle_pin_d"] - parameters["seal_inner_d"]
    pin_seal_delta = _tolerance_sum(shared, "spindle_pin_diameter") + _tolerance_sum(
        pin_seal, "seal_bore_tolerance"
    )

    seal_bore = interfaces["elastomer_seal_to_bearing_bore"]
    bearing_bore_diameter = parameters["spindle_pin_d"] + 2 * parameters["bearing_bore_clearance"]
    seal_bore_nominal = bearing_bore_diameter - parameters["seal_outer_d"]
    seal_bore_delta = _tolerance_sum(
        shared, "bearing_bore_diameter"
    ) + _tolerance_sum(seal_bore, "seal_outer_diameter_tolerance")

    results = {
        "roller_to_curved_seat": (seat_nominal, seat_delta),
        "roller_band_to_wall_slot": (band_nominal, band_delta),
        "spindle_pin_to_bearing_bore": (bearing_nominal, bearing_delta),
        "spindle_pin_to_elastomer_seal": (pin_seal_nominal, pin_seal_delta),
        "elastomer_seal_to_bearing_bore": (seal_bore_nominal, seal_bore_delta),
    }
    calculated = {
        name: {"nominal": nominal, "worst_case_min": nominal - delta, "worst_case_max": nominal + delta}
        for name, (nominal, delta) in results.items()
    }

    axial = ledger["axial_alignment"]
    axial_delta = _tolerance_sum(axial, "band_position_tolerance", "slot_position_tolerance")
    calculated["band_to_slot_axial_alignment"] = {
        "nominal": 0.0,
        "worst_case_min": -axial_delta,
        "worst_case_max": axial_delta,
        "worst_case_absolute_offset": axial_delta,
    }
    return calculated


def _pin_seal_interpretation(
    low: float,
    high: float,
    zero_tolerance: float = REPORT_ZERO_TOLERANCE_MM,
) -> str:
    """Classify pin-minus-seal-bore results, treating report-rounded zero as line-to-line."""
    if zero_tolerance < 0:
        raise ValueError("zero_tolerance must be non-negative")
    if abs(low) <= zero_tolerance:
        low = 0.0
    if abs(high) <= zero_tolerance:
        high = 0.0

    if low > 0:
        return "INTERFERENCE"
    if high < 0:
        return "CLEARANCE"
    if low == 0 and high == 0:
        return "LINE_TO_LINE"
    if low < 0 < high:
        return "INTERFERENCE_AND_CLEARANCE_POSSIBLE"
    if low == 0:
        return "INTERFERENCE_OR_LINE_TO_LINE"
    return "CLEARANCE_OR_LINE_TO_LINE"


def main() -> int:
    """Print a reproducible tolerance report and flag any calculated interference."""
    parameters, ledger = load_inputs()
    calculated = calculate_stackups(parameters, ledger)
    print("PRELIMINARY TOLERANCE / INTERACTION REPORT")
    print("Status:", ledger["status"])
    print("All dimensions are assumptions; this is not a production tolerance analysis.\\n")

    for name, result in calculated.items():
        if name == "band_to_slot_axial_alignment":
            print(
                f"- {name}: ±{result['worst_case_absolute_offset']:.3f} mm "
                "[MEASUREMENT_AND_DYNAMIC_CLEARANCE_CHECK]"
            )
            continue
        low, high = result["worst_case_min"], result["worst_case_max"]
        if name == "spindle_pin_to_elastomer_seal":
            flag = _pin_seal_interpretation(low, high)
        else:
            flag = "INTERFERENCE_POSSIBLE" if low < 0 else "POSITIVE_IN_THIS_ASSUMED_STACK"
        print(f"- {name}: nominal {result['nominal']:.3f} mm; {low:.3f} to {high:.3f} mm [{flag}]")

    band_result = calculated["roller_band_to_wall_slot"]
    if band_result["worst_case_min"] < 0:
        print(
            "\\nREVIEW FLAG: calculated band-to-slot stack permits "
            f"{abs(band_result['worst_case_min']):.3f} mm interference."
        )
        print("Do not interpret nominal alignment as verified running clearance.")

    print("\\nRelease gates:")
    for gate in ledger["release_gate"]:
        print("  *", gate)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
