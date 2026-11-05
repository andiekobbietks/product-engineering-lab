# Build record — curved-wall iteration, 5 November 2026

**Status:** successful Sand3D export smoke test; geometry consistency checks passed.  
**Workflow:** [Sand3D reconstruction smoke test #42065639230](https://github.com/andiekobbietks/product-engineering-lab/actions/runs/42065639230)  
**Source commit:** dca9a33d36471f3f28cffbeac743b9be3d102651  
**Sand3D:** 1.6.2 (pinned)  
**Python:** 3.13 (GitHub Actions runner)

## Checks completed

| Check | Result |
|---|---|
| Evidence provenance validator | Passed |
| Curved-wall geometry consistency validator | Passed |
| Sand3D assembly build | Passed |
| GLB / OBJ export | Passed |
| Artifact upload | Passed |
| MkDocs strict build | Passed at [run #42065708254](https://github.com/andiekobbietks/product-engineering-lab/actions/runs/42065708254) |

## Geometry represented

- 180-degree semi-cylindrical wall segment, selected from the Figure 6B embodiment.
- Concave roller seat radius: 12.5 mm (12 mm roller radius plus 0.5 mm assumed radial clearance).
- Convex wall outer radius: 14.5 mm (2 mm assumed wall thickness).
- Eight blade-tooth proxies at a provisional 15 mm centre pitch.
- Seven 2 mm-wide axial-band cuts, interpreted as circumferential arc slots in the wall cross-section, one in each gap between adjacent teeth.
- 112 mm provisional roller and wall axial length, selected to span the current 110 mm tooth-row envelope.

All dimensions other than the patent-described embodiment values and the selected 180-degree example are assumptions or derived proxies. The patent does not provide the fit, tolerance, wall thickness, slot width, roller length or complete manufacturing dimensions.

## Generated artifact

- Artifact: `nyfasi-curved-wall-research-proxy`
- Artifact ID: `13433527348`
- Archive size: 15,429 bytes
- Archive SHA-256: `205fb3673a1e49140ebacda1cc9b5d44acbad00fbd6550377fe3f30bc843bbfd`
- Retention expiry: 19 November 2026
- Exports: `hair_applicator_curved_wall_exploded.glb` and `hair_applicator_curved_wall_exploded.obj`

## What the checks do not establish

The geometry validator checks internal arithmetic and layout consistency only. A successful Sand3D export proves the model can be generated and exported, not that its shape is dimensionally accurate, mechanically functional, leak-tight, manufacturable or identical to a Nyfasi retail revision. No authorised physical sample, production drawing or supplier CAD was used. Visual inspection and reference-sample metrology remain outstanding.
