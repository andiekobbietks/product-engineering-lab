# ADR-0002: Sand3D-native, source-linked assembly gallery

- **Status:** Accepted
- **Date:** 2026-11-05
- **Decision owners:** Product Engineering Lab
- **Scope:** Nyfasi assembly inspection experience

## Context

Sandflow's official Sand3D articulated gallery demonstrates a useful inspection pattern: a 3D viewport, a selectable object/component, the program that builds it, source highlighting for selected geometry, and controls for articulated joints. The previous Nyfasi page did not achieve that experience. It used a custom Three.js scene, schematic fallback geometry, separately loaded component GLBs and generated presentation offsets from component bounds. The viewer could therefore look assembled without proving that it was reading the actual assembly hierarchy or joint definition.

The purpose of the Nyfasi gallery is to make the relationship between model, program and engineering evidence inspectable.

## Decision

Replace the previous viewer with a browser gallery that uses the complete Sand3D assembly GLB and the exact Python build program that generated it.

The gallery will provide:

- a 3D viewport with orbit, zoom and camera reset;
- a seven-group component tree and geometry picking;
- source-code display beside the model;
- component-to-function highlighting using source ranges generated from Python's AST during the build, including clicked subparts mapped to their generating functions;
- Python syntax highlighting in the source pane;
- a parameter context read from the same CAD parameter ledger;
- discovery and operation of the exported `s3d_joint` metadata for the roller's continuous rotation;
- component isolation and wireframe inspection;
- an optional exploded presentation whose offsets are explicitly display-only.

The viewer must not create fallback geometry or invent a joint when generated Sand3D artefacts are missing. It must display an actionable load error instead.

## Implementation boundary

The build publishes `nyfasi_complete_assembly.glb`, `manifest.json`, `build_reconstruction.py` and `cad-parameters.json` together. The manifest records component node names, evidence descriptions, source function ranges, engine version and expected joint. The viewer resolves component roots by their exported node names and reads the actual `s3d_joint` extras from the GLB.

The slider and playback transform the exported joint pivot node. They are not a physics simulation. The explode control is a visual aid and must never be interpreted as a real assembly sequence, clearance or motion path.

## Alternatives considered

- **Embed the official Sandflow gallery in an iframe:** rejected because it would show Sandflow's example objects, not the Nyfasi assembly.
- **Copy the full upstream gallery implementation:** rejected in favour of a smaller project-owned viewer that follows the interaction model while keeping the Nyfasi-specific component, evidence and parameter mappings explicit.
- **Continue using the custom mesh viewer:** rejected because it did not expose the source-to-geometry relationship or native articulation.
- **Load seven GLBs and reconstruct the assembly in the browser:** rejected because the complete assembly GLB already carries the hierarchy and joint metadata.

## Consequences

- The gallery depends on the Sand3D build workflow publishing all four linked artefacts.
- Source highlighting stays current because ranges are generated from the build program's AST rather than maintained manually.
- A changed component root name must be reflected by the generated manifest; the viewer fails clearly if the node cannot be found.
- Joint controls are enabled only when the corresponding GLB extra is present.
- The viewer is an inspection tool, not a CAD editor, solver, physics engine or manufacturing approval system.
- The viewer uses a third-party Three.js runtime for browser rendering; Sand3D remains the geometry and articulation authority.

## Verification

CI must build the assembly and its source artefacts, run integrity tests, and confirm the manifest's component count, node names and source ranges. Browser verification must confirm that the complete GLB loads, component selection highlights the correct source range, the roller joint node responds to the slider and playback, and no schematic fallback is rendered.
