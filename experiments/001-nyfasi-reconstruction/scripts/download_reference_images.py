"""Fetch public Nyfasi product-reference images for short-lived CI analysis artifacts.

Images are not committed or published with the documentation. Their original URLs,
attribution, retrieval time and SHA-256 hashes are recorded in the generated manifest.
Check source rights before any redistribution or commercial use.
"""
from __future__ import annotations
import hashlib, json, time
from pathlib import Path
from urllib.request import Request, urlopen
from PIL import Image
from io import BytesIO

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "output" / "reference-images"
SOURCES = [
    {
        "id": "REF-PDR-01", "filename": "pdr-hero.jpg",
        "url": "https://www.pdr-consultancy.com/cmsassets/general/_newSlideshowImage/Work-Nyfasi-Detangler-Hero.jpg",
        "attribution": "PDR Cardiff Met Company Ltd, Deluxe Detangler case study",
        "purpose": "angled retail-form view; housing, comb teeth and two-tone finish",
        "rights": "third-party copyrighted image; research reference only; no redistribution permission established",
    },
    {
        "id": "REF-PDR-02", "filename": "pdr-detail.jpg",
        "url": "https://www.pdr-consultancy.com/cmsassets/general/Work-Nyfasi-Detangler-Image-10.jpg",
        "attribution": "PDR Cardiff Met Company Ltd, Deluxe Detangler case study",
        "purpose": "cover and comb assembly detail",
        "rights": "third-party copyrighted image; research reference only; no redistribution permission established",
    },
    {
        "id": "REF-NYFASI-01", "filename": "nyfasi-open-product.png",
        "url": "https://nyfasi.com/cdn/shop/files/Untitleddesign_14.png?v=1727448849&width=1445",
        "attribution": "Nyfasi official product listing",
        "purpose": "open product, reservoir and roller presentation",
        "rights": "brand product image; research reference only; no redistribution permission established",
    },
    {
        "id": "REF-NYFASI-02", "filename": "nyfasi-front.jpg",
        "url": "https://nyfasi.com/cdn/shop/files/Nyfasi_Peach_Backgroud-10_fc4b853c-a8f8-4fb2-bb4b-950e745b2fc3.jpg?v=1659789657",
        "attribution": "Nyfasi official website",
        "purpose": "front-facing comb geometry and tooth arrangement",
        "rights": "brand product image; research reference only; no redistribution permission established",
    },
    {
        "id": "REF-CORE77-01", "filename": "core77-comb-angle.jpg",
        "url": "https://s3files.core77.com/blog/images/1463053_81_126476_pwGkpogql.jpg",
        "attribution": "Core77 industrial design case study",
        "purpose": "angled comb and tooth profile",
        "rights": "third-party copyrighted image; research reference only; no redistribution permission established",
    },
]
def main():
    OUT.mkdir(parents=True, exist_ok=True)
    records=[]
    for source in SOURCES:
        request=Request(source["url"], headers={"User-Agent":"Nyfasi-Research-ReferenceBot/1.0 (GitHub Actions; non-commercial research)"})
        with urlopen(request, timeout=45) as response:
            data=response.read()
            content_type=response.headers.get("Content-Type","")
        image=Image.open(BytesIO(data))
        image.verify()
        image=Image.open(BytesIO(data)).convert("RGB")
        if image.width < 300 or image.height < 200:
            raise ValueError(f"Reference image too small: {source['id']} {image.size}")
        path=OUT/source["filename"]
        path.write_bytes(data)
        records.append({
            **source, "downloaded_at_utc":time.strftime("%Y-%m-%dT%H:%M:%SZ",time.gmtime()),
            "content_type":content_type, "bytes":len(data),
            "width_px":image.width, "height_px":image.height,
            "sha256":hashlib.sha256(data).hexdigest(),
            "local_file":source["filename"],
        })
        print(f"{source['id']}: {image.width}x{image.height} {len(data)} bytes")
    (OUT/"manifest.json").write_text(json.dumps({
        "schema_version":"1.0.0",
        "note":"Temporary CI research inputs; not a redistribution licence or metric calibration.",
        "sources":records,
    },indent=2)+"\n",encoding="utf-8")
    print(f"Fetched and verified {len(records)} images into {OUT}")
if __name__=="__main__": main()
