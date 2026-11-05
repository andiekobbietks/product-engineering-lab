# Interactive assembly explorer

Explore the patent-led reconstruction as a component-level 3D research model. Drag to orbit, scroll to zoom, select components to inspect their evidence classification, and adjust exploded spacing.

<iframe src="assembly-explorer.html" title="Interactive 3D assembly explorer" width="100%" height="760" style="border:1px solid #34445c;border-radius:12px" loading="lazy"></iframe>

[Open the viewer in a full browser tab](assembly-explorer.html){ .md-button .md-button--primary }

## Evidence-to-geometry workflow

1. Public patent descriptions and drawings are interpreted as component concepts.
2. A versioned parameter ledger separates disclosed, derived, measured and assumed values.
3. Sand3D provides editable programmatic modelling patterns and mesh previews.
4. CadFlow builds deterministic B-rep components, validates topology and exports STEP, STL and GLB files.
5. The browser viewer makes the research model inspectable.

The viewer's local GLB loader can inspect an individual generated component, the aggregate nyfasi_research_assembly.glb, or the exploded nyfasi_exploded_preview.glb. The exploded file is the better overview for seeing the component layout; its offsets are for presentation only. For the full component pack, download the nyfasi-cadflow-brep artifact from the [CadFlow workflow](https://github.com/andiekobbietks/product-engineering-lab/actions/workflows/cadflow-cad.yml), extract the aggregate GLB, and load it in the viewer. For the Sand3D export, use the [Sand3D CAD workflow](https://github.com/andiekobbietks/product-engineering-lab/actions/workflows/cad-smoke.yml). Files selected in the viewer remain local to your browser.

## Component status

| Feature | Status |
|---|---|
| Eight teeth in illustrated embodiment | Patent disclosed |
| Approximate tooth width | Patent disclosed |
| Roller radius range | Patent disclosed; selected diameter is derived |
| 180-degree curved wall | Patent illustrated embodiment |
| Seven slots between eight teeth | Geometric interpretation |
| Roller bands, end walls, pins and bearing supports | Partly inferred / assumed |
| Housing and reservoir envelope | Engineering assumptions |
| Fit, tolerances, sealing and performance | Not validated |

This is **not a verified digital twin** of a retail Nyfasi product. A true validated digital twin requires an identified physical unit or authorised source CAD, calibrated measurements, known revision, material and tolerance information, and verification against the physical system. The current work is an evidence-linked digital research prototype.

## Reproduce the models

- [CadFlow B-rep build and outputs](cadflow-reconstruction.md)
- [Sand3D reconstruction script](https://github.com/andiekobbietks/product-engineering-lab/blob/main/experiments/001-nyfasi-reconstruction/scripts/build_reconstruction.py)
- [CAD parameter ledger](https://github.com/andiekobbietks/product-engineering-lab/blob/main/experiments/001-nyfasi-reconstruction/models/cad-parameters.json)
- [Sand3D dataset licence and reuse policy](https://github.com/andiekobbietks/product-engineering-lab/blob/main/experiments/001-nyfasi-reconstruction/models/sand3d-dataset-policy.md)
- [Curved-wall geometry explanation](curved-wall-geometry.md)
- [Colab notebook](https://colab.research.google.com/github/andiekobbietks/product-engineering-lab/blob/main/experiments/001-nyfasi-reconstruction/notebooks/nyfasi_reconstruction_colab.ipynb)

## Documentation and IP boundary

This public research page describes evidence classifications and reproducibility. The repository itself is public, so anything committed here should be treated as public. Third-party CAD and dataset assets are not copied into the repository without a row-level rights review.

The viewer is a research instrument, not engineering approval, manufacturing instruction, a freedom-to-operate opinion or permission to reproduce a protected design. See [licensing](../licensing.md), the [IP register](../ip-register.md) and the [commercial proposal structure](../commercial-proposal.md).
