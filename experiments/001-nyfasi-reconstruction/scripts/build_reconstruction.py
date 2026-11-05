"""Patent-led complete roller mechanism research proxy; not production CAD."""
from pathlib import Path
import json
import sand3d as s3d

HERE = Path(__file__).resolve().parent
PARAMETER_FILE = HERE.parent / "models" / "cad-parameters.json"
RECORDS = json.loads(PARAMETER_FILE.read_text(encoding="utf-8"))["parameters"]
P = {name: record["value"] for name, record in RECORDS.items()}


def cylinder_x(name, diameter, length, x=0, y=0, z=0):
    return s3d.at(s3d.cylinder(name, diameter, length), x=x, y=y, z=z, ry=90)


def annular_band(name, outer_d, inner_d, width, x, y, z):
    ring = s3d.cut(
        s3d.cylinder(name + "_outer", outer_d, width),
        s3d.cylinder(name + "_bore", inner_d, width + 0.4),
    )
    return s3d.at(ring, x=x, y=y, z=z, ry=90)


def build_curved_wall():
    radius = P["roller_d"] / 2 + P["roller_seat_clearance"]
    outer_radius = radius + P["wall_thickness"]
    length = P["wall_len"]
    if P["wall_segment_angle_deg"] != 180:
        raise ValueError("Only the 180-degree Figure 6B embodiment is implemented.")
    outer = s3d.cylinder("curved_wall_outer_stock", outer_radius * 2, length)
    inner = s3d.cylinder("roller_seat_inner_tool", radius * 2, length + 2)
    half_tool = s3d.at(
        s3d.box("remove_upper_half_tool", outer_radius + 2, outer_radius * 2 + 2, length + 2),
        x=-(outer_radius + 2) / 2,
    )
    slots = []
    count = P["tooth_count"] - 1
    for i in range(count):
        x = (i - (count - 1) / 2) * P["tooth_pitch"]
        slots.append(s3d.at(
            s3d.box(f"arcuate_slot_tool_{i+1:02d}", outer_radius + 2, outer_radius * 2 + 2, P["slot_w"]),
            x=(outer_radius + 2) / 2, z=x,
        ))
    wall = s3d.cut(outer, inner, half_tool, *slots)
    wall = s3d.at(wall, y=P["housing_d"] / 2, z=-P["lower_shell_h"] / 2, ry=90)
    s3d.material(wall, "plastic", color="#d7d9dc")
    return wall


def build_roller_mechanism():
    y, z = P["housing_d"] / 2, -P["lower_shell_h"] / 2
    length = P["roller_len"]
    core = cylinder_x("roller_smooth_core_and_sealing_lands", P["roller_core_d"], length, y=y, z=z)
    s3d.material(core, "rubber", color="#59636b")
    bands = []
    n = P["roller_band_count"]
    for i in range(n):
        x = (i - (n - 1) / 2) * P["tooth_pitch"]
        band = annular_band(
            f"roller_textured_circumferential_band_{i+1:02d}",
            P["roller_d"], P["roller_core_d"] - 0.2,
            P["roller_band_width"], x, y, z,
        )
        s3d.material(band, "rubber", color="#a9b0b5")
        bands.append(band)
    end_walls, pins = [], []
    end_x = length / 2 - P["roller_endwall_t"] / 2
    pin_x = length / 2 + P["spindle_pin_len"] / 2
    for side, sign in (("left", -1), ("right", 1)):
        disc = cylinder_x(f"roller_{side}_end_wall", P["roller_endwall_d"], P["roller_endwall_t"], sign * end_x, y, z)
        pin = cylinder_x(f"roller_{side}_spindle_pin", P["spindle_pin_d"], P["spindle_pin_len"], sign * pin_x, y, z)
        s3d.material(disc, "plastic", color="#3d454b")
        s3d.material(pin, "plastic", color="#c5cbd0")
        end_walls.append(disc)
        pins.append(pin)
    return s3d.group("roller_mechanism", core, *bands, *end_walls, *pins)



def build_elastomeric_seals():
    """Schematic shaft seals; dimensions are placeholders, not product evidence."""
    seals = []
    y, z = P["housing_d"] / 2, -P["lower_shell_h"] / 2
    x = P["roller_len"] / 2 + P["roller_endwall_t"] / 2
    for side, sign in (("left", -1), ("right", 1)):
        seal = annular_band(
            f"{side}_elastomeric_spindle_seal",
            P["seal_outer_d"], P["seal_inner_d"],
            P["seal_axial_width"], sign * x, y, z,
        )
        s3d.material(seal, "rubber", color="#30383c")
        seals.append(seal)
    return s3d.group("elastomeric_spindle_seals_research_proxy", *seals)


def build_housing_retention_features():
    y, z = P["housing_d"] / 2, -P["lower_shell_h"] / 2
    x_support = P["roller_len"] / 2 + P["spindle_pin_len"] / 2
    supports = []
    for side, sign in (("left", -1), ("right", 1)):
        block = s3d.at(
            s3d.box(f"{side}_spindle_bearing_support_stock",
                    P["bearing_block_w"], P["bearing_block_d"], P["bearing_block_h"]),
            x=sign * x_support, y=y, z=z,
        )
        bore = cylinder_x(f"{side}_spindle_bearing_bore_tool",
                          P["spindle_pin_d"] + 2 * P["bearing_bore_clearance"],
                          P["bearing_block_w"] + 1, sign * x_support, y, z)
        support = s3d.cut(block, bore)
        s3d.material(support, "plastic", color="#343b42")
        supports.append(support)
    tabs = []
    for i in range(P["snap_tab_count"]):
        x = (i - (P["snap_tab_count"] - 1) / 2) * (P["housing_w"] - 24)
        tab = s3d.at(s3d.box(f"housing_snap_fit_tab_{i+1:02d}",
                             P["snap_tab_w"], P["snap_tab_d"], P["snap_tab_h"]),
                     x=x, z=P["lower_shell_h"] / 2 + P["snap_tab_h"] / 2)
        s3d.material(tab, "plastic", color="#e3a44b")
        tabs.append(tab)
    return s3d.group("housing_bearings_and_snap_fit_proxies", *supports, *tabs)


def build_research_assembly(exploded=True):
    gap = P["exploded_gap"] if exploded else 0
    lower = s3d.box("lower_housing_proxy", P["housing_w"], P["housing_d"], P["lower_shell_h"])
    upper = s3d.at(
        s3d.box("upper_housing_proxy", P["housing_w"], P["housing_d"], P["upper_shell_h"]),
        z=(P["lower_shell_h"] + P["upper_shell_h"]) / 2 + gap,
    )
    reservoir = s3d.at(
        s3d.box("reservoir_volume_proxy", P["reservoir_w"], P["reservoir_d"], P["reservoir_h"]),
        z=P["lower_shell_h"] / 2,
    )
    s3d.material(lower, "plastic", color="#34383d")
    s3d.material(upper, "plastic", color="#555b62")
    s3d.material(reservoir, "glass", color="#8bbac8", opacity=0.45)
    wall = build_curved_wall()
    teeth = []
    outer_radius = P["roller_d"] / 2 + P["roller_seat_clearance"] + P["wall_thickness"]
    for i in range(P["tooth_count"]):
        x = (i - (P["tooth_count"] - 1) / 2) * P["tooth_pitch"]
        tooth = s3d.at(
            s3d.box(f"blade_tooth_{i+1:02d}", P["tooth_width"], P["tooth_length"], P["tooth_height"]),
            x=x, y=P["housing_d"] / 2,
            z=-P["lower_shell_h"] / 2 - outer_radius - P["tooth_height"] / 2,
        )
        teeth.append(tooth)
    comb = s3d.group("curved_wall_and_blade_teeth", wall, *teeth)
    s3d.material(comb, "plastic", color="#e2e4e7")
    return s3d.assembly(
        "hair_applicator_complete_roller_mechanism_research_proxy",
        lower, upper, reservoir, build_roller_mechanism(), comb,
        build_housing_retention_features(),
    )


def main():
    model = build_research_assembly(exploded=True)
    output = HERE.parent / "output"
    output.mkdir(exist_ok=True)
    s3d.export(model, str(output / "hair_applicator_complete_roller_exploded.glb"))
    s3d.export(model, str(output / "hair_applicator_complete_roller_exploded.obj"))
    print("Wrote complete roller-mechanism research exports to:", output.resolve())


if __name__ == "__main__":
    main()
