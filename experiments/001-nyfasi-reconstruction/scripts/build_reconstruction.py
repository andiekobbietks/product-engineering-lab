"""
Illustrative component-level detangler research assembly.

This is a parametric experiment, not Nyfasi CAD and not a claim about actual
internal construction. All dimensions below are placeholders.
Run with a Sand3D-supported Python (3.11 or 3.13) and Blender bpy runtime.
"""
from pathlib import Path
import sand3d as s3d

# Explicit placeholder parameters (millimetres), not measured specifications.
PARAMS = {
    "housing_w": 110.0,
    "housing_d": 68.0,
    "housing_h": 34.0,
    "comb_w": 104.0,
    "comb_d": 58.0,
    "comb_t": 5.0,
    "roller_d": 24.0,
    "roller_len": 82.0,
    "tooth_count": 11,
    "tooth_d": 2.0,
    "tooth_h": 14.0,
    "exploded_gap": 18.0,
}


def build_research_assembly(exploded=True):
    p = PARAMS
    gap = p["exploded_gap"] if exploded else 0.0

    housing = s3d.box("main_housing_proxy", p["housing_w"], p["housing_d"], p["housing_h"])
    s3d.material(housing, "plastic", color="#34383d")

    comb_plate = s3d.at(
        s3d.box("comb_carrier_proxy", p["comb_w"], p["comb_d"], p["comb_t"]),
        z=p["housing_h"] + gap,
    )
    teeth = []
    usable = p["comb_w"] * 0.78
    for i in range(p["tooth_count"]):
        x = -usable / 2 + i * usable / (p["tooth_count"] - 1)
        tooth = s3d.at(
            s3d.cylinder(f"guide_tooth_{i + 1:02d}", p["tooth_d"], p["tooth_h"]),
            x=x,
            y=0,
            z=p["housing_h"] + p["comb_t"] + gap,
        )
        teeth.append(tooth)
    comb = s3d.group("comb_guide_proxy", comb_plate, *teeth)
    s3d.material(comb, "plastic", color="#d7d9dc")

    roller = s3d.at(
        s3d.cylinder("roller_proxy", p["roller_d"], p["roller_len"]),
        x=0,
        y=0,
        z=-(p["roller_len"] + gap),
    )
    s3d.material(roller, "rubber", color="#555b62")

    reservoir = s3d.at(
        s3d.box("reservoir_proxy", 72, 28, 18),
        x=0,
        y=p["housing_d"] / 2 + 14 + gap,
        z=0,
    )
    s3d.material(reservoir, "plastic", color="#8bbac8", opacity=0.55)

    return s3d.assembly(
        "nyfasi_deluxe_detangler_research_proxy",
        housing,
        comb,
        roller,
        reservoir,
    )


def main():
    model = build_research_assembly(exploded=True)
    output = Path("output")
    output.mkdir(exist_ok=True)
    s3d.export(model, str(output / "nyfasi_research_exploded.glb"))
    s3d.export(model, str(output / "nyfasi_research_exploded.obj"))
    print("Wrote illustrative research exports to:", output.resolve())


if __name__ == "__main__":
    main()
