# Nyfasi reconstruction validation protocol

## Objective

Measure how closely an explicitly approximate, evidence-conditioned reconstruction corresponds to an authorised reference product. This is a protocol, not a claim that validation has already been completed.

## Evidence tiers

| Tier | Evidence | Permitted interpretation |
|---|---|---|
| A | Calibrated physical measurement, manufacturer CAD/specification with permission | Dimensional validation within stated measurement uncertainty |
| B | Orthographic or calibrated product photography with known scale | Projected silhouette and selected dimension estimates |
| C | Perspective product photography | Visual comparison only unless camera and scale are calibrated |
| D | Patent drawings or marketing renderings | Design-context reference; do not assume retail geometry or scale |
| E | Unverified secondary image or commentary | Lead for further research, not a model constraint |

## Procedure

1. Record source ID, date, rights basis, camera/view, scale and measurement uncertainty.
2. Select matching views and define image crop/registration method before comparing.
3. Separate silhouette, component placement, visible dimensions, material appearance and articulation.
4. Compare only like-for-like views; document camera perspective and occlusion.
5. Report pixel/contour measures only alongside registration method and image resolution.
6. For dimensions, report absolute and relative error against measured reference, including uncertainty.
7. Mark each component supported, partially supported, assumed or unknown.
8. Record reviewer, tool versions, parameters and excluded regions.

## Metrics

- Silhouette intersection-over-union (IoU) for registered orthographic views.
- Contour distance (e.g. symmetric Chamfer distance) in image pixels or calibrated units.
- Dimension absolute error and percentage error where reference measurements exist.
- Component presence/placement checklist.
- Provenance coverage: supported model parameters divided by all model parameters.

Do not use a single image similarity score as proof of mechanical correctness, internal geometry, materials, tolerances or manufacturability.

## Acceptance gate

A result is accepted only for the specific claim and evidence tier tested. A visual match cannot upgrade an assumed internal mechanism to verified fact.
