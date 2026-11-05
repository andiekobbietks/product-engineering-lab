# Sand3D complete-roller build record · 5 November 2026

**Status:** successful procedural geometry/export smoke test.

- Workflow: [Sand3D reconstruction smoke test #42071636587](https://github.com/andiekobbietks/product-engineering-lab/actions/runs/42071636587)
- Source commit: d2cd7acee6ecf5b7fe4c289692832b80b4e8f362
- Sand3D: 1.6.2 (pinned)
- Python: 3.13
- Artifact: nyfasi-curved-wall-research-proxy
- Artifact ID: 13437046910
- Archive size: 1,093,422 bytes
- SHA-256: 8fb927bd321084d1da876d88fe3478b3268022ed688cd9ef32512dd657f64677
- Retention expiry: 19 November 2026

## Checks completed

| Check | Result |
|---|---|
| Evidence provenance validator | Passed |
| Curved-wall geometry consistency validator | Passed |
| Sand3D component/assembly generation | Passed |
| GLB / OBJ export | Passed |
| Artifact upload | Passed |

## Geometry represented

- 180-degree semi-cylindrical wall and concave roller seat
- Seven interpreted axial slots between eight tooth proxies
- Roller core and seven procedurally knurled annular bands
- Exposed smooth lands between the bands
- Two end walls and spindle pins
- Two bearing-support proxies with bores
- Lower housing and inverted upper cap proxies
- Reservoir volume proxy
- Snap-fit tabs and perimeter gasket proxy
- Continuous X-axis roller rotation joint in the procedural assembly description

The procedural texture is a visual feature, not evidence of the original roller's exact texture or pitch. Housing, retention, bearing, gasket and most roller dimensions remain assumptions.

## Relationship to CadFlow

Use this artifact for a readable procedural assembly preview and web visualisation. Use the separate [CadFlow B-rep build](2026-11-05-cadflow-brep.md) for validated component solids and STEP/STL exchange. Neither output is a verified retail digital twin.

## Limitations

Successful export establishes that Sand3D generated the geometry and wrote the expected formats. It does not establish dimensional accuracy, fit, sealing, material behaviour, durability, manufacturing suitability or identity with a Nyfasi retail revision. No authorised physical sample, supplier drawing or original CAD was used.
