# TRELLIS.2 mesh inspection and repair

## Purpose

This stage starts after the official Microsoft TRELLIS.2 Space, Colab notebook or local CUDA route has produced a GLB. It does not require a GPU. It uses the Python mesh ecosystem to turn that output into an inspectable, traceable candidate while keeping the original file immutable.

## Install

```bash
python -m pip install -r requirements-reconstruction.txt
```

The baseline stack includes NumPy/SciPy and Trimesh. PyMeshFix is kept in a separate optional requirements file because it is AGPL-3.0 licensed; review that licence against the intended distribution and deployment model before installing or redistributing it. Open3D and PyMeshLab are also deliberately not mandatory: they add substantial binary dependencies and should be introduced only when the experiment needs point-cloud registration, surface reconstruction or advanced remeshing.

## Inspect a downloaded GLB

```bash
python experiments/001-nyfasi-reconstruction/scripts/process_trellis2_mesh.py \
  nyfasi_trellis2_hypothesis.glb \
  --report output/trellis2/nyfasi_mesh_report.json
```

The report includes source SHA-256, scene geometry nodes, vertex/face counts, model-space bounds and extents, surface area, connected components, winding consistency, watertightness, Euler characteristic and volume when the mesh is watertight.

**Units remain unknown.** TRELLIS.2's model-space bounds must not be labelled millimetres or used to update the Sand3D dimension ledger.

## Optional topology repair

```bash
python experiments/001-nyfasi-reconstruction/scripts/process_trellis2_mesh.py \
  nyfasi_trellis2_hypothesis.glb \
  --report output/trellis2/nyfasi_mesh_report.json \
  --repair-output output/trellis2/nyfasi_mesh_repaired.glb
```

The pipeline first removes unreferenced vertices and corrects winding/normals. If the mesh is still open, the optional PyMeshFix backend attempts a topology repair. It does not silently discard small connected components. The original GLB is never overwritten.

PyMeshFix can change geometry and may not preserve PBR materials, UVs, or the appearance of fine comb teeth. Treat the repaired GLB as a diagnostic derivative. Compare it with the untouched GLB before using it for any downstream work.

## Further Python ecosystem stages

- **Trimesh:** scene/GLB inspection, mesh metrics, component analysis and exports.
- **PyMeshFix:** conservative repair attempt for holes and non-manifold defects.
- **Open3D (optional next stage):** point-cloud filtering, FPFH/RANSAC registration and ICP alignment when calibrated multi-view scans or a physical scan exist.
- **PyMeshLab (optional next stage):** controlled quadric decimation, remeshing and surface-quality experiments. Preserve a copy before any lossy operation.
- **SciPy:** robust fitting of measured dimensions and uncertainty, not invented scale.
- **OpenCV:** calibrated planar rectification of product photographs.

Do not run aggressive smoothing or decimation before measuring silhouette error. The comb teeth, roller edges and narrow slots are high-value features and are especially vulnerable to generic mesh cleanup.

## Promotion gate

A processed mesh can be promoted to a comparison candidate only after recording source image ID, TRELLIS.2 model/revision, generation route/settings, source and output hashes, repair operations, and visual review. It cannot replace the Sand3D assembly or populate physical dimensions without calibrated evidence.
