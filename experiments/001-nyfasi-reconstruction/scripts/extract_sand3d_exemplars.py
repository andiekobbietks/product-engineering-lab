"""Extract a small, rights-screened set of Sand3D mechanical exemplar programs.

The output is a temporary research artifact with attribution metadata. It does
not download or redistribute source meshes/USD assets and is not product evidence.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path
from datasets import Image, load_dataset

TARGETS = {
    "sand3d-automate": {
        "roller_conveyor", "flanged_bearing", "shaft_and_bearing_block",
        "gear_reducer", "gear_train",
    },
    "sand3d-simready": {
        "bearing", "stepped_ring", "sprayer", "pump", "reservoir",
    },
    "sand3d-articraft": {"single_revolute_hinge"},
    "sand3d-objaverse": {"housing", "cylinder_valve"},
}
ALLOWED_SOURCE_LICENSES = {"CC0-1.0", "CC-BY-4.0", "Apache-2.0"}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--max-scan", type=int, default=20000)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()

    result = {
        "schema_version": "1.0.0",
        "purpose": "Small, attribution-bearing Sand3D program references for modelling-pattern research only.",
        "policy": {
            "license_status_required": "ok",
            "program_license_required": "CC-BY-4.0",
            "source_license_allowlist": sorted(ALLOWED_SOURCE_LICENSES),
            "source_meshes_downloaded": False,
            "source_usd_downloaded": False,
            "nyfasi_product_evidence": False,
        },
        "datasets": [],
    }

    for dataset_name, wanted_entries in TARGETS.items():
        repo_id = f"Sandflow/{dataset_name}"
        stream = load_dataset(repo_id, split="train", streaming=True)
        for column, feature in stream.features.items():
            if isinstance(feature, Image):
                stream = stream.cast_column(column, Image(decode=False))

        matches = {}
        scanned = 0
        for row in stream:
            scanned += 1
            entry = str(row.get("entry") or "")
            if entry not in wanted_entries:
                if scanned >= args.max_scan:
                    break
                continue

            if row.get("license_status") != "ok":
                continue
            if row.get("license") != "CC-BY-4.0":
                continue
            source_license = str(row.get("source_license") or "")
            if source_license not in ALLOWED_SOURCE_LICENSES:
                continue

            program = row.get("program")
            if isinstance(program, str):
                program_text = program
            elif isinstance(program, dict):
                program_text = str(
                    program.get("source")
                    or program.get("code")
                    or program.get("program")
                    or json.dumps(program, ensure_ascii=False)
                )
            elif program is not None:
                program_text = json.dumps(program, ensure_ascii=False)
            else:
                continue
            if not program_text.strip():
                continue

            matches[entry] = {
                "id": row.get("id"),
                "family": row.get("family"),
                "entry": entry,
                "license": row.get("license"),
                "source_license": source_license,
                "license_status": row.get("license_status"),
                "attribution": row.get("attribution"),
                "source": row.get("source"),
                "asset_id": row.get("asset_id"),
                "f_score": row.get("f_score"),
                "sand3d_version": row.get("sand3d_version"),
                "program_sha256": row.get("program_sha256"),
                "program": program_text,
            }
            if wanted_entries.issubset(matches.keys()):
                break
            if scanned >= args.max_scan:
                break

        result["datasets"].append({
            "repo_id": repo_id,
            "rows_scanned": scanned,
            "requested_entries": sorted(wanted_entries),
            "matched_entries": sorted(matches),
            "missing_entries": sorted(wanted_entries - matches.keys()),
            "records": [matches[key] for key in sorted(matches)],
        })

    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        json.dumps(result, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    missing = [
        f"{dataset['repo_id']}:{entry}"
        for dataset in result["datasets"]
        for entry in dataset["missing_entries"]
    ]
    print(
        f"Extracted {sum(len(d['records']) for d in result['datasets'])} "
        "attributed programs"
    )
    if missing:
        print("Unmatched requested exemplars:", ", ".join(missing))


if __name__ == "__main__":
    main()
