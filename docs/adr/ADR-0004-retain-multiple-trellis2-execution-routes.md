# ADR-0004: Retain multiple TRELLIS.2 execution routes

- **Status:** Accepted
- **Date:** 2026-11-26
- **Decision owners:** Product Engineering Lab
- **Context:** Nyfasi product reconstruction experiment

## Context

The Nyfasi reconstruction lab needs image-to-3D visual hypotheses to compare with a separately maintained, dimensionally constrained Sand3D assembly. The team has access to Microsoft's TRELLIS.2 through an official Hugging Face Space, and has also prepared a Google Colab notebook and a self-managed CUDA inference script.

Removing the Colab notebook when prioritising the hosted Space would discard useful reproducibility work and falsely imply that the execution routes are mutually exclusive. Each route has different operational properties: a hosted demo reduces setup effort, Colab makes setup and GPU preflight visible, and local CUDA supports developer-controlled execution.

## Decision

Retain all three TRELLIS.2 execution routes in the lab:

1. **Hugging Face Space — primary hosted route.** Use the official Microsoft Space for quick interactive experiments where its availability, queue and usage limits are acceptable.
2. **Google Colab — alternative reproducible route.** Keep the notebook as a documented, runnable path for explicit environment setup, GPU checks, image selection, inference and artifact export. GPU availability and session limits are controlled by Colab.
3. **Local CUDA — developer route.** Keep the repository inference script for Linux/NVIDIA environments meeting the model's hardware and software requirements.

Sand3D remains the canonical parametric engineering model. TRELLIS.2 outputs are visual hypotheses only. They must not overwrite measured dimensions, CAD parameters, mechanical constraints or the source-of-truth model.

## Rationale

- Preserves the work already invested in the Colab notebook.
- Avoids dependence on one hosted provider, its queue, quotas or interface.
- Supports reproducibility and comparison of execution environments.
- Keeps the lab's experiments and negative results auditable.
- Separates generative visual plausibility from dimensional engineering evidence.

## Consequences

### Positive

- Researchers can choose the route available to them without losing the experiment.
- The same source-image IDs and provenance manifest can be used across routes.
- Outputs can be compared by silhouette, surface appearance and topology.
- Future automation can add routes without changing the CAD authority model.

### Trade-offs and limitations

- Different environments may produce different outputs due to model revisions, settings, preprocessing and runtime dependencies.
- Hosted Space and Colab availability, queues, quotas and retention policies are outside this repository's control.
- A single image cannot establish true scale, hidden geometry or mechanical fit.
- Source-image download and generated-artifact handling must respect third-party rights and retention requirements.

## Required experiment record

For every generated candidate, record:

- Source image ID and source URL
- Execution route (Hugging Face Space, Colab or local CUDA)
- Model identifier and revision, where available
- Generation settings and preprocessing notes
- Output filename, format and SHA-256
- Known limitations, failures and manual edits
- Whether the result was compared with calibrated photographs and Sand3D

## References

- Microsoft TRELLIS.2: https://github.com/microsoft/TRELLIS.2
- Official Hugging Face Space: https://huggingface.co/spaces/microsoft/TRELLIS.2
- Hugging Face ZeroGPU documentation: https://huggingface.co/docs/hub/main/spaces-zerogpu
- Google Colab: https://colab.research.google.com/
- Nyfasi image-to-3D experiment: ../experiments/nyfasi-image-to-3d.md
