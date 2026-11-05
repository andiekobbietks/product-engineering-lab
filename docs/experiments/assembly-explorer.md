# Sand3D assembly gallery

The gallery loads the **complete Sand3D assembly GLB**, not seven separately positioned mesh exports. It uses the native GLB node hierarchy and the `s3d_joint` extras written by Sand3D.

[Open the Sand3D assembly gallery](assembly-explorer.html){ .md-button .md-button--primary }

## Gallery capabilities

- **Original assembly coordinates:** the full assembly is loaded as one GLB, preserving the hierarchy created by the Sand3D program.
- **Component tree:** select any of the seven named assembly groups or click its geometry in the viewport.
- **Program-linked inspection:** the exact `build_reconstruction.py` used for the build is published with an AST-generated source map. Selecting a component highlights its generating functions; clicking a nested band, seal, tooth or housing feature selects the corresponding source function. Python syntax is highlighted in the source pane.
- **Joint playback and control:** the viewer discovers the `roller_rotation` joint from Sand3D's `s3d_joint` GLB extras. The slider and Play/Pause control transform that exported joint node. If the joint record is absent, the controls remain unavailable rather than simulating motion.
- **Isolation, wireframe and camera reset:** inspect one group or the whole assembly.
- **Exploded presentation:** the explode control applies clearly labelled display-only offsets. It is not a mechanical movement, assembly clearance or engineering datum.
- **Parameter context:** relevant values are read from the same versioned CAD parameter ledger used by the model build.

The viewer does not silently fall back to schematic geometry. If the generated manifest, assembly, source program or parameter ledger is missing, it reports an explicit error.

## Canonical Sand3D pipeline

`build_reconstruction.py` is the authoritative model program. It builds the assembly, writes the complete GLB, and exports secondary component GLBs for downstream inspection and other consumers. The web gallery uses the complete assembly GLB as its geometry and articulation source of truth. The component GLBs are not independently repositioned to recreate an assembly.

The build also publishes:

- `manifest.json`: component identities, node names, evidence descriptions, source symbols, engine version and joint expectations.
- `build_reconstruction.py`: the exact program used to create the geometry.
- `cad-parameters.json`: the versioned parameter ledger.
- `nyfasi_complete_assembly.glb`: the complete articulated assembly.

Sand3D also produces URDF and USDA for mechanism and scene interchange, plus OBJ for mesh inspection. These exports are generated from the same program and are not separate modelling authorities.

## Evidence and engineering boundary

This remains an evidence-led research proxy, not a verified digital twin of a retail Nyfasi unit. Patent-to-retail-SKU mapping is not confirmed. Many dimensions, materials, retention details, seal geometry and all tolerance values remain assumptions. The gallery proves that the program, assembly hierarchy, exported joint metadata and source map can be inspected together. It does not prove physical fit, sealing performance, fatigue life, manufacturability or regulatory suitability.

See the [Sand3D architecture decision](../decisions/adr-0001-sand3d-canonical-engine.md), [gallery decision](../decisions/adr-0002-sand3d-source-linked-gallery.md), [CAD parameter provenance](cad-parameter-provenance.md), [roller seal and tolerance study](roller-seal-and-tolerance.md) and [validation protocol](nyfasi-validation.md).
