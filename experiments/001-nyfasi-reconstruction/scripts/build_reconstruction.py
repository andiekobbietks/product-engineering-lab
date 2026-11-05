"""
Parametric Sand3D research reconstruction of the GB2591502A / CN115003190B
hair-applicator patent-family architecture.

This is not official Nyfasi CAD, a verified retail reconstruction, or
manufacturing geometry. Numeric parameters are loaded from the provenance
ledger. The curved wall is represented as a 180-degree cylindrical shell
segment with circumferential slot cuts between adjacent teeth, based on the
patent's Figure 5 / Figure 6 disclosure.

Coordinate convention:
- X: roller axis and tooth-row direction
- Y: front-to-back body depth
- Z: vertical; the curved wall and teeth project in negative Z
- The local cylinder Z axis is rotated onto global X.
"""
from pathlib import Path
import json
import sand3d as s3d

HERE = Path(__file__).resolve().parent
PARAMETER_FILE = HERE.parent / "models" / "cad-parameters.json"
PARAMETER_RECORDS = json.loads(PARAMETER_FILE.read_text(encoding="utf-8"))["parameters"]
PARAMS = {name: record["value"] for name, record in PARAMETER_RECORDS.items()}


def _parameter(name):
    return PARAMS[name]


def build_curved_wall():
    """Build a semi-cylindrical seat and cut circumferential slots.

    The stock cylinder's local Z axis is its length. After the completed
    Boolean operations, the wall is rotated so that its axis is global X.
    Each slot is a narrow axial band cut through the retained 180-degree arc.
    """
    p = PARAMS
    roller_radius = p["roller_d"] / 2
    inner_radius = roller_radius + p["roller_seat_clearance"]
    outer_radius = inner_radius + p["wall_thickness"]
    wall_length = p["wall_len"]
    outer_diameter = outer_radius * 2
    inner_diameter = inner_radius * 2
    angle = p["wall_segment_angle_deg"]

    if angle != 180:
        raise ValueError(
            "This Sand3D clipping construction currently supports the "
            "180-degree Figure 6B embodiment only."
        )

    outer = s3d.cylinder("curved_wall_outer_stock", outer_diameter, wall_length)
    inner = s3d.cylinder("roller_seat_inner_tool", inner_diameter, wall_length + 2)

    # Cylinder local X maps to global -Z after ry=90. Remove local X<0,
    # retaining the local X>0 half, which becomes the lower/global -Z arc.
    upper_half_tool = s3d.at(
        s3d.box(
            "remove_upper_half_tool",
            outer_radius + 2,
            outer_diameter + 2,
            wall_length + 2,
        ),
        x=-(outer_radius + 2) / 2,
    )

    # One circumferential opening is placed in each clear gap between teeth.
    # Each cutter is a thin axial band spanning the full retained arc.
    slot_tools = []
    slot_count = p["tooth_count"] - 1
    for index in range(slot_count):
        axial_position = (
            index - (slot_count - 1) / 2
        ) * p["tooth_pitch"]
        slot_tools.append(
            s3d.at(
                s3d.box(
                    f"arcuate_slot_tool_{index + 1:02d}",
                    outer_radius + 2,
                    outer_diameter + 2,
                    p["slot_w"],
                ),
                x=(outer_radius + 2) / 2,
                z=axial_position,
            )
        )

    wall = s3d.cut(outer, inner, upper_half_tool, *slot_tools)
    wall = s3d.at(
        wall,
        y=p["housing_d"] / 2,
        z=-p["lower_shell_h"] / 2,
        ry=90,
    )
    s3d.material(wall, "plastic", color="#d7d9dc")
    return wall


def build_research_assembly(exploded=True):
    p = PARAMS
    gap = p["exploded_gap"] if exploded else 0.0
    roller_radius = p["roller_d"] / 2
    inner_radius = roller_radius + p["roller_seat_clearance"]
    outer_radius = inner_radius + p["wall_thickness"]
    roller_y = p["housing_d"] / 2
    roller_z = -p["lower_shell_h"] / 2

    lower = s3d.box(
        "lower_housing_proxy",
        p["housing_w"],
        p["housing_d"],
        p["lower_shell_h"],
    )
    s3d.material(lower, "plastic", color="#34383d")

    upper = s3d.at(
        s3d.box(
            "upper_housing_proxy",
            p["housing_w"],
            p["housing_d"],
            p["upper_shell_h"],
        ),
        z=(p["lower_shell_h"] + p["upper_shell_h"]) / 2 + gap,
    )
    s3d.material(upper, "plastic", color="#555b62")

    reservoir = s3d.at(
        s3d.box(
            "reservoir_volume_proxy",
            p["reservoir_w"],
            p["reservoir_d"],
            p["reservoir_h"],
        ),
        z=p["lower_shell_h"] / 2,
    )
    s3d.material(reservoir, "glass", color="#8bbac8", opacity=0.45)

    # Roller axis is aligned with the tooth row (global X).
    roller = s3d.at(
        s3d.cylinder("roller_drum_proxy", p["roller_d"], p["roller_len"]),
        y=roller_y,
        z=roller_z,
        ry=90,
    )
    s3d.material(roller, "rubber", color="#626a70")

    wall = build_curved_wall()

    # Teeth are represented as simple blade-like rectangular proxies.
    # The patent describes tapered / elliptical alternatives; those details
    # are intentionally not claimed by this first curved-wall iteration.
    teeth = []
    for index in range(p["tooth_count"]):
        x = (index - (p["tooth_count"] - 1) / 2) * p["tooth_pitch"]
        tooth = s3d.at(
            s3d.box(
                f"blade_tooth_{index + 1:02d}",
                p["tooth_width"],
                p["tooth_length"],
                p["tooth_height"],
            ),
            x=x,
            y=roller_y,
            z=roller_z - outer_radius - p["tooth_height"] / 2,
        )
        teeth.append(tooth)

    comb = s3d.group("curved_wall_and_blade_teeth", wall, *teeth)
    s3d.material(comb, "plastic", color="#e2e4e7")

    return s3d.assembly(
        "hair_applicator_patent_architecture_curved_wall_research_proxy",
        lower,
        upper,
        reservoir,
        roller,
        comb,
    )


def main():
    model = build_research_assembly(exploded=True)
    output = HERE.parent / "output"
    output.mkdir(exist_ok=True)
    s3d.export(model, str(output / "hair_applicator_curved_wall_exploded.glb"))
    s3d.export(model, str(output / "hair_applicator_curved_wall_exploded.obj"))
    print("Wrote curved-wall research exports to:", output.resolve())


if __name__ == "__main__":
    main()
