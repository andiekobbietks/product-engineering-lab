# Nyfasi image references and TRELLIS.2 experiment

## Image inputs collected by CI

The workflow downloads a temporary, short-retention research image set from PDR's industrial-design case study, Nyfasi's official product pages and Core77's design coverage. It validates each file, records dimensions and SHA-256, and uploads the files plus source manifest as a GitHub Actions artifact. The photos are deliberately not committed to the repository or copied into the public Pages site. The artifact is a research convenience, not a grant of image redistribution rights.

Run locally with Python and Pillow:

```bash
python -m pip install Pillow
python experiments/001-nyfasi-reconstruction/scripts/download_reference_images.py
```

## Why both Sand3D and TRELLIS.2 are used

- **Sand3D** remains the canonical editable, parameter-driven assembly. It is where explicit dimensions, component relationships, joints and provenance are controlled.
- **Microsoft TRELLIS.2** is an optional image-to-3D generative route. Its model can produce a textured GLB from a single image, but the output is a visual hypothesis. It cannot establish hidden dimensions, exact scale, mechanical fits, tooth count from occluded views, or internal reservoir construction.
- Compare TRELLIS.2's generated silhouette and surface form against the calibrated photographs. Do not copy its arbitrary scale into the CAD parameter ledger.
- Use the open-product Nyfasi image for a separate generation pass to explore the roller/reservoir appearance. The open and closed images depict different configurations; do not ask one generation to merge them into one physically impossible object.

## TRELLIS.2 requirements and execution

The official Microsoft Research implementation is at https://github.com/microsoft/TRELLIS.2. Its published setup expects Linux, CUDA 12.4 and an NVIDIA GPU with at least 24 GB VRAM; the project reports validation on A100/H100. Standard GitHub-hosted runners do not provide that GPU. The model inference script is therefore opt-in and must run on an appropriately provisioned GPU machine or the official hosted demo.

Example, from the official TRELLIS.2 environment:

```bash
python experiments/001-nyfasi-reconstruction/scripts/run_trellis2_image_to_3d.py \
  experiments/001-nyfasi-reconstruction/output/reference-images/nyfasi-front.jpg \
  --output experiments/001-nyfasi-reconstruction/output/trellis2/front-hypothesis.glb
```

Repeat with the angled PDR image and the open Nyfasi image as separate inputs. Keep the generated GLBs as separate candidates. The image-to-3D outputs are not engineering measurements or verified digital twins.

## Source and rights register

| Source ID | Publisher | Intended visual evidence | Rights handling |
|---|---|---|---|
| REF-PDR-01 / 02 | PDR | Retail form, comb and cover details | Copyrighted; research artifact only |
| REF-NYFASI-01 / 02 | Nyfasi | Open reservoir/roller and front comb view | Brand imagery; research artifact only |
| REF-CORE77-01 | Core77 | Angled comb/tooth profile | Copyrighted; research artifact only |

Sources:
- https://www.pdr-consultancy.com/work/deluxe-detangler
- https://nyfasi.com/en-us/products/deluxe-detangler
- https://www.core77.com/posts/126476

No source photograph is redistributed in the repository. Obtain permission before publishing images, using them commercially, or creating a public training dataset.
