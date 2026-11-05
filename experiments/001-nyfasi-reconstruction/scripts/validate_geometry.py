"""Internal consistency checks for the complete patent-led CAD proxy."""
from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[1]
P = {k: v["value"] for k, v in json.loads((ROOT / "models" / "cad-parameters.json").read_text())["parameters"].items()}


def main():
    errors = []
    roller_r = P["roller_d"] / 2
    seat_r = roller_r + P["roller_seat_clearance"]
    outer_r = seat_r + P["wall_thickness"]
    tooth_span = (P["tooth_count"] - 1) * P["tooth_pitch"] + P["tooth_width"]
    clear_gap = P["tooth_pitch"] - P["tooth_width"]
    band_span = (P["roller_band_count"] - 1) * P["tooth_pitch"] + P["roller_band_width"]
    support_x = P["roller_len"] / 2 + P["roller_endwall_t"] + P["spindle_pin_len"] / 2

    checks = [
        (P["wall_segment_angle_deg"] == 180, "Only the 180-degree Figure 6B wall is implemented."),
        (outer_r > seat_r > roller_r, "Expected outer wall radius > seat radius > roller radius."),
        (P["wall_len"] >= tooth_span, "Wall must span the tooth row."),
        (P["housing_wall_t"] > 0 and P["housing_wall_t"] < min(P["lower_shell_h"], P["upper_shell_h"]) / 2, "Housing shell wall thickness is invalid."),
        (P["housing_corner_r"] > P["housing_wall_t"], "Housing corner radius should exceed shell wall thickness."),
        (P["reservoir_corner_r"] > 0, "Reservoir corner radius must be positive."),
        (P["roller_axis_y"] == P["housing_d"] / 2, "Roller axis Y datum must match the current housing-centre convention."),
        (P["roller_knurl_pitch"] > 0, "Knurl pitch must be positive."),
        (P["gasket_section_d"] > 0 and P["gasket_inset"] > 0, "Gasket proxy dimensions must be positive."),
        (P["tooth_corner_r"] >= 0, "Tooth corner radius cannot be negative."),
        (P["snap_tab_pitch"] > 0, "Snap-tab pitch must be positive."),
        (P["roller_len"] >= P["wall_len"], "Roller must span the wall."),
        (0 < P["slot_w"] < clear_gap, "Slot width must be positive and below tooth clear gap."),
        (P["roller_core_d"] < P["roller_d"], "Smooth core must be smaller than textured roller OD."),
        (P["roller_band_count"] == P["tooth_count"] - 1, "Model expects one textured band per inter-tooth slot."),
        (0 < P["roller_band_width"] < clear_gap, "Textured band width must fit the assumed clear gap."),
        (band_span <= P["roller_len"], "Textured band row exceeds roller length."),
        (P["roller_endwall_d"] > P["roller_d"] and P["roller_endwall_t"] > 0, "End walls must exceed roller OD and have positive thickness."),
        (P["spindle_pin_d"] > 0 and P["spindle_pin_len"] > 0, "Spindle pins need positive dimensions."),
        (P["bearing_bore_clearance"] >= 0, "Bearing clearance cannot be negative."),
        (P["spindle_pin_d"] + 2 * P["bearing_bore_clearance"] < min(P["bearing_block_d"], P["bearing_block_h"]), "Bearing bore does not fit its support block."),
        (support_x + P["bearing_block_w"] / 2 <= P["housing_w"] / 2, "Bearing supports exceed housing envelope."),
        (P["snap_tab_count"] >= 1 and min(P["snap_tab_w"], P["snap_tab_d"], P["snap_tab_h"]) > 0, "Snap-fit proxy dimensions/count must be positive."),
        (abs(P["tooth_root_z"] - (P["roller_axis_z"] - outer_r - P["tooth_height"])) < 1e-6, "Tooth root datum must remain tied to the roller seat envelope."),
    ]
    errors.extend(message for ok, message in checks if not ok)
    if errors:
        print("Complete roller geometry validation FAILED:")
        for error in errors:
            print("- " + error)
        return 1
    print(
        f"Complete roller checks passed: {P['roller_band_count']} textured bands, "
        "smooth lands, 2 end walls, 2 spindle pins, 2 bearing supports, "
        f"{P['snap_tab_count']} snap-fit tabs."
    )
    print("Checks cover internal consistency only, not product or manufacturing validation.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
