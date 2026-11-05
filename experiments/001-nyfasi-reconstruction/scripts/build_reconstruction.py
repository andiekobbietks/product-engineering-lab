"""Evidence-led, component-first Nyfasi patent-architecture research proxy.

This is deliberately not a claim of original Nyfasi CAD or a verified retail twin.
All dimensions come from the provenance ledger; unverified values remain assumptions.
"""
from pathlib import Path
import ast
import hashlib
import json
import math
import struct
import sand3d as s3d

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
PARAMETER_FILE = ROOT / "models" / "cad-parameters.json"
RECORDS = json.loads(PARAMETER_FILE.read_text(encoding="utf-8"))["parameters"]
P = {name: record["value"] for name, record in RECORDS.items()}
COMPONENTS = []


def validate_articulated_glb(path, expected_component_nodes, expected_joint):
    """Fail the build if the complete GLB loses named groups or Sand3D joint extras."""
    payload = Path(path).read_bytes()
    if len(payload) < 20 or payload[:4] != b"glTF":
        raise ValueError(f"Invalid GLB header: {path}")
    version, total_length = struct.unpack_from("<II", payload, 4)
    if version != 2 or total_length != len(payload):
        raise ValueError(f"Unexpected GLB version or length: {path}")
    json_length, json_type = struct.unpack_from("<II", payload, 12)
    if json_type != 0x4E4F534A:
        raise ValueError("GLB first chunk is not JSON")
    document = json.loads(payload[20:20 + json_length].decode("utf-8").rstrip(" \\0"))
    nodes = document.get("nodes", [])
    node_names = {node.get("name") for node in nodes if node.get("name")}
    missing = sorted(set(expected_component_nodes) - node_names)
    if missing:
        raise ValueError(f"Sand3D GLB is missing named component nodes: {missing}")
    joint_records = [
        node.get("extras", {}).get("s3d_joint")
        for node in nodes
        if isinstance(node.get("extras"), dict)
    ]
    matching = [joint for joint in joint_records if isinstance(joint, dict) and joint.get("name") == expected_joint]
    if not matching:
        raise ValueError(f"Sand3D GLB is missing s3d_joint metadata for {expected_joint!r}")
    if matching[0].get("type") != "continuous":
        raise ValueError(f"Expected {expected_joint!r} to be a continuous joint")
    print(
        "Validated articulated Sand3D GLB:",
        len(nodes), "nodes;",
        len(expected_component_nodes), "named component roots;",
        expected_joint, "joint metadata present",
    )


def cylinder_on_x(name, diameter, length, x=0, y=0, z=0):
    """Create an X-axis cylinder centred at (x, y, z)."""
    solid = s3d.cylinder(name, d=diameter, h=length)
    return s3d.at(solid, x=x - length / 2, y=y, z=z, ry=90)


def housing_outline_points(width, depth, waist_depth, end_radius):
    """Patent-led waisted planform: full-width ends and a narrower centre."""
    return [
        (-width * 0.5 + end_radius, -depth / 2),
        (-width * 0.30, -depth / 2),
        (-width * 0.18, -waist_depth / 2),
        (width * 0.18, -waist_depth / 2),
        (width * 0.30, -depth / 2),
        (width / 2 - end_radius, -depth / 2),
        (width / 2, -depth / 2 + end_radius),
        (width / 2, depth / 2 - end_radius),
        (width / 2 - end_radius, depth / 2),
        (width * 0.30, depth / 2),
        (width * 0.18, waist_depth / 2),
        (-width * 0.18, waist_depth / 2),
        (-width * 0.30, depth / 2),
        (-width / 2 + end_radius, depth / 2),
        (-width / 2, depth / 2 - end_radius),
        (-width / 2, -depth / 2 + end_radius),
    ]


def housing_outline_profile(width, depth, waist_depth, corner):
    return s3d.poly(housing_outline_points(width, depth, waist_depth, corner), fillet=corner)


def rounded_tray(name, width, depth, height, wall, corner):
    """Open-top, waisted clamshell housing half, built at its own origin."""
    waist_depth = P["housing_waist_depth"]
    blank_profile = housing_outline_profile(width, depth, waist_depth, corner)
    blank = s3d.extrude(name + "_blank", blank_profile, height)
    blank = s3d.at(blank, z=-height / 2)
    cavity_profile = housing_outline_profile(
        width - 2 * wall,
        depth - 2 * wall,
        waist_depth - 2 * wall,
        max(0.5, corner - wall),
    )
    cavity = s3d.extrude(
        name + "_cavity_tool",
        cavity_profile,
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
        P["roller_d"], P["roller_len"],
        y=P["roller_axis_y"], z=P["roller_axis_z"],
    )
    s3d.material(core, "rubber", color="#59636b")
    return core


def build_textured_band(index, axial_position):
    """A circumferential array of patent-described spheroidal roller projections."""
    projections = []
    projection_d = P["roller_projection_d"]
    surface_radius = P["roller_d"] / 2 - P["roller_projection_overlap"]
    for projection_index in range(P["roller_projection_count"]):
        angle = 2 * math.pi * projection_index / P["roller_projection_count"]
        projection = s3d.dome(
            f"roller_projection_{index:02d}_{projection_index + 1:02d}",
            projection_d,
            P["roller_projection_height"],
        )
        # The dome base sits on the smooth drum; rotate its local +Z axis
        # onto the radial direction so the spheroidal cap projects outwards.
        projection = s3d.at(
            projection,
            x=axial_position,
            y=P["roller_axis_y"] + surface_radius * math.cos(angle),
            z=P["roller_axis_z"] + surface_radius * math.sin(angle),
            rx=math.degrees(angle) - 90,
        )
        s3d.material(projection, "rubber", color="#a9b0b5", roughness=0.82)
        projections.append(projection)
    return s3d.group(f"textured_annular_band_{index:02d}", *projections)


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


def build_roller_core_and_bands():
    """Rotating roller body: smooth core with separately modelled raised bands."""
    parts = [build_roller_core()]
    band_count = P["roller_band_count"]
    for index in range(band_count):
        axial = (index - (band_count - 1) / 2) * P["tooth_pitch"]
        parts.append(build_textured_band(index + 1, axial))
    return s3d.group("rotatable_roller_body", *parts)


def build_roller_end_features():
    """Separate end walls and spindle pins at both ends of the roller."""
    parts = []
    for side, sign in (("left", -1), ("right", 1)):
        parts.append(build_roller_end_wall(side, sign))
        parts.append(build_spindle_pin(side, sign))
    return s3d.group("roller_end_features", *parts)


def build_elastomeric_spindle_seals():
    """Build two annular seal proxies around spindle pins; fit remains unvalidated."""
    seals = []
    x_position = (
        P["roller_len"] / 2
        + P["roller_endwall_t"]
        + P["spindle_pin_len"] / 2
    )
    for side, sign in (("left", -1), ("right", 1)):
        outer = cylinder_on_x(
            f"{side}_spindle_seal_outer",
            P["seal_outer_d"], P["seal_axial_width"],
            x=sign * x_position, y=P["roller_axis_y"], z=P["roller_axis_z"],
        )
        bore = cylinder_on_x(
            f"{side}_spindle_seal_bore_tool",
            P["seal_inner_d"], P["seal_axial_width"] + 0.4,
            x=sign * x_position, y=P["roller_axis_y"], z=P["roller_axis_z"],
        )
        seal = s3d.cut(outer, bore)
        s3d.material(seal, "rubber", color="#30383c", roughness=0.9)
        seals.append(s3d.group(f"{side}_elastomeric_spindle_seal_proxy", seal))
    return s3d.group("elastomeric_spindle_seals_research_proxy", *seals)


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
    """Compatibility helper; use the canonical tapered tooth builder."""
    wall = build_curved_wall()
    teeth = build_comb_teeth()
    return s3d.group("curved_wall_and_blade_teeth", wall, teeth)


def build_housing_gasket():
    """Separate perimeter seal proxy; section and compression remain assumptions."""
    w = P["housing_w"] - 2 * P["gasket_inset"]
    d = P["housing_d"] - 2 * P["gasket_inset"]
    waist = P["housing_waist_depth"] - 2 * P["gasket_inset"]
    path = housing_outline_points(w, d, waist, P["housing_corner_r"])
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
            s3d.superellipse(P["tooth_width"], P["tooth_length"], n=2),
            P["tooth_height"],
            taper=P["tooth_tip_taper_deg"],
        )
        tooth = s3d.at(tooth, x=x, y=P["roller_axis_y"], z=P["tooth_root_z"])
        s3d.material(tooth, "plastic", color="#e2e4e7")
        teeth.append(tooth)
    return s3d.group("eight_comb_teeth", *teeth)


def build_research_assembly(exploded=False):
    """Build the complete seven-group assembly in a shared datum frame."""
    global COMPONENTS
    lower_shell = build_lower_housing()
    housing_supports_and_tabs = build_housing_retention_features()
    housing_gasket = build_housing_gasket()
    lower = s3d.group(
        "lower_housing_complete", lower_shell, housing_supports_and_tabs, housing_gasket
    )
    upper = s3d.at(
        build_upper_housing(),
        z=(P["lower_shell_h"] + P["upper_shell_h"]) / 2,
    )
    reservoir = s3d.at(build_reservoir(), z=P["reservoir_z"])
    roller = build_roller_core_and_bands()
    # Keep the component root name unique. The previous root reused the name of
    # its nested geometry group, causing Sand3D to suffix one name with .001.
    roller_ends = s3d.group(
        "roller_end_features_component_group",
        build_roller_end_features(),
        build_elastomeric_spindle_seals(),
    )
    wall = build_curved_wall()
    teeth = build_comb_teeth()

    # Seven top-level groups correspond to the public component register.
    COMPONENTS = [
        ("lower-housing", "Lower housing", lower, "Engineering assumption",
         "Lower shell, housing bearing supports, snap-fit tabs and perimeter seal. Envelope and retention dimensions are provisional."),
        ("upper-housing", "Upper housing", upper, "Engineering assumption",
         "Upper clamshell shell; envelope and closure geometry are provisional."),
        ("reservoir", "Reservoir", reservoir, "Engineering assumption",
         "Translucent internal reservoir proxy; capacity and detailed geometry are unknown."),
        ("rotatable-roller", "Rotatable roller", roller, "Patent-derived estimate",
         "Smooth drum with circumferential bands of discrete spheroidal projections. Roller diameter is a patent-derived estimate; projection count and spacing are derived assumptions."),
        ("curved-slotted-wall", "Curved slotted wall", wall, "Patent-led interpretation",
         "180-degree concave seat with seven interpreted axial through-slots."),
        ("eight-comb-teeth", "Eight comb teeth", teeth, "Patent disclosed / derived",
         "Eight-tooth illustrated embodiment; approximate width and length are patent-described, while height and pitch remain assumptions."),
        ("roller-end-features", "Roller end features", roller_ends, "Engineering assumption",
         "Two end walls, spindle pins and annular spindle-seal proxies. Seal fit and retention geometry remain unverified assumptions."),
    ]

    roller_frame = s3d.local(
        lower, x=0, y=P["roller_axis_y"], z=P["roller_axis_z"]
    )
    s3d.joint(
        "roller_rotation", roller, roller_frame, kind="continuous", axis="+X"
    )
    return s3d.assembly(
        "nyfasi_complete_research_assembly",
        lower, upper, reservoir, roller, wall, teeth, roller_ends,
    )


def main():
    s3d.empty_scene()
    model = build_research_assembly(exploded=False)
    output = ROOT / "output"
    output.mkdir(exist_ok=True)
    assembly_path = output / "nyfasi_complete_assembly.glb"
    s3d.export(model, str(assembly_path))
    assembly_sha256 = hashlib.sha256(assembly_path.read_bytes()).hexdigest()
    validate_articulated_glb(
        assembly_path,
        [component.name for _, _, component, _, _ in COMPONENTS],
        "roller_rotation",
    )
    # Keep the benchmark and older local workflows compatible with the established export name.
    s3d.export(model, str(output / "hair_applicator_complete_roller_exploded.glb"))
    s3d.export(model, str(output / "hair_applicator_complete_roller_exploded.obj"))
    s3d.export(model, str(output / "hair_applicator_complete_roller.urdf"))
    s3d.export(model, str(output / "hair_applicator_complete_roller.usda"))

    # Publish each top-level component as its own GLB so the viewer can select,
    # isolate and explode real Sand3D geometry rather than a hand-drawn schematic.
    web_dir = output / "web-components"
    web_dir.mkdir(parents=True, exist_ok=True)
    # Publish the exact modelling program and an AST-derived source map. The
    # browser viewer therefore highlights real source ranges, not hand-written
    # snippets that can drift away from the geometry-producing program.
    source_path = Path(__file__).resolve()
    source_text = source_path.read_text(encoding="utf-8")
    source_tree = ast.parse(source_text)
    source_ranges = {
        node.name: {"start_line": node.lineno, "end_line": node.end_lineno}
        for node in ast.walk(source_tree)
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))
    }
    component_symbols = {
        "lower-housing": ["housing_outline_points", "housing_outline_profile", "rounded_tray", "build_lower_housing", "build_housing_retention_features", "build_housing_gasket", "build_research_assembly"],
        "upper-housing": ["housing_outline_points", "housing_outline_profile", "rounded_tray", "build_upper_housing"],
        "reservoir": ["build_reservoir"],
        "rotatable-roller": ["cylinder_on_x", "build_roller_core", "build_textured_band", "build_roller_core_and_bands"],
        "curved-slotted-wall": ["build_curved_wall"],
        "eight-comb-teeth": ["build_comb_teeth"],
        "roller-end-features": ["cylinder_on_x", "build_roller_end_wall", "build_spindle_pin", "build_roller_end_features", "build_elastomeric_spindle_seals"],
    }
    source_object_prefixes = {
        "lower-housing": [
            ("lower_housing_shell_proxy", "build_lower_housing"),
            ("housing_bearings_and_snap_fit_proxies", "build_housing_retention_features"),
            ("housing_interface_gasket_proxy", "build_housing_gasket"),
        ],
        "upper-housing": [("upper_housing_shell_proxy", "build_upper_housing")],
        "reservoir": [("reservoir_volume_proxy", "build_reservoir")],
        "rotatable-roller": [
            ("roller_smooth_core_and_sealing_lands", "build_roller_core"),
            ("textured_annular_band_", "build_textured_band"),
        ],
        "curved-slotted-wall": [("semi_cylindrical_slotted_wall", "build_curved_wall")],
        "eight-comb-teeth": [("blade_tooth_", "build_comb_teeth")],
        "roller-end-features": [
            ("roller_left_end_wall_component", "build_roller_end_wall"),
            ("roller_right_end_wall_component", "build_roller_end_wall"),
            ("roller_left_spindle_pin_component", "build_spindle_pin"),
            ("roller_right_spindle_pin_component", "build_spindle_pin"),
            ("elastomeric_spindle_seals_research_proxy", "build_elastomeric_spindle_seals"),
            ("left_elastomeric_spindle_seal_proxy", "build_elastomeric_spindle_seals"),
            ("right_elastomeric_spindle_seal_proxy", "build_elastomeric_spindle_seals"),
        ],
    }
    (web_dir / "build_reconstruction.py").write_text(source_text, encoding="utf-8")
    (web_dir / "cad-parameters.json").write_text(
        PARAMETER_FILE.read_text(encoding="utf-8"), encoding="utf-8"
    )
    manifest = {
        "schema_version": "1.1.0",
        "engine": "Sand3D",
        "engine_version": "1.6.2",
        "units": "mm",
        "model_status": "research_only",
        "assembly_file": "nyfasi_complete_assembly.glb",
        "assembly_sha256": assembly_sha256,
        "source": {
            "program_file": "build_reconstruction.py",
            "parameters_file": "cad-parameters.json",
            "sha256": hashlib.sha256(source_text.encode("utf-8")).hexdigest(),
            "symbol_index": source_ranges,
        },
        "joint_expectations": [
            {"name": "roller_rotation", "type": "continuous", "axis": "+X", "component_id": "rotatable-roller"}
        ],
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
            "node_name": component.name,
            "file": filename,
            "provenance": provenance,
            "description": description,
            "source_symbols": [
                {"name": symbol, **source_ranges[symbol]}
                for symbol in component_symbols.get(component_id, [])
                if symbol in source_ranges
            ],
            "source_object_prefixes": [
                {"prefix": prefix, "symbol": symbol}
                for prefix, symbol in source_object_prefixes.get(component_id, [])
                if symbol in source_ranges
            ],
        })
    (web_dir / "manifest.json").write_text(
        json.dumps(manifest, indent=2) + "\n", encoding="utf-8"
    )
    print("Sand3D source fingerprint:", s3d.fingerprint())
    print("Built complete seven-group Sand3D assembly and component GLBs:", output.resolve())


if __name__ == "__main__":
    main()
