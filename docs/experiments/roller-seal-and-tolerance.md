# Roller seal, interaction and tolerance study

## Scope and evidence status

This iteration adds two separately named annular elastomer spindle-seal proxies to the component-first Sand3D assembly and introduces a preliminary interface analysis for the roller, curved seat, wall slots, spindle bearings and seal bores.

The seal placeholders use a 3.8 mm bore around a 4 mm spindle pin, a 4.4 mm outside diameter inside a nominal 4.5 mm bearing bore, and a 1 mm axial width. These are engineering assumptions, not Nyfasi dimensions. The width is checked against both the 5 mm spindle projection and the 8 mm bearing-support width. The model does not represent a validated lip seal, O-ring gland, material specification or compression design.

## Roller-to-slot interaction

Seven circumferential projection bands align nominally with seven wall slots. Each band is represented by 18 discrete spheroidal domes around the smooth drum; the nominal axial footprint is 2 mm, matching the current 2 mm slot width, so nominal width clearance is zero. The provisional 1.3 mm wall thickness places the 2 mm-high projection tips approximately flush with the wall's outer envelope after the 0.5 mm seat clearance and 0.15 mm mesh overlap are accounted for. This fit is an engineering assumption, not a patent dimension. The tolerance ledger assigns illustrative slot-width and band-width variations of ±0.15 mm and ±0.10 mm respectively. The calculated worst-case stack is therefore -0.25 to +0.25 mm: interference is possible. This is a design-review flag, not an acceptable production fit or evidence of free rotation.

## Calculated interface stack-up

The tolerance ledger stores only tolerance inputs. Shared physical-feature tolerances for the spindle-pin diameter and bearing-bore diameter are each defined once under `shared_tolerances`, then reused by every affected interface stack. The analysis script reads nominal dimensions from `cad-parameters.json`, calculates the nominal interface values, and derives worst-case limits at runtime. This avoids stale or contradictory results when a CAD parameter or shared tolerance changes. Regression tests verify shared-tolerance propagation and fixed worst-case bounds for both seal interfaces.

| Interface | Nominal | Calculated worst-case range | Interpretation |
|---|---:|---:|---|
| Roller to curved seat (radial clearance) | 0.50 mm | 0.30 to 0.70 mm | Positive in this assumed stack |
| Band to slot (width clearance) | 0.00 mm | -0.25 to +0.25 mm | Interference possible |
| Spindle to bearing (diametral clearance) | 0.50 mm | 0.40 to 0.60 mm | Positive geometric clearance |
| Spindle to seal bore (diametral interference) | 0.20 mm | 0.05 to 0.35 mm | Positive values mean interference; elastomer deformation not modelled |
| Seal OD to bearing bore (diametral clearance) | 0.10 mm | -0.05 to +0.25 mm | Possible interference or gap |

Axial band-to-slot centre alignment is calculated as ±0.25 mm from the two assumed position tolerances. These are arithmetic worst-case stacks, not statistical RSS analysis. They omit thermal expansion, elastomer constitutive behaviour, compression set, eccentricity, mould shrinkage, surface finish, shaft runout and wear.

## Reproduce from the repository root

Use a clean Python environment and install the repository's pinned CAD dependency before invoking the geometry builder:

```bash
python -m pip install --upgrade pip
python -m pip install -r requirements-cad.txt
python experiments/001-nyfasi-reconstruction/scripts/validate_geometry.py
python experiments/001-nyfasi-reconstruction/scripts/analyse_interaction.py
python -m unittest discover -s experiments/001-nyfasi-reconstruction/tests -v
python experiments/001-nyfasi-reconstruction/scripts/build_reconstruction.py
```

The build exports GLB, OBJ, URDF and USDA research representations. The interaction report is a separate reproducible calculation; it is not a contact simulation or a physical test.

## Engineering next steps

1. Obtain an authorised sample or drawings and establish datums.
2. Measure smooth drum OD/runout, projection diameter/height/count/pitch, slot width, axial band pitch and spindle diameter with measurement uncertainty.
3. Redesign band/slot clearance from measured data, then inspect the full rotational envelope.
4. Specify elastomer chemistry, hardness, compression, gland dimensions and fluid compatibility.
5. Validate with spin torque, leakage, wear, temperature and contamination tests.

## Rights and evidence boundary

This is independent patent-led research geometry. It is not Nyfasi manufacturing CAD, a verified digital twin, a production drawing, a freedom-to-operate opinion or permission to reproduce protected subject matter. All seal and tolerance values introduced in this study remain engineering assumptions.
