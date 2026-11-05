# Experiment 001 · Nyfasi Deluxe Detangler

## Research question

What product architecture can be reconstructed from public product pages, design case studies and patent records while preserving the difference between documented facts, visual observations and engineering assumptions?

## Sources to inspect

- [Nyfasi official website](https://nyfasi.com/)
- [PDR Deluxe Detangler case study](https://www.pdr-consultancy.com/work/deluxe-detangler)
- [iF Design entry](https://ifdesign.com/en/winner-ranking/project/deluxe-detangler/345596)
- [UK patent GB2591502A](https://patents.google.com/patent/GB2591502A/en)
- [US design patent USD1031151S1](https://patents.google.com/patent/USD1031151S1/en)

Patent embodiments must not automatically be treated as the exact retail configuration. Verify patent status and ownership in official registers.

## China IP and manufacturing evidence

The China patent-family record and secondary reports of mould manufacture/initial production are documented in the [China diligence dossier](../../docs/experiments/nyfasi-china-due-diligence.md) and machine-readable [China evidence register](evidence/china-diligence-register.json). The 8 and 15 October 2025 reports differ in how they describe grant support; the funding relationship remains unresolved.

## Sand3D research connection

Sand3D is used as a text-driven editable 3D generation experiment. This study asks what additional structure makes generated output useful in product engineering: component identity, evidence-linked dimensions, assembly relationships, editability, constraint checks and provenance.

The current iteration replaces the earlier flat slotted carrier with a 180-degree cylindrical wall segment, concave roller seat and seven circumferential arc-slot cuts positioned between the eight illustrated teeth. The geometric interpretation and its limits are documented in [curved-wall geometry](../../docs/experiments/curved-wall-geometry.md). It remains a patent-led proxy, not original Nyfasi CAD or a verified retail reconstruction.

Compare text-only generation, evidence-conditioned generation, component-by-component generation, assembly reconstruction and independent validation. The repository pins Sand3D 1.6.2 for the initial adapter experiment.

## Repository artefacts

- Product data model and JSON Schema: `models/product-model.json` and `models/product-model.schema.json`.
- Single-source CAD parameter ledger with provenance: `models/cad-parameters.json`.
- Provenance validator (no Sand3D dependency): `scripts/validate_provenance.py`.
- Curved-wall geometry validator (no Sand3D dependency): `scripts/validate_geometry.py`.
- Parameter provenance documentation: [CAD provenance and reconstruction boundary](../../docs/experiments/cad-parameter-provenance.md).
- Curved wall, roller seat and slot interpretation: [geometry reconstruction note](../../docs/experiments/curved-wall-geometry.md).
- Rights-aware image inventory: `evidence/image-inventory.csv`.
- Patent figure locators: `evidence/patent-figure-register.csv`.
- Patent reading notes: [GB2591502A](../../docs/experiments/patent-reading-notes.md).
- Component-level Sand3D script: `scripts/build_reconstruction.py`.
- CadFlow B-rep builder: `scripts/build_cadflow_reconstruction.py`.
- CadFlow Colab reproduction: `notebooks/nyfasi_cadflow_reconstruction_colab.ipynb`.
- CadFlow B-rep and STEP export guide: [documentation](../../docs/experiments/cadflow-reconstruction.md).
- Sand3D dataset licence and reuse policy: `models/sand3d-dataset-policy.md`.
- Metadata-only Sand3D exemplar discovery: `scripts/catalog_sand3d_examples.py`.
- Curved-wall CI build record and artifact digest: [build record](builds/2026-11-05-curved-wall.md).
- Reproduction notebook: `notebooks/nyfasi_reconstruction_colab.ipynb`.
- Validation protocol: [documentation](../../docs/experiments/nyfasi-validation.md).

The current product model deliberately records the patent-to-Nyfasi mapping as unverified. The geometry proxy is named after the patent family because the disclosed architecture has not been proven to match a specific Nyfasi-branded retail revision.

## Reconstruction boundary

Illustrative research reconstruction only. Not official Nyfasi CAD, not a verified manufacturing model and not exact dimensions. No original SolidWorks, Fusion 360, STEP or IGES files are claimed to have been located.

Third-party imagery is not mirrored by default. Record attribution and rights; do not manufacture from illustrative geometry or make commercial replication decisions without qualified engineering and legal review.
