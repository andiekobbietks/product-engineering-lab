"""
Illustrative Sand3D proxy for the GB2591502A hair-applicator architecture.

This is not official Nyfasi CAD, a verified retail reconstruction, or
manufacturing geometry. The patent supports the existence of component types
and some embodiment details; all unverified dimensions and shapes below are
explicit placeholders. The slotted wall is represented by a flat proxy, not
the disclosed curved wall profile.
"""
from pathlib import Path
import sand3d as s3d

# Millimetres. Values marked as proxies are not manufacturing specifications.
PARAMS = {
    "housing_w": 110.0,       # placeholder envelope
    "housing_d": 68.0,        # placeholder envelope
    "lower_shell_h": 14.0,    # placeholder
    "upper_shell_h": 12.0,    # placeholder
    "reservoir_w": 64.0,      # placeholder
    "reservoir_d": 36.0,      # placeholder
    "reservoir_h": 8.0,       # placeholder
    "roller_d": 24.0,         # placeholder, not measured
    "roller_len": 82.0,       # placeholder, not measured
    "tooth_count": 8,         # eight teeth described in the patent embodiment
    "tooth_width": 5.0,       # approx. 5 mm described for the embodiment
    "tooth_length": 10.0,     # approx. twice the stated width; schematic
    "tooth_height": 12.0,     # placeholder
    "tooth_pitch": 15.0,      # derived illustrative spacing; verify convention
    "wall_w": 104.0,          # placeholder
    "wall_d": 8.0,            # placeholder; flat proxy for curved wall
    "wall_h": 12.0,           # placeholder
    "slot_w": 2.0,            # placeholder, not patent-derived
    "exploded_gap": 18.0,
}


def build_research_assembly(exploded=True):
    p = PARAMS
    gap = p["exploded_gap"] if exploded else 0.0

    lower = s3d.box("lower_housing_proxy", p["housing_w"], p["housing_d"], p["lower_shell_h"])
    s3d.material(lower, "plastic", color="#34383d")

    upper = s3d.at(
        s3d.box("upper_housing_proxy", p["housing_w"], p["housing_d"], p["upper_shell_h"]),
        z=p["lower_shell_h"] + gap,
    )
    s3d.material(upper, "plastic", color="#555b62")

    reservoir = s3d.at(
        s3d.box("reservoir_volume_proxy", p["reservoir_w"], p["reservoir_d"], p["reservoir_h"]),
        z=p["lower_shell_h"] + (gap / 2) + 2,
    )
    s3d.material(reservoir, "glass", color="#8bbac8", opacity=0.45)

    # Patent describes a roller seated against a curved wall. This cylindrical
    # proxy is pulled forward from the housing for an exploded presentation.
    roller = s3d.at(
        s3d.cylinder("roller_drum_proxy", p["roller_d"], p["roller_len"]),
        x=0,
        y=p["housing_d"] / 2 + p["roller_d"] / 2 + gap,
        z=p["lower_shell_h"] / 2,
        rx=90,
    )
    s3d.material(roller, "rubber", color="#626a70")

    # A flat slotted carrier stands in for the patent's curved wall. Seven
    # slots are cut between eight blade-like teeth; curvature is not modelled.
    wall = s3d.box("flat_slotted_wall_proxy", p["wall_w"], p["wall_d"], p["wall_h"])
    slot_tools = []
    for i in range(p["tooth_count"] - 1):
        x = (i - (p["tooth_count"] - 2) / 2) * p["tooth_pitch"]
        slot_tools.append(
            s3d.at(
                s3d.box(f"slot_tool_{i + 1:02d}", p["slot_w"], p["wall_d"] + 2, p["wall_h"] + 2),
                x=x,
                z=-1,
            )
        )
    s3d.cut(wall, *slot_tools)
    wall = s3d.at(wall, z=p["lower_shell_h"] + p["wall_h"] + gap)
    s3d.material(wall, "plastic", color="#d7d9dc")

    teeth = []
    for i in range(p["tooth_count"]):
        x = (i - (p["tooth_count"] - 1) / 2) * p["tooth_pitch"]
        tooth = s3d.at(
            s3d.box(f"blade_tooth_{i + 1:02d}", p["tooth_width"], p["tooth_length"], p["tooth_height"]),
            x=x,
            y=p["housing_d"] / 2 + p["tooth_length"] / 2 + gap,
            z=p["lower_shell_h"] + p["wall_h"] + gap,
        )
        teeth.append(tooth)
    comb = s3d.group("comb_and_wall_proxy", wall, *teeth)
    s3d.material(comb, "plastic", color="#e2e4e7")

    return s3d.assembly(
        "hair_applicator_patent_architecture_research_proxy",
        lower,
        upper,
        reservoir,
        roller,
        comb,
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
