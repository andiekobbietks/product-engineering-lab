# Experiment 001 · Nyfasi Deluxe Detangler

## Research question

What product architecture can be reconstructed from public product pages, design case studies and patent records while preserving the difference between documented facts, visual observations and engineering assumptions?

## Sources to inspect

- [Nyfasi official website](https://nyfasi.com/)
- [PDR design case study](https://www.pdr-consultancy.com/work/deluxe-detangler)
- [iF Design entry](https://ifdesign.com/en/winner-ranking/project/deluxe-detangler/345596)
- [UK patent GB2591502A](https://patents.google.com/patent/GB2591502A/en)
- [US design patent USD1031151S1](https://patents.google.com/patent/USD1031151S1/en)

Patent embodiments must not automatically be treated as the exact retail configuration. Verify patent status and ownership in official registers.

## Sand3D research connection

Sand3D is relevant as a text-driven editable 3D generation research project. This experiment asks what additional structure makes generated output useful in product engineering: component identity, evidence-linked dimensions, assembly relationships, editability, constraint checks and provenance.

Compare text-only generation, evidence-conditioned generation, component-by-component generation, assembly reconstruction and independent validation. The repository pins Sand3D 1.6.2 for the initial adapter experiment. The script is authored against the documented API but has not yet been executed in a compatible runtime; API and geometry output remain unverified.

## Repository artefacts

- Product data model and JSON Schema: `models/product-model.json` and `models/product-model.schema.json`.
- Rights-aware image inventory: `evidence/image-inventory.csv`.
- Patent figure locators: `evidence/patent-figure-register.csv`.
- Patent reading notes: [GB2591502A](../../docs/experiments/patent-reading-notes.md).
- Component-level Sand3D script: `scripts/build_reconstruction.py`.
- Reproduction notebook: `notebooks/nyfasi_reconstruction_colab.ipynb`.
- Validation protocol: [documentation](../../docs/experiments/nyfasi-validation.md).

The current product model deliberately records the patent-to-Nyfasi mapping as unverified. The first geometry proxy is named after GB2591502A, because the disclosed architecture has not yet been proven to match the Nyfasi-branded retail SKU.

## Reconstruction boundary

Illustrative research reconstruction only. Not official Nyfasi CAD, not a verified manufacturing model and not exact dimensions. No original SolidWorks, Fusion 360, STEP or IGES files are claimed to have been located.

Third-party imagery is not mirrored by default. Record attribution and rights; do not manufacture from illustrative geometry or make commercial replication decisions without qualified engineering and legal review.