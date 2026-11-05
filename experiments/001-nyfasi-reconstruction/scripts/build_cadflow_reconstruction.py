"""Build a component-level, OpenCascade B-rep research reconstruction with CadFlow.

Every shape is a separately validated solid and exported as STEP/STL/GLB.
The final compound preserves the component set for review. It is not a
constraint-solved assembly or a verified retail/manufacturing model.
"""
from __future__ import annotations

import json
import math
from pathlib import Path

import cadflow as cad

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
PARAMS = json.loads(
    (ROOT / "models" / "cad-parameters.json").read_text(encoding="utf-8")
)["parameters"]
P = {key: value["value"] for key, value in PARAMS.items()}
OUT = ROOT / "output" / "cadflow"


def box_at(model: cad.Model, width: float, depth: float, height: float,
           x: float = 0, y: float = 0, z: float = 0):
    """Create a box from its centre datum."""
    shape = model.box(width=width, depth=depth, height=height)
    return model.translate(
        shape,
        x=x - width / 2,
        y=y - depth / 2,
        z=z - height / 2,
    )


def cylinder_x(model: cad.Model, radius: float, length: float,
               x: float = 0, y: float = 0, z: float = 0):
    """Create a cylinder whose axis is X and whose centre is (x, y, z)."""
    shape = model.cylinder(radius=radius, height=length)
    shape = model.rotate(
        shape,
        degrees=90,
        axis=(0, 1, 0),
        origin=(0, 0, 0),
    )
    return model.translate(shape, x=x - length / 2, y=y, z=z)


def hollow_box(model: cad.Model, width: float, depth: float, height: float,
               wall: float, floor: float, open_top: bool = True):
    """Hollow rectangular shell with either its top or bottom open."""
    outer = box_at(model, width, depth, height)
    inner_height = height - floor + 1.0
    if open_top:
        inner_z = -height / 2 + floor + inner_height / 2
    else:
        # Extend the cavity one millimetre through the bottom; leave a roof.
        inner_z = height / 2 - floor - inner_height / 2
    inner = box_at(
        model,
        width - 2 * wall,
        depth - 2 * wall,
        inner_height,
        z=inner_z,
    )
    return model.cut(outer, inner)


def build_lower_housing(model: cad.Model):
    return hollow_box(
        model,
        P["housing_w"],
        P["housing_d"],
        P["lower_shell_h"],
        P["housing_wall_t"],
        P["housing_wall_t"],
        open_top=True,
    )


def build_upper_housing(model: cad.Model):
    shell = hollow_box(
        model,
        P["housing_w"],
        P["housing_d"],
        P["upper_shell_h"],
        P["housing_wall_t"],
        P["housing_wall_t"],
        open_top=False,
    )
    # Seat the upper cap on the lower shell's top datum.
    return model.translate(
        shell,
        x=0,
        y=0,
        z=P["lower_shell_h"] / 2 + P["upper_shell_h"] / 2,
    )


def build_reservoir(model: cad.Model):
    return model.translate(
        hollow_box(
            model,
            P["reservoir_w"],
            P["reservoir_d"],
            P["reservoir_h"],
            1.5,
            1.0,
            open_top=True,
        ),
        x=0,
        y=0,
        z=P["reservoir_z"],
    )


def build_curved_wall(model: cad.Model, axis_y: float, axis_z: float):
    """Create the semi-cylindrical wall and its interpreted axial slots."""
    seat_radius = P["roller_d"] / 2 + P["roller_seat_clearance"]
    outer_radius = seat_radius + P["wall_thickness"]
    length = P["wall_len"]

    outline = []
    for index in range(65):
        angle = math.radians(-90 + 180 * index / 64)
        outline.append((0, outer_radius * math.cos(angle), outer_radius * math.sin(angle)))
    for index in range(64, -1, -1):
        angle = math.radians(-90 + 180 * index / 64)
        outline.append((0, seat_radius * math.cos(angle), seat_radius * math.sin(angle)))

    profile_wire = model.polyline(tuple(outline), closed=True)
    profile_face = model.face(profile_wire)
    wall = model.extrude(profile_face, x=length, y=0, z=0)
    wall = model.translate(wall, x=-length / 2, y=0, z=0)

    # One axial through-slot in each inter-tooth gap. The patent drawing is
    # schematic; slot width and this exact count-to-pitch mapping are assumptions.
    for index in range(P["tooth_count"] - 1):
        axial_x = (index - (P["tooth_count"] - 2) / 2) * P["tooth_pitch"]
        cutter = box_at(
            model,
            P["slot_w"],
            outer_radius * 2 + 2,
            outer_radius * 2 + 2,
            x=axial_x,
            y=outer_radius / 2,
        )
        wall = model.cut(wall, cutter)

    # Critical datum: move the local wall profile onto the roller axis.
    return model.translate(wall, x=0, y=axis_y, z=axis_z)


def build_roller_core(model: cad.Model, axis_y: float, axis_z: float):
    return cylinder_x(
        model,
        P["roller_core_d"] / 2,
        P["roller_len"],
        y=axis_y,
        z=axis_z,
    )


def build_roller_band(model: cad.Model, index: int, axis_y: float, axis_z: float):
    """Raised annular band; the exposed core between bands is the smooth land."""
    axial_x = (index - (P["roller_band_count"] - 1) / 2) * P["tooth_pitch"]
    outer = cylinder_x(
        model,
        P["roller_d"] / 2,
        P["roller_band_width"],
        x=axial_x,
        y=axis_y,
        z=axis_z,
    )
    bore = cylinder_x(
        model,
        (P["roller_core_d"] - 0.2) / 2,
        P["roller_band_width"] + 0.4,
        x=axial_x,
        y=axis_y,
        z=axis_z,
    )
    return model.cut(outer, bore)


def build_roller_end_wall(model: cad.Model, sign: int, axis_y: float, axis_z: float):
    centre_x = sign * (P["roller_len"] / 2 - P["roller_endwall_t"] / 2)
    return cylinder_x(
        model,
        P["roller_endwall_d"] / 2,
        P["roller_endwall_t"],
        x=centre_x,
        y=axis_y,
        z=axis_z,
    )


def build_spindle_pin(model: cad.Model, sign: int, axis_y: float, axis_z: float):
    centre_x = sign * (P["roller_len"] / 2 + P["spindle_pin_len"] / 2)
    return cylinder_x(
        model,
        P["spindle_pin_d"] / 2,
        P["spindle_pin_len"],
        x=centre_x,
        y=axis_y,
        z=axis_z,
    )


def build_bearing_support(model: cad.Model, sign: int, axis_y: float, axis_z: float):
    centre_x = sign * (
        P["roller_len"] / 2 + P["roller_endwall_t"] + P["spindle_pin_len"] / 2
    )
    block = box_at(
        model,
        P["bearing_block_w"],
        P["bearing_block_d"],
        P["bearing_block_h"],
        x=centre_x,
        y=axis_y,
        z=axis_z,
    )
    bore = cylinder_x(
        model,
        (P["spindle_pin_d"] + 2 * P["bearing_bore_clearance"]) / 2,
        P["bearing_block_w"] + 1,
        x=centre_x,
        y=axis_y,
        z=axis_z,
    )
    return model.cut(block, bore)


def build_comb_tooth(model: cad.Model, index: int, axis_y: float, axis_z: float):
    axial_x = (index - (P["tooth_count"] - 1) / 2) * P["tooth_pitch"]
    outer_radius = (
        P["roller_d"] / 2
        + P["roller_seat_clearance"]
        + P["wall_thickness"]
    )
    centre_z = axis_z - outer_radius - P["tooth_height"] / 2
    return box_at(
        model,
        P["tooth_width"],
        P["tooth_length"],
        P["tooth_height"],
        x=axial_x,
        y=axis_y,
        z=centre_z,
    )


def build_snap_tab(model: cad.Model, index: int):
    centre_x = (
        index - (P["snap_tab_count"] - 1) / 2
    ) * P["snap_tab_pitch"]
    centre_z = P["lower_shell_h"] / 2 + P["snap_tab_h"] / 2
    return box_at(
        model,
        P["snap_tab_w"],
        P["snap_tab_d"],
        P["snap_tab_h"],
        x=centre_x,
        z=centre_z,
    )


def build_perimeter_gasket(model: cad.Model):
    """Rectangular perimeter gasket proxy at the lower/upper shell interface."""
    width = P["housing_w"] - 2 * P["gasket_inset"]
    depth = P["housing_d"] - 2 * P["gasket_inset"]
    section = P["gasket_section_d"]
    z = P["lower_shell_h"] / 2 + section / 2
    outer = box_at(model, width, depth, section, z=z)
    inner = box_at(
        model,
        width - 2 * section,
        depth - 2 * section,
        section + 0.4,
        z=z,
    )
    return model.cut(outer, inner)


def build_component_shapes(model: cad.Model):
    """Return a stable component-ID to B-rep mapping in the shared datum frame."""
    axis_y = P["roller_axis_y"]
    axis_z = P["roller_axis_z"]
    components = {
        "housing_lower": build_lower_housing(model),
        "housing_upper": build_upper_housing(model),
        "reservoir": build_reservoir(model),
        "roller_core_and_smooth_lands": build_roller_core(model, axis_y, axis_z),
        "curved_slotted_wall": build_curved_wall(model, axis_y, axis_z),
        "housing_perimeter_gasket": build_perimeter_gasket(model),
    }

    for index in range(P["roller_band_count"]):
        key = f"roller_textured_band_{index + 1:02d}"
        components[key] = build_roller_band(model, index, axis_y, axis_z)

    for side, sign in (("left", -1), ("right", 1)):
        components[f"roller_end_wall_{side}"] = build_roller_end_wall(
            model, sign, axis_y, axis_z
        )
        components[f"spindle_pin_{side}"] = build_spindle_pin(
            model, sign, axis_y, axis_z
        )
        components[f"bearing_support_{side}"] = build_bearing_support(
            model, sign, axis_y, axis_z
        )

    for index in range(P["tooth_count"]):
        components[f"comb_tooth_{index + 1:02d}"] = build_comb_tooth(
            model, index, axis_y, axis_z
        )

    for index in range(P["snap_tab_count"]):
        components[f"housing_snap_tab_{index + 1:02d}"] = build_snap_tab(
            model, index
        )

    return components


def export_component(component_id: str, shape, expected_solids: int = 1):
    report = shape.validate()
    if not report.ok:
        raise RuntimeError(
            f"CadFlow B-rep validation failed for {component_id}: {report.to_dict()}"
        )
    if shape.volume <= 0:
        raise RuntimeError(f"Non-positive B-rep volume for {component_id}")
    expected_solids = P["tooth_count"] if component_id == "curved_slotted_wall" else 1
    if shape.topology["solids"] != expected_solids:
        raise RuntimeError(
            f"Expected {expected_solids} solid(s) for {component_id}, "
            f"got {shape.topology['solids']}"
        )

    stem = OUT / component_id
    shape.export_step(str(stem.with_suffix(".step")))
    shape.export_stl(str(stem.with_suffix(".stl")), binary=True)
    shape.export_preview_glb(str(stem.with_suffix(".glb")))

    return {
        "kind": shape.kind,
        "volume_mm3": shape.volume,
        "area_mm2": shape.area,
        "bbox_mm": list(shape.bbox),
        "topology": shape.topology,
        "expected_solids": expected_solids,
        "validation": report.to_dict(),
        "files": {
            "step": stem.with_suffix(".step").name,
            "stl": stem.with_suffix(".stl").name,
            "glb": stem.with_suffix(".glb").name,
        },
    }


def build():
    OUT.mkdir(parents=True, exist_ok=True)
    manifest = {
        "schema_version": "1.1.0",
        "engine": "CadFlow",
        "engine_version": getattr(cad, "__version__", "unknown"),
        "geometry_kernel": "OpenCascade",
        "units": "mm",
        "model_status": "research_only",
        "source_parameter_file": "models/cad-parameters.json",
        "source_parameter_schema_version": json.loads(
            (ROOT / "models" / "cad-parameters.json").read_text(encoding="utf-8")
        )["schema_version"],
        "component_count": 0,
        "components": {},
        "assembly": {
            "status": "flattened_native_multi_solid_shape",
            "constraint_solution": "not_performed",
            "note": "Components share a common datum frame; the compound is for review/export, not a constraint-solved kinematic assembly.",
        },
        "limitations": [
            "No authorised physical sample, supplier drawing or native Nyfasi CAD was used.",
            "The patent-to-retail-SKU/revision mapping remains unverified.",
            "Most dimensions and all tolerances/material properties remain assumptions.",
            "The roller bands are smooth annular B-rep rings; texture microgeometry is not dimensioned by the patent.",
            "Housing and reservoir corner-radius ledger values are not yet applied as fillets in this build.",

            "The seven-slot/seven-band mapping is an engineering interpretation; the slotted wall is represented as eight separate arc solids.",

            "No contact, tolerance-stack, seal-compression, fatigue or performance analysis was performed.",
            "Not a manufacturing release or verified digital twin.",
        ],
    }

    with cad.Model() as model:
        components = build_component_shapes(model)
        for component_id, shape in components.items():
            # Seven through-slots divide the semi-cylindrical wall into eight
            # disconnected arc segments. That is intentional in this proxy;
            # all other named components must remain single solids.
            expected_solids = P["tooth_count"] if component_id == "curved_slotted_wall" else 1
            manifest["components"][component_id] = export_component(
                component_id, shape, expected_solids=expected_solids
            )

        # CadFlow's new Model/Shape frontend and legacy Part/Assembly facade
        # are separate API surfaces. Keep each component as its own validated
        # Shape and create an aggregate native Shape for convenient preview/export.
        component_shapes = list(components.values())
        aggregate = component_shapes[0]
        for next_shape in component_shapes[1:]:
            aggregate = model.union(aggregate, next_shape)

        aggregate_report = aggregate.validate()
        if not aggregate_report.ok:
            raise RuntimeError(
                "CadFlow aggregate validation failed: "
                + json.dumps(aggregate_report.to_dict(), sort_keys=True)
            )
        aggregate.export_step(str(OUT / "nyfasi_research_assembly.step"))
        aggregate.export_preview_glb(str(OUT / "nyfasi_research_assembly.glb"))

        manifest["component_count"] = len(components)
        manifest["assembly"]["component_ids"] = list(components)
        manifest["assembly"]["status"] = "flattened_native_multi_solid_shape"
        manifest["assembly"]["compound"] = {
            "volume_mm3": aggregate.volume,
            "bbox_mm": list(aggregate.bbox),
            "topology": aggregate.topology,
            "validation": aggregate_report.to_dict(),
            "step": "nyfasi_research_assembly.step",
            "glb": "nyfasi_research_assembly.glb",
            "note": "Aggregate preview/export only; named component STEP files remain the component-level source artefacts.",
        }

    (OUT / "cadflow-build-manifest.json").write_text(
        json.dumps(manifest, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    return manifest


if __name__ == "__main__":
    result = build()
    print(
        f"CadFlow built {result['component_count']} separately validated components "
        "plus a flattened assembly compound"
    )
