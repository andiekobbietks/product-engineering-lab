# Complete roller mechanism reconstruction

**Status:** patent-led research geometry, not production CAD.  
**Primary reference:** [GB2591502A](https://patents.google.com/patent/GB2591502A/en), cross-checked against [EP4096470B1 official EPO publication](https://data.epo.org/publication-server/rest/v1.2/publication-dates/2024-08-21/patents/EP4096470NWB1/document.pdf).

## Patent-supported architecture

The patent describes a roller drum with circumferential textured bands/projections aligned to curved-wall slots, smoother intervening surfaces that act as sealing lands, end walls and spindle pins. The housing retains the roller at its ends. Embodiments also describe upper/lower housing engagement with resilient sealing and snap-fit features.

The patent figures are schematic. They do not provide dimensions, tolerances, material grades or flexural design sufficient for manufacture.

## Components now represented in Sand3D

1. Smooth roller core and intervening sealing lands.
2. Seven raised circumferential bands, aligned with the seven modelled wall slots.
3. Two roller end walls.
4. Two coaxial spindle pins.
5. Two bored housing bearing-support blocks.
6. Two simplified housing snap-fit tabs.
7. The previously modelled 180-degree curved wall, seven arc slots and eight tooth proxies.
8. Upper/lower housing and reservoir envelope proxies.

The model preserves component names and separate solids in assembly groups where supported. The seven-band mapping, all component dimensions and retention geometries are assumptions unless explicitly labelled otherwise in the parameter ledger.

## Parameter ledger

| Parameter | Current value | Classification |
|---|---:|---|
| Roller outer diameter | 24 mm | Patent-derived estimate |
| Smooth core diameter | 22.6 mm | Engineering assumption |
| Textured bands | 7 | Engineering interpretation |
| Band width | 2 mm | Engineering assumption |
| Band radial projection | 0.7 mm | Engineering assumption |
| End-wall diameter | 25 mm | Engineering assumption |
| End-wall thickness | 1.5 mm | Engineering assumption |
| Spindle-pin diameter | 4 mm | Engineering assumption |
| Spindle-pin projection | 5 mm | Engineering assumption |
| Bearing block | 8 × 12 × 18 mm | Engineering assumption |
| Bearing radial clearance | 0.25 mm | Engineering assumption |
| Snap-fit tabs | 2 | Engineering assumption |
| Snap-tab dimensions | 8 × 3 × 5 mm | Engineering assumption |

All parameters, evidence IDs, confidence levels and notes are stored in [cad-parameters.json](https://github.com/andiekobbietks/product-engineering-lab/blob/main/experiments/001-nyfasi-reconstruction/models/cad-parameters.json).

## Build and validation

From the experiment directory:

```bash
python scripts/validate_provenance.py
python scripts/validate_geometry.py
python scripts/build_reconstruction.py
```

The geometry validator checks arithmetic, dimensional relationships and envelope consistency. The Sand3D CI workflow tests script execution and GLB/OBJ export. Neither test establishes rotational clearance under load, bearing friction, seal compression, snap-fit fatigue, leak-tightness, durability, material suitability or manufacturing readiness.

## Next engineering work

- Replace simple annular bands with the exact disclosed texture/projection pattern after careful figure inspection and, ideally, an authorised sample.
- Add the elastomeric seal as a separate component and define a measurable compression interface.
- Refine bearing supports and spindle retention using an authorised physical sample or supplier drawing.
- Model snap-fit hooks, lead-ins, undercuts and flexural beams only after dimensions and material data are evidenced.
- Add contact/clearance inspection and a controlled tolerance stack.
- Compare the model against calibrated photographs or a physical sample.

## Rights boundary

This is a research proxy based on public patent disclosure. It is not Nyfasi's original CAD, a verified retail revision, a manufacturing package, a freedom-to-operate opinion or permission to commercialise a replica.
