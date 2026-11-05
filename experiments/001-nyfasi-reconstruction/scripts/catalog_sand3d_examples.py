"""Create a metadata-only index of relevant Sand3D CAD examples."""
from __future__ import annotations
import argparse
import json
from pathlib import Path
from datasets import Image, load_dataset

DATASETS=("sand3d-cad","sand3d-objaverse","sand3d-articraft","sand3d-simready","sand3d-automate")
TERMS=("roller","bearing","shaft","housing","wheel","gear","seal","bracket","hinge","spring","pump","motor","cylinder","valve","mechanical","tool","fastener")

def relevant(row):
    haystack=" ".join(str(row.get(k,"")) for k in ("family","entry","program")).lower()
    return any(term in haystack for term in TERMS)

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument("--max-scan",type=int,default=12000)
    parser.add_argument("--max-results",type=int,default=80)
    parser.add_argument("--output",type=Path,default=Path(__file__).resolve().parent.parent/"models"/"sand3d-exemplar-catalog.json")
    args=parser.parse_args()
    result={"schema_version":"1.0.0","purpose":"Metadata-only reference discovery; not product evidence.","datasets":[]}
    for name in DATASETS:
        repo=f"Sandflow/{name}"
        stream=load_dataset(repo,split="train",streaming=True)
        # Keep media as metadata references. We only need text/metadata fields;
        # decoding source images would require Pillow and waste bandwidth.
        for column, feature in stream.features.items():
            if isinstance(feature, Image):
                stream=stream.cast_column(column,Image(decode=False))
        records=[]
        scanned=0
        for row in stream:
            scanned+=1
            if row.get("license_status")=="ok" and relevant(row):
                records.append({k:row.get(k) for k in ("id","family","entry","license","source_license","attribution","license_status","source","asset_id","f_score","sand3d_version","program_sha256","usda_sha256","usda_path")})
                if len(records)>=args.max_results:
                    break
            if scanned>=args.max_scan:
                break
        result["datasets"].append({"repo_id":repo,"rows_scanned":scanned,"matches_recorded":len(records),"records":records})
    args.output.parent.mkdir(parents=True,exist_ok=True)
    args.output.write_text(json.dumps(result,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
    print(f"Indexed {sum(d['matches_recorded'] for d in result['datasets'])} metadata references")

if __name__=="__main__":
    main()
