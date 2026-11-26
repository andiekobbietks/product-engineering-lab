# Metric reconstruction workflow

## Why this is the next step

The current Sand3D model is procedurally valid, but several numeric inputs are not measurements. More geometry code cannot make an assumed 130 × 68 mm envelope, 24 mm roller or 112 mm roller length true. The next stage is to acquire metric observations and fit the model to them.

## Python toolchain

- OpenCV (opencv-python-headless): perspective correction of a planar view when a known-size rectangular scale target is visible in the same plane.
- PyCOLMAP / COLMAP: Structure-from-Motion camera-pose estimation and Multi-View Stereo from overlapping photographs. Use a photo set with texture, strong overlap and varied camera positions. COLMAP returns a reconstruction up to scale; anchor scale using a known measured distance.
- SciPy: robust weighted least-squares fitting of repeated dimensional observations. The implementation uses scipy.optimize.least_squares with soft-L1 loss.
- Trimesh / Open3D: mesh inspection, point-cloud processing, registration and comparison after reconstruction.
- Sand3D remains the canonical scripted assembly/export engine in this repository. CadQuery/OpenCascade is useful for a separate parametric B-rep/STEP validation path, not a substitute for missing evidence.

## Workflow

1. Obtain rights-cleared product photographs or a physical sample. Prefer top, side, front, rear, comb-end and opened/internal views. Keep the camera fixed or record focal length and camera metadata where possible.
2. For planar views, include a measured rectangular scale target coplanar with the product face. Record its four image corners in TL, TR, BR, BL order and its real dimensions.
3. Install requirements-reconstruction.txt, then use scripts/calibrate_planar_image.py to rectify that plane. A homography corrects perspective on one plane only; it does not correct curved surfaces or depth.
4. For overlapping multi-view capture, run COLMAP/PyCOLMAP SfM then MVS. Align reconstruction scale using a measured reference length. A single photo or images with no known dimension cannot establish absolute millimetres.
5. Annotate multiple independent dimensions in evidence/measurement-template.json. Each observation needs a source, view, calibration ID and standard uncertainty in millimetres.
6. Run python experiments/001-nyfasi-reconstruction/scripts/fit_dimensions.py observations.json --output dimension-fit-report.json.
7. Review residuals and confidence, then promote only supported values into models/cad-parameters.json with source IDs and provenance. The fitter deliberately never edits the canonical ledger automatically.
8. Rebuild Sand3D, inspect silhouettes and section profiles, compare mesh-to-reference in a consistent coordinate frame, then run the full CI suite.

## Mathematical model

For repeated observations x_i with standard uncertainties sigma_i, the initial inverse-variance estimate is the sum of x_i/sigma_i squared divided by the sum of 1/sigma_i squared.

The implementation refines this using robust soft-L1 least squares on normalized residuals (x - x_i)/sigma_i, reducing the influence of a bad annotation. The reported standard uncertainty is the inverse square root of total observation precision. This is a measurement-combination estimate, not a full camera/shape uncertainty model.

## Patent constraints that can be used

GB2591502A describes an example roller radius of approximately 10–30 mm, eight teeth in the illustrated embodiment, approximately 5 mm tooth width, adjacent spacing of at least 5 mm and approximately 10 mm, and teeth around twice their width in longitudinal length. These are patent embodiment constraints, not proof that a retail Nyfasi revision has those exact dimensions. The existing 24 mm roller diameter is inside the disclosed radius range but remains an unverified selected value. The retail-form 28 mm tooth length remains a separate low-confidence image estimate.

## What cannot be inferred from exterior images

Reservoir capacity, wall thickness, snap-fit beam dimensions, spindle/bearing fit, seal compression and hidden internal clearances require opened-product photography, a physical sample, sectioning, supplier drawings or authorised CAD. Do not let an optimiser invent these values to make the assembly close.

## Reproducibility and rights

Do not commit third-party product photos unless permission and redistribution rights are established. Keep original image files local when necessary; commit calibration metadata, measurement annotations, source identifiers and derived reports. This workflow is an evidence acquisition and fitting layer, not a claim of exact digital-twin status.
