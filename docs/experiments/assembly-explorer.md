# Interactive assembly explorer

Explore the current patent-led reconstruction as a component-level 3D research model. Drag to orbit, scroll to zoom, select components to inspect their evidence classification, and adjust the exploded spacing.

<iframe src="assembly-explorer.html" title="Interactive 3D assembly explorer" width="100%" height="760" style="border:1px solid #34445c;border-radius:12px" loading="lazy"></iframe>

[Open the viewer in a full browser tab](assembly-explorer.html){ .md-button .md-button--primary }

## What this demonstrates

The viewer makes the evidence-to-model workflow tangible:

1. Public patent descriptions and drawings are interpreted as component concepts.
2. A product model separates component identity from numeric parameters.
3. A parameter ledger records whether each value is disclosed, derived, measured or assumed.
4. Sand3D produces an editable research assembly.
5. A browser visualiser makes the component structure inspectable.

The viewer includes a procedural preview and a local GLB loader. To inspect the latest Sand3D output, download the `nyfasi-curved-wall-research-proxy` artifact from the [CAD workflow](https://github.com/andiekobbietks/product-engineering-lab/actions/workflows/cad-smoke.yml), extract the GLB, then use **Load Sand3D GLB**. The selected file is loaded locally in your browser and is not uploaded.

## Evidence and geometry boundary

| Feature | Status |
|---|---|
| Eight teeth in illustrated embodiment | Patent disclosed |
| Approximate tooth width | Patent disclosed |
| Roller radius range | Patent disclosed; selected diameter is derived |
| 180° curved wall | Patent illustrated embodiment |
| Seven slots between eight teeth | Geometric interpretation |
| Housing and reservoir envelope | Engineering assumptions |
| Fit, tolerances, sealing and performance | Not validated |

This is **not a verified digital twin** of a retail Nyfasi product. A true validated digital twin would require an identified physical unit or authorised source CAD, calibrated measurements, known revision, material and tolerance information, and verification against the physical system. The current work is an evidence-linked digital research prototype.

## Latest component-level iteration

The current Sand3D build now separates the housing halves, reservoir, curved slotted wall, tooth array, knurled roller bands, smooth lands, end walls, spindle pins, bearing supports, snap-fit proxies and perimeter gasket. The roller is represented with a continuous revolute joint. These details improve editability and make the assumptions inspectable; they do not establish measured fidelity. See the [Sand3D dataset and demo strategy](sand3d-dataset-strategy.md).

## Reproduce the model

- [Colab notebook](https://colab.research.google.com/github/andiekobbietks/product-engineering-lab/blob/main/experiments/001-nyfasi-reconstruction/notebooks/nyfasi_reconstruction_colab.ipynb)
- [Sand3D reconstruction script](https://github.com/andiekobbietks/product-engineering-lab/blob/main/experiments/001-nyfasi-reconstruction/scripts/build_reconstruction.py)
- [CAD parameter ledger](https://github.com/andiekobbietks/product-engineering-lab/blob/main/experiments/001-nyfasi-reconstruction/models/cad-parameters.json)
- [Curved-wall geometry explanation](curved-wall-geometry.md)
- [Latest build manifest](https://github.com/andiekobbietks/product-engineering-lab/blob/main/experiments/001-nyfasi-reconstruction/builds/2026-11-05-curved-wall.md)

## Documentation and IP boundary

This public research page describes observable functionality, evidence classifications and reproducibility. It does not publish confidential customer data, private source material or any third-party CAD that has not been authorised for redistribution. The repository itself is public, so anything committed here should be treated as public.

The viewer is a research instrument, not engineering approval, manufacturing instruction, a freedom-to-operate opinion or permission to reproduce a protected design. See [licensing](../licensing.md), the [IP register](../ip-register.md) and the [commercial proposal structure](../commercial-proposal.md).
