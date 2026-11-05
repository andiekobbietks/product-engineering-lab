# Product Engineering Lab

### From product evidence to engineering intelligence.

Research · Reconstruction · Validation · Productisation

![Status](https://img.shields.io/badge/status-research%20prototype-orange) ![Docs](https://img.shields.io/badge/docs-MkDocs%20Material-526CFE) ![Licence](https://img.shields.io/badge/licence-undecided-lightgrey)

<p align="center"><img src="assets/diagrams/product-engineering-loop.svg" alt="Product engineering loop" width="900"></p>

Product Engineering Lab investigates how fragmented product evidence can become structured, editable, traceable and testable engineering knowledge.

This is not simply a text-to-3D showcase. It explores the engineering layer around generative 3D: evidence provenance, component semantics, constraints, uncertainty, validation and governed decisions.

## Why Sand3D?

[Sand3D](https://github.com/Sandflow-ai/sand3d) is a key reference for exploring editable 3D generation. Sandflow describes its research direction as generating assets with separate parts, real dimensions and geometry that can continue through tools such as Blender.

Our research question is: **how do we move from a generated 3D object to an evidence-aware product model that can be inspected, tested, revised and responsibly handed into an engineering workflow?**

Sand3D remains an independently maintained third-party project. We will respect its own licence, notices and API boundaries, integrating through documented adapters rather than assuming ownership of its internals.

## Experiment 001: Nyfasi Deluxe Detangler

This case study investigates what can responsibly be reconstructed from public product pages, design case studies and patent publications. It separates documented claims from patent embodiments, visual observations from inferred components, assumptions from measured dimensions, and illustrative geometry from manufacturing-ready CAD.

See [Experiment 001](experiments/001-nyfasi-reconstruction/README.md), the [Colab notebook](experiments/001-nyfasi-reconstruction/notebooks/nyfasi_reconstruction_colab.ipynb), the [Sand3D reconstruction script](experiments/001-nyfasi-reconstruction/scripts/build_reconstruction.py), and the [interactive GLB viewer instructions](docs/experiments/viewer.md).

No original Nyfasi SolidWorks, Fusion 360, STEP or IGES files are claimed to have been located. Patent drawings are not native CAD.

## Engineering loop

1. Discover evidence, requirements and constraints.
2. Structure product, component and provenance records.
3. Reconstruct geometry with explicit assumptions.
4. Validate against independent evidence and measurable constraints.
5. Record decisions, unknowns, failures and approvals.
6. Carry reusable capabilities into production workflows.

## Platform direction

- **Product Engineering Lab:** experiments, benchmarks and reference implementations.
- **OKF:** portable, durable product knowledge.
- **AgentSON:** typed execution events, provenance and decision history.
- **AK Build:** reconciliation, validation, governance and productionisation.

The lab remains independently useful and provider-neutral.

## Status and rights

**Project-wide licence: undecided.** The previous MIT licence file was removed pending the IP review. See [LICENSING.md](LICENSING.md) and the [IP register](docs/ip-register.md).

Early research foundation. The reconstruction script and notebook have been committed but have not yet been executed in a compatible Sand3D runtime. A successful render is not engineering validation.

This independent research is not affiliated with or endorsed by Nyfasi, Dr Youmna Mouhamad, PDR or Sandflow AI. Third-party images and text remain with their rights holders. Link to sources and record attribution; do not redistribute without permission. Do not use illustrative geometry for manufacture or commercial replication without qualified engineering review and legal clearance.

See [methodology](docs/methodology.md), [architecture](docs/architecture.md) and [contributing](CONTRIBUTING.md).
