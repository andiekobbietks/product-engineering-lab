"""Evidence-led, component-first Nyfasi patent-architecture research proxy.

This is deliberately not a claim of original Nyfasi CAD or a verified retail twin.
All dimensions come from the provenance ledger; unverified values remain assumptions.
"""
from pathlib import Path
import json
import sand3d as s3d

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
PARAMETER_FILE = ROOT / "models" / "cad-parameters.json"
RECORDS = json.loads(PARAMETER_FILE.read_text(encoding="utf-8"))["parameters"]
P = {name: record["value"] for name, record in RECORDS.items()}
COMPONENTS = []


def cylinder_on_x(name, diameter, length, x=0, y=0, z=0):
    """Create an X-axis cylinder centred at (x, y, z)."""
    solid = s3d.cylinder(name, d=diameter, h=length)
    return s3d.at(solid, x=x - length / 2, y=y, z=z, ry=90)


def rounded_tray(name, width, depth, height, wall, corner):
    """Open-top, rounded rectangular housing half, built at its own origin."""
    blank = s3d.extrude(name + "_blank", s3d.rect(width, depth, r=corner), height)
    blank = s3d.at(blank, z=-height / 2)
    cavity = s3d.extrude(
        name + "_cavity_tool",
        s3d.rect(width - 2 * wall, depth - 2 * wall, r=max(0.5, corner - wall)),
        height - wall,
    )
    cavity = s3d.at(cavity, z=-height / 2 + wall)
    shell = s3d.cut(blank, cavity)
    s3d.material(shell, "plastic", color="#34383d")
    return s3d.group(name, shell)


def build_lower_housing():
    return rounded_tray(
        "lower_housing_shell_proxy",
        P["housing_w"], P["housing_d"], P["lower_shell_h"],
        P["housing_wall_t"], P["housing_corner_r"],
    )


def build_upper_housing():
    cap = rounded_tray(
        "upper_housing_shell_proxy",
        P["housing_w"], P["housing_d"], P["upper_shell_h"],
        P["housing_wall_t"], P["housing_corner_r"],
    )
    cap = s3d.at(cap, rx=180)  # invert the open face so the cap opens toward the lower shell
    s3d.material(cap, "plastic", color="#555b62")
    return cap


def build_reservoir():
    tank = s3d.extrude(
        "reservoir_body_proxy",
        s3d.rect(P["reservoir_w"], P["reservoir_d"], r=P["reservoir_corner_r"]),
        P["reservoir_h"],
    )
    tank = s3d.at(tank, z=-P["reservoir_h"] / 2)
    s3d.material(tank, "glass", color="#8bbac8", opacity=0.38)
    return s3d.group("reservoir_volume_proxy", tank)


def build_curved_wall():
    """Semi-cylindrical wall, concave roller seat and interpreted arc slots."""
    seat_radius = P["roller_d"] / 2 + P["roller_seat_clearance"]
    outer_radius = seat_radius + P["wall_thickness"]
    length = P["wall_len"]
    if P["wall_segment_angle_deg"] != 180:
        raise ValueError("This build implements only the 180-degree Figure 6B proxy.")

    outer = s3d.cylinder("curved_wall_outer_stock", d=2 * outer_radius, h=length)
    inner = s3d.cylinder("roller_seat_inner_tool", d=2 * seat_radius, h=length + 2)
    # Remove the negative-X half of the annular stock, leaving a semi-cylindrical cradle.
    half_tool = s3d.at(
        s3d.box("remove_negative_radial_half", outer_radius + 2, 2 * outer_radius + 2, length + 2),
        x=-(outer_radius + 2) / 2,
    )
    slot_tools = []
    slot_count = P["tooth_count"] - 1
    for index in range(slot_count):
        axial = (index - (slot_count - 1) / 2) * P["tooth_pitch"]
        tool = s3d.box(
            f"arc_slot_tool_{index + 1:02d}",
            outer_radius + 2, 2 * outer_radius + 2, P["slot_w"],
        )
        slot_tools.append(s3d.at(tool, x=(outer_radius + 2) / 2, z=axial))

    wall = s3d.cut(outer, inner, half_tool, *slot_tools)
    wall = s3d.at(
        wall,
        x=-length / 2,
        y=P["roller_axis_y"],
        z=P["roller_axis_z"],
        ry=90,
    )
    s3d.material(wall, "plastic", color="#d7d9dc")
    return s3d.group("semi_cylindrical_slotted_wall", wall)


def build_roller_core():
    core = cylinder_on_x(
        "roller_smooth_core_and_sealing_lands",
        P["roller_core_d"], P["roller_len"],
        y=P["roller_axis_y"], z=P["roller_axis_z"],
    )
    s3d.material(core, "rubber", color="#59636b")
    return core


def build_textured_band(index, axial_position):
    """A knurled annular band; the exposed core remains the smooth sealing land."""
    outer = s3d.knurl(
        f"roller_knurled_band_{index:02d}",
        d=P["roller_d"],
        h=P["roller_band_width"],
        pitch=P["roller_knurl_pitch"],
        straight=False,
    )
    bore = s3d.cylinder(
        f"roller_band_bore_tool_{index:02d}",
        d=P["roller_core_d"] - 0.2,
        h=P["roller_band_width"] + 0.6,
    )
    band = s3d.cut(outer, bore)
    band = s3d.at(
        band,
        x=axial_position - P["roller_band_width"] / 2,
        y=P["roller_axis_y"],
        z=P["roller_axis_z"],
        ry=90,
    )
    s3d.material(band, "rubber", color="#a9b0b5", roughness=0.82)
    return s3d.group(f"textured_annular_band_{index:02d}", band)


def build_roller_end_wall(side, sign):
    disc = cylinder_on_x(
        f"roller_{side}_end_wall",
        P["roller_endwall_d"], P["roller_endwall_t"],
        x=sign * (P["roller_len"] / 2 + P["roller_endwall_t"] / 2),
        y=P["roller_axis_y"], z=P["roller_axis_z"],
    )
    s3d.material(disc, "plastic", color="#3d454b")
    return s3d.group(f"roller_{side}_end_wall_component", disc)


def build_spindle_pin(side, sign):
    pin = cylinder_on_x(
        f"roller_{side}_spindle_pin",
        P["spindle_pin_d"], P["spindle_pin_len"],
        x=sign * (
            P["roller_len"] / 2
            + P["roller_endwall_t"]
            + P["spindle_pin_len"] / 2
        ),
        y=P["roller_axis_y"], z=P["roller_axis_z"],
    )
    s3d.material(pin, "steel", color="#c5cbd0", metallic=0.72)
    return s3d.group(f"roller_{side}_spindle_pin_component", pin)


def build_roller_mechanism():
    parts = [build_roller_core()]
    band_count = P["roller_band_count"]
    for index in range(band_count):
        axial = (index - (band_count - 1) / 2) * P["tooth_pitch"]
        parts.append(build_textured_band(index + 1, axial))
    for side, sign in (("left", -1), ("right", 1)):
        parts.append(build_roller_end_wall(side, sign))
        parts.append(build_spindle_pin(side, sign))
    return s3d.group("roller_mechanism", *parts)


def build_housing_retention_features():
    supports = []
    support_x = P["roller_len"] / 2 + P["roller_endwall_t"] + P["spindle_pin_len"] / 2
    for side, sign in (("left", -1), ("right", 1)):
        block = s3d.box(
            f"{side}_bearing_support_stock",
            P["bearing_block_w"], P["bearing_block_d"], P["bearing_block_h"],
        )
        block = s3d.at(
            block,
            x=sign * support_x,
            y=P["roller_axis_y"],
            z=P["roller_axis_z"],
        )
        bore = cylinder_on_x(
            f"{side}_bearing_bore_tool",
            P["spindle_pin_d"] + 2 * P["bearing_bore_clearance"],
            P["bearing_block_w"] + 1,
            x=sign * support_x,
            y=P["roller_axis_y"],
            z=P["roller_axis_z"],
        )
        support = s3d.cut(block, bore)
        s3d.material(support, "plastic", color="#343b42")
        supports.append(s3d.group(f"{side}_bearing_support", support))

    tabs = []
    for index in range(P["snap_tab_count"]):
        x = (index - (P["snap_tab_count"] - 1) / 2) * P["snap_tab_pitch"]
        tab = s3d.box(
            f"housing_snap_fit_tab_{index + 1:02d}",
            P["snap_tab_w"], P["snap_tab_d"], P["snap_tab_h"],
        )
        tab = s3d.at(
            tab,
            x=x,
            z=P["lower_shell_h"] / 2 + P["snap_tab_h"] / 2,
        )
        s3d.material(tab, "plastic", color="#e3a44b")
        tabs.append(tab)
    return s3d.group("housing_bearings_and_snap_fit_proxies", *supports, *tabs)


def build_comb_and_wall():
    wall = build_curved_wall()
    teeth = []
    for index in range(P["tooth_count"]):
        x = (index - (P["tooth_count"] - 1) / 2) * P["tooth_pitch"]
        tooth = s3d.extrude(
            f"blade_tooth_{index + 1:02d}",
            s3d.rect(P["tooth_width"], P["tooth_length"], r=P["tooth_corner_r"]),
            P["tooth_height"],
        )
        tooth = s3d.at(
            tooth,
            x=x,
            y=P["roller_axis_y"],
            z=P["tooth_root_z"],
        )
        s3d.material(tooth, "plastic", color="#e2e4e7")
        teeth.append(tooth)
    return s3d.group("curved_wall_and_blade_teeth", wall, *teeth)


def build_housing_gasket():
    """Separate perimeter seal proxy; section and compression remain assumptions."""
    w = P["housing_w"] - 2 * P["gasket_inset"]
    d = P["housing_d"] - 2 * P["gasket_inset"]
    path = [
        (-w / 2, -d / 2, 0),
        (w / 2, -d / 2, 0),
        (w / 2, d / 2, 0),
        (-w / 2, d / 2, 0),
    ]
    gasket = s3d.wire(
        "upper_lower_housing_perimeter_gasket",
        path=path,
        d=P["gasket_section_d"],
        closed=True,
        fillet=P["housing_corner_r"],
    )
    gasket = s3d.at(gasket, z=P["lower_shell_h"] / 2)
    s3d.material(gasket, "rubber", color="#24282c")
    return s3d.group("housing_interface_gasket_proxy", gasket)


def build_comb_teeth():
    """Eight separately named teeth, retained as a component group for export."""
    teeth = []
    for index in range(P["tooth_count"]):
        x = (index - (P["tooth_count"] - 1) / 2) * P["tooth_pitch"]
        tooth = s3d.extrude(
            f"blade_tooth_{index + 1:02d}",
            s3d.rect(P["tooth_width"], P["tooth_length"], r=P["tooth_corner_r"]),
            P["tooth_height"],
        )
        tooth = s3d.at(tooth, x=x, y=P["roller_axis_y"], z=P["tooth_root_z"])
        s3d.material(tooth, "plastic", color="#e2e4e7")
        teeth.append(tooth)
    return s3d.group("eight_comb_teeth", *teeth)


def build_research_assembly(exploded=False):
    """Build the complete seven-group assembly in a shared datum frame."""
    global COMPONENTS
    lower = build_lower_housing()
    upper = s3d.at(
        build_upper_housing(),
        z=(P["lower_shell_h"] + P["upper_shell_h"]) / 2,
    )
    reservoir = s3d.at(build_reservoir(), z=P["reservoir_z"])
    roller = build_roller_mechanism()
    wall = build_curved_wall()
    teeth = build_comb_teeth()
    retention = build_housing_retention_features()
    gasket = build_housing_gasket()

    # Keep the named engineering groups separate for web rendering and inspection.
    COMPONENTS = [
        ("lower-housing", "Lower housing", lower, "Engineering assumption",
         "Lower clamshell shell; envelope and wall geometry are provisional."),
        ("upper-housing", "Upper housing", upper, "Engineering assumption",
         "Upper clamshell shell; envelope and closure geometry are provisional."),
        ("reservoir", "Reservoir", reservoir, "Engineering assumption",
         "Translucent internal reservoir proxy; capacity and detailed geometry are unknown."),
        ("rotatable-roller", "Rotatable roller", roller, "Patent-derived estimate",
         "Smooth core, raised knurled circumferential bands, end walls and spindle pins. Most dimensions and texture are assumptions."),
        ("curved-slotted-wall", "Curved slotted wall", wall, "Patent-led interpretation",
         "180-degree concave seat with seven interpreted axial through-slots."),
        ("eight-comb-teeth", "Eight comb teeth", teeth, "Patent disclosed / derived",
         "Eight-tooth illustrated embodiment; approximate width and length are patent-described, while height and pitch remain assumptions."),
        ("roller-end-features", "Roller end features", retention, "Engineering assumption",
         "Bearing supports, bores and housing snap-fit retention proxies; exact construction is unverified."),
    ]

    roller_frame = s3d.local(
        lower, x=0, y=P["roller_axis_y"], z=P["roller_axis_z"]
    )
    s3d.joint(
        "roller_rotation", roller, roller_frame, kind="continuous", axis="+X"
    )
    return s3d.assembly(
        "nyfasi_complete_research_assembly",
        lower, upper, reservoir, roller, wall, teeth, retention, gasket,
    )


def main():
    s3d.empty_scene()
    model = build_research_assembly(exploded=False)
    output = ROOT / "output"
    output.mkdir(exist_ok=True)
    s3d.export(model, str(output / "nyfasi_complete_assembly.glb"))
    # Keep the benchmark and older local workflows compatible with the established export name.
    s3d.export(model, str(output / "hair_applicator_complete_roller_exploded.glb"))
    s3d.export(model, str(output / "hair_applicator_complete_roller_exploded.obj"))
    s3d.export(model, str(output / "hair_applicator_complete_roller.urdf"))
    s3d.export(model, str(output / "hair_applicator_complete_roller.usda"))

    # Publish each top-level component as its own GLB so the viewer can select,
    # isolate and explode real Sand3D geometry rather than a hand-drawn schematic.
    web_dir = output / "web-components"
    web_dir.mkdir(parents=True, exist_ok=True)
    manifest = {
        "schema_version": "1.0.0",
        "engine": "Sand3D",
        "engine_version": "1.6.2",
        "units": "mm",
        "model_status": "research_only",
        "assembly_file": "nyfasi_complete_assembly.glb",
        "components": [],
        "limitations": [
            "Patent-to-retail-SKU mapping is unverified.",
            "Most dimensions and all fit/tolerance values remain assumptions.",
            "The model is not a manufacturing release or validated physical digital twin."
        ]
    }
    for component_id, name, component, provenance, description in COMPONENTS:
        filename = component_id + ".glb"
        s3d.export(component, str(web_dir / filename))
        manifest["components"].append({
            "id": component_id,
            "name": name,
            "file": filename,
            "provenance": provenance,
            "description": description
        })
    (web_dir / "manifest.json").write_text(
        json.dumps(manifest, indent=2) + "\\n", encoding="utf-8"
    )
    print("Sand3D source fingerprint:", s3d.fingerprint())
    print("Built complete seven-group Sand3D assembly and component GLBs:", output.resolve())


if __name__ == "__main__":
    main()
