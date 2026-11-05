The latest successful output is recorded in the [build record](https://github.com/andiekobbietks/product-engineering-lab/blob/main/experiments/001-nyfasi-reconstruction/builds/2026-11-05.md), including output hashes and validation limitations.

# Interactive 3D assembly viewer

1. Open the [Sand3D smoke-test workflow](https://github.com/andiekobbietks/product-engineering-lab/actions/workflows/cad-smoke.yml) and download the latest successful artifact named `nyfasi-curved-wall-research-proxy`, or run the [Colab notebook](https://github.com/andiekobbietks/product-engineering-lab/blob/main/experiments/001-nyfasi-reconstruction/notebooks/nyfasi_reconstruction_colab.ipynb).
2. Extract the artifact ZIP and locate `hair_applicator_complete_roller_exploded.glb`.
3. Clone or download this repository, then open `docs/experiments/glb-viewer.html` in a modern browser and select the file. The viewer loads its model-viewer component from a public CDN, so internet access is required.

The viewer uses Google's model-viewer component from its public CDN. It runs in a modern browser with internet access. It does not perform dimensional or mechanical validation.
