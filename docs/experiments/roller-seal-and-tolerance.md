# Roller seal, interaction and tolerance study

## Scope

This iteration adds a pair of schematic elastomeric spindle seals to the Sand3D assembly and introduces a first-pass interface analysis for the roller, curved seat, wall slots, spindle bearings and seal bores.

The seal geometry is deliberately simple: annular elastomer proxies around the spindle region. It is **not** a validated liquid seal, lip seal, O-ring gland or recovered Nyfasi component. No material grade, compression, gland geometry, surface finish, swelling allowance or leak performance is known.

## Roller-to-slot interaction

The current model places seven circumferential band proxies at the same nominal axial pitch as the seven wall slots. The model's current nominal band width and slot width are both 2 mm. This gives **zero nominal width clearance** before manufacturing variation, deformation, runout, assembly error or rotation is considered.

The tolerance ledger assigns illustrative values of ±0.15 mm to slot width and ±0.10 mm to band width. A worst-case stack therefore ranges from -0.25 mm interference to +0.25 mm clearance. This is a design-review flag, not an acceptable production result. It means the current geometry is useful for visualising the concept but is not yet a proven free-running mechanism.

## Preliminary interface stack-up

| Interface | Nominal clearance | Illustrative worst-case range | Interpretation |
|---|---:|---:|---|
| Roller to curved seat (radial) | 0.50 mm | 0.30 to 0.70 mm | Positive in this assumed stack |
| Band to slot (width) | 0.00 mm | -0.25 to +0.25 mm | Potential interference; redesign/measure |
| Spindle to bearing (diametral) | 0.50 mm | 0.40 to 0.60 mm | Positive geometric clearance |
| Spindle to seal bore (diametral) | 0.20 mm | 0.05 to 0.35 mm | Geometry only; no sealing inference |

The calculations are intentionally conservative arithmetic stacks, not statistical RSS analysis. They do not account for thermal expansion, material compliance, eccentricity, mould shrinkage, surface finish, shaft runout or wear.

## Reproduce

```bash
python experiments/001-nyfasi-reconstruction/scripts/analyse_interaction.py
python experiments/001-nyfasi-reconstruction/scripts/validate_geometry.py
python experiments/001-nyfasi-reconstruction/scripts/build_reconstruction.py
```

The generated GLB/OBJ now include separately named seal proxies. The interaction report is a separate analysis artefact so geometric assumptions remain visible rather than hidden in the CAD script.

## Engineering next steps

1. Obtain a physical sample or authorised drawings and establish datums.
2. Measure roller OD/runout, slot width, band profile, axial pitch and shaft diameter with uncertainty.
3. Redesign band/slot clearance from the measured tolerance stack, then check the full rotational envelope.
4. Specify elastomer chemistry, hardness, compression, gland dimensions and fluid compatibility.
5. Validate with spin torque, leakage, wear, temperature and contamination tests.

## Rights and evidence boundary

This is independent patent-led research geometry. It is not Nyfasi manufacturing CAD, a verified digital twin, a production drawing, a freedom-to-operate opinion or permission to reproduce protected subject matter. All new seal and tolerance values are engineering assumptions.
