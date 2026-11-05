"""Preliminary worst-case interface checks for the research assembly."""
from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[1]
DATA = json.loads((ROOT / "models" / "tolerance-stackup.json").read_text(encoding="utf-8"))

def main():
    print("PRELIMINARY TOLERANCE / INTERACTION REPORT")
    print("Status:", DATA["status"])
    print("All dimensions are assumptions; this is not a production tolerance analysis.\n")
    failed = False
    for name, item in DATA["interfaces"].items():
        lo, hi = item["worst_case_min"], item["worst_case_max"]
        print(f"- {name}: worst-case {lo:.3f} to {hi:.3f} mm [{item['status']}]")
        if name == "roller_band_to_wall_slot" and lo < 0:
            failed = True
    axial = DATA["axial_alignment"]
    print(f"- band/slot centre alignment: ±{axial['worst_case_absolute_offset']:.3f} mm [{axial['status']}]")
    if failed:
        print("\nREVIEW FLAG: band-to-slot width stack permits up to 0.25 mm interference.")
        print("Do not interpret nominal alignment as verified running clearance.")
    print("\nRelease gates:")
    for gate in DATA["release_gate"]:
        print("  *", gate)
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
