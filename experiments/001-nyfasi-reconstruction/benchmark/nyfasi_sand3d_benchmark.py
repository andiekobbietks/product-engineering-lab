"""Sand3D-native parametric edit and constraint-preservation benchmark.

Runs the real Sand3D authoring program in isolated temporary workspaces. The
benchmark deliberately tests declared relationships, regeneration, output
structure and edit sensitivity. It does not claim physical product validation.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import shutil
import subprocess
import sys
import tempfile
import xml.etree.ElementTree as ET
from pathlib import Path

HERE = Path(__file__).resolve().parent
EXPERIMENT = HERE.parent
PARAMETER_FILE = EXPERIMENT / "models" / "cad-parameters.json"
BUILDER = EXPERIMENT / "scripts" / "build_reconstruction.py"
OUTPUT_NAMES = (
    "hair_applicator_complete_roller_exploded.glb",
    "hair_applicator_complete_roller_exploded.obj",
    "hair_applicator_complete_roller.urdf",
    "hair_applicator_complete_roller.usda",
)


def load_parameters(path: Path) -> dict:
    data = json.loads(path.read_text(encoding="utf-8"))
    return {key: value["value"] for key, value in data["parameters"].items()}


def check_constraints(p: dict) -> list[str]:
    errors: list[str] = []
    def require(condition: bool, message: str) -> None:
        if not condition:
            errors.append(message)

    roller_r = p["roller_d"] / 2
    seat_r = roller_r + p["roller_seat_clearance"]
    outer_r = seat_r + p["wall_thickness"]
    tooth_span = (p["tooth_count"] - 1) * p["tooth_pitch"] + p["tooth_width"]
    band_span = (p["roller_band_count"] - 1) * p["tooth_pitch"] + p["roller_band_width"]
    support_x = p["roller_len"] / 2 + p["roller_endwall_t"] + p["spindle_pin_len"] / 2

    require(p["roller_core_d"] < p["roller_d"], "roller core must remain below roller outer diameter")
    require(outer_r > seat_r > roller_r, "roller/seat/wall radial ordering must be preserved")
    require(abs(seat_r - roller_r - p["roller_seat_clearance"]) < 1e-9, "declared radial seat clearance must be preserved")
    require(p["wall_len"] >= tooth_span, "curved wall must span the tooth row")
    require(p["roller_len"] >= p["wall_len"], "roller must span the wall")
    require(p["roller_band_count"] == p["tooth_count"] - 1, "band count must equal inter-tooth slot count")
    require(band_span <= p["roller_len"], "textured band row must fit roller length")
    require(0 < p["roller_band_width"] < p["tooth_pitch"] - p["tooth_width"], "band must fit the inter-tooth clear gap")
    require(p["spindle_pin_d"] + 2 * p["bearing_bore_clearance"] < min(p["bearing_block_d"], p["bearing_block_h"]), "spindle and bearing bore must fit support")
    require(support_x + p["bearing_block_w"] / 2 <= p["housing_w"] / 2, "bearing supports must remain inside housing envelope")
    require(p["housing_wall_t"] > 0 and p["housing_wall_t"] < min(p["lower_shell_h"], p["upper_shell_h"]) / 2, "housing wall thickness must remain feasible")
    require(p["tooth_root_z"] <= p["roller_axis_z"] - outer_r, "tooth root must remain outside roller-seat envelope")
    require(p["roller_knurl_pitch"] > 0, "knurl pitch must remain positive")
    return errors


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def prepare_workspace(target: Path, parameter_data: dict) -> Path:
    workspace = target / "001-nyfasi-reconstruction"
    shutil.copytree(EXPERIMENT, workspace, ignore=shutil.ignore_patterns("output", "__pycache__", "*.pyc"))
    (workspace / "models" / "cad-parameters.json").write_text(
        json.dumps(parameter_data, indent=2) + "\n", encoding="utf-8"
    )
    return workspace


def run_case(name: str, mutations: dict[str, float], expected: dict[str, float], root: Path) -> dict:
    with tempfile.TemporaryDirectory(prefix=f"nyfasi-{name}-") as temporary:
        workspace = prepare_workspace(Path(temporary), json.loads(PARAMETER_FILE.read_text(encoding="utf-8")))
        parameter_path = workspace / "models" / "cad-parameters.json"
        data = json.loads(parameter_path.read_text(encoding="utf-8"))
        for key, value in mutations.items():
            if key not in data["parameters"]:
                raise KeyError(f"Unknown benchmark parameter: {key}")
            data["parameters"][key]["value"] = value
        values = {key: item["value"] for key, item in data["parameters"].items()}
        errors = check_constraints(values)
        if errors:
            return {"scenario": name, "status": "rejected", "constraint_errors": errors, "mutations": mutations}

        for key, value in expected.items():
            if abs(values[key] - value) > 1e-9:
                return {"scenario": name, "status": "failed", "reason": f"Expected {key}={value}, got {values[key]}"}

        parameter_path.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")
        completed = subprocess.run(
            [sys.executable, str(workspace / "scripts" / "build_reconstruction.py")],
            cwd=workspace, capture_output=True, text=True, timeout=600,
        )
        if completed.returncode:
            return {
                "scenario": name, "status": "failed", "returncode": completed.returncode,
                "stdout": completed.stdout[-4000:], "stderr": completed.stderr[-4000:],
            }

        output = workspace / "output"
        files = {}
        for filename in OUTPUT_NAMES:
            artifact = output / filename
            if not artifact.is_file() or artifact.stat().st_size < 128:
                return {"scenario": name, "status": "failed", "reason": f"Missing or empty export: {filename}"}
            files[filename] = {"bytes": artifact.stat().st_size, "sha256": sha256(artifact)}

        urdf = ET.parse(output / "hair_applicator_complete_roller.urdf").getroot()
        joint = next((node for node in urdf.findall("joint") if node.attrib.get("name") == "roller_rotation"), None)
        if joint is None or joint.attrib.get("type") != "continuous":
            return {"scenario": name, "status": "failed", "reason": "continuous roller_rotation joint missing from URDF"}
        axis = joint.find("axis")
        if axis is None or axis.attrib.get("xyz") not in {"1 0 0", "1.0 0.0 0.0", "+1 0 0"}:
            return {"scenario": name, "status": "failed", "reason": "roller joint axis is not +X", "axis": None if axis is None else axis.attrib}

        return {
            "scenario": name, "status": "passed", "mutations": mutations,
            "constraints_checked": 13, "joint": {"name": "roller_rotation", "type": "continuous", "axis": axis.attrib.get("xyz")},
            "exports": files, "builder_stdout": completed.stdout[-1200:],
        }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, default=HERE / "results" / "latest.json")
    args = parser.parse_args()
    baseline = load_parameters(PARAMETER_FILE)
    baseline_errors = check_constraints(baseline)
    if baseline_errors:
        print("Baseline constraint failure:", *baseline_errors, sep="\n- ")
        return 1

    scenarios = [
        ("baseline", {}, {}),
        ("roller_diameter_plus_2mm", {
            "roller_d": baseline["roller_d"] + 2.0,
            "tooth_root_z": baseline["tooth_root_z"] - 1.0,
        }, {"roller_d": baseline["roller_d"] + 2.0, "tooth_root_z": baseline["tooth_root_z"] - 1.0}),
        ("housing_width_plus_10mm", {
            "housing_w": baseline["housing_w"] + 10.0,
        }, {"housing_w": baseline["housing_w"] + 10.0}),
    ]
    results = []
    with tempfile.TemporaryDirectory(prefix="nyfasi-sand3d-benchmark-") as temporary:
        root = Path(temporary)
        for name, mutations, expected in scenarios:
            results.append(run_case(name, mutations, expected, root))

    # A deliberately invalid edit must be rejected before invoking Sand3D.
    invalid = dict(baseline)
    invalid["roller_d"] = baseline["roller_core_d"] - 1
    invalid_errors = check_constraints(invalid)
    results.append({
        "scenario": "invalid_roller_diameter_below_core",
        "status": "passed" if invalid_errors else "failed",
        "expected_rejection": True,
        "constraint_errors": invalid_errors,
    })

    baseline_result = next(item for item in results if item["scenario"] == "baseline")
    baseline_hashes = baseline_result.get("exports", {})
    for item in results:
        if item["scenario"] == "baseline" or item["status"] != "passed" or "exports" not in item:
            continue
        changed = any(
            item["exports"][filename]["sha256"] != baseline_hashes.get(filename, {}).get("sha256")
            for filename in ("hair_applicator_complete_roller_exploded.glb", "hair_applicator_complete_roller_exploded.obj")
        )
        item["geometry_output_changed"] = changed
        if not changed:
            item["status"] = "failed"
            item["reason"] = "Declared parameter edit did not change GLB or OBJ output"
    passed = sum(item["status"] == "passed" for item in results)
    report = {
        "benchmark": "Sand3D-native Nyfasi engineering intelligence",
        "benchmark_version": "0.1.0",
        "status": "passed" if passed == len(results) else "failed",
        "engine": "Sand3D",
        "engine_version": "1.6.2",
        "baseline_parameter_sha256": sha256(PARAMETER_FILE),
        "scenarios_passed": passed,
        "scenarios_total": len(results),
        "scope": "Procedural regeneration, declared parametric relationships, selected constraints, exports and URDF joint semantics.",
        "not_claimed": [
            "Nyfasi retail dimensional fidelity",
            "manufacturing readiness or tolerances",
            "material or fatigue validation",
            "physical clearance/contact validation",
            "AI model reasoning quality (this harness executes prescribed edits; agent evaluation is a later benchmark track)",
        ],
        "results": results,
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({key: report[key] for key in ("status", "scenarios_passed", "scenarios_total", "baseline_parameter_sha256")}, indent=2))
    return 0 if report["status"] == "passed" else 1


if __name__ == "__main__":
    raise SystemExit(main())
