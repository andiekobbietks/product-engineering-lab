# CadFlow B-rep build record · 5 November 2026

<badge>Successful CI build</badge>

- Workflow: [CadFlow B-rep reconstruction #42071621074](https://github.com/andiekobbietks/product-engineering-lab/actions/runs/42071621074)
- Source commit: 137434e1c5728823bb295893b66bd7e6d901c27b
- Engine: CadFlow 0.2.0
- CadFlow source: 43fbac0515a560229d700e07281cc5c08c3f9765
- Geometry kernel: OpenCascade 7.9.3.1
- Python: 3.12
- Units: mm

## Checks completed

| Check | Result |
|---|---|
| Evidence provenance validator | Passed |
| CAD parameter geometry validator | Passed |
| Native build toolchain check | Passed |
| CadFlow source build/install | Passed |
| Component B-rep construction | Passed |
| Component shape validation | Passed |
| STEP/STL/GLB component exports | Passed |
| Aggregate STEP/GLB export | Passed |
| Artifact file-count checks | Passed |
| Artifact upload | Passed |

## Output

- Artifact: nyfasi-cadflow-brep
- Artifact ID: 13436657199
- Files uploaded: 90
- Archive size: 2,017,275 bytes
- SHA-256: a13334ccd160d7fe8d6af34e0912386f7a8bf40ad91e38e0b0dfb1217e1740e4
- Retention expiry: 5 December 2026

The build generated 29 separately validated component outputs, with individual STEP, STL and GLB files. It also generated nyfasi_research_assembly.step and nyfasi_research_assembly.glb as a flattened aggregate preview/export.

## Geometry represented

- Lower housing and upper cap proxies
- Reservoir enclosure proxy
- Roller core with exposed smooth lands
- Seven raised annular roller bands
- Two end walls and two spindle pins
- Two bored bearing-support blocks
- Semi-cylindrical curved wall, divided into eight arc solids by seven interpreted slots
- Eight comb-tooth proxies
- Two snap-tab proxies
- Perimeter gasket proxy

## Interpretation and limits

This confirms the B-rep geometry was generated, validated by CadFlow's shape checks and exported. It does not establish dimensional accuracy or mechanical performance.

The curved wall's eight-solid result is the expected topology of the current seven-through-slot interpretation. The aggregate is a flattened geometry preview, not a kinematic assembly. Individual component exports and the manifest are the appropriate files for detailed CAD inspection.

No authorised physical sample, native supplier CAD or production drawing was used. Housing, bearing, seal, retention, material and fit details remain assumptions or proxies. The model is not a verified digital twin, manufacturing release or permission to reproduce a protected product.
