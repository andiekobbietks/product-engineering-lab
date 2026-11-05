# CAD parameter provenance and reconstruction boundary

**Status:** research-only parameter ledger. Values are not verified retail dimensions or manufacturing specifications.

## Single source of truth

The Sand3D script loads numeric parameters from [cad-parameters.json](https://github.com/andiekobbietks/product-engineering-lab/blob/main/experiments/001-nyfasi-reconstruction/models/cad-parameters.json). Do not independently edit a second hard-coded parameter dictionary. Each parameter stores value, unit, provenance, evidence IDs, confidence and an explanatory note.

Run both checks from the experiment directory:

```bash
python scripts/validate_provenance.py
python scripts/validate_geometry.py
```

The provenance check validates source-ID integrity and required labels. The geometry check validates internal relationships such as radii ordering, wall span, tooth-row envelope and slot placement. Neither check validates patent interpretation, geometry against a physical sample or engineering performance.

## Provenance classes

| Class | Meaning | Example |
|---|---|---|
| `PATENT_DISCLOSED` | Explicitly disclosed in patent text or an illustrated embodiment; not automatically a retail measurement | Eight teeth; Figure 6B semi-cylindrical wall |
| `PATENT_DERIVED_ESTIMATE` | Selected or calculated within a patent-disclosed range; exact value is not disclosed | A 24 mm roller diameter selected within a disclosed 10–30 mm radius range |
| `MEASURED` | Measured from an authorised physical sample with method and uncertainty recorded | None yet |
| `IMAGE_ESTIMATED` | Estimated from imagery with scale and calibration recorded | None yet |
| `ENGINEERING_ASSUMPTION` | Schematic value chosen to make a proxy model | Housing envelope, shell thickness, seat clearance, slot width and axial length |
| `SUPPLIER_CONFIRMED` | Supported by authorised tooling or manufacturing documentation | None yet |

## Current model parameter interpretation

- **Eight teeth:** the patent describes an eight-tooth illustrated embodiment. This is not a confirmed count for every retail revision.
- **Tooth width around 5 mm:** an approximate patent-description value, not a metrology result.
- **Tooth length around 10 mm:** derived from the patent's statement that tooth length is approximately twice its width; not a measured retail dimension.
- **Tooth pitch 15 mm:** an engineering assumption formed from a 5 mm tooth width plus a 10 mm interpreted clear gap. The patent's spacing convention remains ambiguous.
- **Roller diameter 24 mm:** a selected proxy value. It corresponds to a 12 mm radius, inside the patent description's example radius range of approximately 10–30 mm.
- **Wall segment angle 180 degrees:** the semi-cylindrical example shown in patent Figure 6B. The disclosure also allows other angles greater than 90 degrees; this model iteration selects 180 degrees.
- **Wall thickness 2 mm and seat clearance 0.5 mm:** engineering assumptions only. The patent does not provide a fit/tolerance stack.
- **Seven slots:** one per clear gap between eight teeth. This is an explicit modelling interpretation, not a disclosed dimensioned count.
- **Slot width 2 mm:** placeholder; no authoritative dimension located.
- **Wall/roller length 112 mm:** selected to span the current 110 mm tooth-row envelope; not disclosed.
- **Housing and reservoir dimensions:** schematic placeholders.
- **Exploded gap:** presentation-only spacing; never product geometry.

## Geometry iteration

The first Sand3D proxy used a flat slotted carrier. The current iteration replaces it with a 180-degree annular cylinder segment, with an inner concave seat around the roller and circumferential slot cuts positioned between teeth. See [curved-wall geometry reconstruction](curved-wall-geometry.md) for the figure reading, coordinate system, assumptions and simplifications.

## Evidence and rights

The Chinese patent publication is a family member of the same international application as the UK filing. It adds a China publication/grant record, not a native CAD package. The official CNIPA register must be checked for current legal events and the applicant/assignment chain. Patent drawings are not a production drawing package, and this model is not a freedom-to-operate opinion.

The China tooling account remains secondary-media reporting. No supplier-confirmed geometry, material, tolerance, mould ownership or manufacturing process has been added to the CAD model.
