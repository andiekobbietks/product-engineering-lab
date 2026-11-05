# Architecture

Product Engineering Lab and AK Build are related layers, not one product.

~~~mermaid
flowchart TD
 I[Product / software idea] --> B[AK Build: build, deploy and operate micro-SaaS]
 B --> S[Application runtime and customer workflows]
 E[Evidence: images, patents, CAD, requirements, data] --> L[Product Engineering Lab]
 L --> P[Evidence-linked product model]
 L --> G[Geometry, component and validation experiments]
 P --> O[OKF: portable knowledge]
 G --> A[AgentSON: execution and provenance events]
 O --> B
 A --> B
 B --> R[Reconcile · validate · govern · approve]
 R --> S
~~~

| Layer | Responsibility | Product relationship |
|---|---|---|
| AK Build | Build, deploy, secure, integrate and operate micro-SaaS and AI-enabled applications | Commercial productisation and delivery environment |
| Product Engineering Lab | Research, experiments, benchmarks and reference implementations | Develops reusable engineering capabilities; not the AK Build application builder |
| OKF | Durable, portable knowledge and relationships | Knowledge layer that applications and workflows can consume |
| AgentSON | Typed execution and coordination events | Event/provenance layer for traceability and audit |
| Sand3D adapter | Programmatic, editable 3D generation and example-data patterns | Optional geometry authoring and reference-pattern source |
| CadFlow adapter | Deterministic OpenCascade B-rep construction, measurement and export | Optional exact-geometry and validation engine; not a required AK Build dependency |

## Why this separation matters

AK Build should remain useful to someone building an ordinary booking SaaS, internal portal, workflow application or AI-enabled service. It must not require product CAD or 3D reconstruction.

The Lab develops specialist capabilities that AK Build may selectively use when a project needs them. For example, an application could ingest a product's public evidence, maintain a structured component record, expose a browser-based model viewer and record validation decisions. That is an optional engineering workflow, not the definition of every AK Build project.

## Reusable capability boundary

Potential reusable interfaces include:

- Versioned schemas for products, components, requirements and evidence.
- Provenance records linking a value to a source and confidence classification.
- Tool adapters that record versions, parameters, inputs and generated outputs.
- Exportable engineering artefacts and browser visualisations.
- Validation reports and human approval checkpoints.

The Lab publishes research findings and reference implementations. AK Build may consume stable interfaces or separately licensed modules. Proprietary product implementation details, customer-specific integrations, private prompts, operational playbooks and unreleased commercial capabilities do not need to be published in this repository.

## Geometry adapter boundary

Sand3D and CadFlow solve different problems. Sand3D provides an LLM-friendly 3D-as-code language and a large set of programmatic examples. CadFlow is a Python CAD SDK over OpenCascade for deterministic B-rep construction, topology inspection, measurement and STEP/STL/GLB export. The Lab keeps them behind separate adapters: Sand3D is useful for authoring patterns and visual assets; CadFlow is the geometry-grounded CAD path. Neither supplies missing product measurements.

Every adapter records its exact version or source commit, input parameters, evidence links, generated files and validation output. Third-party dataset rows must retain row-level source licences and attribution. Do not assume undocumented APIs or make either engine a mandatory AK Build dependency.

Principles: stable identifiers, explicit schema versions, open interchange formats, CAD/model adapters, human review, customer-owned data and reproducible runs.

## Non-goals

- Turning AK Build into a CAD-only platform.
- Claiming generated geometry is automatically manufacturing-ready.
- Treating a patent drawing as an exact retail product model.
- Making any single model provider, harness or 3D generation engine a mandatory dependency.
