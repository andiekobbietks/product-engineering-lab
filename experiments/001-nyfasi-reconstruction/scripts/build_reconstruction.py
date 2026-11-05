"""
Illustrative Sand3D proxy for the GB2591502A / CN115003190B hair-applicator
patent-family architecture.

Not official Nyfasi CAD, a verified retail reconstruction, or manufacturing
geometry. Numeric parameters are loaded from models/cad-parameters.json, where
each value has provenance, evidence IDs, confidence and an explanatory note.
The curved wall is still represented by a flat proxy.
"""
from pathlib import Path
import json
import sand3d as s3d

HERE = Path(__file__).resolve().parent
PARAMETER_FILE = HERE.parent / "models" / "cad-parameters.json"
PARAMETER_RECORDS = json.loads(PARAMETER_FILE.read_text(encoding="utf-8"))["parameters"]
PARAMS = {name: record["value"] for name, record in PARAMETER_RECORDS.items()}


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
        z=p["lower_shell_h"] + (gap / 2) - (p["reservoir_h"] / 2),
    )
    s3d.material(reservoir, "glass", color="#8bbac8", opacity=0.45)

    # Patent family describes a roller seated against a curved wall. This
    # cylinder is a schematic proxy; diameter is selected inside a disclosed
    # radius range, not a measured retail dimension.
    roller = s3d.at(
        s3d.cylinder("roller_drum_proxy", p["roller_d"], p["roller_len"]),
        x=0,
        y=p["housing_d"] / 2 + p["roller_d"] / 2 + gap + p["roller_len"],
        z=p["lower_shell_h"] / 2,
        rx=-90,
    )
    s3d.material(roller, "rubber", color="#626a70")

    # Flat wall proxy only. The patent describes a curved wall and arcuate
    # through-slots; this script does not claim to reproduce that geometry.
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
    wall = s3d.at(
        wall,
        y=p["housing_d"] / 2 + p["wall_d"] / 2 + gap,
        z=p["lower_shell_h"] + p["wall_h"] + gap,
    )
    s3d.material(wall, "plastic", color="#d7d9dc")

    teeth = []
    for i in range(p["tooth_count"]):
        x = (i - (p["tooth_count"] - 1) / 2) * p["tooth_pitch"]
        tooth = s3d.at(
            s3d.box(f"blade_tooth_{i + 1:02d}", p["tooth_width"], p["tooth_length"], p["tooth_height"]),
            x=x,
            y=p["housing_d"] / 2 + p["wall_d"] + p["tooth_length"] / 2 + gap,
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
    output = HERE.parent / "output"
    output.mkdir(exist_ok=True)
    s3d.export(model, str(output / "hair_applicator_research_exploded.glb"))
    s3d.export(model, str(output / "hair_applicator_research_exploded.obj"))
    print("Wrote illustrative research exports to:", output.resolve())


if __name__ == "__main__":
    main()
