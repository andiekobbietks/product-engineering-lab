# CAD parameter provenance and reconstruction boundary

**Status:** research-only parameter ledger. Values are not verified retail dimensions or manufacturing specifications.

## Single source of truth

The Sand3D script loads numeric parameters from [cad-parameters.json](../../experiments/001-nyfasi-reconstruction/models/cad-parameters.json). Do not independently edit a second hard-coded parameter dictionary. Each parameter stores value, unit, provenance, evidence IDs, confidence and an explanatory note.

Run the provenance check from the experiment directory:

```bash
python scripts/validate_provenance.py
```

This check does not require Sand3D. It checks source-ID integrity, required provenance labels and that the reconstruction script consumes the parameter ledger. It does not validate geometry, patent interpretation or engineering performance.

## Provenance classes

| Class | Meaning | Example |
|---|---|---|
| `PATENT_DISCLOSED` | Explicitly described in a patent embodiment; not automatically a retail measurement | Eight teeth in the illustrated embodiment |
| `PATENT_DERIVED_ESTIMATE` | Selected or calculated within a patent-disclosed range; exact value is not disclosed | A 24 mm roller diameter selected within a disclosed 10–30 mm radius range |
| `MEASURED` | Measured from an authorised physical sample with method and uncertainty recorded | None yet |
| `IMAGE_ESTIMATED` | Estimated from imagery with scale and calibration recorded | None yet |
| `ENGINEERING_ASSUMPTION` | Schematic value chosen to make a proxy model | Housing envelope and placeholder reservoir |
| `SUPPLIER_CONFIRMED` | Supported by authorised tooling/manufacturing documentation | None yet |

## Current model parameter interpretation

- **Eight teeth:** the patent describes an eight-tooth illustrated embodiment. This is not a confirmed count for every retail revision.
- **Tooth width around 5 mm:** an approximate patent-description value, not a metrology result.
- **Tooth pitch 15 mm:** an engineering assumption formed from a 5 mm tooth width plus a 10 mm interpreted gap. The patent's spacing convention must be checked before treating this as a dimensional constraint.
- **Roller diameter 24 mm:** a selected proxy value. It corresponds to a 12 mm radius, inside the patent description's example radius range of approximately 10–30 mm. It is not an exact disclosed or measured diameter.
- **Housing, reservoir, wall and slot dimensions:** schematic placeholders until measured from an authorised sample or supplied in an authoritative drawing.
- **Exploded gap:** presentation-only spacing; never product geometry.

## Geometry limitation

The current Sand3D script still uses a flat wall with rectangular cut-outs as a visible proxy. The patent describes a curved wall and arcuate slots. Do not present the proxy as a geometrically faithful patent reconstruction. A next geometry iteration should model the curved wall/roller seat and arc-slot interface only after the relevant patent figure geometry has been transcribed and checked against the written description.

## Evidence and rights

The Chinese patent publication is a family member of the same international application as the UK filing. It adds a China publication/grant record, not a native CAD package. The official CNIPA register must be checked for current legal events and the applicant/assignment chain. Patent drawings are not a production drawing package, and this model is not a freedom-to-operate opinion.

The China tooling account remains secondary-media reporting. No supplier-confirmed geometry, material, tolerance, mould ownership or manufacturing process has been added to the CAD model.
