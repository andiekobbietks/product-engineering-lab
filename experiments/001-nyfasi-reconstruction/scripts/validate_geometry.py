"""Check geometric consistency of the patent-led CAD proxy without Sand3D."""
from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[1]
PARAMETER_FILE = ROOT / "models" / "cad-parameters.json"


def main():
    records = json.loads(PARAMETER_FILE.read_text(encoding="utf-8"))["parameters"]
    p = {name: item["value"] for name, item in records.items()}
    errors = []

    roller_radius = p["roller_d"] / 2
    seat_radius = roller_radius + p["roller_seat_clearance"]
    outer_radius = seat_radius + p["wall_thickness"]
    tooth_span = (p["tooth_count"] - 1) * p["tooth_pitch"] + p["tooth_width"]
    slot_count = p["tooth_count"] - 1
    clear_gap = p["tooth_pitch"] - p["tooth_width"]

    if p["wall_segment_angle_deg"] != 180:
        errors.append("Current Sand3D wall construction supports the 180-degree Figure 6B embodiment only.")
    if p["wall_segment_angle_deg"] <= 90:
        errors.append("Patent-described wall segment angle must be greater than 90 degrees.")
    if p["roller_seat_clearance"] < 0:
        errors.append("Roller seat clearance cannot be negative.")
    if p["wall_thickness"] <= 0:
        errors.append("Wall thickness must be positive.")
    if not (outer_radius > seat_radius > roller_radius):
        errors.append("Expected outer wall radius > seat radius > roller radius.")
    if p["wall_len"] < tooth_span:
        errors.append(
            f"Wall length {p['wall_len']} mm is shorter than the tooth-row envelope {tooth_span} mm."
        )
    if p["roller_len"] < p["wall_len"]:
        errors.append("Roller length must be at least the curved wall length in this proxy.")
    if slot_count < 1:
        errors.append("At least two teeth are required to create an inter-tooth slot.")
    if p["slot_w"] <= 0 or p["slot_w"] >= clear_gap:
        errors.append("Slot width must be positive and smaller than the assumed clear tooth gap.")
    if p["tooth_pitch"] <= p["tooth_width"]:
        errors.append("Tooth pitch must exceed tooth width to leave a clear gap.")

    if errors:
        print("Curved-wall geometry validation FAILED:")
        for error in errors:
            print(f"- {error}")
        return 1

    print(
        "Curved-wall geometry checks passed: "
        f"{p['tooth_count']} teeth, {slot_count} inter-tooth arc slots, "
        f"{p['wall_segment_angle_deg']} degree wall arc, "
        f"{seat_radius:.2f} mm seat radius, {outer_radius:.2f} mm outer radius, "
        f"{tooth_span:.2f} mm tooth-row envelope."
    )
    print("These are internal consistency checks, not dimensional or manufacturing validation.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
