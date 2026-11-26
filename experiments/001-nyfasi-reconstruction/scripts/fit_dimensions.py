"""Fit calibrated dimensional observations without silently rewriting the CAD ledger."""
from __future__ import annotations
import argparse
import json
from collections import defaultdict
from pathlib import Path
from scipy.optimize import least_squares

ROOT = Path(__file__).resolve().parents[1]
LEDGER = ROOT / "models" / "cad-parameters.json"

def fit_group(rows):
    values = [float(row["value_mm"]) for row in rows]
    sigmas = [float(row["sigma_mm"]) for row in rows]
    if any(value <= 0 for value in values) or any(sigma <= 0 for sigma in sigmas):
        raise ValueError("Measurements and standard deviations must be positive")
    def residual(candidate):
        return [(candidate[0] - value) / sigma for value, sigma in zip(values, sigmas)]
    initial = sum(value / sigma**2 for value, sigma in zip(values, sigmas)) / sum(1 / sigma**2 for sigma in sigmas)
    result = least_squares(residual, [initial], loss="soft_l1", f_scale=1.0)
    estimate = float(result.x[0])
    uncertainty = sum(1 / sigma**2 for sigma in sigmas) ** -0.5
    return {
        "estimate_mm": round(estimate, 4),
        "standard_uncertainty_mm": round(uncertainty, 4),
        "observation_count": len(rows),
        "independent_views": len({row["view_id"] for row in rows}),
        "source_ids": sorted({row["source_id"] for row in rows}),
        "calibration_ids": sorted({row["calibration_id"] for row in rows}),
        "residuals_mm": [round(value - estimate, 4) for value in values],
        "classification": "MEASURED" if len({r["view_id"] for r in rows}) >= 2 and len({r["calibration_id"] for r in rows}) >= 2 else "IMAGE_ESTIMATED",
    }

def build_report(payload, ledger):
    grouped = defaultdict(list)
    for row in payload.get("observations", []):
        required = ("parameter", "value_mm", "sigma_mm", "source_id", "view_id", "calibration_id")
        missing = [key for key in required if key not in row or row[key] in (None, "")]
        if missing:
            raise ValueError("Observation missing required fields: " + ", ".join(missing))
        if row["parameter"] not in ledger["parameters"]:
            raise ValueError("Unknown CAD parameter: " + row["parameter"])
        grouped[row["parameter"]].append(row)
    return {
        "schema_version": "1.0.0",
        "units": "mm",
        "method": "SciPy least_squares(loss=soft_l1), inverse-variance weighting",
        "ledger_is_modified": False,
        "fits": {name: fit_group(rows) for name, rows in sorted(grouped.items())},
        "limitations": [
            "A fitted image measurement is not automatically a retail-manufacturing measurement.",
            "Views must be independently captured and metric-calibrated.",
            "Planar homography does not correct depth variation on curved surfaces.",
            "Unseen internal dimensions cannot be inferred from exterior photographs alone.",
            "Human review and source-rights checks are required before promoting any value.",
        ],
    }

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("observations", type=Path)
    parser.add_argument("--output", type=Path, default=Path("dimension-fit-report.json"))
    args = parser.parse_args()
    ledger = json.loads(LEDGER.read_text(encoding="utf-8"))
    report = build_report(json.loads(args.observations.read_text(encoding="utf-8")), ledger)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(f"Wrote {len(report['fits'])} fits to {args.output}; canonical ledger unchanged.")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
