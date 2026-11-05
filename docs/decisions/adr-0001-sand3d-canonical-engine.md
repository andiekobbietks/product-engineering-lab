# ADR-0001: Sand3D as the canonical Nyfasi modelling and assembly engine

- **Status:** Accepted
- **Date:** 2026-11-05
- **Decision owners:** Product Engineering Lab
- **Scope:** Experiment 001, Nyfasi reconstruction and its reproducible engineering pipeline

## Context

The experiment began with several modelling and presentation approaches. A custom Three.js viewer supplied a schematic preview. CadFlow was explored for deterministic OpenCascade B-rep construction and STEP output. Sand3D was then adopted for component-first procedural geometry, named assembly groups and articulated joints.

Maintaining multiple active modelling authorities creates avoidable divergence: component definitions can drift, coordinate frames and assembly relationships can be represented differently, and the viewer can become a separate interpretation of geometry rather than an inspection surface for the model that generated it. The previous viewer demonstrated this problem: it loaded component GLBs independently, derived display offsets from their bounding-box centres and did not inspect the complete articulated assembly's native joint hierarchy.

The engineering objective is not merely to produce a mesh. It is to keep one traceable chain from evidence and parameter assumptions through source code, named components, assembly relationships, exported artefacts, validation and inspection.

## Decision

Use **Sand3D as the single canonical modelling and assembly engine** for the active Nyfasi reconstruction.

The canonical path is:

1. Public evidence and the parameter ledger define what is disclosed, derived, measured or assumed.
2. `build_reconstruction.py` is the authoritative geometry and assembly program.
3. Sand3D creates named component groups and the assembly-level joint relationship.
4. Sand3D exports the complete articulated GLB and secondary formats from that same model.
5. The benchmark and integrity checks evaluate the generated artefacts and declared constraints.
6. The browser gallery inspects the generated assembly and its source map; it does not rebuild geometry independently.

The complete assembly GLB is authoritative for browser geometry and articulation. Individual component GLBs remain useful secondary exports, not independent assembly inputs.

CadFlow is removed from the active Nyfasi build and publication path. Existing CadFlow scripts, reports and historical results remain in the repository as archived research and comparison material; they are not deleted or represented as the current model.

## Why Sand3D

- **One source of truth:** geometry, hierarchy and joints originate in the same Python program.
- **Semantic assembly:** named groups and explicit joints carry more meaning than a collection of disconnected meshes.
- **Articulation in the export:** Sand3D writes joint information into GLB node extras and provides URDF and USDA exports for downstream mechanism and scene consumers.
- **Inspectable source:** a generated source map can link each assembly group to the actual Python functions that create it.
- **Reproducibility:** a pinned Sand3D dependency, parameter ledger, build script and benchmark can be exercised in CI.
- **Lower integration drift:** the viewer reads the model output instead of approximating the assembly through a second geometry implementation.

## Alternatives considered

### Keep the dual Sand3D + CadFlow active pipeline

Rejected for this experiment. It preserves access to two different modelling strengths, but duplicates build paths and invites confusion over which geometry, coordinate system and export should be treated as authoritative. The active scope values a single coherent engineering record over parallel CAD implementations.

### Keep the custom schematic / Three.js viewer

Rejected as the primary inspection experience. It can render meshes, but the previous implementation used a schematic fallback and independently loaded component GLBs. It did not provide the original Sand3D gallery's source-linked component inspection or operate the native exported joint.

### Use Sand3D only as a mesh generator

Rejected. This would discard the assembly and joint semantics that distinguish Sand3D from a simple mesh-export utility.

## Consequences and trade-offs

- Sand3D is the required dependency for the active Nyfasi build, benchmark and gallery.
- The canonical browser model is the complete assembly GLB; component GLBs are secondary deliverables.
- URDF and USDA are the supported articulated interchange outputs. GLB is the interactive web output.
- Sand3D does **not** provide the same OpenCascade B-rep topology workflow or STEP export that CadFlow provided. This decision does not claim otherwise. If STEP delivery, robust B-rep operations or manufacturing-grade topology validation becomes a requirement, the ADR must be revisited and a separately governed conversion or specialist CAD stage may be introduced.
- Sand3D's existence of a joint record does not establish correct physical motion, collision-free operation, bearing fit or material behaviour.
- All patent interpretation and parameter provenance labels remain visible. A coherent model is not automatically an accurate model.
- Historical CadFlow material remains clearly labelled as historical and must not silently re-enter the canonical build.

## Revisit when

Reconsider this decision if an authorised source CAD model becomes available; a customer or manufacturing deliverable requires STEP/B-rep; Sand3D cannot represent a required feature or constraint; the dependency becomes unmaintained or incompatible; or independent validation demonstrates a material loss of engineering fidelity.

## Verification

The decision is considered implemented only when CI builds the complete Sand3D assembly, publishes its source and parameter artefacts, confirms the expected joint metadata exists in the GLB, and the browser gallery loads that same GLB without a schematic fallback. Benchmark success is evidence for the tested scenarios only, not proof of general engineering capability.
