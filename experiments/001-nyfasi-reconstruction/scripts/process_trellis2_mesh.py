"""Inspect and optionally repair a TRELLIS.2 GLB without changing the CAD source of truth.

The original GLB is never overwritten. MeshFix is an optional topology-repair
stage; its output is a diagnostic derivative and may not retain PBR materials.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any

import numpy as np
import trimesh


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def mesh_metrics(mesh: trimesh.Trimesh) -> dict[str, Any]:
    bounds = np.asarray(mesh.bounds, dtype=float)
    components = mesh.split(only_watertight=False)
    metrics: dict[str, Any] = {
        "vertices": int(len(mesh.vertices)),
        "faces": int(len(mesh.faces)),
        "bounds_model_units": bounds.tolist(),
        "extents_model_units": np.asarray(mesh.extents, dtype=float).tolist(),
        "surface_area_model_units_squared": float(mesh.area),
        "is_watertight": bool(mesh.is_watertight),
        "is_winding_consistent": bool(mesh.is_winding_consistent),
        "euler_number": int(mesh.euler_number),
        "connected_components": int(len(components)),
        "component_face_counts": [int(len(part.faces)) for part in components],
        "volume_model_units_cubed": (
            float(mesh.volume) if mesh.is_watertight else None
        ),
    }
    return metrics


def repair_mesh(mesh: trimesh.Trimesh) -> tuple[trimesh.Trimesh, dict[str, Any]]:
    """Repair a copy using conservative cleanup then PyMeshFix if still open."""
    candidate = mesh.copy()
    before = mesh_metrics(candidate)

    # Remove only unreferenced vertices before topology repair.
    candidate.remove_unreferenced_vertices()
    trimesh.repair.fix_winding(candidate)
    trimesh.repair.fix_normals(candidate, multibody=True)

    meshfix_used = False
    if not candidate.is_watertight:
        try:
            from pymeshfix import MeshFix
        except ImportError as exc:
            raise RuntimeError(
                "PyMeshFix is required for open-mesh repair. Install "
                "requirements-reconstruction.txt or omit --repair."
            ) from exc
        fixer = MeshFix(
            np.asarray(candidate.vertices, dtype=np.float64),
            np.asarray(candidate.faces, dtype=np.int32),
        )
        fixer.repair(joincomp=False, remove_smallest_components=False)
        candidate = trimesh.Trimesh(
            vertices=np.asarray(fixer.points),
            faces=np.asarray(fixer.faces),
            process=True,
        )
        meshfix_used = True
        trimesh.repair.fix_winding(candidate)
        trimesh.repair.fix_normals(candidate, multibody=True)

    return candidate, {
        "meshfix_used": meshfix_used,
        "before": before,
        "after": mesh_metrics(candidate),
    }


def load_scene(path: Path) -> trimesh.Scene:
    loaded = trimesh.load(path, force="scene", process=False)
    if isinstance(loaded, trimesh.Trimesh):
        scene = trimesh.Scene()
        scene.add_geometry(loaded, geom_name=path.stem, node_name=path.stem)
        return scene
    if not isinstance(loaded, trimesh.Scene) or not loaded.geometry:
        raise ValueError(f"No mesh geometry found in {path}")
    return loaded


def process_glb(source: Path, report_path: Path, repaired_path: Path | None) -> dict[str, Any]:
    scene = load_scene(source)
    report: dict[str, Any] = {
        "schema_version": "1.0.0",
        "source_file": source.name,
        "source_sha256": sha256(source),
        "source_bytes": source.stat().st_size,
        "units": "unknown; TRELLIS.2 output is not physically calibrated",
        "interpretation": (
            "AI-generated visual hypothesis. Bounds are model-space units, "
            "not millimetres. This report does not establish physical scale."
        ),
        "geometry": [],
    }

    output_scene = trimesh.Scene()
    for node in list(scene.graph.nodes_geometry):
        transform, geometry_name = scene.graph[node]
        geometry = scene.geometry[geometry_name]
        if not isinstance(geometry, trimesh.Trimesh):
            report["geometry"].append({
                "node": str(node),
                "geometry": str(geometry_name),
                "kind": type(geometry).__name__,
                "status": "skipped_non_triangle_geometry",
            })
            continue

        item: dict[str, Any] = {
            "node": str(node),
            "geometry": str(geometry_name),
            "before": mesh_metrics(geometry),
        }
        processed = geometry.copy()
        if repaired_path is not None:
            processed, repair_record = repair_mesh(geometry)
            item["repair"] = repair_record
        else:
            item["repair"] = {"performed": False}
        item["after"] = mesh_metrics(processed)

        # Preserve scene placement. Repaired geometry is a separate derivative;
        # material/UV preservation is not guaranteed by topology repair.
        output_scene.add_geometry(
            processed,
            geom_name=f"{geometry_name}_processed",
            node_name=f"{node}_processed",
            transform=transform,
        )
        report["geometry"].append(item)

    if not report["geometry"]:
        raise ValueError("GLB contained no triangle meshes to inspect")

    if repaired_path is not None:
        repaired_path.parent.mkdir(parents=True, exist_ok=True)
        output_scene.export(repaired_path, file_type="glb")
        report["repaired_file"] = repaired_path.name
        report["repaired_sha256"] = sha256(repaired_path)
        report["repaired_bytes"] = repaired_path.stat().st_size
        report["repair_notice"] = (
            "Diagnostic topology derivative. Check appearance, UVs, textures, "
            "component separation and dimensions against the untouched source."
        )

    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    return report


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input", type=Path, help="TRELLIS.2 GLB downloaded from the Space/Colab/local run")
    parser.add_argument("--report", type=Path, default=Path("nyfasi_mesh_report.json"))
    parser.add_argument(
        "--repair-output", type=Path,
        help="Optional separate GLB output; original input is never overwritten",
    )
    args = parser.parse_args()
    if not args.input.is_file():
        parser.error(f"Input GLB does not exist: {args.input}")
    report = process_glb(args.input, args.report, args.repair_output)
    print(f"Inspected {len(report['geometry'])} geometry node(s)")
    for item in report["geometry"]:
        if "after" in item:
            metrics = item["after"]
            print(
                f"{item['node']}: {metrics['vertices']} vertices, "
                f"{metrics['faces']} faces, watertight={metrics['is_watertight']}, "
                f"components={metrics['connected_components']}"
            )
    print(f"Report: {args.report}")
    if args.repair_output:
        print(f"Separate repaired derivative: {args.repair_output}")


if __name__ == "__main__":
    main()
