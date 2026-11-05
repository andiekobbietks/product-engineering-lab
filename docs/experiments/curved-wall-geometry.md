# Curved roller-seat and arcuate-slot reconstruction

**Status:** patent-led research geometry, not production CAD.  
**Primary reference:** [GB2591502A / GB2591502B patent family](https://patents.google.com/patent/GB2591502A/en), cross-checked against [EP4096470B1, Figures 5 and 6](https://data.epo.org/publication-server/rest/v1.2/publication-dates/2024-08-21/patents/EP4096470NWB1/document.pdf).

## What the drawings establish

- **Figure 5** shows a transverse section: a roller sits against a concave inner face of a curved wall; the opposite face is convex and carries the comb teeth. Openings pass through the curved wall to expose portions of the roller.
- **Figure 6A** shows a cylindrical wall segment with an obtuse central angle greater than 90 degrees.
- **Figure 6B** shows an approximately 180-degree semi-cylindrical segment. The text explains that larger angles increase the arc length of the wall and slots; angles greater than 180 degrees may overhang the roller and complicate removal.
- The description states that each slot follows a circular arc around the cylindrical segment. The roller's textured circumferential bands align with the slots.
- The illustrated embodiment has eight teeth. The description gives approximately 5 mm tooth width, approximately 10 mm spacing between adjacent teeth, and tooth length approximately twice tooth width.

The figures are schematic patent drawings, not dimensioned manufacturing drawings. The 180-degree arc is a disclosed example selected for this model iteration, not a verified retail measurement.

## Model interpretation

The reconstruction uses a coordinate convention with the roller axis and tooth row along X. The roller is a cylindrical drum. The wall is modelled as a 180-degree annular cylinder segment underneath the roller, producing a concave seat on the inside and a convex exterior on the outside.

Seven narrow slot cuts are placed at the centres of the seven clear gaps between eight teeth. Each cut is an axial band through the semi-cylindrical wall; viewed in cross-section, the opening follows the retained circular arc. This is an explicit modelling interpretation of the patent's statement that slots are interposed between teeth and extend circumferentially around the cylinder segment. The exact slot count, axial width and retail layout are not confirmed by a dimensioned drawing.

## Parameter ledger

| Parameter | Current value | Classification | Interpretation |
|---|---:|---|---|
| Roller diameter | 24 mm | Patent-derived estimate | 12 mm radius selected within the disclosed 10–30 mm example range |
| Seat radial clearance | 0.5 mm | Engineering assumption | Placeholder fit; no tolerance disclosed |
| Wall thickness | 2 mm | Engineering assumption | Placeholder solid thickness |
| Wall segment angle | 180° | Patent disclosed | Figure 6B semi-cylinder example |
| Wall / roller axial length | 112 mm | Engineering assumption | Chosen to cover the provisional 110 mm tooth-row envelope |
| Teeth | 8 | Patent disclosed | Illustrated embodiment |
| Tooth width | approx. 5 mm | Patent disclosed | Approximate embodiment value |
| Tooth length | approx. 10 mm | Patent-derived from text | Twice the approximate 5 mm width |
| Tooth centre pitch | 15 mm | Engineering assumption | 5 mm tooth width + interpreted 10 mm clear gap; spacing convention remains ambiguous |
| Inter-tooth slots | 7 | Engineering interpretation | One opening in each gap between adjacent teeth |
| Slot axial width | 2 mm | Engineering assumption | No patent dimension located |

All numeric values and evidence IDs are maintained in [cad-parameters.json](https://github.com/andiekobbietks/product-engineering-lab/blob/main/experiments/001-nyfasi-reconstruction/models/cad-parameters.json). Do not add independent hard-coded dimensions to the Sand3D script.

## Build and checks

From the experiment directory:

```bash
python scripts/validate_provenance.py
python scripts/validate_geometry.py
python scripts/build_reconstruction.py
```

The geometry validator checks only internal consistency: radii ordering, wall/tooth-row span, slot count and width, and supported arc angle. The Sand3D build workflow separately smoke-tests export generation. Neither check establishes geometric accuracy against a retail sample, sealing performance, fit, material suitability, tolerances or manufacturing readiness.

## Known simplifications

- The wall is a constant-thickness semi-cylinder, not a measured moulded profile.
- The slots are represented as simple axial bands cut through the full 180-degree arc.
- The teeth are rectangular blade proxies. The patent also describes tapered blades and elliptical cross-sections; these are not reconstructed in this iteration.
- Housing, reservoir, wall thickness, clearances, slot width, axial length and tooth pitch remain assumptions or derived proxies.
- Roller texture, textured bands, sealing lands, end walls, spindle pins, snap-fits and the elastomeric seal are not yet modelled in this curved-wall iteration.
- Exact mapping from this patent embodiment to a specific Nyfasi retail SKU/revision remains unverified.

## Evidence and rights boundary

Patent drawings are referenced, not copied into the repository. The patent is not native CAD and does not disclose production tolerances, material grades, tooling dimensions or supplier identity. This model is for research and product-architecture analysis only. It is not a manufacturing package, legal opinion or permission to reproduce protected product features.
