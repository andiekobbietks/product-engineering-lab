# CadFlow B-rep reconstruction

**Status:** active research implementation. The build is not yet certified against an authorised retail sample.

## Why CadFlow is in this project

[CadFlow](https://github.com/yhz5613813/CadFlow) is a Python CAD SDK backed by OpenCascade. It exposes exact boundary-representation (B-rep) modelling, booleans, shape inspection, topology validation, STEP/STL exchange, GLB preview and product-level assembly APIs. The upstream repository is MIT-licensed and documents its OpenCascade notice separately.

The upstream demonstrations are useful engineering references:

- [CadFlow README and demo videos](https://github.com/yhz5613813/CadFlow#demo-videos)
- [Two-stage planetary reducer example](https://github.com/yhz5613813/CadFlow/tree/main/examples/16_compact_two_stage_planetary_reducer)
- [Reinforced mounting bracket example](https://github.com/yhz5613813/CadFlow/blob/main/examples/cadflow_complex_mounting_bracket.py)
- [Modern Python frontend guide](https://github.com/yhz5613813/CadFlow/blob/main/docs/guides/modern-frontend.md)

CadFlow is the preferred engine here for separately validated solids and neutral CAD exchange. It does not replace the evidence ledger or supply missing product dimensions.

## Relationship to Sand3D and the Hugging Face datasets

This repository uses two complementary tools:

- **CadFlow:** OpenCascade B-rep construction, component-level solid validation and STEP/STL export.
- **Sand3D:** concise procedural geometry programs, named parts, articulation and web-friendly GLB/URDF/USD exports.

The five Hugging Face datasets linked from Sand3D belong to the Sandflow project, not CadFlow. They are useful for learning procedural modelling patterns and assembly decomposition. They are not Nyfasi product evidence and do not contain a verified Nyfasi CAD model. See [Sand3D dataset strategy](sand3d-dataset-strategy.md) for the five datasets and rights controls.

The intended pipeline is:

1. Patent, product imagery and authorised measurements populate the evidence register.
2. The CAD parameter ledger classifies every dimension as disclosed, derived, image-estimated, measured, supplier-confirmed or assumed.
3. Sand3D programs provide a readable procedural model and articulated visual preview.
4. CadFlow creates separately inspectable OpenCascade B-rep solids from the same parameter ledger.
5. STEP/STL/GLB outputs and validation reports are compared against new evidence.
6. Discrepancies are recorded; no assumption is promoted to a measured fact because the model looks plausible.

## Current CadFlow components

The script at experiments/001-nyfasi-reconstruction/scripts/build_cadflow_reconstruction.py now builds the following as separate B-rep components:

- Lower housing shell and upper housing cap
- Reservoir enclosure
- Roller core, with the exposed core surface representing smooth lands
- Seven raised annular roller bands
- Two roller end walls and two spindle pins
- Two bored bearing-support blocks
- Semi-cylindrical slotted wall
- Eight comb-tooth proxies
- Two housing snap-tab proxies
- Perimeter gasket proxy

The curved wall is positioned using the same roller-axis datum as the roller. Each named component is checked for positive volume and topology, then exported as STEP, STL and GLB. Most components are single solids; the seven through-slots intentionally divide the curved wall into eight separate arc solids, matching the eight-tooth proxy layout.

For the all-components preview, the current build sequentially unions the named solids into a flattened aggregate B-rep Shape and exports it as STEP/GLB. This is a visual/export convenience, not a constraint-solved product assembly. The individual component files and manifest remain the component-level evidence trail; the aggregate may fuse contacting or intersecting parts and should not be used to infer assembly joints or serviceability.

## Reproduce

- [Open the CadFlow Google Colab notebook](https://colab.research.google.com/github/andiekobbietks/product-engineering-lab/blob/main/experiments/001-nyfasi-reconstruction/notebooks/nyfasi_cadflow_reconstruction_colab.ipynb)

The pinned CI workflow uses Python 3.12, OpenCascade 7.9.3.1 and a pinned CadFlow source commit:

- [CadFlow B-rep workflow](https://github.com/andiekobbietks/product-engineering-lab/actions/workflows/cadflow-cad.yml)
- [CadFlow reconstruction script](https://github.com/andiekobbietks/product-engineering-lab/blob/main/experiments/001-nyfasi-reconstruction/scripts/build_cadflow_reconstruction.py)
- [Shared CAD parameter ledger](https://github.com/andiekobbietks/product-engineering-lab/blob/main/experiments/001-nyfasi-reconstruction/models/cad-parameters.json)

A successful workflow produces an artifact named nyfasi-cadflow-brep. It contains individual component STEP/STL/GLB files, a flattened aggregate STEP/GLB and cadflow-build-manifest.json with volumes, areas, bounding boxes, topology and validation reports.

## Current fidelity boundary

The B-rep representation is more suitable than a mesh-only preview for CAD exchange and topology inspection. It does not make the dimensions more authoritative.

Still unknown or unvalidated:

- Retail unit identity, revision and exact mapping to the patent embodiment
- Housing dimensions, wall thicknesses and corner radii
- Roller diameter, axial length, precise texture profile and material
- Slot cross-section, width and exact count/spacing
- Spindle/bearing fit, axial retention and operating clearances
- Seal profile, compression, material and leak performance
- Snap-fit beam geometry, deflection, fatigue and retention force
- Fluid path, reservoir capacity and manufacturing details

No calibrated retail sample, authorised supplier drawing or original CAD has been used. The model is not a verified digital twin, manufacturing release, freedom-to-operate opinion or permission to reproduce a protected product.
