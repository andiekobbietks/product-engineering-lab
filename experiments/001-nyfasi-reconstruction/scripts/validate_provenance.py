"""Validate evidence references and CAD parameter provenance without Sand3D."""
from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[1]
MODELS = ROOT / "models"
EVIDENCE = ROOT / "evidence"
SCRIPT = ROOT / "scripts" / "build_reconstruction.py"
ALLOWED = {
    "PATENT_DISCLOSED", "PATENT_DERIVED_ESTIMATE", "MEASURED",
    "IMAGE_ESTIMATED", "ENGINEERING_ASSUMPTION", "SUPPLIER_CONFIRMED",
}


def load(path):
    return json.loads(path.read_text(encoding="utf-8"))


def main():
    source_records = load(EVIDENCE / "source-register.json")
    source_ids = {item["id"] for item in source_records}
    cad = load(MODELS / "cad-parameters.json")
    product = load(MODELS / "product-model.json")
    errors = []

    for name, record in cad["parameters"].items():
        if record.get("provenance") not in ALLOWED:
            errors.append(f"{name}: missing or invalid provenance")
        if not record.get("unit") or not record.get("note"):
            errors.append(f"{name}: unit and explanatory note are required")
        if not isinstance(record.get("evidence_ids"), list):
            errors.append(f"{name}: evidence_ids must be a list")
        for source_id in record.get("evidence_ids", []):
            if source_id not in source_ids:
                errors.append(f"{name}: unknown evidence ID {source_id}")
        if record.get("value") is None:
            errors.append(f"{name}: CAD parameter value is null")

    for component in product["components"]:
        for parameter in component["parameters"]:
            if parameter.get("provenance") not in ALLOWED:
                errors.append(f"{component['component_id']}.{parameter['name']}: missing provenance")
            for source_id in parameter.get("evidence_ids", []):
                if source_id not in source_ids:
                    errors.append(f"{component['component_id']}.{parameter['name']}: unknown source {source_id}")

    if "cad-parameters.json" not in SCRIPT.read_text(encoding="utf-8"):
        errors.append("build_reconstruction.py must load cad-parameters.json")

    if errors:
        print("CAD provenance validation FAILED:")
        for error in errors:
            print(f"- {error}")
        return 1

    print(
        f"CAD provenance validation passed: {len(cad['parameters'])} CAD parameters, "
        f"{sum(len(c['parameters']) for c in product['components'])} product-model parameters, "
        f"{len(source_ids)} registered sources."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
