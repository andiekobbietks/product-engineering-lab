# Sand3D dataset reference policy

**Purpose:** discover useful programmatic modelling patterns for the Nyfasi research reconstruction. Dataset objects are examples, not evidence of Nyfasi geometry.

## Official Sandflow collections

| Collection | Hugging Face dataset | Approximate rows / context | Use |
|---|---|---:|---|
| CAD | [Sandflow/sand3d-cad](https://huggingface.co/datasets/Sandflow/sand3d-cad) | About 24,495 train/validation rows; Zero-To-CAD and CADFS | Mechanical-part construction patterns |
| Objaverse | [Sandflow/sand3d-objaverse](https://huggingface.co/datasets/Sandflow/sand3d-objaverse) | 64.6k train rows shown in viewer | Broad product and object patterns |
| Articraft | [Sandflow/sand3d-articraft](https://huggingface.co/datasets/Sandflow/sand3d-articraft) | 9,209 source objects | Articulated-part and assembly patterns |
| SimReady | [Sandflow/sand3d-simready](https://huggingface.co/datasets/Sandflow/sand3d-simready) | 2,334 source assets | Materials, hierarchy and simulation metadata |
| AutoMate | [Sandflow/sand3d-automate](https://huggingface.co/datasets/Sandflow/sand3d-automate) | 3,169 source objects | Articulated mechanism examples |

Sandflow describes the overall library as approximately 100K objects written as Sand3D programs. Rows can include program, render, OpenUSD path, family, quality score, source, source licence, attribution, Sand3D version and content hashes.

## Licence handling

Dataset pages declare CC-BY-4.0 for the Sandflow dataset layer. That does **not** erase the upstream asset's licence. Each row separately carries license, source_license, attribution and license_status.

1. Do not bulk-copy third-party programs, USD, meshes, renders or textures into this public repository.
2. Use datasets to study modelling structure and identify candidate patterns.
3. Before adapting an individual program or redistributing an asset, inspect its row-level source_license and preserve complete attribution and modification notice.
4. Exclude records whose license_status is not ok.
5. Keep dataset ID, source, source licence, attribution, source revision and hashes with any future derivative.
6. Never use a dataset object as evidence of Nyfasi dimensions, design or construction.

Candidate families: shafts, rollers, cylindrical housings, bearing supports, snap-fits, seals, mechanical brackets and articulated assemblies. A human must review every candidate before reuse.

## Sources

- [Sand3D library and examples](https://sandflow.ai/sand3d/)
- [Sand3D Hugging Face collection](https://huggingface.co/collections/Sandflow/sand3d)
- [Sandflow CAD dataset card](https://huggingface.co/datasets/Sandflow/sand3d-cad)
- [Hugging Face 3D dataset documentation](https://huggingface.co/docs/hub/main/en/datasets-3d)
