# Complete roller mechanism reconstruction

**Status:** patent-led research geometry, not production CAD.  
**Primary reference:** [GB2591502A](https://patents.google.com/patent/GB2591502A/en), cross-checked against [EP4096470B1 official EPO publication](https://data.epo.org/publication-server/rest/v1.2/publication-dates/2024-08-21/patents/EP4096470NWB1/document.pdf).

## Patent-supported architecture

The patent describes a roller drum with circumferential textured bands/projections aligned to curved-wall slots, smoother intervening surfaces that act as sealing lands, end walls and spindle pins. The housing retains the roller at its ends. Embodiments also describe upper/lower housing engagement with resilient sealing and snap-fit features.

The patent figures are schematic. They do not provide overall housing dimensions, shell thicknesses, complete roller dimensions, tolerances, material grades or flexural design sufficient for manufacture. The patent description does provide useful approximate comb-tooth proportions: around 5 mm width, approximately twice that length, widely spaced teeth, and an elliptical cross-section.

## Components now represented in Sand3D

The reconstruction script follows Sand3D's current component-first guidance: one named function per distinct part, dimensions sourced from the provenance ledger, parts placed in a parent frame, and assembly articulation represented explicitly. The roller is now a separate assembly with a continuous X-axis rotation joint. The roller is modelled as a smooth 24 mm drum with seven circumferential bands of discrete spheroidal dome projections, rather than generic knurling. The bands retain smooth sealing lands between them and align with the seven wall slots. The eight teeth use elliptical cross-sections, a tapered distal profile and a softened tip, rooted on the wall's outer surface and pointing away from the roller. The active builder now uses Sand3D `station`, `loft` and `fillet` operations to preserve an elliptical section while narrowing the blade in both width and thickness. The 0.30 width ratio, root/tip section thicknesses and tip fillet remain explicit engineering assumptions. The curved-wall thickness is provisionally 1.3 mm so the 2 mm projections reach approximately flush with the wall's outer envelope through the slots. The clamshell housing uses the waisted planform illustrated in patent Figure 2B, with a 54 mm waist depth marked as image-estimated. A separate perimeter gasket proxy and rounded/waisted housing-shell proxies have also been added. See the [Sand3D demos, API and Hugging Face dataset strategy](sand3d-dataset-strategy.md).

1. Smooth 24 mm roller drum and intervening sealing lands.
2. Seven circumferential projection bands, each with 18 spheroidal dome proxies, aligned with the seven modelled wall slots.
3. A 180-degree concave roller seat and seven through-slots.
4. Eight elliptical, tapered blade teeth. The patent describes approximately 5 mm width and a length approximately twice the width (about 10 mm); the numeric taper ratio and section thickness remain assumptions. The tooth roots now sit on the wall's outer surface and the tapered tips extend radially away from the roller.
5. Two roller end walls and two coaxial spindle pins.
6. Two bored housing bearing-support blocks, two upper-housing spindle-retaining arms with cut-outs, and two simplified snap-fit tabs.
7. A waisted upper/lower clamshell housing, perimeter gasket and reservoir envelope proxy.

The model preserves component names and separate solids in assembly groups where supported. The eight-tooth embodiment and approximate tooth width/length are patent-described; the 18 projections per band, seven-band mapping, waist depth and most other dimensions remain derived or assumed values as classified in the parameter ledger.


## Visual-reference refinement (2026-11-26)

A further multi-view source has been registered as [SRC-014](../../experiments/001-nyfasi-reconstruction/evidence/source-register.json): the Nyfasi exhibitor page in the Glee Birmingham 2023 *New To Glee* look book (printed page 125). The page describes closed, open, front, side and comb views. It supports qualitative visual decisions that the earlier patent-only proxy did not capture clearly: a compact rounded clamshell, dark-purple outer casing, pale peach/pink comb section, a visibly curved ergonomic profile, and a central dispensing region. It is not dimensioned or calibrated.

The latest Sand3D pass therefore:
- rounds both top and bottom perimeter rims of the upper and lower clamshell blanks before hollowing, using a 2.5 mm image-led edge-radius parameter (clipped at build time to fit the shell height and wall thickness);
- keeps the moulded shell perimeter geometry rounded;
- corrects the active comb blade from a flat polygonal prism to an elliptical section, tapered toward its distal end and softly filleted;
- corrects tooth length from the earlier unsupported 28 mm image estimate to approximately 10 mm, following the patent's statement that a tooth is about twice its approximately 5 mm width;
- records the 0.30 far-end width ratio, 1.5 mm root section thickness and 0.9 mm tip section thickness as assumptions rather than patent facts;
- adds validation for the patent-derived tooth proportion, minimum clear spacing and shell edge-radius envelope.

The look-book imagery is used for qualitative shape and colour blocking only. It does not justify changing the assumed 130 × 68 mm housing envelope into a claimed exact measurement. The public source does not expose a calibrated ruler, dimensioned orthographic drawing or physical sample. Exact retail dimensions remain unresolved until authorised CAD or physical metrology is available.

## Spindle-seal research proxies

Two separately named annular elastomer seal proxies are included around the spindle pins, conceptually within the bearing supports. Their 4.4 mm OD, 3.8 mm bore and 1 mm axial width are engineering assumptions, not recovered product dimensions. The width is constrained by both the 5 mm spindle projection and 8 mm bearing support. This geometry does not establish a functioning seal or an O-ring gland. See the [roller seal and tolerance study](roller-seal-and-tolerance.md) for the calculated worst-case interfaces and limitations.

## Parameter ledger

| Parameter | Current value | Classification |
|---|---:|---|
| Smooth roller drum diameter | 24 mm | Patent-derived estimate |
| Textured projection bands | 7 | Engineering interpretation |
| Projections per band | 18 | Engineering assumption derived from circumference and spacing |
| Projection base diameter / height | 2 mm / 2 mm | Patent-described example |
| Projection overlap into drum | 0.15 mm | Rendering/geometry assumption |
| Curved slotted-wall thickness | 1.3 mm | Engineering assumption to align projection tips with the outer envelope |
| Band axial footprint | 2 mm | Engineering assumption |
| Housing waist depth | 54 mm | Image-estimated from Figure 2B; low confidence |
| Tooth tip width ratio | 0.30 far-end/root width ratio | Engineering assumption; not dimensioned by patent |
| Tooth tip section thickness | 0.9 mm | Engineering assumption; not dimensioned by patent |
| Housing vertical edge fillet | 2.5 mm | Low-confidence image-led assumption from SRC-014; clipped to fit shell height and wall thickness |
| Tooth-root datum | -20.8 mm | Derived from the wall outer radius; teeth point away from the roller |
| End-wall diameter | 25 mm | Engineering assumption |
| End-wall thickness | 1.5 mm | Engineering assumption |
| Spindle-pin diameter | 4 mm | Engineering assumption |
| Spindle-pin projection | 5 mm | Engineering assumption |
| Bearing block | 8 × 12 × 18 mm | Engineering assumption |
| Upper retaining-arm section | 6 × 8 mm | Engineering assumption; height derived from upper-shell roof to spindle axis |
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

- Calibrate projection count, pitch, cap shape and band alignment against an authorised sample or dimensioned drawing.
- Refine the elastomeric seal geometry and define a measurable compression interface.
- Refine bearing supports and spindle retention using an authorised physical sample or supplier drawing.
- Model snap-fit hooks, lead-ins, undercuts and flexural beams only after dimensions and material data are evidenced.
- Add contact/clearance inspection and a controlled tolerance stack.
- Compare the model against calibrated photographs or a physical sample.

## Rights boundary

This is a research proxy based on public patent disclosure. It is not Nyfasi's original CAD, a verified retail revision, a manufacturing package, a freedom-to-operate opinion or permission to commercialise a replica.
