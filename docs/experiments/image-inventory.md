# Image and patent-figure inventory

The [image inventory CSV](https://github.com/andiekobbietks/product-engineering-lab/blob/main/experiments/001-nyfasi-reconstruction/evidence/image-inventory.csv) is a rights-aware catalogue scaffold. It records where imagery is expected to be found without copying third-party assets into the repository.

## Classification vocabulary

For each image or patent figure, record one or more of:

- **Product evidence:** front, rear, side, top, bottom, three-quarter, in-use or packaging view.
- **Design process:** sketch, concept, prototype, material/finish board or design development.
- **Patent disclosure:** figure number, view direction, embodiment and claim relevance.
- **Mechanical evidence:** visible interface, joint, fastener, opening, seam or service feature.
- **Scale evidence:** ruler, known object, dimension annotation or calibrated orthographic view.
- **Marketing-only:** stylised render or lifestyle image with unknown scale/perspective.

## Rights and provenance

Do not download, embed or commit source imagery unless a suitable permission or licence is recorded. Record canonical source URL, figure/page locator, access date, creator/rights holder, permitted display/adaptation/distribution, attribution, and a content hash for authorised local copies.

The current CSV rows are **inventory leads**, not completed visual classifications. A separate [GB2591502A figure-level register](https://github.com/andiekobbietks/product-engineering-lab/blob/main/experiments/001-nyfasi-reconstruction/evidence/patent-figure-register.csv) now maps Figures 1, 2A–2C and 3–6 from the patent's drawing description. Those classifications are based on the textual drawing descriptions; each drawing still needs direct visual inspection before geometry is inferred. Exact figure locators, image observations and rights clearances remain outstanding.
