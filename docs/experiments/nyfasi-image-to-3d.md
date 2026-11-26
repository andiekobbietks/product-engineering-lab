# Nyfasi image references and TRELLIS.2 experiment

## Image inputs collected by CI

The workflow downloads a temporary, short-retention research image set from PDR's industrial-design case study, Nyfasi's official product pages and Core77's design coverage. It validates each file, records dimensions and SHA-256, and uploads the files plus source manifest as a GitHub Actions artifact. The photos are deliberately not committed to the repository or copied into the public Pages site. The artifact is a research convenience, not a grant of image redistribution rights.

Run locally with Python and Pillow:

```bash
python -m pip install Pillow
python experiments/001-nyfasi-reconstruction/scripts/download_reference_images.py
```

## Generate with the official Hugging Face Space

Use Microsoft's hosted TRELLIS.2 Space directly:

**https://huggingface.co/spaces/microsoft/TRELLIS.2**

The Space is currently listed as running on ZeroGPU. It exposes an image upload, generation preview and an **Extract GLB** step. Its UI accepts PNG images and recommends an alpha-masked foreground object. For ordinary opaque product photographs, its upload preprocessing attempts background removal automatically. Check the preview carefully: the fine comb teeth and narrow gaps can be damaged by segmentation.

Recommended Nyfasi runs, one image per generation:

1. **REF-PDR-01** `pdr-hero.jpg`: best first pass for the closed retail form and overall silhouette.
2. **REF-PDR-02** `pdr-detail.jpg`: separate pass for cover/comb detail.
3. **REF-NYFASI-01** `nyfasi-open-product.png`: separate pass for the open reservoir and roller configuration.
4. **REF-NYFASI-02** `nyfasi-front.jpg`: separate pass for front-facing tooth arrangement.
5. **REF-CORE77-01** `core77-comb-angle.jpg`: separate pass for another angled view.

Do not combine the open and closed product photographs into one input. They depict different configurations. Generate separate candidates and retain the source ID with each downloaded GLB. Start at 1024 resolution; increase only if the first result preserves the thin teeth and silhouette. Use **Extract GLB** after reviewing the preview, then download the model.

The Space reports that uploaded images are temporarily cached on Hugging Face and deleted after the session ends. Avoid uploading confidential or private material. The source photographs remain third-party copyrighted material; public accessibility does not grant redistribution permission.

## Why both Sand3D and TRELLIS.2 are used

- **Sand3D** remains the canonical editable, parameter-driven assembly. It is where explicit dimensions, component relationships, joints and provenance are controlled.
- **Microsoft TRELLIS.2** generates a textured GLB from one image. Its output is a visual hypothesis, not a measured reconstruction.
- Compare generated silhouettes and surface form against calibrated photographs. Do not copy arbitrary generated scale into the CAD parameter ledger.
- A single photograph cannot establish hidden geometry, exact physical scale, mechanical fits, tooth count where occluded, or internal reservoir construction. Use multiple calibrated views and physical measurements for those.

## Source and rights register

| Source ID | Publisher | Intended visual evidence | Rights handling |
|---|---|---|---|
| REF-PDR-01 / 02 | PDR | Retail form, comb and cover details | Copyrighted; research artifact only |
| REF-NYFASI-01 / 02 | Nyfasi | Open reservoir/roller and front comb view | Brand imagery; research artifact only |
| REF-CORE77-01 | Core77 | Angled comb/tooth profile | Copyrighted; research artifact only |

Sources:
- https://www.microsoft.com/en-us/research/workbench/project/trellis
- https://huggingface.co/spaces/microsoft/TRELLIS.2
- https://www.github.com/microsoft/TRELLIS.2
- https://www.pdr-consultancy.com/work/deluxe-detangler
- https://nyfasi.com/en-us/products/deluxe-detangler
- https://www.core77.com/posts/126476

No source photograph is redistributed in the repository. Obtain permission before publishing images, using them commercially, or creating a public training dataset.
