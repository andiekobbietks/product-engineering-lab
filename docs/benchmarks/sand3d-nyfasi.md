# Sand3D Engineering Intelligence Benchmark

<div class="nyfasi-hero" markdown="1">
<div class="nyfasi-eyebrow">PRODUCT ENGINEERING LAB · BENCHMARK 001 · SAND3D 1.6.2</div>

# From editable 3D programs to constraint-aware engineering

A multi-part hair-applicator mechanism is our first test case. The benchmark changes real program parameters, regenerates the assembly through Sand3D, and checks whether declared geometric relationships and articulation survive.

<div class="nyfasi-actions">
  <a class="nyfasi-button primary" href="../experiments/assembly-explorer/">Open the 3D assembly explorer ↗</a>
  <a class="nyfasi-button" href="https://github.com/andiekobbietks/product-engineering-lab/tree/main/experiments/001-nyfasi-reconstruction">Explore source and benchmark ↗</a>
</div>
</div>

<div class="nyfasi-metrics">
  <div><strong>100K</strong><span>Sand3D programmatic asset corpus, upstream claim</span></div>
  <div><strong>29</strong><span>Named B-rep components in companion CadFlow build</span></div>
  <div><strong>4</strong><span>Sand3D export formats exercised</span></div>
  <div><strong>4</strong><span>Benchmark scenarios in v0.1</span></div>
</div>

## Explore the mechanism

The interactive preview below provides orbit, component selection, wireframe and exploded-assembly controls. It starts with the schematic assembly; load the generated Sand3D GLB from the benchmark artefact to inspect the regenerated geometry.

<iframe src="../../experiments/assembly-explorer.html" title="Interactive Nyfasi mechanism assembly explorer" loading="lazy" style="width:100%;height:780px;border:0;border-radius:16px;background:#0b1020"></iframe>

## Live benchmark result

<div id="benchmark-status" class="benchmark-status">Loading the latest CI benchmark report…</div>
<div id="benchmark-results" class="benchmark-results"></div>
<div id="benchmark-scope" class="benchmark-scope"></div>

<script>
(async function () {
  const status = document.getElementById("benchmark-status");
  const results = document.getElementById("benchmark-results");
  const scope = document.getElementById("benchmark-scope");
  try {
    const response = await fetch("../data/latest.json", { cache: "no-store" });
    if (!response.ok) throw new Error("No published benchmark report yet");
    const report = await response.json();
    status.innerHTML = '<span class="status-dot ' + (report.status === "passed" ? "good" : "bad") + '"></span><strong>' + report.status.toUpperCase() + '</strong><span>' + report.scenarios_passed + ' / ' + report.scenarios_total + ' scenarios passed</span><span>Sand3D ' + report.engine_version + ' · benchmark ' + report.benchmark_version + '</span>';
    results.innerHTML = report.results.map(function (item) {
      const ok = item.status === "passed";
      const detail = item.mutations ? Object.entries(item.mutations).map(function (entry) { return entry[0] + ': ' + entry[1]; }).join(' · ') : (item.expected_rejection ? 'Invalid edit rejected before geometry generation' : 'Unmodified parameter baseline');
      return '<article class="benchmark-row"><div class="row-state ' + (ok ? 'good' : 'bad') + '">' + (ok ? 'PASS' : 'FAIL') + '</div><div><strong>' + item.scenario.replaceAll('_',' ') + '</strong><p>' + detail + '</p>' + (item.reason ? '<small>' + item.reason + '</small>' : '') + '</div><div class="row-meta">' + (item.geometry_output_changed ? 'Geometry changed' : (item.joint ? item.joint.type + ' joint verified' : 'Constraint gate')) + '</div></article>';
    }).join('');
    scope.innerHTML = '<p><strong>Scope:</strong> ' + report.scope + '</p><p><strong>Not claimed:</strong> ' + report.not_claimed.join(' · ') + '</p><p>Parameter ledger SHA-256: <code>' + report.baseline_parameter_sha256 + '</code></p>';
  } catch (error) {
    status.textContent = error.message + '. The first report is published by the benchmark GitHub Actions workflow.';
  }
})();
</script>

## What is being tested?

<div class="nyfasi-grid">
  <article><span class="step">01 / PROGRAM</span><h3>Editable source</h3><p>Named Sand3D functions describe the housing, reservoir, roller, textured bands, end walls, spindle pins, bearing supports, comb teeth, gasket and retention features.</p></article>
  <article><span class="step">02 / PARAMETRICS</span><h3>Controlled edits</h3><p>Change the roller diameter and housing width in the parameter ledger. The actual Sand3D program runs again in an isolated workspace for each scenario.</p></article>
  <article><span class="step">03 / CONSTRAINTS</span><h3>Preserved intent</h3><p>Check radial seat clearance, core-to-roller ordering, wall and tooth span, band spacing, spindle/bearing fit, housing envelope and the roller joint axis.</p></article>
  <article><span class="step">04 / REGENERATION</span><h3>Real outputs</h3><p>Export GLB, OBJ, URDF and USDA. The benchmark checks that geometry exports change after a valid parameter edit and that the continuous +X roller joint remains represented in URDF.</p></article>
</div>

## The first controlled edit tasks

| Scenario | Edit | Expected invariant |
|---|---|---|
| Baseline | No change | Reference assembly builds and exports |
| Roller diameter +2 mm | Increase roller OD by 2 mm; move tooth-root datum by 1 mm | Radial seat clearance, wall relationship and roller axis remain valid |
| Housing width +10 mm | Increase housing envelope | Bearing supports remain inside the housing |
| Invalid roller diameter | Set roller OD below the smooth core | Constraint gate rejects the edit before Sand3D runs |

The first roller-diameter change is an AI-authored engineering proposal, recorded with its natural-language request, parameter patch, rationale and expected invariants. The benchmark executes that proposal through the real Sand3D program and independent constraint checks. This is a reproducible single-agent fixture, **not yet a blind or comparative evaluation of autonomous model reasoning**. The next evaluation track will let an agent receive unseen change requests, propose patches without access to expected values, explain affected constraints and pass or fail against the same evaluator.

## How the representations work together

~~~mermaid
flowchart LR
 E[Evidence and parameter ledger] --> S[Sand3D editable program]
 D[Hugging Face Sand3D examples] --> R[Rights-aware retrieval]
 R --> S
 S --> G[GLB / OBJ / URDF / USDA]
 E --> C[CadFlow B-rep builder]
 C --> T[STEP / topology / dimensions]
 G --> V[Scene and articulation checks]
 T --> V
 V --> H[Engineering review]
~~~

Sand3D is the semantic, editable program and assembly layer. The Hugging Face collections provide program examples for retrieval and evaluation. CadFlow is an independent OpenCascade B-rep path for exact-solid inspection and STEP exchange. The engines must share a parameter contract; neither should become an independently hard-coded version of the product.

## Inspect the model

- [Open the interactive assembly explorer](../experiments/assembly-explorer/). Load the individual GLB files from a benchmark artifact or use the exploded preview.
- [Download benchmark artefacts from GitHub Actions](https://github.com/andiekobbietks/product-engineering-lab/actions/workflows/sand3d-nyfasi-benchmark.yml).
- [Read the Nyfasi parameter and evidence ledger](https://github.com/andiekobbietks/product-engineering-lab/tree/main/experiments/001-nyfasi-reconstruction/models).
- [Read the Sand3D dataset retrieval strategy](../experiments/sand3d-dataset-strategy/).

## Benchmark integrity and limitations

This is a procedural engineering-intelligence benchmark, not proof that the generated model matches a Nyfasi retail product. Most housing, reservoir, retention and fit dimensions remain assumptions. The current test suite checks selected declared relationships and file regeneration; it does not establish manufacturing tolerances, material properties, seal compression, fatigue, physical interference, or contact mechanics.

A passing result means that this particular program accepted the declared edits, regenerated outputs, and preserved the selected machine-checkable constraints. It does not certify the design.

<style>
.nyfasi-hero{padding:clamp(26px,5vw,58px);border-radius:22px;background:linear-gradient(130deg,#101c2c,#172d3e 58%,#244d50);color:#f5f7fa;margin:12px 0 22px}
.nyfasi-hero h1{font-size:clamp(2rem,5vw,3.65rem);line-height:1.03;letter-spacing:-.045em;max-width:850px;margin:14px 0}
.nyfasi-hero p{font-size:1.08rem;max-width:760px;color:#cbd8df}
.nyfasi-eyebrow,.step{font-size:.72rem;letter-spacing:.13em;font-weight:800;color:#a7d8ca}
.nyfasi-actions{display:flex;gap:10px;flex-wrap:wrap;margin-top:24px}
.nyfasi-button{display:inline-block;padding:11px 16px;border:1px solid #9bb7bb;border-radius:9px;color:#f6fbfa!important;text-decoration:none!important;font-weight:700}
.nyfasi-button.primary{background:#b9e5d6;color:#10232b!important;border-color:#b9e5d6}
.nyfasi-metrics{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:10px;margin:18px 0 32px}
.nyfasi-metrics>div{padding:17px;border:1px solid var(--md-default-fg-color--lightest);border-radius:12px;background:var(--md-code-bg-color)}
.nyfasi-metrics strong{display:block;font-size:1.8rem;letter-spacing:-.04em}
.nyfasi-metrics span{display:block;font-size:.78rem;color:var(--md-default-fg-color--light)}
.benchmark-status{display:flex;align-items:center;gap:12px;flex-wrap:wrap;padding:15px 17px;border:1px solid var(--md-default-fg-color--lightest);border-radius:12px;margin:12px 0}
.status-dot{width:10px;height:10px;border-radius:50%;display:inline-block}.status-dot.good{background:#27ae78}.status-dot.bad{background:#d45b5b}
.benchmark-results{display:grid;gap:8px}
.benchmark-row{display:grid;grid-template-columns:60px minmax(0,1fr) minmax(120px,auto);gap:12px;align-items:center;border:1px solid var(--md-default-fg-color--lightest);padding:13px;border-radius:10px}
.row-state{font-size:.72rem;font-weight:900}.row-state.good{color:#21956a}.row-state.bad{color:#d45b5b}.benchmark-row p{margin:3px 0 0;color:var(--md-default-fg-color--light);font-size:.85rem}.benchmark-row small{color:#c56b56}.row-meta{font-size:.76rem;color:var(--md-default-fg-color--light);text-align:right}
.benchmark-scope{font-size:.82rem;color:var(--md-default-fg-color--light);margin:12px 0 28px;overflow-wrap:anywhere}
.nyfasi-grid{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:12px;margin:20px 0}
.nyfasi-grid article{border:1px solid var(--md-default-fg-color--lightest);border-radius:12px;padding:18px;background:var(--md-code-bg-color)}
.nyfasi-grid h3{margin:8px 0}.nyfasi-grid p{font-size:.9rem;color:var(--md-default-fg-color--light)}
@media(max-width:650px){.nyfasi-metrics{grid-template-columns:repeat(2,minmax(0,1fr))}.nyfasi-grid{grid-template-columns:1fr}.benchmark-row{grid-template-columns:48px 1fr}.row-meta{grid-column:2;text-align:left}}
</style>
