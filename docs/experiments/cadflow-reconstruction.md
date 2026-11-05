# CadFlow B-rep reconstruction

This experiment adds a deterministic CAD layer alongside the existing Sand3D programmatic 3D workflow.

## Why two tools?

- **Sand3D** is an LLM-friendly 3D-as-code language and dataset ecosystem. Its examples demonstrate named parts, editable parameters, materials and object hierarchies.
- **CadFlow** is a Python CAD SDK over OpenCascade. It builds and measures deterministic boundary-representation geometry, validates topology, and exports STEP, STL and GLB previews. It is not a text-to-3D model.

CadFlow is the geometry-grounded construction and inspection layer. Sand3D remains a useful reference for readable part programs and presentation. Neither tool supplies missing Nyfasi product measurements.

## Reproducible source

- [CadFlow upstream repository](https://github.com/yhz5613813/CadFlow)
- [CadFlow README and demos](https://github.com/yhz5613813/CadFlow#readme)
- [CadFlow Python package](https://pypi.org/project/cadflow/)
- [Pinned CadFlow source commit](https://github.com/yhz5613813/CadFlow/commit/43fbac0515a560229d700e07281cc5c08c3f9765)
- [CadFlow MIT licence](https://github.com/yhz5613813/CadFlow/blob/main/LICENSE)

Upstream examples demonstrate B-rep modelling, inspection, STEP export, GLB preview, assemblies and component-oriented product structures. CadFlow is alpha software; the workflow pins a source revision.

## Build outputs

The script scripts/build_cadflow_reconstruction.py reads the shared models/cad-parameters.json ledger and generates separately named components: housing shells, reservoir envelope, roller core and raised bands, end walls, spindle pins, bearing supports with bores, curved slotted wall, eight comb teeth and snap-tab proxies.

Each component is validated before export. STEP is the editable CAD exchange artefact; STL and GLB are derivative mesh/preview formats. The build manifest records component bounds, volume, topology and validation reports. The build also emits a flattened aggregate STEP/GLB and a presentation-only exploded GLB. The exploded preview applies visual offsets to separate the parts; those offsets are not engineering clearances. The separately exported component STEP files and manifest retain the component IDs; neither aggregate is a constraint-solved assembly.

Generated files are CI artefacts, not committed binary CAD. Download the nyfasi-cadflow-brep workflow artifact.

## Reproduce

- [Open the CadFlow Colab notebook](https://colab.research.google.com/github/andiekobbietks/product-engineering-lab/blob/main/experiments/001-nyfasi-reconstruction/notebooks/nyfasi_cadflow_reconstruction_colab.ipynb)
- [View the CadFlow build workflow](https://github.com/andiekobbietks/product-engineering-lab/actions/workflows/cadflow-cad.yml)

Use Python 3.12 and follow .github/workflows/cadflow-cad.yml, then run:

~~~bash
python experiments/001-nyfasi-reconstruction/scripts/build_cadflow_reconstruction.py
~~~

## Accuracy boundary

This is a higher-integrity CAD construction path, not proof of high dimensional fidelity. It improves geometric exactness and inspection compared with a browser-only mesh, but it does not improve the underlying evidence. The model still mixes patent-disclosed, patent-derived and assumed values. No physical sample, supplier drawing, original native CAD or tolerance specification has been verified.

A validated digital twin requires calibrated measurements from an identified product revision, documented uncertainty, materials and tolerances, and comparison against the physical system. Do not use these files for manufacture, fit checks or product claims.
