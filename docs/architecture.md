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
| Sand3D | Canonical modelling, named assembly hierarchy, joint semantics and generated exports for the Nyfasi case study | Active engineering engine for this experiment; not a required AK Build dependency |
| CadFlow | Historical OpenCascade B-rep and STEP exploration | Retained for reference; not part of the active Nyfasi build or publication path |

## Sand3D is a first-class engineering capability

Sand3D is the canonical modelling and semantic assembly engine for the active Nyfasi case study, not merely a source of example meshes or a viewer adapter. Its Python programs describe named parts, editable modelling operations, materials, local frames, joints and assembly hierarchy. The same source program generates the complete GLB, URDF, USDA, OBJ and STL representations used by this experiment. The browser gallery reads the complete articulated GLB and highlights the exact Python functions that create selected components.

The Hugging Face collections are an active research corpus. Retrieve actual program bodies for few-shot authoring, component decomposition, operation selection, joint reasoning and benchmark evaluation. The metadata catalogue is an index, not a substitute for using the programs. Preserve row-level source licences, attribution and hashes.

The Nyfasi benchmark runs the real Sand3D source in isolated workspaces after controlled parameter edits. It checks declared geometric relationships, regenerated exports and URDF joint semantics. Its next track will evaluate an AI agent receiving natural-language engineering change requests and proposing constraint-preserving program edits.

CadFlow was explored as an independent OpenCascade B-rep and STEP path. It is retained as historical research, not as a second active Nyfasi modelling authority. Sand3D is Blender mesh/scene based, not a B-rep kernel, and does not provide STEP export or OpenCascade topology checks. The decision to use one active Sand3D stack prioritises a coherent source-to-assembly-to-viewer chain over parallel CAD capabilities. If STEP/B-rep becomes a delivery requirement, the architecture decision must be revisited rather than implying Sand3D already supplies those capabilities.

The Lab owns the evidence, shared parameter contract, uncertainty, constraints, evaluation and human approval. AK Build may productise this as a specialist workflow: evidence intake → product graph → Sand3D authoring → geometry and articulation checks → CadFlow validation → approval → viewer or engineering report. Ordinary micro-SaaS projects do not need this specialist stack.

## Why this separation matters

AK Build should remain useful to someone building an ordinary booking SaaS, internal portal, workflow application or AI-enabled service. It must not require product CAD or 3D reconstruction.

The Lab develops specialist capabilities that AK Build may selectively use when a project needs them. For example, an application could ingest a product's public evidence, maintain a structured component record, expose a browser-based model viewer and record validation decisions. That is an optional engineering workflow, not the definition of every AK Build project. The Nyfasi experiment uses Sand3D end-to-end for its active geometry and assembly path; that project decision does not make Sand3D a mandatory dependency for AK Build.

## Reusable capability boundary

Potential reusable interfaces include:

- Versioned schemas for products, components, requirements and evidence.
- Provenance records linking a value to a source and confidence classification.
- Tool adapters that record versions, parameters, inputs and generated outputs.
- Exportable engineering artefacts and browser visualisations.
- Validation reports and human approval checkpoints.

The Lab publishes research findings and reference implementations. AK Build may consume stable interfaces or separately licensed modules. Proprietary product implementation details, customer-specific integrations, private prompts, operational playbooks and unreleased commercial capabilities do not need to be published in this repository.

## Geometry adapter boundary

Sand3D and CadFlow solve different problems, but only Sand3D is active in the Nyfasi reconstruction. Sand3D provides an LLM-friendly 3D-as-code language, named assembly groups, joints and GLB/URDF/USDA/OBJ/STL exports. CadFlow is a Python CAD SDK over OpenCascade for deterministic B-rep construction, topology inspection, measurement and STEP exchange; its Nyfasi work is historical and is not silently mixed into the current build. Neither engine supplies missing product measurements.

Every adapter records its exact version or source commit, input parameters, evidence links, generated files and validation output. Third-party dataset rows must retain row-level source licences and attribution. Do not assume undocumented APIs or make either engine a mandatory AK Build dependency.

Principles: stable identifiers, explicit schema versions, open interchange formats, CAD/model adapters, human review, customer-owned data and reproducible runs.

## Non-goals

- Turning AK Build into a CAD-only platform.
- Claiming generated geometry is automatically manufacturing-ready.
- Treating a patent drawing as an exact retail product model.
- Making any single model provider, harness or 3D generation engine a mandatory AK Build dependency. The Nyfasi case study has its own explicit Sand3D engine decision.
