# Sand3D datasets and reconstruction strategy

**Purpose:** document how the Sandflow Sand3D program datasets inform this research without treating generic training examples as Nyfasi product evidence.

## How this fits with CadFlow

This project also uses [CadFlow](https://github.com/yhz5613813/CadFlow), an OpenCascade-backed Python B-rep SDK. CadFlow is the preferred route for exact solid topology, per-component validation and STEP/STL exchange. Sand3D and its Hugging Face program datasets are complementary: they provide readable procedural modelling patterns, assembly decomposition and articulation examples. The Hugging Face datasets are Sandflow/Sand3D datasets, not CadFlow datasets, and they do not contain verified Nyfasi CAD. See the [CadFlow B-rep reconstruction page](cadflow-brep.md).

## Toolchain verified

- [Sand3D repository](https://github.com/Sandflow-ai/sand3d)
- [Sand3D website and demonstrations](https://sandflow.ai/sand3d/)
- [Interactive gallery](https://sand3d.sandflow.ai/gallery.html)
- [API reference](https://sand3d.sandflow.ai/api.html)
- [Assembly-writing guidelines](https://sand3d.sandflow.ai/guidelines.html)
- [Hugging Face explorer](https://huggingface.co/spaces/Sandflow/sand3d-explorer)
- [Hugging Face collection](https://huggingface.co/collections/Sandflow/sand3d-6aec268fbdcd3bc174236168)

Sand3D is a Python modelling language over Blender's `bpy`. Its current published README documents Python 3.11 and 3.13, Blender Python API 4.5 and 5.2, named parts, profiles, solids, boolean edits, frames, joints, groups and assemblies. It exports GLB, URDF, USDA, OBJ and STL. The project is Apache-2.0. This repository pins Sand3D 1.6.2 for reproducibility; check upstream release notes before changing that pin.

## Five Sandflow datasets

The current Hugging Face dataset cards declare CC-BY-4.0 for the Sandflow dataset layer. Each row also carries source_license, attribution and license_status. The upstream asset licence remains relevant: do not assume the dataset-level label overrides it. For example, sand3d-cad includes Zero-To-CAD and CADFS sources, while Objaverse-derived rows preserve per-object source attribution. Review the exact row before reuse. See the [metadata and reuse policy](https://github.com/andiekobbietks/product-engineering-lab/blob/main/experiments/001-nyfasi-reconstruction/models/sand3d-dataset-policy.md).

| Dataset | Source family | Useful role in this project | What it does not establish |
|---|---|---|---|
| [sand3d-cad](https://huggingface.co/datasets/Sandflow/sand3d-cad) | Public CAD mechanical parts | Learn how mechanical features are expressed as editable, named Sand3D programs; compare holes, bores, fillets, shells and profiles | Dimensions or geometry of the Nyfasi product |
| [sand3d-automate](https://huggingface.co/datasets/Sandflow/sand3d-automate) | AutoMate mechanical assemblies | Study part separation, assembly hierarchy and constraints | The actual roller, housing or bearing arrangement |
| [sand3d-articraft](https://huggingface.co/datasets/Sandflow/sand3d-articraft) | Articulated objects | Learn joint declarations and articulation patterns | Verified roller bearing design or operating range |
| [sand3d-objaverse](https://huggingface.co/datasets/Sandflow/sand3d-objaverse) | Objaverse objects | Broad shape/program examples and visualisation references | Authoritative product evidence; Objaverse source assets can have varied individual licences |
| [sand3d-simready](https://huggingface.co/datasets/Sandflow/sand3d-simready) | NVIDIA SimReady assets | Material, scene and simulation packaging patterns; useful later for USD workflows | Product-specific materials, mechanical properties or tolerances |

## Dataset provenance register

The machine-readable [dataset register](https://github.com/andiekobbietks/product-engineering-lab/blob/main/experiments/001-nyfasi-reconstruction/evidence/sand3d-huggingface-dataset-register.json) records the five source IDs, intended use and reuse restrictions. No source mesh or model has been copied into the repository. The generated Sand3D programs may be labelled CC BY 4.0 by the upstream project, but Hugging Face notes that dataset-card licence metadata is a declaration and users should review the actual card and underlying source rights before use. See [Hugging Face dataset-card guidance](https://huggingface.co/docs/hub/en/datasets-cards) and [licence guidance](https://huggingface.co/docs/hub/main/repositories-licenses).

## How the datasets are used

1. **API learning:** use the Sand3D examples and dataset programs to learn idiomatic operations such as `revolve`, `loft`, `shell`, `knurl`, `hole`, `fillet`, `joint`, `group` and `assembly`.
2. **Component design:** structure each physical concept as a named function with a small parameter set. Place it once in its parent coordinate frame.
3. **Assembly design:** use explicit parent frames and joints, rather than a collection of unrelated world-space meshes.
4. **Validation:** compare geometry against the patent evidence register, parameter ledger and eventually calibrated retail photographs or an authorised physical sample.
5. **Rights:** do not copy a dataset asset into this repository just because it appears in a public dataset. Record the exact asset identifier, source, author, item-level licence, attribution and modifications before reuse.

No Sandflow dataset is treated as evidence that it contains Nyfasi CAD. The current reconstruction is generated from the patent-led parameter ledger and documented assumptions, not from a borrowed product model.

## Current reconstruction changes

The Sand3D build is being structured around separate named components:

- Rounded lower housing and upper cap proxies
- Reservoir volume proxy
- Semi-cylindrical slotted wall
- Eight tooth proxies
- Roller core and exposed smooth sealing lands
- Seven knurled annular bands
- Two roller end walls and two spindle pins
- Two bored bearing-support proxies
- Housing snap-fit tabs
- Perimeter gasket proxy
- Continuous roller-rotation joint

The knurled texture is a procedural visual feature, not a claim that the original roller uses the same knurl pitch or exact texture. The seven-band/seven-slot relationship is an interpretation. The housing, gasket, retention, bearing and most roller dimensions remain engineering assumptions.

## Reproducibility and outputs

The CAD smoke-test workflow pins the Python/Sand3D toolchain and validates the provenance ledger and geometric relationships before exporting:

- GLB for the browser viewer
- OBJ for broad CAD/DCC interchange
- URDF for articulated robotics/simulation workflows
- USDA for OpenUSD pipelines

The export formats do not make the model mechanically validated. URDF and USD are interchange outputs for further engineering work, not evidence that forces, clearances, material behaviour or performance have been simulated correctly.

## High-fidelity acceptance gates

A more detailed render is not, by itself, high fidelity. The next fidelity gates are:

1. Calibrated front/side/top/oblique photographs of an identified retail revision, with scale references and image uncertainty.
2. An authorised physical sample or original CAD/supplier drawings.
3. Measured datum scheme, component dimensions, wall thicknesses, radii, hole locations and tolerances.
4. Correct roller surface pattern, slot cross-sections, seal interfaces, bearing supports, snap-fit beams and fluid path.
5. Assembly fit checks, tolerance stack, motion/clearance checks and material confirmation.
6. Independent comparison report with deviations and confidence per feature.

Until those inputs exist, the model remains a traceable patent-led engineering research proxy, not original Nyfasi CAD, a verified digital twin or a manufacturing package.



## Selected mechanical pattern references

The first automated pass produced **400 metadata references** (80 per collection). From that index, the following records are the most directly relevant to the reconstruction's roller, shaft and bearing decomposition:

| Dataset example | Pattern relevance | Source licence |
|---|---|---|
| AutoMate: roller_conveyor | Repeated roller arrangement | CC0-1.0 |
| AutoMate: shaft_and_bearing_block | Shaft, bore and bearing support | CC0-1.0 |
| AutoMate: split_pillow_block | Split bearing housing and retention | CC0-1.0 |
| AutoMate: flanged_bearing | Bearing mounting geometry | CC0-1.0 |
| SimReady: consumable_bearing_ball_d01 | Bearing component reference | CC-BY-4.0 |
| Articraft: road_bike_crankset | Rotating multi-part assembly hierarchy | CC-BY-4.0 |
| Objaverse: finned_motor | Cylindrical housing and radial features | CC-BY-4.0 |

The complete IDs, asset IDs, SHA-256 program hashes and attribution strings are recorded in the [curated exemplar shortlist](https://github.com/andiekobbietks/product-engineering-lab/blob/main/experiments/001-nyfasi-reconstruction/models/sand3d-exemplar-shortlist.json). These are modelling-pattern references only. The Nyfasi model's dimensions still come from its evidence ledger, not these unrelated objects.

## Reproducible exemplar discovery

A metadata-only discovery script scans the five public collections for mechanical terms such as roller, bearing, shaft, housing, gear, seal and fastener. It retains source IDs, item-level licences, attribution and hashes; it does not copy program bodies, USD, meshes or textures into this repository.

- [Catalogue script](https://github.com/andiekobbietks/product-engineering-lab/blob/main/experiments/001-nyfasi-reconstruction/scripts/catalog_sand3d_examples.py)
- [Run the catalogue workflow](https://github.com/andiekobbietks/product-engineering-lab/actions/workflows/sand3d-catalog.yml)
- Download the generated sand3d-exemplar-catalog artifact from the workflow run.

A candidate is not automatically reused. Review its exact source licence and attribution first. The catalogue is a research index, not a source of Nyfasi product dimensions.
