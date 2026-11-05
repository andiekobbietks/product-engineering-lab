# Get started

This guide runs the public research workflow locally. It does not require AK Build or any private AK Build implementation.

## 1. Clone the repository

~~~bash
git clone https://github.com/andiekobbietks/product-engineering-lab.git
cd product-engineering-lab
~~~

## 2. Create an isolated Python environment

~~~bash
python -m venv .venv
~~~

Activate it:

~~~powershell
# Windows PowerShell
.\.venv\Scripts\Activate.ps1
~~~

~~~bash
# macOS / Linux
source .venv/bin/activate
~~~

## 3. Validate the research inputs

Run the dependency-light checks first:

~~~bash
python experiments/001-nyfasi-reconstruction/scripts/validate_provenance.py
python experiments/001-nyfasi-reconstruction/scripts/validate_geometry.py
python -m unittest discover -s tests -v
~~~

These checks validate the internal structure of the evidence ledger and the declared geometry constraints. They do not validate a physical product.

## 4. Build the Sand3D research assembly

Install the pinned CAD dependencies and run the build:

~~~bash
python -m pip install -r requirements-cad.txt
python experiments/001-nyfasi-reconstruction/scripts/build_reconstruction.py
~~~

Generated GLB and OBJ files are written to the experiment output directory. The [CAD workflow](https://github.com/andiekobbietks/product-engineering-lab/actions/workflows/cad-smoke.yml) runs the same core checks in GitHub Actions and stores downloadable build artifacts.

## 5. Inspect the assembly

Open the [interactive assembly explorer](experiments/assembly-explorer.md). It includes a procedural preview and a local GLB file loader. You can download the latest workflow artifact, extract the GLB and load it into the browser without uploading it.

Alternatively, run the [Google Colab notebook](https://colab.research.google.com/github/andiekobbietks/product-engineering-lab/blob/main/experiments/001-nyfasi-reconstruction/notebooks/nyfasi_reconstruction_colab.ipynb).

## 6. Understand the evidence

Before changing dimensions, read:

- [CAD parameter provenance](experiments/cad-parameter-provenance.md)
- [Curved-wall geometry](experiments/curved-wall-geometry.md)
- [Patent reading notes](experiments/patent-reading-notes.md)
- [Validation protocol](experiments/nyfasi-validation.md)

Do not silently promote an assumption to a measured value. A measured value needs an identified sample, method, units, uncertainty and evidence reference.

## Reproducibility

Record the Git commit, Python version, Sand3D version, parameter-ledger hash and output hashes with each meaningful build. Keep generated outputs distinct from source evidence. Use the GitHub Actions workflow as the repeatable baseline.

## Public research boundary

This repository contains public research material and reference implementations. It is not the location for confidential customer information, private supplier documents, unreleased AK Build code or third-party CAD without redistribution permission.
